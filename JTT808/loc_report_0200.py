#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
位置信息汇报
'''

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QComboBox, QGridLayout, QLineEdit

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
		label11 = QLabel('体:高程')
		label12 = QLabel('体:速度')
		label13 = QLabel('体:方向')
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
		edit05 = QLineEdit('00 03') # '消息流水号'
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

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,16,0)
		grid.addWidget(self.result_text,16,1)
		grid.addWidget(result_button,16,2)
		result_button.clicked.connect(self.resultButtonClicked)

		self.setLayout(grid)
		self.setWindowTitle('位置信息汇报')
		self.show()

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = '%04X' % new_flow_num
		new_text = new_text[:2] + ' ' + new_text[2:]
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = LocReport()
	sys.exit(app.exec_())