# -*- coding: utf-8 -*-
from djangoplus.db import models
from enderecos.db.fields import CepField


class Regiao(models.Model):
    nome = models.CharField(u'Nome', search=True)
    codigo = models.CharField(u'Código', search=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('nome', 'codigo')}),)

    class Meta:
        verbose_name = u'Região'
        verbose_name_plural = u'Regiões'
        list_menu = u'Cadastros Gerais::Regiões', 'fa-th'

    def __unicode__(self):
        return u'%s' % self.nome


class Estado(models.Model):
    nome = models.CharField(u'Nome', search=True)
    sigla = models.CharField(u'Sigla', search=True)
    codigo = models.CharField(u'Código', search=True)
    regiao = models.ForeignKey(Regiao, verbose_name=u'Região', null=True, blank=False, filter=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('nome', ('sigla', 'codigo'), 'regiao')}),)

    class Meta:
        verbose_name = u'Estado'
        verbose_name_plural = u'Estados'
        list_menu = u'Cadastros Gerais::Estados', 'fa-th'
        list_per_page = 50

    def __unicode__(self):
        return u'%s' % self.sigla


class Municipio(models.Model):
    nome = models.CharField(verbose_name=u'Nome', search=True)
    estado = models.ForeignKey(Estado, verbose_name=u'Estado', filter=True)
    codigo = models.CharField(u'Código', search=True)

    fieldsets = ((u'Dados Gerais', {'fields': ('estado', 'nome', 'codigo')}),)

    class Meta:
        verbose_name = u'Município'
        verbose_name_plural = u'Municípios'
        list_menu = u'Cadastros Gerais::Municípios', 'fa-th'
        list_per_page = 100

    def __unicode__(self):
        return u'%s/%s' % (self.nome, self.estado)


class Endereco(models.Model):
    cep = CepField(u'CEP', example=u'59.141-000')
    logradouro = models.CharField(u'Logradouro', example=u'Centro')
    numero = models.IntegerField(u'Número', example=123)
    complemento = models.CharField(u'Complemento', null=True, blank=True, example=u'Apartamento 100')
    municipio = models.ForeignKey(Municipio, verbose_name=u'Município', filter=True, example=u'Parnamirim', lazy=True)
    bairro = models.CharField(u'Bairro', example=u'Cohabinal')

    fieldsets = ((u'Dados Gerais', {'fields': (('cep', 'numero'), ('complemento', 'logradouro'), ('bairro', 'municipio'))}),)

    class Meta:
        verbose_name = u'Endereço'
        verbose_name_plural = u'Endereços'

    def __unicode__(self):
        return u'%s, %s, %s' % (self.logradouro, self.numero, self.municipio)

