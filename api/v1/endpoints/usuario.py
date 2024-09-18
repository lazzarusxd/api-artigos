"""
Módulo de rotas para gerenciamento de usuários.
Define as rotas para criação, leitura, atualização e exclusão de usuários, bem como autenticação.

Rotas:

- GET /logado: Retorna o usuário autenticado.
- POST /signup: Cria um novo usuário.
- GET /: Retorna uma lista de usuários.
- GET /{usuario_id}: Retorna um usuário específico pelo ID.
- PUT /{usuario_id}: Atualiza um usuário existente pelo ID.
- DELETE /{usuario_id}: Remove um usuário pelo ID.
- POST /login: Autentica um usuário e retorna um token de acesso.
"""

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaArtigos
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()


@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)) -> UsuarioSchemaBase:
    """
    Retorna o usuário autenticado.

    :param usuario_logado: Usuário autenticado.

    :return: Dados do usuário autenticado.
    """
    return usuario_logado


@router.post("/signup", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)) -> UsuarioSchemaBase:
    """
    Cria um novo usuário.

    :param usuario: Dados do novo usuário.
    :param db: Sessão do banco de dados.

    :return: O usuário recém-criado.

    :raises HTTPException: Se já existir um usuário com o e-mail fornecido (HTTP 406).
    """
    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        admin=usuario.admin
    )
    try:
        db.add(novo_usuario)
        await db.commit()
        return novo_usuario
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Já existe um usuário com esse e-mail cadastrado."
        )


@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuario(db: AsyncSession = Depends(get_session)) -> List[UsuarioSchemaBase]:
    """
    Retorna uma lista de usuários.

    :param db: Sessão do banco de dados.

    :return: Lista de usuários.
    """
    async with db:
        query = select(UsuarioModel)
        result = await db.execute(query)
        usuarios = list(result.scalars().unique().all())
        return usuarios


@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)) -> UsuarioSchemaArtigos:
    """
    Retorna um usuário específico pelo ID.

    :param usuario_id: ID do usuário a ser recuperado.
    :param db: Sessão do banco de dados.

    :return: O usuário correspondente ao ID fornecido.

    :raises HTTPException: Se o usuário não for encontrado (HTTP 404).
    """
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuario = result.scalars().unique().one_or_none()

    if usuario:
        return usuario
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )


@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int,
                      usuario_atualizado: UsuarioSchemaUp,
                      db: AsyncSession = Depends(get_session)) -> UsuarioSchemaBase:
    """
    Atualiza um usuário existente pelo ID.

    :param usuario_id: ID do usuário a ser atualizado.
    :param usuario_atualizado: Dados atualizados do usuário.
    :param db: Sessão do banco de dados.

    :return: O usuário atualizado.

    :raises HTTPException: Se o usuário não existir (HTTP 404).
    """
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuario = result.scalars().unique().one_or_none()

    if usuario:
        if usuario_atualizado.nome is not None:
            usuario.nome = usuario_atualizado.nome
        if usuario_atualizado.sobrenome is not None:
            usuario.sobrenome = usuario_atualizado.sobrenome
        if usuario_atualizado.email is not None:
            usuario.email = usuario_atualizado.email
        if usuario_atualizado.admin is not None:
            usuario.admin = usuario_atualizado.admin
        if usuario_atualizado.senha is not None:
            usuario.senha = gerar_hash_senha(usuario_atualizado.senha)

        await db.commit()
        return usuario
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Remove um usuário pelo ID.

    :param usuario_id: ID do usuário a ser removido.
    :param db: Sessão do banco de dados.

    :return: Mensagem de sucesso se o usuário for removido.

    :raises HTTPException: Se o usuário não existir (HTTP 404).
    """
    query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
    result = await db.execute(query)
    usuario = result.scalars().unique().one_or_none()

    if usuario:
        await db.delete(usuario)
        await db.commit()
        return JSONResponse(
            content={"message": "Exclusão feita com sucesso."},
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Autentica um usuário e retorna um token de acesso.

    :param form_data: Dados de autenticação (usuário e senha).
    :param db: Sessão do banco de dados.

    :return: Token de acesso e tipo de token (bearer).

    :raises HTTPException: Se os dados de acesso estiverem incorretos (HTTP 400).
    """
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados de acesso incorretos."
        )

    return JSONResponse(
        content={
            "access_token": criar_token_acesso(sub=usuario.id),
            "token_type": "bearer"
        },
        status_code=status.HTTP_200_OK
    )
