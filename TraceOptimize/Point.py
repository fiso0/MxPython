#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Point:
	def __init__(self, lat=0, lon=0, time="1999-11-30 00:00:00", note=''):
		self.lat = lat  # 纬度
		self.lon = lon  # 经度
		self.time = time  # 时间，一般取数据库中的基站时间
		self.note = note  # 备注信息

def points_parser(text):
	'''
	解析经纬度数据，每行一组经纬度，纬度lat在前，以空格、逗号或制表符分隔
	解析结果构成Point对象，放入列表
	:param text: 经纬度数据
	:return: Point列表
	'''
	points = []
	textLines = text.split('\n')
	for line in textLines:
		if ',' in line:
			lat,lon = line.strip().split(',')
			points.append(Point(lat,lon))
		elif '\t' in line:
			lat,lon = line.strip().split('\t')
			points.append(Point(lat,lon))
		elif ' ' in line:
			lat,lon = line.strip().split(' ')
			points.append(Point(lat,lon))
		elif line == '':
			print('empty line found')
		else:
			print('unknown split found')
			return None
	return points