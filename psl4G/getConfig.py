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
		dd[d[k]['name']] = d[k]['keywords'].split(',')

	return dd

if __name__ == '__main__':
	get_config()
	input()