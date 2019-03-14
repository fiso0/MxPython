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
		ptn = r'> (\S*)'
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

	def search_log_lines(self, line_set, search_ptn, mark = False):
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
						pos.append((i.start(),i.end()))
					pos.reverse()  # 插入时必须按逆序处理
					for (s,e) in pos:
						str_f = self.log[line_no][:s]
						str_m = self.log[line_no][s:e]
						str_r = self.log[line_no][e:]
						str_new = str_f + '<b>' + str_m + '</b>' + str_r
						self.log[line_no] = str_new
		return search_res


import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QButtonGroup, QRadioButton, \
	QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QTextBrowser, QMessageBox, QStatusBar, \
	QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor
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
		self.initUI()
		self.__stop_show = False
		self.L = None
		self.resMatch = set()
		self.history = []

	def initUI(self):
		mainBox = QVBoxLayout()
		fileBox = QHBoxLayout()
		menuBox = QHBoxLayout()
		resBox = QHBoxLayout()
		self.outEdit = QTextBrowser()  # 筛选结果输出框
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
		self.toolBtn3 = QPushButton('停止筛选')
		self.toolBtn3.setEnabled(False)
		menuBox.addWidget(self.toolBtn3)

		# tip
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
		# self.statusLabel.showMessage('Ready')
		toolBox.addWidget(toolBtn1)
		toolBox.addWidget(toolBtn2)
		toolBox.addStretch()
		mainBox.addWidget(self.statusLabel)

		searchLabel = QLabel('4.搜索内容：')
		self.searchInput = QComboBox()
		self.searchInput.setEditable(True)
		self.searchInput.setInsertPolicy(QComboBox.NoInsert)  # 回车时不自动插入，由按键处理
		self.searchInput.setSizeAdjustPolicy(1)
		self.searchInput.setToolTip('Python正则表达式：\n^ 开始位置\n$ 结尾位置\n. 任意字符\n| 或\n\ 特殊字符\n'\
		                            '[] 多种字符\n() 子表达式\n{} 匹配次数\n? 0 次或 1 次\n+ 至少 1次\n* 0次或任意次')
		self.regex = QCheckBox('正则表达式')
		self.searchOutput = QTextBrowser()  # 搜索结果输出框
		searchInputBox.addWidget(searchLabel)
		searchInputBox.addWidget(self.searchInput, 1)  # 使用stretch参数修改控件大小，填满空间
		searchInputBox.addWidget(self.regex)
		searchResBox.addWidget(self.searchOutput)

		# # test rich text
		# self.searchOutput.setText("123<b>345</b>456")
		# self.searchOutput.setText('123<span style="background-color: red">345</span>456')

		searchBtn1 = QPushButton('新建搜索')
		searchBtn2 = QPushButton('追加搜索')
		searchBtn3 = QPushButton('清空')
		searchBtn4 = QPushButton('复制')
		searchBtn4.setObjectName('copy_search')
		searchBtn5 = QPushButton('保存')
		searchBtn5.setObjectName('save_search')
		searchToolBox.addWidget(searchBtn1)
		searchToolBox.addWidget(searchBtn2)
		searchToolBox.addWidget(searchBtn3)
		searchToolBox.addWidget(searchBtn4)
		searchToolBox.addWidget(searchBtn5)
		searchToolBox.addStretch()

		self.setLayout(mainBox)

		# 按钮连接到槽
		openFileBtn.clicked.connect(self.open_file)
		parseFileBtn.clicked.connect(self.parse_file)

		self.levelCombo.activated.connect(self.show_lines)
		self.modCombo.activated.connect(self.show_lines)
		self.funCombo.activated.connect(self.show_lines)

		self.toolBtn3.clicked.connect(self.stop_show)
		toolBtn1.clicked.connect(self.copy_result)
		searchBtn4.clicked.connect(self.copy_result)
		toolBtn2.clicked.connect(self.save_result)
		searchBtn5.clicked.connect(self.save_result)

		searchBtn1.clicked.connect(self.new_search)
		searchBtn2.clicked.connect(self.add_search)
		searchBtn3.clicked.connect(self.clr_search)

		self.setGeometry(200, 300, 700, 500)
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

		# self.show_file(filename)  # 显示文件内容（没意义，暂取消）

	def show_file(self, filename):
		# 使用另一线程读取文件，发信号显示文件全部内容，结果会卡死
		t = OpenFileThread(filename)
		t.signal.connect(self.append_result)
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
		self.please_wait()
		filename = self.fileNameEdit.text()

		start = time.time()  # 计时开始

		self.L = Parser(filename)
		self.resMatch = set([a for a in range(0, self.L.lines)])  # 重置筛选结果为所有行号
		for line_no in range(0, self.L.lines):  # 遍历所有log
			try:
				self.L.parse_log_level(line_no)  # log级别
				self.L.parse_log_mod(line_no)  # log模块
				self.L.parse_log_all_func(line_no)  # 其他功能
			except Exception as e:
				print(e)
			if line_no % 1000 == 0 or line_no == self.L.lines - 1:  # 每1000行和最后一行执行一次刷新，可大大加快解析速度！
				self.outEdit.setText('解析中，请等待...(' + str(line_no) + '/' + str(self.L.lines) + ')')
				QApplication.processEvents()

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
		self.outEdit.setText(print_log)

	def show_lines(self):
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
			self.outEdit.setText(self.parse_result)
			return

		self.please_wait()

		# 取筛选结果
		self.resMatch = set([a for a in range(0, self.L.lines)])  # 重置筛选结果为所有行号
		if selLevel != '全部':
			resLevel = self.L.get_log_lines(selLevel)
			self.resMatch = self.resMatch & resLevel

		if selMod != '全部':
			resMod = self.L.get_log_lines(selMod)
			self.resMatch = self.resMatch & resMod

		if selFun != '全部':
			resFun = self.L.get_log_lines(selFun)
			self.resMatch = self.resMatch & resFun

		# 逐行显示筛选结果
		self.show_result_by_line(self.outEdit, self.resMatch)

		self.toolBtn3.setEnabled(False)

	def show_result_by_line(self, container, line_set):
		'''
		逐行显示
		:param container: 输出内容的容器
		:param line_set: 要显示内容的行号
		:return:
		'''
		container.clear()
		lines_num = 0
		for line_no in range(0, self.L.lines):
			if self.__stop_show == True:
				break
			if line_no not in line_set:  # 不满足筛选条件
				continue
			# i满足所有筛选条件
			container.moveCursor(QTextCursor.End)  # 使用insertPlainText需保证cursor在末尾
			container.insertPlainText(self.L.log[line_no])  # 如果带格式，需使用insertHTML
			lines_num = lines_num + 1  # 统计满足条件的log条数
			if lines_num % 100 == 0 or line_no == self.L.lines - 1:  # 每100行和最后一行执行一次刷新，可大大加快解析速度！
				self.show_status('当前' + str(lines_num) + '条')
				QApplication.processEvents()
		self.show_status('共' + str(lines_num) + '条')
		if self.__stop_show == True:
			self.show_status('\n（已停止）', True)

	def stop_show(self):
		# 设置标识，停止show_lines操作
		self.__stop_show = True
		self.toolBtn3.setEnabled(False)

	def please_wait(self):
		self.outEdit.setText('解析中，请等待...')
		QApplication.processEvents()
		self.show_status('')

	def show_status(self, status, append=False):
		if append:
			self.statusLabel.showMessage(self.statusLabel.currentMessage() + status)
		else:
			self.statusLabel.showMessage(status)
		QApplication.processEvents()

	def copy_result(self):
		sender = self.sender()
		clipboard = QApplication.clipboard()
		if sender.objectName() == 'copy_filt':
			clipboard.setText(self.outEdit.toPlainText())
		elif sender.objectName() == 'copy_search':
			clipboard.setText(self.searchOutput.toPlainText())
		self.show_status('复制成功')

	def save_result(self):
		sender = self.sender()
		file = QFileDialog.getSaveFileName(self, '保存log文件', '')
		filename = file[0]
		try:
			with open(filename, 'w+') as f:
				if sender.objectName() == 'save_filt':
					result = self.outEdit.toPlainText()
				elif sender.objectName() == 'save_search':
					result = self.searchOutput.toPlainText()
				f.write(result)
			self.show_status('保存成功')
		except Exception as e:
			print(e)
			self.show_status('保存失败')

	def append_result(self, data):
		self.outEdit.moveCursor(QTextCursor.End)  # 使用insertPlainText需保证cursor在末尾
		self.outEdit.insertPlainText(data)
		QApplication.processEvents()

	def show_result(self, data):
		self.outEdit.setText(data)

	def get_search_ptn(self):
		'''
		获得待搜索内容，可能需要格式处理，同时将搜索内容加入下拉框列表中（搜索历史）
		:return:
		'''
		a = self.searchInput.currentText()  # 获取输入

		# 搜索历史
		try:
			self.history.remove(a)
		except Exception as e:
			pass
		self.history.append(a)

		self.searchInput.clear()
		for c in self.history:
			self.searchInput.insertItem(0, c)  # 插入到下拉框列表

		regex = self.regex.isChecked()  # 获取是否正则表达式
		if not regex:
			# 转换正则表达式中的特殊字符
			a = a.replace('\\', '\\\\') # 放最前面
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
		line_set = self.resMatch  # 在筛选范围内搜索
		search_ptn = self.get_search_ptn()

		if len(line_set) == 0 or len(search_ptn) == 0:
			return

		self.resLine = self.L.search_log_lines(line_set, search_ptn)  # 在line_set范围内搜索包含search_ptn内容的行

		# 逐行显示查找结果
		self.show_result_by_line(self.searchOutput, self.resLine)

	def add_search(self):
		'''
		在目前搜索结果的基础上，追加搜索，并显示搜索结果（会按行号顺序显示）
		:return:
		'''
		line_set = self.resMatch  # 在筛选范围内搜索
		search_ptn = self.get_search_ptn()

		if len(line_set) == 0 or len(search_ptn) == 0:
			return

		new_resLine = self.L.search_log_lines(line_set, search_ptn)  # 在line_set范围内搜索包含search_ptn内容的行
		self.resLine = self.resLine | new_resLine # 求搜索结果的并集

		# 逐行显示查找结果
		self.show_result_by_line(self.searchOutput, self.resLine)

	def clr_search(self):
		self.searchOutput.setText('')
		self.show_status('已清空')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	try:
		ex = GUI()
	except Exception as e:
		print(e)
	sys.exit(app.exec_())
