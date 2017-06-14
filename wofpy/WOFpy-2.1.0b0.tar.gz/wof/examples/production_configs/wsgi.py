#! /home/ubuntu/miniconda/envs/wofpy/bin/python
from runserver import app as application
application.secret_key = 'Thisismysecretkey'
