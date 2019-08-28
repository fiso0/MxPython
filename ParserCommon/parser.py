#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# import inputToHexText

class msg4005(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout()  # 创建网格布局

		# '消息'
		message_label = QLabel('4005消息')
		self.message_text = QTextEdit('262626260057000000000866888a2a41732640050000000a2e28742a0933275957180000000010003d454e0001cc0010be927b003c110b1c122e29046aaaa684253458000002000000003b3230313731313238313834363431ff002185')
		grid.addWidget(message_label, 0, 0)
		grid.addWidget(self.message_text, 0, 1)

		break_button = QPushButton('分解')
		# break_button.setFixedWidth(80)
		grid.addWidget(break_button, 0, 2, alignment=Qt.AlignHCenter)
		break_button.clicked.connect(self.breakButtonClicked)

		label01 = QLabel('消息头')
		label02 = QLabel('消息ID')
		label03 = QLabel('GPS定位时间')
		label04 = QLabel('经度')
		label05 = QLabel('纬度')
		label06 = QLabel('速度')
		label07 = QLabel('方向')
		label08 = QLabel('高度')
		label09 = QLabel('定位状态')
		label10 = QLabel('报警状态')
		label11 = QLabel('电量')
		label12 = QLabel('经度标志')
		label13 = QLabel('纬度标志')
		label14 = QLabel('预留')
		label15 = QLabel('国别')
		label16 = QLabel('运营商')
		label17 = QLabel('小区编号')
		label18 = QLabel('基站扇区')
		label19 = QLabel('预留')
		label20 = QLabel('信号量')
		label21 = QLabel('基站时间')
		label22 = QLabel('IMSI')
		label23 = QLabel('预留')
		label24 = QLabel('卫星定位方式')
		label25 = QCheckBox('步数')
		label26 = QLabel('附近wifi数据')
		label27 = QLabel('分隔符')
		label28 = QLabel('附近基站数据')
		label29 = QLabel('流水号')
		label30 = QLabel('校验码')
		self.labels = [label01, label02, label03, label04, label05, label06, label07, label08, label09, 
		               label10, label11, label12, label13, label14, label15, label16, label17, label18, label19, 
		               label20, label21, label22, label23, label24, label25, label26, label27, label28, label29, label30]

		# 添加labels和edits和description
		i = 0
		self.edits = []
		self.descs = []
		while i < 30:
			grid.addWidget(self.labels[i], i + 1, 0)

			self.edits.append(QLineEdit(''))
			grid.addWidget(self.edits[i], i + 1, 1)
			self.edits[i].setReadOnly(True)

			self.descs.append(QLineEdit(''))
			grid.addWidget(self.descs[i], i + 1, 2)
			self.descs[i].setReadOnly(True)

			i = i + 1

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('分解消息')
		self.show()

	def breakButtonClicked(self):
		import parser_4005
		(res, des) = parser_4005.parser_4005(self.message_text.toPlainText())

		for i in range(0,28):
			self.edits[i].setText(res[i])
			try:
				ind = des[i].index(':')
				desi = des[i][ind+1:]
			except:
				desi = ''
			self.descs[i].setText(desi)

class msg4007(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		grid = QGridLayout()  # 创建网格布局

		# '消息'
		message_label = QLabel('4007消息')
		self.message_text = QTextEdit('262626260041000000000866888a2a556172400703ffff800d606412081c09050c72173f11211e1e20095f110033e6006e00a001040302000401280000000000004dffff0004bd')
		# self.message_text.setFixedHeight(50)
		grid.addWidget(message_label, 0, 0)
		grid.addWidget(self.message_text, 0, 1)

		break_button = QPushButton('分解')
		# break_button.setFixedWidth(80)
		grid.addWidget(break_button, 0, 2, alignment=Qt.AlignHCenter)
		break_button.clicked.connect(self.breakButtonClicked)

		label01 = QLabel('消息头')
		label02 = QLabel('消息ID')

		label29 = QLabel('数据标识符长度')
		label30 = QLabel('数据量标识符')
		label31 = QLabel('数据类型')
		label32 = QLabel('信号强度')
		label11 = QLabel('电量')

		label03 = QLabel('GPS定位时间')
		label04 = QLabel('经度')
		label05 = QLabel('纬度')

		label34 = QLabel('经纬度标志')
		label08 = QLabel('高度')

		label35 = QLabel('经度理论解精度')
		label36 = QLabel('纬度理论解精度')
		label37 = QLabel('高度理论解精度')
		label09 = QLabel('定位状态')
		label38 = QLabel('解状态')
		label39 = QLabel('差分龄')
		label40 = QLabel('位置因子')
		label41 = QLabel('GPS平均CNO')
		label42 = QLabel('GPS卫星数')
		label43 = QLabel('BDS平均CNO')
		label44 = QLabel('BDS卫星数')
		label06 = QLabel('速度')
		label07 = QLabel('方向')
		label26 = QLabel('附近wifi数据')
		label28 = QLabel('附近基站数据')
		label29 = QLabel('流水号')
		label30 = QLabel('校验码')

		# label10 = QLabel('报警状态')
		# label12 = QLabel('经度标志')
		# label13 = QLabel('纬度标志')
		# label14 = QLabel('预留')
		# label15 = QLabel('国别')
		# label16 = QLabel('运营商')
		# label17 = QLabel('小区编号')
		# label18 = QLabel('基站扇区')
		# label19 = QLabel('预留')
		# label20 = QLabel('信号量')
		# label21 = QLabel('基站时间')
		# label22 = QLabel('IMSI')
		# label23 = QLabel('预留')
		# label24 = QLabel('卫星定位方式')
		# label25 = QCheckBox('步数')
		# label27 = QLabel('分隔符')
		self.labels = [label01, label02, label29, label30, label31, label32, label11, label03, label04, label05,
		               label34, label08, label35, label36, label37, label09, label38, label39, label40, label41,
		               label42, label43, label44, label06, label07, label26, label28, label29, label30]

		# 添加labels和edits和description
		i = 0
		self.edits = []
		self.descs = []
		while i < 29:
			grid.addWidget(self.labels[i], i + 1, 0)

			self.edits.append(QLineEdit(''))
			grid.addWidget(self.edits[i], i + 1, 1)
			self.edits[i].setReadOnly(True)

			self.descs.append(QLineEdit(''))
			grid.addWidget(self.descs[i], i + 1, 2)
			self.descs[i].setReadOnly(True)

			i = i + 1

		box = QVBoxLayout()
		box.addLayout(grid)
		box.addStretch()

		self.setLayout(box)
		self.setWindowTitle('分解消息')
		self.show()

	def breakButtonClicked(self):
		import parser_4005
		text = self.message_text.toPlainText()
		text.strip().replace(' ','')

		if(text[:8]=='26262626'):
			lens_4007 = [18,2,1,-1,1,1,1,6,5,5,1,3,2,2,2,1,1,2,2,1,1,1,1,2,1,-2,-2,2,1]
			res = parser_4005.parser_break(text, lens_4007)

			for i in range(0,29):
				self.edits[i].setText(' '.join(res[i]))

		else: # only parameters
			lens_4007 = [1,-1,1,1,1,6,5,5,1,3,2,2,2,1,1,2,2,1,1,1,1,2,1,-2,-2]
			res = parser_4005.parser_break(text, lens_4007)

			for i in range(2,27):
				self.edits[i].setText(' '.join(res[i-2]))

class msg400x(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		vbox = QVBoxLayout()
		hbox = QHBoxLayout()
		grid = QGridLayout()  # 创建网格布局

		# '消息'
		message_label = QLabel('400x消息')
		self.message_text = QTextEdit('262626260041000000000866888a2a556172400703ffff800d606412081c09050c72173f11211e1e20095f110033e6006e00a001040302000401280000000000004dffff0004bd')
		# self.message_text.setFixedHeight(50)
		# grid.addWidget(message_label, 0, 0)
		# grid.addWidget(self.message_text, 0, 1)
		hbox.addWidget(message_label)
		hbox.addWidget(self.message_text)

		break_button = QPushButton('分解')
		add_button = QPushButton('+')
		mns_button = QPushButton('-')
		# break_button.setFixedWidth(80)
		# grid.addWidget(break_button, 0, 2, alignment=Qt.AlignHCenter)

		btn_box = QVBoxLayout()

		btn_box.addWidget(break_button)
		btn_box.addWidget(add_button)
		btn_box.addWidget(mns_button)

		hbox.addLayout(btn_box)

		break_button.clicked.connect(self.breakButtonClicked)
		add_button.clicked.connect(self.addButtonClicked)
		mns_button.clicked.connect(self.mnsButtonClicked)

		vbox.addLayout(hbox)

		self.labels = [\
						QLineEdit('消息头'),\
						QLineEdit('消息ID'),\
						QLineEdit('数据标识符长度'),\
						QLineEdit('数据量标识符'),\
						QLineEdit('数据类型'),\
						QLineEdit('信号强度'),\
						QLineEdit('电量'),\
						QLineEdit('GPS定位时间'),\
						QLineEdit('经度'),\
						QLineEdit('纬度'),\
						QLineEdit('经纬度标志'),\
						QLineEdit('高度'),\
						QLineEdit('经度理论解精度'),\
						QLineEdit('纬度理论解精度'),\
						QLineEdit('高度理论解精度'),\
						QLineEdit('定位状态'),\
						QLineEdit('解状态'),\
						QLineEdit('差分龄'),\
						QLineEdit('位置因子'),\
						QLineEdit('GPS平均CNO'),\
						QLineEdit('GPS卫星数'),\
						QLineEdit('BDS平均CNO'),\
						QLineEdit('BDS卫星数'),\
						QLineEdit('速度'),\
						QLineEdit('方向'),\
						QLineEdit('附近wifi数据'),\
						QLineEdit('附近基站数据'),\
						QLineEdit('流水号'),\
						QLineEdit('校验码')]

		# 添加labels和edits和description
		i = 0
		self.edits = []
		self.descs = []
		while i < 29:
			grid.addWidget(self.labels[i], i + 1, 0)

			self.edits.append(QLineEdit(''))
			grid.addWidget(self.edits[i], i + 1, 1)
			self.edits[i].setReadOnly(True)

			self.descs.append(QLineEdit(''))
			grid.addWidget(self.descs[i], i + 1, 2)
			self.descs[i].setReadOnly(True)

			i = i + 1

		# box = QVBoxLayout()
		# box.addLayout(grid)
		# box.addStretch()
		vbox.addLayout(grid)

		# self.setLayout(box)
		self.setLayout(vbox)
		self.setWindowTitle('分解消息')
		self.show()

	def breakButtonClicked(self):
		import parser_4005
		text = self.message_text.toPlainText()
		text.strip().replace(' ','')

		if(text[:8]=='26262626'):
			lens_4007 = [18,2,1,-1,1,1,1,6,5,5,1,3,2,2,2,1,1,2,2,1,1,1,1,2,1,-2,-2,2,1]
			res = parser_4005.parser_break(text, lens_4007)

			for i in range(0,29):
				self.edits[i].setText(' '.join(res[i]))

		else: # only parameters
			lens_4007 = [1,-1,1,1,1,6,5,5,1,3,2,2,2,1,1,2,2,1,1,1,1,2,1,-2,-2]
			res = parser_4005.parser_break(text, lens_4007)

			for i in range(2,27):
				self.edits[i].setText(' '.join(res[i-2]))

	def addButtonClicked(self):
		pass


	def mnsButtonClicked(self):
		pass

class TabWindow(QTabWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		# self.mMsg400x = msg400x()
		self.mMsg4005 = msg4005()
		self.mMsg4007 = msg4007()

		# self.addTab(self.mMsg400x, '400x')
		self.addTab(self.mMsg4005, '4005')
		self.addTab(self.mMsg4007, '4007')

		self.setWindowTitle('OneNet')
		self.setMinimumSize(700, 900)
		# self.setGeometry(300,300,700,900)
		# self.resize(self.sizeHint())
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = TabWindow()
	sys.exit(app.exec_())
