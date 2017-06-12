import os
from sqlalchemy import create_engine


def connect_sqlalchemy():
    """
    Connect to sqlalchemy and return the engine
    """
    username = os.getenv('db_user')
    password = os.getenv('db_password')
    database = os.getenv('db_name')
    host = os.getenv('db_host')

    if username is None or password is None or database is None or host is None:
        raise Exception("""Cannot connect to SQLAlchemy Engine. Database configurations are not set in env.
        \n Set env like following:
        \t export db_host=example.com
        \t export db_name=my_db_name
        \t export db_user=my_db_user
        \t export db_password=my_db_password""")
    engine = create_engine('mysql://%s:%s@%s/%s' % (username, password, host, database))
    return engine.connect()


def run_db_query(sql):
    """
    Run a given query and return output if any
    """
    with connect_sqlalchemy() as conn:
        return conn.execute(sql)
