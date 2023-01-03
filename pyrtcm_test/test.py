#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyrtcm import RTCMReader

if __name__ == '__main__':
	stream = open('test_data.txt', 'rb')
	rtr = RTCMReader(stream)
	try:
		for (raw_data, parsed_data) in rtr:
			print(parsed_data.identity)
	except Exception as e:
		print(e)
	pass