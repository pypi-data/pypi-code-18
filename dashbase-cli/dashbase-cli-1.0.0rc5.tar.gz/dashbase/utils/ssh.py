import paramiko
from pexpect import pxssh, TIMEOUT

from dashbase.services import LogService
from dashbase.utils.errors import CliRuntimeError


class Connect:
    def __init__(self, host, username, password=None, private_file=None, port=22):
        try:
            self.client = SSHClient(host=host, username=username, password=password, private_file=private_file,
                                    port=port)
        except pxssh.ExceptionPxssh:
            try:
                self.client = SSHClient(host=host, username=username, password=password, private_file=private_file,
                                        port=port)
            except pxssh.ExceptionPxssh:
                LogService.log('Connection to %s failed.' % host)
                LogService.log('Please check your configuration.')
                LogService.log('You may need to contact your administrator or support for more information.')
                raise CliRuntimeError('SSH Connection Error')

    def __enter__(self):
        # todo  add connect
        # self.client.connect()
        return self.client

    def __exit__(self, type, value, traceback):
        self.client.close()


class SSHClient:
    def __init__(self, host, username, password, private_file, port=22):
        if not private_file and not password:
            raise AttributeError("Please specify a key file.")

        self.host = host
        self.username = username
        self.password = password
        self.private_file = private_file
        self.port = port
        self.client = pxssh.pxssh()

        if private_file:
            self.client.login(server=host, port=port, username=username, ssh_key=private_file)

        elif password:
            self.client.login(server=host, port=port, username=username, password=password)

        self.paramiko = paramiko.SSHClient()
        self.paramiko.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if private_file:
            pkey = paramiko.RSAKey.from_private_key_file(private_file)
            self.paramiko.connect(host, port, username, pkey=pkey)

        elif password:
            self.paramiko.connect(host, port, username, password)

    def close(self):
        self.client.logout()

    def run(self, cmd, print_function=None):
        """
        :param cmd:
        :param print_function:
        :return: exitcode
        :return: output
        """
        try:
            self.client.sendline(cmd.replace('\n', ''))
            # ignore send cmd
            self.client.expect('\n')
            expect = [self.client.PROMPT, TIMEOUT, '\n', '\r']
            index = self.client.expect(expect)
            output = ''
            while True:
                buffer = self.client.before
                if index < 2:
                    output += buffer
                    if print_function:
                        print_function(buffer)
                    break
                output += buffer + expect[index]
                if print_function:
                    print_function(buffer + expect[index])
                index = self.client.expect(expect)
            self.client.sendline("echo $?")
            # ignore send cmd
            self.client.expect('\n')

            self.client.prompt()
            return int(self.client.before.strip()), output
        except TIMEOUT:
            raise CliRuntimeError("SSH connection timed out. Please check that SSH access is possible.")

    def get_output(self, cmd):
        stdin, stdout, stderr = self.paramiko.exec_command(cmd)
        return "".join(stdout.readlines()).join(stderr.readlines())

    def send_file(self, src, dst):
        sftp = self.paramiko.open_sftp()
        sftp.put(src, dst)
