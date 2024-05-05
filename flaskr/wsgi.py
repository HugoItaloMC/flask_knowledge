"""
TODO:
    After install application 'flaskr'
    `pip install pyuwsgi uwsgi`
    or
    `pip install --no-binary pyuwsgi pyuwsgi`
    Now we run server wsgi, writte at terminal:
   `$ uwsgi --http 127.0.0.1:8080 --master -p 4 -w wsgi:app`
"""
from flaskr import create_app
app = create_app()
