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


def transmit(client):
	"""
	发送数据
	:param client:
	:return:
	"""
	while True:
		data = input('>')
		if data:
			client.send(data.encode("utf-8"))


def start_socket(host, port):
	tcp_client = create_socket(host, port)  # 建立TCP client
	t_r = threading.Thread(target=receive, args=(tcp_client,))  # 新建线程用于接收数据
	t_t = threading.Thread(target=transmit, args=(tcp_client,))  # 新建线程用于发送数据
	t_r.start()  # 启动线程
	t_t.start()  # 启动线程


if __name__ == '__main__':
	start_socket(HOST, PORT)
