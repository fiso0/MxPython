#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class GUI(QWidget):
	def __init__(self):
		super().__init__()
		self.ui_init()

	def ui_init(self):
		self.textFix = QLineEdit()
		testBtn = QPushButton('执行')
		self.textFlex = QTextEdit()
		self.textFlex.setFixedSize(50,50)

		testBtn.clicked.connect(self.btnClicked)

		# 布局
		mainBox = QVBoxLayout()
		mainBox.addWidget(self.textFix)
		mainBox.addWidget(testBtn)
		mainBox.addWidget(self.textFlex)
		self.setLayout(mainBox)

		self.resize(200, 100)
		self.setWindowTitle('测试改变widget大小')
		self.show()

	def btnClicked(self):
		num = int(self.textFix.text()) # 注意转换为int类型
		# self.textFlex.resize(100, 100) # 实测不需要此行
		self.textFlex.setFixedSize(num, num)


if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		ex = GUI()
		sys.exit(app.exec_())
	except Exception as e:
		print(e)
