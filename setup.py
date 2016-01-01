from setuptools import setup, Extension

yahdlc = Extension(
	'yahdlc',
	sources = ['src/python4yahdlc.c', 'lib/fcs16.c', 'lib/yahdlc.c'],
	include_dirs = ['include/'],
)

setup(
	name = 'python4yahdlc',
	version = '1.0.0',
	description = 'Python bindings for the yahdlc library',
	license = 'GPLv3',
	keywords = 'hdlc yahdlc bindings',
	author = 'Paul-Emmanuel Raoul',
	author_email = 'skyper@skyplabs.net',
	url = 'https://github.com/SkypLabs/python4yahdlc',
	download_url = 'https://github.com/SkypLabs/python4yahdlc/archive/v1.0.0.zip',
	ext_modules = [yahdlc],
	test_suite = 'test',
)
