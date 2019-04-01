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
			dd[d[k]['name']] = list(eval(d[k]['keywords']))  # for example: dd['GNSS'] = '[GPS]'.split(',')
		except:
			dd[d[k]['name']] = [d[k]['keywords']]

	return dd


import re


class Parser(object):
	'''
	解析器类
	'''

	def __init__(self, filename):
		self.filename = filename  # log文件名
		self.log = []  # log内容
		self.lines = 0  # log总行数
		self.config = None  # 功能关键词配置

		self.__log_level_line_dicts = dict()  # 按log级别分类保存行号
		self.__log_mod_line_dicts = dict()  # 按log模块分类保存行号
		self.__log_function_line_dicts = dict()  # 按log功能分类保存行号

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
			# 注：使用列表而不是集合，因为列表有序，集合无序
			# 但是集合比列表操作快很多很多，还是改为集合
			line_set = self.__log_level_line_dicts.get(level_name, set())
			line_set.add(line_no)
			self.__log_level_line_dicts[level_name] = line_set
		except:
			level_name = ''
		return level_name

	def parse_log_mod(self, line_no):
		"""
		判断该行log所属的模块，同时按模块分别记录行号
		:param line_no: 行号
		:return: log模块
		"""
		ptn = r'<.*?> (\S*)'
		try:
			mod_name = re.search(ptn, self.log[line_no]).group(1)  # try to find mod_name
			line_set = self.__log_mod_line_dicts.get(mod_name, set())  # get line set
			line_set.add(line_no)  # update line set
			self.__log_mod_line_dicts[mod_name] = line_set  # set line set
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
		line_set = self.__log_function_line_dicts.get(log_name, set())
		try:
			for key in key_words:
				if method == 'or':
					if key in self.log[line_no]:
						line_set.add(line_no)
						self.__log_function_line_dicts[log_name] = line_set
						return True
				elif method == 'and':
					if key not in self.log[line_no]:
						return False
			if method == 'or':  # 到这里说明所有关键词都无
				return False
			elif method == 'and':  # 到这里说明所有关键词都有
				line_set.add(line_no)
				self.__log_function_line_dicts[log_name] = line_set
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
		:return: log行号集合
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

	def search_log_lines(self, line_set, search_ptn, mark=False):
		'''
		在指定的行号范围内搜索指定内容
		:param line_set: 行号范围
		:param search_ptn: 待搜索内容
		:param mark: 是否添加格式（加粗）
		:return: 包含搜索内容的行号集合
		'''
		search_res = set()
		for line_no in line_set:
			if re.search(search_ptn, self.log[line_no]) is not None:
				# 符合搜索要求
				search_res.add(line_no)

				if mark:  # 添加格式（加粗），显示时会比较慢，暂不使用
					search_iter = re.finditer(search_ptn, self.log[line_no])
					pos = []
					for i in search_iter:
						pos.append((i.start(), i.end()))
					pos.reverse()  # 插入时必须按逆序处理
					for (s, e) in pos:
						str_f = self.log[line_no][:s]
						str_m = self.log[line_no][s:e]
						str_r = self.log[line_no][e:]
						str_new = str_f + '<b>' + str_m + '</b>' + str_r
						self.log[line_no] = str_new
		return search_res


import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QComboBox, QLabel, QVBoxLayout, \
	QHBoxLayout, QMessageBox, QStatusBar, QCheckBox, QListWidget, QMenu, QDockWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time
import threading


class OpenFileThread(QThread):
	signal = pyqtSignal(str)

	def __init__(self, filename):
		super().__init__()
		self.filename = filename
		self.__stop = threading.Event()

	def __del__(self):
		self.wait()

	def run(self):
		# 显示文件全部内容

		# with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
		# 	for data in f.readlines():
		# 		self.signal.emit(data)

		for data in open(self.filename, 'r', encoding='utf-8', errors='ignore'):
			if self.__stop.isSet():  # 如果设置了stop标识，则停止循环，等于停止线程
				break
			else:
				self.signal.emit(data)
				time.sleep(0.001)  # 必须有延时，否则会卡死

			# with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
			# 	data = f.read()
			# self.signal.emit(data)

	def stop(self):
		self.__stop.set()


class GUI(QWidget):
	def __init__(self):
		super().__init__()
		self.ui_init()
		self.__stop_show = False
		self.L = None  # 解析器对象
		self.filterRes = set()  # 筛选结果
		self.searchRes = set()  # 搜索结果
		self.searchHistory = []  # 搜索历史
		self.context_lines = []  # 上下文显示结果
		self.filterResInvalid = True  # 当前筛选结果是否为全部

	def ui_init(self):
		self.contextOut = QListWidget()  # 上下文内容显示框
		self.filterResOut = QListWidget()  # 筛选结果输出框
		self.searchResOut = QListWidget()  # 搜索结果输出框

		# 创建可停靠的窗口
		self.dock = QDockWidget("上下文log（只显示选中log的前后10条）", self)
		self.dock.setWidget(self.contextOut)
		self.dock.setFloating(True)  # 将可停靠窗口置于浮动状态
		self.dock.setFeatures(QDockWidget.DockWidgetFloatable)  # 改为只允许float，不允许关闭、移动
		self.dock.resize(700,300)
		self.dock.setVisible(False)  # 默认不可见

		self.fileNameEdit = QLineEdit()
		openFileBtn = QPushButton('1.选择文件')
		parseFileBtn = QPushButton('2.开始解析')

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
		self.toolBtn3 = QPushButton('停止筛选')
		self.toolBtn3.setEnabled(False)

		# 初始状态
		self.levelCombo.addItem('请先解析')
		self.modCombo.addItem('请先解析')
		self.funCombo.addItem('请先解析')
		self.levelCombo.setEnabled(False)
		self.modCombo.setEnabled(False)
		self.funCombo.setEnabled(False)

		toolBtn1 = QPushButton('复制')
		toolBtn1.setObjectName('copy_filt')
		toolBtn2 = QPushButton('保存')
		toolBtn2.setObjectName('save_filt')
		self.statusLabel = QStatusBar()

		searchLabel = QLabel('4.搜索内容：')
		self.searchInput = QComboBox()
		self.searchInput.setEditable(True)
		self.searchInput.setInsertPolicy(QComboBox.NoInsert)  # 回车时不自动插入，由按键处理
		self.searchInput.setSizeAdjustPolicy(1)
		self.regex = QCheckBox('正则表达式')
		self.regex.setToolTip('Python正则表达式：\n^ 开始位置\n$ 结尾位置\n. 任意字符\n| 或\n\ 特殊字符\n' \
		                            '[] 多种字符\n() 子表达式\n{} 匹配次数\n? 0 次或 1 次\n+ 至少 1次\n* 0次或任意次')

		searchBtn1 = QPushButton('新建搜索')
		searchBtn2 = QPushButton('追加搜索')
		searchBtn6 = QPushButton('结果中搜索')
		searchBtn3 = QPushButton('清空')
		searchBtn4 = QPushButton('复制')
		searchBtn4.setObjectName('copy_search')
		searchBtn5 = QPushButton('保存')
		searchBtn5.setObjectName('save_search')

		# 按钮连接到槽
		openFileBtn.clicked.connect(self.open_file)
		parseFileBtn.clicked.connect(self.parse_file)

		self.levelCombo.activated.connect(self.filter_activated)
		self.modCombo.activated.connect(self.filter_activated)
		self.funCombo.activated.connect(self.filter_activated)

		self.toolBtn3.clicked.connect(self.show_lines_stop)
		toolBtn1.clicked.connect(self.copy_result)
		searchBtn4.clicked.connect(self.copy_result)
		toolBtn2.clicked.connect(self.save_result)
		searchBtn5.clicked.connect(self.save_result)

		searchBtn1.clicked.connect(self.new_search)
		searchBtn2.clicked.connect(self.add_search)
		searchBtn6.clicked.connect(self.more_search)
		searchBtn3.clicked.connect(self.clr_search)

		self.filterResOut.itemClicked.connect(self.filter_item_clicked)  # 选中某条筛选结果时显示上下文
		self.contextOut.itemClicked.connect(self.context_item_clicked)  # 选中某条上下文时刷新显示上下文
		self.searchResOut.itemClicked.connect(self.search_item_clicked)  # 选中某条搜索结果时显示上下文

		# ListWidget右键菜单
		self.filterResOut.setContextMenuPolicy(Qt.CustomContextMenu)
		self.filterResOut.customContextMenuRequested.connect(self.right_click_menu)
		self.contextOut.setContextMenuPolicy(Qt.CustomContextMenu)
		self.contextOut.customContextMenuRequested.connect(self.right_click_menu)
		self.searchResOut.setContextMenuPolicy(Qt.CustomContextMenu)
		self.searchResOut.customContextMenuRequested.connect(self.right_click_menu)

		# ListWidget选择模式
		self.filterResOut.setSelectionMode(3)
		self.contextOut.setSelectionMode(3)
		self.searchResOut.setSelectionMode(3)

		# 布局
		mainBox = QVBoxLayout()
		resBox = QHBoxLayout()
		fileBox = QHBoxLayout()
		menuBox = QHBoxLayout()
		toolBox = QVBoxLayout()
		searchBox = QHBoxLayout()
		searchResBox = QVBoxLayout()
		searchInputBox = QHBoxLayout()
		searchToolBox = QVBoxLayout()

		mainBox.addLayout(fileBox)
		mainBox.addLayout(menuBox)
		mainBox.addLayout(resBox)
		mainBox.addLayout(searchBox)
		mainBox.addWidget(self.dock)
		mainBox.addWidget(self.statusLabel)

		resBox.addWidget(self.filterResOut)
		resBox.addLayout(toolBox)

		fileBox.addWidget(openFileBtn)
		fileBox.addWidget(self.fileNameEdit)
		fileBox.addWidget(parseFileBtn)

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
		menuBox.addWidget(self.toolBtn3)

		toolBox.addWidget(toolBtn1)
		toolBox.addWidget(toolBtn2)
		toolBox.addStretch()

		searchBox.addLayout(searchResBox)
		searchBox.addLayout(searchToolBox)

		searchResBox.addLayout(searchInputBox)
		searchResBox.addWidget(self.searchResOut)

		searchInputBox.addWidget(searchLabel)
		searchInputBox.addWidget(self.searchInput, 1)  # 使用stretch参数修改控件大小，填满空间
		searchInputBox.addWidget(self.regex)

		searchToolBox.addWidget(searchBtn1)
		searchToolBox.addWidget(searchBtn2)
		searchToolBox.addWidget(searchBtn6)
		searchToolBox.addWidget(searchBtn3)
		searchToolBox.addWidget(searchBtn4)
		searchToolBox.addWidget(searchBtn5)
		searchToolBox.addStretch()

		self.setLayout(mainBox)

		self.setGeometry(50, 50, 700, 800)
		self.setWindowTitle('log解析工具')
		self.show()

	def open_file(self):
		file = QFileDialog.getOpenFileName(self, '选择log文件', 'D://log//sCRTlog')
		filename = file[0]
		self.fileNameEdit.setText(filename)

	# # 直接打开文件并显示，会卡，暂取消
	# with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
	# 	data = f.read()
	# self.outEdit.setText(data)

	# # 显示文件内容（没意义，暂取消）
	# self.show_file(filename)

	def show_file(self, filename):
		"""
		显示文件内容(未使用)
		:param filename:
		:return:
		"""
		# 使用另一线程读取文件，发信号显示文件全部内容，结果会卡死
		t = OpenFileThread(filename)
		t.signal.connect(self.append_filter_result)
		t.start()

		# 弹窗-停止读取线程
		msgBox = QMessageBox(self)  # 指定parent为self，用于居中
		msgBox.setWindowTitle('请等待')
		msgBox.setText('正在读取文件（可选）')
		abort = msgBox.addButton('放弃', QMessageBox.ActionRole)  # 自定义内容按键
		msgBox.exec()
		if (msgBox.clickedButton() == abort):
			t.stop()
			QApplication.processEvents()

	def parse_file(self):
		"""
		开始解析文件内容
		:return:
		"""
		self.show_filter_result('解析中，请等待...')

		filename = self.fileNameEdit.text()

		start = time.time()  # 计时开始

		self.L = Parser(filename)
		self.filterRes = set([a for a in range(0, self.L.lines)])  # 重置筛选结果为所有行号
		for line_no in range(0, self.L.lines):  # 遍历所有log
			try:
				self.L.parse_log_level(line_no)  # log级别
				self.L.parse_log_mod(line_no)  # log模块
				self.L.parse_log_all_func(line_no)  # 其他功能
			except Exception as e:
				print(e)
			if line_no % 1000 == 0 or line_no == self.L.lines - 1:  # 每1000行和最后一行执行一次刷新，可大大加快解析速度！
				# self.filterResOut.addItem('解析中，请等待...(' + str(line_no) + '/' + str(self.L.lines) + ')')
				self.show_filter_result('解析中，请等待...(' + str(line_no) + '/' + str(self.L.lines) + ')')
			# QApplication.processEvents()

		end = time.time()  # 计时结束

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

		self.levelCombo.setEnabled(True)
		self.modCombo.setEnabled(True)
		self.funCombo.setEnabled(True)

		# 输出结果
		print_log = ''
		print_log += 'log行数：%d\n' % self.L.lines
		print_log += '解析时间：%.2fs\n\n' % (end - start)
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
		self.parse_result = print_log  # 保存解析结果
		self.show_filter_result(print_log)

	def filter_activated(self):
		'''
		筛选框操作后，处理并显示结果
		此函数与三个QComboBox的activated事件绑定
		'''
		self.__stop_show = False  # 重置
		self.toolBtn3.setEnabled(True)

		# sender = self.sender() # 获取触发此函数的信号发送者

		selLevel = self.levelCombo.currentText()
		selMod = self.modCombo.currentText()
		selFun = self.funCombo.currentText()

		if (selLevel == '全部' and selMod == '全部' and selFun == '全部'):  # 不要显示全部log
			self.filterRes = set([a for a in range(0, self.L.lines)])  # 重置筛选结果为所有行号
			self.show_filter_result(self.parse_result)
			self.filterResInvalid = True
			return

		self.filterResInvalid = False
		self.show_filter_result('解析中，请等待...')

		# 取筛选结果
		self.filterRes = set([a for a in range(0, self.L.lines)])  # 重置筛选结果为所有行号
		if selLevel != '全部':
			resLevel = self.L.get_log_lines(selLevel)
			self.filterRes = self.filterRes & resLevel

		if selMod != '全部':
			resMod = self.L.get_log_lines(selMod)
			self.filterRes = self.filterRes & resMod

		if selFun != '全部':
			resFun = self.L.get_log_lines(selFun)
			self.filterRes = self.filterRes & resFun

		# 逐行显示筛选结果
		self.show_lines(self.filterResOut, self.filterRes)

		self.toolBtn3.setEnabled(False)

	def show_filter_result(self, data_string):
		"""
		在筛选结果输出框显示内容(清空/添加/刷新)
		:param data:
		:return:
		"""
		self.filterResOut.clear()
		for data in data_string.split('\n'):
			self.filterResOut.addItem(data)
		QApplication.processEvents()

	def append_filter_result(self, data):
		"""
		在筛选结果输出框添加内容(添加/刷新)(未使用)
		:param data:
		:return:
		"""
		self.filterResOut.addItem(data)
		QApplication.processEvents()

	def show_lines(self, container, line_set):
		"""
		逐行显示
		:param container: 输出内容的容器（QListWidget)
		:param line_set: 要显示内容的行号（集合或列表均可）
		:return:
		"""
		container.clear()
		lines_num = 0
		for line_no in range(0, self.L.lines):
			if self.__stop_show == True:
				break
			if line_no not in line_set:  # 不满足筛选条件
				continue
			# i满足所有筛选条件
			# container.moveCursor(QTextCursor.End)  # 使用insertPlainText需保证cursor在末尾
			# container.insertPlainText(self.L.log[line_no])  # 如果带格式，需使用insertHTML
			container.addItem(self.L.log[line_no].strip())
			lines_num = lines_num + 1  # 统计满足条件的log条数
			if lines_num % 100 == 0 or line_no == self.L.lines - 1:  # 每100行和最后一行执行一次刷新，可大大加快解析速度！
				self.show_status('当前' + str(lines_num) + '条')
				QApplication.processEvents()
		if container is not self.contextOut:
			self.show_status('共' + str(lines_num) + '条')
		if self.__stop_show == True:
			self.show_status('\n（已停止）', True)

	def show_lines_stop(self):
		# 设置标识，停止show_lines操作
		self.__stop_show = True
		self.toolBtn3.setEnabled(False)

	def show_status(self, status, append=False):
		"""
		显示状态栏内容
		:param status:
		:param append:
		:return:
		"""
		if append:
			self.statusLabel.showMessage(self.statusLabel.currentMessage() + status)
		else:
			self.statusLabel.showMessage(status)
		QApplication.processEvents()

	def copy(self, data):
		clipboard = QApplication.clipboard()
		clipboard.setText(data)
		self.show_status('复制成功')

	def copy_result(self):
		sender = self.sender()
		text = ''
		if sender.objectName() == 'copy_filt':
			# clipboard.setText(self.filterResOut.toPlainText())
			for i in range(0, self.filterResOut.count()):
				text += self.filterResOut.item(i).text() + '\n'
		elif sender.objectName() == 'copy_search':
			# clipboard.setText(self.searchResOut.toPlainText())
			for i in range(0, self.searchResOut.count()):
				text += self.searchResOut.item(i).text() + '\n'
		self.copy(text)

	def save_result(self):
		sender = self.sender()
		file = QFileDialog.getSaveFileName(self, '保存log文件', '')
		filename = file[0]
		try:
			with open(filename, 'w+') as f:
				if sender.objectName() == 'save_filt':
					# result = self.filterResOut.toPlainText()
					text = ''
					for i in range(0, self.filterResOut.count() + 1):
						text += self.filterResOut.item(i).text()
					result = text
				elif sender.objectName() == 'save_search':
					result = self.searchResOut.toPlainText()
				f.write(result)
			self.show_status('保存成功')
		except Exception as e:
			print(e)
			self.show_status('保存失败')

	def get_search_ptn(self):
		'''
		获得待搜索内容，可能需要格式处理，同时将搜索内容加入下拉框列表中（搜索历史）
		:return:
		'''
		a = self.searchInput.currentText()  # 获取输入

		# 搜索历史
		try:
			self.searchHistory.remove(a)
		except Exception as e:
			pass
		self.searchHistory.append(a)  # 最新的搜索内容在列表最后

		self.searchInput.clear()
		for c in self.searchHistory:
			self.searchInput.insertItem(0, c)  # 插入到下拉框列表
		self.searchInput.setCurrentIndex(0)  # 设置当前项为最新的搜索内容

		regex = self.regex.isChecked()  # 获取是否正则表达式
		if not regex:
			# 转换正则表达式中的特殊字符
			a = a.replace('\\', '\\\\')  # 放最前面
			a = a.replace('^', '\^')
			a = a.replace('$', '\$')
			a = a.replace('.', '\.')
			a = a.replace('[', '\[')
			a = a.replace(']', '\]')
			a = a.replace('*', '\*')
			a = a.replace('?', '\?')
			a = a.replace('+', '\+')
			a = a.replace('{', '\{')
			a = a.replace('}', '\}')
			a = a.replace('|', '\|')
			a = a.replace('(', '\(')
			a = a.replace(')', '\)')
		return a

	def new_search(self):
		'''
		新建搜索，并显示搜索结果（会按行号顺序显示）
		:return:
		'''
		line_set = self.filterRes  # 在筛选范围内搜索
		search_ptn = self.get_search_ptn()

		if len(line_set) == 0 or len(search_ptn) == 0:
			return

		self.searchRes = self.L.search_log_lines(line_set, search_ptn)  # 在line_set范围内搜索包含search_ptn内容的行

		# 逐行显示查找结果
		self.show_lines(self.searchResOut, self.searchRes)

	def add_search(self):
		'''
		在目前搜索结果的基础上，追加搜索，并显示搜索结果（会按行号顺序显示）
		:return:
		'''
		line_set = self.filterRes  # 在筛选范围内搜索
		search_ptn = self.get_search_ptn()

		if len(line_set) == 0 or len(search_ptn) == 0:
			return

		new_resLine = self.L.search_log_lines(line_set, search_ptn)  # 在line_set范围内搜索包含search_ptn内容的行
		self.searchRes = self.searchRes | new_resLine  # 求搜索结果的并集

		# 逐行显示查找结果
		self.show_lines(self.searchResOut, self.searchRes)

	def more_search(self):
		'''
		在当前搜索结果中搜索
		:return:
		'''
		line_set = self.searchRes  # 在搜索结果范围内搜索
		search_ptn = self.get_search_ptn()

		if len(line_set) == 0 or len(search_ptn) == 0:
			return

		self.searchRes = self.L.search_log_lines(line_set, search_ptn)  # 在line_set范围内搜索包含search_ptn内容的行

		# 逐行显示查找结果
		self.show_lines(self.searchResOut, self.searchRes)

	def clr_search(self):
		self.searchResOut.clear()
		self.show_status('已清空')
		self.searchRes = set()

	def filter_item_clicked(self, item):
		"""
		选中某条筛选结果时显示上下文
		:param item:
		:return:
		"""
		if self.filterResInvalid:  # 还未执行有效筛选
			return

		row = self.filterResOut.row(item)
		lines_list = sorted(list(self.filterRes))
		line = lines_list[row]  # 当前选中的log行号
		self.show_context_lines(line)  # 显示上下文内容

	def search_item_clicked(self, item):
		row = self.searchResOut.row(item)
		lines_list = sorted(list(self.searchRes))
		line = lines_list[row]  # 当前选中的log行号
		self.show_context_lines(line)  # 显示上下文内容

	def context_item_clicked(self, item):
		"""
		选中某条上下文时刷新显示上下文
		:param item:
		:return:
		"""
		row = self.contextOut.row(item)
		line = self.context_lines[row]  # 当前选中的log行号
		self.show_context_lines(line)  # 显示上下文内容

	def show_context_lines(self, log_line, lines=10):
		"""
		显示某一行的上下文内容
		:param log_line: 要显示上下文的某一行的行号
		:param lines: 显示上下各多少行，默认10
		:return:
		"""
		self.context_lines = list(range((log_line - lines) if (log_line > lines) else 0,
		                                (log_line + lines) if (log_line + lines < self.L.lines) else self.L.lines))
		row = self.context_lines.index(log_line)

		# 逐行显示上下文内容
		self.show_lines(self.contextOut, self.context_lines)
		self.contextOut.setCurrentRow(row)  # 选中对应行

		self.dock.setVisible(True)

	def right_click_menu(self, pos):
		menu = QMenu()
		opt_copy = menu.addAction('复制')
		action = menu.exec_(self.sender().mapToGlobal(pos))
		if action == opt_copy:
			# text = self.sender().itemAt(pos).text()
			text = ''
			for a in self.sender().selectedItems():
				text += a.text() + '\n'
			self.copy(text)


if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		ex = GUI()
	except Exception as e:
		print(e)
	sys.exit(app.exec_())
