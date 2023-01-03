#!/usr/bin/python3.5
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
		inTextLabel = QLabel('待解析消息（RTCM等）')
		self.message_in = QTextEdit(
			'D3008A432000312973020020002921C080000000200040007FFFA3A627A4A1A3272627DBE259D6B74B3B16CF0E562CA5A6B78EB7768FF0BCFD7DE5934B35ABC4FFC8108942303B463ADA83A0581641CFA775FF1BC1FD')
		outTextLabel = QLabel('解析结果')
		self.message_out = QTextEdit()
		break_button = QPushButton('分解')
		break_button.clicked.connect(self.breakButtonClicked)
		# self.ifAssignFormatCheck = QCheckBox()
		# self.ifAssignFormatCheck.stateChanged.connect(self.ifAssignFormat)
		# cmdLabel = QLabel('指定格式')
		# self.cmdCombo = QComboBox()
		# self.cmdCombo.addItems(self.formatList)
		# self.cmdCombo.setEnabled(False)

		break_button.setMaximumWidth(100)
		# self.cmdCombo.setMaximumWidth(100)

		# self.message_in.setFixedHeight(100)
		# self.message_out.setFixedHeight(200)

		# 格式
		hBox = QHBoxLayout()
		# hBox.addWidget(self.ifAssignFormatCheck)
		# hBox.addWidget(cmdLabel)
		# hBox.addWidget(self.cmdCombo)
		hBox.addStretch()
		hBox.addWidget(break_button)

		vBox = QVBoxLayout()
		vBox.addWidget(inTextLabel)
		vBox.addWidget(self.message_in)
		vBox.addLayout(hBox)

		vBox2 = QVBoxLayout()
		vBox2.addWidget(outTextLabel)
		vBox2.addWidget(self.message_out)

		hBox2 = QHBoxLayout()
		hBox2.addLayout(vBox,1)
		hBox2.addLayout(vBox2,2)

		self.setLayout(hBox2)
		# self.setFixedHeight(400)
		self.setWindowTitle('RTCM数据解析')
		self.show()

	# def ifAssignFormat(self):
	# 	# 根据是否勾选‘指定格式’使能下拉框
	# 	self.assign = self.ifAssignFormatCheck.checkState()
	# 	self.cmdCombo.setEnabled(self.assign)

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
		# if not self.assign:  # 自动格式
		# 	cmd = None
		# else:  # 指定格式
		# 	cmd = self.cmdCombo.currentText()

		# 根据指令类型解析
		# format = None
		try:
			labels, alens, fields, format = parser_cmd.parser_common_cmd(text, "RTCM3x消息编号")
		except Exception as e:
			print(e)

		# if format is None:
		# 	self.message_out.setText('失败，请手动选择指令类别\n')
		# 	return
		# else:
		# 	print('指令格式：' + format)
		# 	self.cmdCombo.setCurrentText(format)

		# 输出解析结果
		res_str = ''
		try:
			for label, alen, field in zip(labels, alens, fields):
				if alen != 0:  # 只输出长度不为0的字段
					res_str = res_str + (
						"{label:.<{width}}{field}".format(label=label, field=field if len(field) > 0 else "空",
						                                  width=20 - len(label.encode('GBK')) + len(
							                                  label))) + '\n'  # 为了输出对齐
		except:
			res_str='失败\n'
		# self.resizeAll(res_str)
		self.message_out.setText(res_str)


	def resizeAll(self, result_str):
		# 原高度
		oldHeightAll = self.height()
		oldHeightOut = self.message_out.height()

		# 新高度
		import math
		# lines = result_str.count('\n') + 1
		# 计算行数时要考虑一行内容可能很长需要分多行显示
		result_list = result_str.split('\n')
		result_lines_list = [math.ceil(len(a)/39) for a in result_list]
		lines = sum(result_lines_list)

		newHeightOut = lines * 16
		newHeightAll = newHeightOut-oldHeightOut+oldHeightAll

		# 调整为新高度
		self.message_out.setFixedHeight(newHeightOut)
		self.setFixedHeight(newHeightAll)
		# self.setMinimumHeight(0)
		# self.setMinimumHeight(newHeightAll)

		# 显示内容
		# self.message_out.setText(result_str)

# class TabWindow(QTabWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.mMsgCommon = MsgCommon()
# 		self.init_ui()
#
# 	def init_ui(self):
# 		self.addTab(self.mMsgCommon, '通用')
# 		self.setWindowTitle('消息分解')
# 		self.setMinimumWidth(350)
# 		# self.setMinimumHeight(450)
# 		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = MsgCommon() #TabWindow() # 只需要一个窗口，不需要使用TabWindow，且使用TabWindow后无法自动根据内容调整窗口大小
	sys.exit(app.exec_())
