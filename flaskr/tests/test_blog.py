import pytest
from flaskr.db import get_db
"""
    NA Maioria das rotas em `blog` vai precisar de as funcionalidades
de autenticacão 'auth' 
"""


def test_index(client, auth):
    """
        Na rota root 'index' é disponibilizado posts recentes
    se o usuário ñ estiver  logado   deve  estar  disponível
    links para  registrar  um  novo ou logar em um existente.
        Após usuário logado deve estar disponível link para
    deslogar e editar seus posts no blog

    :param client: Proxy para a fixeture client
    :param auth: Proxy para a fixeture auth
    :return: aifrmacões de testes
    """

    response = client.get('/')  # buscando página index sem usuário logado
    assert b'Log In' in response.data  # Afirmando link para logar usuário
    assert b'Register' in response.data  # Afirmando link para registrar novo usuário

    auth.login()  # Logando usuário de teste
    response = client.get('/')  # Buscando página index com usuário logado

    response = client.get('/')
    assert b'Log Out' in response.data  # Afirmando link para saída
    assert b'test title' in response.data  # Dados para testes contidos em post no blog
    assert b'by test on 2018-01-01' in response.data  # Dados para testes contidos em post no blog
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data  # Link para edita posts do usuário no blog
