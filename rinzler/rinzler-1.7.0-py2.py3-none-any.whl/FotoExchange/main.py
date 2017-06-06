import sys
import os
import django
import traceback
from datetime import datetime

# Turn off bytecode generation
sys.dont_write_bytecode = True

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Import your models for use in your script
from services.sync import Sync

try:
    # Init sync
    Sync().run()
except KeyboardInterrupt:
    print("Operacao interrompida pelo usuario as {0}".format(datetime.now()))
    sys.exit(1)
except Exception as e:
    print(e)
    print('<pre>' + traceback.format_exc() + '</pre>')
    print("Erro as {0}".format(datetime.now()))
    sys.exit(1)
