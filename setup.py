#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Setup configuration for `mktheapidocs`.

"""
from os import path

import versioneer

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

__status__ = "Development"
__author__ = "Jonathan Gray"
__maintainer__ = "Jonathan Gray"
__email__ = "jonathan.gray@nanosheep.net"
__copyright__ = "Copyright 2020, Jonathan Gray"

setup(
    name="mknotebooks",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points={"mkdocs.plugins": ["mknotebooks = mknotebooks.plugin:Plugin"]},
    description="Plugin for mkdocs to generate markdown documents from jupyter notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url="https://github.com/greenape/mknotebooks",
    license="MIT",
    keywords="mkdocs documentation markdown",
    packages=["mknotebooks"],
    include_package_data=True,
    install_requires=["nbconvert", "mkdocs>=1.1", "jupyter_client"],
    platforms=["MacOS X", "Linux"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
    ],
)
