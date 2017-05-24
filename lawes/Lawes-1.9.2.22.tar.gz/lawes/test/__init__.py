
from lawes.db import models

conf_dict = {'MONGO_URI': 'mongodb://127.0.0.1:27017/', 'DB_NAME': 'testdb'}
models.setup(conf=conf_dict)

class Fruit(models.Model):
    class Meta:
        db_table = 'fruit'

    name = models.CharField(default='')
    color = models.CharField(default='')
    sid = models.AutoField()
    nid = models.AutoField(start=1000000000)