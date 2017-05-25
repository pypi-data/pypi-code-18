
import click


def print_with_separators(text, top_space=True):
    print(text_with_separators(text, top_space=top_space))


def print_with_separators_and_space(text, pager=False):

    text_result = text_with_separators(text, space=True)

    if pager:
        click.echo_via_pager(text_result)

    print(text_result)


def text_with_separators(text, top_space=True, space=False):

    if top_space:
        prefix = '\n'
    else:
        prefix = ''

    if space:
        space_holder = '\n'
    else:
        space_holder = ''

    separator = 90 * '-'

    result = '{prefix}{separator}{space}\n{text}\n{space}{separator}\n'.format(
        prefix=prefix,
        text=text,
        separator=separator,
        space=space_holder
    )

    return result
