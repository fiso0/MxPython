#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re


def open_file(file):
	with open(file, 'br') as f:
		log = f.read()
	return log  # string list


# 写入csv文件（追加）
RESULT_FILE_CSV = 'decode_result.csv'
def save_basic_result_to_csv(res):
	import csv
	basic_result_file = RESULT_FILE_CSV
	try:
		f = open(basic_result_file, 'x', newline='')
		res_list = ['序号', '类型', '长度', '内容', '时间']
		spam_writer = csv.writer(f)
		spam_writer.writerow(res_list)
	except FileExistsError:
		f = open(basic_result_file, 'a', newline='')
	finally:
		spam_writer = csv.writer(f)
		for item in res:
			spam_writer.writerow(item)
		f.close()


def basic_parse():
	file = input('待解析posi_bk.txt文件地址：')
	try:
		log = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	# 解析得到wr_t和rd_t
	wr_t = (log[0] << 24) + (log[1] << 16) + (log[2] << 8) + (log[3] << 0)
	rd_t = (log[4] << 24) + (log[5] << 16) + (log[6] << 8) + (log[7] << 0)
	print('wr_t=' + str(wr_t) + ', rd_t=' + str(rd_t))

	i = 0 # 数据条数
	idx = 16 # 待解析数据位置
	msg_type = [] # 数据类型
	msg_len = [] # 数据长度（净长）
	msg_data = [] # 数据内容
	msg_datetime = [] # datetime字段内容
	while idx < 16+wr_t: # 文件总长为16+wr_t
		try:
			type = log[idx] >> 4 # 数据类型
			msg_type.append(type)
			len = ((log[idx] & 0xF) << 8) + log[idx + 1] # 数据长度（净长）
			msg_len.append(len)
			data = log[idx + 2:idx + 2 + len].decode(encoding='utf-8', errors='ignore') # 数据内容
			msg_data.append(data)
			datetime = re.search(r'"datetime":"([\d -:]*)"', data).group(1) # datetime字段内容
			msg_datetime.append(datetime)
			i += 1 # 数据条数
			idx += 2 + len # 下一条数据起始位置（头）
		except Exception as e:
			print(e)
			break

	num = list(range(1,i+1)) # 序号
	result = list(zip(num,msg_type,msg_len,msg_data,msg_datetime)) # 所有结果
	save_basic_result_to_csv(result) # 写入csv文件
	print(result)

	# 粗暴查找所有datetime
	# log1 = log.decode(encoding='utf-8', errors='ignore')
	# datetime = re.findall(r'"datetime":"([\d -:]*)"', log1)
	# print(datetime)


basic_parse()
input('done')