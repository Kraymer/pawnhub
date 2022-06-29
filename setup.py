#!/usr/bin/env python3

# Copyright (c) 2022 Fabrice Laporte - kray.me
# The MIT License http://www.opensource.org/licenses/mit-license.php

import codecs
import os
import re
from setuptools import setup


PKG_NAME = "pawnhub"

# Extract module docstring and version from package root __init__.py
with codecs.open("{}/__init__.py".format(PKG_NAME), encoding="utf-8") as fd:
    metadata = fd.read()
    VERSION = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', metadata, re.MULTILINE
    ).group(1)
    DESCRIPTION = metadata.split('"""')[1].strip()


def read_rsrc(filename, pypi_compat=False):
    """Return content of given text file.
    If pypi_compat is True then remove lines that contain the string "nopypi"
    """
    with codecs.open(filename, encoding="utf-8") as _file:
        lines = _file.readlines()
        if pypi_compat:
            lines = [x for x in lines if "[nopypi]" not in x]
        return "".join(lines).strip()


setup(
    name=PKG_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read_rsrc("README.md", True),
    long_description_content_type="text/markdown",
    author="Fabrice Laporte",
    author_email="kraymer@gmail.com",
    url=f"https://github.com/KraYmer/{PKG_NAME}",
    license="MIT",
    platforms="ALL",
    packages=[PKG_NAME],
    install_requires=read_rsrc("requirements.txt").split("\n"),
    python_requires=">=3.6",
    extras_require={
        "test": [
            "coverage>5",
            "pytest>=6",
            "tox>=3",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Environment :: Console",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    keywords="chess",
)
