import sys

if sys.version_info < (3,4):
    raise Exception("Requires Python3.4+")

from setuptools import setup, find_packages

import mand

with open('README.md') as fh:
    long_description = fh.read()

setup(name=mand.__name__,
      version=mand.__version__,
      description='Run multiple modules with the same interpreter',
      author='Bryce Guinta',
      author_email='contact@bryceguinta.me',
      long_description=long_description,
      packages=[mand.__name__],
      license='MIT',
      entry_points={'console_scripts': ['mand = mand:mand']},
      zip_safe=True,
      classifiers=[
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development :: Libraries'
      ],
     )
