# pylint: disable=wildcard-import, unused-wildcard-import, unused-import, missing-docstring, invalid-name
"""Test 'cli' module."""
import os
import sys

import mock
import pytest

from hypershot import config
from hypershot.cli import *

TEST_SERVICES = dict(imgur=dict(handler='chevereto', url='https://example.com/'))


def sys_argv_mock(*args):
    cmd = ['test', '--debug', '-c', config.config_dir] + list(args)
    return mock.patch('sys.argv', cmd)


def test_docopt_called_with_h():
    with mock.patch('sys.argv', ['test', '-h']):
        with pytest.raises(SystemExit):
            parse_args()


def test_docopt_called_with_version(capsys):
    with mock.patch('sys.argv', ['test', '--version']):
        with pytest.raises(SystemExit):
            parse_args()
        out, _ = capsys.readouterr()
        words = out.split()

        assert out, "Version string is empty"
        assert words[0] == 'hypershot'
        assert words[1][0].isdigit()
        assert words[1][1] == '.'
        assert words[2] == 'from'
        assert words[3].split(os.sep)[-1] == 'hypershot'
        assert 'Python' in out
        assert len(out.rstrip().splitlines()) == 1


def test_docopt_upload():
    with mock.patch('sys.argv', ['test', 'upload', '-v', 'fake.png']):
        options, args = parse_args()

        assert args.upload is True
        assert args.image == ['fake.png']
        assert options.verbose


def test_image_service_with_empty_config():
    with mock.patch('hypershot.config.debug', True):
        with pytest.raises(SystemExit):
            image_service()


def test_unknown_image_service():
    with mock.patch('hypershot.config.services', {}):
        with pytest.raises(SystemExit):
            image_service()


def test_image_service_with_empty_settings():
    with mock.patch('hypershot.config.services', dict(imgur={})):
        with pytest.raises(SystemExit):
            image_service()


def test_image_service_with_bad_handler():
    with mock.patch('hypershot.config.services', dict(imgur=dict(handler='foobar'))):
        with pytest.raises(SystemExit):
            image_service()


def test_unknown_image_service_with_empty_config():
    with mock.patch('hypershot.config.services', TEST_SERVICES):
        handler = image_service()

        assert handler.__class__.__name__ == 'CheveretoHandler'
        assert handler.settings.enabled is True


@pytest.mark.parametrize('no_debug,exc,envvar', [
    (False, RuntimeError, 'HYPERSHOT_NO_PROGRESS'),
    (True, SystemExit, 'HYPERSHOT_NO_PROGRESS'),
    (True, SystemExit, 'HYPERSHOT_TABLE_STYLE'),
])
def test_main_with_bad_envvar(examples_config_dir, fake_netrc, no_debug, exc, envvar):
    os.environ['HYPERSHOT_DEBUG'] = '0'
    os.environ[envvar] = 'foobar'
    try:
        with examples_config_dir, fake_netrc, sys_argv_mock('templates'):
            if no_debug:
                sys.argv.remove('--debug')
            with pytest.raises(exc):
                HyperShot().main()
    finally:
        del os.environ['HYPERSHOT_DEBUG']
        del os.environ[envvar]


def test_upload_command(capsys, examples_config_dir, fake_netrc):
    with examples_config_dir, fake_netrc:
        cmd = sys_argv_mock('-n', '-s', 'imgur', '-t', 'bbcode', 'upload',
                            os.path.join(config.config_dir, '../_static/hypershot-templates.png'))
        with cmd:
            HyperShot().main()
            out, _ = capsys.readouterr()

            assert 'docs/examples/../_static/hypershot-templates.png' in out
            assert '[img]' in out


def test_services_command(capsys, examples_config_dir, fake_netrc):
    with examples_config_dir, fake_netrc, sys_argv_mock('services'):
        HyperShot().main()
        out, _ = capsys.readouterr()

        assert '\nimgur ' in out
        assert 'https://api.imgur.com  \n' in out


def test_templates_command(capsys, examples_config_dir, fake_netrc):
    with examples_config_dir, fake_netrc, sys_argv_mock('templates'):
        HyperShot().main()
        out, _ = capsys.readouterr()

        assert '\nyaml ' in out


def test_videos(capsys, examples_config_dir, fake_netrc):
    with examples_config_dir, fake_netrc, sys_argv_mock('foo.mkv'):
        HyperShot().main()
        out, _ = capsys.readouterr()

        assert 'Not implemented' in out
