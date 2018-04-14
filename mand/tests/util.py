"""Utilities for multirunpy tests"""
import os


def stem(filename):
    """Get the stem of a filename"""
    if '.' in filename:
        return ''.join(filename.split(".")[:-1])
    return filename


def module_name_from_path(path):
    """Return module name from path"""
    return stem(os.path.basename(path))
