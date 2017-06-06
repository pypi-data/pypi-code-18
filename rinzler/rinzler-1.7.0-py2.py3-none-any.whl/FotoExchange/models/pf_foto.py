# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from .pf import Pf

class PfFoto(models.Model):
    pf_foto_cod = models.AutoField(primary_key=True)
    pf_cod = models.ForeignKey('Pf', models.DO_NOTHING, db_column='pf_cod')
    app_cod = models.IntegerField()
    orgao_cod = models.IntegerField()
    orgao_entidade_cod = models.IntegerField()
    usuario_cod = models.IntegerField()
    data_hora = models.DateTimeField(blank=True, null=True)
    pf_foto_nome = models.CharField(max_length=100)
    pf_foto_hash = models.CharField(max_length=35)
    pf_foto_mime = models.CharField(max_length=20)
    pf_foto_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pf_foto'
