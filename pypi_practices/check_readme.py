from __future__ import print_function

import io
import os.path
import pkg_resources

from pypi_practices.errors import FileValidationError
from pypi_practices.make_entry import make_entry


# pylint:disable=star-args


TRAVIS_BLING = (
    '[![Build Status](https://travis-ci.org/{0}/{1}.svg?branch=master)]'
    '(https://travis-ci.org/{0}/{1})'
)


COVERALLS_BLING = (
    '[![Coverage Status]'
    '(https://img.shields.io/coveralls/{0}/{1}.svg?branch=master)]'
    '(https://coveralls.io/r/{0}/{1})'
)


def _check_file_exists(errors, cwd, fix, config):
    """Check that the readme exists."""
    readme_path = os.path.join(cwd, 'README.md')
    if os.path.exists(readme_path):
        return

    errors.append(('README.md', None, 'File does not exist.'))

    if fix:
        errors.append(('README.md', None, 'Fixed!'))
        readme_template_filename = pkg_resources.resource_filename(
            'pypi_practices', 'resources/README.md.template',
        )
        template_contents = io.open(readme_template_filename).read()

        with io.open(readme_path, 'w') as readme_file:
            readme_file.write(template_contents.format(**config))

    raise FileValidationError(errors)


def _check_has_installation(errors, original_contents, fix, config):
    """Check that the readme has an Installation section."""
    if '### Installation\n' in original_contents:
        return original_contents

    errors.append((
        'README.md', None, 'Expected an ### Installation section.',
    ))

    if fix:
        errors.append(('README.md', None, 'Fixed!'))
        return original_contents + (
            '\n'
            '### Installation\n'
            '\n'
            '`$ pip install {0}`\n'
            '\n\n'.format(config['package_name'])
        )
    else:
        return original_contents


# Each step takes the following arguments:
#    errors - mutable list to append errors to
#    original_contents - text contents when the step was called
#    fix - boolean whether the step should fix things
#    config - pypi_practices config
# If a step finds a problem it should:
#    - append to errors
#    - If `fix` and it is possible: return new updated contents with the fix
# Otherwise:
#    - return the original contents and do nothing
STEPS = [
    _check_has_installation,
]


def check_readme(cwd, fix, config):
    errors = []

    # First check that our file exists
    _check_file_exists(errors, cwd, fix, config)

    readme_path = os.path.join(cwd, 'README.md')
    original_contents = io.open(readme_path).read()
    contents = original_contents

    # Each step may change the contents / append to errors
    for step in STEPS:
        contents = step(errors, contents, fix, config)

    # If a fix modified the contents, write them out
    if fix and contents != original_contents:
        with io.open(readme_path, 'w') as readme_file:
            readme_file.write(contents)

    # If we had errors, raise
    if errors:
        raise FileValidationError(errors)

    # Otherwise all is good :)
    return 0


entry = make_entry(check_readme)


if __name__ == '__main__':
    exit(entry())
