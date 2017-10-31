#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 天才枪手页面：https://gaoqing.fm/view/3763566ec44a
# 首页：https://gaoqing.fm

import sys
sys.path.append('..')
import WebBug.WebBug
import pprint

def scan_all_new():
	url = 'https://gaoqing.fm'
	soup = WebBug.WebBug.get_soup_of(url)
	film_tags = soup("div", "item-desc pull-left")
	
	good_films = dict()
	for tag in film_tags:
		ttag = tag('a')[0]
		href = ttag.get('href')
		desc = tag.text.strip()
		name,score = desc.split(' ')
		score = float(score)
		if(score >= 7):
			good_films[name] = [href,score]
	
	return(good_films)
	
def save_file(result):
	try:
		with open('gaoqing.fm','w') as file:
			file.write(result)
	except:
		print('file error')

if __name__ == '__main__':
	good_films = scan_all_new()
	save_file(pprint.pformat(good_films))
	input('done')
	# url = input('网址：')
	# soup = WebBug.WebBug.get_soup_of(url)
	# all = soup.select('#all').text
