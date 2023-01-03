#!/usr/bin/python3
# -*- coding: utf-8 -*-

# print(chr(0x31)) # 1

test_1 = '''
30 30 30 30 2c 31 33 38 30 38 36 32 38 38 36 33 2c 31 2c 30 30 30 30 30 30 30 30 30 30 30 30 31 30 30 30 30 30 30 30 30 30 30 30 32 30 30 30 30 30 30 30 30 30 30 30 2c 31 2c 30 31 30
'''


def ascii2char(data_list):
	result = []
	for data in data_list:
		a = int(data,16)
		result.append(chr(a))
	return result


test_list = test_1.strip().split(' ')
res = ascii2char(test_list)
print(''.join(res))