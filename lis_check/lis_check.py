#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import pprint


# find_cur(string, path)实现对path目录下文件的查找，列出文件命中含string的文件
def find_cur(string, path):
	# print('cur_dir is %s' % os.path.abspath(path))
	l = []

	# 遍历当前文件，找出符合要求的文件，将路径添加到l中
	for x in os.listdir(path):
		if os.path.isfile(path + '/' + x):
			if string in x:
				l.append(os.path.abspath(x))
	if not l:
		print('no %s in %s' % (string, os.path.abspath(path)))
	else:
		print(l)

	return l


# deeper_dir(string, p)主要通过递归，在每个子目录中调用find_cur()
def deeper_dir(string='', p='..'):  # '.'表示当前路径，'..'表示当前路径的父目录
	find_cur(string, p)
	for x in os.listdir(p):
		# 关键，将父目录的路径保留下来，保证在完成子目录的查找之后能够返回继续遍历。
		pp = p
		if os.path.isdir(pp):
			pp = os.path.join(pp, x)
			if os.path.isdir(pp):
				deeper_dir(string, pp)


# 在文件file中查找所有***.obj，返回集合（所有.obj去重的结果）
def find_obj(file):
	s = []
	for line in file.readlines():
		strings = re.split(r'[^A-Za-z0-9_.]',line)
		#strings = line.strip().split(' ')
		for string in strings:
			if(string.endswith('.obj')):
				s.append(string)
	return set(s)


# 在文件file中查找所有***.lib，返回集合（所有.obj去重的结果）
def find_lib(file):
	s = []
	for line in file.readlines():
		strings = re.split(r'[^A-Za-z0-9_.]',line)
		#strings = line.strip().split(' ')
		for string in strings:
			if(string.endswith('.lib')):
				s.append(string)
	return set(s)


if __name__ == '__main__':
	f_name = find_cur('.lis', '.')
	if(len(f_name) > 0):
		f_name = f_name[0]
	f = open(f_name, 'r')

	obj = find_obj(f)
	pprint.pprint(obj)
	print('Total .obj: '+str(len(obj)))

	input()