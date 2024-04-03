from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp_blog = Blueprint('blog', __name__, template_folder='template', static_folder='static')


@bp_blog.route('/')
def index():
    #  Index vai mostrar vários os posts mais recentes, a consulta vai utilizar JOIN com ORDER BY

    db = get_db()
    posts = db.execute(
        """
        SELECT p.id, title, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY created DESC
        """
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

