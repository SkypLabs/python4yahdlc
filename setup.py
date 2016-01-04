#!/usr/bin/env python3

from setuptools import setup, Extension
from os.path import dirname, abspath

DIR = dirname(abspath(__file__))
VERSION = '1.0.3'

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

setup(
	name = 'python4yahdlc',
	version = VERSION,
	description = 'Python bindings for the yahdlc library',
	license = 'GPLv3',
	keywords = 'hdlc yahdlc bindings',
	author = 'Paul-Emmanuel Raoul',
	author_email = 'skyper@skyplabs.net',
	url = 'https://github.com/SkypLabs/python4yahdlc',
	download_url = 'https://github.com/SkypLabs/python4yahdlc/archive/v{0}.zip'.format(VERSION),
	setup_requires = ['setuptools-markdown'],
	long_description_markdown_filename = 'README.md',
	ext_modules = [yahdlc],
	test_suite = 'test',
)
