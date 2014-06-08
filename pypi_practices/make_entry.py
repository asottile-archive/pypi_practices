from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from pypi_practices import five
from pypi_practices.errors import ValidationError
from pypi_practices.load_config import load_config


def make_entry(check_fn, fix_fn):
    """Make a cmdline entry.

    The cmdline entry will have the following options:

    --cwd - Current working directory to find files at.
    --fix - Attempt auto-fixing of rule.
    filenames - (Ignored) for compatibility with pre-commit.

    The check and fix functions take the following arguments:
        cwd - Current working directory to find files at.
        config - Configuration in .pypi-practices-config.yaml

    :param function check_fn: Function to check the rule.
    :param function fix_fn: Function which attempts to fix the rule.
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

        try:
            config = load_config(cwd)
        except ValidationError as e:
            print(five.text(e))
            return 1

        if args.fix:
            return fix_fn(cwd, config)

        try:
            return check_fn(cwd, config)
        except ValidationError as e:
            print(five.text(e))
            return 1

    return entry
