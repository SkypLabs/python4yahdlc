#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setuptools build system configuration file
for python4yahdlc.

See https://setuptools.readthedocs.io.
"""

try:
    from setuptools import setup, Extension
except Exception as setuptools_not_present:
    raise ImportError(
        "Setuptools is required to install python4yahdlc!"
    ) from setuptools_not_present

from codecs import open as fopen
from os.path import dirname, abspath, join

DIR = dirname(abspath(__file__))

VERSION = "1.2.0"

URL = "https://github.com/SkypLabs/python4yahdlc"
DL_URL = URL + "/archive/v{0}.zip"

yahdlc = Extension(
    "yahdlc",
    sources=[
        DIR + "/src/python4yahdlc.c",
        DIR + "/lib/fcs16.c",
        DIR + "/lib/yahdlc.c",
    ],
    include_dirs=[
        DIR + "/include/",
    ],
)

with fopen(join(DIR, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="python4yahdlc",
    version=VERSION,
    description="""Python binding of the yahdlc library allowing to encode and
    decode HDLC frames""",
    long_description=LONG_DESCRIPTION,
    license="GPLv3",
    keywords="hdlc yahdlc binding network",
    author="Paul-Emmanuel Raoul",
    author_email="skyper@skyplabs.net",
    url=URL,
    download_url=DL_URL.format(VERSION),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: C",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    ext_modules=[yahdlc],
    python_requires=">=3.6, <4",
    extras_require={
        "examples": [
            "fysom",
            "pyserial",
        ],
        "tests": [
            "flake8",
            "pylint",
            "tox",
        ],
    },
)
