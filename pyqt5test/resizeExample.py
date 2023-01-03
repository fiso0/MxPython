#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # 2019-9-20 测试了，没明白怎么用
#
#
# from PyQt5 import QtCore, QtGui, QtWidgets
# import sys
# # from mainwin import Ui_MainWindow
# from PyQt5.QtWidgets import *
#
# try:
# 	_fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
# 	def _fromUtf8(s):
# 		return s
#
# try:
# 	_encoding = QApplication.UnicodeUTF8
#
#
# 	def _translate(context, text, disambig):
# 		return QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
# 	def _translate(context, text, disambig):
# 		return QApplication.translate(context, text, disambig)
#
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFontMetrics, QPainter
#
#
# class MyLabel(QLabel):
# 	def paintEvent(self, event):
# 		painter = QPainter(self)
#
# 		metrics = QFontMetrics(self.font())
# 		elided = metrics.elidedText(self.text(), Qt.ElideRight, self.width())
#
# 		painter.drawText(self.rect(), self.alignment(), elided)
#
#
# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	mainwin = QMainWindow()
# 	# ui = Ui_MainWindow()
# 	# ui.setupUi(mainwin)
#
# 	# centralwidget = QtGui.QWidget(mainwin)
#
# 	grid = QGridLayout()
#
# 	label = QLabel()
# 	txt = "234234"
# 	metrics = QFontMetrics(label.font())
# 	w = metrics.width(txt)
# 	label.setGeometry(QtCore.QRect(20, 20, w, 80))
# 	label.setObjectName(_fromUtf8("label_3"))
# 	label.setText(_translate("MainWindow", txt, None))
#
# 	grid.addWidget(label, 0, 0)
#
# 	l = ['123', '3451111111111111', '1111111111', '0000000000000', '123']
# 	comboBox = QComboBox()
# 	txt = (max(l, key=len))
# 	metrics = QFontMetrics(comboBox.font())
# 	w = metrics.width(txt)
# 	comboBox.setGeometry(QtCore.QRect(80, 5, 20, 20))
# 	comboBox.setMinimumWidth(w)
#
# 	comboBox.setObjectName(_fromUtf8("comboBox_2"))
# 	comboBox.addItems(l)
# 	comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
#
# 	grid.addWidget(comboBox, 0, 1)
#
# 	label1 = QLabel()
# 	txt = "2342341111111111111111"
# 	metrics = QFontMetrics(label1.font())
# 	w = metrics.width(txt)
# 	label1.setGeometry(QtCore.QRect(20, 20, w, 80))
# 	label1.setObjectName(_fromUtf8("label_3"))
# 	label1.setText(_translate("MainWindow", txt, None))
#
# 	grid.addWidget(label1, 1, 0)
#
# 	l = ['123', '3451', '111', '000', '123']
# 	comboBox1 = QComboBox()
# 	txt = (max(l, key=len))
# 	metrics = QFontMetrics(comboBox1.font())
# 	w = metrics.width(txt)
# 	comboBox1.setGeometry(QtCore.QRect(80, 5, 20, 20))
# 	comboBox1.setMinimumWidth(w)
#
# 	comboBox1.setObjectName(_fromUtf8("comboBox_2"))
# 	comboBox1.addItems(l)
# 	comboBox1.setSizeAdjustPolicy(QComboBox.AdjustToContents)
#
# 	grid.addWidget(comboBox1, 1, 1)
#
# 	l = ['123', '3451', '111', '000', '123']
# 	comboBox2 = QComboBox()
# 	txt = (max(l, key=len))
# 	metrics = QFontMetrics(comboBox2.font())
# 	w = metrics.width(txt)
# 	comboBox2.setGeometry(QtCore.QRect(80, 5, 20, 20))
# 	comboBox2.setMinimumWidth(w)
#
# 	comboBox2.setObjectName(_fromUtf8("comboBox_2"))
# 	comboBox2.addItems(l)
# 	comboBox2.setSizeAdjustPolicy(QComboBox.AdjustToContents)
# 	grid.addWidget(comboBox2, 2, 1)
#
# 	# centralwidget = QtGui.QWidget()
# 	# mainwin.setCentralWidget(centralwidget)
#
# 	# tabWidget = QtGui.QTabWidget(centralwidget)
# 	tabWidget = QTabWidget()
# 	tabWidget.setGeometry(QtCore.QRect(20, 20, 500, 500))
# 	tabWidget.setObjectName(_fromUtf8("tabWidget"))
# 	tab = QWidget()
# 	tab.setObjectName(_fromUtf8("tab"))
# 	tabWidget.addTab(tab, _fromUtf8(""))
# 	tab_2 = QWidget()
# 	tab_2.setObjectName(_fromUtf8("tab_2"))
# 	tabWidget.addTab(tab_2, _fromUtf8(""))
#
# 	tabWidget.setTabText(tabWidget.indexOf(tab), _translate("MainWindow", "Tab 1", None))
# 	tabWidget.setTabText(tabWidget.indexOf(tab_2), _translate("MainWindow", "Tab 2", None))
#
# 	tabWidget.setDocumentMode(True)
#
# 	# tabcentralwidget = QtGui.QWidget(centralwidget)
# 	# tabWidget.setCentralWidget(tabcentralwidget)
# 	# tabcentralwidget.setLayout(grid)
#
# 	tab.setLayout(grid)
#
# 	mainwin.setCentralWidget(tabWidget)
#
# 	mainwin.show()
# 	app.exec_()




import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Test(object):
	def setupUi(self, Test):
		Test.setObjectName("Test")
		Test.resize(852, 714)
		Test.setFixedSize(852, 714)
		self.lineEdit = QtWidgets.QLineEdit(Test)
		self.lineEdit.setGeometry(QtCore.QRect(150, 20, 200, 41))
		self.lineEdit.setObjectName("lineEdit")
		self.listWidget = QtWidgets.QListWidget(Test)
		self.listWidget.setGeometry(QtCore.QRect(0, 140, 420, 421))
		self.listWidget.setObjectName("listWidget")
		self.toolButton = QtWidgets.QToolButton(Test, clicked=lambda: self._resize(Test))
		self.toolButton.setGeometry(QtCore.QRect(0, 20, 41, 41))
		self.toolButton.setObjectName("toolButton")

		self.retranslateUi(Test)
		QtCore.QMetaObject.connectSlotsByName(Test)

	def retranslateUi(self, Test):
		_translate = QtCore.QCoreApplication.translate
		Test.setWindowTitle(_translate("Test", "Test"))
		self.toolButton.setText(_translate("Test", "<"))

	def _resize(self, Test):
		Test.resize(420, 714)  # 420, 714
		Test.setFixedSize(420, 714)
		self.listWidget.clear()  # 清空list


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Test()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())