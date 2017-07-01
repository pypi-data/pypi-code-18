# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

APP_TYPE_CHOICES = (
    ('RDBMS', 'RDBMS'),
    ('NoSql', 'NoSql'),
    ('Logger', 'Logger'),
)

CRED_TYPE_CHOICES = (
    ('POSTGRES', 'POSTGRES'),
    ('REDSHIFT', 'REDSHIFT'),
    ('ELASTICSEARCH', 'ELASTICSEARCH'),    
)

class UserCreds(models.Model):
    """ 
        Used to track the user credentials 
    """
    user = models.ForeignKey(User, related_name = "user_creds")
    app_type = models.CharField(max_length = 50, choices = APP_TYPE_CHOICES, default = "RDBMS")
    cred_type = models.CharField(max_length = 50, choices = CRED_TYPE_CHOICES, default = "POSTGRES")
    host = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    port = models.CharField(max_length = 10)
    db = models.CharField(max_length = 50)
    status = models.CharField(max_length = 20, choices = (('Active', 'Active'), ('InActive', 'InActive')))

    class Meta:
        db_table = "qvad_user_creds"

