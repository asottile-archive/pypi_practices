from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path

from pypi_practices.errors import ConfigValidationError
from pypi_practices.load_config import load_config
from testing.util import assert_raises_with_msg
from testing.util import REMatcher


def test_load_config_returns_empty_dict_non_existing(tmpdir):
    ret = load_config(tmpdir.strpath)
    assert ret == {}


def _write_config_file(cwd, contents):
    path = os.path.join(cwd, '.pypi-practices-config.yaml')
    with io.open(path, 'w') as config_file:
        config_file.write(contents)


def test_load_trivial_config(tmpdir):
    _write_config_file(
        tmpdir.strpath,
        'autofix: true\n'
        'github_user: asottile\n'
        'package_name: pypi_practices\n'
    )

    assert load_config(tmpdir.strpath) == {
        'autofix': True,
        'github_user': 'asottile',
        'package_name': 'pypi_practices',
    }


def test_load_invalid_yaml(tmpdir):
    # It's surprisingly hard to make invalid yaml!
    _write_config_file(tmpdir.strpath, 'foo: "')

    with assert_raises_with_msg(
        ConfigValidationError,
        REMatcher(
            r'^.pypi-practices-config.yaml: Invalid Yaml:\n\n'
            r'while scanning a quoted scalar\n'
            r'  in ".+\.pypi-practices-config.yaml", line 1, column 6\n'
            r'found unexpected end of stream\n'
            r'  in ".+\.pypi-practices-config.yaml", line 1, column 7'
        ),
    ):
        load_config(tmpdir.strpath)


def test_valid_yaml_invalid_config(tmpdir):
    # autofix is a boolean
    _write_config_file(tmpdir.strpath, 'autofix: herp')

    with assert_raises_with_msg(
        ConfigValidationError,
        REMatcher(
            r"^.pypi-practices-config.yaml: File does not satisfy schema:\n\n"
            r"'herp' is not of type u?'boolean'\n\n"
            r"Failed validating u?'type' "
            r"in schema\[u?'properties'\]\[u?'autofix'\]:\n"
            r"    {u?'type': u?'boolean'}\n\n"
            r"On instance\[u?'autofix'\]:\n"
            r"    'herp'"
        )
    ):
        load_config(tmpdir.strpath)
