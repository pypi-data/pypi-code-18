# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Pf(models.Model):
    pf_cod = models.AutoField(primary_key=True)
    app_cod = models.IntegerField()
    orgao_cod = models.IntegerField(blank=True, null=True)
    orgao_entidade_cod = models.IntegerField(blank=True, null=True)
    usuario_cod = models.IntegerField(blank=True, null=True)
    data_hora = models.DateTimeField(blank=True, null=True)
    pf_cpf = models.CharField(max_length=11)
    pf_verif = models.CharField(max_length=1, blank=True, null=True)
    pf_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pf'
