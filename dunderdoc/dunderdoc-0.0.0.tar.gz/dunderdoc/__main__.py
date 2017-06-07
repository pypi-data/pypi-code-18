import click

from .dunders import dunder_dict



def print_dunder(dunder):
    s = '''\
{method}: {reason}
    section: {section}
    Usage: {usage}

    Example implementation:
    {example}
    ''' \
        .format(
        method=dunder.method, reason=dunder.reason, section=dunder.section.value,
        usage=dunder.usage, example=dunder.example)
    print(s)


@click.group()
def cli():
    pass

@click.command()
def print_all():
    for c, v in dunder_dict.items():
        print_dunder(v)

@click.command()
@click.argument('name')
def find_dunder(name):
    try:
        print_dunder(dunder_dict[name])
    except KeyError:
        print('Dunder method {} not found.'.format(name))


cli.add_command(print_all, name='print')
cli.add_command(find_dunder, name='find')

if __name__ == '__main__':
    cli()