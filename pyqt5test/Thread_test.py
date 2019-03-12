#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python多线程+PyQt综合使用，实现用UI上的按键控制进程的启停
用到了threading（多线程）模块的：
	Thread对象，isAlive()方法，start()方法，
	Event对象，set方法，clear方法
"""

import sys

from PyQt5.QtWidgets import *
import threading
import time


class UIExample(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.init_thread()

	def init_ui(self):
		# 设置UI
		self.text = QLineEdit()
		startBtn = QPushButton('开始')
		stopBtn = QPushButton('停止')

		startBtn.clicked.connect(self.start_btn_clicked)
		stopBtn.clicked.connect(self.stop_btn_clicked)

		box = QHBoxLayout()
		box.addWidget(self.text)
		box.addWidget(startBtn)
		box.addWidget(stopBtn)

		self.setLayout(box)
		self.setWindowTitle('测试多线程+事件')
		self.show()

	def init_thread(self):
		self.thread = threading.Thread(target=self.update_number) # 定义线程
		self.__running = threading.Event() # 定义开始事件，默认为False

	def update_number(self):
		self.number = 0
		while True: # 每0.1s数字加0.1
			self.__running.wait() # 等待开始事件为True
			self.text.setText(str(self.number)) # 输出数字值
			self.number = round(self.number + 0.1, 1) # 使用round避免精度误差
			time.sleep(0.1)

	def start_btn_clicked(self):
		if not self.thread.isAlive():
			self.thread.start()
		self.__running.set() # 设置开始事件为True

	def stop_btn_clicked(self):
		self.__running.clear() # 设置开始事件为False

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = UIExample()
	sys.exit(app.exec_())
