# -*- coding: utf-8 -*-
import sys
import requests
import click

@click.command()
@click.version_option('1.2')
@click.argument('css_file', type=click.Path(exists=True))
def main(css_file):

    # Grab the file contents
    with open(css_file, 'r') as c:
        css = c.read()

    # Pack it, ship it
    payload = {'input': css}
    url = 'https://cssminifier.com/raw'
    click.secho("Requesting mini-me of {}. . .".format(c.name), fg='green', bold=True)
    r = requests.post(url, payload)

    # Write out minified version
    minified = css_file.rstrip('.css')+'.min.css'
    with open(minified, 'w') as m:
        m.write(r.text)

    click.secho("Minification complete. See {}".format(m.name), fg='green', bold=True)



if __name__ == '__main__':
    main()
