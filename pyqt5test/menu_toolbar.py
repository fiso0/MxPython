#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QAction,qApp,QTextEdit
from PyQt5.QtGui import QIcon

class Example(QMainWindow): # QMainWindow类提供了一个应用主窗口。默认创建一个拥有状态栏、工具栏和菜单栏的经典应用窗口骨架
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# 状态栏
		self.statusBar().showMessage('Ready') # 状态栏是用来显示状态信息的组件

		# 创建一个抽象动作行为，用于菜单栏、工具栏或自定义快捷键
		exitAction = QAction(QIcon('exit.png'),'&Exit',self) # 设置图标、文本
		exitAction.setShortcut('Ctrl+Q') # 设置快捷键
		exitAction.setStatusTip('Exit application') # 在状态栏显示提示内容
		exitAction.triggered.connect(qApp.quit) # 选中后中断应用

		# 菜单栏
		menubar = self.menuBar() # 创建菜单栏
		fileMenu = menubar.addMenu('&File') # 创建File菜单
		fileMenu.addAction(exitAction) # 增加退出动作为菜单项

		# 工具栏
		self.toolbar = self.addToolBar('Exit') # 创建工具栏
		self.toolbar.addAction(exitAction) # 增加退出动作为工具项

		# 中心组件，文本框
		textEdit = QTextEdit() # 创建文本框
		self.setCentralWidget(textEdit) # 设置文本框为中心组件，自动占据所有剩下的空间

		# 其他设置
		self.setGeometry(300,300,500,400) # 位置、尺寸
		self.setWindowTitle('Menu Toolbar and Statusbar') # 标题
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())