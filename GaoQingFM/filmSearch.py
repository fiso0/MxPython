#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 搜索：https://gaoqing.fm/s.php?q=光辉岁月

import sys
sys.path.append('..')
import WebBug.WebBug
import re

def search_film(film_name):
	url = 'https://gaoqing.fm/s.php?q=' + film_name.strip()
	soup = WebBug.WebBug.get_soup_of(url)
	result = soup.find(text=re.compile("相关搜索"))

if __name__ == '__main__':
	search_film('小丑回魂')
	input('done')
	
