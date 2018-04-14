"""Tests for mand package"""

import sys
import os

from mand import mand
from mand.util import temp_directory, create_module_file

from .util import stem, module_name_from_path


def test_running_multiple_modules(capsys):
    """Make sure all modules given are executed"""
    module_a = "print('from module a')"
    module_b = "print('from module b')"
    with temp_directory() as directory_path:
        sys.path.append(directory_path)
        module_a_path = create_module_file(module_a,
                                           directory_path)
        module_b_path = create_module_file(module_b,
                                           directory_path)
        modules = [module_name_from_path(path)
                   for path in (module_a_path, module_b_path)]
        mand(modules)
    assert capsys.readouterr().out == "from module a\nfrom module b\n"


def test_multiple_modules_with_arguments(capsys):
    """Make sure system arguments are properly swapped out for each module"""
    a_module = """
import sys
print(sys.argv[1])
"""
    with temp_directory() as directory_path:
        sys.path.append(directory_path)
        module_path = create_module_file(a_module, directory_path)
        module_name = module_name_from_path(module_path)
        args = ["{module} cats".format(module=module_name),
                "{module} dogs".format(module=module_name)]
        mand(args)
    assert capsys.readouterr().out == "cats\ndogs\n"

def test_multiple_modules_with_arguments_tuple(capsys):
    """Test alternative way of specify arguments to mand"""
    a_module = """
import sys
print(sys.argv[1])
"""
    with temp_directory() as directory_path:
        sys.path.append(directory_path)
        module_path = create_module_file(a_module, directory_path)
        module_name = stem(os.path.basename(module_path))
        args = [(module_name, "cats"),
                (module_name, "dogs")]
        mand(args)
    assert capsys.readouterr().out == "cats\ndogs\n"


def test_module_paths(capsys):
    """Make sure module paths are executed"""
    module_a = "print('from module a')"
    module_b = "print('from module b')"
    with temp_directory() as directory_path:
        module_a_path = create_module_file(module_a, directory_path)
        module_b_path = create_module_file(module_b, directory_path)
        mand([module_a_path, module_b_path])
    assert capsys.readouterr().out == "from module a\nfrom module b\n"
