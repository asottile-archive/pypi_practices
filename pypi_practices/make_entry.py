from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from pypi_practices.errors import FileValidationError


def make_entry(check_fn, fix_fn):
    """Make a cmdline entry.

    The cmdline entry will have the following options:

    --cwd - Current working directory to find files at.
    --fix - Attempt auto-fixing of rule.
    filenames - (Ignored) for compatibility with pre-commit.

    :param function check_fn: Function to check the rule.  The check_fn takes
        a single argument: the cwd.
    :param function fix_fn: Function which attempts to fix the rule.
        The fix_fn takes a single argument: the cwd.
    """
    def entry(argv=None):
        if argv is None:
            argv = sys.argv[1:]

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--cwd',
            default='.',
            help='Current working directory to find files at.',
        )
        parser.add_argument(
            '--fix',
            default=False,
            action='store_true',
            help='Attempt auto-fixing of rule.',
        )
        parser.add_argument(
            'filenames',
            nargs='*',
            help='(Ignored) for compatibility with pre-commit.',
        )
        args = parser.parse_args(argv)

        cwd = args.cwd
        if type(cwd) is bytes:  # pragma: no cover (PY2 only)
            cwd = cwd.decode('utf-8')

        # TODO: load .practices-config.yaml

        if args.fix:
            return fix_fn(cwd)

        try:
            return check_fn(cwd)
        except FileValidationError as e:
            print(
                '{0}{1}: {2}'.format(
                    e.filename,
                    ':{0}'.format(e.line) if e.line is not None else '',
                    e.validation_message,
                )
            )
            print()

            if e.is_auto_fixable:
                print(
                    'To attempt automatic fixing of this run:\n'
                    '    {0} --fix'.format(sys.argv[0])
                )
            else:
                print('Manually edit the files above to fix.')

            return 1

    return entry
