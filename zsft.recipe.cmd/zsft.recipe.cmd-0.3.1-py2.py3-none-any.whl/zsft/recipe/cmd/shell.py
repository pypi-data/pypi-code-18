import sys
import os
import logging
import shutil
import tempfile
import zc.buildout
from subprocess import check_call

def _env(env):
    """Parse multiline KEY=VALUE string into dict."""
    return dict((key.strip(), val)
         for line in env.strip().splitlines()
             for key, _, val in line.partition('='))

class ShellRecipe(object):
    """zc.buildout recipe to execute commands with shell"""

    def __init__(self, buildout, name, options):
        """Recipe constructor"""
        self.log      = logging.getLogger(name)
        self.buildout = buildout
        self.name     = name
        self.options  = options
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'], name)

    def _execute(self, content, env={}, shell='', shell_opts=''):
        """Execute code with given shell by creating temporary script"""
        log = self.log
        name = self.name
        options = self.options
        buildout = self.buildout

        path = tempfile.mkdtemp()
        try:
            env = dict(os.environ, **env)
            suffix = ''
            if os.name == 'nt': # TODO: jython?
                suffix = '.ps1' if 'powershell' in shell.lower() else '.bat'
            script = os.path.join(path, 'run'+suffix)

            if not shell:
                if os.name == 'nt':
                    shell = os.environ.get('COMSPEC', 'COMMAND.COM')
                    shell_opts = '/c'
                else:
                    shell = os.environ.get('SHELL', '/bin/sh')
                    shell_opts = ''

            with open(script, 'w') as f:
                f.write(content)
            del f

            if shell == 'internal':
                self.log.debug('Executing python code: %r', content)
                exec(content)
            else:
                command = list(filter(None, [shell, shell_opts, script]))
                self.log.debug('Executing: %r, shell=%r', command, shell)
                check_call(command, env=env)
        finally:
            shutil.rmtree(path)

    def _process(self, prefix):
        """Common logic for both install and update"""
        options = self.options
        script = options.get(prefix, '').strip()
        if script:
            env = _env(options.get(prefix+'-env') or options.get('env') or '')
            shell = (options.get(prefix+'-shell')
                          or options.get('shell') or '')
            shell_opts = (options.get(prefix+'-shell-options') or 
                                  options.get('shell-options') or '')
            self.log.info('Executing %s script', prefix)
            self._execute(script, env=env, shell=shell, shell_opts=shell_opts)
        return ()

    def install(self):
        """Execute script on install phase"""
        return self._process('install')

    def update(self):
        """Execute script on update phase"""
        return self._process('update')
