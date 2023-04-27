#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script needs some external modules. To install them:

::

    pip install python4yahdlc[examples]

To create a virtual serial bus, you can use socat as followed:

::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

Then, edit `ser.port` variable as needed.
"""

import signal
from sys import exit as sys_exit
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
SERIAL_PORT = "/dev/pts/5"
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 0


# -------------------------------------------------- #
# Set up timeout handler
# -------------------------------------------------- #
def timeout_handler(signum, frame):
    """
    Timeout handler.
    """

    raise TimeoutError("Timeout")


signal.signal(signal.SIGALRM, timeout_handler)
# 1-second timeout.
signal.alarm(1)

# -------------------------------------------------- #
# Open serial port
# -------------------------------------------------- #
print("[*] Connection...")

try:
    with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
        # -------------------------------------------------- #
        # Send HDLC frame
        # -------------------------------------------------- #
        print("[*] Sending data frame...")
        ser.write(frame_data("test", FRAME_DATA, 0))

        # -------------------------------------------------- #
        # Wait for (N)ACK
        # -------------------------------------------------- #
        print("[*] Waiting for (N)ACK...")
        while True:
            try:
                # 200 µs.
                sleep(200 / 1000000.0)
                data, ftype, seq_no = get_data(ser.read(ser.in_waiting))
                signal.alarm(0)
                break
            except MessageError:
                # No HDLC frame detected.
                pass
            except FCSError:
                sys_exit("[x] Bad FCS")
            except TimeoutError as err:
                sys_exit(f"[x] {str(err)}")
            except KeyboardInterrupt:
                print("[*] Bye!")
                sys_exit(0)
except serial.SerialException as err:
    sys_exit(f"[x] Serial connection problem: {err}")

# -------------------------------------------------- #
# Handle response
# -------------------------------------------------- #
if ftype not in (FRAME_ACK, FRAME_NACK):
    sys_exit(f"[x] Bad frame type: {ftype}")
elif ftype == FRAME_ACK:
    print("[*] ACK received")

    if seq_no != 1:
        sys_exit(f"[x] Bad sequence number: {seq_no}")
    else:
        print("[*] Sequence number OK")
else:
    print("[*] NACK received")

    if seq_no != 0:
        sys_exit(f"[x] Bad sequence number: {seq_no}")
    else:
        print("[*] Sequence number OK")
