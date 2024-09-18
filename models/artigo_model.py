from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import base


class ArtigoModel(base):
    """
    Modelo de dados para representar um artigo na aplicação.
    Define a estrutura da tabela "artigos", incluindo suas colunas e relacionamentos com outros modelos.

    Tabela "artigos":

    - "id" (int): ID único do artigo. É a chave primária e é gerado automaticamente.
    - "titulo" (str): Título do artigo. Este campo é obrigatório e pode ter até 256 caracteres.
    - "descricao" (str): Descrição do artigo. Este campo é opcional e pode ter até 256 caracteres.
    - "url_fonte" (str): URL de origem do artigo. Este campo é opcional e pode ter até 256 caracteres.
    - "usuario_id" (int): ID do criador do artigo. O campo é obrigatório e é uma FK que referencia "usuarios.id".

    Relacionamentos:

    - "criador": Relaciona com o modelo "UsuarioModel", representando o usuário que criou o artigo.
    """

    __tablename__ = 'artigos'

    # Atributos da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256), nullable=False)
    descricao = Column(String(256))
    url_fonte = Column(String(256))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relacionamento com "UsuarioModel"
    criador = relationship("UsuarioModel", back_populates="artigos", lazy="joined")
