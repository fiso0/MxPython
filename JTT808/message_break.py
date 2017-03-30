#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
分解消息
'''

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QComboBox, QGridLayout, QLineEdit

class Register(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout() # 创建网格布局

		# '消息'
		message_label = QLabel('消息')
		self.message_text = QTextEdit()
		self.message_text.setFixedHeight(80)
		break_button = QPushButton('分解')
		grid.addWidget(message_label,0,0)
		grid.addWidget(self.message_text,0,1)
		grid.addWidget(break_button,0,2)
		break_button.clicked.connect(self.breakButtonClicked)

		label01 = QLabel('=标识位=')
		label02 = QLabel('头:消息ID')
		label03 = QLabel('头:消息体属性（长度）')
		label04 = QLabel('头:终端手机号')
		label05 = QLabel('头:消息流水号')
		label06 = QLabel('头:消息包封装项')
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
		edit06 = QLineEdit() # '消息包封装项'
		edit07 = QTextEdit()
		edit07.setFixedHeight(60)
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

		self.setLayout(grid)
		self.setWindowTitle('分解消息')
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
		else:
			body = chrstr[-3]

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


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Register()
	sys.exit(app.exec_())