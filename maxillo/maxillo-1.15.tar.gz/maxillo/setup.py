import logging
import subprocess

import docker
import docker.errors
import docker.types.services
import jinja2

LOGGER = logging.getLogger()

def master(hostname, email, password, letsencrypt_staging=False):
    LOGGER.info("Setting up master at '%s' with admin email %s", hostname, email)
    env = jinja2.Environment(
        loader = jinja2.FileSystemLoader('/src/templates'),
    )
    client = docker.from_env()
    _create_overlay_network(client)
    _setup_maxillo_master(client)
    _ensure_have_ssl_certs(client, hostname, email, staging=letsencrypt_staging)
    _setup_nginx(client, env, hostname, email, password)

def _create_overlay_network(client):
    if client.networks.get('docker-swarm-overlay'):
        LOGGER.info("docker-swarm-overlay already exists")
        return
    network = client.networks.create(
        name    = 'docker-swarm-overlay',
        driver  = 'overlay',
        options = {
            'subnet'    : '10.0.9.0/24',
            'opt'       : 'encrypted',
        },
    )
    LOGGER.info('Created docker-swarm-overlay %s', network)

def _setup_maxillo_master(client):
    try:
        client.services.get('maxillo')
        LOGGER.info("maxillo service is already defined")
        return
    except docker.errors.NotFound:
        LOGGER.info("Creating maxillo service")
    service = client.services.create(
        args            = ['master'],
        image           = 'authentise/maxillo',
        mounts          = ['/etc/maxillo:/etc/maxillo:rw'],
        name            = 'maxillo',
        networks        = ['docker-swarm-overlay'],
    )
    LOGGER.info("Created maxillo service %s", service)

def _ensure_have_ssl_certs(client, hostname, email, staging=False):
    try:
        client.volumes.get('letsencrypt')
        LOGGER.info("Looks like we have an letsencrypt volume. Assuming it's set up")
        return
    except docker.errors.NotFound:
        LOGGER.info("Generating SSL certificates")
    volume = client.volumes.create(
        driver  = 'local',
        name    = 'letsencrypt',
    )
    LOGGER.info('Created letsencrypt volume. Running certbot...')
    command = ['certonly', '-n', '-d', hostname, '-m', email, '--agree-tos', '--standalone']
    if staging:
        command.append('--staging')
    output = client.containers.run(
        command = command,
        image   = 'certbot/certbot',
        ports   = {
            '80/tcp'    : 80,
            '443/tcp'   : 443,
        },
        volumes = {'letsencrypt': {
            'bind'  : '/etc/letsencrypt/',
            'mode'  : 'rw',
        }}
    )
    LOGGER.info("Ran certbot container with output: %s", output)

def _setup_nginx(client, env, hostname, email, password):
    LOGGER.info("Setting up nginx service for '%s'", hostname)
    try:
        client.services.get('nginx')
        LOGGER.info("nginx service is already defined")
        return
    except docker.errors.NotFound:
        LOGGER.info("Creating nginx service")
    _create_nginx_config(client, env, hostname, email, password)
    client.services.create(
        endpoint_spec   = docker.types.services.EndpointSpec(ports={80: 80, 443: 443}),
        image           = 'nginx:1.12-alpine',
        mounts          = [
            docker.types.services.Mount(
                target      = '/etc/nginx/conf.d',
                source      = 'nginx-config',
                type        = 'volume',
                read_only   = True,
            ),
            docker.types.services.Mount(
                target      = '/etc/letsencrypt',
                source      = 'letsencrypt',
                type        = 'volume',
                read_only   = True,
            ),
        ],
        name            = 'nginx',
        networks        = ['docker-swarm-overlay'],
    )
    LOGGER.info("Created nginx service")

def _create_nginx_config(client, env, hostname, email, password):
    volume = client.volumes.create(
        name='nginx-config',
        driver='local',
    )

    FILES = ('letsencrypt.conf', 'maxillo.conf',)
    for file_ in FILES:
        LOGGER.info("Generating %s in volume nginx-config", file_)
        template = env.get_template('/config/nginx/{}'.format(file_))
        content = template.render(hostname=hostname)
        output = client.containers.run(
            entrypoint = ['/src/bin/maxillo', 'populate-volume', '/output/{}'.format(file_), content],
            image   = 'authentise/maxillo',
            volumes = {'nginx-config': {
                'bind'  : '/output/',
                'mode'  : 'rw',
            }},
        )
        LOGGER.info("Result: %s", output)

    LOGGER.info("Creating htpasswd file")
    secret = _make_secret(password)
    output = client.containers.run(
        entrypoint  = ['/src/bin/maxillo', 'populate-volume', '/output/users.htpasswd', '{}:{}'.format(email, secret)],
        image       = 'authentise/maxillo',
        volumes     = {'nginx-config': {
            'bind'  : '/output/',
            'mode'  : 'rw',
        }},
    )
    LOGGER.info("Result: %s", output)

def _make_secret(password):
    return subprocess.check_output(['openssl', 'passwd', '-apr1', '-stdin'], input=password.encode('utf-8')).decode('utf-8')
