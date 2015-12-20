#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from yahdlc import *
from fysom import Fysom
from sys import stdout, stderr
from time import sleep

# Serial port configuration
ser = serial.Serial()
ser.port = '/dev/pts/6'
ser.baudrate = 9600
ser.timeout = 0

def serial_connection(e):
	stdout.write('[*] Connection ...\n')

	try:
		ser.open()
		e.fsm.connection_ok()
	except serial.serialutil.SerialException as err:
		stderr.write('[x] Serial connection problem : {0}\n'.format(err))
		e.fsm.connection_ko()

def retry_serial_connection(e):
	stdout.write('[*] Retry in 3 seconds ...\n')
	sleep(3)

def wait_for_data(e):
	stdout.write('[*] Waiting for data ...\n')

	while True:
		try:
			data, type, seq_no = get_data(ser.read(ser.inWaiting()))
			break
		except MessageError:
			pass
		except FCSError:
			stderr.write('[x] Bad FCS\n')
			e.fsm.data_ko()

	if type != FRAME_DATA:
		stderr.write('[x] Bad frame type: {0}\n'.format(type))
		e.fsm.data_ko()
	else:
		stdout.write('[*] Data frame received\n')

		if seq_no != 1:
			stderr.write('[x] Bad sequence number: {0}\n'.format(seq_no))
		else:
			stdout.write('[*] Sequence number OK\n')

		e.fsm.data_ok()

def send_ack_frame(e):
	stdout.write('[*] Sending ACK ...\n')
	ser.write(frame_data('', FRAME_ACK, 2))
	e.fsm.ack_sent()

def send_nack_frame(e):
	stdout.write('[*] Sending NACK ...\n')
	ser.write(frame_data('', FRAME_NACK, 2))
	e.fsm.nack_sent()

try:
	fsm = Fysom({
		'initial': 'init',
		'events': [
			{'name': 'connection_ok', 'src': 'init', 'dst': 'wait_data'},
			{'name': 'connection_ko', 'src': 'init', 'dst': 'init'},
			{'name': 'data_ok', 'src': 'wait_data', 'dst': 'send_ack'},
			{'name': 'data_ko', 'src': 'wait_data', 'dst': 'send_nack'},
			{'name': 'ack_sent', 'src': 'send_ack', 'dst': 'wait_data'},
			{'name': 'nack_sent', 'src': 'send_nack', 'dst': 'wait_data'},
		],
		'callbacks': {
			'oninit': serial_connection,
			'onreenterinit': retry_serial_connection,
			'onconnection_ok': wait_for_data,
			'onconnection_ko': serial_connection,
			'ondata_ok': send_ack_frame,
			'ondata_ko': send_nack_frame,
			'onack_sent': wait_for_data,
			'onnack_sent': wait_for_data,
		},
	})
except KeyboardInterrupt:
	stdout.write('[*] Bye !\n')
	ser.close()
	exit(0)
