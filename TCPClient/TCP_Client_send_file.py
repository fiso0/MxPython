#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 2021-9-16实测TCP_Client.py：ok

"""
建立TCP client，然后新建2个线程分别用于接收和发送数据
"""

from socket import *
import threading

HOST = '139.196.252.69'
PORT = 333

FILENAME = 'obs.log'

SIZE_PER_SEND = 1024 # 单笔发送数据量
SEND_GAP = 500 # ms (0.5s) 多笔数据发送间隔
# FILE_GAP = 300000 # ms (5min) 多个文件处理间隔

BUF_SIZE = 2048


def create_socket(host, port):
	"""
	建立TCP client
	:param host:
	:param port:
	:return:
	"""
	address = (host, port)
	client = socket(AF_INET, SOCK_STREAM)
	client.connect(address)
	return client


def receive(client):
	"""
	接收数据
	:param client:
	:return:
	"""
	while True:
		data = client.recv(BUF_SIZE)
		if data:
			print(data)

def read_file():
	f = FILENAME
	lines = None
	try:
		with open(f, 'rb') as file:
			lines = file.read(SIZE_PER_SEND)
	except Exception as e:
		print(e)
	return lines

def transmit(client):
	"""
	发送数据
	:param client:
	:return:
	"""
	while True:
		# data = input('>')
		# 读文件
		f = FILENAME
		try:
			with open(f, 'rb') as file:
				while True:
					line = file.read(SIZE_PER_SEND)
					read_len = len(line)
					file.seek(read_len, 1)
					client.send(line)
					if(read_len < SIZE_PER_SEND):
						break
		except Exception as e:
			print(e)



def start_socket(host, port):
	tcp_client = create_socket(host, port)  # 建立TCP client
	t_r = threading.Thread(target=receive, args=(tcp_client,))  # 新建线程用于接收数据
	t_t = threading.Thread(target=transmit, args=(tcp_client,))  # 新建线程用于发送数据
	t_r.start()  # 启动线程
	t_t.start()  # 启动线程


if __name__ == '__main__':
	start_socket(HOST, PORT)
