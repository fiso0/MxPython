#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget,QApplication,QLCDNumber,QSlider,QVBoxLayout,QPushButton,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		lcd = QLCDNumber() # lcd数字显示
		sld = QSlider(Qt.Horizontal) # 滑块条
		btn1 = QPushButton('-')
		btn2 = QPushButton('+')
		btn1.setFixedWidth(30)
		btn2.setFixedWidth(30)
		textLabel = QLabel()

		# 水平箱布局
		hbox = QHBoxLayout()
		hbox.addWidget(btn1)
		hbox.addWidget(sld)
		hbox.addWidget(btn2)

		# 垂直箱布局
		vbox = QVBoxLayout()
		vbox.addWidget(lcd)
		vbox.addLayout(hbox)
		vbox.addWidget(textLabel)

		# 将滑块条的valueChanged信号和lcd数字显示的display槽连接在一起
		sld.valueChanged.connect(lcd.display)

		btn1.clicked.connect(self.buttonClicked)
		btn2.clicked.connect(self.buttonClicked)

		self.setLayout(vbox)
		self.setGeometry(200,300,250,150)
		self.setWindowTitle('Signal & Slot')
		self.show()

	def buttonClicked(self):
		sender = self.sender()
		#TODO:怎么影响到slider？

	# 重写keyPressEvent()事件处理函数
	def keyPressEvent(self, QKeyEvent):
		if QKeyEvent.key() == Qt.Key_Escape:
			self.close() # 如果点击了Esc按钮，应用将会被终止

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())