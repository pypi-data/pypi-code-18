
import os
import sys
import doctest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_HOST = BASE_DIR.split('\\')[-1]
sys.path.append(BASE_DIR)

def all_doctest():
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext == '.py':
                root = root.replace(BASE_DIR, '').replace('/', '.').replace('\\', '.')
                import_name = DIR_HOST + root + '.' + name
                importpy = __import__(import_name, globals(), locals(), name, 0)
                doctest.testmod(importpy)

