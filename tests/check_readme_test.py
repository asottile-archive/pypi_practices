from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os.path
import pkg_resources

from pypi_practices.check_readme import _check_has_installation
from pypi_practices.check_readme import check_readme
from pypi_practices.errors import FileValidationError
from testing.util import assert_raises_with_msg


def test_readme_does_not_exist(tmpdir):
    with assert_raises_with_msg(
        FileValidationError, 'README.md: File does not exist.'
    ):
        check_readme(tmpdir.strpath, False, {})


def test_returns_zero_readme_exists_and_is_correct(tmpdir):
    """Tests both that when everything is happy we get zero and that our
    template README file passes all of the checks.
    """
    readme_template_file = pkg_resources.resource_filename(
        'pypi_practices', 'resources/README.md.template',
    )
    template_contents = io.open(readme_template_file).read()
    with io.open(os.path.join(tmpdir.strpath, 'README.md'), 'w') as readme:
        readme.write(template_contents.format(
            github_user='asottile',
            package_name='pypi_practices',
            repo_description=(
                'Scripts enforcing best practices for python packaging'
            ),
        ))

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


def test_fixes_readme_dne(tmpdir):
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


def test_fixes(tmpdir):
    readme_path = os.path.join(tmpdir.strpath, 'README.md')
    with io.open(readme_path, 'w') as readme_file:
        readme_file.write('before\n')

    with assert_raises_with_msg(
        FileValidationError,
        'README.md: Expected an ### Installation section.\n'
        'README.md: Fixed!'
    ):
        check_readme(
            tmpdir.strpath,
            True,
            {'package_name': 'package_name'},
        )

    new_readme_contents = io.open(readme_path).read()
    assert new_readme_contents == (
        'before\n'
        '\n'
        '### Installation\n'
        '\n'
        '`$ pip install package_name`\n'
        '\n\n'
    )


def test_installation_has_installation_has_it():
    contents = '### Installation\n'
    errors = []
    ret = _check_has_installation(errors, contents, True, {})
    assert ret == contents
    assert errors == []


def test_installation_missing_installation_no_fix():
    contents = 'before\n'
    errors = []
    ret = _check_has_installation(errors, contents, False, {})
    assert ret == contents
    assert errors == [
        ('README.md', None, 'Expected an ### Installation section.'),
    ]


def test_installation_fix_no_package_name():
    contents = 'before\n'
    errors = []
    ret = _check_has_installation(errors, contents, True, {})
    assert ret == contents
    assert errors == [
        ('README.md', None, 'Expected an ### Installation section.'),
        (
            'README.md',
            None,
            'Could not fix: set `package_name` in '
            '.pypi-practices-config.yaml.'
        ),
    ]


def test_installation_fixes():
    contents = 'before\n'
    errors = []
    ret = _check_has_installation(
        errors, contents, True, {'package_name': 'package_name'}
    )
    assert ret == (
        'before\n'
        '\n'
        '### Installation\n'
        '\n'
        '`$ pip install package_name`\n'
        '\n\n'
    )
    assert errors == [
        ('README.md', None, 'Expected an ### Installation section.'),
        ('README.md', None, 'Fixed!'),
    ]
