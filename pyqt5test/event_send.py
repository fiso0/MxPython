#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QObject,pyqtSignal
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton

class Communicate(QObject):
	closeApp = pyqtSignal() # 创建一个新的信号叫做closeApp，信号使用了pyqtSignal()方法创建，并且成为外部类Communicate类的属性

class Example(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.c = Communicate()
		self.c.closeApp.connect(self.close) # 把自定义的closeApp信号连接到QMainWindow的close()槽上

		self.setGeometry(300,300,290,150)
		self.setWindowTitle('Emit signal')
		self.show()

	def mousePressEvent(self, *args, **kwargs): # 当在窗口上触发鼠标点击事件时信号会被发射
		self.c.closeApp.emit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())