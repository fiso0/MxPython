#!/usr/bin/python3
# -*- coding: utf-8 -*-

def num2hex(int_num, digits, hasBlank = True):
	format = '%%0%dX' % digits
	int_num = int(int_num)
	new_text = format % int_num
	if hasBlank and digits > 2:
		chr_str = [new_text[i:i + 2] for i in range(0, len(new_text), 2)]
		new_text = ' '.join(chr_str)
	return new_text


def string2hex(string, digits, hasBlank = True, rear0 = False):
	string = string.strip().replace(' ','')
	str_len = len(string)
	if str_len <= digits:
		if rear0:
			new_text = string + '0'*(digits - str_len)
		else:
			new_text = '0'*(digits - str_len) + string
	else:
		new_text = string[0:digits]
	if hasBlank and digits > 2:
		chr_str = [new_text[i:i + 2] for i in range(0, len(new_text), 2)]
		new_text = ' '.join(chr_str)
	return new_text


if __name__ == '__main__':
	print(string2hex('12345', 12))
	print(num2hex(114000000, 8))
	print(num2hex(114000000, 8, False))
	print(num2hex(1, 4))
	print(num2hex(1, 4, False))