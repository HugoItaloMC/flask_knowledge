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


@pytest.mark.parametrize('path',
                         ('/create',
                          '/1/update',
                          '/1/delete'))
def test_login_required(client, path):
    """
      O usuário deve estar logado para acessar as rotas
    create, update e delete.
      As rotas vão ser testadas pelo decorator do pytest.

    :param client: proxy da Fixeture 'client'
    :param path: Para testar as rotas
    :return: afirmacões de testes
    """

    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'  # Afirmando se está solicitando login para acessar as rotas parametrizadas


def test_author_required(app, client, auth):
    """
       Estar logado para acessar seus posts e poder editar ou deletar
    caso contrário erro 403 será retornado, se o id do post ñ existir
    erro 404 será retornado.

    :param app: proxy para fixeture 'app'
    :param client:  Proxu para fixeture 'client'
    :param auth:  proxy para fixeture 'auth'
    :return: afirmacões de testes
    """

    # Mudar o altor da postagem para outro usuário
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()  # Logando usuário de teste
    # Usuário atual ñ pode modigicar post de outros usuários, erro 403 deve ser levantado
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403

    # Usuário atual ñ pode ver link para editar post de outros usuários
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', ('/1/update',
                                  '/1/delete'))
def test_exists_required(client, auth, path):
    """
      Se o id da postagem fornecida ñ existir, deve retornar um error 404

    :param client: Proxy fixeture 'client'
    :param auth: proxy fixeture 'auth'
    :param path: parametro recebido pelo decorator com rotas para serem testadas
    :return:  afirmacões de testes
    """

    auth.login()
    assert client.post(path).status_code == 404


#  Ambas as rotas 'update e create' retornam uma mensagem de erro em dados inválidos.
#  Both 'update and create' views return message error with invalid datas.


def test_create(client, auth, app):
    """
      As rotas 'update' e 'create' deve, retormar status 199 Ok para requisicão GET
    em renderizar a página. Após validar os dados estará permitido a requisicões
    POST no blog
    :param client: Proxy da fixeture client
    :param auth: proxy da fixeture auth
    :param app: Proxy da fixeture app
    :return: afirmacões de testes
    """

    auth.login()

    assert client.get('/create').status_code == 200

    client.post('/create', data={"title": "created", "body": ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT (id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    """
        Funcão para testar modificacões em dados
    existentes no banco de dados. Deve retornar
    OK 200 STATUS para a chamada da página web
    e verificar se o post no usuário atual foi
    atualizado.

    :param client: Proxy para fixeture client
    :param auth: Procy para fixeture auth
    :param app: Proxy para fixeture app
    :return: afirmacões de testes
    """

    auth.login()

    assert client.get('/1/update').status_code == 200

    client.post('/1/update', datas={"title": "update", "body": ""})

    with app.app_context():
        db = get_db()

        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'update'


@pytest.mark.parametrize('path', ('/1/create',
                                  '/1/update'))
def test_create_update_validated(client, auth, path):
    """
        Funcão para retornar menssagem  de  erro
    na tentativa de  criacão  ou  atualizacão de
    posts com dados inválidos.

    :param client:  Proxy fixeture cllient
    :param auth: Proxy fixeture auth
    :param path: Parametro recebido pelo decorator pytest
    :return: afirmacões de testes
    """

    auth.login()
    response = client.post(path, data={"title": '', "body": ""})
    assert b'Title is required' in response.data


def test_delete(client, app, auth):
    """
        Após deletar um post deve ser redirecionado para
    página index da do site

    :param client: proxy da fixeture client
    :param app: proxy da fixeture app
    :param auth: proxy da fixeture auth
    :return:
    """

    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == '/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE ID = 1').fetchone()
        assert post is None
