"""
Módulo de configuração do banco de dados.
Configura a conexão com o banco de dados, o motor de banco de dados assíncrono e a fábrica de sessões assíncronas.

Objetos:

- "engine": Motor de banco de dados assíncrono para comunicação com o banco de dados.
- "base": Base declarativa para a criação de modelos ORM.
- "async_session_local": Fábrica de sessões assíncronas para interações com o banco de dados.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from .configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL, future=True, echo=True)
"""
Motor de banco de dados assíncrono criado usando a URL de conexão fornecida nas configurações.

:param settings.DB_URL: URL de conexão com o banco de dados.
"""

base = declarative_base()
"""
Base declarativa usada para criar modelos ORM.
"""

async_session_local = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)
"""
Fábrica de sessões assíncronas para interações com o banco de dados.

:param bind: Motor de banco de dados ao qual a fábrica de sessões está associada.
:param autoflush: Desativa o flush automático de mudanças na sessão.
:param autocommit: Desativa o commit automático de transações.
:param expire_on_commit: Desativa a expiração automática de objetos após o commit.
:param class_: Classe de sessão a ser usada (AsyncSession).
"""
