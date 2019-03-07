#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton

class Example(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		btn1 = QPushButton('button 1',self)
		btn2 = QPushButton('button 2',self)
		btn1.move(30,50)
		btn2.move(150,50)

		# 状态栏，注意只有QMainWindow有状态栏，QWidget没有
		self.statusBar().showMessage('ready')

		# 按钮连接到同一个槽
		btn1.clicked.connect(self.buttonClicked)
		btn2.clicked.connect(self.buttonClicked)

		self.setGeometry(200,300,290,150)
		self.setWindowTitle('Event sender')
		self.show()

	def buttonClicked(self):
		sender = self.sender() # 调用sender()方法判断哪一个按钮按下
		self.statusBar().showMessage(sender.text()+' was pressed') # 显示在状态栏中

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())