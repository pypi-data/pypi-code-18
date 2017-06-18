# pylint: disable=wildcard-import, unused-wildcard-import, unused-import, missing-docstring, invalid-name
"""Test 'templating' module."""
import os
import mock
import pytest

from hypershot.templating import *

BUILTINS = "bbcode json links plain yaml".split()
EMPTY_NS = dict(settings={}, videos={}, images=[])
FAKE_URL = 'http://example.com/test.png'


@pytest.mark.parametrize('name', BUILTINS)
def test_load_builtin_template(name):
    text = load(name, True)
    lines = text.splitlines()

    assert text.startswith('{#')
    assert lines[0].endswith('#}')
    assert '[built-in]' in lines[0]
    assert len(lines) >= 2


@pytest.mark.parametrize('name', ['really/bad/name', 'really_bad_name'])
def test_load_raises_on_bad_names(empty_config_dir, name):
    with empty_config_dir:
        with pytest.raises(ValueError):
            load(name)


def test_inventory_returns_builtin_templates(empty_config_dir):
    with empty_config_dir:
        templates = dict(inventory())

    assert len(templates) >= len(BUILTINS)
    assert set(templates) >= set(BUILTINS)
    assert all('[built-in]' in x for x in templates.values())


def test_inventory_scans_config_dir(filled_config_dir):
    with filled_config_dir:
        templates = dict(inventory())

    assert 'test' in templates
    assert 'Custom' in templates['test']
    assert 'data/nodescription.j2' in templates['nodescription']


@pytest.mark.parametrize('name', ['bbcode', 'links', 'yaml', 'nodescription'])
def test_render_template_with_fake_URL(filled_config_dir, name):
    namespace = EMPTY_NS.copy()
    namespace['images'] = [dict(hypershot=dict(link=FAKE_URL))]

    with filled_config_dir:
        text = render(name, namespace)

    assert FAKE_URL in text


def test_render_custom_template_from_config(filled_config_dir):
    with filled_config_dir:
        text = render('test', {})

    assert text.rstrip() == ''


def test_render_custom_template_from_path(empty_config_dir):
    testfile = os.path.join(os.path.dirname(__file__), 'data', 'test.j2')
    with empty_config_dir:
        text = render(testfile, {})

    assert text.rstrip() == ''
