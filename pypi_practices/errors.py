from __future__ import unicode_literals


# pylint:disable=star-args


class ValidationError(ValueError):
    pass


class ConfigValidationError(ValidationError):
    def __init__(self, filename, validation_message):
        super(ConfigValidationError, self).__init__({
            'filename': filename,
            'validation_message': validation_message,
        })
        self.filename = filename
        self.validation_message = validation_message

    def __str__(self):
        return '{0}: {1}'.format(self.filename, self.validation_message)


def _format_error_line(filename, line, msg):
    return '{0}{1}: {2}'.format(
        filename,
        ':{0}'.format(line) if line is not None else '',
        msg,
    )


class FileValidationError(ValidationError):
    """Represents an error in validating."""

    def __init__(self, errors):
        super(FileValidationError, self).__init__(errors)
        self.errors = errors

    def __str__(self):
        return '\n'.join([_format_error_line(*error) for error in self.errors])
