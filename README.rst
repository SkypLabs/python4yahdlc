=============
python4yahdlc
=============

|PyPI Package| |PyPI Downloads| |PyPI Python Versions| |Build Status| |LGTM Grade| |LGTM Alerts|

python4yahdlc is a Python binding of the
`yahdlc <https://github.com/bang-olufsen/yahdlc>`__ library, allowing to encode and decode `HDLC <https://en.wikipedia.org/wiki/High-Level_Data_Link_Control>`__ frames.

Dependencies
============

This software requires Python 3.

Installation
============

With pip (recommanded)
----------------------

::

    pip3 install --upgrade python4yahdlc

From sources
------------

::

    git clone https://github.com/SkypLabs/python4yahdlc.git
    cd python4yahdlc
    git submodule update --init --recursive
    python3 setup.py install

You need the `setuptools <https://pypi.python.org/pypi/setuptools>`_ package to execute ``setup.py``.

Usage
=====

To generate a new HDLC data frame:

::

    from yahdlc import *

    frame = frame_data('hello world!')

To generate a new HDLC ``ACK`` frame with a specific sequence number:

::

    frame = frame_data('', FRAME_ACK, 3)

The highest sequence number is 7 and the following frame types are
available:

- ``FRAME_DATA``
- ``FRAME_ACK``
- ``FRAME_NACK``

Note that when you generate an ``ACK`` or ``NACK`` frame, the payload is
useless.

To decode a received HDLC frame:

::

    data, ftype, seq_no = get_data(frame)

For a more advanced use, take a look at the examples available in the
`examples <https://github.com/SkypLabs/python4yahdlc/tree/master/examples>`__
folder.

Development
===========

Releasing a new version
-----------------------

Before publishing the new release:

* Run all tests and be sure they all pass
* Update the ``VERSION`` variable in ``setup.py``
* Update ``MANIFEST.in`` if needed
* Update the package's metadata (description, classifiers, etc) in ``setup.py`` if needed
* Update ``README.rst`` and ``examples/README.rst`` if needed

After having pushed the changes:

* Edit the release note on GitHub

License
=======

This project is released under the `GPL version
3 <https://www.gnu.org/licenses/gpl.txt>`__ license. The
`yahdlc <https://github.com/bang-olufsen/yahdlc>`__ library is released
under the
`MIT <https://github.com/bang-olufsen/yahdlc/blob/master/LICENSE>`__
license.

.. |Build Status| image:: https://github.com/SkypLabs/python4yahdlc/actions/workflows/test_and_publish.yml/badge.svg?branch=develop
   :target: https://github.com/SkypLabs/python4yahdlc/actions/workflows/test_and_publish.yml?query=branch%3Adevelop
   :alt: Build Status

.. |LGTM Alerts| image:: https://img.shields.io/lgtm/alerts/g/SkypLabs/python4yahdlc.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/SkypLabs/python4yahdlc/alerts/
   :alt: LGTM Alerts

.. |LGTM Grade| image:: https://img.shields.io/lgtm/grade/python/g/SkypLabs/python4yahdlc.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/SkypLabs/python4yahdlc/context:python
   :alt: LGTM Grade

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/python4yahdlc.svg?style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Downloads Per Month

.. |PyPI Package| image:: https://img.shields.io/pypi/v/python4yahdlc.svg?style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Latest Release

.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/python4yahdlc.svg?logo=python&style=flat
   :target: https://pypi.org/project/python4yahdlc/
   :alt: PyPI Package Python Versions
