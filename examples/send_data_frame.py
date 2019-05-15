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

import signal
from sys import exit as sys_exit
from sys import stderr, stdout
from time import sleep

import serial

# pylint: disable=no-name-in-module
from yahdlc import (FRAME_ACK, FRAME_DATA, FRAME_NACK, FCSError, MessageError,
                    frame_data, get_data)

# Serial port configuration
ser = serial.Serial()
ser.port = "/dev/pts/5"
ser.baudrate = 9600
ser.timeout = 0

stdout.write("[*] Connection...\n")

try:
    ser.open()
except serial.serialutil.SerialException as err:
    stderr.write(f"[x] Serial connection problem: {err}\n")
    sys_exit(1)

stdout.write("[*] Sending data frame...\n")
ser.write(frame_data("test", FRAME_DATA, 0))

stdout.write("[*] Waiting for (N)ACK...\n")


def timeout_handler():
    """
    Timeout handler.
    """

    raise TimeoutError("[x] Timeout")


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
        stdout.write("[*] Done\n")
        ser.close()
        sys_exit(0)
    except TimeoutError as err:
        stderr.write(str(err) + "\n")
        stdout.write("[*] Done\n")
        ser.close()
        sys_exit(0)
    except KeyboardInterrupt:
        stdout.write("[*] Bye!\n")
        ser.close()
        sys_exit(0)

if ftype not in (FRAME_ACK, FRAME_NACK):
    stderr.write(f"[x] Bad frame type: {ftype}\n")
elif ftype == FRAME_ACK:
    stdout.write("[*] ACK received\n")

    if seq_no != 1:
        stderr.write(f"[x] Bad sequence number: {seq_no}\n")
    else:
        stdout.write("[*] Sequence number OK\n")
else:
    stdout.write("[*] NACK received\n")

    if seq_no != 0:
        stderr.write(f"[x] Bad sequence number: {seq_no}\n")
    else:
        stdout.write("[*] Sequence number OK\n")

stdout.write("[*] Done\n")
ser.close()
