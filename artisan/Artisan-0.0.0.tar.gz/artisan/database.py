from flask import Response


def sql():
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

    class Model(db.Model):
        __abstract__ = True
        _visible = ['id']

        id = db.Column(db.Integer, primary_key=True)

        def to_dict(self):
            return {c: getattr(self, c) for c in self._visible}

    return db, Model


def mongo():
    from flask_mongoengine import MongoEngine
    db = MongoEngine()

    class Model(db.DynamicDocument):
        meta = {
            'abstract': True,
        }
        _visible = ['id']

    return db, Model


def bsonify(value):
    from bson.json_util import dumps
    value = dumps(value, sort_keys=True, indent=4)
    return Response(value, mimetype='application/json')
