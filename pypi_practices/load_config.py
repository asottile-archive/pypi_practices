from __future__ import unicode_literals

import io
import jsonschema
import os.path
import yaml
import yaml.error

from pypi_practices.errors import FileValidationError


CONFIG_SCHEMA = {
    'properties': {
        'autofix': {'type': 'boolean'},
        'github_user': {'type': 'string'},
        'package_name': {'type': 'string'},
    },
}


def load_config(cwd):
    """Loads the pypi_practices config file.  The file is assumed to exist
    at `cwd`/.pypi-practices-config.yaml

    If the file does not exist, an empty config is returned.

    :param text cwd: Current working directory.
    """
    config_filename = os.path.join(cwd, '.pypi-practices-config.yaml')
    if not os.path.exists(config_filename):
        return {}

    with io.open(config_filename) as config_file:
        try:
            config_contents = yaml.load(config_file)
        except yaml.error.YAMLError as e:
            raise FileValidationError(
                '.pypi-practices-config.yaml',
                'Invalid Yaml:\n\n{0}'.format(e)
            )

    try:
        jsonschema.validate(config_contents, CONFIG_SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        raise FileValidationError(
            '.pypi-practices-config.yaml',
            'File does not satisfy schema:\n\n{0}'.format(e)
        )

    return config_contents
