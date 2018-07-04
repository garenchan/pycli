#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re

try:
    # Use setuptools if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Check python version info, we need Function Annotations support.
# https://www.python.org/dev/peps/pep-3107/
if sys.version_info < (3, 0, 0):
    raise Exception("PyCLI only support Python 3.0.0+")


version = re.compile(r'__version__\s*=\s*"(.*?)"')


def get_package_version():
    """return package version without importing it"""
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "pycli", "__init__.py"),
              mode="rt",
              encoding="utf-8") as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return m.groups()[0]


def get_long_description():
    """return package's long description"""
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "README.md"),
              mode="rt",
              encoding="utf-8") as readme:
        return readme.read()


if __name__ == "__main__":
    setup(
        name="py3cli",
        version=get_package_version(),
        packages=["pycli", "pycli.tests"],
        description="A Tiny Python CLI Library Based On argparse",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        author="garenchan",
        author_email="1412950785@qq.com",
        url="https://github.com/garenchan/pycli",
        license="BSD",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Operating System :: OS Independent",
        ],
    )
