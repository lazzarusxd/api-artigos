"""
Módulo de roteamento da API.
Define o roteamento principal para a API, incluindo os endpoints de artigos e usuários.

Roteadores:

- /artigos: Roteador para as rotas relacionadas a artigos.
- /usuarios: Roteador para as rotas relacionadas a usuários.
"""

from fastapi import APIRouter
from .endpoints import artigo, usuario

api_router = APIRouter()

# Inclui as rotas do módulo "artigo" sob o prefixo "/artigos".
api_router.include_router(artigo.router, prefix="/artigos", tags=["Artigos"])

# Inclui as rotas do módulo "usuario" sob o prefixo "/usuarios".
api_router.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"])
