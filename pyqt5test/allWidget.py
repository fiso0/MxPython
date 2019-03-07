#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys

class allWidget(QWidget):
	def __init__(self, parent=None):
		super(allWidget, self).__init__(parent)
		QLabel_label = QLabel("QLabel")
		QLabel_widget = QLabel("QLabel")

		QSlider_label = QLabel("QSlider")
		QSlider_widget = QSlider(Qt.Horizontal)

		QLCDNumber_label = QLabel("QLCDNumber")
		QLCDNumber_widget = QLCDNumber()
		QLCDNumber_widget.display("42")

		QLineEdit_label = QLabel("QLineEdit")
		QLineEdit_widget = QLineEdit("QLineEdit")

		QTextEdit_label = QLabel("QTextEdit")
		QTextEdit_widget = QTextEdit()

		QPushButton_label = QLabel("QPushButton")
		QPushButton_widget = QPushButton("QPushButton")

		QRadioButton_label = QLabel("QRadioButton")
		QRadioButton_widget = QRadioButton("QRadioButton")

		QScrollBar_label = QLabel("QScrollBar")
		QScrollBar_widget = QScrollBar(Qt.Horizontal)

		QComboBox_label = QLabel("QComboBox")
		QComboBox_widget = QComboBox()
		QComboBox_widget.addItems(['QComboBox 1','QComboBox 2','QComboBox 3'])

		QCheckBox_label = QLabel("QCheckBox")
		QCheckBox_widget = QCheckBox("QCheckBox")

		QCalendarWidget_label = QLabel("QCalendarWidget")
		QCalendarWidget_widget = QCalendarWidget()

		QDateTimeEdit_label = QLabel("QDateTimeEdit")
		QDateTimeEdit_widget = QDateTimeEdit()
		QDateTimeEdit_widget.setCalendarPopup(True)

		QProgressBar_label = QLabel("QProgressBar")
		QProgressBar_widget = QProgressBar()
		QProgressBar_widget.setValue(42)

		statusBar_widget = QStatusBar()
		statusBar_widget.showMessage("QStatusBar")

		grid = QGridLayout()
		grid.addWidget(QLabel_label,1,0)
		grid.addWidget(QLabel_widget,1,1)
		grid.addWidget(QSlider_label,2,0)
		grid.addWidget(QSlider_widget,2,1)
		grid.addWidget(QLCDNumber_label,3,0)
		grid.addWidget(QLCDNumber_widget,3,1)
		grid.addWidget(QLineEdit_label,4,0)
		grid.addWidget(QLineEdit_widget,4,1)
		grid.addWidget(QTextEdit_label,5,0)
		grid.addWidget(QTextEdit_widget,5,1)
		grid.addWidget(QPushButton_label,6,0)
		grid.addWidget(QPushButton_widget,6,1)
		grid.addWidget(QRadioButton_label,7,0)
		grid.addWidget(QRadioButton_widget,7,1)
		grid.addWidget(QScrollBar_label,8,0)
		grid.addWidget(QScrollBar_widget,8,1)
		grid.addWidget(QComboBox_label,9,0)
		grid.addWidget(QComboBox_widget,9,1)
		grid.addWidget(QCheckBox_label,10,0)
		grid.addWidget(QCheckBox_widget,10,1)
		grid.addWidget(QCalendarWidget_label,11,0)
		grid.addWidget(QCalendarWidget_widget,11,1)
		grid.addWidget(QDateTimeEdit_label,12,0)
		grid.addWidget(QDateTimeEdit_widget,12,1)
		grid.addWidget(QProgressBar_label,13,0)
		grid.addWidget(QProgressBar_widget,13,1)

		grid.addWidget(statusBar_widget,18,0)

		self.setLayout(grid)
		self.setWindowTitle("Widget Example")
		# self.resize(300,200)
		self.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = allWidget()
	sys.exit(app.exec_())