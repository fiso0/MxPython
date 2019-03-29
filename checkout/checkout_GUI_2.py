import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

EXAMPLE_1 = '''{"devicename":"866888020518396","battery":"100","datetime":"2019-1-16 11:02:08"}'''

EXAMPLE_2 = '''30 30 30 30 2c 31 33 38 30 38 36 32 38 38 36'''

class GUI(QWidget):
	def __init__(self):
		super().__init__()
		self.ui_init()

	def ui_init(self):
		# 组件
		label1 = QLabel("需要校验的数据：")
		label2 = QLabel("校验计算结果（HEX）：")

		self.text1 = QTextEdit()
		self.text1.setAcceptRichText(False)
		self.text2 = QTextEdit()
		self.text2.setAcceptRichText(False)

		self.filename_text = QLineEdit('文件名')
		self.filename_text.setEnabled(False)
		file_btn = QPushButton('文件')
		file_btn.setFixedWidth(60)

		copy_btn1 = QPushButton('复制')
		copy_btn2 = QPushButton('复制')
		copy_btn1.setFixedWidth(60)
		copy_btn2.setFixedWidth(60)

		label3 = QLabel('输入格式：')
		label4 = QLabel('校验长度：')
		label5 = QLabel('校验方法：')
		label6 = QLabel('字节顺序：')

		self.format = QComboBox()
		self.format.addItems(['HEX', 'ASCII'])

		self.length = QComboBox()
		self.length.addItems(['1','2','4'])

		self.method = QComboBox()
		self.method.addItems(['和校验','进位和校验','异或校验','CRC校验'])

		self.flow = QComboBox()
		self.flow.addItems(['大端模式', '小端模式'])

		# 默认不显示字节顺序项
		self.flow.setEnabled(False)

		check_btn = QPushButton('计算')
		clr_btn = QPushButton('清空')

		# 布局
		leftBox = QVBoxLayout()
		fileBox = QHBoxLayout()
		rightBox = QVBoxLayout()
		toolBox = QVBoxLayout()
		mainBox = QHBoxLayout()

		fileBox.addWidget(label1)
		fileBox.addWidget(self.filename_text)
		fileBox.addWidget(file_btn)

		leftBox.addLayout(fileBox)
		leftBox.addWidget(self.text1)
		leftBox.addWidget(copy_btn1)

		rightBox.addWidget(label2)
		rightBox.addWidget(self.text2)
		rightBox.addWidget(copy_btn2)

		toolBox.addWidget(label3)
		toolBox.addWidget(self.format)
		toolBox.addWidget(label5)
		toolBox.addWidget(self.method)
		toolBox.addWidget(label4)
		toolBox.addWidget(self.length)
		toolBox.addWidget(label6)
		toolBox.addWidget(self.flow)
		toolBox.addStretch()
		toolBox.addWidget(check_btn)
		toolBox.addWidget(clr_btn)

		mainBox.addLayout(leftBox)
		mainBox.addLayout(rightBox)
		mainBox.addLayout(toolBox)

		self.setLayout(mainBox)

		# 连接
		file_btn.clicked.connect(self.open_file)
		self.method.currentIndexChanged.connect(self.method_changed)
		clr_btn.clicked.connect(self.buttonClrClicked)
		copy_btn1.clicked.connect(self.copyButton1Clicked)
		copy_btn2.clicked.connect(self.copyButton2Clicked)
		check_btn.clicked.connect(self.checkClicked)

		self.resize(600, 350)
		self.setWindowTitle('校验码计算')
		self.show()

	def method_changed(self):
		method = self.method.currentText()
		if method == '进位和校验':
			# 显示字节顺序项
			self.flow.setEnabled(True)
		else:
			self.flow.setEnabled(False)

		if method == 'CRC校验':
			# 只支持16位CRC校验
			self.length.clear()
			self.length.addItem('2')
		else:
			self.length.clear()
			self.length.addItems(['1', '2', '4'])

	def open_file(self):
		file = QFileDialog.getOpenFileName(self, '选择文件')
		filename = file[0]
		self.filename_text.setText(filename)
		self.filename_text.setToolTip(filename)

		# 读取文件
		if filename.endswith('bin'):
			with open(filename, 'rb') as f:
				data = f.read()
			data = ' '.join(['%02X'%x for x in bytes(data)])

			# bin文件，自动设置输入格式为HEX，校验方法为进位和校验，校验长度为4，字节顺序为小端模式
			self.format.setCurrentText('HEX')
			self.method.setCurrentText('进位和校验')
			self.length.setCurrentText('4')
			self.flow.setCurrentText('小端模式')
		else:
			with open(filename, 'r', encoding='utf-8') as f:
				data = f.read()
			self.format.setCurrentText('ASCII')
		self.text1.setText(data)

	def buttonClrClicked(self):
		self.text1.setPlainText("")
		self.text2.setPlainText("")

	def copyButton1Clicked(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.text1.toPlainText())

	def copyButton2Clicked(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.text2.toPlainText())

	def checkClicked(self):
		self.set_output("")  # 清空输出
		string_origin = self.get_input(self.text1.toPlainText())  # 获取输入
		method = self.method.currentText()  # 获取校验方法

		# 计算
		try:
			if method == '和校验':
				string_result = sum(string_origin)
			elif method == '异或校验':
				string_result = self.xor(string_origin, int(self.length.currentText()))
			elif method == 'CRC校验':
				import crc16
				string_result = crc16.crc16_check(string_origin)
			elif method == '进位和校验':
				string_result = self.sum_long(string_origin, int(self.length.currentText()))
			self.set_output(string_result)
		except Exception as e:
			self.set_output('ERROR: ' + str(e), True)

	def set_output(self, output_result, is_error=False):
		if is_error:  # 错误提示以红色字体显示
			if len(self.text2.toPlainText()):  # 若已有内容，在最后插入换行
				self.text2.moveCursor(QTextCursor.End)
				self.text2.insertPlainText('\r\n')
			self.text2.insertHtml('<span style="color:red">' + output_result + '</span>')
			return

		if output_result == '':  # 清空输出
			self.text2.setPlainText(output_result)
			return

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

	def get_input(self, input_text):
		'''
		获取输入数据，按照选择的格式解析，得到输入数据的数值列表
		:return: 输入数据的数值列表
		例如：
		输入30 31 32，选择HEX，返回[48,49,50]
		输入abc，选择ASCII，返回[97,98,99]
		'''
		current_format = self.format.currentText()
		if(input_text == ""):
			if current_format == 'ASCII': # ASCII
				input_text = EXAMPLE_1
			elif current_format == 'HEX': # HEX
				input_text = EXAMPLE_2
			self.text1.setPlainText(input_text)

		if current_format == 'ASCII': # ASCII
			data = [ord(a) for a in input_text]
		elif current_format == 'HEX': # HEX
			input_text = self.removeBlank(input_text)
			if len(input_text)%2 != 0: # 输入HEX数据必须是偶数长度
				self.set_output('输入HEX数据必须是偶数长度!', True)
				return None
			input_text = self.addBlank(input_text)
			data = input_text.split()
			data = [int(a,16) for a in data]

		QApplication.processEvents()  # 刷新显示
		return data

	def removeBlank(self, message):
		# 去掉所有空字符（空格、换行）
		return ''.join(message.split())

	def addBlank(self, message):
		# 每两个字符之间加一个空格
		chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]
		return ' '.join(chrstr)

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

	def sum_long(self, data, length):
		if length == 1:
			pass
		elif length == 2:
			if (len(data) % 2 != 0):
				data.extend([0])  # 长度不为2的倍数时在末尾补0
			if self.flow.currentText() == '大端模式':
				data = [(data[i] << 8) + data[i + 1] for i in range(0, len(data), 2)]  # 重新按长度为2字节解析数据
			else:
				data = [(data[i + 1] << 8) + data[i] for i in range(0, len(data), 2)]  # 重新按长度为2字节解析数据
		elif length == 4:
			if (len(data) % 4 != 0):
				data.extend([0] * (4 - len(data) % 4))  # 长度不为4的倍数时在末尾补0
			if self.flow.currentText() == '大端模式':
				data = [(data[i] << 24) + (data[i + 1] << 16) + (data[i + 2] << 8) + data[i + 3] for i in
				        range(0, len(data), 4)]  # 重新按长度为4字节解析数据
			else:
				data = [(data[i + 3] << 24) + (data[i + 2] << 16) + (data[i + 1] << 8) + data[i] for i in
				        range(0, len(data), 4)]  # 重新按长度为4字节解析数据
		result = sum(data)
		return result

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = GUI()
	sys.exit(app.exec_())
