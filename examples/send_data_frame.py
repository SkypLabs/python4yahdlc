#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script needs some external modules.
# To install them:
# pip3 install pyserial

# To create a virtual serial bus, you can use socat as followed:
# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# Then, edit ser.port variable as needed

import serial
import signal
from yahdlc import *
from sys import stdout, stderr
from time import sleep

# Serial port configuration
ser = serial.Serial()
ser.port = '/dev/pts/5'
ser.baudrate = 9600
ser.timeout = 0

stdout.write('[*] Connection ...\n')

try:
	ser.open()
except serial.serialutil.SerialException as e:
	stderr.write('[x] Serial connection problem : {0}\n'.format(e))
	exit(1)

stdout.write('[*] Sending data frame ...\n')
ser.write(frame_data('test', FRAME_DATA, 0))

stdout.write('[*] Waiting for (N)ACK ...\n')

def timeout_handler(signum, frame):
	raise TimeoutError('[x] Timeout')

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
		stderr.write('[x] Bad FCS\n')
		stdout.write('[*] Done\n')
		ser.close()
		exit(0)
	except TimeoutError as e:
		stderr.write(str(e) + '\n')
		stdout.write('[*] Done\n')
		ser.close()
		exit(0)
	except KeyboardInterrupt:
		stdout.write('[*] Bye !\n')
		ser.close()
		exit(0)

if ftype != FRAME_ACK and ftype != FRAME_NACK:
	stderr.write('[x] Bad frame type: {0}\n'.format(ftype))
elif ftype == FRAME_ACK:
	stdout.write('[*] ACK received\n')

	if seq_no != 1:
		stderr.write('[x] Bad sequence number: {0}\n'.format(seq_no))
	else:
		stdout.write('[*] Sequence number OK\n')
else:
	stdout.write('[*] NACK received\n')

	if seq_no != 0:
		stderr.write('[x] Bad sequence number: {0}\n'.format(seq_no))
	else:
		stdout.write('[*] Sequence number OK\n')

stdout.write('[*] Done\n')
ser.close()
