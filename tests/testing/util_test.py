from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from testing.util import assert_raises_with_msg
from testing.util import REMatcher


def test_assert_raise_exactly_passing():
    with assert_raises_with_msg(ValueError, 'herpderp'):
        raise ValueError('herpderp')


def test_assert_raises_with_msg_mismatched_type():
    with pytest.raises(AssertionError):
        with assert_raises_with_msg(ValueError, 'herpderp'):
            raise TypeError('herpderp')


def test_assert_raises_mismatched_message():
    with pytest.raises(AssertionError):
        with assert_raises_with_msg(ValueError, 'herpderp'):
            raise ValueError('harpdarp')


def test_assert_raises_does_not_raise():
    with pytest.raises(AssertionError):
        with assert_raises_with_msg(ValueError, 'herpderp'):
            pass


def test_assert_raises_subclass():
    class MyClass(ValueError):
        pass

    with pytest.raises(AssertionError):
        with assert_raises_with_msg(ValueError, 'herpderp'):
            raise MyClass('herpderp')


@pytest.mark.parametrize(
    ('regex', 'input_str', 'expected'),
    (
        ('^foo$', 'foo', True),
        ('^foo', 'food', True),
        ('^foo$', 'bar', False),
        ('foo', 'afoo', False),
    )
)
def test_re_matcher(regex, input_str, expected):
    ret = REMatcher(regex) == input_str
    assert ret is expected


def test_re_matcher_repr():
    matcher = REMatcher(str('foo'))
    assert repr(matcher) == "testing.util.REMatcher('foo')"
