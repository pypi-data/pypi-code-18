#!/usr/bin/env python
import click
import webbrowser

"""
Groups all commands under the "v-one" command.
"""
@click.group()
def cli():
    """SproutLoud VersionOne CLI Tool"""


"""
Opens a new tab or window in the current browser and directs that tab to 
the link location with provided parameter.

@param string num  The story, feature, or epic number
"""
@cli.command()
@click.argument('num')

def view(num):
    """View story, epic, or feature in browser."""

    url = "https://www9.v1host.com/SproutLoud/Search.mvc/Advanced?q=" + str(num)
    webbrowser.open_new_tab(url)