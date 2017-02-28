#!/usr/bin/python3
# -*- coding: utf-8 -*-

my_help = '''
功能说明：
	basic_parse() -- 读取log文件并进行基础解析（请首先执行这个）

	line_list变量包括：
	start -- 所有start
	stop -- 所有stop
	fw,stop,stop_1,stop_all,stop_hold,drv_start,period,start,locate,stop_2,stop_pos,stop_ack,time_fin......

	pt2file(True) -- 为True则将后续所有输出存入文件psl.log，否则输出到console（默认为False）
	
	pt_log(line_list) -- 显示行号和具体内容

	find_nearest(line_list,1362,big=True)
	-- 查找line_list中最接近（默认小于，big=True表示大于）1362的值

	search('GGA',1301,1362,pt=True)
	-- 查询在1301和1362之间包含'GGA'的行数，pt为True则显示该行具体内容（默认为False）

	search_or(['GGA','GST'],1301,1362)
	-- 查询在1301和1362之间包含'GGA'或'GST'的行数（可加pt），保存到.csv文件

	search_or_with_time(['GGA','GST'])
	-- 查询包含'GGA'或'GST'的行号和内容，保存到.csv文件

	search_and(['GGA',',E,1,'],1301,1362)
	-- 查询在1301和1362之间包含'GGA'和',E,1,'的行数（可加pt）
	
	calc(',T3,','[GPSstop]pos',',E,1,')
	-- 查询在',T3,'和'[GPSstop]pos'之间',E,1,'的个数
	calc(start,time_fin,'GPSstop',max=True)
	-- 查询在start和time_fin之间'GPSstop'的个数（max为True表示按最大范围）
	
	calc_time(stop_list,string='GGA')
	-- 自动寻找最近的start，然后计算中间GGA的个数，打印输出结果，返回所有结果的列表
	
	save_to(start,'start.txt',line_no=Ture)
	-- 将start行号对应的内容保存到start.txt，line_no为True表示同时保存行号（默认为False）
	
	select_to('RMC')
	-- 按文件名+' RMC'保存结果到文件
	-- 参数line_no为True表示同时保存行号（默认为False）
	-- 参数result不为空时直接保存result到文件（默认为空时，保存搜索'RMC'的结果）
	
	get_speed()
	-- 获取包含有效RMC速度的NMEA到同名文件(valid RMC)
'''

import re

MY_OUT_FILE = False
LOG_FILE = 'psl.log'
RESULT_FILE = 'psl_basic_result.log'
RESULT_FILE_CSV = 'psl_basic_result.csv'
TIME_RESULT_FILE_CSV = 'time_result.csv'

# 自定义打印函数
def myprint(*objects, sep=' ', end='\n', flush=False):
	global MY_OUT_FILE
	if not MYOUT_FILE:
		print(*objects, sep=sep, end=end, flush=flush)
	else:
		try:
			f = open(LOG_FILE, 'x')
		except FileExistsError:
			f = open(LOG_FILE, 'a')
		print(*objects, sep=sep, end=end, file=f, flush=flush)
		f.close()

# 设置打印到文件
def pt2file(a=False):
	global MY_OUT_FILE, file
	MYOUT_FILE = a
	myprint('\n\n')
	myprint("====================================================")
	myprint("  " + file)
	myprint("====================================================")


def open_file(file):
	# global log
	log = []
	with open(file, 'r', encoding='utf-8') as f:
		for line in f.readlines():
			log.append(line)
	return log  # string list


# v1: 从line_from到line_to找出内容包含string的行，返回行号
def search(string, line_from=0, line_to=0, pt=False):
	# global file
	# log = open_file(file)
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
				myprint(line_index, log[line_index].strip())

	myprint(string, ': ', str(len(search_res)))
	return search_res  # list


# v2: 从line_from到line_to找出内容包含string_list内任一内容的行，返回行号
def search_or(string_list, line_from=0, line_to=0, pt=False):
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
					myprint(line_index, log[line_index].strip())
				break

	myprint(string_list, ': ', str(len(search_res)))

	csv_file_name = new_file_name(string_list[0]+str(len(string_list)),'csv')
	for i in search_res:
		save_to_csv(csv_file_name, [str(i),log[i].strip()])

	print("结果保存到文件："+csv_file_name)

	return search_res  # list

def string_has_time(string):
	ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	res = re.match(ptn, string)
	if res:
		return True
	else:
		return False
		
# 从line_from到line_to找出内容包含string_list内任一内容的行，以及前面最近的时间，统一输出到csv文件
def search_or_with_time(string_list, line_from=0, line_to=0):
	search_res = []
	time_res = []
	
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
				break
	
	for line_index_end in search_res:
		for line_index in reversed(range(0,line_index_end)):
			string = log[line_index]
			if string_has_time(string):
				time_res.append(line_index)
				break

	time_res = list(set(time_res)) # remove redundant
	res = search_res + time_res
	res.sort()
	
	myprint(res, ': ', str(len(res)))

	csv_file_name = new_file_name(string_list[0]+str(len(string_list)),'csv')
	for i in res:
		save_to_csv(csv_file_name, [str(i),log[i].strip()])

	print("结果保存到文件："+csv_file_name)
	return res  # list	

# v3：从line_from到line_to找出内容包含string_list内所有内容的行，返回行号
def search_and(string_list, line_from=0, line_to=0, pt=False):
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
				myprint(line_index, log[line_index].strip())

	myprint(string_list, ': ', str(len(search_res)))
	return search_res  # list


# v1:找出line_list（从小到大排列）中最接近（小于）line_goal的一个
# def find_nearest(line_list, line_goal):
# res = 0
# if len(line_list) == 0:
# myprint('error: line_list empty')
# return None
# for line_no in line_list:
# if line_no < line_goal:
# res = line_no
# return res

# v2:应该是找line_list（从小到大排列）中最接近（大于）line_goal的一个
# def find_nearest(line_list, line_goal):
# if len(line_list) == 0:
# myprint('error: line_list empty')
# return None
# for line_no in line_list:
# if line_no > line_goal:
# res = line_no
# return res

# v3：默认找出line_list（从小到大排列）中最接近（小于）line_goal的一个
# big为True时，找出line_list（从小到大排列）中最接近（大于）line_goal的一个
def find_nearest(line_list, line_goal, big=False):
	res = 0
	if len(line_list) == 0:
		myprint('error: line_list empty')
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
		myprint('\tbetween line %d and %d, ' % (start_line, stop_line), end='')
		if string != 'GGA':
			cnt = len(search_and([string, 'GGA'], start_line, stop_line))
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
def calc(start_str_or_list, stop_str_or_list, goal_str, if_max=False):
	goal_cnt = []

	if type(start_str_or_list) == list:
		start_list = start_str_or_list
	else:
		start_list = search(start_str_or_list)

	if type(stop_str_or_list) == list:
		stop_list = stop_str_or_list
	else:
		stop_list = search(stop_str_or_list)

	for i in range(len(stop_list)):
		stop_line = stop_list[i]
		if if_max:
			if i == 0:
				start_line = 0
			else:
				prev_stop = stop_list[i - 1]
				start_line = find_nearest(start_list, prev_stop, big=True)
				if start_line > stop_line:
					start_line = find_nearest(start_list, stop_line)
		else:
			start_line = find_nearest(start_list, stop_line)
		myprint('\tbetween line %d and %d, ' % (start_line, stop_line), end='')
		cnt = len(search(goal_str, start_line, stop_line))
		goal_cnt.append(cnt)
	return goal_cnt


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

	myprint('IMEI: ' + imei)
	myprint('First date & time: \t' + first_date + ' ' + first_time)
	myprint('Last date & time: \t' + last_date + ' ' + last_time)


# 解析结束时间，排序输出
def sort_time_finish():
	ptn = r'.*?(\d+)'

	time_finish_res = []
	for i in time_fin:
		res = re.match(ptn, log[i])
		if res:
			time_finish_res.append(int(res.group(1)))

	time_finish_res.sort()
	myprint(time_finish_res)


# 换行打印列表
def pt(list_a):
	for i in list_a:
		myprint(i)


# 按行号打印log内容
def pt_log(list_a):
	for i in list_a:
		myprint(str(i) + ' ' + log[i].strip())


# 按行号保存log内容到新文件
def save_to(lines, file_name, line_no=False):
	# new_file = '\\'.join(file.split('\\')[0:-1]) + '\\' + file_name
	new_file = file_name
	try:
		with open(new_file, 'x') as f:
			for i in lines:
				if line_no:
					f.write(str(i) + '\t' + log[i])
				else:
					f.write(log[i])
		myprint('保存成功：' + new_file)
	except FileExistsError:
		myprint('保存失败：文件已存在')

# 在原文件名的基础上加上一个后缀string作为新文件名
def new_file_name(string,format=None):
	log_file_names = file.split('.')
	log_file_names[-2] += ('_'+string)
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
def get_speed():
	result = search_and(['RMC', ',A,'])
	select_to('valid RMC', result)


# 保存基础解析结果到文件
# 格式：
# 文件名，版本号（最后一条版本号记录），IMEI，开始时间，结束时间，drv_start个数，period个数，start个数，stop个数，stop_1个数，stop_all个数，stop_hold个数，stop_2个数，stop_pos个数，stop_ack个数，time_finish个数，AGPS开始个数，AGPS成功个数，AGPS失败个数
def save_basic_result_to():
	basic_result_file = RESULT_FILE
	try:
		f = open(basic_result_file, 'x')
		f.write('文件名,版本号（最后一条版本号记录）,IMEI,开始时间,结束时间,start个数,drv_start个数,\
		period个数,stop个数,stop_1个数,stop_all个数,stop_hold个数,stop_2个数,stop_pos个数,\
		stop_ack个数,time_finish个数,AGPS开始个数,AGPS成功个数,AGPS失败个数\n')
	except FileExistsError:
		f = open(basic_result_file, 'a')
	finally:
		last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
		first_dt = first_date + ' ' + first_time
		last_dt = last_date + ' ' + last_time
		res_list = [file, last_fw, imei, first_dt, last_dt, str(len(start)), \
					str(len(drv_start)), str(len(period)), str(len(stop)), \
					str(len(stop_1)), str(len(stop_all)), str(len(stop_hold)), \
					str(len(stop_2)), str(len(stop_pos)), str(len(stop_ack)), \
					str(len(time_fin)), str(len(agps_start)), str(len(agps_ok)), \
					str(len(agps_fail))]
		res_string = ','.join(res_list)
		f.write(res_string + '\n')
		f.close()

def save_to_csv(file, result, title = None):
	import csv
	try:
		f = open(file, 'x', newline='')
		if title:
			spam_writer = csv.writer(f)
			spam_writer.writerow(title)
	except FileExistsError:
		f = open(file, 'a', newline='')
	finally:
		spam_writer = csv.writer(f)
		spam_writer.writerow(result)
		f.close()
		
def save_basic_result_to_csv():
	title = ['文件名', '版本号（最后一条版本号记录）', 'IMEI', '开始时间', '结束时间', \
					'start个数', 'drv_start个数', 'period个数', 'stop个数', 'stop_1个数', \
					'stop_all个数', 'stop_hold个数', 'stop_2个数', 'stop_pos个数', \
					'stop_ack个数', 'time_finish个数', 'AGPS开始个数', 'AGPS成功个数', 'AGPS失败个数']
	last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
	first_dt = first_date + ' ' + first_time
	last_dt = last_date + ' ' + last_time
	result = [file, last_fw, imei, first_dt, last_dt, str(len(start)), \
					str(len(drv_start)), str(len(period)), str(len(stop)), \
					str(len(stop_1)), str(len(stop_all)), str(len(stop_hold)), \
					str(len(stop_2)), str(len(stop_pos)), str(len(stop_ack)), \
					str(len(time_fin)), str(len(agps_start)), str(len(agps_ok)), \
					str(len(agps_fail))]
	save_to_csv(RESULT_FILE_CSV, result, title)


# 基础解析
def basic_parse():
	global file, log, fw, stop, stop_1, stop_all, stop_hold, drv_start, period, start, locate, stop_2, stop_pos, stop_ack, time_fin, agps_start, agps_ok, agps_fail

	file = input('待解析文件地址：')
	try:
		log = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	# 寻找imei，日期，时间
	myprint('\n')
	find_imei_date_time()

	# 版本号
	myprint('\n')
	myprint('__fw__')
	fw = search('FW')
	first_fw = log[fw[0]][log[fw[0]].index('bb'):-1].strip()
	myprint(first_fw)
	last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
	if first_fw != last_fw:
		myprint(last_fw)

	# myprint('__GGA__',end='')
	# GGA = search('GGA')

	# 定位开始
	myprint('\n')
	myprint('__drv_start__', end='')
	drv_start = search('mx_gps_ctrl_drv_start')
	myprint('__period__', end='')
	period = search('mx_location_period_timer__cb')

	start = drv_start + period
	start.sort()
	myprint('__start__ = drv_start + period')

	# 定位结束
	myprint('__stop__', end='')
	stop = search('[GPSstop]')

	# 定位起止
	locate = start + stop
	locate.sort()
	# for i in locate:
	# myprint('%d: %s'%(i,log[i]))

	## 固定时间
	myprint('\n')
	myprint('[30s]__stop_1__', end='')
	stop_1 = search('[GPSstop]phase 1 timeout')

	myprint('[5min]__stop_all__', end='')
	stop_all = search('[GPSstop]phase all timeout')

	myprint('[2min]__stop_hold__', end='')
	stop_hold = search('[GPSstop]hold timer timeout')

	## 变化时间
	myprint('\n')
	myprint('__stop_2__', end='')
	stop_2 = search('[GPSstop]phase 2 end')
	if len(stop_2) > 0 and len(stop_2) < 30:
		myprint('calculate GGA before [GPSstop]phase 2 end (calc_time(stop_2)):')
		calc_time(stop_2)
		myprint("calculate valid GGA before [GPSstop]phase 2 end (calc_time(stop_2,',E,1,')):")
		calc_time(stop_2, ',E,1,')
	elif len(stop_2) > 29:
		myprint("\ttoo much, call -> calc_time(stop_2,',E,1,')")

	myprint('\n')
	myprint('__stop_pos__', end='')
	stop_pos = search('[GPSstop]postion complete')
	if len(stop_pos) > 0 and len(stop_pos) < 30:
		myprint('calculate GGA before [GPSstop]postion complete (calc_time(stop_pos)):')
		calc_time(stop_pos)
		myprint("calculate valid GGA before [GPSstop]postion complete: (calc_time(stop_pos,',E,1,'))")
		calc_time(stop_pos, ',E,1,')
	elif len(stop_pos) > 29:
		myprint("\ttoo much, call -> calc_time(stop_pos,',E,1,')")

	myprint('\n')
	myprint('__stop_ack__', end='')
	stop_ack = search('[GPSstop]ACKOK all done')
	if len(stop_ack) > 0 and len(stop_ack) < 30:
		myprint('calculate GGA before [GPSstop]ACKOK all done (calc_time(stop_ack)):')
		calc_time(stop_ack)
		myprint("calculate valid GGA before [GPSstop]ACKOK all done (calc_time(stop_ack,',E,1,')):")
		calc_time(stop_ack, ',E,1,')
	elif len(stop_ack) > 29:
		myprint("\ttoo much, call -> calc_time(stop_ack,',E,1,')")

	# 结束时间
	myprint('\n')
	myprint('__time_fin__')
	time_fin = search('[GPS]time_finish')
	sort_time_finish()

	# AGPS
	myprint('\n')
	myprint('__agps_start__', end='')
	agps_start = search('[AGPS]mx_agps_request_start')

	myprint('\n')
	myprint('__agps_ok__', end='')
	agps_ok = search('[AGPS]ACKOK all done')

	myprint('\n')
	myprint('__agps_fail__', end='')
	agps_fail = search('[AGPS]mx_agps_request_stop')

	# 保存结果
	save_basic_result_to()
	save_basic_result_to_csv()
	input('\n基础分析到此完毕，结果已保存到%s，建议使用Excel按逗号分列查看\n' % (RESULT_FILE))


# 无限读取用户命令并执行
def cmd_parse():
	while True:
		cmd = input('\ncmd:')
		try:
			exec(cmd)
		except Exception as e:
			myprint(e)


try:
	basic_parse()
except Exception as e:
	myprint(e)

myprint(my_help)
cmd_parse()
