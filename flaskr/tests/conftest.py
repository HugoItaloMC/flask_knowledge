import os, tempfile, pytest

from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as filerr:
    # Instânciando DML como binário e decodificando e trazendo para chamada da pilha principal sua instância
    _data_sql = filerr.read().decode('utf8')

@pytest.fixture  # Fazendo a jogada de teste
def app():
    db_fb, db_path = tempfile.mkstemp()  # Substituir por pontos temporários para modo de teste da aplicacão

    app = create_app({
        'TESTING': True,  # Passando pro flask que a aplicacão está em modo de teste, o mesmo facilita comportamentos
        'DATABASE': db_path
        }
    )

    with app.app_context():
        init_db()  # Zerando a base de dados
        get_db().executescript(_data_sql)  # Executando DML

    yield app  # Generator function da app para melhor iteracão

    os.close(db_fb)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # Chama a jogada `fixture` app
    return app.test_client()  # Cria requisicões como cliente sem execucões no servidor


@pytest.fixture
def runner(app):
    # Chama a jogada `fixture` app
    return app.test_cli_runner()  # Cria execucões para chamar comandos registrados na aplicacão
