#!/usr/bin/python3
# -*- coding: utf-8 -*-

def tran7e(msg):
	# 转义
	# 消息不带空格
	msg_len = len(msg)
	new_msg = msg
	i = 0
	while(i<msg_len):
		if new_msg[i] == '7' and new_msg[i+1] == 'e':
			new_msg = new_msg[:i] + '7d02' + new_msg[i+2:]
		elif new_msg[i] == '7' and new_msg[i+1] == 'd':
			new_msg = new_msg[:i] + '7d01' + new_msg[i+2:]
		i += 2
	if new_msg != msg:
		print('tran7e result: '+new_msg)
	return new_msg

def detran7e(msg):
	# 逆转义
	# 消息不带空格
	msg_len = len(msg)
	new_msg = msg
	i = 0
	while(i<msg_len):
		if new_msg[i:i+4] == '7d02':
			new_msg = new_msg[:i] + '7e' + new_msg[i+4:]
		elif new_msg[i:i+4] == '7d01':
			new_msg = new_msg[:i] + '7d' + new_msg[i+4:]
		i += 2
	if new_msg != msg:
		print('tran7e result: '+new_msg)
	return new_msg

if __name__ == '__main__':
	test = input('input:')
	# res = tran7e(test)
	res = detran7e(test)
	print(res)