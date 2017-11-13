#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QTextEdit,QGridLayout,QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import Qt

EXAMPLE_1 = '''0x5C 0xA 0x65 0x6C 0x76 0x84 0x5B 0xA2 0x62 0x37 0xFF 0xC 0x60 0xA8 0x59 0x7D 0xFF 0x1 0x62 0x63 0x96 0x64 0x60 0xA8 0x5D 0xF2 0x4E 0xA7 0x75 0x1F 0x76 0x84 0x6D 0x88 0x8D 0x39 0xFF 0x8 0x0 0x30 0x0 0x2E 0x0 0x35 0x0 0x39 0x51 0x43 0xFF 0xC 0x51 0x76 0x4E 0x2D 0x67 0x2C 0x67 0x8 0x6D 0x88 0x8D 0x39 0x0 0x30 0x0 0x2E 0x0 0x35 0x0 0x39 0x51 0x43 0x30 0x1 0x4E 0xA 0x67 0x8 0x53 0xCA 0x4E 0xE5 0x52 0x4D 0x76 0x84 0x53 0x86 0x53 0xF2 0x6D 0x88 0x8D 0x39 0x0 0x30 0x0 0x2E 0x0 0x30 0x0 0x30 0x51 0x43 0xFF 0x9 0x54 0xE 0xFF 0xC 0x60 0xA8 0x5F 0x53 0x52 0x4D 0x4F 0x59 0x98 0x9D 0x0 0x34 0x0 0x34 0x0 0x2E 0x0 0x35 0x0 0x31 0x51 0x43 0x30 0x2'''

EXAMPLE_2 = '''尊敬的客户，您好！扣除您已产生的消费（0.59元，其中本月消费0.59元、上月及以前的历史消费0.00元）后，您当前余额44.51元。'''

EXAMPLE_3 = '''30 30 30 30 2c 31 33 38 30 38 36 32 38 38 36 33 2c 31 2c 30 30 30 30 30 30 30 30 30 30 30 30 31 30 30 30 30 30 30 30 30 30 30 30 32 30 30 30 30 30 30 30 30 30 30 30 2c 31 2c 30 31 30'''

EXAMPLE_4 = '''0000,13808628863,1,000000000000100000000000200000000000,1,010'''

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.label1 = QLabel("待转换内容：（字符以空格或回车分隔）")
		self.label2 = QLabel("转换结果：")

		self.text1 = QTextEdit()
		self.text1.setAcceptRichText(False)
		self.text2 = QTextEdit()
		self.text2.setAcceptRichText(False)
		self.btn1 = QPushButton('短信转中文 >>')
		self.btn2 = QPushButton('ASCII转字符 >>')
		self.btn3 = QPushButton('每2个字符加空格 >>')
		self.btn_clr = QPushButton('清空')

		leftGrid = QGridLayout()
		leftGrid.setSpacing(10)
		leftGrid.addWidget(self.label1,1,0)
		leftGrid.addWidget(self.label2,1,1)
		leftGrid.addWidget(self.text1,2,0)
		leftGrid.addWidget(self.text2,2,1)

		rightVBox = QVBoxLayout()
		rightVBox.setAlignment(Qt.AlignVCenter)
		rightVBox.addStretch()
		rightVBox.addWidget(self.btn1)
		rightVBox.addWidget(self.btn2)
		rightVBox.addWidget(self.btn3)
		rightVBox.addStretch()
		rightVBox.addWidget(self.btn_clr)

		mainBox = QHBoxLayout()
		mainBox.addLayout(leftGrid)
		mainBox.addLayout(rightVBox)

		self.setLayout(mainBox)

		# 按钮连接到槽
		self.btn1.clicked.connect(self.button1Clicked)
		self.btn2.clicked.connect(self.button2Clicked)
		self.btn3.clicked.connect(self.button3Clicked)
		self.btn_clr.clicked.connect(self.buttonClrClicked)

		self.setGeometry(200,300,600,350)
		self.setWindowTitle('字符转换')
		self.show()

	def button1Clicked(self):
		string_origin = self.text1.toPlainText()
		if(string_origin is not ""):
			try:
				string_result = self.u2c(string_origin)
				self.text2.setPlainText(''.join(string_result))
			except:
				self.text2.setPlainText('ERROR!')
		else:
			self.text1.setPlainText(EXAMPLE_1)
			self.text2.setPlainText(EXAMPLE_2)
		# print(string_result)

	def button2Clicked(self):
		string_origin = self.text1.toPlainText()
		if(string_origin is not ""):
			try:
				string_result = self.a2c(string_origin)
				self.text2.setPlainText(''.join(string_result))
			except:
				self.text2.setPlainText('ERROR!')
		else:
			self.text1.setPlainText(EXAMPLE_3)
			self.text2.setPlainText(EXAMPLE_4)

	def button3Clicked(self):
		string_origin = self.text1.toPlainText()
		# try:
		# 	string_result = addBlank(string_origin)
		# 	self.text2.setPlainText(string_result)
		if(string_origin is not ""):
			try:
				string_result = self.addBlank(string_origin)
				self.text2.setPlainText(''.join(string_result))
			except:
				self.text2.setPlainText('ERROR!')
		else:
			self.text1.setPlainText(EXAMPLE_1)
			self.text2.setPlainText(EXAMPLE_2)
	def buttonClrClicked(self):
		self.text1.setPlainText("")
		self.text2.setPlainText("")

	def u2c(self,data_str):
		result=[]
		if('\n' in data_str):
			data = data_str.split('\n')
		elif(' ' in data_str):
			data = data_str.split(' ')
		else:
			data = [data_str]
		# print(data)
		for i in range(0,len(data)-1,2):
			try:
				a = int(data[i].strip().replace("0x",""),16)
				b = int(data[i+1].strip().replace("0x",""),16)
				res=b'\\u%02x%02x'%(a,b)
				res1=res.decode('unicode_escape')
				result.append(res1)
				# print(res1,end='')
			except Exception as e:
				print(e)
		return result

	def a2c(self,data_str):
		result=[]
		if('\n' in data_str):
			data = data_str.split('\n')
		elif(' ' in data_str):
			data = data_str.split(' ')
		else:
			data = [data_str]
		for i in data:
			try:
				a = int(i,16)
				result.append(chr(a))
			except Exception as e:
				print(e)
		return result

	def addBlank(self,message):
		# 每两个字符之间加一个空格
		chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]
		return ' '.join(chrstr)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())