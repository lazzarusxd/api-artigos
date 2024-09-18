"""
Módulo de configuração da aplicação.
Define as configurações da aplicação usando o Pydantic para validação e gerenciamento de configurações.

Configurações:

- API_V1_STR: String de prefixo para a versão da API.
- DB_URL: URL de conexão com o banco de dados.
- JWT_SECRET: Segredo para geração de tokens JWT.
- ALGORITHM: Algoritmo de criptografia para tokens JWT.
- ACCESS_TOKEN_EXPIRE_MINUTES: Tempo de expiração dos tokens de acesso em minutos.
"""

from pydantic import BaseModel


class Settings(BaseModel):
    """
    #Classe que define as configurações da aplicação.
    """

    API_V1_STR: str = '/api/v1'
    """
    Prefixo para a versão da API.
    """

    DB_URL: str = 'postgresql+asyncpg://lazzarus:lazaro123@localhost:5432/faculdade'
    """
    URL de conexão com o banco de dados PostgreSQL usando asyncpg.
    """

    JWT_SECRET: str = 'w7PQnn5XdHs14ltivJ3g8r_MirZiR4jb1KEV4sVNdSw'
    """
    Segredo para geração de tokens JWT.

    Para gerar um novo segredo:
    - No terminal Python, execute:
          python
          import secrets
          token = secrets.token_urlsafe(32)
          token
    """

    ALGORITHM: str = 'HS256'
    """
    Algoritmo de criptografia para tokens JWT.
    """

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    """
    Tempo de expiração dos tokens de acesso em minutos (7 dias).
    """

    class Config:
        """
        Configurações adicionais para a classe Settings.
        """
        case_sensitive = True


settings: Settings = Settings()
"""
Instância da classe Settings que carrega as configurações da aplicação.
"""
