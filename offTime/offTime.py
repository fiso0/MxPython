#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
# import pprint


def pickle_dump(data):
	p_f = open('data.pkl', 'wb')
	pickle.dump(data, p_f)
	p_f.close()


def pickle_load():
	p_f = open('data.pkl', 'rb')
	data = pickle.load(p_f)
	p_f.close()
	# pprint.pprint(data)
	return data


def calc():
	# 读取记录
	old_data = pickle_load()
	print('上次输入：%s' % old_data.get('inp'))
	print("offset=%d" % old_data.get('offset'))
	print("下班时间：%s\n" % old_data.get('result'))

	# 本次计算
	print('标准时间：08:30 ~ 17:30')
	inp = input('富余值（分钟）：')
	offset = int(eval(inp))
	print("offset=%d" % offset)
	normalTime = '17:30'
	h, m = normalTime.split(':')
	offTime = 60 * int(h) + int(m) - offset
	h, m = int(offTime / 60), offTime % 60
	result = '%d:%02d' % (h, m)
	print("下班时间：%s\n" % result)

	# 保存记录
	data = {'inp': inp,
	        'offset': offset,
	        'result': result}
	pickle_dump(data)


if __name__ == '__main__':
	while True:
		try:
			calc()
			input('==计算完毕==\n') # 暂停
		except Exception as e:
			print(e)
