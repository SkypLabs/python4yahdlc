=============
python4yahdlc
=============

|Build Status| |Code Coverage|

python4yahdlc is a Python bindings for the
`yahdlc <https://github.com/bang-olufsen/yahdlc>`__ library.

Dependencies
============

To build and make the Python module work, you need the following
elements:

- Python 3
- The `setuptools <https://pypi.python.org/pypi/setuptools>`__ package

On Fedora
---------

::

    yum install python3-setuptools

On Debian
---------

::

    aptitude install python3-setuptools

Installation
============

With pip (recommanded)
----------------------

::

    pip3 install python4yahdlc

From sources
------------

::

    git clone https://github.com/SkypLabs/python4yahdlc.git
    cd python4yahdlc
    python3 setup.py install

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

    data, type, seq_no = get_data(frame)

For a more advanced use, take a look at the examples available in the
`examples <https://github.com/SkypLabs/python4yahdlc/tree/master/examples>`__
folder.

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
