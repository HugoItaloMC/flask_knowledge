"""
TODO:
    After install application 'flaskr'
    `pip install pyuwsgi uwsgi`
    or
    `pip install --no-binary pyuwsgi pyuwsgi`
     To gonna next step it account I consider
    the user defined configurations  in  your
    server proxy (apache/nginx).
     Now we run server wsgi, writte at terminal:
   `$ uwsgi --socket localhost:8080 --wsgi-file flaskr/wsgi.py --callable app --master -p 4 --threads 2 --stats localhost:8181`
"""
from flaskr import create_app


app = create_app()
