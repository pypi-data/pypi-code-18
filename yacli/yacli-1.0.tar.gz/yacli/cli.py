import os, sys, click, fabric
from fabric import api as fa

CONTEXT_SETTINGS = dict(auto_envvar_prefix='YACLI')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Context(object):

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
        self.level = 0

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def increment_indent(self):
        self.level += 1

    def decrement_indent(self):
        if self.level > 0: 
            self.level -= 1

    def indent(self):
        res=""
        for i in range(self.level):
            res += self.indent_character
        return res

pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'commands'))

class YacliCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('yacli.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=YacliCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-h', '--home', envvar='ACTITO_HOME', 
        type=click.Path(exists=True, file_okay=False, resolve_path=True),
        help='Changes the home directory (default: $ACTITO_HOME)')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('-u', '--user', envvar='USER', 
        help='Default user for ssh connection (default: $USER)')
@pass_context
def cli(ctx, verbose, home, user):
    """Yet Another Command Line Interface."""
    ctx.verbose = verbose
    ctx.indent_character="  "
    if home is not None:
        ctx.home = home

    fa.env.use_ssh_config = True
    fa.env.user = user
    fa.env.sudo_user = 'root'
    fa.env.key_filename = '~/.ssh/id_rsa'
    fa.env.output_prefix = False
















# ---------------------------------------------------------------------
# Old classes
# ---------------------------------------------------------------------


class ProjectBranch(object):

    GROUP_BY_BRANCH='branch'
    GROUP_BY_PROJECT='project'

    def __init__(self, group_by, level=0):
        self.output={}
        self.group_by=group_by
        self.level=level
        self.pre_indentation = self.indentation_level()

    def add(self, branch, project):
        if 'branch' in self.group_by:
            self.output.setdefault(branch, []).append(project)
        elif 'project' in self.group_by: 
            self.output.setdefault(project, []).append(branch)
        else :
            raise Exception('Invalid group-by option!', group_by)

    def indentation_level(self):
        pre=""
        for i in range(self.level) :
            pre+="\t"
        return pre

    def list_key(self):
        res=[]
        for key in self.output :
            res.append("{}{}".format(self.pre_indentation, key))
        return '\n'.join(res)

    def __str__(self):
        res=[]
        for key in self.output :
            res.append("{}{}".format(self.pre_indentation, key))
            for value in self.output[key]:
                res.append("{}\t{}".format(self.pre_indentation, value))

        return '\n'.join(res)
