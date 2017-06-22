import os
import webbrowser
import time
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    try:
        import rxncon_site.settings
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rxncon_site.settings")
    except :
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.rxncon_site.settings")

application = get_wsgi_application()
webbrowser.open('http://127.0.0.1:8888/')
call_command('runserver',  '127.0.0.1:8888', '--verbosity=0')


