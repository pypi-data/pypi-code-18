from coreapi import Document, Link, Field
import re
from .document import Link


def parse_spore_description(data, base_url=None):
    schema_url = base_url if base_url is not None else data.get('base_url')
    if 'meta' in data and 'documentation' in data.get('meta'):
        description = data['meta']['documentation']
    else:
        description = ''

    spore_methods = data.get('methods')
    content = {}

    for method in spore_methods.items():
        action, keys, link = _get_link_from_method(method)

        base_dict = content
        for key in keys:
            base_dict = base_dict.setdefault(key, {})
        base_dict[action] = link

    return Document(
        title=data.get('name'),
        url=schema_url,
        description=description,
        content=content,
        media_type='application/sporeapi+json'
    )


def _get_link_from_method(method):
    spore_name, spore_method = method
    action, *keys = spore_name.split('_')
    link = Link(
        url=spore_method.get('path'),
        action=spore_method.get('method').lower(),
        title=spore_method.get('description',
                               spore_name.replace('_', ' ').capitalize()),
        authentication=spore_method.get('authentication', False),
        formats=spore_method.get('formats', []),
        fields=_get_fields_from_method(spore_method),
        description=spore_method.get('documentation', '')
    )
    return action, keys, link


def _get_fields_from_method(spore_method):
    fields = []
    required_params = spore_method.get('required_params', [])
    path = spore_method.get('path')
    optional_params = spore_method.get('optional_params', [])

    for param in required_params:
        if re.search(r'\{%s\}' % param, path):
            location = 'path'
        else:
            location = 'query'
        fields.append(
            Field(
                name=param,
                required=True,
                location=location,
                description=spore_method.get('documentation', '')
            )
        )

    for param in optional_params:
        fields.append(
            Field(
                name=param,
                required=False,
                location='query',
                description=spore_method.get('documentation', '')
            )
        )

    return fields
