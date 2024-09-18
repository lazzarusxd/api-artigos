from core.database import engine, base


async def create_tables() -> None:
    """
    Função assíncrona para criar as tabelas no banco de dados.

    Esta função importa todos os modelos de tabelas do diretório de modelos
    e utiliza o engine do SQLAlchemy para se conectar ao banco de dados.
    Ela remove todas as tabelas existentes e cria novas tabelas de acordo
    com os modelos definidos.

    :return: None
    """
    import models.__all_models
    print("Criando as tabelas no banco de dados.")
    async with engine.begin() as conn:
        # Remove todas as tabelas existentes no banco de dados
        await conn.run_sync(base.metadata.drop_all)
        # Cria as tabelas definidas pelos modelos
        await conn.run_sync(base.metadata.create_all)
    print("Tabelas criadas com sucesso...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
