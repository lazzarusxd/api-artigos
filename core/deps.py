"""
Módulo de dependências para o FastAPI.
Fornece funções auxiliares para obter a sessão do banco de dados e o usuário atual a partir do token de autenticação.

Classes:

- "TokenData": Modelo de dados para armazenar informações sobre o token JWT.

Funções:

- "get_session": Fornece uma sessão assíncrona do banco de dados.
- "get_current_user": Recupera o usuário autenticado com base no token JWT fornecido.
"""

from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from .database import async_session_local
from .auth import oauth2_schema
from .configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fornece uma sessão assíncrona do banco de dados.

    :return: Um gerador que fornece uma sessão assíncrona para interações com o banco de dados.
    """
    async with async_session_local() as session:
        yield session


async def get_current_user(
        db: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_schema)) -> UsuarioModel:
    """
    Recupera o usuário autenticado com base no token JWT fornecido.

    :param db: Sessão assíncrona do banco de dados.
    :param token: Token JWT fornecido pelo cliente para autenticação.

    :return: O usuário autenticado.

    :raises HTTPException: Se a autenticação falhar ou o usuário não for encontrado (HTTP 401).
    """
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))
    result = await db.execute(query)
    usuario: UsuarioModel = result.scalars().unique().one_or_none()

    if usuario is None:
        raise credential_exception

    return usuario
