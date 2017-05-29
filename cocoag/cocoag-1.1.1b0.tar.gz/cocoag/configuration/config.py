import configparser
import logging
import os
from pathlib import Path

current_file = os.path.realpath(__file__)
CONFIG_ROOT = Path(current_file).parent
CONFIG_TEMPLATE = os.path.join(CONFIG_ROOT, "default_cocoag.cfg")
PACKAGE_ROOT = Path(CONFIG_ROOT).parent
COCOAG_ROOT = os.path.join(PACKAGE_ROOT, "cocoag")
GENERATOR_ROOT = os.path.join(COCOAG_ROOT, "generator")
S3_ROOT = os.path.join(COCOAG_ROOT, "s3")


# Taken from: https://stackoverflow.com/questions/335695/lists-in-configparser
class MyConfigParser(configparser.ConfigParser):
    def getlist(self,section,option):
        value = self.get(section,option)
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def getlistint(self,section,option):
        return [int(x) for x in self.getlist(section,option)]


# Method taken from the Airflow project: https://github.com/apache/incubator-airflow
def expand_env_var(env_var):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


def generate_default_conf():
    with open(CONFIG_TEMPLATE) as config_template:
        conf = config_template.read()
        return conf.format(PACKAGE_ROOT=PACKAGE_ROOT)


# Style taken from the Airflow project: https://github.com/apache/incubator-airflow
if 'COCOAG_CONF' not in os.environ:
    COCOAG_CONF = expand_env_var('~/.cocoag.cfg')
else:
    COCOAG_CONF = expand_env_var(os.environ['COCOAG_CONF'])

if not os.path.isfile(COCOAG_CONF):
    logging.info('Creating new Cocoag config file in: {}'.format(COCOAG_CONF))
    with open(COCOAG_CONF, 'w') as f:
        f.write(generate_default_conf())

config = MyConfigParser()
config.read(COCOAG_CONF)
