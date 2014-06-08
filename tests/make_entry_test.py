from __future__ import unicode_literals

import mock
import pytest
import sys

from pypi_practices import five
from pypi_practices.errors import FileValidationError
from pypi_practices.make_entry import make_entry


# pylint:disable=redefined-outer-name

noop = mock.Mock()


@pytest.yield_fixture
def fake_entry():
    class fake_entry_state(object):
        check_called_cwd = None
        fix_called_cwd = None
        entry = None

    def check_fn(cwd):
        fake_entry_state.check_called_cwd = cwd
        return 0

    def fix_fn(cwd):
        fake_entry_state.fix_called_cwd = cwd
        return 0

    fake_entry_state.entry = staticmethod(make_entry(check_fn, fix_fn))
    yield fake_entry_state


def test_converts_args_to_text(fake_entry):
    # Native str (py2 vs py3)
    args = [str('--cwd'), str('path')]
    fake_entry.entry(args)
    assert type(fake_entry.check_called_cwd) is five.text
    assert fake_entry.check_called_cwd == 'path'


def test_cwd_defaults_to_dot(fake_entry):
    fake_entry.entry([])
    assert fake_entry.check_called_cwd == '.'


def test_fix_calls_fix(fake_entry):
    fake_entry.entry(['--fix'])
    assert fake_entry.fix_called_cwd == '.'


def test_ignores_extra_filename_args(fake_entry):
    fake_entry.entry(['README.md', 'tox.ini'])
    assert fake_entry.check_called_cwd == '.'


@pytest.mark.parametrize('args', ([], ['--fix']))
def test_returns_0_for_ok(fake_entry, args):
    ret = fake_entry.entry(args)
    assert ret == 0


def test_no_args_passed_uses_sys_argv(fake_entry):
    with mock.patch.object(sys, 'argv', ['hook-exe', '--cwd', 'foo_cwd']):
        fake_entry.entry()
        assert fake_entry.check_called_cwd == 'foo_cwd'


@pytest.yield_fixture
def print_mock():
    with mock.patch.object(five.builtins, 'print') as print_mock:
        yield print_mock


def test_ok_prints_nothing(fake_entry, print_mock):
    fake_entry.entry()
    assert print_mock.call_count == 0


def test_raises_validation_error(print_mock):
    def raising_check(_):
        raise FileValidationError(
            'README.md',
            'Missing something.'
        )

    entry = make_entry(raising_check, noop)
    ret = entry([])
    assert ret == 1
    print_mock.assert_called_once_with(
        'README.md: Missing something.\n'
        '\n'
        'Manually edit the file above to fix.'
    )


def test_message_contains_line_if_specified(print_mock):
    def raising_check_with_line_number(_):
        raise FileValidationError(
            'README.md',
            'Missing something.',
            line=5,
        )

    entry = make_entry(raising_check_with_line_number, noop)
    ret = entry([])
    assert ret == 1
    print_mock.assert_called_once_with(
        'README.md:5: Missing something.\n'
        '\n'
        'Manually edit the file above to fix.'
    )


def test_auto_fixable_prints_auto_fixable(print_mock):
    def raising_check_auto_fixable(_):
        raise FileValidationError(
            'README.md',
            'Missing something.',
            is_auto_fixable=True,
        )

    entry = make_entry(raising_check_auto_fixable, noop)
    ret = entry([])
    assert ret == 1
    print_mock.assert_called_once_with(
        'README.md: Missing something.\n'
        '\n'
        'To attempt automatic fixing, run with --fix.'
    )
