from flask import Flask, g
from werkzeug.local import LocalProxy


from papimem.storage import get_storage


webapp = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = get_storage(webapp.config['STORAGE_DSN'])
    return db


db = LocalProxy(get_db)


from papimem.web import views
