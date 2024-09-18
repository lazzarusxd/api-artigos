from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='API - Gerenciamento de Artigos')
"""
Instancia a aplicação FastAPI com o título 'API - Gerenciamento de Artigos'.

Inclui o roteador de endpoints, definindo um prefixo de rota com base
na configuração "API_V1_STR", para organizar as rotas da API.

:param title: O título da aplicação.
:param include_router: Adiciona um roteador de rotas da API.
"""
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, log_level='debug', reload=True)
