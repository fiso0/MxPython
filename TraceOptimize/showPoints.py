#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QStatusBar
import Point
import math
import time

SAMPLE_DATA = '''\
114.41949164302063	30.461033485055296
114.41846381019388	30.4622002973333
114.41458611233168	30.45950709179514
114.4077428177772	30.463077007081246
114.40817668124448	30.475378292859453
114.40847752577413	30.47532227196288
114.40985525305773	30.480758695560873
114.41080730745642	30.48793061768552
114.40424257394479	30.49065929361563
114.40512497188713	30.498470701573023
114.40556204124425	30.501036514001903
114.40021167694789	30.505357650443262
114.3988055692615	30.502927409460074
114.39954156153658	30.503332807270766
'''

STATUS_TIP = '状态：'

class ShowPoints(QWidget):
	def __init__(self):
		super().__init__()
		self.webView = QtWebEngineWidgets.QWebEngineView()
		self.inputText = QTextEdit()
		self.inputText.setFixedWidth(280)
		self.runButton = QPushButton('确定')
		self.runButton.setFixedWidth(100)
		self.clrButton = QPushButton('清除')
		self.clrButton.setFixedWidth(100)
		self.statusBar = QStatusBar()
		self.statusBar.showMessage(STATUS_TIP+"Ready")
		self.init_ui()

	def init_ui(self):
		path = os.getcwd()
		url = path + '\\test4_ok.htm'
		self.webView.setUrl(QtCore.QUrl(url))
		self.webView.page().loadFinished.connect(self.load_finished)  # for test

		self.inputText.setEnabled(False)
		self.inputText.setAcceptRichText(False)
		self.inputText.setToolTip("每行一组经纬度，纬度lat在前\n" + "以空格、逗号或制表符分隔\n" + \
		                          "GCJ-02（高德）坐标系\n\n" + "点击确定显示样本数据")

		self.runButton.clicked.connect(self.add_points)  # show all points in input text window
		self.clrButton.clicked.connect(self.clr_points)

		buttonBox = QHBoxLayout()  # button box
		buttonBox.addStretch()
		buttonBox.addWidget(self.runButton)
		buttonBox.addWidget(self.clrButton)

		rightBox = QVBoxLayout()  # right box
		rightBox.addWidget(self.inputText)
		rightBox.addLayout(buttonBox)
		rightBox.addWidget(self.statusBar)

		layout = QHBoxLayout()  # main box
		layout.addWidget(self.webView)
		layout.addLayout(rightBox)

		self.setLayout(layout)
		self.setWindowTitle('经纬度地图显示')
		self.show()

	def load_finished(self):
		self.inputText.setEnabled(True)

	def add_marker(self):
		"""
		添加标记，ok
		:return:
		"""
		a = self.webView.page()
		# a.runJavaScript("addMarker(114.39387,30.505299,true,1);")
		# a.runJavaScript("var point = new BMap.Point(114,30);var marker = new BMap.Marker(point);map.addOverlay(marker);")
		a.runJavaScript("testfunc(1);")  # ok
		a.runJavaScript("addMarker(114,30.01,true,2);")

	def run_script(self, script):
		a = self.webView.page()
		a.runJavaScript(script)

	def add_points(self):
		self.statusBar.showMessage(STATUS_TIP+"Running...")
		points_text = self.inputText.toPlainText()  # 获取输入

		if points_text == "":  # 使用示例输入
			points_text = SAMPLE_DATA
			self.inputText.setPlainText(points_text)

		points = Point.points_parser(points_text)  # 解析输入
		lats = [p.lat for p in points]
		lons = [p.lon for p in points]

		N = len(lats)  # 共N组经纬度
		G = math.ceil((N - 1) / 9)  # 每10个一组，首尾相接，共G组

		if N == 1:
			G = 1

		for g in range(G):  # 0,1,...,G-1
			index_s = 9 * g
			index_e = 9 * g + 10
			index_e = N if (index_e > N) else index_e
			latsStr = "[" + ",".join(lats[index_s:index_e]) + "]"
			lonsStr = "[" + ",".join(lons[index_s:index_e]) + "]"
			script = "addSimpleMarker(%s,%s,true);" % (latsStr, lonsStr)
			self.run_script(script)
			time.sleep(0.1)  # seconds，延时0.1秒，避免回调函数的执行顺序被打乱

		self.statusBar.showMessage(STATUS_TIP+"Done")

	def clr_points(self):
		self.run_script("clearMarkers();")
		self.inputText.setPlainText("")
		self.statusBar.showMessage(STATUS_TIP+"Ready")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = ShowPoints()
	sys.exit(app.exec_())
