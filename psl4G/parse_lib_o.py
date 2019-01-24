#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Parser(object):
	def __init__(self, filename):
		self.filename = filename # log文件名
		self.log = [] # log内容
		self.lines = 0 # log总行数
		self.config = None # 功能关键词配置

		self.__log_level_line_dicts = dict() # 按log级别分类保存行号
		self.__log_mod_line_dicts = dict() # 按log模块分类保存行号
		self.__log_function_line_dicts = dict() # 按log功能分类保存行号

		self.__open_file(filename)


	def __open_file(self, file):
		'''
		打开log文件，解析得到log内容（列表），得到log行数
		:param file: log文件名
		:return: log内容
		'''
		with open(file, 'r', encoding='utf-8', errors='ignore') as f:
			for line in f.readlines():
				self.log.append(line)
		self.lines = len(self.log)
		return self.log  # string list


	def parse_log_level(self, line_no):
		'''
		判断该行log属于哪种级别，同时按级别分别记录行号
		:param line_no: 行号
		:return: log级别
		'''
		ptn = r'\|\S*\|(\S*)>'
		try:
			level_name = re.search(ptn, self.log[line_no]).group(1)
			line_list = self.__log_level_line_dicts.get(level_name, [])
			line_list.append(line_no)
			self.__log_level_line_dicts[level_name] = line_list
		except:
			level_name = ''
		return level_name

	def parse_log_mod(self, line_no):
		"""
		判断该行log所属的模块，同时按模块分别记录行号
		:param line_no: 行号
		:return: log模块
		"""
		ptn = r'> (\S*)'
		try:
			mod_name = re.search(ptn, self.log[line_no]).group(1)  # try to find mod_name
			line_list = self.__log_mod_line_dicts.get(mod_name, [])  # get line list
			line_list.append(line_no)  # update line lists
			self.__log_mod_line_dicts[mod_name] = line_list  # set line list
		except:
			mod_name = ''
		return mod_name

	def parse_log_func(self, line_no, key_words, log_name):
		'''
		查找该行内是否包含关键词内容（任一即可），包含则将该行号记录到log_function_line_dicts[log_name]中
		:param line_no:行号
		:param key_words:关键词
		:param log_name:字典索引
		:return: log是否包含关键词
		'''
		line_list = self.__log_function_line_dicts.get(log_name, [])
		try:
			for key in key_words:
				if key in self.log[line_no]:
					line_list.append(line_no)
					self.__log_function_line_dicts[log_name] = line_list
					return True
		except:
			return False

	def parse_log_all_func(self, line_no):
		'''
		读取配置文件，得到所有预置功能关键词，按照功能关键词条件解析该行log
		:param line_no: 行号
		:return: 无
		'''
		import getConfig
		self.config = getConfig.get_config()

		for log_name in self.config:
			key_words = self.config[log_name]
			self.parse_log_func(line_no, key_words, log_name)


	def get_levels(self):
		return self.__log_level_line_dicts

	def get_mods(self):
		return self.__log_mod_line_dicts

	def get_funcs(self):
		return self.__log_function_line_dicts

if __name__ == '__main__':
	input()