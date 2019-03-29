#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

format_list = {
	'GGA': 'NMEA,UTC,lat,N S,lon,E W,quality,numSV,HDOP,Alt,UAlt,Sep,USep,diffS,ID,cs',
	'RMC': 'NMEA,UTC,status,lat,N S,lon,E W,speed,course,date,mag,E W,mode,navS,cs',
	'GSV': 'NMEA,total,num,sat total,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sid,cs',
	'GST': 'NMEA,UTC,RMS dev,semi major dev,semi minor dev,semi major ori,lat err dev,lon err dev,alt err dev,cs'
}


class Example(QWidget):
	def __init__(self):
		# noinspection PyArgumentList
		super().__init__()
		self.init_ui()

	def init_ui(self):
		# 设置UI
		inputLabel = QLabel('完整NMEA语句：')
		self.inputText = QLineEdit()

		btn = QPushButton('解析')

		self.outputLabel = QLabel('解析结果：')
		self.outputLabel.setVisible(False)

		box = QHBoxLayout()
		box.addWidget(self.inputText)
		box.addWidget(btn)

		layout = QVBoxLayout()
		layout.addWidget(inputLabel)
		layout.addLayout(box)
		layout.addWidget(self.outputLabel)
		# layout.addWidget(self.outputTable)
		self.setLayout(layout)

		btn.clicked.connect(self.parser)

		self.setFont(QFont('微软雅黑'))
		self.setWindowTitle('NMEA解析')
		self.initSize()
		self.show()

	def parser(self):
		import re
		nmea = self.inputText.text()  # todo:如果要支持多行数据，至少要保证是同一种NMEA
		nmea.strip()

		# 验证校验码
		content = nmea[1:-3]
		cs = nmea[-2:]
		cs_calc = self.checksum(content)

		data = re.split('[,*]', nmea)
		type = data[0][3:]
		format = format_list.get(type)

		if type == 'RMC':
			data = self.rmc_fit(data)

		if type == 'GSV':
			data = self.gsv_fit(data)

		# if format == None:
		# 	self.delTable()
		# 	self.outputLabel.setText('解析结果：无法识别语句')
		# 	return

		if format != None:
			format = format.split(',')

			if len(data) != len(format):
				self.delTable()
				self.outputLabel.setText('解析结果：格式错误')
				return

		if cs == cs_calc:
			self.outputLabel.setText('解析结果：校验码正确')
		else:
			self.outputLabel.setText('解析结果：校验码错误（应为%s）' % cs_calc)

		self.addTable()
		col = len(data)
		self.output.setColumnCount(col)  # 设置表格列数
		self.output.setRowCount(1)  # 设置表格行数

		if format != None:
			self.output.setHorizontalHeaderLabels(format)  # 设置表格水平标题内容

		# 设置表格内容
		c = 0
		for d in data:
			item = QTableWidgetItem(d)
			self.output.setItem(0, c, item)
			c += 1

		self.output.resizeColumnsToContents()  # 根据内容自适应宽度
		width = sum([self.output.columnWidth(i) for i in range(len(data))])
		size = self.size()
		size.setWidth(width + 50)
		self.resize(size)
		self.outputLabel.setVisible(True)

	def initSize(self):
		size = self.sizeHint()  # height: 93
		self.setMinimumWidth(600)
		self.resize(600, size.height())

	def delTable(self):
		layout = self.layout()
		try:
			layout.removeWidget(self.output)
			self.output.deleteLater()
			self.output = None
		except Exception as e:
			print(e)
		QApplication.processEvents()
		self.initSize()

	def addTable(self):
		layout = self.layout()
		try:
			layout.removeWidget(self.output)
			self.output.deleteLater()
			self.output = None
		except Exception as e:
			print(e)
		self.output = QTableWidget()
		layout.addWidget(self.output)

	def rmc_fit(self, data):
		# 旧版本RMC格式中缺少字段“navS”，补充空值
		if len(data) == 14:
			data.insert(-1, '')
		return data

	def gsv_fit(self, data):
		if len(data) != 22:
			data = data[:-1] + [''] * (22 - len(data)) + data[-1:]
		return data

	def checksum(self, data):
		"""
		:param data: content after $, before *
		:return:
		"""
		CS = 0
		for a in data:
			CS ^= ord(a)
		return '%02X' % CS


if __name__ == '__main__':
	app = QApplication(sys.argv)
	try:
		ex = Example()
	except Exception as e:
		print(e)
	sys.exit(app.exec_())
