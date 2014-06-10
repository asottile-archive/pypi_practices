from __future__ import absolute_import
from __future__ import unicode_literals

import io
import mock
import os.path
import pytest
import sys

from pypi_practices import five
from pypi_practices.errors import FileValidationError
from pypi_practices.make_entry import make_entry
from testing.util import REMatcher


# pylint:disable=redefined-outer-name


def fake_load_config(_):
    return {
        'autofix': False,
        'github_user': 'asottile',
        'package_name': 'pypi_practices',
        'repo_description': 'Description of pypi_practices',
    }


@pytest.yield_fixture
def fake_entry():
    class fake_entry_state(object):
        cwd_arg = None
        config_arg = None
        entry = None

    def check_fn(cwd, fix, config):
        fake_entry_state.cwd_arg = cwd
        fake_entry_state.fix_arg = fix
        fake_entry_state.config_arg = config
        return 0

    fake_entry_state.check_fn = staticmethod(check_fn)
    fake_entry_state.entry = staticmethod(make_entry(check_fn))
    yield fake_entry_state


@pytest.yield_fixture
def fake_entry_with_config(fake_entry):
    fake_entry.entry = staticmethod(make_entry(
        fake_entry.check_fn, load_config_fn=fake_load_config,
    ))
    yield fake_entry


def test_converts_args_to_text(fake_entry_with_config):
    # Native str (py2 vs py3)
    args = [str('--cwd'), str('path')]
    fake_entry_with_config.entry(args)
    assert type(fake_entry_with_config.cwd_arg) is five.text
    assert fake_entry_with_config.cwd_arg == 'path'


def test_cwd_defaults_to_dot(fake_entry_with_config):
    fake_entry_with_config.entry([])
    assert fake_entry_with_config.cwd_arg == '.'


def test_fix_calls_fix(fake_entry_with_config):
    fake_entry_with_config.entry(['--fix'])
    assert fake_entry_with_config.fix_arg is True


def test_ignores_extra_filename_args(fake_entry_with_config):
    fake_entry_with_config.entry(['README.md', 'tox.ini'])
    assert fake_entry_with_config.cwd_arg == '.'


@pytest.mark.parametrize('args', ([], ['--fix']))
def test_returns_0_for_ok(fake_entry_with_config, args):
    ret = fake_entry_with_config.entry(args)
    assert ret == 0


def test_no_args_passed_uses_sys_argv(fake_entry_with_config):
    with mock.patch.object(sys, 'argv', ['hook-exe', '--cwd', 'foo_cwd']):
        fake_entry_with_config.entry()
        assert fake_entry_with_config.cwd_arg == 'foo_cwd'


@pytest.yield_fixture
def print_mock():
    with mock.patch.object(five.builtins, 'print') as print_mock:
        yield print_mock


def test_ok_prints_nothing(fake_entry_with_config, print_mock):
    fake_entry_with_config.entry([])
    assert print_mock.call_count == 0


def test_raises_validation_error(print_mock):
    def raising_check(*_):
        raise FileValidationError(
            errors=[('README.md', 0, 'Missing something.')],
        )

    entry = make_entry(raising_check, load_config_fn=fake_load_config)
    ret = entry([])
    assert ret == 1
    print_mock.assert_called_once_with('README.md:0: Missing something.')


def test_passes_config(tmpdir, fake_entry):
    config_path = os.path.join(tmpdir.strpath, '.pypi-practices-config.yaml')
    with io.open(config_path, 'w') as config_file:
        config_file.write(
            'autofix: true\n'
            'github_user: asottile\n'
            'package_name: pypi_practices\n'
            'repo_description: Best practices for python packaging\n'
        )

    ret = fake_entry.entry(['--cwd', tmpdir.strpath])
    assert ret == 0
    assert fake_entry.config_arg == {
        'autofix': True,
        'github_user': 'asottile',
        'package_name': 'pypi_practices',
        'repo_description': 'Best practices for python packaging'
    }


def test_failing_config(tmpdir, fake_entry, print_mock):
    config_path = os.path.join(tmpdir.strpath, '.pypi-practices-config.yaml')
    with io.open(config_path, 'w') as config_file:
        config_file.write('foo: "')

    ret = fake_entry.entry(['--cwd', tmpdir.strpath])
    assert ret == 1
    print_mock.assert_called_once_with(REMatcher(
        r'.pypi-practices-config.yaml: Invalid Yaml:\n\n'
        r'while scanning a quoted scalar\n'
        r'  in ".+\.pypi-practices-config.yaml", line 1, column 6\n'
        r'found unexpected end of stream\n'
        r'  in ".+/.pypi-practices-config.yaml", line 1, column 7'
    ))
