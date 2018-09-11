#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class msgxxxx(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		inTextLabel = QLabel('待解析消息')
		self.message_in = QTextEdit('262626260057000000000866888a2a41732640050000000a2e28742a0933275957180000000010003d454e0001cc0010be927b003c110b1c122e29046aaaa684253458000002000000003b3230313731313238313834363431ff002185')
		outTextLabel = QLabel('解析结果')
		self.message_out = QTextEdit()
		break_button = QPushButton('分解')
		break_button.clicked.connect(self.breakButtonClicked)
		cmdLabel = QLabel('指令类别')
		self.cmdCombo = QComboBox()
		self.cmdCombo.addItems(['自动','4005','4007'])

		break_button.setMaximumWidth(100)
		self.cmdCombo.setMaximumWidth(100)

		self.message_in.setMaximumHeight(100)
		self.message_out.setMinimumHeight(500)

		hBox = QHBoxLayout()
		hBox.addWidget(cmdLabel)
		hBox.addWidget(self.cmdCombo)
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

	def breakButtonClicked(self):
		import parser_common_cmd

		# 获取输入
		text = self.message_in.toPlainText()

		# 获取指令类型
		cmdIdx = self.cmdCombo.currentIndex()
		if cmdIdx == 0:
			cmd = parser_common_cmd.get_cmd(text)
			if cmd == None:
				res_str = '失败，请手动选择指令类别\n'
				self.message_out.setText(res_str)
				return
		else:
			cmd = self.cmdCombo.itemText(cmdIdx)

		# 根据指令类型解析
		res = parser_common_cmd.parser_common(text,cmd)

		# 输出解析结果
		res_str = ''
		try:
			for label,alen,field in res:
				if(alen!=0): # 只输出长度不为0的字段
					res_str = res_str+("{label:.<{width}}{field}".format(label=label, field=field, width=16-len(label.encode('GBK'))+len(label)))+'\n' # 为了输出对齐
		except:
			res_str = '失败\n'
		self.message_out.setText(res_str)

class TabWindow(QTabWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		self.mMsg = msgxxxx()

		self.addTab(self.mMsg, 'OneNet消息分解')

		self.setWindowTitle('OneNet')
		# self.setMinimumSize(700, 900)
		# self.setGeometry(300,300,700,900)
		# self.resize(self.sizeHint())
		self.setMinimumWidth(350)
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = TabWindow()
	sys.exit(app.exec_())
