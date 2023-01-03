import re

def open_file(file):
	# global log
	log = []
	with open(file, 'r', encoding='utf-8') as f:
		for line in f.readlines():
			log.append(line)
	return log  # string list

def re_text(string):
	ptn = r'ci=(\d+), lac=(\d+)'
	res = re.search(ptn, string)
	if res:
		ci=res.group(1)
		lac=res.group(2)
		return (ci,lac)
	else:
		return None

def new_file_name(string,format=None):
	log_file_names = file.split('.')
	log_file_names[-2] += ('_'+string)
	if format:
		log_file_names[-1] = format
	new_name = '.'.join(log_file_names)
	return new_name


def save_re_file(lines):
	new_file = new_file_name('re')
	try:
		with open(new_file, 'x') as f:
			for line in lines:
				f.write(line)
		print('保存成功：' + new_file)
	except FileExistsError:
		print('保存失败：文件已存在')


def main():
	global file, log

	file = input('文件地址：')
	try:
		log = open_file(file)
	except Exception as e:
		input('读取文件失败,' + str(e))
		return

	new_log = []
	for line in log:
		new_line = re_text(line)
		new_log.append(new_line)

	save_re_file(new_log)


main()