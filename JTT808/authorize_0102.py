#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
鉴权
'''

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QComboBox, QGridLayout, QLineEdit

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
		self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,9,0)
		grid.addWidget(self.result_text,9,1)
		grid.addWidget(result_button,9,2)
		result_button.clicked.connect(self.resultButtonClicked)

		self.setLayout(grid)
		self.setWindowTitle('鉴权')
		self.show()

	def lenButtonClicked(self):
		i = 6
		body = '' # 消息体
		while i < 7:
			body += self.edits[i].text().strip().replace(' ','')
			i += 1
		body_len = int(len(body)/2)
		new_text = '%04X' % body_len
		new_text = new_text[:2] + ' ' + new_text[2:]
		self.edits[2].setText(new_text)

	def flowButtonClicked(self):
		text = self.edits[4].text().strip().replace(' ','')
		flow_num = int(text,16)
		new_flow_num = flow_num+1
		new_text = '%04X' % new_flow_num
		new_text = new_text[:2] + ' ' + new_text[2:]
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Register()
	sys.exit(app.exec_())