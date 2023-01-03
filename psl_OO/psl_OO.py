import re

class LogData(object):
	pass

class LogFile(object):
	print_to_file = False
	LOG_FILE = 'psl.log'
	RESULT_FILE = 'psl_basic_result.log'
	RESULT_FILE_CSV = 'psl_basic_result.csv'

	def __init__(self, filename):
		self.filename = filename
		self.log = []
		self.imei = ''
		self.first_date = ''
		self.first_time = ''
		self.last_date = ''
		self.last_time = ''

		try:
			with open(filename, 'r', encoding='utf-8') as f:
				for line in f.readlines():
					self.log.append(line)
		except Exception as e:
			input('读取文件失败,' + str(e))

	# 自定义打印函数
	def my_print(self, *objects, sep=' ', end='\n', flush=False):
		if not LogFile.print_to_file:
			print(*objects, sep=sep, end=end, flush=flush)
		else:
			try:
				f = open(LogFile.LOG_FILE, 'x')
			except FileExistsError:
				f = open(LogFile.LOG_FILE, 'a')
			print(*objects, sep=sep, end=end, file=f, flush=flush)
			f.close()

	# 设置是否打印到文件
	def set_print_to_file(self, set=False):
		LogFile.print_to_file = set
		self.my_print('\n\n')
		self.my_print("====================================================")
		self.my_print("  " + self.filename)
		self.my_print("====================================================")

	def find_imei_date_time(self):
		ptn = r'^(\d{15}),(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$'

		# 找第一个
		for log_i in self.log:
			res = re.match(ptn, log_i)
			if res:
				self.imei = res.group(1)
				self.first_date = res.group(2)
				self.first_time = res.group(3)
				break

		# 找最后一个
		for log_i in reversed(self.log):
			res = re.match(ptn, log_i)
			if res:
				self.last_date = res.group(2)
				self.last_time = res.group(3)
				break
				
		self.my_print('IMEI: ' + self.imei)
		self.my_print('First date & time: \t' + self.first_date + ' ' + self.first_time)
		self.my_print('Last date & time: \t' + self.last_date + ' ' + self.last_time)
	
	# v1: 从line_from到line_to找出内容包含string的行，返回行号
	def search(self, string, line_from=0, line_to=0, pt=False):
		search_res = []
		if line_from == 0:
			start = 0
		else:
			start = line_from

		if line_to == 0:
			stop = len(self.log)
		else:
			stop = line_to

		for line_index in range(start, stop):
			if string in self.log[line_index]:
				search_res.append(line_index)
				if pt:
					self.my_print(line_index, self.log[line_index].strip())

		return search_res

	
	pass