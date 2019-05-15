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

from sys import exit as sys_exit
from sys import stderr, stdout
from time import sleep

import serial

# pylint: disable=no-name-in-module
from yahdlc import (FRAME_ACK, FRAME_DATA, FRAME_NACK, FCSError, MessageError,
                    frame_data, get_data)

# Serial port configuration
ser = serial.Serial()
ser.port = "/dev/pts/6"
ser.baudrate = 9600
ser.timeout = 0

stdout.write("[*] Connection...\n")

try:
    ser.open()
except serial.serialutil.SerialException as err:
    stderr.write(f"[x] Serial connection problem: {err}\n")
    sys_exit(1)

stdout.write("[*] Waiting for data...\n")

while True:
    try:
        # 200 µs
        sleep(200 / 1000000.0)
        data, ftype, seq_no = get_data(ser.read(ser.inWaiting()))
        break
    except MessageError:
        pass
    except FCSError:
        stderr.write("[x] Bad FCS\n")
        stdout.write("[*] Sending NACK...\n")
        ser.write(frame_data("", FRAME_NACK, 0))
        ser.close()
        sys_exit(0)
    except KeyboardInterrupt:
        ser.close()
        stdout.write("[*] Bye!\n")
        sys_exit(0)

FRAME_ERROR = False

if ftype != FRAME_DATA:
    stderr.write(f"[x] Bad frame type: {ftype}\n")
    FRAME_ERROR = True
else:
    stdout.write("[*] Data frame received\n")

if seq_no != 0:
    stderr.write(f"[x] Bad sequence number: {seq_no}\n")
    FRAME_ERROR = True
else:
    stdout.write("[*] Sequence number OK\n")

if FRAME_ERROR is False:
    stdout.write("[*] Sending ACK ...\n")
    ser.write(frame_data("", FRAME_ACK, 1))
else:
    stdout.write("[*] Sending NACK ...\n")
    ser.write(frame_data("", FRAME_NACK, 0))

stdout.write("[*] Done\n")
ser.close()
