import json, pika, uuid, configparser
from enum import Enum


def is_meta(dictionary, meta):
    if dictionary['meta']:
        return True if dictionary['meta']['code'] == meta.value else False
    else:
        return True if dictionary['code'] == meta.value else False


class Meta(Enum):
    SUCCESS = 200, 'Success'
    BAD_REQUEST = 400, 'Bad Request'
    UN_AUTH = 401, 'Unauthorized Request'
    FORBIDDEN = 403, 'Forbidden Access'
    NOT_FOUND = 404, 'Not Handling Requests'

    def __new__(cls, value, message):
        member = object.__new__(cls)
        member._value_ = value
        member.message = message
        return member

    def asDict(self):
        return {"code": self.value, "message": self.message}


class Body(Enum):
    SUCCESS = 1000, 'Success'
    CODE_VERIFICATION = 1001, 'token or verification code wrong'
    DB_COMMIT_FAILED = 2001, 'Database commit failed, rolling back changes'
    VALIDATION_CODE_ERROR = 2002, 'Validation code does not match'
    TOKEN_INACTIVE = 2003, 'Token is inactive'
    TOKEN_NOT_FOUND = 2004, 'Token not found'
    USER_NOT_FOUND = 2005, 'User not found'
    USER_INACTIVE = 2006, 'User inactive'
    UN_AUTH = 2007, 'Unauthorized access'

    def __new__(cls, value, message):
        member = object.__new__(cls)
        member._value_ = value
        member.message = message
        return member

    def asDict(self):
        return {"code": self.value, "message": self.message}


class RpcData:
    CONST_DATA = 'data'
    CONST_META = 'meta'
    CONST_BODY = 'body'
    CONST_TAG = 'tag'
    CONST_METHOD = 'method'

    def __init__(self, *args, **kwargs):
        if self.CONST_DATA in kwargs:
            data = json.loads(kwargs.get(self.CONST_DATA, '{}'))
            if self.CONST_META in data:
                self.meta = data[self.CONST_META]
            if self.CONST_BODY in data:
                self.body = data[self.CONST_BODY]
        if self.CONST_META in kwargs:
            self.meta = kwargs.get(self.CONST_META, None)
        if self.CONST_BODY in kwargs:
            self.body = kwargs.get(self.CONST_BODY, None)

    def required(self):
        if self.meta and self.body and self.CONST_TAG in self.meta and self.CONST_METHOD in self.meta:
            return True
        else:
            return False

    @property
    def meta(self):
        if hasattr(self, '_meta'):
            return self._meta
        return {}

    @meta.setter
    def meta(self, value):
        if isinstance(value, Meta):
            self._meta = value.asDict()
        elif isinstance(value, dict):
            self._meta = value
        else:
            ValueError("body must be instance of dict or meta")

    @property
    def body(self):
        if hasattr(self, '_body'):
            return self._body
        return {}

    @body.setter
    def body(self, value):
        if isinstance(value, Body):
            self._body = value.asDict()
        elif isinstance(value, dict):
            self._body = value
        else:
            ValueError("body must be instance of dict or body")

    def dump(self):
        return json.dumps({self.CONST_META: self.meta, self.CONST_BODY: self.body})


class RpcClient:
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            config = kwargs.get('config')
            self.host = config['host']
            self.user = config['user']
            self.password = config['password']
            self.port = config['port']
            self.queue_name = config['queue_name']
        elif all(key in kwargs for key in ['host', 'port', 'user', 'password', 'queue_name']):
            self.host = kwargs.get('host')
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.port = kwargs.get('port')
            self.queue_name = kwargs.get('queue_name')
        else:
            config = configparser.ConfigParser()
            config.read('/etc/rpclient.ini')
            self.host = config['CREDENTIALS']['host']
            self.user = config['CREDENTIALS']['user']
            self.password = config['CREDENTIALS']['password']
            self.port = config['CREDENTIALS']['port']
            self.queue_name = config['CREDENTIALS']['queue_name']

    def print_params(self):
        print(self.host, self.user, self.password, self.port, self.queue_name)

    def start(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, int(self.port), '/', credentials)
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, queue=self.callback_queue)
        self.channel.start_consuming()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def consume(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return RpcData(data=self.response)

    def call(self, n):
        self.start()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        self.channel.stop_consuming()
        self.channel.close()
        self.connection.close()

        return RpcData(data=self.response)

    def close(self):
        self.channel.stop_consuming()
        self.channel.close()
        self.connection.close()
