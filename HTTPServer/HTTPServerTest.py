#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime,time
import http

def func():
	http.server(8080)

sched_time = datetime.datetime.now()+datetime.timedelta(seconds=1) #datetime.datetime(2018, 10, 15, 17, 31, 0)
loopflag = 0
while True:
	now = datetime.datetime.now()
	if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
		loopflag = 1
		time.sleep(1)
	if loopflag == 1:
		func() #此处为你自己想定时执行的功能函数
		loopflag = 0

if __name__ == '__main__':
	input()
	func()