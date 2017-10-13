#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import requests

def send_notice(product, prices):
	text = (product if (product is not None) else '') + '降价啦'
	desp = prices[0] + '降到' + prices[1]
	content = "https://sc.ftqq.com/SCU13848Tc8c8c82df0c2f7a251d8676d2d87245a59e029d80bf3e.send?text=%s&desp=%s" % (
	text, desp)
	requests.get(content)
	print('已下发方糖消息')


# 使用selenium
driver = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
driver.maximize_window()

url = input('商品地址：')
# 测试：https://detail.tmall.com/item.htm?spm=a230r.1.14.8.5de81d2cSXh2qL&id=555790918859&cm_id=140105335569ed55e27b&abbucket=11
driver.get(url)
print('请等待...')
time.sleep(1)

try:
	prices = [e.text for e in driver.find_elements_by_class_name('tm-price')]
	try:
		print('商品原价：' + prices[0] + '\n商品优惠价：' + prices[1])
		send_notice(None, prices)
	except:
		print('查询结果：' + str(prices))
except:
	print('查询价格失败')
