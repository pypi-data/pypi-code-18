"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# A list of strings representing the host/domain names that this Django site can serve.
# If you are unsure, just enter here your domain name, eg. ['mysite.com', 'www.mysite.com']

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
    'default': {
        # Misago requires PostgreSQL to run
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


# Caching
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/cache/#setting-up-the-cache

CACHES = {
    'default': {
        # Misago doesn't run well with LocMemCache in production environments
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


# Password validation
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username', 'email'],
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'


# User uploads (Avatars, Attachments, files uploaded in other Django apps, ect.)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

MEDIA_URL = '/media/'


# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#static-root

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Absolute filesystem path to the directory that will hold user-uploaded files.
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#media-root

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# https://docs.djangoproject.com/en/1.10/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'theme', 'static'),
]


# Email configuration
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#email-backend

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25


# If either of these settings is empty, Django won't attempt authentication.

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


# Default email address to use for various automated correspondence from the site manager(s).

DEFAULT_FROM_EMAIL = 'Forums <%s>' % EMAIL_HOST_USER


# Application definition

AUTH_USER_MODEL = 'misago_users.User'

AUTHENTICATION_BACKENDS = [
    'misago.users.authbackends.MisagoBackend',
]

CSRF_FAILURE_VIEW = 'misago.core.errorpages.csrf_failure'

INSTALLED_APPS = [
    # Misago overrides for Django core feature
    'misago',
    'misago.users',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps used by Misago
    'debug_toolbar',
    'crispy_forms',
    'mptt',
    'rest_framework',

    # Misago apps
    'misago.admin',
    'misago.acl',
    'misago.core',
    'misago.conf',
    'misago.markup',
    'misago.legal',
    'misago.categories',
    'misago.threads',
    'misago.readtracker',
    'misago.search',
    'misago.faker',

    # Utility for moving data from Misago 0.5
    'misago.datamover',
]

INTERNAL_IPS = [
    '127.0.0.1'
]

LOGIN_REDIRECT_URL = 'misago:index'

LOGIN_URL = 'misago:login'

LOGOUT_URL = 'misago:logout'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'misago.users.middleware.RealIPMiddleware',
    'misago.core.middleware.frontendcontext.FrontendContextMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'misago.users.middleware.UserMiddleware',
    'misago.core.middleware.exceptionhandler.ExceptionHandlerMiddleware',
    'misago.users.middleware.OnlineTrackerMiddleware',
    'misago.admin.middleware.AdminAuthMiddleware',
    'misago.threads.middleware.UnreadThreadsCountMiddleware',
    'misago.core.middleware.threadstore.ThreadStoreMiddleware',
]

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'theme', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'misago.core.context_processors.site_address',
                'misago.core.context_processors.momentjs_locale',
                'misago.conf.context_processors.settings',
                'misago.users.context_processors.user_links',
                'misago.legal.context_processors.legal_links',

                # Data preloaders
                'misago.conf.context_processors.preload_settings_json',
                'misago.core.context_processors.current_link',
                'misago.markup.context_processors.preload_api_url',
                'misago.threads.context_processors.preload_threads_urls',
                'misago.users.context_processors.preload_user_json',

                # Note: keep frontend_context processor last for previous processors
                # to be able to expose data UI app via request.frontend_context
                'misago.core.context_processors.frontend_context',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Django Crispy Forms
#http://django-crispy-forms.readthedocs.io/en/latest/install.html

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',

    'misago.acl.panels.MisagoACLPanel',

    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]


# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'misago.core.rest_permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'misago.core.exceptionhandler.handle_api_exception',
    'UNAUTHENTICATED_USER': 'misago.users.models.AnonymousUser',
    'URL_FORMAT_OVERRIDE': None,
}


# Misago specific settings
# https://misago.readthedocs.io/en/latest/developers/settings.html

# PostgreSQL text search configuration to use in searches
# Defaults to "simple", for list of installed configurations run "\dF" in "psql"
# Standard configs as of PostgreSQL 9.5 are: dutch, english, finnish, french,
# german, hungarian, italian, norwegian, portuguese, romanian, russian, simple,
# spanish, swedish and turkish
# Example on adding custom language can be found here: https://github.com/lemonskyjwt/plpstgrssearch

MISAGO_SEARCH_CONFIG = 'simple'


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command

MISAGO_AVATAR_GALLERY = os.path.join(BASE_DIR, 'avatargallery')
