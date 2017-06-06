import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.realpath("./")

DATABASES = {
    'default': {
        'HOST': "dev-cluster.cluster-c6xdmpf9l5iu.us-east-2.rds.amazonaws.com",
        'ENGINE': "mysql_cymysql",
        'NAME': "onyxappc_social",
        'USER': "onyxappc_social",
        'PASSWORD': "v6n5g0a9%",
    }
}

INSTALLED_APPS = (
    'models',
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = 'secret_key'

SOCIAL_API_CONFIG = {
    'storage_path': os.path.realpath("/Library/WebServer/Documents/BRA/SocialAPI/storage/arquivos/"),
    'max_rows': 5
}

URL_DRIVE_API = "http://drive-api.alpha.onyxapis.com"
URL_AUTH_API = "http://auth-api.alpha.onyxapis.com"
URL_ACCOUNT_API = "http://account-api.alpha.onyxapis.com"
URL_JWT_API = "http://jwt-api.alpha.onyxapis.com"

#698078e594880ea7234827b965c40b913878a6e3