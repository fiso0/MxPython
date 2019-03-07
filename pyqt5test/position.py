#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget,QLabel,QApplication,QPushButton,QHBoxLayout,QVBoxLayout,QGridLayout

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI_absolute()

	def initUI_absolute(self):
		# 使用move()方法定位组件，坐标从左上角开始计算，x值从左到右增长，y值从上到下增长
		lb1 = QLabel('label 1',self)
		lb1.move(15,10)

		lb2 = QLabel('label 2',self)
		lb2.move(35,40)

		lb3 = QLabel('label 3',self)
		lb3.move(55,70)

		self.setGeometry(300,300,250,150)
		self.setWindowTitle('Absolute position')
		self.show()

	def initUI_box(self):
		# 箱布局
		okButton = QPushButton('OK')
		cancleButton = QPushButton('Cancle')

		# 创建一个水平箱布局，并且增加了一个拉伸因子和两个按钮
		# 拉伸因子在两个按钮之前增加了一个可伸缩空间，这会将按钮推到窗口的右边
		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(okButton)
		hbox.addWidget(cancleButton)

		# 为了创建必要的布局，把水平布局放置在垂直布局内
		# 拉伸因子将把包含两个按钮的水平箱布局推到窗口的底边
		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)

		# 设置窗口的主布局
		self.setLayout(vbox)

		self.setGeometry(300,300,250,150)
		self.setWindowTitle('Box position')
		self.show()

	def initUI_grid(self):
		grid = QGridLayout() # 创建网格布局
		self.setLayout(grid)

		names = ['Cls','Bck','','CLose',
		         '7','8','9','/',
		         '4','5','6','*',
		         '1','2','3','-',
		         '0','.','=','+'] # 标签会在之后的按钮中使用

		positions = [(i,j) for i in range(5) for j in range(4)] # 创建网格的定位列表，左上角是0,0

		for position, name in zip(positions,names):
			if name == '':
				continue
			button = QPushButton(name) # 创建按钮组件
			grid.addWidget(button,*position) # 向布局中添加按钮，星号可将(1,2)变为1,2传入

		self.move(300,150)
		self.setWindowTitle('Calculator')
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())