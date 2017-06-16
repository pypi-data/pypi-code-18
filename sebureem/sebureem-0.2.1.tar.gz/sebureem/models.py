"""Models
"""
from datetime import datetime
from peewee import Model
from peewee import CharField, TextField, BooleanField
from peewee import DateTimeField, ForeignKeyField
from sebureem import db

__all__ = ['Sebuks', 'Sebura']


class BaseModel(Model):

    class Meta:
        database = db


class Sebusik(BaseModel):
    pass


class Sebuks(BaseModel):
    name = CharField()
    locked = BooleanField(default=False)


class Sebura(BaseModel):
    text = TextField()
    date = DateTimeField(default=datetime.now())
    topic = ForeignKeyField(Sebuks, related_name='comments')
    published = BooleanField(default=False)
