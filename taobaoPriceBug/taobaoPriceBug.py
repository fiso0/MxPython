#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 本代码尝试使用BS4静态读取页面内容，但由于价格部分使用了动态显示，无法获取

from bs4 import BeautifulSoup
import requests
import urllib
import os
import sys
import time


def get_soup_of(url):
	"""获取某个url的soup
	:param url: 待获取的网页地址
	"""
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	return (soup)

	
if __name__ == '__main__':
	URL = input('商品网址：')

	# get current page
	soup = get_soup_of(URL)
	price = int(soup.select_one('.tm-price').text[1:-1]) # Find only the first tag that matches a selector(class="tm-price")