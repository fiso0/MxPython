#!/usr/bin/python3
# -*- coding: utf-8 -*-

import struct

def open_file(file):
	with open(file, 'r') as f:
		data = f.readlines()
	return data  # string list

def open_result():
	RESULT_FILE = 'encoder_result.txt'
	try:
		f = open(RESULT_FILE, 'xb')
	except FileExistsError:
		f = open(RESULT_FILE, 'wb')
	except Exception as e:
		print(e)

	f.write(struct.pack('B', 0)*16) # file header: 16 * 0
	# f.close()
	return f

def write_msg(f,header,content):
	f.write(struct.pack('>H', header)) # big-endian unsigned short (2 bytes)
	f.write(content.encode('ascii'))
	return

def write_wr(f,wr):
	f.seek(0)
	f.write(struct.pack('>I', wr)) # big-endian unsigned int (4 bytes)

def basic():
	file = input('数据文件(.txt)地址：')
	try:
		data = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	f=open_result()
	total_len=16
	for line in data:
		try:
			(msg_type,msg_len,msg_content) = line.strip().split(maxsplit=2) #空字符分隔，3段
		except:
			(msg_type,msg_content) = line.strip().split(maxsplit=1) #空字符分隔，2段（无长度字段）
			msg_len = len(msg_content)

		msg_header = (int(msg_type) << 12) | int(msg_len)
		write_msg(f, msg_header, msg_content)

		total_len += (int(msg_len)+2)

	write_wr(f,total_len)
	f.close()

note='''
输入txt文件，每行一条数据，格式为：数据类型 数据长度 数据内容
示例：
14	277	{"devicename":"135790246811230","wifi":[{"mac":"02:bd:5f:15:b9:dd","rssi":"-49"},{"mac":"50:bd:5f:15:b9:dd","rssi":"-50"},{"mac":"b8:08:d7:86:6c:50","rssi":"-54"},{"mac":"02:27:1d:1a:59:2e","rssi":"-58"},{"mac":"12:27:1d:1a:59:2e","rssi":"-58"}],"datetime":"2015-4-1 00:09:30"}
13	101	{"devicename":"135790246811230","lng":"114.394017","lat":"30.504774","datetime":"2018-6-29 10:32:25"}
14	278	{"devicename":"135790246811230","wifi":[{"mac":"02:27:1d:1a:59:2e","rssi":"-57"},{"mac":"00:27:1d:1a:59:2e","rssi":"-57"},{"mac":"50:bd:5f:15:b9:dd","rssi":"-57"},{"mac":"02:bd:5f:15:b9:dd","rssi":"-57"},{"mac":"12:27:1d:1a:59:2e","rssi":"-58"}],"datetime":"2018-6-29 10:33:28"}
'''
print(note)
basic()
input('done')