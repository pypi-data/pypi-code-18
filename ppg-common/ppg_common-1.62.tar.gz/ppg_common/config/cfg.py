import io
import yaml
from sqlalchemy import create_engine


class Config(object):

    DB_CONNECTION_FORMAT = 'postgresql://{user}:{pass}@{host}:{port}/{name}'

    def __init__(self, config_path):
        self.config_path = config_path
        with io.open(config_path, 'r') as cfg:
            self.data = yaml.safe_load(cfg)

        database = self.data.get('db')
        if database:
            self.DATABASE = self.DB_CONNECTION_FORMAT.format(**database)
            self.engine = create_engine(self.DATABASE, echo=True)

        service_session = self.data.get('service_session')
        if service_session:
            self.service_session = service_session

        version = self.application.get('version')
        if version:
            self.version = version

        self.APP_PORT = self.application.get('port')

    @property
    def application(self):
        return self.data.get('application')

    @property
    def db(self):
        return self.data.get('db')

    @property
    def redis_params(self):
        return self.data.get('redis_params')

    @property
    def session_params(self):
        return self.data.get('session_params')
