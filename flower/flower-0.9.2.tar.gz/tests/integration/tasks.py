import os
import time
from datetime import datetime

from celery import Celery


app = Celery("tasks",
             broker=os.environ.get('CELERY_BROKER', 'amqp://'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://'))
app.conf.CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']


@app.task
def add(x, y):
    return x + y


@app.task
def sleep(seconds):
    time.sleep(seconds)


@app.task
def error(msg):
    raise Exception(msg)


if __name__ == "__main__":
    app.start()
