import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200  # Requisicões GET devem retornar status code 200 para renderizar a página

    # Requisicões POST o usuário deve estar logado
    response = client.post('/auth/register',
                           data={'username': 'a', 'password': 'a'})
    assert response.headers["Location"] == '/auth/login'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username == 'a' ",
        ).fetchone() is not None


# Chama Pytest para executatar diferentes testes, verificando diferentes tipos inválidos de entrada de dados
@pytest.mark.parametrize(('username', 'password', 'message'),
                         (('', '', b'Username is Required'),
                          ('a', '', b'Password is required'),
                          ('test', 'test', b'already redistered'),))
def test_register_validate_input(client, username, password, message):
    response = client.post('/auth/register', data={'username': username, 'password': password})
    assert message in response.data
