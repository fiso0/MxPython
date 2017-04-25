#!/usr/bin/python3
# -*- coding: utf-8 -*-

def addBlank(message):
	# 每两个字符之间加一个空格
	chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]
	return ' '.join(chrstr)

def removeBlank(message):
	# 删除全部空格
	return message.replace(' ','')

def formatBody(msg_id, body):
	# 根据msg_id格式化消息体body

	# 删除输入内容的空格
	msg_id = removeBlank(msg_id)
	body = removeBlank(body)

	# 根据msg_id对body分段
	body_sec = []
	if(msg_id == '0200'): # 位置上报
		body_sec_len = [8,8,8,8,4,4,4,12]
	elif(msg_id == '8001' or msg_id == '0001'): # 平台通用应答 终端通用应答
		body_sec_len = [4,4,2]
	elif(msg_id == '0100'): # 终端注册
		body_sec_len = [4,4,10,40,14,2,0]
	elif(msg_id == '8100'): # 终端注册应答
		body_sec_len = [4,2,0]
	else: # 其他消息不作处理
		return body

	i = 0
	for len in body_sec_len:
		if len == 0: # 0 表示不限定长度
			body_sec.append(body[i:])
		else:
			body_sec.append(body[i:i+len])
		i += len

	# 对每段内容加空格
	body_sec = [addBlank(sec) for sec in body_sec]

	# 用换行符连接每段内容
	new_body = '\n'.join(body_sec)
	return new_body


if __name__ == '__main__':
	res = formatBody('0200','000000000000000001d17a5906d183790032000a00b4170411144742')
	print(res+'\n')

	res = formatBody('8001','00 26 01 02 00')
	print(res+'\n')

	res = formatBody('0100','002c0133373039363054372d54383038000000000000000000000000003033323931373001d4c14238383838')
	print(res+'\n')

	res = formatBody('8100','00 25 00 02 00 00 00 00 15')
	print(res+'\n')

	test = input('input:')
