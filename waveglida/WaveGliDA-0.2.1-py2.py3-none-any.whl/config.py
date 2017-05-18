import json
import os


DEBUG = True
PORT = 5000

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

THREADS_PER_PAGE = 2

CONFIG_FNAME = os.path.normpath("{}/static/json/config.json".format(BASE_DIR))
with open(CONFIG_FNAME) as cf:
    plot_config = json.load(cf)

PLOTTING_NAMES = plot_config['plotting_names']
MAP_DOMAIN = plot_config['map_defaults']

UPLOAD_DIR = os.path.normpath("{}/data/".format(BASE_DIR))
