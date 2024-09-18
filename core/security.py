"""
Módulo para operações relacionadas à segurança, incluindo verificação e geração de hashes de senha.
Utiliza o `passlib` para gerenciar a criptografia de senhas.

Funções:

- "verificar_senha": Verifica se uma senha fornecida corresponde ao hash armazenado.
- "gerar_hash_senha": Gera um hash para uma senha fornecida.
"""

from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    :param senha: Senha fornecida pelo usuário em texto puro.
    :param hash_senha: Hash da senha armazenado no banco de dados.

    :return: Retorna "True" se a senha corresponder ao hash fornecido e "False" caso contrário.
    """
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash para a senha fornecida.

    :param senha: Senha fornecida pelo usuário.

    :return: Retorna o hash gerado para a senha.
    """
    return CRIPTO.hash(senha)
