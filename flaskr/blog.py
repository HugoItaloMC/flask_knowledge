from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from flaskr.auth import login_required  # Autamente utilizado para verificar autenticacão de usuário na rota em uso
from flaskr.db import get_db

bp_blog = Blueprint('blog', __name__, template_folder='template', static_folder='static')


@bp_blog.route('/')
def index():
    #  Index vai mostrar vários os posts mais recentes, a consulta vai utilizar JOIN com ORDER BY

    db = get_db()
    posts = db.execute(
        """
        SELECT p.id, title, created, author_id, username, text_body FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY created DESC
        """
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp_blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, text_body, author_id) VALUES (?, ?, ?)', (title, body, g.user['id'],)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """

    :param id_: Id do usuário logado
    :param check_author: Condicão para verificar se o usuário logado é o dono do post a ser editado/deletado
    :return: o conteúdo do post do usuário em questão
    """
    post = get_db().execute(
        """SELECT p.id, title, text_body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?""", (id,)
    ).fetchone()
    if post is None:
        abort(404, "Post id %s doesn't exists" % id)

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp_blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            db.execute(
                """UPDATE post SET title = ?, text_body = ? WHERE id = ?""", (title, body, id,)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp_blog.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):

    get_post(id)
    db = get_db()
    db.execute(
        """DELETE FROM post WHERE id = ?""", (id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))

