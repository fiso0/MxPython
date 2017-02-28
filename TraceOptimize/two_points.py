#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
两点相关函数：
计算两点距离
计算两时间差
计算两点间速度
'''

import math
import time

EARTH_RADIUS = 6378137  # meters


def calc_distance(lat1, lon1, lat2, lon2):
	"""
	计算两点距离
	:param lat1: 点1的纬度
	:param lon1: 点1的经度
	:param lat2: 点2的纬度
	:param lon2: 点2的经度
	:return: 两点距离，单位为米
	"""
	radLat1 = math.radians(lat1)
	radLat2 = math.radians(lat2)
	a = radLat1 - radLat2
	b = math.radians(lon1) - math.radians(lon2)

	s = 2 * math.asin(math.sqrt((math.sinh(a / 2) * math.sin(a / 2)) + math.cos(radLat1) * math.cos(radLat2) * (
		math.sin(b / 2) * math.sin(b / 2))))
	s *= EARTH_RADIUS
	return s  # meters


def calc_time(time_start, time_end):  # 19 2017 01 00:00:02
	"""
	计算两时间间隔
	:param time_start: 起始时间，格式为“日 年 月 时:分:秒”
	:param time_end: 终止时间，格式为“日 年 月 时:分:秒”
	:return: 时间差，单位为秒
	"""
	time1_t = time.strptime(time_start, "%d %Y %m %H:%M:%S")
	time2_t = time.strptime(time_end, "%d %Y %m %H:%M:%S")
	time1_s = time.mktime(time1_t)
	time2_s = time.mktime(time2_t)
	return int(time2_s - time1_s)  # seconds


def calc_speed(point_start, point_end):
	distance = calc_distance(point_start.lat, point_start.lon, point_end.lat, point_end.lon)
	duration = calc_time(point_start.time, point_end.time)
	if duration is not 0:
		return distance / duration  # meters/seconds
	else:
		return 0
