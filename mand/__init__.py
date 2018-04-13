"""Execute multiple modules in the same interpreter"""
import sys

__version__ = "0.9.4"
if sys.version_info[0] < 3:
    raise Exception("Cannot run on python 2")

from .mand import mand # pylint: disable=wrong-import-position
