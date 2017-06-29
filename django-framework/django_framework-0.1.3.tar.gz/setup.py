from distutils.core import setup

setup(
    # Application name:
    name="django_framework",

    # Version number (initial):
    version="0.1.3",

    # Application author details:
    author="redsands",
    author_email="name@addr.ess",

    # Packages
    packages=["django_framework"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful stuff for django.  .",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        
        "Django",
        "django-cors-headers",
        "django-debug-toolbar",
        "django-extensions",
        "django-nose",
        "django-redis",
        
        "googlemaps",
        "inflection",
        "Inflector",
        
        "jsonfield",
        "requests",
        "arrow",
        "pytz",
        
        
        "kafka-python",
        "redis",
        "MySQL-python",
        
        "websocket-client",
        
    ],
)