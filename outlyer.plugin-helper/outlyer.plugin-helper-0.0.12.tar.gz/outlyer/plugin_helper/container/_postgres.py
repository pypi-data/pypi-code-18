from outlyer.plugin_helper import container
import psycopg2
import re


POSSIBLE_HOSTS_REGEX = "host=(localhost|127.0.0.1|::1)"


def postgres_connect(dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
    container_ip = container.get_container_ip()
    if dsn is not None and container.is_container() and container_ip is not None:
        match = re.search(POSSIBLE_HOSTS_REGEX, dsn)
        if match is not None:
            to_replace = match.group(0)
            new_host = "host=%s" % container_ip
            dsn = dsn.replace(to_replace, new_host)
    return psycopg2._old_connect(dsn, connection_factory, cursor_factory,  **kwargs)


def patch():
    if not is_patched():
        psycopg2._old_connect = psycopg2.connect
        psycopg2.connect = postgres_connect


def unpatch():
    if is_patched():
        psycopg2.connect = psycopg2._old_connect
        delattr(psycopg2, '_old_connect')


def is_patched():
    return hasattr(psycopg2, '_old_connect')
