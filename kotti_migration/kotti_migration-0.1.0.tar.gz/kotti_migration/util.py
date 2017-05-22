
import time
import uuid
import json
import re
import subprocess
import transaction
from uuid import UUID
from datetime import datetime, date
from unicodedata import normalize
from sqlalchemy.exc import IntegrityError

from kotti import DBSession
from kotti.resources import Content
from kotti.resources import LocalGroup
from kotti_migration import config


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def uuid_factory():
    return uuid.uuid4()


def format_email_username(user):
    return '"{}" <{}>'.format(user.title, user.email)


def file_endswith(string, *args):
    extensions = '|'.join(args)
    return re.match(r'.*\.('+extensions+')$', string)


def chunk_list(ls, n):
    return [ls[i:i+n] for i in xrange(0, len(ls), n)]


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    text = unicode(text)
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def unslugify(text, delim=u'-'):
    return text.replace(delim, " ")


def list_to_tuple(ls):
    return [(v,v) for v in ls]

def dict_to_tuple(dt):
    return [(k,v) for k,v in dt.items()]

def to_int(value, default=None, ceiling=True):
    try:
        if ceiling:
            return int(round(value))
        return int(value)
    except TypeError:
        return default


def json_value(value):
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [json_value(v) for v in value]
    if isinstance(value, long):
        # Big numbers are sent as strings for accuracy in JavaScript
        if value > 9007199254740992 or value < -9007199254740992:
            return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, LocalGroup):
        return {
            'principal_name': value.principal_name,
            'id': value.id,
            'node_id': value.node_id,
            'group_name': value.group_name
        }
    return value


def export(context, recursively=True):
    context_data = export_base(context)
    if recursively:
        context_data["children"] = export_children(context, recursively=recursively)
    return context_data


def export_children(context, recursively=True):
    children = context.children
    context_children = {}
    for child in children:
        context_children[child.name] = export(child, recursively=recursively)
    return context_children


def export_base(context):
    context_data = {}

    _data = context.__dict__

    keys = [k for k in context.__mapper__.columns.keys() if not k.startswith("_")]
    keys.append('local_groups')
    keys.append('position')

    for key in keys:
        context_data[key] = json_value(_data[key])

    context_data["__class__"] = "{0}.{1}".format(
        context.__class__.__module__,
        context.__class__.__name__
    )
    context_data["__foreign_keys__"] = {}
    for fk in context.__table__.foreign_keys:
        context_data["__foreign_keys__"][fk.parent.name] = "{}.{}".format(
            str(fk.column.table.name),
            str(fk.column.name)
        )
    return context_data


def import_data(base, context_data, recursively=True):
    _class_path = context_data["__class__"].rsplit(".", 1)
    if ".".join(_class_path) in config.ignore_content_types:
        return
    _class = get_content_type(
        content_type=_class_path[1],
        package=_class_path[0])

    default_attrs = {
        k: v for k,v in context_data.iteritems() if (
            not k.startswith("_") and k not in config.ignore_attrs
        )
    }
    base[context_data["name"]] = context = _class(**default_attrs)
    if recursively:
        import_children(base[context_data["name"]], context_data, recursively=recursively)



def import_children(context, context_data, recursively=True):
    children_data = context_data["children"]
    for child_name, child in children_data.iteritems():
        if child_name not in context:
            import_data(context, child)
        else:
            import_children(context[child_name], child)





def get_content_type(content_type, package="."):
    """ Get Content from kotti package.

    :param content_type:       Class name of the content type
    :param package:            Package path of the content type
    :returns:                  Content type

    """
    imported = getattr(__import__(package, fromlist=[content_type]), content_type)
    return imported


def find_key(d, val):
    return d.keys()[d.values().index(val)]


def remove_duplicates(list1):
    return reduce(lambda r, v: v in r and r or r + [v], list1, [])


def merge_list(list1, list2):
    """Remove duplicate values after merging the two lists"""
    return remove_duplicates((list1 or []) + (list2 or []))
