#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs some external modules. To install them:

::

    pip install python4yahdlc[examples]

To create a virtual serial bus, you can use socat as followed:

::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

Then, edit `ser.port` variable as needed
"""

from sys import exit as sys_exit
from sys import stderr
from time import sleep

import serial

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
SERIAL_PORT = "/dev/pts/6"
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 0

# -------------------------------------------------- #
# Open serial port
# -------------------------------------------------- #
print("[*] Connection...")

try:
    with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
        # -------------------------------------------------- #
        # Wait for HDLC frame
        # -------------------------------------------------- #
        print("[*] Waiting for data...")

        while True:
            try:
                # 200 µs
                sleep(200 / 1000000.0)
                data, ftype, seq_no = get_data(ser.read(ser.in_waiting))
                break
            except MessageError:
                # No HDLC frame detected.
                pass
            except FCSError:
                stderr.write("[x] Bad FCS\n")

                print("[*] Sending NACK...")
                ser.write(frame_data("", FRAME_NACK, 0))
                sys_exit(0)
            except KeyboardInterrupt:
                print("[*] Bye!")
                sys_exit(0)

        # -------------------------------------------------- #
        # Handle HDLC frame received
        # -------------------------------------------------- #
        FRAME_ERROR = False

        if ftype != FRAME_DATA:
            stderr.write(f"[x] Bad frame type: {ftype}\n")
            FRAME_ERROR = True
        else:
            print("[*] Data frame received")

        if seq_no != 0:
            stderr.write(f"[x] Bad sequence number: {seq_no}\n")
            FRAME_ERROR = True
        else:
            print("[*] Sequence number OK")

        if FRAME_ERROR is False:
            print("[*] Sending ACK ...")
            ser.write(frame_data("", FRAME_ACK, 1))
        else:
            print("[*] Sending NACK ...")
            ser.write(frame_data("", FRAME_NACK, 0))
except serial.SerialException as err:
    sys_exit(f"[x] Serial connection problem: {err}")
