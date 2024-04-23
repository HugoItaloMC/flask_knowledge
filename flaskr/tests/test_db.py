import sqlite3

import pytest

from flaskr.db import  get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()  # Deve retornar a mesma conexão em tempo de chamada, após o contexto a conexão deve ser fechada
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as err:
        db.executescript('SELECT 1')

    assert 'closed' in str(err.value)


def test_init_db_command(runner, monkeypatch):

    """
    Testes na funcão init_db que registra um comando na aplicacão e retorna uma mensagem de saída

    :param runner: É o método de criado em conftest.py para testar comandos registrados na aplicacão
    :param monkeypatch: Ferramenta do Pytest para alterar funcões da aplicacão por uma registrada na chamada
    :return: non
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialize' in result.output
    assert Recorder.called