#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from yahdlc import *
from sys import stdout, stderr

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
ser.write(frame_data('test', FRAME_DATA, 1))

stdout.write('[*] Waiting for (N)ACK ...\n')

while True:
	try:
		data, type, seq_no = get_data(ser.read(ser.inWaiting()))
		break
	except MessageError:
		pass
	except FCSError:
		stderr.write('[x] Bad FCS\n')
		stdout.write('[*] Done\n')
		ser.close()
		exit(0)
	except KeyboardInterrupt:
		stdout.write('[*] Bye !\n')
		ser.close()
		exit(0)

if type != FRAME_ACK and type != FRAME_NACK:
	stderr.write('[x] Bad frame type: {0}\n'.format(type))
elif type == FRAME_ACK:
	stdout.write('[*] ACK received\n')
else:
	stdout.write('[*] NACK received\n')

if seq_no != 2:
	stderr.write('[x] Bad sequence number: {0}\n'.format(seq_no))
else:
	stdout.write('[*] Sequence number OK\n')

stdout.write('[*] Done\n')
ser.close()
