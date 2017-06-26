import socket
import paramiko
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException


from retrying import retry


@retry(wait_fixed=2000, stop_max_attempt_number=3)
def check_ssh(ip, user='test', password='Test123.'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=user, password=password)
        print 'Node {0} ssh connected.'.format(ip)
    except (BadHostKeyException, AuthenticationException,
            SSHException, socket.error) as err:
        print 'There was an error during ssh check ip: {0}, user: {1}'.format(ip, user)
        print err

        return 1