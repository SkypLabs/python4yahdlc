#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs some external modules. To install them:

::

    pip install python4yahdlc[examples]

To create a virtual serial bus, you can use socat as follows:

::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

Then, edit `ser.port` accordingly.
"""

from sys import stderr
from time import sleep

import serial
from fysom import Fysom

from yahdlc import (
    FRAME_ACK,
    FRAME_DATA,
    FRAME_NACK,
    FCSError,
    MessageError,
    frame_data,
    get_data,
)

# -------------------------------------------------- #
# Serial port configuration
# -------------------------------------------------- #
ser = serial.Serial()
ser.port = "/dev/pts/6"
ser.baudrate = 9600
ser.timeout = 0


def serial_connection(e):
    """
    Serial connection state.

    Connect to the serial bus.
    """

    print("[*] Connection...")

    try:
        ser.open()
        e.fsm.connection_ok()
    except serial.SerialException as err:
        stderr.write(f"[x] Serial connection problem: {err}\n")
        e.fsm.connection_ko()


def retry_serial_connection(e):
    """
    Retry serial connection state.

    Wait 3 seconds.
    """

    print("[*] Retry in 3 seconds...")
    sleep(3)


def wait_for_data(e):
    """
    Wait for data state.

    For wait an incoming data frame and trigger the appropriate transition.
    """

    print("[*] Waiting for data...")

    while True:
        try:
            _, ftype, seq_no = get_data(ser.read(ser.in_waiting))
            break
        except MessageError:
            # No HDLC frame detected.
            pass
        except FCSError:
            stderr.write("[x] Bad FCS\n")
            e.fsm.data_ko()

    if ftype != FRAME_DATA:
        stderr.write(f"[x] Bad frame type: {ftype}\n")
        e.fsm.data_ko()
    else:
        print("[*] Data frame received")

        if seq_no != 0:
            stderr.write(f"[x] Bad sequence number: {seq_no}\n")
        else:
            print("[*] Sequence number OK")

        e.fsm.data_ok()


def send_ack_frame(e):
    """
    Send ACK frame state.
    """

    print("[*] Sending ACK...")
    ser.write(frame_data("", FRAME_ACK, 1))
    e.fsm.ack_sent()


def send_nack_frame(e):
    """
    Send NACK frame state.
    """

    print("[*] Sending NACK...")
    ser.write(frame_data("", FRAME_NACK, 0))
    e.fsm.nack_sent()


if __name__ == "__main__":
    try:
        Fysom(
            {
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
            }
        )
    except KeyboardInterrupt:
        print("[*] Bye!")
    finally:
        ser.close()
