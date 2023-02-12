#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs some external modules. To install them:

::

    pip3 install python4yahdlc[examples]

To create a virtual serial bus, you can use socat as followed:

::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

Then, edit `ser.port` variable as needed.
"""

import signal
from sys import exit as sys_exit
from sys import stderr
from time import sleep

import serial

# pylint: disable=no-name-in-module
from yahdlc import (
    FRAME_ACK,
    FRAME_DATA,
    FRAME_NACK,
    FCSError,
    MessageError,
    frame_data,
    get_data,
)

# Serial port configuration
ser = serial.Serial()
ser.port = "/dev/pts/5"
ser.baudrate = 9600
ser.timeout = 0

print("[*] Connection...")

try:
    ser.open()
except serial.SerialException as err:
    stderr.write(f"[x] Serial connection problem: {err}\n")
    sys_exit(1)

print("[*] Sending data frame...")
ser.write(frame_data("test", FRAME_DATA, 0))

print("[*] Waiting for (N)ACK...")


def timeout_handler(signum, frame):
    """
    Timeout handler.
    """

    raise TimeoutError("Timeout")


signal.signal(signal.SIGALRM, timeout_handler)
# 1-second timeout
signal.alarm(1)

while True:
    try:
        # 200 µs
        sleep(200 / 1000000.0)
        data, ftype, seq_no = get_data(ser.read(ser.inWaiting()))
        signal.alarm(0)
        break
    except MessageError:
        pass
    except FCSError:
        stderr.write("[x] Bad FCS\n")
        print("[*] Done")
        ser.close()
        sys_exit(0)
    except TimeoutError as err:
        stderr.write("[x] " + str(err) + "\n")
        print("[*] Done")
        ser.close()
        sys_exit(0)
    except KeyboardInterrupt:
        print("[*] Bye!")
        ser.close()
        sys_exit(0)

if ftype not in (FRAME_ACK, FRAME_NACK):
    stderr.write(f"[x] Bad frame type: {ftype}\n")
elif ftype == FRAME_ACK:
    print("[*] ACK received")

    if seq_no != 1:
        stderr.write(f"[x] Bad sequence number: {seq_no}\n")
    else:
        print("[*] Sequence number OK")
else:
    print("[*] NACK received")

    if seq_no != 0:
        stderr.write(f"[x] Bad sequence number: {seq_no}\n")
    else:
        print("[*] Sequence number OK")

print("[*] Done")
ser.close()
