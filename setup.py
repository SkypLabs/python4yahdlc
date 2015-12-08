from distutils.core import setup, Extension

yahdlc = Extension(
	'yahdlc',
	sources = ['src/python4yahdlc.c', 'lib/fcs16.c', 'lib/yahdlc.c'],
	include_dirs = ['include/'],
)

setup(
	name = 'python4yahdlc',
	version = '0.1.0',
	description = 'Python bindings for the yahdlc library',
	author = 'Paul-Emmanuel Raoul',
	author_email = 'skyper@skyplabs.net',
	url = 'https://github.com/SkypLabs/python4yahdlc',
	ext_modules = [yahdlc],
)
