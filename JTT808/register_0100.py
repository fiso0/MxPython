#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
注册
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
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QLineEdit('00 2A') # '省'
		edit08 = QLineEdit('00 6F') # '市'
		edit09 = QLineEdit('31 32 33 34 35') # '制造商'
		edit10 = QLineEdit('4D 58 31 36 30 38 53 00 00 00 00 00 00 00 00 00 00 00 00 00') # '终端型号'
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

		# '完整消息'
		result_label = QLabel('完整消息')
		self.result_text = QTextEdit()
		self.result_text.setFixedHeight(80)
		result_button = QPushButton('转义(3)')
		grid.addWidget(result_label,15,0)
		grid.addWidget(self.result_text,15,1)
		grid.addWidget(result_button,15,2)
		result_button.clicked.connect(self.resultButtonClicked)

		self.setLayout(grid)
		self.setWindowTitle('注册')
		self.show()

	def lenButtonClicked(self):
		i = 6
		body = '' # 消息体
		while i < 13:
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Register()
	sys.exit(app.exec_())