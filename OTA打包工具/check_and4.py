#!/usr/bin/python3
# -*- coding: utf-8 -*-

import struct

while(1):
	filename = input('filename:')

	with open(filename,'rb') as f_ota:
		sum = 0
		xor = 0

		f_ota.seek(0,0)
		data_ota = f_ota.read()
		i = 0
		num = int(len(data_ota)/4)
		for i in range(num):
			data32 = struct.unpack('i', data_ota[4*i:4*i+4])[0]
			sum = sum + data32
			xor = xor ^ data32

	print('AND: ', end='')
	print(str(hex(sum&0xFFFFFFFF))+'('+str(hex(sum))+')', end='')
	print('\r\n', end='')
	print('XOR: ', end='')
	print(str(hex(xor)), end='')
	print('\r\n', end='')
	print('end\r\n', end='')
