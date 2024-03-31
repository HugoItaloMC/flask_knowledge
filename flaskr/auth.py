"""
    BluePrint serve para gerenciar grupos de rotas da aplicacão
podemos criar diversas rotas associadas a um determinado blue-print
tendo assim um melhor controle das rotas e seus grupos associados
"""

import functools

from flask import (Blueprint, flash,
                   g, redirect,
                   render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

blue_auth = Blueprint('auth', __name__, url_prefix='/auth')  # Grupo de rotas associadas a rota '/auth'


@blue_auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not passwd:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES(?, ?)",  # Utilizando esse método é evitado ataques de SQL Injection
                    (username, generate_password_hash(passwd))  # Por seguranca senhas nunca devem ser armaznadas diretamente, sempre utilizar hashs para as senhas
                )
                db.commit()
            except db.IntegrityError:
                error = 'User %s is ready registered' % username

            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('register.html')


@blue_auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']

        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Username'
        elif not check_password_hash(user['password'], passwd):
            error = 'Incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('login.html')


#  Validando usuário se na sessão existe usuário logado
@blue_auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id)
        ).fetchone()

# logout
@blue_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Criar, editar ou deletar vai requerer um usuário logado. Um decorator para ser usado e checar este em cada requisicão
def login_required(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapper_view