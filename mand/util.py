"""utility functions for mand package"""
import os
from contextlib import contextmanager
import tempfile
import shutil
import importlib
import pkgutil
import random
import re

VALID_PACKAGE_RE = r'^[A-za-z_]+$'


def create_module_file(txt, directory):
    """Create a file in the given directory with
    a valid module name populated with the given txt.

    Returns:
        A path to the file"""
    name = nonpresent_module_filename()
    path = os.path.join(directory, name)
    with open(path, 'w') as fh:
        fh.write(txt)
    return path


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
