#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
轨迹优化算法模拟程序
过滤参数为：K_avg和K_max（预设为10和5）
数据库导出文本文件为：DB_FILE
'''

import two_points as tp
# from Point import *
import db_parser as db
import logging
import sys

logging_lv = input("是否需要细节log（Y/N）：")
if logging_lv == 'Y' or logging_lv == 'y':
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(level=logging.INFO)  # 改为logging.DEBUG可以看到更多细节

# 过滤参数
K_avg = 10  # guess 10
K_max = 5  # guess 5

# 数据库导出文本文件
# DB_FILE = "WiFi转换结果异常_0116_part.txt"
# DB_FILE = "866888020241213_0114.txt"
# DB_FILE = "866888020240835_0120_单偏点.txt"
# DB_FILE = "866888020237229_0119-0120_单偏点.txt"
# DB_FILE = "866888020237294_0119-0120_单偏点.txt"
DB_FILE = "29_0213.txt"
file = input("待分析数据库文件：")

# 以下为测试使用
# print(tp.calc_distance(35, 114, 36, 115))  # lat1,lon1,lat2,lon2
# print(tp.calc_time("18 2017 01 23:59:01", "19 2017 01 00:00:02"))  # time_start, time_end
#
# p1 = Point(35,114,"18 2017 01 23:59:01")
# p2 = Point(36,115,"19 2017 01 00:00:02")
# print(tp.calc_speed(p1, p2))

def data_statics(key):
	"""
	检查第key个点是否为偏点
	:param key: 关键点序号（第几个点，从1开始数）
	:return bias: 是否偏点（使用过滤方法A）
	:return Q_avg: 得到此偏点结果，K_avg可取的最大值
	:return Q_max: 得到此偏点结果，K_max可取的最大值
	"""
	logging.info('检查第%d个点（%s）>>>' % (key,points[key].time))

	# 速度取绝对值
	speeds_abs = [abs(s) for s in speeds]
	logging.debug('speeds_abs:')
	logging.debug(speeds_abs)

	# 关键点的前后速度
	S1 = speeds_abs[key - 2]
	S2 = speeds_abs[key - 1]
	logging.debug('S1=%.4f S2=%.4f' % (S1, S2))

	# 除关键点前后以外其他的速度（最多取前2个+后2个）
	if key > 4:
		speeds_front = speeds_abs[(key - 4):(key - 2)]
	else:
		speeds_front = speeds_abs[0:(key - 2)]
	if key < N - 3:
		speeds_rear = speeds_abs[key:(key + 2)]
	else:
		speeds_rear = speeds_abs[key:]
	speeds_others = speeds_front + speeds_rear
	logging.debug('speeds_others:')
	logging.debug(speeds_others)

	# 其他点速度的均值、最大值
	try:
		S_avg = sum(speeds_others) / len(speeds_others)
	except ZeroDivisionError:
		logging.error('Not enough data!')
		sys.exit(1)
	S_max = max(speeds_others)
	logging.debug('S_avg=%.4f S_max=%.4f' % (S_avg, S_max))

	# 过滤参数
	STOP_avg = S_avg * K_avg
	STOP_max = S_max * K_max
	logging.debug('K_avg=%d K_max=%d STOP_avg=%.4f STOP_max=%.4f' % (K_avg, K_max, STOP_avg, STOP_max))

	# 参数范围
	Q_avg = min(S1 / S_avg, S2 / S_avg)
	Q_max = min(S1 / S_max, S2 / S_max)
	logging.info("Q_avg=%d Q_max=%d" % (Q_avg, Q_max))

	# filter A
	if S1 > STOP_avg and S1 > STOP_max and S2 > STOP_avg and S2 > STOP_max:
		logging.info('>>>【A】偏！！！！！')
		if_bias = True
	else:
		logging.info('>>>【A】不偏')
		if_bias = False

	# filter B
	if (S1 > STOP_avg or S1 > STOP_max) and (S2 > STOP_avg or S2 > STOP_max):
		logging.debug('>>>【B】偏')
	else:
		logging.debug('>>>【B】不偏')

	# filter C
	if (S1 > STOP_avg and S1 > STOP_max) or (S2 > STOP_avg and S2 > STOP_max):
		logging.debug('>>>【C】偏')
	else:
		logging.debug('>>>【C】不偏')

	# filter D
	if (S1 > STOP_avg or S1 > STOP_max) or (S2 > STOP_avg or S2 > STOP_max):
		logging.debug('>>>【D】偏')
	else:
		logging.debug('>>>【D】不偏')

	return if_bias, Q_avg, Q_max


def delete_point(n):
	logging.info('！！！！！删除原第%d个点！！！！！' % n)

	del points[n - 1]  # 删除第n个点
	del speeds[n - 1]  # 删除第n个速度
	del speeds[n - 2]  # 删除第n-1个速度

	speed_new = tp.calc_speed(points[n - 2], points[n - 1])  # 计算第n-1个点和第n个点（新）之间的速度
	speeds.insert(n - 2, speed_new)


# 以下为执行部分

# 读取数据
# points = db.parser(DB_FILE)
points = db.parser(file)
N = len(points)

# 计算速度
speeds = []
for i in range(N - 1):
	speed = tp.calc_speed(points[i], points[i + 1])
	speeds.append(speed)
logging.debug('speeds:')
logging.debug(speeds)

i = 2  # 从第二个点开始检查 实际为数据文件中的第3个点（下标i从0开始）
bias_points = []  # 记录偏点
Q_rec = []
while True:
	N = len(points)
	if i >= N:
		break  # 到倒数第二个点结束
	bias, Q1, Q2 = data_statics(i)  # 检查第i个点是否偏点
	Q_rec.append((i, int(Q1), int(Q2)))
	if bias: # 当前点偏，记录并删除，然后重新检查前面的点
		bias_points.append(points[i - 1])  # 记录偏点
		delete_point(i)  # 删除第i个点并重新整理速度列表结果
		if i >= 5:
			i -= 3  # 重新检查第i-3个点
		else:
			i = 2
	else: # 当前点不偏，检查下一个点
		i += 1

# 打印所有不全为0的Q值
logging.info('=============\n所有不全为0的Q值:')
for i in range(len(Q_rec)):
	if (Q_rec[i][1] >= 1) or (Q_rec[i][2] >= 1):
		logging.info('%d %d %d' % (Q_rec[i][0], Q_rec[i][1], Q_rec[i][2]))

# 打印所有偏点的信息
if len(bias_points):
	logging.info('=============\n所有偏点:')
	for p in bias_points:
		logging.info('>>>base_time=%s, lat=%f, lon=%f' % (p.time, p.lat, p.lon))
else:
	logging.info('=============\n无偏点')

logging.info('完毕')
input('按回车结束，关闭窗口')
