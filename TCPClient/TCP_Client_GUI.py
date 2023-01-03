#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 2021-9-16实测TCP_Client_GUI.py：异常

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QButtonGroup, QRadioButton, QLineEdit, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		# widgets
		label1 = QLabel("IP")
		label2 = QLabel("端口")
		self.host = QLineEdit("")
		self.port = QLineEdit("")
		btn1 = QPushButton('连接')
		btn2 = QPushButton('发送')
		self.text_r = QTextEdit()
		self.text_r.setAcceptRichText(False)
		self.text_t = QTextEdit()
		self.text_t.setAcceptRichText(False)

		# layouts
		mainBox = QVBoxLayout()
		paraBox = QHBoxLayout()
		paraBox.addWidget(label1)
		paraBox.addWidget(self.host)
		paraBox.addWidget(label2)
		paraBox.addWidget(self.port)
		paraBox.addWidget(btn1)
		transBox = QHBoxLayout()
		transBox.addWidget(self.text_t)
		transBox.addWidget(btn2)
		mainBox.addLayout(paraBox)
		mainBox.addWidget(self.text_r)
		mainBox.addLayout(transBox)
		self.setLayout(mainBox)

		# actions
		btn1.clicked.connect(self.button1Clicked)
		btn2.clicked.connect(self.button2Clicked)

		# others
		self.setGeometry(200, 300, 600, 350)
		self.setWindowTitle('TCP Client')
		self.show()

	def button1Clicked(self):
		import TCP_Client
		ip = self.host.text()
		port = int(self.port.text())
		client = TCP_Client.start_socket(ip, port)

	def button2Clicked(self):
		# client.send("123")
		pass

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
