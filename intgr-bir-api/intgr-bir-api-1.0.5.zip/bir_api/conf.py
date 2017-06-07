# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings
from appconf import AppConf

settings = dj_settings

class BirAppConf(AppConf):
    TEST_MODE = True

    TEST_KEY = ''
    TEST_URL = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'

    PROD_KEY = ''
    PROD_URL = 'https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
