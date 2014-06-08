from __future__ import unicode_literals

import io
import os.path
import pytest

from pypi_practices.errors import FileValidationError
from pypi_practices.load_config import load_config


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

    # TODO: assert exception message
    with pytest.raises(FileValidationError):
        load_config(tmpdir.strpath)


def test_valid_yaml_invalid_config(tmpdir):
    # autofix is a boolean
    _write_config_file(tmpdir.strpath, 'autofix: herp')

    # TODO: assert exception message
    with pytest.raises(FileValidationError):
        load_config(tmpdir.strpath)
