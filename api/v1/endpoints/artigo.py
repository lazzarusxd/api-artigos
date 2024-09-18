"""
Módulo de rotas para gerenciamento de artigos.
Este módulo define as rotas para criação, leitura, atualização e exclusão de artigos.

Rotas:

- POST /: Cria um novo artigo.
- GET /: Retorna uma lista de artigos.
- GET /{artigo_id}: Retorna um artigo específico pelo ID.
- PUT /{artigo_id}: Atualiza um artigo existente pelo ID.
- DELETE /{artigo_id}: Remove um artigo pelo ID.
"""

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema, ArtigoSchemaUp
from core.deps import get_session, get_current_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema,
                      usuario_logado: UsuarioModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session)) -> ArtigoSchema:
    """
    Cria um novo artigo.

    :param artigo: Dados do novo artigo.
    :param usuario_logado: Usuário autenticado que está criando o artigo.
    :param db: Sessão do banco de dados.

    :return: O artigo recém-criado.
    """
    novo_artigo = ArtigoModel(titulo=artigo.titulo,
                              descricao=artigo.descricao,
                              url_fonte=str(artigo.url_fonte),
                              usuario_id=usuario_logado.id)
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo


@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)) -> List[ArtigoSchema]:
    """
    Retorna uma lista de artigos.

    :param db: Sessão do banco de dados.

    :return: Lista de artigos.
    """
    query = select(ArtigoModel)
    result = await db.execute(query)
    artigos = list(result.scalars().unique().all())
    return artigos


@router.get("/{artigo_id}", response_model=ArtigoSchema)
async def get_artigo(artigo_id: int,
                     db: AsyncSession = Depends(get_session)) -> ArtigoSchema:
    """
    Retorna um artigo específico pelo ID.

    :param artigo_id: ID do artigo a ser recuperado.
    :param db: Sessão do banco de dados.

    :return: O artigo correspondente ao ID fornecido.

    :raises HTTPException: Se o artigo não for encontrado (HTTP 404).
    """
    query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    result = await db.execute(query)
    artigo = result.scalars().unique().one_or_none()

    if artigo:
        return artigo
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado."
        )


@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int,
                     artigo_atualizado: ArtigoSchemaUp,
                     db: AsyncSession = Depends(get_session),
                     usuario_logado: UsuarioModel = Depends(get_current_user)) -> ArtigoSchema:
    """
    Atualiza um artigo existente pelo ID.

    :param artigo_id: ID do artigo a ser atualizado.
    :param artigo_atualizado: Dados atualizados do artigo.
    :param db: Sessão do banco de dados.
    :param usuario_logado: Usuário autenticado que está atualizando o artigo.

    :return: O artigo atualizado.

    :raises HTTPException: Se o usuário não for o criador do artigo (HTTP 401) ou se o artigo não existir (HTTP 404).
    """
    query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    result = await db.execute(query)
    artigo = result.scalars().unique().one_or_none()

    if artigo:
        if usuario_logado.id != artigo.usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Somente o criador pode atualizar o artigo."
            )
        if artigo_atualizado.titulo:
            artigo.titulo = artigo_atualizado.titulo
        if artigo_atualizado.descricao:
            artigo.descricao = artigo_atualizado.descricao
        if artigo_atualizado.url_fonte:
            artigo.url_fonte = str(artigo_atualizado.url_fonte)

        await db.commit()
        return artigo
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado."
        )


@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int,
                        db: AsyncSession = Depends(get_session),
                        usuario_logado: UsuarioModel = Depends(get_current_user)) -> JSONResponse:
    """
    Remove um artigo pelo ID.

    :param artigo_id: ID do artigo a ser removido.
    :param db: Sessão do banco de dados.
    :param usuario_logado: Usuário autenticado que está removendo o artigo.

    :return: Mensagem de sucesso se o artigo for removido.

    :raises HTTPException: Se o usuário não for o criador do artigo (HTTP 401) ou se o artigo não existir (HTTP 404).
    """
    query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
    result = await db.execute(query)
    artigo = result.scalars().unique().one_or_none()

    if artigo:
        if artigo.usuario_id != usuario_logado.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Somente o criador pode deletar o artigo."
            )
        await db.delete(artigo)
        await db.commit()
        return JSONResponse(
            content={"message": "Exclusão feita com sucesso."},
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado."
        )
