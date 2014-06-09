from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path

from pypi_practices.check_readme import check_readme
from pypi_practices.errors import FileValidationError
from testing.util import assert_raises_with_msg


def test_readme_does_not_exist(tmpdir):
    with assert_raises_with_msg(
        FileValidationError, 'README.md: File does not exist.'
    ):
        check_readme(tmpdir.strpath, False, {})


def test_returns_zero_readme_exists_and_is_correct(tmpdir):
    with io.open(os.path.join(tmpdir.strpath, 'README.md'), 'w') as readme:
        readme.write('my package\n=========\n')

    ret = check_readme(tmpdir.strpath, False, {})
    assert ret == 0


def test_cannot_fix_due_to_no_config(tmpdir):
    with assert_raises_with_msg(
        FileValidationError,
        'README.md: File does not exist.\n'
        'README.md: Could not fix: set `github_user` in '
        '.pypi-practices-config.yaml.\n'
        'README.md: Could not fix: set `package_name` in '
        '.pypi-practices-config.yaml.\n'
        'README.md: Could not fix: set `repo_description` in '
        '.pypi-practices-config.yaml.'
    ):
        check_readme(tmpdir.strpath, True, {})


def test_fixes(tmpdir):
    with assert_raises_with_msg(
        FileValidationError,
        'README.md: File does not exist.\n'
        'README.md: Fixed!'
    ):
        check_readme(
            tmpdir.strpath,
            True,
            {
                'github_user': 'asottile',
                'package_name': 'pypi_practices',
                'repo_description': (
                    'Scripts enforcing best practices for python packaging'
                )
            },
        )
    readme_path = os.path.join(tmpdir.strpath, 'README.md')
    assert os.path.exists(readme_path)
    readme_contents = io.open(readme_path).read()
    assert 'asottile/pypi_practices' in readme_contents
    assert (
        'Scripts enforcing best practices for python packaging' in
        readme_contents
    )
