"""Execute multiple modules in the same interpreter"""
import sys

__version__ = "0.9.8"
if sys.version_info[0] < 3:
    raise Exception("Cannot run on python 2")

# pylint: disable=wrong-import-position
from .mand import mand, main
from . import util
