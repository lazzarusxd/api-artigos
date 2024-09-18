from typing import Optional
from pydantic import BaseModel, HttpUrl


class ArtigoSchema(BaseModel):
    """
    Schema para representar os dados de um artigo.
    Utilizado para validação e serialização dos dados de um artigo no sistema.

    Atributos:

    - "id" (int, opcional): Identificador único do artigo.
    - "titulo" (str): Título do artigo.
    - "descricao" (str): Descrição do artigo.
    - "url_fonte" (HttpUrl): URL da fonte do artigo.
    - "usuario_id" (int, opcional): Identificador do usuário que criou o artigo.
    - "senha" (str): Hash da senha do usuário.
    """
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[int] = None

    class Config:
        """
        Configurações da classe "ArtigoSchema".

        Atributos:

        - "from_attributes" (bool): Habilita a criação de instâncias do schema a partir de objetos do SQLAlchemy.
        """
        from_attributes = True


class ArtigoSchemaUp(ArtigoSchema):
    """
    Schema para atualização parcial dos dados de um artigo.

    Herda todos os campos do ArtigoSchema, porém os campos são opcionais para facilitar atualizações parciais.

    Atributos:

    - "titulo" (str, opcional): Título do artigo (opcional para atualizações).
    - "descricao" (str, opcional): Descrição do artigo (opcional para atualizações).
    - "url_fonte" (HttpUrl, opcional): URL da fonte do artigo (opcional para atualizações).
    """
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    url_fonte: Optional[HttpUrl] = None
