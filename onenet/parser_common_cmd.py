#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser_4005

'''
根据配置解析协议
	允许仅参数部分
	允许带空格
	大小写均可
配置示例：format.txt
	消息头	18
	消息ID	2
	数据标识符长度	1
	数据量标识符	-1
	数据类型	1
	信号强度	1
	电量	1
	GPS定位时间	6
	经度	5
	纬度	5
	经纬度标志	1
	高度	3
	经度理论解精度	2
	纬度理论解精度	2
	高度理论解精度	2
	定位状态	1
	解状态	1
	差分龄	2
	位置因子	2
	GPS平均CNO	1
	GPS卫星数	1
	BDS平均CNO	1
	BDS卫星数	1
	速度	2
	方向	1
	附近wifi数据	-2
	附近基站数据	-2
	流水号	2
	校验码	1
配置说明：
	每行为一个字段（每行必须至少2个字符串，取前两项）
	第一项是字段名
	第二项是字段长度
		>0表示长度
		0表示该字段跳过
		-1表示长度由前一个字段决定
		-2表示该字段以0xFF（包含）结束
		-3表示该字段到最后（流水号之前）结束
'''

DEFAULT_FORMAT_FILE = 'format.txt'

def read_format(f):
	'''
	读取配置文件
	若文件不存在，改读取默认配置文件DEFAULT_FORMAT_FILE
	若读取失败，返回None,None
	:return: 字段名（列表），字段长度（列表）
	'''
	labels = []
	lens = []
	try:
		print('读取配置文件：'+f)
		with open(f, encoding='utf-8') as file:
			for line in file.readlines():
				try:
					label,len = (line.strip().split())[:2] # 每行必须至少2个字符串，取前两项
					labels.append(label)
					lens.append(int(len))
				except Exception as e:
					# print(e)
					pass
		return labels,lens
	except FileNotFoundError:
		# 未找到配置文件，改用默认配置文件
		if(f != DEFAULT_FORMAT_FILE):
			return read_format(DEFAULT_FORMAT_FILE)
		else:
			print('无法读取默认配置文件：'+DEFAULT_FORMAT_FILE)
			return None,None
	except Exception as e:
		print(e)
		return None,None

def get_cmd(text):
	if(text == ''):
		text = '262626260041000000000866888a2a556172400703ffff800d606412081c09050c72173f11211e1e20095f110033e6006e00a001040302000401280000000000004dffff0004bd'
		print('使用示例内容：'+text)
	text = text.strip().replace(' ', '').upper()  # 去掉空格 转为大写

	# 尝试解析指令类别
	if(text[:8] == '26262626'):
		try:
			cmd = text[36:40]
		except:
			cmd = ''
			print('尝试解析指令类别失败，将使用默认指令类别')
	else:
		# 不包含指令头，无指令类别，要求手动输入
		cmd = None
	return cmd

def parser_common(text,cmd):
	# 根据指令类别读取配置文件
	file = 'format'+cmd+'.txt'
	labels,lens = read_format(file)

	# 若没有消息头，仅参数部分，则修改字段长度，跳过相应字段
	if(text[:8] != '26262626'):
		print('仅参数部分，将跳过相应字段')
		lens[0]=0 # 帧头
		lens[1]=0 # 长度
		lens[2]=0 # 终端ID
		lens[3]=0 # 指令类别
		lens[-2]=0 # 流水号
		lens[-1]=0 # 校验码

	# 按字段长度解析内容
	break_res = parser_4005.parser_break(text, lens)
	fields = [' '.join(a) for a in break_res]

	# 打印解析结果
	print('解析结果：')
	try:
		for label,alen,field in zip(labels,lens,fields):
			if(alen!=0): # 只输出长度不为0的字段
				print("{label:.<{width}}{field}".format(label=label, field=field, width=16-len(label.encode('GBK'))+len(label))) # 为了输出对齐
	except:
		print('失败')

	return zip(labels,lens,fields)


if __name__=='__main__':
	while(True):
		# 获取待解析内容
		text = input('待解析内容：')

		# 获取指令类别
		cmd = get_cmd(text)
		if cmd == None:
			# 无指令类别，要求手动输入
			cmd = input('指令类别：')

		parser_common(text,cmd)
		print('')
