'''
说明：
	psl.basic_parse() -- 基础解析流程

	psl.start -- 所有start
	psl.stop -- 所有stop
	psl.stop_2
	psl.stop_pos
	psl.stop_ack

	psl.pt_log(psl.start) -- 显示具体内容

	psl.find_nearest(psl.period,1362)
	-- 查找psl.period中最接近（小于）1362的值

	psl.find_nearest(psl.period,1362,big=True)
	-- 查找psl.period中最接近（大于）1362的值

	psl.search('GGA',1301,1362,pt=True)
	-- 查询在1301和1362之间包含'GGA'的行数，并显示该行具体内容（pt为True）

	psl.search_or(['GGA','GST'],1301,1362)
	-- 查询在1301和1362之间包含'GGA'或'GST'的行数（可加pt）

	psl.search_and(['GGA',',E,1,'],1301,1362)
	-- 查询在1301和1362之间包含'GGA'和',E,1,'的行数（可加pt）
	
	psl.calc(',T3,','[GPSstop]pos',',E,1,')
	-- 查询在',T3,'和'[GPSstop]pos'之间',E,1,'的个数

	psl.calc('mx_agps_request_start','time_finish:119','ACKOK all',max=True)
	-- 查询在'mx_agps_request_start'和'time_finish:119'之间'ACKOK all'的个数（按最大范围）
	
	psl.save_to(psl.start,'start.txt',line_no=Ture)
	-- 将start行号对应的内容保存到start.txt，line_no为True表示同时保存行号（默认为False）
	
	psl.select_to('RMC')
	-- 搜索'RMC'并保存结果到同名文件，例如：
	-- 从D:\log\srv_logs\Y25\Y25_20160519.log寻找RMC，结果将保存到D:\log\srv_logs\Y25\Y25_20160519 RMC.log
'''

import re

def open_file(file):
	# global log
	log = []
	with open(file, 'r') as f:
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
				print(line_index, log[line_index])

	print(string, ': ', str(len(search_res)))
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
					print(line_index, log[line_index])
				break

	print(string_list, ': ', str(len(search_res)))
	return search_res  # list

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
				print(line_index, log[line_index])

	print(string_list, ': ', str(len(search_res)))
	return search_res  # list


# v1:找出line_list（从小到大排列）中最接近（小于）line_goal的一个
# def find_nearest(line_list, line_goal):
	# res = 0
	# if len(line_list) == 0:
		# print('error: line_list empty')
		# return None
	# for line_no in line_list:
		# if line_no < line_goal:
			# res = line_no
	# return res

# v2:应该是找line_list（从小到大排列）中最接近（大于）line_goal的一个
# def find_nearest(line_list, line_goal):
	# if len(line_list) == 0:
		# print('error: line_list empty')
		# return None
	# for line_no in line_list:
		# if line_no > line_goal:
			# res = line_no
			# return res

# v3：默认找出line_list（从小到大排列）中最接近（小于）line_goal的一个
# big为True时，找出line_list（从小到大排列）中最接近（大于）line_goal的一个
def find_nearest(line_list, line_goal, big = False):
	res = 0
	if len(line_list) == 0:
		print('error: line_list empty')
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
def calc_time(stop_list,string='GGA'):
	GGA_cnt = []
	
	for stop_line in stop_list:
		start_line = find_nearest(start,stop_line)
		print('\tbetween line %d and %d, '%(start_line, stop_line),end='')
		if string != 'GGA':
			cnt = len(search_and([string,'GGA'],start_line,stop_line))
		else:
			cnt = len(search(string,start_line,stop_line))
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
	# print('\tbetween line %d and %d, '%(start_line, stop_line),end='')
	# cnt = len(search(string,start_line,stop_line))
	# GGA_cnt.append(cnt)
	
	# for i in range(1,len(stop_list)):
		# stop_line = stop_list[i]
		# start_line = find_nearest(start,stop_list[i-1])
		# print('\tbetween line %d and %d, '%(start_line, stop_line),end='')
		# cnt = len(search(string,start_line,stop_line))
		# GGA_cnt.append(cnt)
	# return GGA_cnt

# 统计从start_str到stop_str之间出现的goal_str的个数
# 默认统计范围：对每一个stop，从它前面最靠近的一个start开始
# max为True情况的统计范围：对每一个stop，从前一个stop之后的第一个start开始
# 如果stop前面没有start，则以0作为start
# 可以直接输入start/stop列表
def calc(start_str_or_list, stop_str_or_list, goal_str, max = False):
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
		if max:
			if i == 0:
				start_line = 0
			else:
				prev_stop = stop_list[i-1]
				start_line = find_nearest(start_list,prev_stop,big=True)
				if start_line > stop_line:
					start_line = find_nearest(start_list,stop_line)
		else:
			start_line = find_nearest(start_list,stop_line)
		print('\tbetween line %d and %d, '%(start_line, stop_line),end='')
		cnt = len(search(goal_str,start_line,stop_line))
		goal_cnt.append(cnt)
	return goal_cnt

# 寻找imei，日期，时间
def find_imei_date_time():
	ptn=r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'
	imei,first_date,first_time,last_date,last_time='','','','',''
	
	# 找第一个
	for log_i in log:
		res = re.match(ptn, log_i)
		if res:
			imei = res.group(1)
			first_date = res.group(2)
			first_time = res.group(3)
			break
			
	#找最后一个
	for log_i in reversed(log):
		res = re.match(ptn, log_i)
		if res:
			last_date = res.group(2)
			last_time = res.group(3)
			break
	
	print('IMEI: '+imei)
	print('First date & time: \t'+first_date+' '+first_time)
	print('Last date & time: \t'+last_date+' '+last_time)

# 解析结束时间，排序输出
def sort_time_finish():
	ptn = r'.*?(\d+)'
	
	time_finish_res = []
	for i in time_fin:
		res = re.match(ptn, log[i])
		if res:
			time_finish_res.append(int(res.group(1)))
	
	time_finish_res.sort()
	print(time_finish_res)

# 换行打印列表
def pt(list):
	for i in list:
		print(i)

# 按行号打印log内容
def pt_log(list):
	for i in list:
		print(log[i])

# 按行号保存log内容到新文件
def save_to(lines, file_name, line_no = False):
	new_file = '\\'.join(file.split('\\')[0:-1]) + '\\' + file_name
	try:
		with open(new_file, 'x') as f:
			for i in lines:
				if line_no:
					f.write(str(i)+'\t'+log[i])
				else:
					f.write(log[i])
		print('保存成功：'+new_file)
	except FileExistsError:
		print('保存失败：文件已存在')

# 寻找string，保存到同名文件
# 例如：从D:\log\srv_logs\Y25\Y25_20160519.log寻找RMC，结果将保存到D:\log\srv_logs\Y25\Y25_20160519 RMC.log
def select_to(string, line_no = False):
	result = search(string)
	log_file_names = file.split('\\')[-1].split('.',maxsplit=1) # 原文件名内只能有一个点
	new_file_name = log_file_names[0] + ' ' + string + '.' + log_file_names[-1]
	save_to(result, new_file_name, line_no)

# todo：保存基础解析结果到文件
# 格式：
# 文件名，版本号（最后一条版本号记录），drv_start个数，period个数，start个数，stop个数，stop_1个数，stop_all个数，stop_hold个数，locate个数，stop_2个数，stop_pos个数，stop_ack个数
def save_basic_result_to():
	basic_result_file = 'basic_result.txt'
	try:
		f = open(basic_result_file, 'x')
		f.write('文件名,版本号（最后一条版本号记录）,drv_start个数,period个数,start个数,stop个数,stop_1个数,stop_all个数,stop_hold个数,locate个数,stop_2个数,stop_pos个数,stop_ack个数\n')
	except FileExistsError:
		f = open(basic_result_file, 'a')
	finally:
		last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
		f.write(file+','+last_fw+','+str(len(drv_start))+','+str(len(period))+','+str(len(start))+','+str(len(stop))+','+str(len(stop_1))+','+str(len(stop_all))+','+str(len(stop_hold))+','+str(len(locate))+','+str(len(stop_2))+','+str(len(stop_pos))+','+str(len(stop_ack))+'\n')
		f.close()



# 基础解析
def basic_parse():
	global file,log,fw,stop,stop_1,stop_all,stop_hold,drv_start,period,start,locate,stop_2,stop_pos,stop_ack,time_fin
	
	file = input('待解析文件地址：')
	log = open_file(file)
	
	# 寻找imei，日期，时间
	print('\n')
	find_imei_date_time()
	
	# 版本号
	print('\n')
	print('__fw__')
	fw = search('FW')
	first_fw = log[fw[0]][log[fw[0]].index('bb'):-1].strip()
	print(first_fw)
	last_fw = log[fw[-1]][log[fw[-1]].index('bb'):-1].strip()
	if first_fw != last_fw:
		print(last_fw)

	# print('__GGA__',end='')
	# GGA = search('GGA')

	# 定位开始
	print('\n')
	print('__drv_start__',end='')
	drv_start = search('mx_gps_ctrl_drv_start')
	print('__period__',end='')
	period = search('mx_location_period_timer__cb')

	start = drv_start+period
	start.sort()
	print('__start__ = drv_start + period')

	# 定位结束
	print('__stop__',end='')
	stop = search('[GPSstop]')
	
	# 定位起止
	locate = start+stop
	locate.sort()
	# for i in locate:
		# print('%d: %s'%(i,log[i]))

	## 固定时间
	print('\n')
	print('[30s]__stop_1__',end='')
	stop_1 = search('[GPSstop]phase 1 timeout')

	print('[5min]__stop_all__',end='')
	stop_all = search('[GPSstop]phase all timeout')

	print('[2min]__stop_hold__',end='')
	stop_hold = search('[GPSstop]hold timer timeout')

	## 变化时间
	print('\n')
	print('__stop_2__',end='')
	stop_2 = search('[GPSstop]phase 2 end')
	if len(stop_2) > 0 and len(stop_2) < 30:
		print('calculate GGA before [GPSstop]phase 2 end (calc_time(stop_2)):')
		calc_time(stop_2)
		print("calculate valid GGA before [GPSstop]phase 2 end (calc_time(stop_2,',E,1,')):")
		calc_time(stop_2,',E,1,')
	elif len(stop_2) > 29:
		print("\ttoo much, call -> calc_time(stop_2,',E,1,')")
		
	print('\n')
	print('__stop_pos__',end='')
	stop_pos = search('[GPSstop]postion complete')
	if len(stop_pos) > 0 and len(stop_pos) < 30:
		print('calculate GGA before [GPSstop]postion complete (calc_time(stop_pos)):')
		calc_time(stop_pos)
		print("calculate valid GGA before [GPSstop]postion complete: (calc_time(stop_pos,',E,1,'))")
		calc_time(stop_pos,',E,1,')
	elif len(stop_pos) > 29:
		print("\ttoo much, call -> calc_time(stop_pos,',E,1,')")
		
	print('\n')
	print('__stop_ack__',end='')
	stop_ack = search('[GPSstop]ACKOK all done')
	if len(stop_ack) > 0 and len(stop_ack) < 30:
		print('calculate GGA before [GPSstop]ACKOK all done (calc_time(stop_ack)):')
		calc_time(stop_ack)
		print("calculate valid GGA before [GPSstop]ACKOK all done (calc_time(stop_ack,',E,1,')):")
		calc_time(stop_ack,',E,1,')
	elif len(stop_ack) > 29:
		print("\ttoo much, call -> calc_time(stop_ack,',E,1,')")
	
	# 结束时间
	print('\n')
	print('__time_fin__')
	time_fin = search('[GPS]time_finish')
	sort_time_finish()
	
	# 保存结果
	save_basic_result_to()
	input('\n基础分析到此完毕\n')

# 双击parse_srv_log.py运行时，执行基础分析，不打印__doc__
# 在命令行内import模块时，执行基础分析，打印__doc__
basic_parse()
if __name__ != '__main__':
	print(__doc__)
