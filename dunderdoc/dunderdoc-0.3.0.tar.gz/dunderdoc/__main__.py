import click

from .dunders import dunder_dict, DunderSections



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
@click.argument('section', default='all')
def print_section(section):
    if section != 'all':
        try:
            section = DunderSections[section]
        except KeyError:
            raise SystemExit('Section {} not found.'.format(section))

    for c, v in dunder_dict.items():
        if section == 'all' or v.section == section:
            print_dunder(v)


@click.command()
@click.argument('name')
def find_dunder(name):
    try:
        print_dunder(dunder_dict[name])
    except KeyError:
        print('Dunder method {} not found.'.format(name))


@click.command()
def list_sections():
    print('all')
    for section in DunderSections:
        if section.name != 'ignore':
            print(section.name)

cli.add_command(print_section, name='print')
cli.add_command(find_dunder, name='find')
cli.add_command(list_sections, name='list')


if __name__ == '__main__':
    cli()
