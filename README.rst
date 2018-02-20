=============
python4yahdlc
=============

|PyPI Package| |Build Status| |Code Coverage|

python4yahdlc is a Python bindings for the
`yahdlc <https://github.com/bang-olufsen/yahdlc>`__ library, allowing to encore and decode `HDLC <https://en.wikipedia.org/wiki/High-Level_Data_Link_Control>`__ frames using Python.

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
* Update ``README.rst`` if needed

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

.. |Build Status| image:: https://travis-ci.org/SkypLabs/python4yahdlc.svg
   :target: https://travis-ci.org/SkypLabs/python4yahdlc
.. |Code Coverage| image:: https://api.codacy.com/project/badge/Grade/313f8d5b98e04b24ae175e4fb5f6de8a
   :target: https://www.codacy.com/app/skyper/python4yahdlc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SkypLabs/python4yahdlc&amp;utm_campaign=Badge_Grade
.. |PyPI Package| image:: https://badge.fury.io/py/python4yahdlc.svg
   :target: https://badge.fury.io/py/python4yahdlc
