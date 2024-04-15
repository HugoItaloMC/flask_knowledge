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
