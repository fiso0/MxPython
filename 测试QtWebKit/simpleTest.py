#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

app = QApplication([])
view = QWebEngineView()

# view.load(QUrl("http://www.baidu.com"))  # ok

# view.setUrl(QUrl(r"D:\MX_bk\python\测试QtWebKit\test.htm"))  # ok

# view.setUrl(QUrl(r"D:\MX_bk\python\测试QtWebKit\test_noJS.htm"))  # ok

# ok
path = os.getcwd()
url = path + '\\test.htm'
view.setUrl(QUrl(url))

view.show()
app.exec_()