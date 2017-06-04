# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = migrate = Migrate()
