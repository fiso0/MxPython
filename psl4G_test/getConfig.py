#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser

def get_config():
	cf = configparser.ConfigParser()
	cf.read('config.ini', 'utf-8')

	# reformat 1
	d = dict(cf._sections)
	for k in d:
		d[k] = dict(d[k])

	# reformat 2
	dd = dict()
	for k in d:
		try:
			dd[d[k]['name']] = list(eval(d[k]['keywords'])) # for example: dd['GNSS'] = '[GPS]'.split(',')
		except:
			dd[d[k]['name']] = [d[k]['keywords']]

	return dd

if __name__ == '__main__':
	get_config()
	input()