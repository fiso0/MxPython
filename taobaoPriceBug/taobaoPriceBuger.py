#!/usr/bin/python3
# -*- coding: utf-8 -*-

import taobaoPriceBug2

try:
	f = open('website_list.txt', 'r') # 打开商品地址列表文件
	for url in f.readlines():
		taobaoPriceBug2.price_bug(url) # 查找价格 成功后发送消息
	f.close()
except Exception as e:
	print(e)