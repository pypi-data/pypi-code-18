import datetime

from celery.schedules import crontab

from .logging_test import test_configure_logging as configure_test
from settei.presets.celery import WorkerConfiguration


def test_worker_config():
    conf = WorkerConfiguration({
        'worker': {
            'broker_url': 'redis://',
            'celery_result_backend': 'redis://',
        },
    })
    assert (conf.worker_config['BROKER_URL'] ==
            conf.worker_broker_url ==
            'redis://')
    assert (conf.worker_config['CELERY_RESULT_BACKEND'] ==
            conf.worker_result_backend ==
            'redis://')


def test_workeron_loaded():
    conf = WorkerConfiguration({
        'worker': {
            'on_loaded': "assert app(self) == 'ok'",
        },
    })
    log = []
    conf.on_worker_loaded(lambda self: log.append(self) or 'ok')
    assert log == [conf]


def test_configure_logging():
    configure_test('settei.workertest.', WorkerConfiguration)


def test_worker_schedule():
    # timedelta
    conf = WorkerConfiguration({
        'worker': {
            'broker_url': 'redis://',
            'celery_result_backend': 'redis://',
            'celerybeat_schedule': {
                'add-every-30-seconds': {
                    'task': 'tasks.add',
                    'schedule': 'timedelta(seconds=30)',
                },
            },
        }
    })
    assert conf.worker_schedule == {
        'add-every-30-seconds': {
            'task': 'tasks.add',
            'schedule': datetime.timedelta(seconds=30),
            'args': (),
        },
    }
    assert conf.worker_config['CELERYBEAT_SCHEDULE'] == conf.worker_schedule
    # crontab
    conf2 = WorkerConfiguration({
        'worker': {
            'broker_url': 'redis://',
            'celery_result_backend': 'redis://',
            'celerybeat_schedule': {
                'add-every-minute': {
                    'task': 'tasks.add',
                    'schedule': "crontab(minute='*')",
                    'args': [16, 16],
                },
            },
        }
    })
    assert conf2.worker_schedule == {
        'add-every-minute': {
            'task': 'tasks.add',
            'schedule': crontab(minute='*'),
            'args': (16, 16),
        },
    }
    assert conf2.worker_config['CELERYBEAT_SCHEDULE'] == conf2.worker_schedule
    # import path
    conf3 = WorkerConfiguration({
        'worker': {
            'broker_url': 'redis://',
            'celery_result_backend': 'redis://',
            'celerybeat_schedule': {
                'add-every-minute': {
                    'task': 'tasks.add',
                    'schedule': "celery.schedules:crontab(minute='*')",
                    'args': [16, 16],
                },
            },
        }
    })
    assert conf3.worker_schedule == conf2.worker_schedule
    assert conf3.worker_config['CELERYBEAT_SCHEDULE'] == conf3.worker_schedule
