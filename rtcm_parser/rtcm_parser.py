#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pprint
import rtcm_crc24

def parser(data):
	result = []
	idx_end = 0
	while (1):
		idx_start = data.tell()
		# data_peek = data.peek() # DO NOT use peek. The number of bytes returned may be less or more than requested.
		ch = data.read(1)
		# ch = data_peek[:1]
		if (ch == b'\xd3'):  # find d3
			len_str = data.read(2)
			# len_str = data_peek[1:3]
			len = int.from_bytes(len_str, byteorder='big')
			content = data.read(len)
			# content = data_peek[3:3+len]
			messageId = int.from_bytes(content[0:2], byteorder='big') >> 4
			crc = data.read(3)
			# crc = data_peek[3+len:6+len]
			crc_read = int.from_bytes(crc, byteorder='big')
			crc_src = ch + len_str + content
			crc_calc = rtcm_crc24.crc24(crc_src, crc_src.__len__())
			if (crc_read == crc_calc):  # crc pass
				if(idx_start != idx_end): # record invalid data
					res = [idx_end, idx_start, -1]
					result.append(res)
					print(res)
				# data.read(6+len) # real read after peek
				idx_end = data.tell()
				res = [idx_start, idx_end, messageId]
				result.append(res)
				print(res)
			else: # crc fail
				# data.read(1) # real read after peek
				data.seek(idx_start+1)
				continue
		elif(ch == b''):# end of file
			data.read(1)
			idx_start = data.tell()
			res = [idx_end, idx_start, -2]
			result.append(res)
			print(res)
			break
		else:
			# data.read(1) # real read after peek
			continue
	return result


if __name__ == '__main__':
	# stream = open('test_data-.txt', 'rb')
	filename = input('文件名:')
	stream = open(filename, 'rb')
	result = parser(stream)
	# save result to file
	try:
		with open('result_'+filename,'a+') as file:
			# print('opened')
			file.write(pprint.pformat(result))
	except IOError:
		print('file error')
	# pprint.pprint(result)
	input('处理完毕')