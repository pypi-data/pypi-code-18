from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':sebs:',
            }
        },
        INSTALLED_APPS=['sebs'],
        SES_ACCESS_KEY='TestKey',
        SES_SECRET_KEY='SecretKey',
        SES_REGION='eu-west-1',
    )
