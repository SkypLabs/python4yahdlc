#!/usr/bin/env python3

from setuptools import setup, Extension
from os.path import dirname, abspath, join
from codecs import open as fopen

DIR = dirname(abspath(__file__))
VERSION = '1.2.0'

yahdlc = Extension(
    'yahdlc',
    sources = [
        DIR + '/src/python4yahdlc.c',
        DIR + '/yahdlc/C/fcs16.c',
        DIR + '/yahdlc/C/yahdlc.c'
    ],
    include_dirs = [
        DIR + '/yahdlc/C/'
    ],
)

with fopen(join(DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'python4yahdlc',
    version = VERSION,
    description = 'Python binding of the yahdlc library allowing to encode and decode HDLC frames',
    long_description = long_description,
    license = 'GPLv3',
    keywords = 'hdlc yahdlc binding network',
    author = 'Paul-Emmanuel Raoul',
    author_email = 'skyper@skyplabs.net',
    url = 'https://github.com/SkypLabs/python4yahdlc',
    download_url = 'https://github.com/SkypLabs/python4yahdlc/archive/v{0}.zip'.format(VERSION),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: C',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    ext_modules = [yahdlc],
    test_suite = 'test',
    python_requires='>=3',
)
