#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser

def get_config():
	'''
	读取配置文件config.ini
	:return:配置内容（字典）
	'''
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

	
import re

class Parser(object):
	'''
	解析器类
	'''
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
			self.log = f.readlines()
		self.lines = len(self.log)

		# 读取配置文件，得到所有预置功能关键词
		self.config = get_config()

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

	def parse_log_func(self, line_no, key_words, log_name, method='and'):
		'''
		查找该行内是否包含关键词内容，包含则将该行号记录到log_function_line_dicts[log_name]中
		:param line_no:行号
		:param key_words:关键词
		:param log_name:字典索引
		:param method:默认'or'按或进行搜索，若为'and'则按与进行搜索
		:return: log是否包含关键词
		'''
		line_list = self.__log_function_line_dicts.get(log_name, [])
		try:
			for key in key_words:
				if method == 'or':
					if key in self.log[line_no]:
						line_list.append(line_no)
						self.__log_function_line_dicts[log_name] = line_list
						return True
				elif method == 'and':
					if key not in self.log[line_no]:
						return False
			if method == 'or': # 到这里说明所有关键词都无
				return False
			elif method == 'and': # 到这里说明所有关键词都有
				line_list.append(line_no)
				self.__log_function_line_dicts[log_name] = line_list
				return True
		except Exception as e:
			print(e)
			return False

	def parse_log_all_func(self, line_no):
		'''
		按照功能关键词条件解析该行log
		:param line_no: 行号
		:return: 无
		'''
		for log_name in self.config:
			key_words = self.config[log_name]
			self.parse_log_func(line_no, key_words, log_name)


	def get_levels(self):
		return self.__log_level_line_dicts

	def get_mods(self):
		return self.__log_mod_line_dicts

	def get_funcs(self):
		return self.__log_function_line_dicts

	def get_log_lines(self, log_type):
		"""
		获取所有指定log类型的log行号
		:param log_type: log类型（级别或模块或功能）
		:return: log行号列表
		"""
		if log_type in self.__log_level_line_dicts.keys():
			return self.__log_level_line_dicts.get(log_type)
		elif log_type in self.__log_mod_line_dicts.keys():
			return self.__log_mod_line_dicts.get(log_type)
		elif log_type in self.__log_function_line_dicts.keys():
			return self.__log_function_line_dicts.get(log_type)
		else:
			print('输入参数有误！')
			return []

			
import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QButtonGroup, QRadioButton, \
	QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import time

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		mainBox = QVBoxLayout()
		fileBox = QHBoxLayout()
		menuBox = QHBoxLayout()
		resBox = QHBoxLayout()
		self.outEdit = QTextEdit()
		toolBox = QVBoxLayout()
		searchBox = QHBoxLayout()
		searchResBox = QVBoxLayout()
		searchInputBox = QHBoxLayout()
		searchToolBox = QVBoxLayout()

		mainBox.addLayout(fileBox)
		mainBox.addLayout(menuBox)
		mainBox.addLayout(resBox)
		mainBox.addLayout(searchBox)
		resBox.addWidget(self.outEdit)
		resBox.addLayout(toolBox)
		searchBox.addLayout(searchResBox)
		searchResBox.addLayout(searchInputBox)
		searchBox.addLayout(searchToolBox)

		openFileBtn = QPushButton('1.选择文件')
		self.fileNameEdit = QLineEdit()
		parseFileBtn = QPushButton('2.开始解析')
		fileBox.addWidget(openFileBtn)
		fileBox.addWidget(self.fileNameEdit)
		fileBox.addWidget(parseFileBtn)

		label1 = QLabel('3.筛选：')
		levelLabel = QLabel('log级别')
		self.levelCombo = QComboBox()
		self.levelCombo.setMinimumWidth(100)
		modLabel = QLabel('log模块')
		self.modCombo = QComboBox()
		self.modCombo.setMinimumWidth(100)
		funLabel = QLabel('功能')
		self.funCombo = QComboBox()
		self.funCombo.setMinimumWidth(100)
		menuBox.addWidget(label1)
		menuBox.addWidget(levelLabel)
		menuBox.addWidget(self.levelCombo)
		menuBox.addSpacing(15)
		menuBox.addWidget(modLabel)
		menuBox.addWidget(self.modCombo)
		menuBox.addSpacing(15)
		menuBox.addWidget(funLabel)
		menuBox.addWidget(self.funCombo)
		menuBox.addStretch()

		toolBtn1 = QPushButton('复制')
		toolBtn2 = QPushButton('保存')
		# toolBtn3 = QPushButton('')
		# toolBtn4 = QPushButton('')
		self.statusLabel = QLabel('')
		toolBox.addWidget(toolBtn1)
		toolBox.addWidget(toolBtn2)
		# toolBox.addWidget(toolBtn3)
		# toolBox.addWidget(toolBtn4)
		toolBox.addStretch()
		toolBox.addWidget(self.statusLabel)

		searchLabel = QLabel('搜索内容：')
		self.searchInput = QComboBox()
		self.searchInput.setEditable(True)
		self.searchInput.setSizeAdjustPolicy(1)
		self.searchOutput = QTextEdit() # 搜索结果输出框
		searchInputBox.addWidget(searchLabel)
		searchInputBox.addWidget(self.searchInput, 1) # 使用stretch参数修改控件大小，填满空间
		searchResBox.addWidget(self.searchOutput)

		# test rich text
		self.searchOutput.setText("123<b>345</b>456")
		self.searchOutput.setText('123<span style="background-color: red">345</span>456')

		searchBtn1 = QPushButton('新建搜索')
		searchBtn2 = QPushButton('合并搜索')
		searchBtn3 = QPushButton('清空')
		searchToolBox.addWidget(searchBtn1)
		searchToolBox.addWidget(searchBtn2)
		searchToolBox.addWidget(searchBtn3)
		searchToolBox.addStretch()

		self.setLayout(mainBox)

		# 按钮连接到槽
		openFileBtn.clicked.connect(self.open_file)
		parseFileBtn.clicked.connect(self.parse_file)

		self.levelCombo.activated.connect(self.show_lines)
		self.modCombo.activated.connect(self.show_lines)
		self.funCombo.activated.connect(self.show_lines)

		toolBtn1.clicked.connect(self.copy_result)
		toolBtn2.clicked.connect(self.save_result)

		searchBtn1.clicked.connect(self.new_search)
		searchBtn2.clicked.connect(self.add_search)
		searchBtn3.clicked.connect(self.clr_search)

		self.setGeometry(200, 300, 700, 500)
		self.setWindowTitle('log解析工具')
		self.show()

	def open_file(self):
		file = QFileDialog.getOpenFileName(self, '选择log文件', '')
		filename = file[0]
		self.fileNameEdit.setText(filename)

	def parse_file(self):
		self.please_wait()
		filename = self.fileNameEdit.text()

		start = time.time() # 计时开始

		self.L = Parser(filename)
		for line_no in range(0,self.L.lines): # 遍历所有log
			try:
				self.L.parse_log_level(line_no) # log级别
				self.L.parse_log_mod(line_no) # log模块
				self.L.parse_log_all_func(line_no) # 其他功能
			except Exception as e:
				print(e)
			if line_no%1000 == 0 or line_no == self.L.lines - 1: # 每100行和最后一行执行一次刷新，可大大加快解析速度！
				self.outEdit.setText('解析中，请等待...('+str(line_no)+'/'+str(self.L.lines)+')')
				QApplication.processEvents()

		end = time.time() # 计时结束

		# log级别
		log_levels = self.L.get_levels()
		self.levelCombo.clear()
		self.levelCombo.addItem('全部')
		self.levelCombo.addItems(log_levels.keys())

		# log模块
		log_mods = self.L.get_mods()
		self.modCombo.clear()
		self.modCombo.addItem('全部')
		self.modCombo.addItems(log_mods.keys())

		# log功能
		log_funcs = self.L.get_funcs()
		self.funCombo.clear()
		self.funCombo.addItem('全部')
		self.funCombo.addItems(log_funcs.keys())

		# 输出结果
		print_log = ''
		print_log += '解析时间：%.2fs\n' % (end-start)
		print_log += ('各级别log统计结果：\n')
		for level_name in log_levels.keys():
			print_log += (level_name + ': ' + str(len(log_levels.get(level_name, []))) + '\n')
		print_log += '\n'
		print_log += ('各模块log统计结果：\n')
		for mod_name in log_mods.keys():
			print_log += (mod_name + ': ' + str(len(log_mods.get(mod_name, []))) + '\n')
		print_log += '\n'
		print_log += ('各功能统计结果：\n')
		for func_name in log_funcs.keys():
			print_log += (func_name + ': ' + str(len(log_funcs.get(func_name, []))) + '\n')
		self.parse_result = print_log # 保存解析结果
		self.outEdit.setText(print_log)

	def show_lines(self):
		'''
		筛选框操作后，显示结果
		'''
		selLevel = self.levelCombo.currentText()
		selMod = self.modCombo.currentText()
		selFun = self.funCombo.currentText()

		if(selLevel == '全部' and selMod == '全部' and selFun == '全部'): # 不要显示全部log
			self.outEdit.setText(self.parse_result)
			return

		self.please_wait()

		if (selLevel != '全部'):
			resLevel = self.L.get_log_lines(selLevel)

		if (selMod != '全部'):
			resMod = self.L.get_log_lines(selMod)

		if (selFun != '全部'):
			resFun = self.L.get_log_lines(selFun)

		# 逐行显示
		self.outEdit.clear()
		lines_num = 0
		for i in range(0, self.L.lines):
			if (selLevel != '全部' and i not in resLevel): # 不满足等级筛选条件
				continue
			if (selMod != '全部' and i not in resMod): # 不满足模块筛选条件
				continue
			if (selFun != '全部' and i not in resFun): # 不满足功能筛选条件
				continue
			# i满足所有筛选条件
			self.outEdit.moveCursor(QTextCursor.End) # 使用insertPlainText需保证cursor在末尾
			self.outEdit.insertPlainText(self.L.log[i])
			lines_num = lines_num + 1
			self.show_status('当前' + str(lines_num) + '条')
			QApplication.processEvents()
		self.show_status('共' + str(lines_num) + '条')

	def please_wait(self):
		self.outEdit.setText('解析中，请等待...')
		QApplication.processEvents()
		self.show_status('')

	def show_status(self, status):
		self.statusLabel.setText(status)
		QApplication.processEvents()

	def copy_result(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.outEdit.toPlainText())
		self.show_status('复制成功')

	def save_result(self):
		file = QFileDialog.getSaveFileName(self, '保存log文件', '')
		filename = file[0]
		try:
			with open(filename, 'w+') as f:
				result = self.outEdit.toPlainText()
				f.write(result)
			self.show_status('保存成功')
		except Exception as e:
			print(e)
			self.show_status('保存失败')

	def get_search_ptn(self):
		a = self.searchInput.currentText()
		return a

	def new_search(self):
		search_ptn = self.get_search_ptn()
		resLine = self.L.search_log_lines(search_ptn) # 搜索包含查找目标的行

	def add_search(self):
		pass

	def clr_search(self):
		self.searchOutput.setText('')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
