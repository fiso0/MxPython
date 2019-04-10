#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

format_list = {
	'GGA': 'NMEA,UTC,lat,N S,lon,E W,quality,numSV,HDOP,Alt,UAlt,Sep,USep,diffS,ID,cs',
	'RMC': 'NMEA,UTC,status,lat,N S,lon,E W,speed,course,date,mag,E W,mode,navS,cs',
	'GSV': 'NMEA,total,num,sat total,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sat id,elevation,azimuth,snr,sid,cs',
	'GST': 'NMEA,UTC,RMS dev,semi major dev,semi minor dev,semi major ori,lat err dev,lon err dev,alt err dev,cs'
}

EXAMPLE_INPUT = """$GPGGA,,,,,,0,,,,M,,M,,*66
$GPRMC,,V,,,,,,,,,,N,U*2A
$GAGSV,2,1,08,01,48,029,,04,73,190,,09,43,311,,19,19,150,,1*79
$GAGSV,2,2,08,21,01,052,,24,16,245,,26,04,090,,31,62,283,,1*7C"""


class Example(QWidget):
	def __init__(self):
		# noinspection PyArgumentList
		self.nmea_count = 0
		self.maxWidth = 0
		super().__init__()
		self.init_ui()

	def init_ui(self):
		# 设置UI
		inputLabel = QLabel('完整NMEA语句：')
		self.inputText = QTextEdit()
		self.inputText.setMinimumHeight(50)
		self.inputText.setText(EXAMPLE_INPUT)

		btn = QPushButton('解析')

		# self.outputLabel = QLabel('解析结果：')
		# self.outputLabel.setVisible(False)

		box = QHBoxLayout()
		box.addWidget(self.inputText)
		box.addWidget(btn)

		layout = QVBoxLayout()
		layout.addWidget(inputLabel)
		layout.addLayout(box)
		# layout.addWidget(self.outputLabel)
		# layout.addWidget(self.outputTable)
		self.setLayout(layout)

		btn.clicked.connect(self.parser)

		self.setFont(QFont('微软雅黑'))
		self.setWindowTitle('NMEA解析')
		self.initSize()
		self.show()

	def initSize(self):
		size = self.sizeHint()  # one-line height: 93
		self.setMinimumWidth(600)
		self.resize(600, size.height())

	def parser(self):
		import re
		# nmea = self.inputText.text()
		nmeas = self.inputText.toPlainText().split('\n')
		self.nmea_count = len(nmeas)
		self.inputText.resize(self.inputText.size().width(), 10 * self.nmea_count)

		self.addScrollArea()
		type_bk = None
		for nmea in nmeas:
			nmea.strip()

			if len(nmea) == 0:
				continue

			# 验证校验码
			content = nmea[1:-3]
			cs = nmea[-2:]
			cs_calc = self.checksum(content)

			data = re.split('[,*]', nmea)
			type = data[0][3:]
			if type != type_bk:
				new_type = True
				type_bk = type  # 备份前一条语句的类型
			else:
				new_type = False

			if new_type:
				self.addTable()  # 如果与前一条语句类型不同，新增一个表格
				row_count = 0
			# self.addTable()

			row_count += 1

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

			# 	if len(data) != len(format):
			# 		self.delTable()
			# 		self.outputLabel.setText('解析结果：格式错误')
			# 		return

			if cs == cs_calc:
				# self.outputLabel.setText(self.outputLabel.text() + ' ' + str(row_count) + '-校验码正确')
				pass
			else:
				self.outputLabel.setText(self.outputLabel.text() + ' ' + str(row_count) + '-校验码应为' + cs_calc)

			col = len(data)
			self.output.setColumnCount(col)  # 设置表格列数
			self.output.setRowCount(row_count)  # 设置表格行数

			if new_type and format != None:
				self.output.setHorizontalHeaderLabels(format)  # 设置表格水平标题内容

			# 设置表格内容
			c = 0
			for d in data:
				item = QTableWidgetItem(d)
				self.output.setItem(row_count - 1, c, item)
				c += 1

			self.output.resizeColumnsToContents()  # 根据内容自适应宽度
			width = sum([self.output.columnWidth(i) for i in range(len(data))])
			if width > self.maxWidth:
				self.maxWidth = width

			self.output.resize(width + 100, 100)#30 * row_count)  # todo:语句太多时表格高度可能不够，分别设置多个表格尺寸无效

		self.scrollWidget.resize(self.maxWidth + 50, 500)
		self.resize(self.maxWidth + 150, 600)

		# self.outputLabel.setVisible(True)

	def addScrollArea(self):
		# 如果已有此区域，先删除
		try:
			layout = self.layout()
			layout.removeWidget(self.topWidget)
			self.topWidget.deleteLater()
			self.topWidget = None
		except Exception as e:
			print(e)

		# 创建顶层widget，比滚动widget小
		self.topWidget = QWidget(self)
		self.topWidget.setMinimumSize(500, 30)

		# 创建滚动widget，比顶层widget大
		self.scrollWidget = QWidget(self.topWidget)
		self.scrollWidget.setMinimumSize(500, 300)
		self.scrollWidget.setLayout(QVBoxLayout())

		# 创建一个滚动区域，添加滚动widget
		area = QScrollArea()
		area.setWidget(self.scrollWidget)

		# 创建一个layout，添加滚动区域
		resultLayout = QVBoxLayout()
		resultLayout.addWidget(area)

		# 设置顶层widget的layout
		self.topWidget.setLayout(resultLayout)
		self.topWidget.show()

		# 放置顶层widget
		layout = self.layout()
		layout.addWidget(self.topWidget, stretch=1)

	def addTable(self):
		layout = self.scrollWidget.layout()

		self.outputLabel = QLabel('解析结果：')
		layout.addWidget(self.outputLabel)
		# self.resultBox.addWidget(self.outputLabel)

		# try:
		# 	layout.removeWidget(self.output)
		# 	self.output.deleteLater()
		# 	self.output = None
		# except Exception as e:
		# 	print(e)
		self.output = QTableWidget()
		layout.addWidget(self.output, stretch=1)
		# self.resultBox.addWidget(self.output)

		self.show()

	# def delTable(self):
	# 	layout = self.layout()
	# 	try:
	# 		layout.removeWidget(self.output)
	# 		self.output.deleteLater()
	# 		self.output = None
	# 	except Exception as e:
	# 		print(e)
	# 	QApplication.processEvents()
	# 	self.initSize()

	def resizeAll(self, contentWidth):
		self.inputText.resize(self.inputText.sizeHint())
		self.scrollWidget.resize()
		pass

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
