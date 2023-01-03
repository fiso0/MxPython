#!/usr/bin/python3
# -*- coding: utf-8 -*-

def u2c(data_str):
	'''
	转换unicode为字符
	unicode格式：每2个字节对应1个字符，字节间可以以空格、换行分隔，字节为十六进制，前面带或不带0x均可
	:param data_str:待转换内容
	:return:转换结果
	'''
	result=[]

	if(len(data_str) < 3):
		return ''

	data = data_str.split() # If sep is not specified or is None, any whitespace string is a separator and empty strings are removed from the result.

	for i in range(0,len(data)-1,2):
		try:
			a = int(data[i],16)
			b = int(data[i+1],16)
			res=b'\\u%02x%02x'%(a,b)
			res1=res.decode('unicode_escape')
			result.append(res1)
			# print(res1,end='')
		except Exception as e:
			print(e)
	return result

def a2c(data_str):
	'''
	转换ascii码为字符
	ascii格式：每1个字节对应1个字符，字节间可以以空格、换行分隔，字节为十六进制，前面带或不带0x均可
	:param data_str:待转换内容
	:return:转换结果
	'''
	result=[]

	data = data_str.split()

	for i in data:
		try:
			a = int(i,16)
			result.append(chr(a))
		except Exception as e:
			print(e)
	return result

def c2a(data_str):
	'''
	转换字符为ascii码
	:param data_str: 待转换内容
	:return: 转换结果
	'''
	result=[]

	data = data_str

	for i in data:
		try:
			a = ord(i)
			result.append('0x%x'%a)
		except Exception as e:
			print(e)
	return result

def addBlank(message):
	# 每两个字符之间加一个空格
	chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]
	return ' '.join(chrstr)


def transformat(str_in,f_from,f_to,delete_blank=False):
	str_out = ''
	if str_in == '':
		return str_out

	if f_from.upper() == f_to.upper():
		# 无需转换
		str_out = str_in

	elif f_from.upper() == 'HEX' and f_to.upper() == 'DEC':
		# 十六进制 转为 十进制 例如 30 转为 48
		if(delete_blank): # 删除空格
			str_out = str(int(str_in.replace(' ',''),16))
		else: # 支持一次性转换多个输入（以空格分隔）
			str_out = ' '.join([str(int(a, 16)) for a in str_in.split(' ')])

	elif f_from.upper() == 'HEX' and f_to.upper() == 'ASCII':
		# 十六进制 转为 ASCII码 例如 30 转为 0
		str_out = a2c(str_in)

	return str_out


if __name__ == '__main__':
	out = transformat('30 30','hex','ascii')
	print(out)
	input()