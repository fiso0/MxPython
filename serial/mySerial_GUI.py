#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import serial  # 导入模块
import threading

class MySerial(object):
	def __init__(self):
		self.STRGLO = ""  # 读取的数据
		self.BOOL = True  # 读取标志位

		# self.STRSEND = "" # 待发送的数据
		# self.INPUT_DONE = False # 待发送数据准备完毕标识位
		# self.SEND_BOOL = True # 发送标识位
	
	# 读数代码本体实现
	def ReadData(self, ser):
		# 循环接收数据，此为死循环，可用线程实现
		while self.BOOL:
			if ser.in_waiting:
				self.STRGLO = ser.read(ser.in_waiting).decode("utf-8", errors='ignore')
				print(self.STRGLO, end='')
	
	# 新增：发送字符串
	# def SendData(ser):
		# while self.SEND_BOOL:
			# if ser.in_waiting and self.INPUT_DONE:
				# result = ser.write(self.STRSEND + "\r\n")
				# if result:
					# self.INPUT_DONE = False
					
	# 打开串口
	# 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
	# 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
	# 超时设置：None为永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
	def DOpenPort(self, portx, bps, timeout):
		ret = False
		try:
			# 打开串口，并得到串口对象
			ser = serial.Serial(portx, bps, timeout=timeout)
			# 判断是否打开成功
			if (ser.is_open):
				ret = True
				threading.Thread(target=self.ReadData, args=(ser,)).start()
				# threading.Thread(target=self.SendData, args=(ser,)).start()
		except Exception as e:
			print("---异常---：", e)
		return ser, ret
	
	
	# 关闭串口
	def DColsePort(self, ser):
		self.BOOL = False
		ser.close()
	
	
	# 写数据
	def DWritePort(self, ser, text):
		result = ser.write(text.encode("gbk"))  # 写数据
		return result
	
	
	# 读数据
	def DReadPort(self):
		str = self.STRGLO
		self.STRGLO = ""  # 清空当次读取
		return str

	

# if __name__ == '__main__':
# 	s = MySerial()
# 	ser, ret = s.DOpenPort("COM1", 19200, None) # 自动开始接收
# 	print('ret=' + str(ret))
# 	# if (ret == True):  # 判断串口是否成功打开
# 		# count=DWritePort(ser,"我是东小东，哈哈")
# 		# print("写入字节数：",count)
# 		# s.DReadPort()  # 读串口数据
# 		# DColsePort(ser)  #关闭串口
# 	input()



import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QButtonGroup, QRadioButton, \
	QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import time

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.s = MySerial()
		self.initUI()

	def initUI(self):
		mainBox = QVBoxLayout()
		txBox = QHBoxLayout()

		self.rxText = QTextEdit()
		self.txText = QLineEdit()
		txBtn = QPushButton('发送')

		mainBox.addWidget(self.rxText)
		mainBox.addLayout(txBox)
		txBox.addWidget(self.txText)
		txBox.addWidget(txBtn)

		self.setLayout(mainBox)

		# 按钮连接到槽
		txBtn.clicked.connect(self.tx)

		self.setGeometry(200, 300, 700, 500)
		self.setWindowTitle('log解析工具')
		self.show()

		self.init_port()

	def init_port(self):
		self.ser, ret = self.s.DOpenPort("COM33", 921600, None) # 自动开始接收
		threading.Thread(target=self.update_rx, args=()).start()

	def update_rx(self):
		try:
			self.rxText.moveCursor(QTextCursor.End) # 使用insertPlainText需保证cursor在末尾
			self.rxText.insertPlainText(self.s.STRGLO)
			QApplication.processEvents()
		except Exception as e:
			print(e)

	def tx(self):
		# pass
		sendStr = "showBaudRate()" # self.txText.text()
		self.s.DWritePort(self.ser, sendStr)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())