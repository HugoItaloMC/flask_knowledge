import os

from flask import Flask


def create_app(test_config=None):
    # Criacão e configuracão da aplicacão
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    if test_config is None:
        # Carregando a instância de configuracão, se ela existir, se há app ñ estiver em test
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Se o teste for verdadeiro
        app.config.from_mapping(test_config)

    # Garantindo a instância de pastas existentes
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World'

    from . import db, auth
    db.init_app(app)
    app.register_blueprint(auth.blue_auth)

    return app
