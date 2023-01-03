#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import re
import time
import logging
logging.basicConfig(filename='logging.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


note='''
==重复测试导航院AGNSS服务器==
===连接/接收数据 耗时情况===

导航院服务器
域名	agnss-server-1.wh-mx.com
IP	27.17.32.34
端口	32101

GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=356674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1
'''

DELAY_SEC = 2
SERVER_DOMAIN = 'agnss-server-1.wh-mx.com'
SERVER_PORT = 32101
BUF_LEN = 1024
GET_DATA = b'GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=356674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1\r\n\r\n'


# 检查是否接收完整
def check_len(data):
	# 分离HTTP头和内容
	header, content=data.split(b'\r\n\r\n', 1)

	# 检查实际内容长度
	content_actual_len = len(content)

	# 获取应得内容长度
	try:
		content_desire_len = int(re.search(r'(content-length: )(\d*)',header.decode('utf-8')).group(2))
		print('content-length: ',str(content_desire_len),', received: ',str(content_actual_len))
		if content_actual_len == content_desire_len:
			cmp_res = True
		else:
			cmp_res = False
	except Exception as e:
		cmp_res = False
		logging.warning(str(e)+' [in check_len]')

	return cmp_res


# 结束后，写入csv文件
def log_result(same_len, try_cnt, time_of_connect, time_of_receive, fail_log):
	import csv
	filename = 'agnss_test_log.csv'

	if fail_log is not None:
		fail_str = '错误信息: '+fail_log+'\n'
	else:
		fail_str = ''

	f = False
	try:
	# NOTICE: the csv file will by default be decoded into unicode using the system default encoding, don't open with encoding='utf-8'
		f = open(filename, 'x', newline='') # 创建文件
		if f: # 创建成功，则写入标题行
			title = ['次数','结果','时间','连接耗时','接收耗时','备注']
			spam_writer = csv.writer(f)
			spam_writer.writerow(title)
	except FileExistsError: # 创建失败（文件已存在）
		try:
			f = open(filename, 'a', newline='') # 尝试以追加方式打开
		except PermissionError as e: # 打开失败（权限问题，例如该文件已被打开）
			print(e)
			logging.warning(str(e)+' [in log_result]')

	if f: # 如果文件已被成功打开，则写入内容
		line = [str(try_cnt),str(same_len),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'%.3fs'%(time_of_connect),'%.3fs'%(time_of_receive),fail_str]
		spam_writer = csv.writer(f)
		spam_writer.writerow(line)
		f.close()


# 失败时，把相关内容写入log文件
def log_fail(data, try_cnt, time_of_connect, time_of_receive, fail_log):
	filename = 'agnss_test_log_'+str(try_cnt)+'.log'

	with open(filename,'w',encoding='utf-8') as f:
		time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+'\n'
		info_str = '连接耗时: %.3fs\n接收耗时: %.3fs\n'%(time_of_connect,time_of_receive)
		if fail_log is not None:
			fail_str = '错误信息: '+fail_log+'\n'
		else:
			fail_str = ''
		seperator_str = '==============================\n\n'

		f.write(time_str+info_str+fail_str+seperator_str)
		f.write(data.decode('utf-8'))


def one_try(try_cnt):
	print('start one try...')
	time_start = time.time()

	# 设置超时时间
	# socket.setdefaulttimeout(10)

	# 创建一个socket 使用IPv4 TCP
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 建立连接
	s.connect((SERVER_DOMAIN,SERVER_PORT))
	time_connected = time.time()

	# 发送数据 获取内容
	s.send(GET_DATA)
	time_sent = time.time()

	buffer=[]
	same_len = False
	fail_log = None
	while True:
		# 每次最多接收BUF_LEN字节
		try:
			d=s.recv(BUF_LEN)
			if d:
				buffer.append(d)
				data=b''.join(buffer)
				# 检查是否接收完整
				same_len = check_len(data)
				if same_len: # 已接收完整
					time_received = time.time()
					break
			# 反复接收直到返回空 表示接收完毕
			else:
				# 关闭连接
				s.close()
				time_received = time.time()
		except Exception as e:
			fail_log = str(e)
			print(e)
			logging.warning(str(e)+' [in one_try]')
			# 关闭连接
			s.close()
			time_received = time.time()
			break

	# 计算耗时
	time_of_connect = time_connected-time_start
	time_of_receive = time_received-time_sent
	print('start-connect: %.3fs, sent-receive: %.3fs'%(time_of_connect,time_of_receive))

	# 写入csv文件
	log_result(same_len, try_cnt, time_of_connect, time_of_receive, fail_log)

	if not same_len:
		# 失败时，把具体内容写入文件
		log_fail(data, try_cnt, time_of_connect, time_of_receive, fail_log)

	return same_len

print(note)
input("按任意键开始测试...")

try_cnt = 0
success_cnt = 0
fail_cnt = 0

while(True):
	try_cnt += 1
	try:
		if(one_try(try_cnt)):
			success_cnt += 1
		else:
			fail_cnt += 1
		print(time.strftime('%H:%M',time.localtime()), '>>> Total: ',str(try_cnt),', Success: ',str(success_cnt),', Fail: ',str(fail_cnt))
	except Exception as e:
		print(e)
		logging.warning(str(e)+' [in main]')
	finally:
		print('sleep %ds...'%(DELAY_SEC))
		time.sleep(DELAY_SEC)
