
from lawes.db import models

conf_dict = {'mongo_uri': 'mongodb://127.0.0.1:27017/', 'db_name': 'testdb'}
models.setup(conf=conf_dict)

class Fruit(models.Model):
    class Meta:
        db_table = 'fruit'

    name = models.CharField(default='')
    color = models.CharField(default='')
    sid = models.AutoField()