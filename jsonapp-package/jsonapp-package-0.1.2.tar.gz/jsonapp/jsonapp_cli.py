# -*- coding: utf-8 -*-

import click
from jsonapp.core.jsonapp_main import json_app, user_output, script_output


@click.group()
def cli():
    pass


@cli.command('format')
@click.option('--clipboard', is_flag=True, default=False,
              help='Get JSON input from clipboard. Set formatted JSON result to clipboard.')
@click.option('--input', 'json_string', help='JSON string for formatting.')
@click.option('--copy-to-clipboard', is_flag=True, default=False, help='Copy formatted json to clipboard.')
@click.option('--output', type=click.Choice([user_output, script_output]), default=user_output,
              help='Output format', show_default=True)
@click.option('--pager', is_flag=True, default=False, help='User pager for long output.')
@click.pass_context
def format(ctx, clipboard, json_string, copy_to_clipboard, output, pager):

    result = json_app.run(
        clipboard=clipboard,
        json_string=json_string,
        copy_to_clipboard=copy_to_clipboard,
        output=output,
        pager=pager
    )

    if result.failure:
        print(ctx.get_help())
        return


if __name__ == "__main__":
    cli()
