'''
modeldocs

Documentation generator for your model subclasses.
'''

__title__ = 'modeldocs'
__version__ = '0.1.1'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Johan Nestaas'


def main():
    import json
    import argparse
    from .document import Document
    parser = argparse.ArgumentParser(prog='modeldocs')
    parser.add_argument('--config', '-c', default='modeldocs.json')
    parser.add_argument('--output', '-o', default='docs')
    parser.add_argument('--include', '-i', nargs='*')
    args = parser.parse_args()
    with open(args.config) as f:
        config = json.load(f)
    if args.include:
        config['include'] = args.include
    elif 'include' not in config:
        config['include'] = ['.']
    doc = Document(**config)
    doc.generate_docs(config['include'])
    doc.output(args.output)


if __name__ == '__main__':
    main()
