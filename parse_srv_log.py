
readme = '''
	说明：
	parse_srv_log.basic_parse() -- 基础解析流程

	parse_srv_log.start -- 所有start
	parse_srv_log.stop -- 所有stop
	parse_srv_log.stop_2
	parse_srv_log.stop_pos
	parse_srv_log.stop_ack

	parse_srv_log.pt_log(parse_srv_log.start) -- 显示具体内容

	parse_srv_log.find_nearest(parse_srv_log.period,1362)
	-- 查找parse_srv_log.period中最接近（小于）1362的值

	parse_srv_log.find_nearest(parse_srv_log.period,1362,big=True)
	-- 查找parse_srv_log.period中最接近（大于）1362的值

	parse_srv_log.search_in('GGA',1301,1362,pt=True)
	-- 查询在1301和1362之间包含'GGA'的行数，并显示该行具体内容（pt为True）

	parse_srv_log.search_more(['GGA','GST'],1301,1362)
	-- 查询在1301和1362之间包含'GGA'或'GST'的行数（可加pt）

	parse_srv_log.calc(',T3,','[GPSstop]pos',',E,1,')
	-- 查询在',T3,'和'[GPSstop]pos'之间',E,1,'的个数

	parse_srv_log.calc('mx_agps_request_start','time_finish:119','ACKOK all',max=True)
	-- 查询在'mx_agps_request_start'和'time_finish:119'之间'ACKOK all'的个数（按最大范围）
'''

def open_file(file):
	global log
	log = []
	with open(file, 'r') as f:
		for line in f.readlines():
			log.append(line)
	return log  # string list

# v1: 从line_from到line_to找出内容包含string的行，返回行号
def search_in(string, line_from=0, line_to=0, pt=False):
	global file
	log = open_file(file)
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
def search_more(string_list, line_from=0, line_to=0, pt=False):
	global file
	log = open_file(file)
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
		cnt = len(search_in(string,start_line,stop_line))
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
	# cnt = len(search_in(string,start_line,stop_line))
	# GGA_cnt.append(cnt)
	
	# for i in range(1,len(stop_list)):
		# stop_line = stop_list[i]
		# start_line = find_nearest(start,stop_list[i-1])
		# print('\tbetween line %d and %d, '%(start_line, stop_line),end='')
		# cnt = len(search_in(string,start_line,stop_line))
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
		start_list = search_in(start_str_or_list)

	if type(stop_str_or_list) == list:
		stop_list = stop_str_or_list
	else:
		stop_list = search_in(stop_str_or_list)
		
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
		cnt = len(search_in(goal_str,start_line,stop_line))
		goal_cnt.append(cnt)
	return goal_cnt

# 换行打印列表
def pt(list):
	for i in list:
		print(i)

# 按行号打印log内容
def pt_log(list):
	for i in list:
		print(log[i])

# 基础解析
def basic_parse():
	global file,fw,stop,stop_1,stop_all,stop_hold,drv_start,period,start,locate,stop_2,stop_pos,stop_ack,GGA
	file = input('待解析文件地址：')

	# 版本号
	print('\n')
	print('__fw__')
	fw = search_in('FW')
	print(log[fw[0]])
	if log[fw[-1]] != log[fw[0]]:
		print(log[fw[-1]])

	# print('__GGA__',end='')
	# GGA = search_in('GGA')

	# 定位开始
	print('\n')
	print('__drv_start__',end='')
	drv_start = search_in('mx_gps_ctrl_drv_start')
	print('__period__',end='')
	period = search_in('mx_location_period_timer__cb')

	start = drv_start+period
	start.sort()
	print('__start__ = drv_start + period')

	# 定位结束
	print('__stop__',end='')
	stop = search_in('[GPSstop]')
	
	# 定位起止
	locate = start+stop
	locate.sort()
	# for i in locate:
		# print('%d: %s'%(i,log[i]))

	## 固定时间
	print('\n')
	print('[30s]__stop_1__',end='')
	stop_1 = search_in('[GPSstop]phase 1 timeout')

	print('[5min]__stop_all__',end='')
	stop_all = search_in('[GPSstop]phase all timeout')

	print('[2min]__stop_hold__',end='')
	stop_hold = search_in('[GPSstop]hold timer timeout')

	## 变化时间
	print('\n')
	print('__stop_2__',end='')
	stop_2 = search_in('[GPSstop]phase 2 end')
	if len(stop_2) > 0 and len(stop_2) < 30:
		print('calculate GGA before [GPSstop]phase 2 end:')
		calc_time(stop_2)
		print('calculate valid GGA before [GPSstop]phase 2 end:')
		calc_time(stop_2,',E,1,')
	else:
		print("\ttoo much, call -> calc_time(stop_2,',E,1,')")
		
	print('\n')
	print('__stop_pos__',end='')
	stop_pos = search_in('[GPSstop]postion complete')
	if len(stop_pos) > 0 and len(stop_pos) < 30:
		print('calculate GGA before [GPSstop]postion complete:')
		calc_time(stop_pos)
		print('calculate valid GGA before [GPSstop]postion complete:')
		calc_time(stop_pos,',E,1,')
	else:
		print("\ttoo much, call -> calc_time(stop_pos,',E,1,')")
		
	print('\n')
	print('__stop_ack__',end='')
	stop_ack = search_in('[GPSstop]ACKOK all done')
	if len(stop_ack) > 0 and len(stop_ack) < 30:
		print('calculate GGA before [GPSstop]ACKOK all done:')
		calc_time(stop_ack)
		print('calculate valid GGA before [GPSstop]ACKOK all done:')
		calc_time(stop_ack,',E,1,')
	else:
		print("\ttoo much, call -> calc_time(stop_ack,',E,1,')")
		
	print(readme)
	input('\n基础分析到此完毕\n')

basic_parse()
