#!/usr/bin/python3
# -*- coding: utf-8 -*-

from psl_module import *
import sys
import re

RS_KEY_WORDS = ['mx_srv_send_handle', 'mxapp_srv_ind']

# 搜索RS_KEY_WORDS，并保存csv结果到log文件同目录下
def RS_result_csv():
	(res_time, res, time) = ORt(RS_KEY_WORDS, save=False)

	result_mix = []
	for line in res_time:
		text = log[line]
		if line in res:
			if(RS_KEY_WORDS[0] in text):
				# send
				t = text.split(':')
				result_mix.append(['send', t[1]])
			elif(RS_KEY_WORDS[1] in text):
				# receive
				ptn = re.compile(r'read \d* (.*)')
				re_res = ptn.search(text)
				if re_res:
					result_mix.append(['receive', re_res.group(1)])
		elif line in time:
			# time
			t = text.split(',')
			result_mix.append(['time', t[1]])

	csv_file_name = new_file_name('+'.join(RS_KEY_WORDS) + '_t', 'csv')
	save_to_csv(csv_file_name, result_mix)


if __name__ == '__main__':
	# 程序开始
	log = open_file()
	# 搜索关键字并保存结果
	RS_result_csv()
	sys.exit(0)