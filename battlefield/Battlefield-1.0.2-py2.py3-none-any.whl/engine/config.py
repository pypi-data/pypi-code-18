# -*- coding: utf-8 -*-
import os


class Config(object):
    """
    A basic configuration class reading from environment containing required 
    values that can be extended and override the default configurations.
    
    Note::
        It removes each key/value it reads.
    """

    def __init__(self, prefix):
        self.__conf = dict(
            MQ_HOST='localhost',
            MQ_VHOST='battlefield',
            MQ_USERNAME='username',
            MQ_PASSWORD='password',
        )
        for key in os.environ:
            if key.startswith(prefix + '_'):

                self.__conf['_'.join(key.split('_')[1:])] = os.environ[key]
                os.environ.unsetenv(key)

    def __getattr__(self, item):
        return self.__conf.get(item)
