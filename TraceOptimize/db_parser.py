#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Point import *


def parser(file):
	"""
	解析数据库文件，得到点列表
	:param file: 待解析的数据库导出文件（txt格式，文本限定符选择无，日期排序为默认DYM）
	:return: 返回解析得到的所有点列表，包含经度、纬度、时间信息
	"""
	points = []
	with open(file) as f:
		for line in f.readlines():
			data = line.split("\t")
			lat = float(data[5])  # latitude
			lon = float(data[4])  # longitude
			# time = data[2]  # create_time
			time = data[17]  # base_time
			point = Point(lat, lon, time)
			points.append(point)
	return points
