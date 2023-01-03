#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


"""
根据配置解析协议
	允许仅参数部分
	允许带空格
	大小写均可
配置示例：format.txt
配置说明参见：格式说明.txt
"""

DEFAULT_FORMAT_JTT = 'JTT'
DEFAULT_FORMAT_OneNet = 'OneNet'
DEFAULT_FORMAT = ''


def read_format(cmd):
	"""
	读取配置文件
	若文件不存在，改读取默认配置文件DEFAULT_FORMAT_FILE
	若读取失败，返回None,None
	:return: 字段名（列表），字段长度（列表）
	"""
	if cmd is None:
		cmd = ''
	f = 'format/format' + cmd + '.txt'
	labels = []
	lens = []
	try:
		print('读取配置文件：' + f)
		with open(f, encoding='utf-8') as file:
			for line in file.readlines():
				if(len(line) > 1):
					try:
						label, length = (line.strip().split())[:2]  # 每行必须至少2个字符串，取前两项
						labels.append(label)
						lens.append(length)
					except Exception as e:
						print(e)
						# print(len(line))
		return labels, lens, cmd
	except FileNotFoundError:
		# 未找到配置文件，改用默认配置文件
		if 'OneNet' in f:
			default_file = DEFAULT_FORMAT_OneNet
		elif 'JTT' in f:
			default_file = DEFAULT_FORMAT_JTT
		else:
			default_file = DEFAULT_FORMAT
		if f != default_file:
			return read_format(default_file)
		else:
			print('无法读取默认配置文件：' + default_file)
			return None, None, None
	except Exception as e:
		print(e)
		return None, None, None


def get_cmd(text):
	# if text == '':
	# 	text = '28F5C180ED2540FFF5EB0057C30D62CA1F2920003FE200F0'
	# 	print('使用示例内容：' + text)
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
	elif text.startswith('D3'):  # RTCM指令头
		try:
			cmd = str(int(text[6:9],16))
		except:
			cmd = ''
			print('尝试解析指令类别失败，将使用默认指令类别')
	else:
		# 不包含指令头，无指令类别，要求手动输入
		cmd = None
	return cmd


def parser_break(msg, types):
	# 根据lens分解msg
	results = []

	message = msg.strip().replace(' ', '').upper()  # 去掉空格 转为大写
	chrstr = [message[i:i + 2] for i in range(0, len(message), 2)] # 每2个字符分割为一列数组
	formatter = '0%db' % (len(message)*4)
	msg_bin = format(int(message, 16), formatter) # 将十六进制字符串转为二进制字符串

	i = 0
	rd_len = 0
	len_sum = sum([int(type[1:]) for type in types])
	msg_len_bits = len(message)*4
	for type in types:
		type_format = type[0] # i-有符号数 u-无符号数 b-二进制
		type_len = int(type[1:])
		if type_len == 0: # 长度为0 需自适应
			type_len = msg_len_bits - len_sum
		# res = []
		try:
			msg_num = msg_bin[rd_len:rd_len+type_len]
			if type_format == 'b': # 二进制数据
				res = msg_num
				results.append('0b'+res)
			elif type_format == 'h': # 十六进制数据
				formatter = '0%dX' % (len(msg_num)/4)
				res = format(int(msg_num, 2), formatter) # 将二进制字符串转为十六进制字符串
				results.append('0x'+res)
			elif type_format == 'u' or type_format == 'i': # 有/无符号数
				res = int(msg_num,2)
				# 有符号数处理
				if type_format == 'i' and msg_num[0] == '1':
					res = res - (1 << type_len)
				results.append('%d' % res)
			elif type_format == 'a': # ASCII
				import  binascii
				formatter = '0%dX' % (len(msg_num) / 4)
				msg_num = format(int(msg_num, 2), formatter)  # 将二进制字符串转为十六进制字符串
				res = binascii.a2b_hex(msg_num).decode('ascii')
				results.append(res)
			else: # 默认按二进制数据处理
				res = msg_num
				results.append('0b'+res)
		except Exception as e:
			print(e)
			# res = ''
			# type = 0

		i += 1
		rd_len += type_len
		# results.append('%d' % res)

	return results


def parser_common_cmd(text, cmd = None):
	"""
	根据给定格式解析
	:param text:
	:param cmd:
	:return:
	"""
	if cmd is None:
		# 获取指令格式
		cmd = get_cmd(text)
		# if cmd is None:
			# print('获取指令格式失败')
			# return None, None, None, None

	# 根据指令格式读取配置文件
	labels, lens, format = read_format(cmd)

	labels_len_max = max([len(label) for label in labels])

	# 按format格式配置文件指定的字段长度解析内容
	break_res = parser_break(text, lens)
	fields = break_res # ['%d' % a for a in break_res]

	# 打印解析结果
	print('解析结果：')
	try:
		for label, alen, field in zip(labels, lens, fields):
			# if(alen!=0): # 只输出长度不为0的字段
			label = label + '(' + alen + ')'
			if True:  # 全部输出
				print("{label:.<{width}}{field}".format(label=label, field=field,
				                                        width=labels_len_max*2+8 - len(label.encode('GBK')) + len(label)))  # 为了输出对齐
	except:
		print('失败')

	return labels, lens, fields, format


if __name__ == '__main__':
	while True:
		# 获取待解析内容
		text = input('待解析内容：')

		if text == '':
			text = '28F5C180ED2540FFF5EB0057C30D62CA1F2920003FE200F0'
			print('使用示例内容：' + text)

		# 获取指令类别
		cmd = get_cmd(text)
		if cmd is None:
			# 无指令类别，要求手动输入
			cmd = input('指令类别：')

		parser_common_cmd(text, cmd)
		# parser_common_cmd(text)
		print('')
