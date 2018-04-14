"""Main file of this package"""
import argparse
import sys
import shlex
import runpy
import re
from contextlib import contextmanager

from .util import VALID_PACKAGE_RE


def main(argv=None):
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
    mand(args.module_seq)


def mand(module_seq):
    """Execute each module in `module_seq`

    module_seq can be a sequence of strings: each module and its optional arguments
    module_seq can be a sequence of sequence of strings: a sequence for each module
    """
    module_gen = _normalize_module_sequence(module_seq)
    call_multiple_modules(module_gen)


def _normalize_module_sequence(module_sequence):
    for module_item in module_sequence:
        if isinstance(module_item, str):
            args_seq = shlex.split(module_item)
        else:
            args_seq = module_item
        yield args_seq


def call_multiple_modules(module_gen):
    """Call each module

    module_gen should be a iterator
    """
    for args_seq in module_gen:
        module_name_or_path = args_seq[0]
        with replace_sys_args(args_seq):
            if re.match(VALID_PACKAGE_RE, module_name_or_path):
                runpy.run_module(module_name_or_path,
                                 run_name='__main__')
            else:
                runpy.run_path(module_name_or_path,
                               run_name='__main__')

@contextmanager
def replace_sys_args(new_args):
    """Temporarily replace sys.argv with current arguments

    Restores sys.argv upon exit of the context manager.
    """
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


def _escape_spaces(iterator):
    if isinstance(iterator, str):
        iterator = [iterator]
    for item in iterator:
        yield item.replace(" ", r"\ ")
