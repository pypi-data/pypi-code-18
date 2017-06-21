import base64
import collections
import json
import logging
import os
import pprint
import uuid as UUID

import arrow
import maxillo.configuration
import maxillo.keys

DEPLOYMENTS = '/etc/maxillo/deployments'
METAFILE = 'metadata.json'
LICENSE = '/etc/maxillo/license'

LOGGER = logging.getLogger(__name__)

class Command():
    def __init__(self, command, deployment, created=None, executed=None, result=None, status='created', uuid=None):
        self.command    = command
        self.created    = arrow.utcnow() if created is None else created
        self.deployment = deployment
        self.executed   = executed
        self.result     = result
        self.status     = status
        self.uuid       = UUID.uuid4() if uuid is None else uuid

    @staticmethod
    def load(deployment, uuid):
        path = os.path.join(DEPLOYMENTS, str(deployment), 'commands', str(uuid), 'metadata.json')
        LOGGER.debug("Loading command from %s", path)
        with open(path, 'r') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                LOGGER.warning("Failed to load JSON at %s: %s", path, e)
                raise
        result = Command(**data)
        result.created = arrow.get(result.created)
        return result

    def write(self):
        os.makedirs(self.path(), exist_ok=True)
        metafile = os.path.join(self.path(), 'metadata.json')
        with open(metafile, 'w') as f:
            data = {
                'command'       : self.command,
                'created'       : self.created.isoformat(),
                'deployment'    : self.deployment,
                'executed'      : self.executed.isoformat() if self.executed else None,
                'result'        : self.result,
                'status'        : self.status,
                'uuid'          : str(self.uuid),
            }
            json.dump(data, f)
        LOGGER.info("Wrote command %s at %s", self, self.path())
        LOGGER.debug("Command content: %s", pprint.pformat(data))

    def path(self):
        return os.path.join(DEPLOYMENTS, self.deployment, 'commands', str(self.uuid))

    def stderr(self):
        path = os.path.join(self.path(), 'stderr')
        if not os.path.exists(path):
            return ''
        with open(path, 'r') as f:
            return f.read()

    def stdout(self):
        path = os.path.join(self.path(), 'stdout')
        if not os.path.exists(path):
            return ''
        with open(path, 'r') as f:
            return f.read()

    def __str__(self):
        return "Command {} for {} to {}".format(
            self.uuid,
            self.deployment,
            self.command if len(self.command) < 15 else self.command[:12] + '...',
        )

Deployment = collections.namedtuple('Deployment', ('application', 'branch', 'key', 'master', 'name', 'uuid'))
def list(application=None):
    if not os.path.exists(DEPLOYMENTS):
        return []
    licenses = [get(uuid) for uuid in os.listdir(DEPLOYMENTS)]
    if application:
        licenses = [license for license in licenses if license.application == application]
    return licenses

def create(name, application):
    uuid = UUID.uuid4()
    path = os.path.join(DEPLOYMENTS, str(uuid))
    os.makedirs(os.path.join(path, 'commands'))
    metafile = os.path.join(path, METAFILE)
    with open(metafile, 'w') as f:
        json.dump({
            'application'       : application.uuid,
            'master'            : maxillo.configuration.get()['hostname'],
            'name'              : name,
            'uuid'              : str(uuid),
        }, f)
    LOGGER.info("Created new license %s in %s", name, metafile)
    public_file = os.path.join(path, 'public.pem')
    private_file = os.path.join(path, 'private.pem')
    maxillo.keys.generate_key(public_file, private_file)
    return uuid

def create_command(deployment, command):
    result = Command(
        command     = command,
        deployment  = deployment,
    )
    result.write()
    LOGGER.info("Created new command %s", result.uuid)
    return result

def get(uuid):
    metafile = os.path.join(DEPLOYMENTS, str(uuid), METAFILE)
    with open(metafile, 'r') as f:
        data = json.load(f)
    data['key'] = None
    return Deployment(**data)

def get_commands(deployment):
    path = os.path.join(DEPLOYMENTS, str(deployment), 'commands')
    commands = [get_command(deployment, uuid) for uuid in os.listdir(path)]
    return sorted(commands, key=lambda x: x.created, reverse=True)

def get_command(deployment, uuid):
    return Command.load(deployment, uuid)

def command_output(deployment, uuid, pipe):
    return open(os.path.join(DEPLOYMENTS, str(deployment), 'commands', str(uuid), pipe), 'wb')

def get_license_content(uuid):
    license = get(uuid)
    public_file = os.path.join(DEPLOYMENTS, uuid, 'private.pem')
    with open(public_file, 'r') as f:
        key = f.read()
    data = {
        'application'   : license.application,
        'key'           : key,
        'master'        : maxillo.configuration.get()['hostname'],
        'name'          : license.name,
        'uuid'          : license.uuid,
    }
    return json.dumps(data)

def has_license():
    return os.path.exists(LICENSE)

def load_license():
    if load_license.license:
        return load_license.license
    with open(LICENSE, 'r') as f:
        data = json.load(f)
    data['key'] = maxillo.keys.deserialize_private(data['key'])
    return Deployment(branch=None, **data)
load_license.license = None

def save_license(license):
    LOGGER.info("Saving new license content to %s", license)
    with open(LICENSE, 'wb') as f:
        while True:
            chunk = license.read(4096)
            if not chunk:
                return
            f.write(chunk)

def generate_auth_headers(body=None):
    license = load_license()
    now = arrow.utcnow()
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    authorization = _generate_authorization(license.key, license.uuid, date, body or '')
    return {
        'license'               : license.uuid,
        'date'                  : date,
        'authorization'         : "RSA-SHA256 {}".format(authorization.decode('utf-8')),
        'authorization-headers' : "license;date;body",
    }

def _auth_content(uuid, date, body):
    return "{};{};{}".format(uuid, date, body).encode('utf-8')

def _generate_authorization(key, uuid, date, body):
    auth_content = _auth_content(uuid, date, body)
    LOGGER.debug("Auth content: %s", auth_content)
    authorization = maxillo.keys.generate_signature(key, auth_content)
    LOGGER.debug("Signature: %s", [hex(x) for x in authorization])
    coded_auth = base64.urlsafe_b64encode(authorization)
    LOGGER.debug("Authorization: %s", coded_auth)
    return coded_auth

def authenticate(uuid, date, body, authorization):
    LOGGER.debug("Authorization: %s", authorization)
    signature = base64.urlsafe_b64decode(authorization)
    LOGGER.debug("Signature: %s", [hex(x) for x in signature])
    path = os.path.join(DEPLOYMENTS, uuid, 'public.pem')
    with open(path, 'r') as f:
        data = f.read()
    key = maxillo.keys.deserialize_public(data)
    auth_content = _auth_content(uuid, date, body)
    LOGGER.debug("Auth content: %s", auth_content)
    return maxillo.keys.is_valid(key, signature, auth_content)
