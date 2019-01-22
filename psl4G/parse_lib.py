#!/usr/bin/python3
# -*- coding: utf-8 -*-

my_help = '''
功能说明：
	BASIC() -- 读取log文件并进行基础解析（请首先执行这个）

	OR(['GGA','GST'],1301,1362)
	-- 查询在1301和1362行之间包含'GGA'或'GST'的行号（可加pt），保存到.csv文件，返回所有结果的行号

	ORt(['GGA','GST'])
	-- 查询包含'GGA'或'GST'的行号，及对应时间，保存到.csv文件，返回所有结果的行号

	AND(['GGA','E,1'],1301,1362)
	-- 查询在1301和1362行之间包含'GGA'和'E,1'的行号（可加pt），保存到.csv文件，返回所有结果的行号

	ANDt(['GGA','E,1'])
	-- 查询包含'GGA'和',E,1,'的行号，及对应时间，保存到.csv文件，返回所有结果的行号

	GGA()
	-- 保存所有GGA语句

	GGAv()
	-- 保存所有有效的GGA语句

	RMC()
	-- 保存所有RMC语句

	RMCv()
	-- 保存所有有效的RMC语句

	STEP()
	-- 查询所有[4005]步数数据

	pt()
	pt_log()
	-- 显示log内容
'''

import re

MY_OUT_FILE = False
LOG_FILE = 'psl.log'
RESULT_FILE_CSV = 'psl_basic_result.csv'

# 一些枚举类型
from enum import Enum, unique


@unique
class LOG_LEVEL(Enum):  # log级别
	NONE = 0
	ASSERT = 1
	ERROR = 2
	WARN = 3
	INFO = 4
	DEBUG = 5


@unique
class LOG_GNSS_TYPE(Enum):  # must be in sequence!
	START = 0
	GPS_TYPE = 1
	TIME = 2
	STOP = 3
	RES = 4


@unique
class GPS_TYPE(Enum):
	COLD = 0
	WARM = 1


@unique
class START_TYPE(Enum):
	ACTIVE = 0
	PERIOD = 1


@unique
class STOP_TYPE(Enum):
	PHASE_1 = 0
	PHASE_ALL = 1
	HOLD = 2
	PHASE_2 = 3
	POS = 4


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


# 设置打印到文件
def pt2file(a=False):
	global MY_OUT_FILE
	MY_OUT_FILE = a
	my_print('\n\n')
	my_print("====================================================")
	my_print("  " + file)
	my_print("====================================================")


def open_file(file):
	global log
	log = []
	with open(file, 'r', encoding='utf-8', errors='ignore') as f:
		for line in f.readlines():
			log.append(line)
	return log  # string list


def string_has_time(string):
	ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	res = re.match(ptn, string)
	if res:
		return True
	else:
		return False


# v1: 从line_from到line_to找出内容包含string的行，返回行号
def search(string, line_from=0, line_to=0, pt=False):
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
		if string in log[line_index]:
			# search_res.append((line_index,log[line_index]))
			search_res.append(line_index)
			if pt:
				my_print(line_index, log[line_index].strip())

	my_print(string, ': ', str(len(search_res)))
	return search_res  # list


# v3：从line_from到line_to找出内容包含string_list内所有内容的行，返回搜索结果list
def AND(string_list, line_from=0, line_to=0, pt=False, save=True, line=True):
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
				continue
			else:
				break
		else:
			search_res.append(line_index)
			if pt:
				my_print(line_index, log[line_index].strip())

	my_print(string_list, ': ', str(len(search_res)))

	if save:
		csv_file_name = new_file_name('='.join(string_list), 'csv')
		if line:
			result = [[str(i), log[i].strip()] for i in search_res]
		else:
			result = [[log[i].strip()] for i in search_res]
		save_to_csv(csv_file_name, result)

	return search_res  # list


def ANDt(string_list, line_from=0, line_to=0, save=True):
	search_res = AND(string_list, line_from, line_to, save=False)
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
		csv_file_name = new_file_name('='.join(string_list) + '_t', 'csv')
		result = [[str(i), log[i].strip()] for i in res]
		save_to_csv(csv_file_name, result)
	# for i in res:
	# 	save_to_csv(csv_file_name, [str(i),log[i].strip()])
	# print("结果保存到文件："+csv_file_name)

	return res  # list


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
				# search_res.append((line_index,log[line_index]))
				search_res.append(line_index)
				if pt:
					my_print(line_index, log[line_index].strip())
				break

	my_print(string_list, ': ', str(len(search_res)))

	if save:
		csv_file_name = new_file_name('+'.join(string_list), 'csv')
		result = [[str(i), log[i].strip()] for i in search_res]
		save_to_csv(csv_file_name, result)
	# for i in search_res:
	# 	save_to_csv(csv_file_name, [str(i),log[i].strip()])
	# print("结果保存到文件："+csv_file_name)

	return search_res  # list


# 从line_from到line_to找出内容包含string_list内任一内容的行，以及前面最近的时间，输出到csv文件，返回搜索结果list
def ORt(string_list, line_from=0, line_to=0, save=True):
	search_res = OR(string_list, line_from, line_to, save=False)
	time_res = []

	# if line_from == 0:
	# 	start = 0
	# else:
	# 	start = line_from
	#
	# if line_to == 0:
	# 	stop = len(log)
	# else:
	# 	stop = line_to
	#
	# for line_index in range(start, stop):
	# 	for string in string_list:
	# 		if string in log[line_index]:
	# 			search_res.append(line_index)
	# 			break

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
	# for i in res:
	# 	save_to_csv(csv_file_name, [str(i),log[i].strip()])
	# print("结果保存到文件："+csv_file_name)

	return res  # list


def GGA(line=False):
	gga = search('GGA')
	csv_file_name = new_file_name('GGA', 'csv')
	if line is True:
		result = [[str(i), log[i].strip()] for i in gga]
	else:
		result = [[log[i].strip()] for i in gga]
	save_to_csv(csv_file_name, result)


def GGAv(line=False):
	AND(['GGA', 'E,1'], line=line)


def RMC(line=False):
	rmc = search('RMC')
	csv_file_name = new_file_name('RMC', 'csv')
	if line is True:
		result = [[str(i), log[i].strip()] for i in rmc]
	else:
		result = [[log[i].strip()] for i in rmc]
	save_to_csv(csv_file_name, result)


def RMCv(line=False):
	AND(['RMC', 'A'], line=line)


# v3：默认找出line_list（从小到大排列）中最接近（小于）line_goal的一个
# big为True时，找出line_list（从小到大排列）中最接近（大于）line_goal的一个
def find_nearest(line_list, line_goal, big=False):
	res = 0
	if len(line_list) == 0:
		my_print('error: line_list empty')
		return None
	if big:
		for line_no in line_list:
			if line_no > line_goal:
				return line_no
	else:
		for line_no in line_list:
			if line_no < line_goal:
				res = line_no
		return res


# # v1:自动寻找最近的start，然后计算中间GGA的个数，打印输出结果，返回所有结果的列表
# def calc_time(stop_list, string='GGA'):
# 	GGA_cnt = []
#
# 	for stop_line in stop_list:
# 		start_line = find_nearest(start, stop_line)
# 		my_print('\tbetween line %d and %d, ' % (start_line, stop_line), end='')
# 		if string != 'GGA':
# 			cnt = len(AND([string, 'GGA'], start_line, stop_line, save=False))
# 		else:
# 			cnt = len(search(string, start_line, stop_line))
# 		GGA_cnt.append(cnt)
# 	return GGA_cnt


# v2:应该是找stop（E1）前一个stop(E0)之后的第一个start（S1），计算S1-E1之间的GGA的个数
# (E0) - S1 - S - S - E1
# 注：无法识别log有缺失的情况
# def calc_time(stop_list,string='GGA'):
# GGA_cnt = []

# stop_line = stop_list[0]
# if stop_line == stop[0]:
# start_line = 0
# else:
# start_line = find_nearest(start,stop_line)
# myprint('\tbetween line %d and %d, '%(start_line, stop_line),end='')
# cnt = len(search(string,start_line,stop_line))
# GGA_cnt.append(cnt)

# for i in range(1,len(stop_list)):
# stop_line = stop_list[i]
# start_line = find_nearest(start,stop_list[i-1])
# myprint('\tbetween line %d and %d, '%(start_line, stop_line),end='')
# cnt = len(search(string,start_line,stop_line))
# GGA_cnt.append(cnt)
# return GGA_cnt

# 统计从start_str到stop_str之间出现的goal_str的个数
# 默认统计范围：对每一个stop，从它前面最靠近的一个start开始
# max为True情况的统计范围：对每一个stop，从前一个stop之后的第一个start开始
# 如果stop前面没有start，则以0作为start
# 可以直接输入start/stop列表
# def calc(start_str_or_list, stop_str_or_list, goal_str, if_max=False):
# 	goal_cnt = []
#
# 	if type(start_str_or_list) == list:
# 		start_list = start_str_or_list
# 	else:
# 		start_list = search(start_str_or_list)
#
# 	if type(stop_str_or_list) == list:
# 		stop_list = stop_str_or_list
# 	else:
# 		stop_list = search(stop_str_or_list)
#
# 	for i in range(len(stop_list)):
# 		stop_line = stop_list[i]
# 		if if_max:
# 			if i == 0:
# 				start_line = 0
# 			else:
# 				prev_stop = stop_list[i - 1]
# 				start_line = find_nearest(start_list, prev_stop, big=True)
# 				if start_line > stop_line:
# 					start_line = find_nearest(start_list, stop_line)
# 		else:
# 			start_line = find_nearest(start_list, stop_line)
# 		myprint('\tbetween line %d and %d, ' % (start_line, stop_line), end='')
# 		cnt = len(search(goal_str, start_line, stop_line))
# 		goal_cnt.append(cnt)
# 	return goal_cnt


# # 寻找imei，日期，时间
# def find_imei_date_time(year=None, month=None, day=None):
# 	if year == None:
# 		year_re = r'\d{4}'
# 	else:
# 		year_re = year
#
# 	if month == None:
# 		month_re = r'\d{2}'
# 	else:
# 		month_re = month
#
# 	if day == None:
# 		day_re = r'\d{2}'
# 	else:
# 		day_re = day
#
# 	ptn = r'^(\d{15}),(%s-%s-%s) (\d{2}:\d{2}:\d{2})$' % (year_re, month_re, day_re)
# 	imei, first_date, first_time, last_date, last_time = '', '', '', '', ''
# 	found = False
#
# 	# 找第一个
# 	for log_i in log:
# 		res = re.match(ptn, log_i)
# 		if res:
# 			imei = res.group(1)
# 			first_date = res.group(2)
# 			first_time = res.group(3)
# 			found = True
# 			break
#
# 	# 找最后一个
# 	for log_i in reversed(log):
# 		res = re.match(ptn, log_i)
# 		if res:
# 			last_date = res.group(2)
# 			last_time = res.group(3)
# 			found = True
# 			break
#
# 	if found:
# 		my_print('IMEI: ' + imei)
# 		my_print('First date & time: \t' + first_date + ' ' + first_time)
# 		my_print('Last date & time: \t' + last_date + ' ' + last_time)
# 	return found, imei, first_date, first_time, last_date, last_time


# # 寻找网络异常（gsm_nw_state_2）
# def find_network_error():
# 	full_service_set = set()
# 	res1 = search('gsm_nw_state_1')
# 	for res1_line in res1:
# 		full_service = re.findall(r'(?<=\[).+?(?= 3\])', log[res1_line])
# 		for item in full_service:
# 			full_service_set.add(item)
#
# 	part_service_set = set()
# 	res2 = search('gsm_nw_state_2')
# 	for res2_line in res2:
# 		part_service = re.findall(r'(?<=\[).+?(?= 2\])', log[res2_line])
# 		for item in part_service:
# 			part_service_set.add(item)
#
# 	network_dict = {}
# 	for part in part_service_set:
# 		network_dict[part] = '失效'
# 	for full in full_service_set:
# 		network_dict[full] = '恢复'
# 	network_dict_sorted = sorted(network_dict.items(), key=lambda d: d[0], reverse=False)
# 	for item in network_dict_sorted:
# 		print(item)
#
# 	if len(part_service_set) > 0:
# 		return True


# # 寻找漂移点
# def find_drift():
# 	res = search('[DRIFT 1]')
# 	if len(res) > 0:
# 		return True


# # 解析结束时间，排序输出
# def sort_time_finish():
# 	ptn = r'.*?(\d+)'
#
# 	time_finish_int = []
# 	for i in time_fin:
# 		res = re.match(ptn, log[i])
# 		if res:
# 			time_finish_int.append(int(res.group(1)))
#
# 	time_finish_int_sorted = sorted(time_finish_int)
# 	my_print(time_finish_int_sorted)
# 	return time_finish_int


# def plot_analyse():
# 	import matplotlib.pyplot as plt
# 	import numpy as np
# 	plt.figure()
#
# 	# x轴数据
# 	x = np.arange(len(time_fin_int))
# 	width = 0.8
# 	# 画bar图
# 	bars = plt.bar(x, time_fin_int, width=width)
# 	# 设置figure大小
# 	fig = plt.gcf()
# 	fig.set_size_inches(8, 6)
# 	# 调整图形边距
# 	plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.1)
# 	# 添加y轴刻度值（定位耗时）
# 	plt.yticks(range(0, 101, 10))
# 	# 显示y轴刻度线
# 	plt.grid(axis='y')
# 	# 添加x轴刻度值（行号）
# 	plt.xticks(x + width / 2, time_fin, rotation=90, size='x-small')
# 	# 在每个bar上方添加文字标识（定位耗时）
# 	for bar in bars:
# 		height = bar.get_height()
# 		plt.text(bar.get_x() + width / 2, height + 2, int(height), ha='center', va='bottom', size='xx-small',
# 		         rotation=90)
# 	# 显示
# 	plt.show(block=False)


# 换行打印列表
def pt(list_a):
	for i in list_a:
		my_print(i)


# 按行号打印log内容
def pt_log(list_a):
	for i in list_a:
		my_print(str(i) + ' ' + log[i].strip())


# 按行号保存log内容到新文件
def save_to(lines, file_name, line_no=False):
	# new_file = '\\'.join(file.split('\\')[0:-1]) + '\\' + file_name
	new_file = file_name
	try:
		with open(new_file, 'x', encoding='utf-8') as f:
			for i in lines:
				if line_no:
					f.write(str(i) + '\t' + log[i])
				else:
					f.write(log[i])
		my_print('保存成功：' + new_file)
	except FileExistsError:
		my_print('保存失败：文件已存在')


# 在原文件名的基础上加上一个后缀string作为新文件名
def new_file_name(string, format=None):
	log_file_names = file.split('.')
	log_file_names[-2] += ('_' + string)  # 加后缀
	if format:
		log_file_names[-1] = format
	new_name = '.'.join(log_file_names)
	return new_name


# 寻找string，保存到同名文件
# 例如：从D:\log\srv_logs\Y25\Y25_20160519.log寻找RMC，结果将保存到D:\log\srv_logs\Y25\Y25_20160519 RMC.log
def select_to(string, result=None, line_no=False):
	if result is None:
		result = search(string)
	file_name = new_file_name(string)
	save_to(result, file_name, line_no)


# 获取包含有效RMC速度的NMEA到同名文件
# todo：考虑按日期分开
# def get_speed():
# 	result = search_and(['RMC', ',A,'])
# 	select_to('valid RMC', result)


def save_to_csv(file, result, title=None):
	import csv
	if len(result) == 0:
		return
	try:
		# NOTICE: the csv file will by default be decoded into unicode using the system default encoding, don't open with encoding='utf-8'
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


# def save_basic_result_to_csv():
# 	title = ['文件名', '版本号（最后一条版本号记录）', 'IMEI', '开始时间', '结束时间', \
# 	         'start个数', 'drv_start个数', 'period个数', 'stop个数', 'stop_1个数', \
# 	         'stop_all个数', 'stop_hold个数', 'stop_2个数', 'stop_pos个数', \
# 	         'stop_ack个数', 'time_finish个数', 'AGPS开始个数', 'AGPS成功个数', \
# 	         'AGPS失败个数', '所有定位耗时']
# 	if len(fw) > 0:
# 		last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
# 	else:
# 		last_fw = 'None'
# 	first_dt = first_date + ' ' + first_time
# 	last_dt = last_date + ' ' + last_time
# 	result = [[file, last_fw, imei, first_dt, last_dt, str(len(start)), \
# 	           str(len(drv_start)), str(len(period)), str(len(stop)), \
# 	           str(len(stop_1)), str(len(stop_all)), str(len(stop_hold)), \
# 	           str(len(stop_2)), str(len(stop_pos)), str(len(stop_ack)), \
# 	           str(len(time_fin)), str(len(agps_start)), str(len(agps_ok)), \
# 	           str(len(agps_fail)), time_fin_int]]
# 	save_to_csv(RESULT_FILE_CSV, result, title)





def get_gps_type(line):
	gps_type = None
	if 'warm' in line:
		gps_type = GPS_TYPE.WARM
	elif 'cold' in line:
		gps_type = GPS_TYPE.COLD
	return gps_type


def get_stop_type(line):
	stop_type = None
	if 'phase 1 timeout' in line:
		stop_type = STOP_TYPE.PHASE_1
	elif 'phase all timeout' in line:
		stop_type = STOP_TYPE.PHASE_ALL
	elif 'hold timer timeout' in line:
		stop_type = STOP_TYPE.HOLD
	elif 'phase 2 end' in line:
		stop_type = STOP_TYPE.PHASE_2
	elif 'postion complete' in line:
		stop_type = STOP_TYPE.POS
	return stop_type


def get_time(line):
	ptn = r'.*?(\d+)'
	time = None
	res = re.match(ptn, line)
	if res:
		time = int(res.group(1))
	return time


def get_rtc(line):
	import re
	ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	res = re.match(ptn, line)
	if res:
		return res.group(2), res.group(3)
	else:
		return None, None


# def get_step(line):
# 	import re
# 	ptn = r'.*?\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} 0x(\w{2}) 0x(\w{2})'
# 	step_1 = re.match(ptn, line).group(1)  # 00
# 	step_2 = re.match(ptn, line).group(2)  # 15
# 	step_num = int(step_1 + step_2, 16)
# 	return step_num


# def STEP():
# 	pos4005 = search('[4005]')
# 	res = []
# 	for line_no in pos4005:
# 		date, time = get_rtc(log[line_no - 1])
# 		step = get_step(log[line_no])
# 		res.append((date, time, step))
# 		if step is not 0:
# 			print("Step: %s %s %d" % (date, time, step))
# 	print("Step: others are 0")
# 	return res

def get_log(lines_list):
	if isinstance(lines_list, list):
		return [log[line] for line in lines_list]
	elif isinstance(lines_list, int):
		return log[lines_list]
	else:
		my_print('输入参数有误！')
		return ''

def get_all_lines():
	return list(range(0, len(log)))


def get_line_number():
	return len(log)

def get_log_lines(log_type):
	"""
	获取所有指定log类型的log行号
	:param log_type: log类型（级别或模块或功能）
	:return: log行号列表
	"""
	if log_type in log_level_line_dicts.keys():
		return log_level_line_dicts.get(log_type)
	elif log_type in log_mod_line_dicts.keys():
		return log_mod_line_dicts.get(log_type)
	elif log_type in log_function_line_dicts.keys():
		return log_function_line_dicts.get(log_type)
	else:
		my_print('输入参数有误！')
		return []


def get_log_levels():
	return log_level_line_dicts


def get_log_mods():
	return log_mod_line_dicts


def get_log_funcs():
	return log_function_line_dicts


def parse_log_level(line_no):
	"""
	判断该行log属于哪种级别，同时按级别分别记录行号
	:param line_no: 行号
	:return: 无
	"""
	ptn = r'\|\S*\|(\S*)>'
	try:
		level_name = re.search(ptn, log[line_no]).group(1)
		line_list = log_level_line_dicts.get(level_name, [])
		line_list.append(line_no)
		log_level_line_dicts[level_name] = line_list
	except:
		pass
	return


def parse_log_mod(line_no):
	"""
	判断该行log所属的模块，同时按模块分别记录行号
	:param line_no: 行号
	:return: 无
	"""
	ptn = r'> (\S*)'
	try:
		mod_name = re.search(ptn, log[line_no]).group(1)  # try to find mod_name
		line_list = log_mod_line_dicts.get(mod_name, [])  # get line list
		line_list.append(line_no)  # update line lists
		log_mod_line_dicts[mod_name] = line_list  # set line list
	except:
		pass  # not find mod_name
	return


def parse_function_log(line_no, key_words, log_name):
	'''
	查找该行内是否包含关键词内容（任一即可），包含则将该行号记录到log_function_line_dicts[log_name]中
	:param line_no:行号
	:param key_words:关键词
	:param log_name:字典索引
	:return:无
	'''
	line_list = log_function_line_dicts.get(log_name, [])
	try:
		for key in key_words:
			if key in log[line_no]:
				line_list.append(line_no)
				log_function_line_dicts[log_name] = line_list
				return
	except:
		return


def parse_locate_log(line_no):
	'''
	判断是否定位相关log，如果是，则将该行号记录到log_function_line_dicts中
	:param line_no: 行号
	:return: 无
	'''
	import getConfig
	config = getConfig.get_config()
	for item in config:
		parse_function_log(line_no, config[item], item)

	# key_words = ['[GPS]']
	# log_name = '定位'
	# parse_function_log(line_no, key_words, log_name)


def parse_GNSS_type(line_no):
	'''
	判断该行log属于哪种LOG_GNSS_TYPE
	:param line_no: 行号
	:return: 该行log的类型、内容
	'''
	line = log[line_no]
	log_type = None
	log_data = None
	if ('mx_location_period_timer__cb' in line) and ('movement[1]' in line) and ('srv_num[0]' in line):
		log_type = LOG_GNSS_TYPE.START
		log_data = START_TYPE.PERIOD
	elif ('mx_location_request' in line) and ('movement[1]' in line) and ('srv_num[0]' in line):
		log_type = LOG_GNSS_TYPE.START
		log_data = START_TYPE.ACTIVE
	elif 'mx_gps_ctrl_drv_start' in line:
		log_type = LOG_GNSS_TYPE.GPS_TYPE
		log_data = get_gps_type(line)
	elif '[GPS]time_finish' in line:
		log_type = LOG_GNSS_TYPE.TIME
		log_data1 = get_time(line)
		log_data2 = get_rtc(log[line_no - 1])
		log_data = log_data1, log_data2
	elif '[GPSstop]' in line:
		log_type = LOG_GNSS_TYPE.STOP
		log_data = get_stop_type(line)
	elif 'best record' in line:
		log_type = LOG_GNSS_TYPE.RES
		log_data = True
	return log_type, log_data


def check_info_filled(locate_info, info_type_to_fill):
	check_type = info_type_to_fill
	while True:
		if check_type is LOG_GNSS_TYPE.RES:
			pass
		elif locate_info[check_type.name] is not None:
			return True
		if check_type.value < len(LOG_GNSS_TYPE) - 1:
			check_type = LOG_GNSS_TYPE(check_type.value + 1)
		else:
			break
	return False


# def plot_locate(locate_info_list):
# 	import matplotlib.pyplot as plt
# 	import numpy as np
# 	plt.figure()
#
# 	# x轴数据
# 	x = np.arange(len(locate_info_list))
# 	y = []
# 	tick = []
# 	for loc in locate_info_list:
# 		try:
# 			y.append(loc.get('TIME')[0])
# 		except:
# 			y.append(0)  # 数据若丢失，按0显示
# 		try:
# 			tick.append(loc.get('TIME')[1][1])
# 		except:
# 			tick.append('None')
#
# 	# 定位数据分组
# 	loc_cold_ok = []
# 	loc_cold_fail = []
# 	loc_warm_ok = []
# 	loc_warm_fail = []
# 	loc_unknown_ok = []
# 	loc_unknown_fail = []
# 	for i in x:
# 		loc = locate_info_list[i]
# 		if loc['GPS_TYPE'] == GPS_TYPE.COLD:
# 			# if (loc['RES'] is not None) and (loc['STOP'] is not STOP_TYPE.POS):
# 			if loc['RES'] is not True:
# 				# 定位结束时有[GPSstop]且不是[GPSstop]postion complete，表示定位失败
# 				loc_cold_fail.append(i)
# 			else:
# 				# 定位结束时没有[GPSstop]或有[GPSstop]postion complete，表示成功
# 				loc_cold_ok.append(i)
# 		elif loc['GPS_TYPE'] == GPS_TYPE.WARM:
# 			# if (loc['STOP'] is not None) and (loc['STOP'] is not STOP_TYPE.POS):
# 			if loc['RES'] is not True:
# 				loc_warm_fail.append(i)
# 			else:
# 				loc_warm_ok.append(i)
# 		else:
# 			# if (loc['STOP'] is not None) and (loc['STOP'] is not STOP_TYPE.POS):
# 			if loc['RES'] is not True:
# 				loc_unknown_fail.append(i)
# 			else:
# 				loc_unknown_ok.append(i)
#
# 	# 按组画bar图
# 	legend = []
# 	width = 0.8
# 	if len(loc_cold_fail) is not 0:
# 		bars_1 = plt.bar([x[i] for i in loc_cold_fail], [y[i] for i in loc_cold_fail], width=width, color='#74A6BD')
# 		legend.append('COLD, GPS Fail')
# 	else:
# 		bars_1 = ()
# 	if len(loc_cold_ok) is not 0:
# 		bars_2 = plt.bar([x[i] for i in loc_cold_ok], [y[i] for i in loc_cold_ok], width=width, color='#89D7ED')
# 		legend.append('COLD, GPS success')
# 	else:
# 		bars_2 = ()
# 	if len(loc_warm_fail) is not 0:
# 		bars_3 = plt.bar([x[i] for i in loc_warm_fail], [y[i] for i in loc_warm_fail], width=width, color='#B06A3B')
# 		legend.append('WARM, GPS Fail')
# 	else:
# 		bars_3 = ()
# 	if len(loc_warm_ok) is not 0:
# 		bars_4 = plt.bar([x[i] for i in loc_warm_ok], [y[i] for i in loc_warm_ok], width=width, color='#EB8540')
# 		legend.append('WARM, GPS success')
# 	else:
# 		bars_4 = ()
# 	if len(loc_unknown_fail) is not 0:
# 		bars_5 = plt.bar([x[i] for i in loc_unknown_fail], [y[i] for i in loc_unknown_fail], width=width,
# 		                 color='#606060')
# 		legend.append('UNKNOWN, GPS Fail')
# 	else:
# 		bars_5 = ()
# 	if len(loc_unknown_ok) is not 0:
# 		bars_6 = plt.bar([x[i] for i in loc_unknown_ok], [y[i] for i in loc_unknown_ok], width=width, color='#C0C0C0')
# 		legend.append('UNKNOWN, GPS success')
# 	else:
# 		bars_6 = ()
# 	bars = bars_1 + bars_2 + bars_3 + bars_4 + bars_5 + bars_6
#
# 	# 画legend
# 	plt.legend(legend)
# 	# 设置figure大小
# 	fig = plt.gcf()
# 	fig.set_size_inches(8, 6)
# 	# 调整图形边距
# 	plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.1)
# 	# 添加y轴刻度值
# 	plt.yticks(range(0, int((max(y) + 9) / 10 * 10) + 1, 10))
# 	# 显示y轴刻度线
# 	plt.grid(axis='y')
# 	# 添加x轴刻度值
# 	plt.xticks(x + width / 2, tick, rotation=90, size='x-small')
# 	# 在每个bar上方添加文字标识
# 	for bar in bars:
# 		height = bar.get_height()
# 		plt.text(bar.get_x() + width / 2, height + 2, '?' if height == 0 else int(height), ha='center', va='bottom',
# 		         size='xx-small', rotation=90)
# 	# 显示
# 	plt.show(block=False)


# def get_mac(line_no):
# 	import re
# 	# line = log[line_no]
# 	ptn = r'AT[+]SCAN=0x([0-9a-zA-Z]{12})-([0-9a-zA-Z]{1,2})'
# 	res = re.findall(ptn, log[line_no])  # 结果为列表
# 	date, time = get_rtc(log[line_no - 1])
# 	if len(res):
# 		# 返回列表，每一项为(行号，日期，时间，MAC，RSSI)
# 		return [(line_no, date, time, a[0], a[1]) for a in res]
# 	else:
# 		# 该行内容中未查找到蓝牙数据
# 		return None


def BASIC(inFile=None, hint=True):
	'''
	基础解析
	:param inFile:
	:return:
	'''
	global file, log
	# global fw, stop, stop_1, stop_all, stop_hold, drv_start, period, start, locate, stop_2, stop_pos, stop_ack, time_fin, agps_start, agps_ok, agps_fail, time_fin_int, locate_info_list, imei, first_date, first_time, last_date, last_time

	global log_level_line_dicts  # 按log级别分类保存行号
	log_level_line_dicts = dict()

	global log_mod_line_dicts  # 按log模块分类保存行号
	log_mod_line_dicts = dict()

	global log_function_line_dicts  # 按log功能分类保存行号
	log_function_line_dicts = dict()

	if (inFile == None):
		file = input('待解析文件地址：')
	else:
		file = inFile

	try:
		log = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	# 遍历所有log
	for line_no in range(0, len(log)):
		line = log[line_no]  # log内容

		try:
			# log级别
			parse_log_level(line_no)

			# log模块
			parse_log_mod(line_no)

			# 其他功能
			parse_locate_log(line_no)

		except Exception as e:
			print(e)

	# 输出结果
	print_log = ''
	print_log += ('各级别log统计结果：\n')
	for level_name in log_level_line_dicts.keys():
		print_log += (level_name + ': ' + str(len(log_level_line_dicts.get(level_name, []))) + '\n')
	print_log += '\n'
	print_log += ('各模块log统计结果：\n')
	for mod_name in log_mod_line_dicts.keys():
		print_log += (mod_name + ': ' + str(len(log_mod_line_dicts.get(mod_name, []))) + '\n')

	my_print(print_log)

	# # 寻找imei，日期，时间
	# my_print('\n')
	# found, imei, first_date, first_time, last_date, last_time = find_imei_date_time()

	# # 版本号
	# my_print('\n')
	# my_print('__fw__')
	# fw = search('FW')
	# if len(fw) > 0:
	# 	first_fw = log[fw[0]][log[fw[0]].index('bb'):-1].strip()
	# 	my_print(first_fw)
	# 	last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
	# 	if first_fw != last_fw:
	# 		my_print(last_fw)

	# mac_list = [] # 所有MAC的结果，格式为[(行号，日期，时间，MAC，RSSI)]
	# all_mac = set() # 所有出现的MAC，格式为{MAC}
	# for line_no in range(0, len(log)):
	# 	if '[BT]rx' in log[line_no]:
	# 		mac_res = get_mac(line_no)
	# 		if mac_res:
	# 			# 扩展合并为一个大的列表
	# 			mac_list.extend(mac_res)
	# 			# 记录所有出现的MAC
	# 			all_mac.update([a[3] for a in mac_res])

	# # 按MAC分为几个列表
	# all_mac = list(all_mac)
	# MAC_N = len(all_mac)
	# mac_list_group = []
	# for n in range(MAC_N):
	# 	mac_list_group.append([])
	# 	mac = all_mac[n]
	# 	for res in mac_list:
	# 		if mac == res[3]:
	# 			mac_list_group[n].append(res)

	# # 准备画散点图（x-时间，y-RSSI，labels-MAC）
	# import matplotlib.pyplot as plt
	# plt.figure()
	# for n in range(MAC_N):
	# 	mac_list = mac_list_group[n]
	#
	# 	# 散点图x坐标
	# 	datetime_list = [a[1]+' '+a[2] for a in mac_list]
	# 	import time
	# 	timestamp_list = [int(time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S"))) for a in datetime_list]
	# 	timestamp_base = timestamp_list[0]
	# 	x = timestamp_shift_list = [a-timestamp_base for a in timestamp_list]
	#
	# 	# 散点图y坐标
	# 	y = signal_list = [-int(a[4],16) for a in mac_list]
	#
	# 	# 画散点图
	# 	plt.scatter(x, y, alpha=0.5)
	# 	plt.plot(x, y, lw=1, label=all_mac[n]+'('+str(len(mac_list_group[n]))+')')
	# 	plt.legend()
	#
	# plt.show()
	#
	# input()

	# # 定位log组，所有定位的信息字典存入一个列表
	# locate_info_list = []
	# # 每次定位保存一个信息字典，包含：开始类型，耗时，结果
	# # 默认每项为空，顺序解析log，得到一个信息则填入字典
	# # 如果该字典后面某项已填，则存入列表，开始填新的字典
	# locate_info = {'START':None,'GPS_TYPE':None,'TIME':None,'STOP':None,'RES':None}
	# for line_no in range(0,len(log)):
	# 	line = log[line_no]
	# 	# 每行log的属性：行号no，内容line，信息类型type（开始主动定位，开始周期定位，定位耗时信息，定位结束类型，其他）
	# 	log_info = {'no':line_no,'line':line,'type':None}
	# 	log_type,log_data = parse_GNSS_type(line_no)
	# 	if log_type is None:
	# 		continue
	#
	# 	log_info['type'] = log_type
	# 	if log_type is LOG_TYPE.RES: # 该项可重复填入，有则设为True，表示定位成功
	# 		pass
	# 	else: # 其他项在每次定位过程中都只会出现一次，不能重复填入
	# 		if_new = check_info_filled(locate_info, log_info['type'])
	# 		if if_new:
	# 			# 存到列表
	# 			locate_info_list.append(locate_info)
	# 			# 初始化locate_info
	# 			locate_info = {'START':None,'GPS_TYPE':None,'TIME':None,'STOP':None,'RES':None}
	# 	locate_info[log_type.name] = log_data
	#
	# print('\n共%d次定位'%(len(locate_info_list)))
	# if_draw = input('\n是否画图？(y/n)')
	# if if_draw == 'y' or if_draw == 'Y':
	# 	print('\n开始画图...')
	# 	# 图形输出
	# 	plot_locate(locate_info_list)
	# 	print('\n画图完毕')
	#
	# # 定位开始
	# my_print('\n')
	# my_print('__drv_start__', end='')
	# drv_start = search('mx_gps_ctrl_drv_start')
	# my_print('__period__', end='')
	# period = search('mx_location_period_timer__cb')
	#
	# start = drv_start + period
	# start.sort()
	# my_print('__start__ = drv_start + period')
	#
	# # 定位结束
	# my_print('__stop__', end='')
	# stop = search('[GPSstop]')
	#
	# # 定位起止
	# locate = start + stop
	# locate.sort()
	#
	# ## 固定时间
	# my_print('\n')
	# my_print('[30s]__stop_1__', end='')
	# stop_1 = search('[GPSstop]phase 1 timeout')
	#
	# my_print('[5min]__stop_all__', end='')
	# stop_all = search('[GPSstop]phase all timeout')
	#
	# my_print('[2min]__stop_hold__', end='')
	# stop_hold = search('[GPSstop]hold timer timeout')
	#
	# ## 变化时间
	# my_print('\n')
	# my_print('__stop_2__', end='')
	# stop_2 = search('[GPSstop]phase 2 end')
	# if len(stop_2) > 0 and len(stop_2) < 30:
	# 	my_print('calculate GGA before [GPSstop]phase 2 end (calc_time(stop_2)):')
	# 	calc_time(stop_2)
	# 	my_print("calculate valid GGA before [GPSstop]phase 2 end (calc_time(stop_2,',E,1,')):")
	# 	calc_time(stop_2, ',E,1,')
	# elif len(stop_2) > 29:
	# 	my_print("\ttoo much, call -> calc_time(stop_2,',E,1,')")
	#
	# my_print('\n')
	# my_print('__stop_pos__', end='')
	# stop_pos = search('[GPSstop]postion complete')
	# if len(stop_pos) > 0 and len(stop_pos) < 30:
	# 	my_print('calculate GGA before [GPSstop]postion complete (calc_time(stop_pos)):')
	# 	calc_time(stop_pos)
	# 	my_print("calculate valid GGA before [GPSstop]postion complete: (calc_time(stop_pos,',E,1,'))")
	# 	calc_time(stop_pos, ',E,1,')
	# elif len(stop_pos) > 29:
	# 	my_print("\ttoo much, call -> calc_time(stop_pos,',E,1,')")
	#
	# my_print('\n')
	# my_print('__stop_ack__', end='')
	# stop_ack = search('[GPSstop]ACKOK all done')
	# if len(stop_ack) > 0 and len(stop_ack) < 30:
	# 	my_print('calculate GGA before [GPSstop]ACKOK all done (calc_time(stop_ack)):')
	# 	calc_time(stop_ack)
	# 	my_print("calculate valid GGA before [GPSstop]ACKOK all done (calc_time(stop_ack,',E,1,')):")
	# 	calc_time(stop_ack, ',E,1,')
	# elif len(stop_ack) > 29:
	# 	my_print("\ttoo much, call -> calc_time(stop_ack,',E,1,')")
	#
	# # 结束时间
	# my_print('\n')
	# my_print('__time_fin__')
	# time_fin = search('[GPS]time_finish')
	# time_fin_int = sort_time_finish()
	#
	# # AGPS
	# my_print('\n')
	# my_print('__agps_start__', end='')
	# agps_start = search('[AGPS]mx_agps_request_start')
	#
	# my_print('\n')
	# my_print('__agps_ok__', end='')
	# agps_ok = search('[AGPS]ACKOK all done')
	#
	# my_print('\n')
	# my_print('__agps_fail__', end='')
	# agps_fail = search('[AGPS]mx_agps_request_stop')
	#
	# # 保存结果
	# save_basic_result_to_csv()
	#
	# # 图形输出
	# # plot_analyse()

	if (hint):
		input('\n基础分析到此完毕\n')

	return print_log


# 基础异常检测
def ADVANCED():
	# # 检查是否有2015-04-**日期异常
	# found, imei, first_date_err, first_time_err, last_date_err, last_time_err = find_imei_date_time('2015', '04')
	# if found:
	# 	my_print('注意！存在终端日期异常')
	# else:
	# 	my_print('不存在终端日期异常')
	#
	# # 检查是否有网络异常（gsm_nw_state_2）
	# if find_network_error():
	# 	my_print('注意！存在网络异常')
	# else:
	# 	my_print('不存在网络异常')
	#
	# # 检查是否有漂移点（[DRIFT 1]）
	# if find_drift():
	# 	my_print('注意！存在漂移点')
	# else:
	# 	my_print('不存在漂移点')
	#
	# # TODO：检查是否有GPS日期错误


	input('\n基础异常检测到此完毕\n')


# 无限读取用户命令并执行
def cmd_parse():
	while True:
		cmd = input('\ncmd:')
		if '(' not in cmd:
			cmd += '()'
		try:
			exec(cmd)
		except Exception as e:
			my_print(e)


if __name__ == '__main__':
	try:
		BASIC()
	except Exception as e:
		my_print(e)

	# try:
	# 	ADVANCED()
	# except Exception as e:
	# 	my_print(e)

	my_print(my_help)
	cmd_parse()
