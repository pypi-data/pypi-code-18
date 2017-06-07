import os
from eva.conf import settings


def get_db_uri():

    '''获取数据库访问接口

    http://docs.sqlalchemy.org/en/latest/core/engines.html
    '''
    if settings.DB_URI:
        return settings.DB_URI

    DB = settings.DB
    engine = DB.get('engine')

    if engine == 'sqlite':
        path = DB.get('path')
        if not path:
            path = 'data.db'

        if not os.path.isabs(path):
            path = os.path.join(
                settings.ROOT_PATH, path)

        DB['path'] = path
        DB_URI = '{engine}:///{path}'

    else:
        DB_URI = '{engine}://{username}:{password}' + \
                 '@{host}/{database}'

    return DB_URI.format(**settings.DB)
