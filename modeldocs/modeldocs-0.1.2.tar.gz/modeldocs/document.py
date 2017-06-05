import os
import re
import sys
import json
from shutil import copytree
from enum import Enum


RE_DOCSTR = re.compile(
    r'.*class (?P<classname>\w+)(?:\((?P<bases>[^\)]*?)\))?:\s*'
    r'(?:\'\'\'|""")(?P<docstr>.*?)(?:\'\'\'|""")',
    flags=re.MULTILINE | re.DOTALL,
)
RE_SINGLE = re.compile(
    r'\s*@model(?P<tag>Group|Title|Description|Version)\s+(?P<value>.*)$'
)
RE_EXAMPLE = re.compile(
    r'\s*@modelExample\s+{(?P<format>[^}]+)}\s+(?P<title>.*)'
)
RE_FIELD = re.compile(
    r'\s*@modelField\s+{(?P<type>[^=}]*)(=(?P<options>[^}]*))?}\s+'
    r'(?P<fullname>\[?(?P<name>\w+)(?:=(?P<default>[^\s\]]+))?\]?)\s+'
    r'(?P<description>.*?)\s*$'
)


class LabelType(Enum):
    group = 'group'
    title = 'title'
    description = 'description'
    example = 'example'
    field = 'field'
    version = 'version'


class ModelPage:

    def __init__(self, name, default_version='0.0.0', url=None):
        self.data = {
            'type': '',
            'url': url or name,
            'title': '',
            'description': '',
            'group': '',
            'version': default_version,
            'parameter': {
                'fields': {
                    'Parameter': [],
                },
                'examples': [],
            },
            'success': {
                'examples': [],
            },
            'filename': '',
            'groupTitle': '',
            'name': name,
        }
        self.ingested = False

    def ingest_example(self, match):
        example = {
            'type': match['format'],
            'title': match['title'],
            'content': match['content'],
        }
        self.data['success']['examples'].append(example)

    def ingest_field(self, match):
        optional = match['fullname'].startswith('[')
        param = {
            'group': 'Parameter',
            'type': match['type'],
            'optional': optional,
            'field': match['name'],
            'description': '<p>' + match['description'] + '</p>',
        }
        if match.get('default'):
            param['defaultValue'] = match['default']
        if match.get('options'):
            options = match['options'].split(',')
            param['allowedValues'] = options
        self.data['parameter']['fields']['Parameter'].append(param)

    def ingest(self, labeltype, match):
        self.ingested = True
        if labeltype == LabelType.group:
            self.data['group'] = match['value']
            self.data['groupTitle'] = match['value']
        elif labeltype == LabelType.title:
            self.data['title'] = match['value']
        elif labeltype == LabelType.description:
            self.data['description'] = match['value']
        elif labeltype == LabelType.version:
            self.data['version'] = match['value']
        elif labeltype == LabelType.example:
            self.ingest_example(match)
        elif labeltype == LabelType.field:
            self.ingest_field(match)
        else:
            raise NotImplementedError


class DocstrBlock:

    def __init__(self, path=None, name=None, bases=None, docstr=None):
        self.path = path
        self.name = name
        self.bases = bases
        self.docstr = docstr


class Document:

    @staticmethod
    def _path_to_module_name(path):
        fname = os.path.basename(path)
        name, ext = os.path.splitext(fname)
        if ext.lower() != '.py':
            raise ValueError('{} doesnt look like a python file'.format(path))
        return name.replace('-', '_')

    def __init__(self, default_version=None, name=None, version=None,
                 description=None, title=None, order=None, **kwargs):
        self.doc_blocks = {}
        self.project = {
            'name': name or 'Data Model Documentation',
            'version': version or '0.0.0',
            'description': description or '',
            'title': title or name or 'Data Model Documentation',
            'url': '',
            'order': order or [],
            'sampleUrl': False,
            'defaultVersion': default_version or version or '0.0.0',
            'apidoc': '0.0.1',
            'generator': {
                'name': 'modeldocs',
                'time': '2017-06-04T21:44:44.061Z',
                'url': 'http://pypi.python.org/pypi/modeldocs',
                'version': '0.0.1',
            },
        }
        self.json_output = None
        self.default_version = default_version or version or '0.0.0'

    def load_path(self, path):
        with open(path) as f:
            text = f.read()
        for classname, basestr, docstr in RE_DOCSTR.findall(text):
            print('Parsing {}::{}'.format(path, classname))
            bases = [x.strip() for x in basestr.split(',')]
            block = DocstrBlock(path=path, name=classname, bases=bases,
                                docstr=docstr)
            self.doc_blocks[(path, classname)] = block

    def load(self, paths=None, dirs=None):
        for path in paths:
            self.load_path(path)
        for d in dirs:
            for root, _, filenames in os.walk(d):
                for fname in filenames:
                    path = os.path.join(root, fname)
                    modname, ext = os.path.splitext(fname)
                    if ext.lower() != '.py':
                        continue
                    self.load_path(path)

    def parse_docline(self, line):
        if RE_SINGLE.match(line):
            match = RE_SINGLE.match(line).groupdict()
            if match['tag'] == 'Group':
                return LabelType.group, match
            elif match['tag'] == 'Title':
                return LabelType.title, match
            elif match['tag'] == 'Description':
                return LabelType.description, match
            elif match['tag'] == 'Version':
                return LabelType.version, match
        elif RE_EXAMPLE.match(line):
            match = RE_EXAMPLE.match(line).groupdict()
            match['content'] = ''
            return LabelType.example, match
        elif RE_FIELD.match(line):
            match = RE_FIELD.match(line).groupdict()
            return LabelType.field, match
        else:
            return None, None

    def parse_class_docstr(self, block):
        lines = block.docstr.splitlines()
        last_type = None
        last_match = None
        page = ModelPage(block.name, default_version=self.default_version,
                         url='{}::{}'.format(block.path, block.name))
        for line in lines:
            # if blank, ingest last and continue
            if not line.strip():
                if last_type:
                    page.ingest(last_type, last_match)
                last_type, last_match = None, None
                continue

            labeltype, match = self.parse_docline(line)
            if last_type:
                # found something and we had something
                if labeltype:
                    page.ingest(last_type, last_match)
                    last_type, last_match = labeltype, match
                # it's nothing, but we had something and it may be continuous
                else:
                    if last_type in (LabelType.description, LabelType.field):
                        last_match['description'] += ' ' + line.strip()
                    elif last_type == LabelType.example:
                        last_match['content'] += ' ' + line.strip()
            else:
                # This is the first thing we've seen in a bit
                if labeltype:
                    last_type, last_match = labeltype, match
                # otherwise, it's comments above what we care about
        # ingest that last thing we were tracking
        if last_type:
            page.ingest(last_type, last_match)
        return page

    def generate_pages(self):
        pages = []
        for path, name in self.doc_blocks:
            block = self.doc_blocks[(path, name)]
            if '@model' not in block.docstr:
                continue
            page = self.parse_class_docstr(block)
            if page.ingested:
                pages.append(page)
        return pages

    def generate_docs(self, include_paths):
        paths = []
        dirs = []
        for path in include_paths:
            if os.path.isfile(path):
                paths.append(path)
            elif os.path.isdir(path):
                dirs.append(path)
            elif not os.path.exists(path):
                print('Does not exist: {}'.format(path), file=sys.stderr)
            else:
                print('Not a file or dir: {}'.format(path), file=sys.stderr)
        self.load(paths=paths, dirs=dirs)
        pages = self.generate_pages()
        self.json_output = json.dumps([x.data for x in pages], indent=4)

    def make_dir(self, out):
        basedir = os.path.dirname(__file__)
        template_dir = os.path.join(basedir, 'templates')
        copytree(template_dir, out)

    def output(self, out):
        self.make_dir(out)
        apidata_js = os.path.join(out, 'api_data.js')
        apidata_json = os.path.join(out, 'api_data.json')
        apiproject_js = os.path.join(out, 'api_project.js')
        apiproject_json = os.path.join(out, 'api_project.json')
        project_json = json.dumps(self.project, indent=4)
        with open(apidata_json, 'w') as f:
            f.write(self.json_output)
        with open(apidata_js, 'w') as f:
            f.write('define({{ "api": {}\n}});\n'.format(self.json_output))
        with open(apiproject_json, 'w') as f:
            f.write(project_json)
        with open(apiproject_js, 'w') as f:
            f.write('define({});\n'.format(project_json))
