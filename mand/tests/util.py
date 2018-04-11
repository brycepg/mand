"""Utilities for multirunpy tests"""

import re
import random
from contextlib import contextmanager
import tempfile
import shutil
import pkgutil
import importlib
import os


VALID_PACKAGE_RE = r'^[a-z_]+$'


@contextmanager
def temp_directory():
    """Temporarily create directory

    Returns: Directory path

    The directory will be removed upon exit of context manager.
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


def stem(filename):
    """Get the stem of a filename"""
    if '.' in filename:
        return ''.join(filename.split(".")[:-1])
    return filename


def module_name_from_path(path):
    """Return module name from path"""
    return stem(os.path.basename(path))


def nonpresent_module_filename():
    """Return module name that doesn't already exist"""
    while True:
        module_name = get_random_name()
        loader = pkgutil.find_loader(module_name)
        if loader is not None:
            continue
        importlib.invalidate_caches()
        return "{}.py".format(module_name)


def get_random_name():
    """Return random lowercase name"""
    char_seq = []
    name_source = random.randint(1, 2**8-1)
    current_value = name_source
    while current_value > 0:
        char_offset = current_value % 26
        current_value = current_value - random.randint(1, 26)
        char_seq.append(chr(char_offset + ord('a')))
    name = ''.join(char_seq)
    assert re.match(VALID_PACKAGE_RE, name)
    return name
