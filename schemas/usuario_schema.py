from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    """
    Schema base para representar os dados de um usuário.

    Utilizado como base para outros schemas de usuário, contendo os campos essenciais para um usuário no sistema.

    Atributos:

    - "id" (int, opcional): Identificador único do usuário.
    - "nome" (str): Nome do usuário.
    - "sobrenome" (str): Sobrenome do usuário.
    - "email" (EmailStr): Endereço de e-mail do usuário.
    - "admin" (bool): Indica se o usuário possui privilégios administrativos.
    """

    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        """
        Configurações da classe "UsuarioSchemaBase".

        Atributos:

        - "from_attributes" (bool): Permite a criação de instâncias do schema a partir de objetos do SQLAlchemy.
        """
        from_attributes = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    """
    Schema utilizado para a criação de um novo usuário.

    Herda os campos do "UsuarioSchemaBase", adicionando o campo de senha para a criação de novos usuários.

    Atributos:

    - "senha" (str): Senha do usuário.
    """

    senha: str


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    """
    Schema utilizado para representar um usuário junto com os artigos que ele criou.

    Herda os campos do "UsuarioSchemaBase" e adiciona uma lista de artigos criados pelo usuário.

    Atributos:

    - "artigos" (List[ArtigoSchema], opcional): Lista de artigos criados pelo usuário.
    """

    artigos: Optional[List[ArtigoSchema]] = None


class UsuarioSchemaUp(UsuarioSchemaBase):
    """
    Schema utilizado para atualização parcial de um usuário.

    Herda os campos do "UsuarioSchemaBase", mas os campos são opcionais para facilitar atualizações parciais.

    Atributos:

    - "nome" (str, opcional): Nome do usuário (opcional para atualização).
    - "sobrenome" (str, opcional): Sobrenome do usuário (opcional para atualização).
    - "email" (str, opcional): Endereço de e-mail do usuário (opcional para atualização).
    - "senha" (str, opcional): Senha do usuário (opcional para atualização).
    - "admin" (bool, opcional): Privilégios administrativos (opcional para atualização).
    """

    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    admin: Optional[bool] = None
