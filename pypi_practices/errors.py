

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
