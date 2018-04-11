"""Main file of this package"""
import argparse
import sys
import shlex
import runpy
import re
from contextlib import contextmanager

VALID_PACKAGE_RE = r'^[a-z_]+$'

def mand(argv=None):
    """Execute each module in the same interpreter.

    Args:
        argv: Each item of argv will be treated as a separate
            module with potential arguments
            each item may be a string or a sequence of strings.
            If a given argument is a string, then treat string as
            shell arguments and split accordingly.
            If the given argument is a tuple or list, then assume
            that the given arguments are already parsed.
            The first item of each argument should be a module or module path
            """
    if argv is None:
        argv = sys.argv[1:]
    args = _get_parser().parse_args(argv)
    for module_item in args.module_seq:
        if isinstance(module_item, str):
            args_seq = shlex.split(module_item)
        elif isinstance(module_item, (list, tuple)):
            args_seq = module_item
        module_name_or_path = args_seq[0]
        with _replace_sys_args(args_seq):
            if re.match(VALID_PACKAGE_RE, module_name_or_path):
                runpy.run_module(module_name_or_path, run_name='__main__')
            else:
                runpy.run_path(module_name_or_path, run_name='__main__')


@contextmanager
def _replace_sys_args(new_args):
    # Replace sys.argv arguments
    # for module import
    old_args = sys.argv
    sys.argv = new_args
    try:
        yield
    finally:
        sys.argv = old_args


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        metavar="MODULE", nargs='+', dest="module_seq",
        help="Module modules and their (optional) arguments")
    return parser
