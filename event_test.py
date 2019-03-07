#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import time


class Job(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Job, self).__init__(*args, **kwargs)
		self.__running = threading.Event()     # 用于暂停线程的标识
		self.__running.set()       # 设置为True
		self.__stop = threading.Event()      # 用于停止线程的标识，默认为False

	def run(self):
		print('run')
		while not self.__stop.isSet():
			self.__running.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
			print(time.time())
			time.sleep(1)

	def pause(self):
		print('pause')
		self.__running.clear()     # 设置为False, 让线程阻塞

	def resume(self):
		print('resume')
		self.__running.set()    # 设置为True, 让线程停止阻塞

	def stop(self):
		print('stop')
		if not self.__running.isSet():
			self.__running.set()       # 将线程从暂停状态恢复, 如果已经暂停的话
		self.__stop.set()        # 设置为True




if __name__ == '__main__':
	a = Job()
	a.start()
	time.sleep(3)
	a.pause()
	time.sleep(3)
	a.resume()
	time.sleep(3)
	a.pause()
	time.sleep(2)
	a.stop()
	input()