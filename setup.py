#!/usr/bin/env python3

from setuptools import setup, Extension
from os.path import dirname, abspath, join
from codecs import open

DIR = dirname(abspath(__file__))
VERSION = '1.0.4'

yahdlc = Extension(
    'yahdlc',
    sources = [
        DIR + '/src/python4yahdlc.c',
        DIR + '/lib/fcs16.c',
        DIR + '/lib/yahdlc.c'
    ],
    include_dirs = [
        DIR + '/include/'
    ],
)

with open(join(DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'python4yahdlc',
    version = VERSION,
    description = 'Python bindings for the yahdlc library',
    long_description = long_description,
    license = 'GPLv3',
    keywords = 'hdlc yahdlc bindings',
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    ext_modules = [yahdlc],
    test_suite = 'test',
)
