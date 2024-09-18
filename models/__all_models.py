"""
Módulo que importa e expõe todos os modelos utilizados na aplicação.
Agrupa os modelos "ArtigoModel" e "UsuarioModel" para facilitar o acesso a eles em outros módulos.

Modelos Importados:

- "ArtigoModel": Modelo de dados para representar artigos.
- "UsuarioModel": Modelo de dados para representar usuários.
"""

from .artigo_model import ArtigoModel
from .usuario_model import UsuarioModel
