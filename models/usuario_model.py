from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import base


class UsuarioModel(base):
    """
    Modelo de usuário para o banco de dados.
    Representa um usuário no sistema, definindo os atributos e relacionamentos associados a um usuário.

    Tabela "usuarios":

    - "id" (int): Identificador único do usuário.
    - "nome" (str): Nome do usuário.
    - "sobrenome" (str): Sobrenome do usuário.
    - "email" (str): Endereço de e-mail do usuário, que deve ser único.
    - "senha" (str): Hash da senha do usuário.
    - "senha" (str): Hash da senha do usuário.

    Relacionamentos:

    - "artigos": Relacionamento com o modelo "ArtigoModel", onde um usuário pode ter múltiplos artigos associados.
    """

    __tablename__ = 'usuarios'

    # Atributos da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=True)
    sobrenome = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    senha = Column(String(256), nullable=False)
    admin = Column(Boolean, default=False)

    # Relacionamento com "ArtigoModel"
    artigos = relationship(
        "ArtigoModel",
        cascade="all, delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )
