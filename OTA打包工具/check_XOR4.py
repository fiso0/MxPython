#!/usr/bin/python3
# -*- coding: utf-8 -*-

while(1):
	filename = input('filename:')

	with open(filename,'rb') as f_ota:
		ck_byte = [0,0,0,0]

		f_ota.seek(0,0)
		data_ota = f_ota.read()
		i = 0
		num = int(len(data_ota)/4)
		for i in range(num):
			ck_byte[0] = ck_byte[0] ^ data_ota[4*i]
			ck_byte[1] = ck_byte[1] ^ data_ota[4*i+1]
			ck_byte[2] = ck_byte[2] ^ data_ota[4*i+2]
			ck_byte[3] = ck_byte[3] ^ data_ota[4*i+3]

		print(ck_byte)
		print('end\r\n')
