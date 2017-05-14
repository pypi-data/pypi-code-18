# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings
from appconf import AppConf

settings = dj_settings

class BirAppConf(AppConf):
    KEY = ''
    URL = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
