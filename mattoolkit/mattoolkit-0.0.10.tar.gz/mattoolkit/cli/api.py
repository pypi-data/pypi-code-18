from collections import defaultdict

import click

from . import cli
from ..api import api as mtk_api, resource_representation


@cli.command()
@click.argument('resource', type=click.Choice(['structures', 'calculations', 'clusters', 'clusterjobs', 'users']))
@click.argument('uuid', required=False, default=None)
@click.option('-o', '--option', multiple=True, default=[])
def api(resource, uuid, option):
    rec = resource_representation(resource, uuid)
    # Collect query parameters
    if uuid is None:
        query_params = defaultdict(list)
        for opt in option:
            if '=' not in opt:
                raise ValueError('must give search option as "name=value"')
            name, value = opt.split('=', 1)
            query_params[name].append(value)
        rec.query(**query_params)
    else:
        if option:
            print('Warning: Ignoring options since item id was specified')
        rec.get()
    print(rec)
