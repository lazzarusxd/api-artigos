"""
Módulo de autenticação e gerenciamento de tokens.
Fornece funções para autenticar usuários e criar tokens JWT para autenticação.

Funções:

- autenticar: Verifica as credenciais de um usuário.
- criar_token_acesso: Cria um token de acesso JWT para um usuário.
"""

from typing import Optional
from pytz import timezone
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel
from .configs import settings
from .security import verificar_senha
from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    """
    Verifica as credenciais de um usuário.

    :param email: Endereço de e-mail do usuário.
    :param senha: Senha do usuário.
    :param db: Sessão do banco de dados.

    :return: O usuário autenticado se as credenciais estiverem corretas, caso contrário, retorna None.
    """
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None

        return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    """
    Cria um token JWT.

    :param tipo_token: Tipo do token (exemplo: 'access_token').
    :param tempo_vida: Tempo de validade do token.
    :param sub: Identificador do assunto (usuário).

    :return: O token JWT codificado.
    """
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3 (parâmetros de payload)
    payload = {
        "type": tipo_token,
        "exp": expira,
        "iat": datetime.now(tz=sp),
        "sub": str(sub)
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    Cria um token de acesso JWT para um usuário.

    :param sub: Identificador do usuário.

    :return: O token de acesso JWT codificado.
    """
    # https://jwt.io (verifica a validade da assinatura)
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
