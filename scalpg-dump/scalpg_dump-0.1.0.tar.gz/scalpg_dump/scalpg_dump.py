# -*- coding: utf-8 -*-
import os
import subprocess

import dj_database_url


def main():
    # Get env vars
    p1 = subprocess.Popen(['scalingo', 'run', 'env'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(
        ['grep', 'postgres://'],
        stdin=p1.stdout,
        stdout=subprocess.PIPE
    )
    p1.stdout.close()
    output, err = p2.communicate()

    # Get db_url
    db_url = output.decode("utf-8").split('=')[1].split('\r\n')[0]

    # Parse db_url
    db_config = dj_database_url.parse(db_url)

    # Construct dump command
    command = "dbclient-fetcher postgresql > /dev/null; "
    command += "PGPASSWORD={PASSWORD} "
    command += "pg_dump --clean --host {HOST} --port {PORT} "
    command += "--username {USER} "
    command += "--no-owner --no-privileges "
    command += "--exclude-schema \'information_schema\' "
    command += "--exclude-schema '^pg_*' --dbname {NAME}"
    command = '"' + command + '"'
    command = command.format(**db_config)

    # Dump database
    result = os.popen("scalingo run " + command).read()
    print(result)


if __name__ == "__main__":
    main()
