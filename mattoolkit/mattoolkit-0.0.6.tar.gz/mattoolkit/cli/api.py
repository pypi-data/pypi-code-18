import click

from . import cli
from ..api import api as mtk_api, resource_representation


@cli.command()
@click.argument('resource', type=click.Choice(['structures', 'calculations', 'clusters', 'clusterjobs', 'users']))
@click.argument('uuid', required=False, default=None)
def api(resource, uuid):
    rec = resource_representation(resource, uuid)
    rec.get()
    print(rec)
