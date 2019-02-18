#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QButtonGroup, QRadioButton, QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

EXAMPLE_1 = '''{"devicename":"866888020518396","battery":"100","datetime":"2019-1-16 11:02:08"}'''

EXAMPLE_2 = '''30 30 30 30 2c 31 33 38 30 38 36 32 38 38 36'''

EXAMPLE_3 = '''30 30 30 30 2c 31 33 38 30 38 36 32 38 38 36 33 2c 31 2c 30 30 30 30 30 30 30 30 30 30 30 30 31 30 30 30 30 30 30 30 30 30 30 30 32 30 30 30 30 30 30 30 30 30 30 30 2c 31 2c 30 31 30'''

EXAMPLE_4 = '''0000,13808628863,1,000000000000100000000000200000000000,1,010'''


class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		label1 = QLabel("需要校验的数据：")
		label2 = QLabel("校验计算结果（HEX）：")

		copy_btn1 = QPushButton('复制')
		copy_btn2 = QPushButton('复制')
		copy_btn1.setFixedWidth(60)
		copy_btn2.setFixedWidth(60)

		self.text1 = QTextEdit()
		self.text1.setAcceptRichText(False)
		self.text2 = QTextEdit()
		self.text2.setAcceptRichText(False)

		label3 = QLabel('输入格式：')
		self.formatGroup = QButtonGroup()
		self.format_ascii = QRadioButton('ASCII')
		self.format_hex = QRadioButton('HEX')
		self.format_hex.setChecked(True)
		self.formatGroup.addButton(self.format_ascii)
		self.formatGroup.addButton(self.format_hex)
		self.formatGroup.setExclusive(True)

		label4 = QLabel('校验长度：')
		# self.lengthGroup = QButtonGroup()
		# self.length_1 = QRadioButton('1')
		# self.length_1.setChecked(True)
		# self.length_2 = QRadioButton('2')
		# self.length_4 = QRadioButton('4')
		# self.lengthGroup.addButton(self.length_1)
		# self.lengthGroup.addButton(self.length_2)
		# self.lengthGroup.addButton(self.length_4)
		# self.lengthGroup.setExclusive(True)

		# self.format = QComboBox()
		# self.format.addItems(['ASCII', 'HEX'])
		# self.format.setCurrentIndex(1)

		self.length = QComboBox()
		self.length.addItems(['1','2','4'])

		btn1 = QPushButton('和校验 >>')
		btn2 = QPushButton('异或校验 >>')
		btn3 = QPushButton('CRC校验 >>')
		btn4 = QPushButton('预留')
		btn5 = QPushButton('预留')
		btn6 = QPushButton('预留')
		btn_clr = QPushButton('清空')

		leftGrid = QGridLayout()
		leftGrid.setSpacing(10)
		leftGrid.addWidget(label1, 1, 0)
		leftGrid.addWidget(label2, 1, 1)
		leftGrid.addWidget(self.text1, 2, 0)
		leftGrid.addWidget(self.text2, 2, 1)
		leftGrid.addWidget(copy_btn1, 3, 0)
		leftGrid.addWidget(copy_btn2, 3, 1)

		rightVBox = QVBoxLayout()
		rightVBox.setAlignment(Qt.AlignVCenter)
		rightVBox.addStretch()
		rightVBox.addWidget(label3)
		rightVBox.addWidget(self.format_hex)
		rightVBox.addWidget(self.format_ascii)
		rightVBox.addStretch()
		rightVBox.addWidget(label4)
		# rightVBox.addWidget(self.length_1)
		# rightVBox.addWidget(self.length_2)
		# rightVBox.addWidget(self.length_4)
		# rightVBox.addWidget(self.format)
		rightVBox.addWidget(self.length)
		rightVBox.addStretch()
		rightVBox.addWidget(btn1)
		rightVBox.addWidget(btn2)
		rightVBox.addWidget(btn3)
		# rightVBox.addWidget(btn4)
		# rightVBox.addWidget(btn5)
		# rightVBox.addWidget(btn6)
		rightVBox.addStretch()
		rightVBox.addWidget(btn_clr)

		mainBox = QHBoxLayout()
		mainBox.addLayout(leftGrid)
		mainBox.addLayout(rightVBox)

		self.setLayout(mainBox)

		# 按钮连接到槽
		btn1.clicked.connect(self.button1Clicked)
		btn2.clicked.connect(self.button2Clicked)
		btn3.clicked.connect(self.button3Clicked)
		btn4.clicked.connect(self.button4Clicked)
		btn5.clicked.connect(self.button5Clicked)
		btn6.clicked.connect(self.button6Clicked)
		btn_clr.clicked.connect(self.buttonClrClicked)

		copy_btn1.clicked.connect(self.copyButton1Clicked)
		# copy_btn2.clicked.connect(self.copyButton2Clicked)

		self.setGeometry(200, 300, 600, 350)
		self.setWindowTitle('校验码计算')
		self.show()

	def get_input(self):
		'''
		获取输入数据，按照选择的格式解析，得到输入数据的数值列表
		:return: 输入数据的数值列表
		例如：
		输入30 31 32，选择HEX，返回[48,49,50]
		输入abc，选择ASCII，返回[97,98,99]
		'''
		input_text = self.text1.toPlainText()
		if(input_text == ""):
			if self.format_ascii.isChecked(): # ASCII
				input_text = EXAMPLE_1
			elif self.format_hex.isChecked(): # HEX
				input_text = EXAMPLE_2
			self.text1.setPlainText(input_text)

		if self.format_ascii.isChecked(): # ASCII
			data = [ord(a) for a in input_text]
		elif self.format_hex.isChecked(): # HEX
			input_text = self.removeBlank(input_text)
			if len(input_text)%2 != 0: # 输入HEX数据必须是偶数长度
				self.text2.setPlainText('WRONG DATA!')
				return None
			input_text = self.addBlank(input_text)
			data = input_text.split()
			data = [int(a,16) for a in data]
		return data

	def set_output(self, output_result):
		length = int(self.length.currentText())
		if length == 1:
			result = output_result & 0xFF
			result_string = '0x%02X' % result
		elif length == 2:
			result = output_result & 0xFFFF
			result_string = '0x%04X' % result
		elif length == 4:
			result = output_result & 0xFFFFFFFF
			result_string = '0x%08X' % result
		return self.text2.setPlainText(result_string)

	def button1Clicked(self):  # 和
		try:
			string_origin = self.get_input()
			string_result = sum(string_origin)
			self.set_output(string_result)
		except Exception as e:
			self.text2.setPlainText(e)

	def button2Clicked(self):  # 异或
		try:
			string_origin = self.get_input()
			string_result = self.xor(string_origin, int(self.length.currentText()))
			self.set_output(string_result)
		except Exception as e:
			self.text2.setPlainText(e)

	def button3Clicked(self):  # CRC
		import crc16
		if int(self.length.currentText()) != 2:
			self.text2.setPlainText('目前只支持16位CRC校验，校验长度请选择2')
		else:
			try:
				string_origin = self.get_input()
				string_result = crc16.crc16_check(string_origin)
				self.set_output(string_result)
			except Exception as e:
				self.text2.setPlainText(e)

	def button4Clicked(self):  # 预留
		pass

	def button5Clicked(self):  # 预留
		pass

	def button6Clicked(self):  # 预留
		pass

	def buttonClrClicked(self):
		self.text1.setPlainText("")
		self.text2.setPlainText("")

	def copyButton1Clicked(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.text1.toPlainText())
		pass

	def u2c(self, data_str):
		'''
		转换unicode为字符
		unicode格式：每2个字节对应1个字符，字节间可以以空格、换行分隔，字节为十六进制，前面带或不带0x均可
		:param data_str:待转换内容
		:return:转换结果
		'''
		result = []

		if (len(data_str) < 3):
			return ''

		data = data_str.split()  # If sep is not specified or is None, any whitespace string is a separator and empty strings are removed from the result.

		for i in range(0, len(data) - 1, 2):
			try:
				a = int(data[i], 16)
				b = int(data[i + 1], 16)
				res = b'\\u%02x%02x' % (a, b)
				res1 = res.decode('unicode_escape')
				result.append(res1)
			# print(res1,end='')
			except Exception as e:
				print(e)
		return result

	def a2c(self, data_str):
		'''
		转换ascii码为字符
		ascii格式：每1个字节对应1个字符，字节间可以以空格、换行分隔，字节为十六进制，前面带或不带0x均可
		:param data_str:待转换内容
		:return:转换结果
		'''
		result = []

		data = data_str.split()

		for i in data:
			try:
				a = int(i, 16)
				result.append(chr(a))
			except Exception as e:
				print(e)
		return result

	def c2a(self, data_str):
		'''
		转换字符为ascii码
		:param data_str: 待转换内容
		:return: 转换结果
		'''
		result = []

		data = data_str

		for i in data:
			try:
				a = ord(i)
				result.append('0x%x' % a)
			except Exception as e:
				print(e)
		return result

	def addBlank(self, message):
		# 每两个字符之间加一个空格
		chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]
		return ' '.join(chrstr)

	def hex386(self, data_str):
		# 去掉第一行和最后两行
		# 每行格式为:LLAAAARRDD...DDDDCC，去掉开头9个字符和最后2个字符
		result = []
		data = data_str.split('\n')
		for i in data[1:-2]:  # 去掉第一行和最后两行
			try:
				a = i[9:-2]  # 去掉开头9个字符和最后2个字符
				result.append(a)
			except Exception as e:
				print(e)
		return result

	def removeBlank(self, message):
		# 去掉所有空字符（空格、换行）
		return ''.join(message.split())

	def xor(self, data, length=1):
		if length == 1:
			pass
		elif length == 2:
			if(len(data)%2 != 0):
				data.extend([0]) # 长度不为2的倍数时在末尾补0
			data = [(data[i]<<8)+data[i+1] for i in range(0, len(data), 2)] # 重新按长度为2字节解析数据
		elif length == 4:
			if(len(data)%4 != 0):
				data.extend([0] * (4-len(data)%4)) # 长度不为4的倍数时在末尾补0
			data = [(data[i]<<24)+(data[i+1]<<16)+(data[i+2]<<8)+data[i+3] for i in range(0, len(data), 4)] # 重新按长度为4字节解析数据
		result = 0
		for a in data:
			result = result ^ a
		return result

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
