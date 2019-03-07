#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QApplication,QToolTip,QPushButton,QMessageBox,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
import sys

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setGeometry(300,300,300,220) # 设置窗口x位置，y位置，x大小，y大小
		self.setWindowTitle('PyQt5 Example') # 设置窗口标题
		self.setWindowIcon(QIcon('plant.png')) # 设置窗口图标

		# 显示提示框
		QToolTip.setFont(QFont('SansSerif',10)) # 设置提示框字体
		self.setToolTip('This is a <b>QWidget</b> widget') # 设置提示框内容

		# 按钮及提示框
		btn = QPushButton('Tip Button', self) # 增加一个按钮
		btn.setToolTip('This is a <b>QPushButton</b> widget') # 设置按钮的提示框内容
		btn.resize(btn.sizeHint()) # 设置按钮为推荐大小
		btn.move(50,50) # 设置按钮位置

		# 使用按钮关闭窗口（事件处理）
		qbtn = QPushButton('Quit', self) # text参数是将显示在按钮中的内容，parent参数是用来放置该按钮的组件
		qbtn.clicked.connect(QCoreApplication.instance().quit) # 将点击按钮信号连接到QCoreApplication类实例的quit()方法
		qbtn.resize(qbtn.sizeHint())
		qbtn.move(150,50)

		self.center() # 居中显示
		self.show() # 显示窗口

	# 关闭窗口时弹窗确认
	def closeEvent(self, event): # 重写QWidget内的closeEvent方法，关闭QWidget时触发此事件方法
		reply = QMessageBox.question(self,'Message','Are you sure to quit?',QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,QMessageBox.No) # 带两个按钮的消息框，指定标题、内容文本，按钮集合，默认选择的按钮，返回值存在reply中
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	# 窗口居中显示
	def center(self):
		qr = self.frameGeometry() # 获得包含主窗口的矩形
		cp = QDesktopWidget().availableGeometry().center() # 获得屏幕中心点
		qr.moveCenter(cp) # 设置矩形中心到屏幕中心点处
		self.move(qr.topLeft()) # 移动应用窗口的位置到矩形处

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())