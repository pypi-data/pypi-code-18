# -*- coding: utf-8 -*-
import json
import urllib2
from urllib2 import HTTPError

from enderecos.models import Municipio
from django.http.response import HttpResponse


def consultar(request, cep):
    try:
        d = json.loads(urllib2.urlopen('http://api.postmon.com.br/v1/cep/%s' % cep).read())
        qs = Municipio.objects.filter(codigo=d['cidade_info']['codigo_ibge'])
        if qs.exists():
            cidade = qs[0]
            d['cidade_id'] = cidade.pk
            d['cidade'] = unicode(cidade)
        return HttpResponse(json.dumps(d))
    except HTTPError:
        return HttpResponse(json.dumps(dict(message=u'CPF inválido!')))