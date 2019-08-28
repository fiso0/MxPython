#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
根据配置解析协议
	允许仅参数部分
	允许带空格
	大小写均可
配置示例：format.txt
配置说明参见：格式说明.txt
"""

DEFAULT_FORMAT_FILE_JTT = 'format/formatJTT.txt'
DEFAULT_FORMAT_FILE_OneNet = 'format/formatOneNet.txt'
DEFAULT_FORMAT_FILE = 'format/format.txt'


def read_format(f):
	"""
	读取配置文件
	若文件不存在，改读取默认配置文件DEFAULT_FORMAT_FILE
	若读取失败，返回None,None
	:return: 字段名（列表），字段长度（列表）
	"""
	labels = []
	lens = []
	try:
		print('读取配置文件：' + f)
		with open(f, encoding='utf-8') as file:
			for line in file.readlines():
				try:
					label, len = (line.strip().split())[:2]  # 每行必须至少2个字符串，取前两项
					labels.append(label)
					lens.append(int(len))
				except Exception as e:
					print(e)
		return labels, lens
	except FileNotFoundError:
		# 未找到配置文件，改用默认配置文件
		if 'OneNet' in f:
			default_file = DEFAULT_FORMAT_FILE_OneNet
		elif 'JTT' in f:
			default_file = DEFAULT_FORMAT_FILE_JTT
		else:
			default_file = DEFAULT_FORMAT_FILE
		if f != default_file:
			return read_format(default_file)
		else:
			print('无法读取默认配置文件：' + default_file)
			return None, None
	except Exception as e:
		print(e)
		return None, None


def get_cmd(text):
	if text == '':
		text = '262626260041000000000866888a2a556172400703ffff800d606412081c09050c72173f11211e1e20095f110033e6006e00a001040302000401280000000000004dffff0004bd'
		print('使用示例内容：' + text)
	text = text.strip().replace(' ', '').upper()  # 去掉空格 转为大写

	# 尝试自动解析指令类别
	# 26262626开头的是OneNet
	# 7E开头和结尾的是JTT808
	if text[:8] == '26262626':  # OneNet指令头
		try:
			cmd = 'OneNet' + text[36:40]
		except:
			cmd = ''
			print('尝试解析指令类别失败，将使用默认指令类别')
	elif text.startswith('7E') and text.endswith('7E'):  # JTT808标识位
		try:
			cmd = 'JTT' + text[2:6]
		except:
			cmd = ''
			print('尝试解析指令类别失败，将使用默认指令类别')
	else:
		# 不包含指令头，无指令类别，要求手动输入
		cmd = None
	return cmd


def parser_break(msg, lens):
	# 根据lens分解msg
	results = []

	message = msg.strip().replace(' ', '').upper()  # 去掉空格 转为大写
	chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]

	i = 0
	rd_len = 0
	for alen in lens:
		res = []
		try:
			if alen > 0:
				res = chrstr[rd_len:rd_len + alen]
			elif alen == 0:  # 特殊情况0：该字段跳过
				res = chrstr[rd_len:rd_len + alen]
			elif alen == -1:  # 特殊情况1：上一项标识此项的长度
				alen = int(results[i - 1][0])
				res = chrstr[rd_len:rd_len + alen]
			elif alen == -2:  # 特殊情况2：以FF结尾
				ind = chrstr[rd_len:].index('FF')
				alen = ind + 1
				res = chrstr[rd_len:rd_len + alen]
			elif alen == -3:  # 特殊情况3：剩余全部内容
				idx = lens.index(alen)
				tail_len = sum(lens[idx + 1:])  # 后续所有字段的长度和 OneNet中为3 JTT中为2
				res = chrstr[rd_len:-tail_len]
				# if(len(res)>=3): # 包含流水号、校验码
				# 	res = chrstr[rd_len:-3]
				alen = len(res)
			elif alen == -4:  # 特殊情况4：以00结尾
				ind = chrstr[rd_len:].index('00')
				alen = ind + 1
				res = chrstr[rd_len:rd_len + alen]
			if alen > len(res):
				print('预期长度大于实际长度')
				res = ''
				alen = 0
		except Exception as e:
			print(e)
			res = ''
			alen = 0

		i += 1
		rd_len += alen
		results.append(res)

	return results


def parser_common_cmd(text, cmd):
	# 根据指令类别读取配置文件
	file = 'format/format' + cmd + '.txt'
	labels, lens = read_format(file)

	# 按字段长度解析内容
	break_res = parser_break(text, lens)
	fields = [' '.join(a) for a in break_res]

	# 打印解析结果
	print('解析结果：')
	try:
		for label, alen, field in zip(labels, lens, fields):
			# if(alen!=0): # 只输出长度不为0的字段
			if True:  # 全部输出
				print("{label:.<{width}}{field}".format(label=label, field=field,
				                                        width=16 - len(label.encode('GBK')) + len(label)))  # 为了输出对齐
	except:
		print('失败')

	return labels, lens, fields


if __name__ == '__main__':
	while True:
		# 获取待解析内容
		text = input('待解析内容：')

		# 获取指令类别
		cmd = get_cmd(text)
		if cmd is None:
			# 无指令类别，要求手动输入
			cmd = input('指令类别：')

		parser_common_cmd(text, cmd)
		print('')
