#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parser_4005
import alignPrint

'''
根据配置解析协议
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
		-2表示该字段以0xFF结束
'''

FORMAT_FILE = 'format.txt'

def read_format():
	'''
	读取配置文件
	:return: 字段名（列表），字段长度（列表）
	'''
	labels = []
	lens = []
	try:
		with open(FORMAT_FILE, encoding='utf-8') as file:
			for line in file.readlines():
				label,len = (line.strip().split())[:2] # 每行必须至少2个字符串，取前两项
				labels.append(label)
				lens.append(int(len))
		return labels,lens
	except Exception as e:
		print(e)
		return None

def main():
	# 读取配置文件
	labels,lens = read_format()

	# 获取待解析内容
	text = input('待解析内容：')
	if(len(text)==0):
		text = '262626260041000000000866888a2a556172400703ffff800d606412081c09050c72173f11211e1e20095f110033e6006e00a001040302000401280000000000004dffff0004bd'

	# 自动判断是否仅参数部分：没有消息头，仅参数部分，修改字段长度，跳过部分字段
	if(text[:8]!='26262626'):
		lens[0]=0 # 帧头
		lens[1]=0 # 长度
		lens[2]=0 # 终端ID
		lens[3]=0 # 指令类别
		lens[-2]=0 # 流水号
		lens[-1]=0 # 校验码

	# 按字段长度解析内容
	break_res = parser_4005.parser_break(text, lens)
	fields = [' '.join(a) for a in break_res]

	# 打印结果
	for label,alen,field in zip(labels,lens,fields):
		if(alen!=0): # 只输出长度不为0的字段
			print("{l:<{width}}\t{f}".format(l=label, f=field, width=16 - len(label.encode('GBK')) + len(label))) # 为了输出对齐


if __name__=='__main__':
	main()