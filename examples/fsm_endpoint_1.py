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

import signal
from sys import exit as sys_exit
from sys import stderr, stdout
from time import sleep

import serial
from fysom import Fysom

# pylint: disable=no-name-in-module
from yahdlc import (FRAME_ACK, FRAME_DATA, FRAME_NACK, MessageError,
                    frame_data, get_data)

# Serial port configuration.
ser = serial.Serial()
ser.port = "/dev/pts/5"
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


def send_data_frame(e):
    """
    Send data frame state.

    Send a test data frame.
    """

    stdout.write("[*] Sending data frame...\n")
    ser.write(frame_data("test", FRAME_DATA, 0))
    e.fsm.send_ok()


def wait_for_ack(e):
    """
    Wait for ACK state.

    Decode received HDLC frames and trigger the appropriate transition.
    """

    def timeout_handler(signum, frame):
        raise TimeoutError("[x] Timeout")

    stdout.write("[*] Waiting for (N)ACK...\n")

    signal.signal(signal.SIGALRM, timeout_handler)
    # 1-second timeout
    signal.alarm(1)

    while True:
        try:
            # 200 µs
            sleep(200 / 1000000.0)
            _, ftype, seq_no = get_data(ser.read(ser.inWaiting()))
            signal.alarm(0)
            break
        except MessageError:
            pass
        except TimeoutError as err:
            stderr.write(str(err) + "\n")
            e.fsm.timeout()

    if ftype not in (FRAME_ACK, FRAME_NACK):
        stderr.write(f"[x] Bad frame type: {ftype}\n")
        e.fsm.bad_frame_received()
    elif ftype == FRAME_ACK:
        stdout.write("[*] ACK received\n")

        if seq_no != 1:
            stderr.write(f"[x] Bad sequence number: {seq_no}\n")
        else:
            stdout.write("[*] Sequence number OK\n")

        e.fsm.ack_received()
    else:
        stdout.write("[*] NACK received\n")

        if seq_no != 0:
            stderr.write("[x] Bad sequence number: {seq_no}\n")
        else:
            stdout.write("[*] Sequence number OK\n")

        e.fsm.nack_received()


def pause(e):
    """
    Pause state.
    """

    sleep(1)
    e.fsm.timesup()


try:
    fsm = Fysom({
        "initial": "init",
        "events": [
            {"name": "connection_ok", "src": "init", "dst": "send_data"},
            {"name": "connection_ko", "src": "init", "dst": "init"},
            {"name": "send_ok", "src": "send_data", "dst": "wait_ack"},
            {"name": "ack_received", "src": "wait_ack", "dst": "pause"},
            {"name": "nack_received", "src": "wait_ack", "dst": "send_data"},
            {"name": "bad_frame_received", "src": "wait_ack", "dst": "pause"},
            {"name": "timeout", "src": "wait_ack", "dst": "send_data"},
            {"name": "timesup", "src": "pause", "dst": "send_data"},
        ],
        "callbacks": {
            "oninit": serial_connection,
            "onreenterinit": retry_serial_connection,
            "onconnection_ko": serial_connection,
            "onconnection_ok": send_data_frame,
            "onsend_ok": wait_for_ack,
            "onack_received": pause,
            "onnack_received": send_data_frame,
            "onbad_frame_received": pause,
            "ontimeout": send_data_frame,
            "ontimesup": send_data_frame,
        },
    })
except KeyboardInterrupt:
    stdout.write("[*] Bye!\n")
    ser.close()
    sys_exit(0)
