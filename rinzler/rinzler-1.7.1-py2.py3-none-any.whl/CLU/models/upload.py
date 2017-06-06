# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Upload(models.Model):
    upload_cod = models.AutoField(primary_key=True)
    app_cod = models.IntegerField()
    orgao_cod = models.IntegerField()
    orgao_entidade_cod = models.IntegerField()
    usuario_cod = models.IntegerField()
    data_hora = models.DateTimeField(blank=True, null=True)
    app_mod_cod = models.IntegerField()
    ref_cod = models.IntegerField()
    upload_nome = models.CharField(max_length=30)
    upload_hash = models.CharField(max_length=35)
    upload_mime = models.CharField(max_length=20)
    upload_s3 = models.CharField(max_length=1, blank=True, null=True)
    upload_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'upload'
