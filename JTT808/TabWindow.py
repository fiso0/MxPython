#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import inputToHexText

class Register(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项（默认空）')
		label07 = QLabel('体:省')
		label08 = QLabel('体:市')
		label09 = QLabel('体:制造商')
		label10 = QLabel('体:终端型号')
		label11 = QLabel('体:终端ID')
		label12 = QLabel('体:车牌颜色')
		label13 = QLabel('体:车辆标识')
		label14 = QLabel('校验码')
		label15 = QLabel('=标识位=')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08, label09, label10, label11, label12, label13, label14, label15]

		edit01 = QLineEdit('7E') # '标识位'
		edit01.setEnabled(False)
		edit02 = QLineEdit('01 00') # '消息ID'
		edit02.setEnabled(False)
		edit03 = QLineEdit('00 2B') # '消息体属性（长度）'
		edit03.setEnabled(False)
		edit04 = QLineEdit('01 20 00 18 71 48') # '终端手机号'
		edit05 = QLineEdit('00 00') # '消息流水号'
		# edit05.setFont(QFont("宋体",9,QFont.Bold))
		p = self.palette()
		c = QColor(Qt.red)
		p.setColor(QPalette.Text,c)
		edit05.setPalette(p)
		# edit05.setAutoFillBackground(True)
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QLineEdit('00 2A') # '省'
		edit08 = QLineEdit('00 6F') # '市'
		edit09 = QLineEdit('31 32 33 34 35') # '制造商'
		edit10 = QLineEdit('4D 58 31 36 30 38 53 00 00 00 00 00 00 00 00 00 00 00 00 00') # '终端型号'
		edit10.setMinimumWidth(400)
		edit11 = QLineEdit('4D 58 32 30 31 37 00') # '终端ID'
		edit12 = QLineEdit('01') # '车牌颜色'
		edit13 = QLineEdit('41 5A 31 32 33 34') # '车辆标识'
		edit14 = QLineEdit() # '校验码'
		edit15 = QLineEdit('7E') # '标识位'
		self.edits = [edit01, edit02, edit03, edit04, edit05, edit06, edit07, edit08, edit09, edit10, edit11, edit12, edit13, edit14, edit15]

		# 添加lebels和edits
		i = 0
		while i < 15:
			grid.addWidget(self.labels[i],i,0)
			grid.addWidget(self.edits[i],i,1)
			i = i + 1

		len_button = QPushButton('计算(1)')
		grid.addWidget(len_button,2,2)

		flow_button = QPushButton('加1')
		grid.addWidget(flow_button,4,2)

		cs_button = QPushButton('计算(2)')
		grid.addWidget(cs_button,13,2)

		len_button.clicked.connect(self.lenButtonClicked)
		flow_button.clicked.connect(self.flowButtonClicked)
		cs_button.clicked.connect(self.csButtonClicked)

		self.cell_input = QLineEdit('12000187148') # 手机号
		grid.addWidget(self.cell_input,3,2)
		self.cell_input.setFixedWidth(75)

		self.province_input = QLineEdit('42') # 省
		grid.addWidget(self.province_input,6,2)
		self.province_input.setFixedWidth(75)

		self.city_input = QLineEdit('111') # 市
		grid.addWidget(self.city_input,7,2)
		self.city_input.setFixedWidth(75)

		self.manu_input = QLineEdit('12345') # 制造商
		grid.addWidget(self.manu_input,8,2)
		self.manu_input.setFixedWidth(75)

		self.dev_type_input = QLineEdit('MX1608S') # 终端型号
		grid.addWidget(self.dev_type_input,9,2)
		self.dev_type_input.setFixedWidth(75)

		self.dev_id_input = QLineEdit('MX2017') # 终端ID
		grid.addWidget(self.dev_id_input,10,2)
		self.dev_id_input.setFixedWidth(75)

		self.license_input = QLineEdit('AZ1234') # 车辆标识
		grid.addWidget(self.license_input,12,2)
		self.license_input.setFixedWidth(75)

		self.cell_input.textChanged.connect(self.cellChanged)
		self.province_input.textChanged.connect(self.provinceChanged)
		self.city_input.textChanged.connect(self.cityChanged)
		self.manu_input.textChanged.connect(self.manuChanged)
		self.dev_type_input.textChanged.connect(self.dev_typeChanged)
		self.dev_id_input.textChanged.connect(self.dev_idChanged)
		self.license_input.textChanged.connect(self.licenseChanged)

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		# self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,15,0)
		grid.addWidget(self.result_text,15,1)
		grid.addWidget(result_button,15,2)
		result_button.clicked.connect(self.resultButtonClicked)

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('注册')
		self.move(100,50)
		self.show()

	def lenButtonClicked(self):
		i = 6
		body = '' # 消息体
		while i < 13:
			body += self.edits[i].text().strip().replace(' ','')
			i += 1
		body_len = int(len(body)/2)
		new_text = inputToHexText.num2hex(body_len, 4, True)
		self.edits[2].setText(new_text)

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = inputToHexText.num2hex(new_flow_num, 4, True)
		self.edits[4].setText(new_text)

	def csButtonClicked(self):
		import checksum
		i = 1
		header_body = '' # 消息头+消息体
		while i < 13:
			header_body += self.edits[i].text().strip().replace(' ','')
			i += 1
		cs = checksum.checksum(header_body)
		cs_text = '%02X' % cs
		self.edits[13].setText(cs_text)

		self.header_body_cs = header_body + cs_text # 消息头+消息体+校验码

		# 自动显示完整消息
		i = 0
		result_text = ''
		while i < 15:
			result_text += self.edits[i].text().strip().replace(' ','')
			i += 1
		self.result_text.setPlainText(result_text)

	def resultButtonClicked(self):
		import tran7e
		tran_res = tran7e.tran7e(self.header_body_cs) # 转义处理消息头+消息体+校验码
		result_text = '7E' + tran_res + '7E'
		self.result_text.setPlainText(result_text) # 显示完整消息

	def cellChanged(self):
		text = self.cell_input.text().strip().replace(' ','')
		new_text = inputToHexText.string2hex(text,12)
		self.edits[3].setText(new_text)

	def provinceChanged(self):
		in_text = self.province_input.text().strip()
		try:
			new_text = inputToHexText.num2hex(int(in_text), 4)
			self.edits[6].setText(new_text)
		except:
			pass

	def cityChanged(self):
		in_text = self.city_input.text().strip()
		try:
			new_text = inputToHexText.num2hex(int(in_text), 4)
			self.edits[7].setText(new_text)
		except:
			pass

	def manuChanged(self):
		in_text = self.manu_input.text().strip()
		text = ''.join(['%02X' % ord(a) for a in in_text])
		new_text = inputToHexText.string2hex(text,10)
		self.edits[8].setText(new_text)

	def dev_typeChanged(self):
		in_text = self.dev_type_input.text().strip()
		text = ''.join(['%02X' % ord(a) for a in in_text])
		new_text = inputToHexText.string2hex(text,40,rear0=True)
		self.edits[9].setText(new_text)

	def dev_idChanged(self):
		in_text = self.dev_id_input.text().strip()
		text = ''.join(['%02X' % ord(a) for a in in_text])
		new_text = inputToHexText.string2hex(text,14,rear0=True)
		self.edits[10].setText(new_text)

	def licenseChanged(self):
		in_text = self.license_input.text().strip()
		text = ''.join(['%02X' % ord(a) for a in in_text])
		new_text = inputToHexText.string2hex(text,len(in_text)*2)
		self.edits[12].setText(new_text)


class Authorize(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项（默认空）')
		label07 = QLabel('体:鉴权码')
		label08 = QLabel('校验码')
		label09 = QLabel('=标识位=')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08, label09]

		edit01 = QLineEdit('7E') # '标识位'
		edit01.setEnabled(False)
		edit02 = QLineEdit('01 02') # '消息ID'
		edit02.setEnabled(False)
		edit03 = QLineEdit('00 06') # '消息体属性（长度）'
		edit03.setEnabled(False)
		edit04 = QLineEdit('01 20 00 18 71 48') # '终端手机号'
		edit05 = QLineEdit('00 01') # '消息流水号'
		p = self.palette()
		c = QColor(Qt.red)
		p.setColor(QPalette.Text,c)
		edit05.setPalette(p)
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QLineEdit('02 00 00 00 00 15') # '鉴权码'
		edit08 = QLineEdit() # '校验码'
		edit09 = QLineEdit('7E') # '标识位'
		self.edits = [edit01, edit02, edit03, edit04, edit05, edit06, edit07, edit08, edit09]

		# 添加labels和edits
		i = 0
		while i < 9:
			grid.addWidget(self.labels[i],i,0)
			grid.addWidget(self.edits[i],i,1)
			i = i + 1

		len_button = QPushButton('计算(1)')
		grid.addWidget(len_button,2,2)

		flow_button = QPushButton('加1')
		grid.addWidget(flow_button,4,2)

		cs_button = QPushButton('计算(2)')
		grid.addWidget(cs_button,7,2)

		len_button.clicked.connect(self.lenButtonClicked)
		flow_button.clicked.connect(self.flowButtonClicked)
		cs_button.clicked.connect(self.csButtonClicked)

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		# self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,9,0)
		grid.addWidget(self.result_text,9,1)
		grid.addWidget(result_button,9,2)
		result_button.clicked.connect(self.resultButtonClicked)

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('鉴权')
		self.move(650,50)
		self.show()

	def lenButtonClicked(self):
		i = 6
		body = '' # 消息体
		while i < 7:
			body += self.edits[i].text().strip().replace(' ','')
			i += 1
		body_len = int(len(body)/2)
		new_text = inputToHexText.num2hex(body_len, 4)
		self.edits[2].setText(new_text)

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = inputToHexText.num2hex(new_flow_num, 4)
		self.edits[4].setText(new_text)

	def csButtonClicked(self):
		import checksum
		i = 1
		header_body = '' # 消息头+消息体
		while i < 7:
			header_body += self.edits[i].text().strip().replace(' ','')
			i += 1
		cs = checksum.checksum(header_body)
		cs_text = '%02X' % cs
		self.edits[7].setText(cs_text)

		self.header_body_cs = header_body + cs_text # 消息头+消息体+校验码

		# 自动显示完整消息
		i = 0
		result_text = ''
		while i < 9:
			result_text += self.edits[i].text().strip().replace(' ','')
			i += 1
		self.result_text.setPlainText(result_text)

	def resultButtonClicked(self):
		import tran7e
		tran_res = tran7e.tran7e(self.header_body_cs) # 转义处理消息头+消息体+校验码
		result_text = '7E' + tran_res + '7E'
		self.result_text.setPlainText(result_text) # 显示完整消息

class LocReport(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项（默认空）')
		label07 = QLabel('体:报警标识')
		label08 = QLabel('体:状态')
		label09 = QLabel('体:纬度')
		label10 = QLabel('体:经度')
		label11 = QLabel('体:高程（米）')
		label12 = QLabel('体:速度（1/10km/h）')
		label13 = QLabel('体:方向（0-359，正北为0）')
		label14 = QLabel('体:时间')
		label15 = QLabel('校验码')
		label16 = QLabel('=标识位=')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08, label09, label10, label11, label12, label13, label14, label15, label16]

		edit01 = QLineEdit('7E') # '标识位'
		edit01.setEnabled(False)
		edit02 = QLineEdit('02 00') # '消息ID'
		edit02.setEnabled(False)
		edit03 = QLineEdit('00 1C') # '消息体属性（长度）'
		edit03.setEnabled(False)
		edit04 = QLineEdit('01 20 00 18 71 48') # '终端手机号'
		edit05 = QLineEdit('00 02') # '消息流水号'
		p = self.palette()
		c = QColor(Qt.red)
		p.setColor(QPalette.Text,c)
		edit05.setPalette(p)
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QLineEdit('00 00 00 00') # '报警标识'
		edit08 = QLineEdit('00 0c 00 03') # '状态'
		edit09 = QLineEdit('01 C9 C3 80') # '纬度'
		edit10 = QLineEdit('06 CB 80 80') # '经度'
		edit11 = QLineEdit('00 32') # '高程'
		edit12 = QLineEdit('00 00') # '速度'
		edit13 = QLineEdit('00 00') # '方向'
		edit14 = QLineEdit('17 03 29 17 03 00') # '时间'
		edit15 = QLineEdit() # '校验码'
		edit16 = QLineEdit('7E') # '标识位'
		edit16.setEnabled(False)
		self.edits = [edit01, edit02, edit03, edit04, edit05, edit06, edit07, edit08, edit09, edit10, edit11, edit12, edit13, edit14, edit15, edit16]

		# 添加labels和edits
		i = 0
		while i < 16:
			grid.addWidget(self.labels[i],i,0)
			grid.addWidget(self.edits[i],i,1)
			i = i + 1

		flow_button = QPushButton('加1')
		grid.addWidget(flow_button,4,2)
		# flow_button.resize(flow_button.sizeHint())
		# width = flow_button.width() # 75

		alarm_button = QPushButton('设置/清除')
		grid.addWidget(alarm_button,6,2)

		time_button = QPushButton('设置(1)')
		grid.addWidget(time_button,13,2)

		cs_button = QPushButton('计算(2)')
		grid.addWidget(cs_button,14,2)

		flow_button.clicked.connect(self.flowButtonClicked)
		alarm_button.clicked.connect(self.alarmButtonClicked)
		time_button.clicked.connect(self.timeButtonClicked)
		cs_button.clicked.connect(self.csButtonClicked)

		self.lat_input = QLineEdit('30') # 纬度
		grid.addWidget(self.lat_input,8,2)
		self.lat_input.setFixedWidth(75)

		self.lon_input = QLineEdit('114') # 经度
		grid.addWidget(self.lon_input,9,2)
		self.lon_input.setFixedWidth(75)

		self.alt_input = QLineEdit('50') # 高程
		grid.addWidget(self.alt_input,10,2)
		self.alt_input.setFixedWidth(75)

		self.spd_input = QLineEdit('0') # 速度
		grid.addWidget(self.spd_input,11,2)
		self.spd_input.setFixedWidth(75)

		self.dir_input = QLineEdit('0') # 方向
		grid.addWidget(self.dir_input,12,2)
		self.dir_input.setFixedWidth(75)

		self.lat_input.textChanged.connect(self.latChanged)
		self.lon_input.textChanged.connect(self.lonChanged)
		self.alt_input.textChanged.connect(self.altChanged)
		self.spd_input.textChanged.connect(self.spdChanged)
		self.dir_input.textChanged.connect(self.dirChanged)

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		# self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,16,0)
		grid.addWidget(self.result_text,16,1)
		grid.addWidget(result_button,16,2)
		result_button.clicked.connect(self.resultButtonClicked)

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('位置信息汇报')
		self.move(1200,50)
		self.show()

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = inputToHexText.num2hex(new_flow_num, 4)
		self.edits[4].setText(new_text)

	def alarmButtonClicked(self):
		text = self.edits[6].text().strip().replace(' ','')
		alarm = int(text)
		if alarm == 0:
			new_text = '00 00 00 01'
		else:
			new_text = '00 00 00 00'
		self.edits[6].setText(new_text)

	def timeButtonClicked(self):
		import time
		new_text = time.strftime("%y %m %d %H %M %S", time.localtime())
		self.edits[13].setText(new_text)

	def csButtonClicked(self):
		import checksum
		i = 1
		header_body = '' # 消息头+消息体
		while i < 14:
			header_body += self.edits[i].text().strip().replace(' ','')
			i += 1
		cs = checksum.checksum(header_body)
		cs_text = '%02X' % cs
		self.edits[14].setText(cs_text)

		self.header_body_cs = header_body + cs_text # 消息头+消息体+校验码

		# 自动显示完整消息
		i = 0
		result_text = ''
		while i < 16:
			result_text += self.edits[i].text().strip().replace(' ','')
			i += 1
		self.result_text.setPlainText(result_text)

	def resultButtonClicked(self):
		import tran7e
		tran_res = tran7e.tran7e(self.header_body_cs) # 转义处理消息头+消息体+校验码
		result_text = '7E' + tran_res + '7E'
		self.result_text.setPlainText(result_text) # 显示完整消息

	def latChanged(self):
		lat_input = self.lat_input.text().strip()
		try:
			lat = float(lat_input)
			new_text = inputToHexText.num2hex(int(lat * 1000000), 8)
			self.edits[8].setText(new_text)
		except:
			pass

	def lonChanged(self):
		lon_input = self.lon_input.text().strip()
		try:
			lon = float(lon_input)
			new_text = inputToHexText.num2hex(int(lon * 1000000), 8)
			self.edits[9].setText(new_text)
		except:
			pass

	def altChanged(self):
		alt_input = self.alt_input.text().strip()
		try:
			alt = int(alt_input)
			new_text = inputToHexText.num2hex(alt, 4)
			self.edits[10].setText(new_text)
		except:
			pass

	def spdChanged(self):
		spd_input = self.spd_input.text().strip()
		try:
			spd = int(spd_input)
			new_text = inputToHexText.num2hex(spd, 4)
			self.edits[11].setText(new_text)
		except:
			pass

	def dirChanged(self):
		dir_input = self.dir_input.text().strip()
		try:
			dir = int(dir_input)
			new_text = inputToHexText.num2hex(dir, 4)
			self.edits[12].setText(new_text)
		except:
			pass


class Heartbeat(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项（默认空）')
		label07 = QLabel('校验码')
		label08 = QLabel('=标识位=')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08]

		edit01 = QLineEdit('7E') # '标识位'
		edit01.setEnabled(False)
		edit02 = QLineEdit('00 02') # '消息ID'
		edit02.setEnabled(False)
		edit03 = QLineEdit('00 00') # '消息体属性（长度）'
		edit03.setEnabled(False)
		edit04 = QLineEdit('01 20 00 18 71 48') # '终端手机号'
		edit05 = QLineEdit('00 03') # '消息流水号'
		p = self.palette()
		c = QColor(Qt.red)
		p.setColor(QPalette.Text,c)
		edit05.setPalette(p)
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QLineEdit() # '校验码'
		edit08 = QLineEdit('7E') # '标识位'
		self.edits = [edit01, edit02, edit03, edit04, edit05, edit06, edit07, edit08]

		# 添加labels和edits
		i = 0
		while i < 8:
			grid.addWidget(self.labels[i],i,0)
			grid.addWidget(self.edits[i],i,1)
			i = i + 1

		flow_button = QPushButton('加1')
		grid.addWidget(flow_button,4,2)

		cs_button = QPushButton('计算(1)')
		grid.addWidget(cs_button,6,2)

		flow_button.clicked.connect(self.flowButtonClicked)
		cs_button.clicked.connect(self.csButtonClicked)

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		# self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(2)')
		grid.addWidget(result_label,8,0)
		grid.addWidget(self.result_text,8,1)
		grid.addWidget(result_button,8,2)
		result_button.clicked.connect(self.resultButtonClicked)

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('心跳')
		self.move(100,600)
		self.show()

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = inputToHexText.num2hex(new_flow_num, 4)
		self.edits[4].setText(new_text)

	def csButtonClicked(self):
		import checksum
		i = 1
		header_body = '' # 消息头+消息体
		while i < 6:
			header_body += self.edits[i].text().strip().replace(' ','')
			i += 1
		cs = checksum.checksum(header_body)
		cs_text = '%02X' % cs
		self.edits[6].setText(cs_text)

		self.header_body_cs = header_body + cs_text # 消息头+消息体+校验码

		# 自动显示完整消息
		i = 0
		result_text = ''
		while i < 8:
			result_text += self.edits[i].text().strip().replace(' ','')
			i += 1
		self.result_text.setPlainText(result_text)

	def resultButtonClicked(self):
		import tran7e
		tran_res = tran7e.tran7e(self.header_body_cs) # 转义处理消息头+消息体+校验码
		result_text = '7E' + tran_res + '7E'
		self.result_text.setPlainText(result_text) # 显示完整消息

class MessageBreak(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		# '消息'
		message_label = QLabel('消息')
		self.message_text = QTextEdit()
		# self.message_text.setFixedHeight(80)
		grid.addWidget(message_label,0,0)
		grid.addWidget(self.message_text,0,1)

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项（默认空）')
		label07 = QLabel('体:')
		label08 = QLabel('校验码')
		label09 = QLabel('=标识位=')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08, label09]

		edit01 = QLineEdit() # '标识位'
		edit01.setEnabled(False)
		edit02 = QLineEdit() # '消息ID'
		edit03 = QLineEdit() # '消息体属性（长度）'
		edit04 = QLineEdit() # '终端手机号'
		edit05 = QLineEdit() # '消息流水号'
		p = self.palette()
		c = QColor(Qt.red)
		p.setColor(QPalette.Text,c)
		edit05.setPalette(p)
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QTextEdit()
		# edit07.setFixedHeight(60)
		edit08 = QLineEdit() # '校验码'
		edit09 = QLineEdit() # '标识位'
		edit09.setEnabled(False)
		self.edits = [edit01, edit02, edit03, edit04, edit05, edit06, edit07, edit08, edit09]

		# 添加labels和edits
		i = 0
		while i < 9:
			grid.addWidget(self.labels[i],i+1,0)
			grid.addWidget(self.edits[i],i+1,1)
			i = i + 1

		break_button = QPushButton('分解↓')
		# grid.addWidget(break_button,0,2)

		result_button = QPushButton('↑转义(3)')
		# grid.addWidget(result_button,7,2)

		vbox = QVBoxLayout()
		vbox.addStretch()
		vbox.addWidget(break_button)
		vbox.addWidget(result_button)
		vbox.addStretch()
		grid.addLayout(vbox,0,2)

		len_button = QPushButton('重新计算(1)')
		grid.addWidget(len_button,3,2)

		flow_button = QPushButton('加1')
		grid.addWidget(flow_button,5,2)

		cs_button = QPushButton('重新计算(2)')
		grid.addWidget(cs_button,8,2)

		break_button.clicked.connect(self.breakButtonClicked)
		result_button.clicked.connect(self.resultButtonClicked)
		len_button.clicked.connect(self.lenButtonClicked)
		flow_button.clicked.connect(self.flowButtonClicked)
		cs_button.clicked.connect(self.csButtonClicked)

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('分解消息')
		self.move(650,450)
		self.show()

	def breakButtonClicked(self):
		message = self.message_text.toPlainText().strip().replace(' ','')
		chrstr = [message[i:i+2] for i in range(0,len(message),2)]
		msg_len = len(chrstr)

		flag_field = chrstr[0]
		msg_id = ' '.join(chrstr[1:3])
		msg_prop = ' '.join(chrstr[3:5])
		cell = ' '.join(chrstr[5:11])
		flow = ' '.join(chrstr[11:13])
		cs = chrstr[-2]

		body_len = int(''.join(chrstr[3:5]),16) & 0x3F
		if body_len > 1:
			body = ' '.join(chrstr[-body_len-2:-2])
		elif body_len == 1:
			body = chrstr[-3]
		else:
			body = ''

		msg_pack_len = msg_len - body_len - 15
		if msg_pack_len > 1:
			msg_pack = ' '.join(chrstr[13:-body_len-2])
		elif msg_pack_len == 1:
			msg_pack = chrstr[13]
		else:
			msg_pack = ''

		self.edits[0].setText(flag_field)
		self.edits[1].setText(msg_id)
		self.edits[2].setText(msg_prop)
		self.edits[3].setText(cell)
		self.edits[4].setText(flow)
		self.edits[5].setText(msg_pack)
		self.edits[6].setText(body)
		self.edits[7].setText(cs)
		self.edits[8].setText(flag_field)

	def lenButtonClicked(self):
		i = 6
		body = '' # 消息体
		while i < 7:
			body += self.edits[i].toPlainText().strip().replace(' ','')
			i += 1
		body_len = int(len(body)/2)
		new_text = inputToHexText.num2hex(body_len, 4)
		self.edits[2].setText(new_text)

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = inputToHexText.num2hex(new_flow_num, 4)
		self.edits[4].setText(new_text)

	def csButtonClicked(self):
		import checksum
		i = 1
		header_body = '' # 消息头+消息体
		while i < 6:
			header_body += self.edits[i].text().strip().replace(' ','')
			i += 1
		header_body += self.edits[6].toPlainText().strip().replace(' ','')
		cs = checksum.checksum(header_body)
		cs_text = '%02X' % cs
		self.edits[7].setText(cs_text)

		self.header_body_cs = header_body + cs_text # 消息头+消息体+校验码

		# 自动显示完整消息
		i = 0
		result_text = ''
		result_text = self.edits[0].text() + self.header_body_cs + self.edits[8].text()
		self.message_text.setPlainText(result_text)

	def resultButtonClicked(self):
		import tran7e
		tran_res = tran7e.tran7e(self.header_body_cs) # 转义处理消息头+消息体+校验码
		result_text = '7E' + tran_res + '7E'
		self.message_text.setPlainText(result_text) # 显示完整消息

class TabWindow(QTabWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		self.mRegister = Register()
		self.mAuthorize = Authorize()
		self.mLocReport = LocReport()
		self.mHeartbeat = Heartbeat()
		self.mMessageBreak = MessageBreak()

		self.addTab(self.mRegister,'注册')
		self.addTab(self.mAuthorize,'鉴权')
		self.addTab(self.mLocReport,'位置信息汇报')
		self.addTab(self.mHeartbeat,'心跳')
		self.addTab(self.mMessageBreak,'消息分解')

		self.setWindowTitle('JTT808')
		self.setMinimumHeight(650)
		# self.setGeometry(300,300,500,700)
		# self.resize(self.sizeHint())
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# gui1 = Register()
	# gui2 = Authorize()
	# gui3 = LocReport()
	# gui4 = Heartbeat()
	# gui5 = MessageBreak()
	gui = TabWindow()
	sys.exit(app.exec_())