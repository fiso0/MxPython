#!/usr/bin/python3
# -*- coding: utf-8 -*-

POLYCRC24Q = 0x1864CFB


def crc24(data8, len):
	cs = 0
	for alen in range(len):
		cs ^= data8[alen] << 16
		for i in range(8):
			cs <<= 1
			if cs & 0x1000000:
				cs ^= POLYCRC24Q
	cs = cs & 0xFFFFFF
	return cs


if __name__ == '__main__':
	print('示例:D300133ED000033AAD4850DA8BA64C3A1C077D94A7FB, CRC24结果:850C8C')
	data = input("数据:")
	data_b = bytes().fromhex(data)
	crc = crc24(data_b, data_b.__len__())
	print('CRC24结果:' + hex(crc))
	input('')
