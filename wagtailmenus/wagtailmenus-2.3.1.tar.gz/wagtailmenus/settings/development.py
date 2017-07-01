"""
Example settings for local development

Use this file as a base for your local development settings and copy
it to development.py. It should not be checked into your code repository.
"""
from .base import *  # NOQA

DEBUG = True

INSTALLED_APPS += (
    'django_extensions',
    # 'debug_toolbar',
    'wagtailmenus.tests',
    'wagtailmenus.development',
    'wagtail.contrib.wagtailstyleguide',
)

DATABASES = {
    'default': {
        'NAME': 'wagtailmenus-development.sqlite',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF = 'wagtailmenus.development.urls'
WAGTAIL_SITE_NAME = 'Wagtailmenus development'
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False
WAGTAIL_ENABLE_UPDATE_CHECK = False
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1']

WAGTAILMENUS_PAGE_FIELD_FOR_MENU_ITEM_TEXT = 'translated_title'
WAGTAILMENUS_DEFAULT_CHILDREN_MENU_USE_SPECIFIC = 3
# WAGTAILMENUS_MAIN_MENU_MODEL = 'tests.CustomMainMenu'
# WAGTAILMENUS_FLAT_MENU_MODEL = 'tests.CustomFlatMenu'
# LANGUAGE_CODE = 'de'
