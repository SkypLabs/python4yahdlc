#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs some external modules. To install them:

::

    pip3 install python4yahdlc[examples]

To create a virtual serial bus, you can use socat as followed:

::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

Then, edit `ser.port` variable as needed
"""

# pylint: disable=invalid-name

from sys import exit as sys_exit
from sys import stderr, stdout
from time import sleep

import serial
from fysom import Fysom

# pylint: disable=no-name-in-module
from yahdlc import (FRAME_ACK, FRAME_DATA, FRAME_NACK, FCSError, MessageError,
                    frame_data, get_data)

# Serial port configuration
ser = serial.Serial()
ser.port = "/dev/pts/6"
ser.baudrate = 9600
ser.timeout = 0


def serial_connection(e):
    """
    Serial connection state.

    Connect to the serial bus.
    """

    stdout.write("[*] Connection...\n")

    try:
        ser.open()
        e.fsm.connection_ok()
    except serial.serialutil.SerialException as err:
        stderr.write(f"[x] Serial connection problem: {err}\n")
        e.fsm.connection_ko()


def retry_serial_connection():
    """
    Retry serial connection state.

    Wait 3 seconds.
    """

    stdout.write("[*] Retry in 3 seconds...\n")
    sleep(3)


def wait_for_data(e):
    """
    Wait for data state.

    For wait an incoming data frame and trigger the appropriate transition.
    """

    stdout.write("[*] Waiting for data...\n")

    while True:
        try:
            _, ftype, seq_no = get_data(ser.read(ser.inWaiting()))
            break
        except MessageError:
            pass
        except FCSError:
            stderr.write("[x] Bad FCS\n")
            e.fsm.data_ko()

    if ftype != FRAME_DATA:
        stderr.write(f"[x] Bad frame type: {ftype}\n")
        e.fsm.data_ko()
    else:
        stdout.write("[*] Data frame received\n")

        if seq_no != 0:
            stderr.write(f"[x] Bad sequence number: {seq_no}\n")
        else:
            stdout.write("[*] Sequence number OK\n")

        e.fsm.data_ok()


def send_ack_frame(e):
    """
    Send ACK frame state.
    """

    stdout.write("[*] Sending ACK...\n")
    ser.write(frame_data("", FRAME_ACK, 1))
    e.fsm.ack_sent()


def send_nack_frame(e):
    """
    Send NACK frame state.
    """

    stdout.write("[*] Sending NACK...\n")
    ser.write(frame_data("", FRAME_NACK, 0))
    e.fsm.nack_sent()


try:
    fsm = Fysom({
        "initial": "init",
        "events": [
            {"name": "connection_ok", "src": "init", "dst": "wait_data"},
            {"name": "connection_ko", "src": "init", "dst": "init"},
            {"name": "data_ok", "src": "wait_data", "dst": "send_ack"},
            {"name": "data_ko", "src": "wait_data", "dst": "send_nack"},
            {"name": "ack_sent", "src": "send_ack", "dst": "wait_data"},
            {"name": "nack_sent", "src": "send_nack", "dst": "wait_data"},
        ],
        "callbacks": {
            "oninit": serial_connection,
            "onreenterinit": retry_serial_connection,
            "onconnection_ok": wait_for_data,
            "onconnection_ko": serial_connection,
            "ondata_ok": send_ack_frame,
            "ondata_ko": send_nack_frame,
            "onack_sent": wait_for_data,
            "onnack_sent": wait_for_data,
        },
    })
except KeyboardInterrupt:
    stdout.write("[*] Bye!\n")
    ser.close()
    sys_exit(0)
