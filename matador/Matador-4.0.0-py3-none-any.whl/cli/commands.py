import sys
import io
import click
import yaml
from dulwich.repo import Repo
from pathlib import Path
from importlib.machinery import SourceFileLoader
from cookiecutter.main import cookiecutter
from matador.cli.decorators import windows_only, deploys_changes
import matador.cli.utils as utils
from matador import git, zippey


@click.version_option(message='%(prog)s version %(version)s')
@click.group()
def matador():
    pass


@matador.command(name='init')
@click.option('--project', '-p', prompt='Project Name')
def create_project(project):
    cookiecutter(
        'https://github.com/Empiria/matador-cookiecutter.git',
        no_input=True,
        extra_context={'project_name': project})
    click.echo(f'Created matador project {project}')


@matador.command(name='create-ticket')
@click.option('--ticket', '-t', prompt='Ticket')
def create_ticket(ticket):
    project_repo = Repo.discover()
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', ticket)
    Path.mkdir(ticket_folder, parents=True, exist_ok=True)

    for file_name in ('deploy.py', 'remove.py'):
        file = Path(ticket_folder, file_name)
        with file.open('w') as f:
            f.write('from matador.deployment import *\n\n')
        git.stage_file(project_repo, file)

    git.commit(project_repo, f'Create ticket {ticket}')
    click.echo(f'Created ticket {ticket}')


@matador.command(name='create-package')
@click.option('--package', '-p', prompt='Package')
def create_package(package):
    project_repo = Repo.discover()
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    Path.mkdir(package_folder, parents=True, exist_ok=True)

    package_file = Path(package_folder, 'tickets.yml')
    with package_file.open('w') as f:
        f.write(
            '# List each ticket on a separate line preceded by - . e.g.\n')
        f.write('# - 30\n')
        f.write('# - 31\n')
    git.stage_file(project_repo, package_file)

    remove_file = Path(package_folder, 'remove.py')
    with remove_file.open('w') as f:
        f.write('from matador.deployment import *\n\n')

    git.stage_file(project_repo, remove_file)
    git.commit(project_repo, f'Create package {package}')
    click.echo(f'Created package {package}')


@matador.command(name='add-t2p')
@click.option('--ticket', '-t', prompt='Ticket')
@click.option('--package', '-p', prompt='Package')
def add_ticket_to_package(ticket, package):
    project_repo = Repo.discover()
    package_file = Path(
        project_repo.path, 'deploy', 'packages', package, 'tickets.yml')

    with package_file.open('a') as f:
        f.write(f'- {ticket}\n')

    git.stage_file(project_repo, package_file)
    git.commit(project_repo, f'Add ticket {ticket} to package {package}')
    click.echo(f'Added ticket {ticket} to package {package}')


@matador.command(name='deploy-ticket')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--ticket', '-t', prompt='Ticket')
@click.option('--commit', '-c', default=None)
@click.option('--packaged', '-p', is_flag=True, default=False)
@deploys_changes
def deploy_ticket(environment, ticket, commit, packaged):
    click.echo(f'Deploying ticket {ticket} to {environment}')
    deployment_folder = utils.ticket_deployment_folder(
        environment, ticket, commit, packaged)
    source_file = Path(deployment_folder, 'deploy.py')
    SourceFileLoader('deploy', str(source_file)).load_module()


@matador.command(name='remove-ticket')
@click.option('--ticket', '-t', prompt='Ticket')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--commit', '-c', default=None)
@click.option('--packaged', '-p', is_flag=True, default=False)
@deploys_changes
def remove_ticket(environment, ticket, commit, packaged):
    click.echo(f'Removing ticket {ticket} from {environment}')
    deployment_folder = utils.ticket_deployment_folder(
        environment, ticket, commit, packaged)
    source_file = Path(deployment_folder, 'remove.py')
    SourceFileLoader('remove', str(source_file)).load_module()


@matador.command(name='deploy-package')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--package', '-p', prompt='Package')
@click.option('--commit', '-c', prompt='Commit Ref')
def deploy_package(environment, package, commit):
    click.echo(f'Deploying package {package} to {environment}')
    tickets_file = utils.package_definition(environment, package, commit)
    with tickets_file.open('r') as f:
        for ticket in yaml.load(f):
            click.echo('*' * 25)
            click.echo(f'Deploying ticket {ticket} to {environment}')
            deployment_folder = utils.ticket_deployment_folder(
                environment, ticket, commit, True)
            source_file = Path(deployment_folder, 'deploy.py')
            SourceFileLoader('deploy', str(source_file)).load_module()
            click.echo('')


@matador.command(name='remove-package')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--package', '-p', prompt='Package')
@click.option('--commit', '-c', prompt='Commit Ref')
def remove_package(environment, package, commit):
    click.echo(f'Removing package {package} from {environment}')
    tickets_file = utils.package_definition(environment, package, commit)
    with tickets_file.open('r') as f:
        for ticket in yaml.load(f):
            click.echo('*' * 25)
            click.echo(f'Removing ticket {ticket} from {environment}')
            deployment_folder = utils.ticket_deployment_folder(
                environment, ticket, commit, True)
            source_file = Path(deployment_folder, 'deploy.py')
            SourceFileLoader('remove', str(source_file)).load_module()
            click.echo('')


@matador.command(name='run-sql-script')
@click.option('--environment', '-e', prompt='Environment')
@click.argument('file', type=click.File('r'))
@deploys_changes
def run_sql_script(environment, file):
    click.echo(f'Executing {file} against {environment}')
    kwargs = {
        **utils.environment()[environment]['database'],
        **utils.credentials()[environment]
    }
    kwargs['directory'] = str(Path(file).parent),
    kwargs['file'] = str(Path(file).name)
    run_sql_script(**kwargs)


@matador.command(name='smudge-zip')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def smudge_zip(input, output):
    input = io.open(sys.stdin.fileno(), 'rb')
    output = io.open(sys.stdout.fileno(), 'wb')
    zippey.init()
    zippey.decode(input, output)


@matador.command(name='clean-zip')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def clean_zip(input, output):
    input = io.open(sys.stdin.fileno(), 'rb')
    output = io.open(sys.stdout.fileno(), 'wb')
    zippey.init()
    zippey.encode(input, output)


@matador.command(name='start-service')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--service', '-s', prompt='Service')
@windows_only
def start_service(environment, service):
    click.echo(f'Starting {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.start(service, services[service])


@matador.command(name='restart-service')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--service', '-s', prompt='Service')
@windows_only
def restart_service(environment, service):
    click.echo(f'Restarting {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.restart(service, services[service])


@matador.command(name='stop-service')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--service', '-s', prompt='Service')
@windows_only
def stop_service(environment, service):
    click.echo(f'Stopping {service} on {environment}')
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    abw_service.stop(service, services[service])


@matador.command(name='service-status')
@click.option('--environment', '-e', prompt='Environment')
@click.option('--service', '-s', prompt='Service')
@windows_only
def service_status(environment, service):
    from matador.cli import abw_service
    services = utils.environment()[environment]['services']
    is_running = abw_service.is_running(services[service])
    click.echo(abw_service.is_running_message(is_running, service))
