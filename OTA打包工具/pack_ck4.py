#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
更新：
整个文件最后补0，补0后长度为4的倍数
最前面加4字节校验（异或），少4个补0（170个）

将升级文件放入本目录下并重命名为"mcu"和"mtk"
双击pack.py运行
程序将自动查找同目录下的文件"mcu"和"mtk"
根据提示输入版本号并回车
出现Finish表示运行完毕
打包结果为"ota"文件
'''

import os
import struct

# file names
file_mcu = 'mcu'
file_mtk = 'mtk'
file_ota = 'ota'

# version
ver_mcu = b''
ver_mtk = b''

# get file size and version
size_mcu = 0
size_mtk = 0
try:
	size_mcu = os.path.getsize(file_mcu)
	ver_mcu = input('MCU version:').encode('ascii')
except FileNotFoundError:
	print("No file 'mcu'")
except Exception as e:
	print(e)
try:
	size_mtk = os.path.getsize(file_mtk)
	ver_mtk = input('MTK version:').encode('ascii')
except FileNotFoundError:
	print("No file 'mtk'")
except Exception as e:
	print(e)

base_mcu = 256
base_mtk = 256+size_mcu

total_size = 256+size_mcu+size_mtk # 文件头+MCU文件长度+MTK文件长度
if total_size%4 == 0:
	tail_zero_len = 0
else:
	tail_zero_len = 4 - total_size%4 # 最后需要补0的长度

# get data
data_mcu = None
cs_mcu = 0
try:
	with open(file_mcu,'rb') as f_mcu:
		data_mcu = f_mcu.read()
	for data in data_mcu:
		cs_mcu += data
	cs_mcu = cs_mcu&0xFF
except Exception as e:
	if size_mcu == 0:
		pass
	else:
		print(e)

data_mtk = None
cs_mtk = 0
try:
	with open (file_mtk, 'rb') as f_mtk:
		data_mtk = f_mtk.read()
	for data in data_mtk:
		cs_mtk += data
	cs_mtk = cs_mtk&0xFF
except Exception as e:
	if size_mtk == 0:
		pass
	else:
		print(e)

# create file
try:
	f_ota = open(file_ota, 'xb+')
except FileExistsError:
	f_ota = open(file_ota, 'wb+')
except Exception as e:
	print(e)

# skip check byte
ck_byte = [0,0,0,0]
f_ota.write(struct.pack('B', ck_byte[0]))  # check byte 4 bytes
f_ota.write(struct.pack('B', ck_byte[1]))
f_ota.write(struct.pack('B', ck_byte[2]))
f_ota.write(struct.pack('B', ck_byte[3]))

# write info
f_ota.write(struct.pack('32s',ver_mcu)) # version 32 bytes
f_ota.write(struct.pack('i', size_mcu)) # size 4 bytes
f_ota.write(struct.pack('i', base_mcu)) # base 4 bytes
f_ota.write(struct.pack('B', cs_mcu))   # checksum 1 bytes

f_ota.write(struct.pack('32s',ver_mtk)) # version 32 bytes
f_ota.write(struct.pack('i', size_mtk)) # size 4 bytes
f_ota.write(struct.pack('i', base_mtk)) # base 4 bytes
f_ota.write(struct.pack('B', cs_mtk))   # checksum 1 bytes

# write 0
f_ota.write(struct.pack('170s',b''))    # 173*0

# write data
if data_mcu is not None:
	f_ota.write(data_mcu)
# noinspection PyUnboundLocalVariable
if data_mtk is not None:
	f_ota.write(data_mtk)

# write 0
zero_format = str(tail_zero_len)+'s'
f_ota.write(struct.pack(zero_format,b''))    # tail zeros

# calc check byte
f_ota.seek(0,0)
data_ota = f_ota.read()
i = 0
num = int(len(data_ota)/4)
for i in range(num):
	ck_byte[0] = ck_byte[0] ^ data_ota[4*i]
	ck_byte[1] = ck_byte[1] ^ data_ota[4*i+1]
	ck_byte[2] = ck_byte[2] ^ data_ota[4*i+2]
	ck_byte[3] = ck_byte[3] ^ data_ota[4*i+3]

# write check byte
f_ota.seek(0,0)
f_ota.write(struct.pack('B', ck_byte[0]))  # check byte 4 bytes
f_ota.write(struct.pack('B', ck_byte[1]))
f_ota.write(struct.pack('B', ck_byte[2]))
f_ota.write(struct.pack('B', ck_byte[3]))

# close file
f_ota.close()

if data_mcu is not None and data_mtk is not None:
	input('Finish: mcu+mtk->ota')
elif data_mcu is not None:
	input('Finish: mcu->ota')
elif data_mtk is not None:
	input('Finish: mtk->ota')
else:
	input('No source file found')