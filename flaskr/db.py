import sqlite3
import click

# ` current_app `Objeto especial  que aponta uma manipulacão para aplicacão flask
# `g` Outro objeto especial que é unico para cada requisicão
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Conversa com a conexão para retornar linhas que agem como dicionários
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():

    db = get_db()
    with current_app.open_resource('schema.sql') as sql:
        db.executescript(sql.read().decode('utf8'))


@click.command('init-db')  # Gera uma interface de comando para executar a funcão decorada
def init_db_command():
    # Limpa o banco de dados se existr e criara novas tabelas
    init_db()
    click.echo('Initialize DataBase')  # Saída no terminal se a execucão for bem sucedida


def init_app(app):
    # close_db e init_db_command são funcões necessárias para registros com a instância da aplicacão

    # Gerando contexto da aplicacão para guardar tracks de nível de requisicões dos dados
    with app.app_context():
        app.teardown_appcontext(close_db)  # Chama o flask para limpar a subida apóes uma resposta
        app.cli.add_command(init_db_command)  # Adiciona novos comandos que podem ser chamados a partir do comando `flask`