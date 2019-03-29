#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
import time
from PyQt5.QtCore import QTimer

INIT_DATA = '$GNGGA,063203.000,3029.284071,N,11433.425580,E,4,18,0.85,76.747,M,0,M,2,3689*50'

class Example(QWidget):
	def __init__(self):
		# noinspection PyArgumentList
		super().__init__()
		self.init_ui()
		self.gen()

	def init_ui(self):
		# 设置UI
		grid = QGridLayout()

		self.check = QCheckBox('位置有效')
		self.check.setChecked(True)

		self.autoTime = QCheckBox('自动时间')

		lb0 = QLabel('talker')
		lb1 = QLabel('UTC')
		lb2 = QLabel('lat')
		lb3 = QLabel('N/S')
		lb4 = QLabel('lon')
		lb5 = QLabel('E/W')
		lb6 = QLabel('quality')
		lb7 = QLabel('numSV')
		lb8 = QLabel('HDOP')
		lb9 = QLabel('Alt')
		lb10 = QLabel('UAlt')
		lb11 = QLabel('Sep')
		lb12 = QLabel('USep')
		lb13 = QLabel('diffS')
		lb14 = QLabel('ID')

		self.text0 = QLineEdit()
		self.text1 = QLineEdit()
		self.text2 = QLineEdit()
		self.text3 = QLineEdit()
		self.text4 = QLineEdit()
		self.text5 = QLineEdit()
		self.text6 = QLineEdit()
		self.text7 = QLineEdit()
		self.text8 = QLineEdit()
		self.text9 = QLineEdit()
		self.text10 = QLineEdit()
		self.text11 = QLineEdit()
		self.text12 = QLineEdit()
		self.text13 = QLineEdit()
		self.text14 = QLineEdit()
		self.init_data()

		self.N = 15

		lb_res = QLabel('GGA生成结果：')
		self.res = QLineEdit()
		copy = QPushButton('复制')

		# add widgets
		grid.addWidget(self.check, 0, 0)
		grid.addWidget(self.autoTime, 0, 1)
		for i in range(0, self.N):  # i: 0~14
			grid.addWidget(eval('lb' + str(i)), 1, i)
			grid.addWidget(eval('self.text' + str(i)), 2, i)
		grid.addWidget(lb_res, 3, 0)
		grid.addWidget(self.res, 3, 1, 1, self.N-3)
		grid.addWidget(copy, 3, self.N-2, 1, 2)

		# change width
		self.text2.setMinimumWidth(85)  # lat
		self.text4.setMinimumWidth(85)  # lon

		# connect
		self.check.stateChanged.connect(self.invalid)
		for i in range(0, self.N-2):
			eval('self.text' + str(i)).textChanged.connect(self.gen)
			self.text1.text()

		self.autoTime.stateChanged.connect(self.autoTimeChanged)
		copy.clicked.connect(self.copyRes)

		self.setLayout(grid)
		self.setWindowTitle('生成GGA')
		self.resize(1000,108)
		self.show()

	def init_data(self):
		self.text0.setText('GPGGA')
		self.text1.setText('021439.00')
		self.text2.setText('3029.2841680')
		self.text3.setText('N')
		self.text4.setText('11433.4259037')
		self.text5.setText('E')
		self.text6.setText('1')
		self.text7.setText('31')
		self.text8.setText('0.5')
		self.text9.setText('89.342')
		self.text10.setText('M')
		self.text11.setText('-12.139')
		self.text12.setText('M')
		self.text13.setText('')
		self.text14.setText('')

	def gen(self):
		sentence = []
		for i in range(0, self.N):
			text = eval('self.text' + str(i)).text()
			sentence.append(text)
		sent = ','.join(sentence)
		cs = self.checksum(sent)
		res = '$' + sent + '*' + cs
		self.res.setText(res)
		return res

	def checksum(self,data):
		"""
		:param data: content after $, before *
		:return:
		"""
		CS = 0
		for a in data:
			CS ^= ord(a)
		return '%02X' % CS

	def invalid(self):
		valid = self.check.checkState()
		if valid == False:
			for i in range(1, self.N):
				eval('self.text' + str(i)).setText('')
			self.text6.setText('0')
			self.text10.setText('M')
			self.text12.setText('M')
		else:
			self.init_data()

	def autoTimeChanged(self):
		if self.autoTime.checkState():
			self.text1.setEnabled(False)
			self.timer = QTimer()
			self.timer.timeout.connect(self.updateTime)
			self.timer.start(1000)
		else:
			self.timer.stop()

	def updateTime(self):
		time_str = time.strftime("%H%M%S.00", time.gmtime())
		self.text1.setText(time_str)

	def copyRes(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.res.text())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
