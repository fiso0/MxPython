#!/usr/bin/python3
# -*- coding: utf-8 -*-

def checksum(input):
	chrstr = [input[i:i+2] for i in range(0,len(input),2)]
	sum = int(chrstr[0],16)
	for a in chrstr[1:]:
		sum = sum ^ int(a,16)
	return sum

test = "0000000001234567765432138001100c0600000001f10019"
res = checksum(test)
print(hex(res))

test = "000000000867478a2aaa7a275028010003"
res = checksum(test)
print(hex(res))

test = "000000000866888a2a237229800111010a0d160001f10001"
res = checksum(test)
print(hex(res))