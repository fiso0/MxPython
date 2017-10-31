#!/usr/bin/python3
# -*- coding: utf-8 -*-


def get_driver_of(url):
	"""
	获取动态网页
	:param url:
	:return:
	"""
	from selenium import webdriver
	import time

	print('请等待...')

	# 使用selenium
	driver = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
	driver.maximize_window()

	driver.get(url)
	time.sleep(1)
	return driver


def get_soup_of(url):
	"""
	获取静态网页
	:param url:
	:return:
	"""
	import requests
	from bs4 import BeautifulSoup

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	return soup


if __name__ == '__main__':
	url = input('网址：')

	soup = get_soup_of(url)
	print(soup.prettify())
	# 示例：
	# price = int(soup.select_one('.tm-price').text[1:-1])

	driver = get_driver_of(url)
	# print(driver)
	# 示例：
	# prices = [e.text for e in driver.find_elements_by_class_name('tm-price')]
