import os
import flask
import flask_pymongo


app = flask.Flask(__name__)
app.config.update([(k, v) for k, v in os.environ.items() if k.startswith("MONGO_")])

import pudb; pudb.set_trace()
mongo = flask_pymongo.PyMongo(app)
