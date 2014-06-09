from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from pypi_practices import five
from pypi_practices.errors import _format_error_line
from pypi_practices.errors import ConfigValidationError
from pypi_practices.errors import FileValidationError


# pylint:disable=star-args


def test_config_validation_error():
    error = ConfigValidationError('filename', 'message')
    assert five.text(error) == 'filename: message'


@pytest.mark.parametrize(
    ('error', 'expected'),
    (
        (('filename', None, 'message'), 'filename: message'),
        (('filename', 5, 'message'), 'filename:5: message'),
    )
)
def test_format_error_line(error, expected):
    assert _format_error_line(*error) == expected


def test_file_validation_error():
    error = FileValidationError(
        [('filename1', None, 'message1'), ('filename2', 1, 'message2')]
    )
    assert five.text(error) == (
        'filename1: message1\n'
        'filename2:1: message2'
    )
