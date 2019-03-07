#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
多线程+信号+事件综合使用，实现用UI上的按键控制进程的启停，子线程执行计算并发信号实现UI刷新
用到了threading（多线程）模块的：
	Thread对象，isRunning()方法，start()方法，
	Event对象，set()方法，clear()方法
自定义线程类MyThread继承QThread（信号功能）：
	pyqtSignal对象，emit()方法，connect()方法
"""

import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
import threading
import time


class MyThread(QThread):
	# 线程类需要继承QThread，才能使用信号功能

	# 定义全局信号（PyQt5信号要定义为类属性，而不是放在 _init_这个方法里面）
	# 如果要传递参数，则括号内要填入参数的类型！
	signal = pyqtSignal(int)  # 定义信号，传递int类型参数

	def __init__(self):
		super().__init__()
		self.__running = threading.Event()  # 定义事件，控制线程启停，默认为False
		self.number = 0  # 数据

	def __del__(self):
		self.wait()

	def run(self):  # 线程运行，每0.1s数字加1
		while True:
			self.__running.wait()  # 阻塞等待事件为True
			self.number += 1
			self.signal.emit(self.number)  # 发送信号，输出数字值
			time.sleep(0.1)

	def pause(self):  # 暂停线程
		self.__running.clear()  # 设置开始事件为False，使线程阻塞

	def resume(self):  # 恢复线程
		self.__running.set()  # 设置开始事件为True，使线程恢复运行


class UI(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()  # 初始化UI
		self.init_thread()  # 初始化线程
		self.init_signal()  # 初始化信号

	def init_ui(self):
		# 设置UI
		self.text = QLineEdit()
		start_btn = QPushButton('开始')
		stop_btn = QPushButton('停止')

		start_btn.clicked.connect(self.start_btn_clicked)
		stop_btn.clicked.connect(self.stop_btn_clicked)

		box = QHBoxLayout()
		box.addWidget(self.text)
		box.addWidget(start_btn)
		box.addWidget(stop_btn)

		self.setLayout(box)
		self.setWindowTitle('测试多线程+信号+事件')
		self.show()

	def init_thread(self):
		self.thread = MyThread()  # 定义线程

	def init_signal(self):
		self.thread.signal.connect(self.signal_handle)  # 绑定信号处理函数

	def signal_handle(self, number):  # 信号处理函数
		self.text.setText(str(number))  # 显示数字

	def start_btn_clicked(self):  # 启动/恢复线程
		if not self.thread.isRunning():
			self.thread.start()
		self.thread.resume()  # 设置开始事件为True

	def stop_btn_clicked(self):  # 暂停线程
		self.thread.pause()  # 设置开始事件为False


if __name__ == '__main__':
	try:
		app = QApplication(sys.argv)
		ex = UI()
		sys.exit(app.exec_())
	except Exception as e:
		print(e)
