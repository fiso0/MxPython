#!/usr/bin/python3
# -*- coding: utf-8 -*-

# def read_from_file():
# 	with open("unicode2chinese.txt",'rb') as f:
# 		data = f.readlines()
# 		for line in data:
# 			line_chinese = line.strip().decode('unicode_escape')
# 			print(line_chinese)

def read_origin_file(file):
	result=[]
	with open(file,'rb') as f:
		data = f.readlines()
		# print(data)
		for i in range(0,len(data),2):
			a = int(data[i].strip().replace(b"0x",b""),16)
			b = int(data[i+1].strip().replace(b"0x",b""),16)
			res=b'\\u%02x%02x'%(a,b)
			res1=res.decode('unicode_escape')
			result.append(res1)
			try:
				print(res1,end='')
			except:
				pass
	# print(''.join(result))

# print('\u0500\u03F9')

# read_origin_file('10086_SMS_1.txt')
try:
	while(1):
		file = input("待解析文件：")
		read_origin_file(file)
		input()
except Exception as e:
	input(e)
# read_from_file()