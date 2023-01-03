#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

'''
合并多个bin文件到一个bin文件
合并结果文件：MERGE_FILE_NAME
	默认为merge.bin
待合并文件个数：BIN_FILE_NUMBER
	默认为3
待合并文件名：BIN_FILE_NAMES
	at32f403a_boot.bin
	gap_0x8008000.bin
	mxt22a03.bin
待合并文件地址：ADDRESS
	0x08000000
	0x08008000
	0x08008200
'''

MERGE_FILE_NAME = "merge.bin"

BIN_FILE_NUMBER = 3 # bin文件个数为3
BIN_FILE_NAMES = []
BIN_FILE_NAMES.append("at32f403a_boot.bin") # bin文件名1
BIN_FILE_NAMES.append("gap_0x8008000.bin") # bin文件名2
BIN_FILE_NAMES.append("mxt22a03.bin") # bin文件名3

ADDRESS = []
ADDRESS.append(0x08000000) # bin文件1地址
ADDRESS.append(0x08008000) # bin文件2地址
ADDRESS.append(0x08008200) # bin文件3地址

###############################################################
import struct

# open files
bin_files = []
bin_sizes = []
for file_name in BIN_FILE_NAMES:
	try:
		with open(file_name,'rb') as file:
			data = file.read()
			bin_files.append(data)
			bin_sizes.append(len(data))
			file.close()
			print("file read: " + file_name)
	except FileNotFoundError:
		print("No file: " + file_name)
	except Exception as e:
		print(e)

# calc gaps
gaps = []
gaps.append(0)
i = 1
while i < BIN_FILE_NUMBER:
	gap = ADDRESS[i] - ADDRESS[i-1] - bin_sizes[i-1]
	if gap < 0:
		print("file %s too big!!!" % BIN_FILE_NAMES[i-1])
		exit(0)
	else:
		gaps.append(gap)
		i += 1

# create/overwrite file
try:
	f_merge = open(MERGE_FILE_NAME, 'xb+')
	print("merge file create done...")
except FileExistsError:
	f_merge = open(MERGE_FILE_NAME, 'wb+')
	print("merge file already exist, overwrite...")
except Exception as e:
	print(e)

# write file data
for file_name, file_data, gap in zip(BIN_FILE_NAMES,bin_files,gaps):
	# f_merge.seek(offset)
	for i in range(gap):
		f_merge.write(struct.pack('B', 0xff))
	f_merge.write(file_data)
	print("file data write: " + file_name)

# close file
f_merge.close()
print("merge file close done...")
