import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': "mysql_cymysql",
        'NAME': "onyxappc_drive",
        'HOST': "192.168.234.235",
        'USER': "onyxappc_drive",
        'PASSWORD': "v6n5g0a9%",
    }
}

INSTALLED_APPS = (
    'models',
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = 'secret'

AWS_CREDENTIALS = {
    'aws_access_key_id': "AKIAIZ2NQ46ORB3BJATA",
    'aws_secret_access_key': "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"
}

DRIVE_API_CONFIG = {
    'bucket_env': "alpha-onxerp",
    'storage_path': os.path.realpath("/Library/WebServer/Documents/BRA/DriveAPI/storage/arquivos/")
}
