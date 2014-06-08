from __future__ import unicode_literals


class FileValidationError(ValueError):
    """Represents an error in validating."""
    def __init__(
            self,
            filename,
            validation_message,
            line=None,
            is_auto_fixable=False,
    ):
        super(FileValidationError, self).__init__({
            'filename': filename,
            'validation_message': validation_message,
            'line': line,
            'is_auto_fixable': is_auto_fixable,
        })
        self.filename = filename
        self.validation_message = validation_message
        self.line = line
        self.is_auto_fixable = is_auto_fixable

    def __str__(self):
        if self.line is not None:
            line_str = ':{0}'.format(self.line)
        else:
            line_str = ''

        if self.is_auto_fixable:
            autofix_str = 'To attempt automatic fixing, run with --fix.'
        else:
            autofix_str = 'Manually edit the file above to fix.'

        return '{0}{1}: {2}\n\n{3}'.format(
            self.filename, line_str, self.validation_message, autofix_str,
        )
