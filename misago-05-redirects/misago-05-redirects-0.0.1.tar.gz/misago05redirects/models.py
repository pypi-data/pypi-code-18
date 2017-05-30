from django.db import models


class OldIdRedirect(models.Model):
    CATEGORY = 0
    POST = 1
    THREAD = 2
    USER = 3

    model = models.PositiveIntegerField()
    old_id = models.PositiveIntegerField()
    new_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'datamover_oldidredirect'
        managed = False
