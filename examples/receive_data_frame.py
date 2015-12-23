#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script needs some external modules.
# To install them:
# pip3 install pyserial

# To create a virtual serial bus, you can use socat as followed:
# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# Then, edit ser.port variable as needed

import serial
from yahdlc import *
from sys import stdout, stderr
from time import sleep

# Serial port configuration
ser = serial.Serial()
ser.port = '/dev/pts/6'
ser.baudrate = 9600
ser.timeout = 0

stdout.write('[*] Connection ...\n')

try:
	ser.open()
except serial.serialutil.SerialException as e:
	stderr.write('[x] Serial connection problem : {0}\n'.format(e))
	exit(1)

stdout.write('[*] Waiting for data ...\n')

while True:
	try:
		# 200 µs
		sleep(200 / 1000000.0)
		data, type, seq_no = get_data(ser.read(ser.inWaiting()))
		break
	except MessageError:
		pass
	except FCSError:
		stderr.write('[x] Bad FCS\n')
		stdout.write('[*] Sending NACK ...\n')
		ser.write(frame_data('', FRAME_NACK, 0))
		ser.close()
		exit(0)
	except KeyboardInterrupt:
		ser.close()
		stdout.write('[*] Bye !\n')
		exit(0)

frame_error = False

if type != FRAME_DATA:
	stderr.write('[x] Bad frame type: {0}\n'.format(type))
	frame_error = True
else:
	stdout.write('[*] Data frame received\n')

if seq_no != 0:
	stderr.write('[x] Bad sequence number: {0}\n'.format(seq_no))
	frame_error = True
else:
	stdout.write('[*] Sequence number OK\n')

if frame_error == False:
	stdout.write('[*] Sending ACK ...\n')
	ser.write(frame_data('', FRAME_ACK, 1))
else:
	stdout.write('[*] Sending NACK ...\n')
	ser.write(frame_data('', FRAME_NACK, 0))

stdout.write('[*] Done\n')
ser.close()
