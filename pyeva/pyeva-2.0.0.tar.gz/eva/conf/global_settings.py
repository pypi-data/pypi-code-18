# Default Eva settings. Override these with settings in the module
# pointed-to by the EVA_SETTINGS_MODULE environment variable.
EVA_SETTINGS_MODULE = "codebase.settings"
MODELS_MODULE = "codebase.models"

####################
# CORE             #
####################

DEBUG = False

# 数据库：默认使用 sqlite 文件型数据库
# DB = {
#     'engine': 'postgresql+psycopg2',
#     'host': '127.0.0.1',
#     'path': '',
#     'database': 'eva',
#     'username': 'eva',
#     'password': 'eva',
# }
DB = {
    'engine': 'sqlite',
    'host': '',
    'path': 'db.dat',
    'database': '',
    'username': '',
    'password': '',
}

MANAGEMENT_COMMAND_DIRS = ()

PACKAGE_NAME = 'MS'
PACKAGE_VERSION = '1.0'
