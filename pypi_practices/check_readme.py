from __future__ import print_function

import os.path

from pypi_practices.errors import FileValidationError
from pypi_practices.make_entry import make_entry


def check_readme(cwd):
    readme_path = os.path.join(cwd, 'README.md')

    if not os.path.exists(readme_path):
        raise FileValidationError(
            'README.md',
            'File does not exist.',
            is_auto_fixable=True,
        )

    # TODO: attempt to get project name from config
    # TODO: attempt to get project name from tox.ini
    # TODO: attempt to get project name from setup.py
    return 0


def fix_readme(_):
    return 0


entry = make_entry(check_readme, fix_readme)


if __name__ == '__main__':
    exit(entry())
