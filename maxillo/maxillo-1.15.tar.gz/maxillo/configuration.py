import json
import logging
import os

CONFIG = '/etc/maxillo/master/configuration.json'
SSH_KEY = '/etc/maxillo/master/.ssh/id_rsa'

LOGGER = logging.getLogger(__name__)

def exists():
    return os.path.exists(CONFIG)

def create(data):
    with open(CONFIG, 'w') as f:
        json.dump({
            'hostname'  : data['hostname'],
        }, f)

def get():
    with open(CONFIG, 'r') as f:
        return json.load(f)

def save_ssh_key(key):
    LOGGER.info("Saving new ssh key to %s", SSH_KEY)
    if not os.path.exists(os.path.dirname(SSH_KEY)):
        os.path.makedirs(os.path.dirname(SSH_KEY))
    with open(SSH_KEY, 'wb') as f:
        while True:
            chunk = key.read(4096)
            if not chunk:
                return
            f.write(chunk)
