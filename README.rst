=============
python4yahdlc
=============

|PyPI Package| |PyPI Downloads| |PyPI Python Versions| |Build Status|

python4yahdlc is a Python binding of the `yahdlc
<https://github.com/bang-olufsen/yahdlc>`__ library, allowing to encode and
decode `HDLC <https://en.wikipedia.org/wiki/High-Level_Data_Link_Control>`__
frames.

Dependencies
============

This software requires Python 3.

Installation
============

From PyPI (recommended)
----------------------

.. code:: sh

    pip install --upgrade python4yahdlc

From sources
------------

.. code:: sh

    git clone https://github.com/SkypLabs/python4yahdlc.git
    cd python4yahdlc
    git submodule update --init --recursive
    pip install --upgrade .

Usage
=====

To generate a new HDLC data frame:

.. code:: python

    from yahdlc import *

    frame = frame_data('hello world!')

To generate a new HDLC ``ACK`` frame with a specific sequence number:

.. code:: python

    frame = frame_data('', FRAME_ACK, 3)

The highest sequence number is 7 and the following frame types are available:

- ``FRAME_DATA``
- ``FRAME_ACK``
- ``FRAME_NACK``

Note that when you generate an ``ACK`` or ``NACK`` frame, the payload is
useless.

To decode a received HDLC frame:

.. code:: python

    data, ftype, seq_no = get_data(frame)

For a more advanced use, take a look at the examples available in the `examples
<https://github.com/SkypLabs/python4yahdlc/tree/main/examples>`__ folder.

Development
===========

To set up a development environment on your local machine:

.. code:: sh

    # Clone the Git repository and initialise its sub-modules.
    git clone https://github.com/SkypLabs/python4yahdlc.git
    cd python4yahdlc
    git submodule update --init --recursive

    # Create a virtual environment and activate it.
    python -m venv .venv
    source .venv/bin/activate

    # Make sure to have the latest versions of pip and setuptools.
    pip install --upgrade pip setuptools

    # Install python4yahdlc in editable mode with all its optional
    # dependencies.
    pip install -e .[examples,tests]

License
=======

This project is released under the `GPL version 3
<https://www.gnu.org/licenses/gpl.txt>`__ license. The `yahdlc
<https://github.com/bang-olufsen/yahdlc>`__ library is released under the `MIT
<https://github.com/bang-olufsen/yahdlc/blob/master/LICENSE>`__ license.

.. |Build Status| image:: https://github.com/SkypLabs/python4yahdlc/actions/workflows/test_and_publish.yml/badge.svg?branch=develop
   :target: https://github.com/SkypLabs/python4yahdlc/actions/workflows/test_and_publish.yml?query=branch%3Adevelop
   :alt: Build Status

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/python4yahdlc.svg?style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Downloads Per Month

.. |PyPI Package| image:: https://img.shields.io/pypi/v/python4yahdlc.svg?style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Latest Release

.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/python4yahdlc.svg?logo=python&style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Python Versions
