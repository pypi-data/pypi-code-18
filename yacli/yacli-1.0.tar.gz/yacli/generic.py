import os, sys, click, subprocess
import paramiko
import yacli.cli
import getpass


def actito_project(ctx, clean_state=True, projects=[]):
    result = []

    ctx.vlog("Retreive actito projects in {}".format(ctx.home))
    for project in os.listdir(ctx.home) :
        git = "{}/{}".format(ctx.home, project)

        ctx.vlog("Taking {} at {}".format(project, git))

        if len(projects) != 0 and project not in projects:
            ctx.vlog("Skip {} because not in project list".format(project))
            continue

        if not os.path.isdir(git) or not os.path.isdir("{}/.git".format(git)):
            ctx.vlog("Skip {} because it's not a git dir".format(project))
            continue

        if project == 'puppet':
            ctx.vlog("Skip {} because it's puppet dir".format(project))
            continue

        if clean_state and subprocess.check_output('git -C {} status --porcelain'.format(git), shell=True):
            ctx.log("Skip {} because change need to be commit".format(project))
            continue

        result.append(git)
        ctx.vlog("Taked {}".format(project))
    
    return result

def create_cmd(cmd, *args, **kwargs) :
    return cmd + ' ' + ' '.join(args)

def cmd_call(prefix, cmd, *args) :
    stdout=click.get_text_stream('stdout')
    stderr=click.get_text_stream('stderr')

    full_cmd = create_cmd(cmd, *args)
    print full_cmd
    subprocess.call(
            '{} {}'.format(prefix, full_cmd), shell=True,
            stdout=stdout, stderr=stderr)

def cmd_check(prefix, cmd, *args) :
    full_cmd = create_cmd(cmd, *args)
    return subprocess.check_output(
            '{} {}'.format(prefix, full_cmd), shell=True)

def git_prefix(project):
    return 'git -C {}'.format(project)

def mvn_prefix(project):
    return 'mvn -f {}'.format(project)

def git_call(project, cmd, *args) :
    print project, cmd
    cmd_call(git_prefix(project), cmd, *args)

def git_check(project, cmd, *args):
    return cmd_check(git_prefix(project), cmd, *args)

def mvn_call(project, cmd, *args):
    cmd_call(mvn_prefix(project), cmd, *args)

def mvn_check(project, cmd, *args):
    return cmd_check(mvn_prefix(project), cmd, *args)






















class GroupMap(object):

    def __init__(self, ctx, key_prefix="", value_prefix=""):
        self.output = {}
        self.ctx = ctx
        self.key_prefix = key_prefix
        self.value_prefix = value_prefix

    def add(self, key, value):
        self.output.setdefault(key, []).append(value)

    def add_all(self, key, value):
        self.output.setdefault(key, []).extend(value)

    def get(self, key):
        return self.output.get(key)

    def keys(self):
        self.output.keys()

    def log_keys(self):
        for key in self.output:
            self.ctx.log.append(self.__str__key(key))
    
    def log(self, key_pattern="", value_pattern=""):
        self.ctx.log(self.__str__(key_pattern, value_pattern))

    def __str__key(self, key) :
        return '{}{}{}'.format(self.ctx.indent(), self.key_prefix, key)

    def __str__value(self, value) :
        return '{}{}{}'.format(self.ctx.indent(), self.value_prefix, value)

    def __str__(self, key_pattern="", value_pattern=""):
        res = []
        for key in [x for x in self.output if key_pattern in x] :
            res.append(self.__str__key(key))

            self.ctx.increment_indent()
            for value in [x for x in self.output[key] if value_pattern in x]:
                res.append(self.__str__value(value))
            self.ctx.decrement_indent()
        return '\n'.join(res)


class InvertGroupMap(GroupMap):

    def __init__(self, ctx, key_prefix="", value_prefix=""):
        super(InvertGroupMap, self).__init__(ctx, key_prefix, value_prefix)

    def add(self, key, value):
        self.output.setdefault(value, []).append(key)

    def add_all(self, key, value):
        self.output.setdefault(value, []).extend(key)
