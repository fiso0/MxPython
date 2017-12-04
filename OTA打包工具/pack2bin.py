#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
将升级文件放入本目录下并重命名为"bin1"和"bin2"
双击pack2bin.py运行
程序将自动查找同目录下的文件"bin1"和"bin2"
bin1放在0x0000开始
bin2放在0x4000开始
出现Finish表示运行完毕
打包结果为"res"文件
'''

import os
import struct

# file names
file_bin1 = 'bin1'
file_bin2 = 'bin2'
file_res = 'res'

# get data
data_bin1 = None
try:
	with open(file_bin1,'rb') as f_bin1:
		data_bin1 = f_bin1.read()
except Exception as e:
	print(e)

data_bin2 = None
try:
	with open (file_bin2, 'rb') as f_bin2:
		data_bin2 = f_bin2.read()
except Exception as e:
	print(e)

# create file
try:
	f_res = open(file_res, 'xb')
except FileExistsError:
	f_res = open(file_res, 'wb')
except Exception as e:
	print(e)

# write data
if data_bin1 is not None:
	f_res.write(data_bin1)

# write 0
# f_res.write(struct.pack('174s',b''))    # 174*0

f_res.seek(0x4000)

# write data
if data_bin2 is not None:
	f_res.write(data_bin2)

# close file
f_res.close()
input('Finish: bin1+bin2->res')
