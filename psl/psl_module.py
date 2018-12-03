#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

# 全局变量
file = ''
log = []

MY_OUT_FILE = False
LOG_FILE = 'psl.log'


# 自定义打印函数
def my_print(*objects, sep=' ', end='\n', flush=False):
	# global MY_OUT_FILE # No need for global declaration to read
	if not MY_OUT_FILE:
		print(*objects, sep=sep, end=end, flush=flush)
	else:
		try:
			f = open(LOG_FILE, 'x', encoding='utf-8')
		except FileExistsError:
			f = open(LOG_FILE, 'a', encoding='utf-8')
		print(*objects, sep=sep, end=end, file=f, flush=flush)
		f.close()


# 程序开始的地方：读取log文件
def open_file():
	import sys
	global file, log
	file = input('待解析文件地址：')
	try:
		with open(file, 'r', encoding='utf-8', errors='ignore') as f:
			for line in f.readlines():
				log.append(line)
		return log
	except Exception as e:
		input('读取文件失败,' + str(e))
		sys.exit(0)


def string_has_time(string):
	ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	res = re.match(ptn, string)
	if res:
		return True
	else:
		return False


# 在原文件名的基础上加上一个后缀string作为新文件名
def new_file_name(string, f_format=None):
	global file
	log_file_names = file.split('.')
	log_file_names[-2] += ('_' + string)  # 加后缀
	if f_format:
		log_file_names[-1] = f_format
	new_name = '.'.join(log_file_names)
	return new_name


def save_to_csv(file, result, title=None):
	import csv
	if len(result) == 0:
		return
	try:
		# NOTICE:
		# the csv file will by default be decoded into unicode
		# using the system default encoding, don't open with encoding='utf-8'
		f = open(file, 'x', newline='')
		if title:
			spam_writer = csv.writer(f)
			spam_writer.writerow(title)
	except FileExistsError:
		f = open(file, 'a', newline='')
	except Exception as e:
		my_print(e)
	finally:
		spam_writer = csv.writer(f)
		for line in result:
			spam_writer.writerow(line)
		f.close()
		print("\n结果保存到文件：" + file)


# v2: 从line_from到line_to找出内容包含string_list内任一内容的行，结果保存到csv文件，返回搜索结果list
def OR(string_list, line_from=0, line_to=0, pt=False, save=True):
	search_res = []
	if line_from == 0:
		start = 0
	else:
		start = line_from

	if line_to == 0:
		stop = len(log)
	else:
		stop = line_to

	for line_index in range(start, stop):
		for string in string_list:
			if string in log[line_index]:
				search_res.append(line_index)
				if pt:
					my_print(line_index, log[line_index].strip())
				break

	my_print(string_list, ': ', str(len(search_res)))

	if save:
		csv_file_name = new_file_name('+'.join(string_list), 'csv')
		result = [[str(i), log[i].strip()] for i in search_res]
		save_to_csv(csv_file_name, result)

	return search_res  # list


# 从line_from到line_to找出内容包含string_list内任一内容的行，以及前面最近的时间，输出到csv文件，返回搜索结果list
def ORt(string_list, line_from=0, line_to=0, save=True):
	search_res = OR(string_list, line_from, line_to, save=False)
	time_res = []

	for line_index_end in search_res:
		for line_index in reversed(range(0, line_index_end)):
			string = log[line_index]
			if string_has_time(string):
				time_res.append(line_index)
				break

	time_res = list(set(time_res))  # remove redundant
	res = search_res + time_res
	res.sort()

	my_print(res, ': ', str(len(res)))

	if save:
		csv_file_name = new_file_name('+'.join(string_list) + '_t', 'csv')
		result = [[str(i), log[i].strip()] for i in res]
		save_to_csv(csv_file_name, result)

	return res, search_res, time_res  # list


