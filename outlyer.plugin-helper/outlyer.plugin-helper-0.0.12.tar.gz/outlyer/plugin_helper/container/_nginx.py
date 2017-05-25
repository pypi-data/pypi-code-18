from datetime import datetime, timedelta
import inspect
import os
import re
import sys
import tempfile
from outlyer.plugin_helper import container


def reverse_read(fname, separator=os.linesep):
    with file(fname) as f:
        f.seek(0, 2)
        fsize = f.tell()
        r_cursor = 1
        while r_cursor <= fsize:
            a_line = ''
            while r_cursor <= fsize:
                f.seek(-1 * r_cursor, 2)
                r_cursor += 1
                c = f.read(1)
                if c == separator and a_line:
                    r_cursor -= 1
                    break
                a_line += c
            a_line = a_line[::-1]
            yield a_line


def patch():
    # check if this is being called from the nginx plugin
    frame = inspect.stack()[2]
    filename = frame[1]

    # The second predicate is because rpc will in some cases give the plugin a
    # generated name. E.g. `/opt/dataloop/.rpc_cache/PATCH_123-abc-nginx`
    # XXX: is this robust?
    if not filename.endswith("nginx.py") or filename.endswith("nginx"):
        return
    module = inspect.getmodule(frame[0])
    container_id = container.get_container_id()

    if container_id:
        import docker
        client = docker.from_env(
            assert_hostname=False,
            version="auto",
            timeout=5,
        )
        target = client.containers.get(container_id)

        def find_nginx_process_docker():
            procs = target.top().get("Processes", [])
            for proc in procs:
                if re.match('nginx', proc[-1]):
                    return True

        def get_logs(logfile, since):
            if logfile == 'stdout':
                target_time = datetime.now() - timedelta(seconds=since)
                logs = target.logs(since=target_time, stderr=False).split("\n")
                logs.reverse()
                return logs
            try:
                log_stream, _ = target.get_archive(logfile)
            except docker.errors.NotFound:
                print("Could not find file %s inside container %s" % (
                    logfile, target.name,
                ))
                sys.exit(2)

            temp_file = tempfile.mkstemp()[1]
            with open(temp_file, 'w') as temp:
                temp.write(log_stream.read())
            logs = list(reverse_read(temp_file))
            os.remove(temp_file)
            return logs

        module.read = get_logs
        module.find_nginx_process = find_nginx_process_docker


def unpatch():
    pass


def is_patched():
    pass
