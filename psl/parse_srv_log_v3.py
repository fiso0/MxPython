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

	pt()
	pt_log()
	-- 显示log内容
'''

import re

MY_OUT_FILE = False
LOG_FILE = 'psl.log'
RESULT_FILE_CSV = 'psl_basic_result.csv'


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
		csv_file_name = new_file_name('='.join(string_list),'csv')
		if line:
			result = [[str(i),log[i].strip()] for i in search_res]
		else:
			result = [[log[i].strip()] for i in search_res]
		save_to_csv(csv_file_name, result)

	return search_res  # list


def ANDt(string_list, line_from=0, line_to=0, save=True):
	search_res = AND(string_list,line_from,line_to,save=False)
	time_res = []

	for line_index_end in search_res:
		for line_index in reversed(range(0,line_index_end)):
			string = log[line_index]
			if string_has_time(string):
				time_res.append(line_index)
				break

	time_res = list(set(time_res)) # remove redundant
	res = search_res + time_res
	res.sort()

	my_print(res, ': ', str(len(res)))

	if save:
		csv_file_name = new_file_name('='.join(string_list)+'_t','csv')
		result = [[str(i),log[i].strip()] for i in res]
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
		csv_file_name = new_file_name('+'.join(string_list),'csv')
		result = [[str(i),log[i].strip()] for i in search_res]
		save_to_csv(csv_file_name, result)
		# for i in search_res:
		# 	save_to_csv(csv_file_name, [str(i),log[i].strip()])
		# print("结果保存到文件："+csv_file_name)

	return search_res  # list


# 从line_from到line_to找出内容包含string_list内任一内容的行，以及前面最近的时间，输出到csv文件，返回搜索结果list
def ORt(string_list, line_from=0, line_to=0, save=True):
	search_res = OR(string_list,line_from,line_to,save=False)
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
		for line_index in reversed(range(0,line_index_end)):
			string = log[line_index]
			if string_has_time(string):
				time_res.append(line_index)
				break

	time_res = list(set(time_res)) # remove redundant
	res = search_res + time_res
	res.sort()
	
	my_print(res, ': ', str(len(res)))

	if save:
		csv_file_name = new_file_name('+'.join(string_list)+'_t','csv')
		result = [[str(i),log[i].strip()] for i in res]
		save_to_csv(csv_file_name, result)
		# for i in res:
		# 	save_to_csv(csv_file_name, [str(i),log[i].strip()])
		# print("结果保存到文件："+csv_file_name)

	return res  # list	


def GGA(line=False):
	gga = search('GGA')
	csv_file_name = new_file_name('GGA','csv')
	if line is True:
		result = [[str(i),log[i].strip()] for i in gga]
	else:
		result = [[log[i].strip()] for i in gga]
	save_to_csv(csv_file_name, result)

	
def GGAv(line=False):
	AND(['GGA','E,1'],line=line)


def RMC(line=False):
	rmc = search('RMC')
	csv_file_name = new_file_name('RMC','csv')
	if line is True:
		result = [[str(i),log[i].strip()] for i in rmc]
	else:
		result = [[log[i].strip()] for i in rmc]
	save_to_csv(csv_file_name, result)


def RMCv(line=False):
	AND(['RMC','A'],line=line)


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


# v1:自动寻找最近的start，然后计算中间GGA的个数，打印输出结果，返回所有结果的列表
def calc_time(stop_list, string='GGA'):
	GGA_cnt = []

	for stop_line in stop_list:
		start_line = find_nearest(start, stop_line)
		my_print('\tbetween line %d and %d, ' % (start_line, stop_line), end='')
		if string != 'GGA':
			cnt = len(AND([string, 'GGA'], start_line, stop_line, save=False))
		else:
			cnt = len(search(string, start_line, stop_line))
		GGA_cnt.append(cnt)
	return GGA_cnt


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


# 寻找imei，日期，时间
def find_imei_date_time():
	global imei, first_date, first_time, last_date, last_time

	ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	imei, first_date, first_time, last_date, last_time = '', '', '', '', ''

	# 找第一个
	for log_i in log:
		res = re.match(ptn, log_i)
		if res:
			imei = res.group(1)
			first_date = res.group(2)
			first_time = res.group(3)
			break

	# 找最后一个
	for log_i in reversed(log):
		res = re.match(ptn, log_i)
		if res:
			last_date = res.group(2)
			last_time = res.group(3)
			break

	my_print('IMEI: ' + imei)
	my_print('First date & time: \t' + first_date + ' ' + first_time)
	my_print('Last date & time: \t' + last_date + ' ' + last_time)


# 解析结束时间，排序输出
def sort_time_finish():
	ptn = r'.*?(\d+)'

	time_finish_int = []
	for i in time_fin:
		res = re.match(ptn, log[i])
		if res:
			time_finish_int.append(int(res.group(1)))

	time_finish_int.sort()
	my_print(time_finish_int)


# 换行打印列表
def pt(list_a):
	for i in list_a:
		my_print(i)


# 按行号打印log内容
def pt_log(list_a):
	for i in list_a:
		my_print(str(i) + ' ' + log[i].strip())


# 按行号保存log内容到新文件
# def save_to(lines, file_name, line_no=False):
# 	# new_file = '\\'.join(file.split('\\')[0:-1]) + '\\' + file_name
# 	new_file = file_name
# 	try:
# 		with open(new_file, 'x', encoding='utf-8') as f:
# 			for i in lines:
# 				if line_no:
# 					f.write(str(i) + '\t' + log[i])
# 				else:
# 					f.write(log[i])
# 		myprint('保存成功：' + new_file)
# 	except FileExistsError:
# 		myprint('保存失败：文件已存在')


# 在原文件名的基础上加上一个后缀string作为新文件名
def new_file_name(string,format=None):
	log_file_names = file.split('.')
	log_file_names[-2] += ('_'+string) # 加后缀
	if format:
		log_file_names[-1] = format
	new_name = '.'.join(log_file_names)
	return new_name


# 寻找string，保存到同名文件
# 例如：从D:\log\srv_logs\Y25\Y25_20160519.log寻找RMC，结果将保存到D:\log\srv_logs\Y25\Y25_20160519 RMC.log
# def select_to(string, result=None, line_no=False):
# 	if result is None:
# 		result = search(string)
# 	file_name = new_file_name(string)
# 	save_to(result, file_name, line_no)


# 获取包含有效RMC速度的NMEA到同名文件
# todo：考虑按日期分开
# def get_speed():
# 	result = search_and(['RMC', ',A,'])
# 	select_to('valid RMC', result)


def save_to_csv(file, result, title = None):
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
		print("\n结果保存到文件："+file)


def save_basic_result_to_csv():
	title = ['文件名', '版本号（最后一条版本号记录）', 'IMEI', '开始时间', '结束时间', \
					'start个数', 'drv_start个数', 'period个数', 'stop个数', 'stop_1个数', \
					'stop_all个数', 'stop_hold个数', 'stop_2个数', 'stop_pos个数', \
					'stop_ack个数', 'time_finish个数', 'AGPS开始个数', 'AGPS成功个数',  \
                    'AGPS失败个数', '所有定位耗时']
	if len(fw)>0:
		last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
	else:
		last_fw = 'None'
	first_dt = first_date + ' ' + first_time
	last_dt = last_date + ' ' + last_time
	result = [[file, last_fw, imei, first_dt, last_dt, str(len(start)), \
					str(len(drv_start)), str(len(period)), str(len(stop)), \
					str(len(stop_1)), str(len(stop_all)), str(len(stop_hold)), \
					str(len(stop_2)), str(len(stop_pos)), str(len(stop_ack)), \
					str(len(time_fin)), str(len(agps_start)), str(len(agps_ok)), \
					str(len(agps_fail)), time_fin_int]]
	save_to_csv(RESULT_FILE_CSV, result, title)


# 基础解析
def BASIC():
	global file, log, fw, stop, stop_1, stop_all, stop_hold, drv_start, period, start, locate, stop_2, stop_pos, stop_ack, time_fin, agps_start, agps_ok, agps_fail, time_fin_int, locate_info_list

	file = input('待解析文件地址：')
	try:
		log = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	# 寻找imei，日期，时间
	my_print('\n')
	find_imei_date_time()

	# 版本号
	my_print('\n')
	my_print('__fw__')
	fw = search('FW')
	if len(fw) > 0:
		first_fw = log[fw[0]][log[fw[0]].index('bb'):-1].strip()
		my_print(first_fw)
		last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
		if first_fw != last_fw:
			my_print(last_fw)

	# 定位开始
	my_print('\n')
	my_print('__drv_start__', end='')
	drv_start = search('mx_gps_ctrl_drv_start')
	my_print('__period__', end='')
	period = search('mx_location_period_timer__cb')

	start = drv_start + period
	start.sort()
	my_print('__start__ = drv_start + period')

	# 定位结束
	my_print('__stop__', end='')
	stop = search('[GPSstop]')

	# 定位起止
	locate = start + stop
	locate.sort()

	## 固定时间
	my_print('\n')
	my_print('[30s]__stop_1__', end='')
	stop_1 = search('[GPSstop]phase 1 timeout')

	my_print('[5min]__stop_all__', end='')
	stop_all = search('[GPSstop]phase all timeout')

	my_print('[2min]__stop_hold__', end='')
	stop_hold = search('[GPSstop]hold timer timeout')

	## 变化时间
	my_print('\n')
	my_print('__stop_2__', end='')
	stop_2 = search('[GPSstop]phase 2 end')
	if len(stop_2) > 0 and len(stop_2) < 30:
		my_print('calculate GGA before [GPSstop]phase 2 end (calc_time(stop_2)):')
		calc_time(stop_2)
		my_print("calculate valid GGA before [GPSstop]phase 2 end (calc_time(stop_2,',E,1,')):")
		calc_time(stop_2, ',E,1,')
	elif len(stop_2) > 29:
		my_print("\ttoo much, call -> calc_time(stop_2,',E,1,')")

	my_print('\n')
	my_print('__stop_pos__', end='')
	stop_pos = search('[GPSstop]postion complete')
	if len(stop_pos) > 0 and len(stop_pos) < 30:
		my_print('calculate GGA before [GPSstop]postion complete (calc_time(stop_pos)):')
		calc_time(stop_pos)
		my_print("calculate valid GGA before [GPSstop]postion complete: (calc_time(stop_pos,',E,1,'))")
		calc_time(stop_pos, ',E,1,')
	elif len(stop_pos) > 29:
		my_print("\ttoo much, call -> calc_time(stop_pos,',E,1,')")

	my_print('\n')
	my_print('__stop_ack__', end='')
	stop_ack = search('[GPSstop]ACKOK all done')
	if len(stop_ack) > 0 and len(stop_ack) < 30:
		my_print('calculate GGA before [GPSstop]ACKOK all done (calc_time(stop_ack)):')
		calc_time(stop_ack)
		my_print("calculate valid GGA before [GPSstop]ACKOK all done (calc_time(stop_ack,',E,1,')):")
		calc_time(stop_ack, ',E,1,')
	elif len(stop_ack) > 29:
		my_print("\ttoo much, call -> calc_time(stop_ack,',E,1,')")

	# 结束时间
	my_print('\n')
	my_print('__time_fin__')
	time_fin = search('[GPS]time_finish')
	time_fin_int = sort_time_finish()

	# AGPS
	my_print('\n')
	my_print('__agps_start__', end='')
	agps_start = search('[AGPS]mx_agps_request_start')

	my_print('\n')
	my_print('__agps_ok__', end='')
	agps_ok = search('[AGPS]ACKOK all done')

	my_print('\n')
	my_print('__agps_fail__', end='')
	agps_fail = search('[AGPS]mx_agps_request_stop')

	# 保存结果
	save_basic_result_to_csv()
	input('\n基础分析到此完毕\n')


# 无限读取用户命令并执行
def cmd_parse():
	while True:
		cmd = input('\ncmd:')
		try:
			exec(cmd)
		except Exception as e:
			my_print(e)


try:
	BASIC()
except Exception as e:
	my_print(e)

my_print(my_help)
cmd_parse()
