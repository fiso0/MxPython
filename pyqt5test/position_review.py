#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QTextEdit,QGridLayout,QLineEdit,QStyle
from PyQt5.QtCore import Qt

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		titleLabel = QLabel('Title')
		authorLabel = QLabel('Author')
		reviewLabel = QLabel('Review')

		titleEdit = QLineEdit() # 单行文本框
		authorEdit = QLineEdit()
		reviewEdit = QTextEdit() # 多行文本框

		grid = QGridLayout() # 网格布局
		grid.setSpacing(10) # 设置间距

		grid.addWidget(titleLabel,1,0)
		grid.addWidget(titleEdit,1,1)

		grid.addWidget(authorLabel,2,0)
		grid.addWidget(authorEdit,2,1)

		grid.addWidget(reviewLabel,3,0,Qt.AlignTop) # 顶部对齐
		grid.addWidget(reviewEdit,3,1,6,1) # 位置，跨度

		self.setLayout(grid) # 设置布局

		self.setGeometry(300,300,350,300) # 位置，尺寸
		# self.resize(self.sizeHint()) # 自动位置和尺寸
		self.setWindowTitle('Text Review')
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())