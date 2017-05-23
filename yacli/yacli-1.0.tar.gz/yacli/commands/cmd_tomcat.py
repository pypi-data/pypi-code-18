import click, os, sys, io
from yacli.cli import pass_context
from fabric import api as fa

BUILD = ['build']
DEV   = ['dev-1', 'dev-2']
TEST  = ['test-1', 'test-4']
PROD  = ['prod-a1','prod-a2','prod-1','prod-2','prod-3','prod-4','prod-5','prod-6']

ENVS  = { 'build' : BUILD, 'dev' : DEV, 'test' : TEST, 'prod' : PROD }

CMD_TRAIL       = "tr '\n' ' '"
CMD_LIST = "find /srv/tomcat/ -name '*all.log' \
        | grep '{}' \
        | sed 's/\/srv\/tomcat\///' \
        | sed 's/logs\///' \
        | sed 's/-all.log//'"

CMD_TOMCAT_LIST = "find /srv/tomcat/ -name '*all.log' \
        | grep '{}' \
        | grep -E '/srv/tomcat/([^/]*)' -o \
        | sed 's/\/srv\/tomcat\///' \
        | uniq"

CMD_RESTART = "find /srv/tomcat/ -name '*all.log' \
        | grep '{}' \
        | grep -E '/srv/tomcat/([^/]*)' -o \
        | sed 's/\/srv\/tomcat\///' \
        | uniq \
        | while read i; do sudo /etc/init.d/tomcat-${{i}} restart; done"

@click.command('tomcat', short_help='Give information about tomcat in environment')
@click.argument('env', required=True)
@click.argument('pattern', default='', required=False)
@click.option('-l', '--list', is_flag=True, default=False,  help='List tomcat and application')
@click.option('-r', '--restart', is_flag=True, default=False, help='Restart tomcat')
@click.option('-t', '--only-tomcat', is_flag=True, default=False, help='Show only tomcat name')
@pass_context
def cli(ctx, env, pattern, list, restart, only_tomcat):
    """Give information about tomcat in environment"""
    env = env.lower()
    if env not in ENVS:
        env = click.prompt('Enter a valid env')
        pattern = click.prompt('Pattern')


    stdout=click.get_text_stream('stdout')

    for host in ENVS[env] :
        with fa.settings(host_string=host):
            ctx.log("Host {}".format(host))
            with fa.hide('running'):
                if only_tomcat:
                    fa.run(CMD_TOMCAT_LIST.format(pattern), stdout=stdout)
                else:
                    fa.run(CMD_LIST.format(pattern), stdout=stdout)

    if restart and click.confirm('Restart these tomcat?') and \
            (not env == 'prod' or click.confirm('You will restart PROD! Are you sur?')):
        for host in ENVS[env] :
            with fa.settings(host_string=host):
                ctx.log("Restart on {}".format(host))
                with fa.hide('running'):
                    fa.sudo(CMD_RESTART.format(pattern), stdout=stdout, shell=False)
