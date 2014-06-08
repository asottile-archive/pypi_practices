from __future__ import unicode_literals

import contextlib
import re

from pypi_practices import five


@contextlib.contextmanager
def assert_raises_with_msg(cls, text):
    try:
        yield
    except Exception as e:
        assert type(e) is cls
        assert five.text(e) == text
    else:
        raise AssertionError('expected to raise')


class REMatcher(object):
    """This object allows you to pass a regex as something to check for
    equality.
    """
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return '{0}.{1}({2!r})'.format(
            type(self).__module__,
            type(self).__name__,
            self.expr,
        )

    def __eq__(self, other):
        return bool(re.compile(self.expr).match(other))
