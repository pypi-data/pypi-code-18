from os.path import dirname, abspath, join

PACKAGE_PATH = dirname(abspath(__file__))
PROJECT_TEMPLATE_PATH = join(PACKAGE_PATH, 'templates/adventure_template')
TRAVEL_TEMPLATE = join(PACKAGE_PATH, 'templates/travel_template.py')
