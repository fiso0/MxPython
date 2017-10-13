#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
	f = open('BB10.LOG', 'rb')
	f_hex = open('BB10_hex.txt', 'w')
	f_bin = open('BB10_bin.txt', 'w')
	for line in f.readlines():
		f_hex.write(line.hex())
		f_hex.write('\n')
		f_bin.write(bin(int(line.hex(), 16)))
		f_bin.write('\n')
	f_hex.close()
	f_bin.close()
	f.close()
except Exception as e:
	print(e)
