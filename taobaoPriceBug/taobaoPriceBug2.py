#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

#使用selenium
driver = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
driver.maximize_window()

url = input('商品地址：')
driver.get(url)
print('请等待...')
time.sleep(1)

try:
	prices = [e.text for e in driver.find_elements_by_class_name('tm-price')]
	try:
		print('商品原价：'+prices[0]+'\n商品优惠价：'+prices[1])
	except:
		print('查询结果：'+str(prices))
except:
	print('查询价格失败')
