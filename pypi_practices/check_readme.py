from __future__ import print_function

import io
import os.path
import pkg_resources

from pypi_practices.errors import FileValidationError
from pypi_practices.make_entry import make_entry


def _check_file_exists(errors, cwd, fix, config):
    readme_path = os.path.join(cwd, 'README.md')
    if os.path.exists(readme_path):
        return

    errors.append(('README.md', None, 'File does not exist.'))

    github_user = config.get('github_user', None)
    package_name = config.get('package_name', None)
    repo_description = config.get('repo_description', None)

    if fix and not github_user:
        errors.append((
            'README.md',
            None,
            'Could not fix: set `github_user` in .pypi-practices-config.yaml.'
        ))

    if fix and not package_name:
        errors.append((
            'README.md',
            None,
            'Could not fix: set `package_name` in .pypi-practices-config.yaml.'
        ))

    if fix and not repo_description:
        errors.append((
            'README.md',
            None,
            'Could not fix: set `repo_description` in '
            '.pypi-practices-config.yaml.'
        ))

    if fix and github_user and package_name and repo_description:
        errors.append(('README.md', None, 'Fixed!'))
        readme_template_filename = pkg_resources.resource_filename(
            'pypi_practices', 'resources/README.md.template',
        )
        template_contents = io.open(readme_template_filename).read()

        with io.open(readme_path, 'w') as readme_file:
            readme_file.write(
                template_contents.format(
                    github_user=github_user,
                    package_name=package_name,
                    repo_description=repo_description,
                )
            )

    raise FileValidationError(errors)


def check_readme(cwd, fix, config):
    errors = []

    _check_file_exists(errors, cwd, fix, config)

    # TODO: attempt to get project name from config
    # TODO: attempt to get project name from tox.ini
    # TODO: attempt to get project name from setup.py
    return 0


entry = make_entry(check_readme)


if __name__ == '__main__':
    exit(entry())
