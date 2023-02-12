"""
Setuptools configuration for building yahdlc as a C extension module.

See https://setuptools.pypa.io/en/latest/userguide/ext_modules.html for further
information on this topic.
"""

from setuptools import Extension, setup

setup(
  ext_modules=[
    Extension(
      name="yahdlc",
      sources=[
        "src/python4yahdlc.c",
        "yahdlc/C/fcs.c",
        "yahdlc/C/yahdlc.c",
      ],
      include_dirs=[
        "yahdlc/C/",
      ]
    )
  ]
)
