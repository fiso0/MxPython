#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time
from datetime import datetime


# GNGGA,000003.000,0000.000000,N,00000.000000,E,,00,0.000,0.000,M,0,M,,
# GNGGA,105548.270,0000.000000,N,00000.000000,E,,00,0.000,0.000,M,0,M,,
# GNGGA,105554.020,3030.317770,N,11423.652197,E,1,05,2.312,86.655,M,0,M,,


class GGA(object):
	# 选择经纬度模拟方式：单点测试或线路测试
	TEST_MODE = 'POINT_TEST'  # 'ROUTE_TEST'
	LAT_DEFAULT = 3030.318596
	LON_DEFAULT = 11423.636076

	index = 0  # 所有GGA实例共同的序号
	now = None

	def __init__(self, quality=''):  # 初始化时传入有效标识值，不传默认为空
		GGA.index += 1  # 每次产生一个GGA实例，序号加1

		self.header = 'GNGGA'
		self.time = '000001.000'
		self.lat = '0000.000000'
		self.N_S = 'N'
		self.lon = '00000.000000'
		self.E_W = 'E'
		self.quality = quality
		self.num = '00'
		self.HDOP = '0.000'
		self.alt = '0.000'
		self.altUnit = 'M'
		self.geoid = '0'
		self.geoidUnit = 'M'
		self.age = ''
		self.diffID = ''

		if quality is not '':
			self.set_pos()

		self.set_time()

		print(self.gen())

	def set_time(self):
		if self.quality is '' and GGA.now is None:
			second = GGA.index % 60
			minute = int(GGA.index / 60) % 60
			hour = int(GGA.index / 3600)
		else:
			GGA.now = datetime.now()
			hour = GGA.now.hour
			minute = GGA.now.minute
			second = GGA.now.second
		self.time = '%02d%02d%02d.000' % (hour, minute, second)
		return

	def set_pos(self):
		lat_offset = 0
		lon_offset = 0
		if self.TEST_MODE is 'POINT_TEST':
			OFFSET = 0.001  # 0.001'
			lat_offset = OFFSET * random.uniform(-1, 1)
			lon_offset = OFFSET * random.uniform(-1, 1)
		elif self.TEST_MODE is 'ROUTE_TEST':
			OFFSET = 0.01
			lat_offset = 0.1 * GGA.index + OFFSET * random.uniform(-1, 1)
			lon_offset = 0.1 * GGA.index + OFFSET * random.uniform(-1, 1)
		lat = self.LAT_DEFAULT + lat_offset
		lon = self.LON_DEFAULT + lon_offset
		self.lat = '%010.6f' % lat
		self.lon = '%011.6f' % lon
		return

	def checksum(self,data):
		CS = 0
		for a in data:
			CS ^= ord(a)
		return '%02X' % CS

	def gen(self):
		wo_cs = ','.join([self.header, self.time, self.lat, self.N_S, self.lon, self.E_W, self.quality,self.num, self.HDOP,self.alt, self.altUnit, self.geoid, self.geoidUnit, self.age, self.diffID])
		cs = self.checksum(wo_cs)
		return '$'+wo_cs+'*'+cs


def save(lines,name=''):
	OUTPUT_FILE = 'GGAgen_output'+name+'.log'
	try:
		f = open(OUTPUT_FILE, 'x')  # create
	except FileExistsError:
		f = open(OUTPUT_FILE, 'w')  # rewrite
	finally:
		for line in lines:
			f.write(line)
			f.write('\n')
		f.close()


# GGA语句列表默认以0无效语句开始，参数表示每组连续无效/有效语句的个数
# 示例：'0,1,1,10'表示0个无效、1个有效、1个无效、10个有效GGA
def parse_cmd(cmd='10,1,1,10'):
	cmd_list = cmd.strip().split(',')
	# while cmd_list[-1] is not '0':
	# 	cmd = input('最后以0结束,重新输入：')
	# 	cmd_list = cmd.strip().split(',')
	return cmd_list


# 命令模式
def cmd_mode():
	cmd = input('请输入每组无效/有效/无效...GGA的个数，以逗号分隔：')
	cmd_num = parse_cmd(cmd)
	valid = False
	gga = []
	for num in cmd_num:
		num = int(num)
		if valid:
			quality = '1'
		else:
			quality = ''
		for i in range(0, num):
			gga.append(GGA(quality).gen())
			time.sleep(1)
		valid = not valid
	save(gga,cmd)


# 手动模式
def man_mode():
	gga = []
	for i in range(1, 3):
		gga.append(GGA().gen())
		time.sleep(1)
	for i in range(1, 3):
		gga.append(GGA('1').gen())
		time.sleep(1)
	save(gga)


# GGA()
# GGA().checksum('GNGGA,000000.000,0000.000000,N,00000.000000,E,,00,0.000,0.000,M,0,M,,')
cmd_mode()
# man_mode()
input('=== Finished ===\n')

# print(gga)
