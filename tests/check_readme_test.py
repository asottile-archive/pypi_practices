from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path

from pypi_practices.check_readme import check_readme
from pypi_practices.errors import FileValidationError
from testing.util import assert_raises_with_msg


def test_readme_does_not_exist(tmpdir):
    with assert_raises_with_msg(
        FileValidationError,
        'README.md: File does not exist.\n\n'
        'To attempt automatic fixing, run with --fix.'
    ):
        check_readme(tmpdir.strpath)


def test_returns_zero_readme_exists_and_is_correct(tmpdir):
    with io.open(os.path.join(tmpdir.strpath, 'README.md'), 'w') as readme:
        readme.write('my package\n=========\n')

    ret = check_readme(tmpdir.strpath)
    assert ret == 0
