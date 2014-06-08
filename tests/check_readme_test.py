from __future__ import unicode_literals

import io
import os.path
import pytest

from pypi_practices.check_readme import check_readme
from pypi_practices.check_readme import fix_readme
from pypi_practices.errors import FileValidationError


def test_readme_does_not_exist(tmpdir):
    # TODO: assert raises exactly
    with pytest.raises(FileValidationError):
        check_readme(tmpdir.strpath)


def test_returns_zero_readme_exists_and_is_correct(tmpdir):
    with io.open(os.path.join(tmpdir.strpath, 'README.md'), 'w') as readme:
        readme.write('my package\n=========\n')

    ret = check_readme(tmpdir.strpath)
    assert ret == 0


def test_fix(tmpdir):
    # TODO: actually assert something
    ret = fix_readme(tmpdir.strpath)
    assert ret == 0
