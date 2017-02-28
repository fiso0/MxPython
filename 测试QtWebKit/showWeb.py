#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout


class ShowWeb(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		self.webView = QtWebEngineWidgets.QWebEngineView()
		path = os.getcwd()
		url = path + '\\test1_ok.htm'
		# url = path + '\\Baidu1.htm'
		self.webView.setUrl(QtCore.QUrl(url))

		self.webView.page().load_finished.connect(self.addMarker)  # connect

		layout = QVBoxLayout()
		layout.addWidget(self.webView)

		self.setLayout(layout)
		self.setWindowTitle('测试WebEngine')
		self.show()

	def addMarker(self):
		'''
		添加标记，ok
		:return:
		'''
		a=self.webView.page()
		# a.runJavaScript("addMarker(114.39387,30.505299,true,1);")
		# a.runJavaScript("var point = new BMap.Point(114,30);var marker = new BMap.Marker(point);map.addOverlay(marker);")
		a.runJavaScript("testfunc(1);")  # ok
		a.runJavaScript("addMarker(114,30.01,true,2);")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = ShowWeb()
	sys.exit(app.exec_())
