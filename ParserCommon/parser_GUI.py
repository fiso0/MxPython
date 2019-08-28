#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
import os
import parser_cmd


class MsgCommon(QWidget):
	def __init__(self):
		super().__init__()
		self.formatList = self.scanFormatFile()  # 获取所有支持的协议格式
		self.assign = False
		self.init_ui()

	def init_ui(self):
		inTextLabel = QLabel('待解析消息（OneNet/JTT808等）')
		self.message_in = QTextEdit(
			'262626260057000000000866888a2a41732640050000000a2e28742a0933275957180000000010003d454e0001cc0010be927b003c110b1c122e29046aaaa684253458000002000000003b3230313731313238313834363431ff002185')
		outTextLabel = QLabel('解析结果')
		self.message_out = QTextEdit()
		break_button = QPushButton('分解')
		break_button.clicked.connect(self.breakButtonClicked)
		self.ifAssignFormatCheck = QCheckBox()
		self.ifAssignFormatCheck.stateChanged.connect(self.ifAssignFormat)
		cmdLabel = QLabel('指定格式')
		self.cmdCombo = QComboBox()
		self.cmdCombo.addItems(self.formatList)
		self.cmdCombo.setEnabled(False)

		break_button.setMaximumWidth(100)
		self.cmdCombo.setMaximumWidth(100)

		self.message_in.setMaximumHeight(100)
		self.message_out.setMinimumHeight(500)

		hBox = QHBoxLayout()
		hBox.addWidget(self.ifAssignFormatCheck)
		hBox.addWidget(cmdLabel)
		hBox.addWidget(self.cmdCombo)
		hBox.addStretch()
		hBox.addWidget(break_button)

		vBox = QVBoxLayout()
		vBox.addWidget(inTextLabel)
		vBox.addWidget(self.message_in)
		vBox.addLayout(hBox)
		vBox.addWidget(outTextLabel)
		vBox.addWidget(self.message_out)

		self.setLayout(vBox)
		self.setWindowTitle('分解消息')
		self.show()

	def ifAssignFormat(self):
		# 根据是否勾选‘指定格式’使能下拉框
		self.assign = self.ifAssignFormatCheck.checkState()
		self.cmdCombo.setEnabled(self.assign)

	@staticmethod
	def scanFormatFile():
		formats = []
		for filename in os.listdir('format'):
			if filename.startswith('format'):
				filename = filename[6:]  # 去掉前缀'format'
			if filename.endswith('.txt'):
				filename = filename[:-4]  # 去掉后缀'.txt'
			if filename != '':
				formats.append(filename)
		return formats

	def breakButtonClicked(self):
		# 获取输入
		text = self.message_in.toPlainText()

		# 获取指令格式
		if not self.assign:  # 自动格式
			cmd = None
		else:  # 指定格式
			cmd = self.cmdCombo.currentText()

		# 根据指令类型解析
		try:
			labels, alens, fields, format = parser_cmd.parser_common_cmd(text, cmd)
		except Exception as e:
			print(e)

		if format is None:
			self.message_out.setText('失败，请手动选择指令类别\n')
			return
		else:
			print('指令格式：' + format)
			self.cmdCombo.setCurrentText(format)

		# 输出解析结果
		res_str = ''
		try:
			for label, alen, field in zip(labels, alens, fields):
				if alen != 0:  # 只输出长度不为0的字段
					res_str = res_str + (
						"{label:.<{width}}{field}".format(label=label, field=field if len(field) > 0 else "空",
						                                  width=20 - len(label.encode('GBK')) + len(
							                                  label))) + '\n'  # 为了输出对齐
			self.message_out.setText(res_str)
		except:
			self.message_out.setText('失败\n')


class TabWindow(QTabWidget):
	def __init__(self):
		super().__init__()
		self.mMsgCommon = MsgCommon()
		self.init_ui()

	def init_ui(self):
		self.addTab(self.mMsgCommon, '通用')
		self.setWindowTitle('消息分解')
		self.setMinimumWidth(350)
		# self.setMinimumHeight(450)
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = TabWindow()
	sys.exit(app.exec_())
