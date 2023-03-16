========
Examples
========

This folder contains several code examples of how to use `python4yahdlc
<https://github.com/SkypLabs/python4yahdlc>`_.

The code examples work in pairs: `send_data_frame.py
<https://github.com/SkypLabs/python4yahdlc/blob/main/examples/send_data_frame.py>`_
works with `receive_data_frame.py
<https://github.com/SkypLabs/python4yahdlc/blob/main/examples/receive_data_frame.py>`_
and `fsm_endpoint_1.py
<https://github.com/SkypLabs/python4yahdlc/blob/main/examples/fsm_endpoint_1.py>`_
works with `fsm_endpoint_2.py
<https://github.com/SkypLabs/python4yahdlc/blob/main/examples/fsm_endpoint_2.py>`_.

Setting up a virtual serial bus
===============================

To make the two code examples of each pair work together, you need a serial bus
of communication. The easiest way to set up a serial bus is to use a virtual
one. `socat <http://www.dest-unreach.org/socat/>`_ is a great tool for carrying
out this task:

.. code:: sh

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

This command will create two virtual devices (e.g. ``/dev/pts/5`` and
``/dev/pts/6``). Everything you write in one will be echoed in the other and
vice versa.

``send_data_frame.py`` and ``receive_data_frame.py``
====================================================

These two code examples need ``pyserial`` as dependency:

.. code:: sh

    pip install --upgrade pyserial

``fsm_endpoint_1.py`` and ``fsm_endpoint_2.py``
===============================================

These two code examples need ``pyserial`` and ``fysom`` as dependencies:

.. code:: sh

    pip install --upgrade pyserial fysom

``fysom`` is used to define the Finite-State Machines (FSM) of the two
endpoints.

The sending FSM endpoint:

.. code:: mermaid

	stateDiagram-v2
    init --> send_data: connection_ok
    init --> init: connection_ko

    send_data --> wait_ack: send_ok

    wait_ack --> pause: ack_received
    wait_ack --> send_data: nack_received
    wait_ack --> send_data: timeout
    wait_ack --> pause: bad_frame_received

    pause --> send_data: timeup

The receiving FSM endpoint:

.. code:: mermaid

	stateDiagram-v2
    init --> wait_data: connection_ok
    init --> init: connection_ko

    wait_data --> send_ack: data_ok
    wait_data --> send_nack: data_ko

    send_ack --> wait_data: ack_sent

    send_nack --> wait_data: nack_sent
