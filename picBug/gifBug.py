from bs4 import BeautifulSoup
import requests
import urllib
import os
import sys
import time

URL = 'http://jandan.net/ooxx'
DIR = os.getcwd() + '\\gif'
PAGES = 10 # total pages to scan

def get_soup_of(url):
	"""获取某个url的soup
	:param url: 待获取的网页地址
	"""
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	return (soup)

if __name__ == '__main__':
	# get current page
	soup = get_soup_of(URL)
	page = int(soup.select_one('.current-comment-page').text[1:-1])

	for i in range(PAGES):
		page_new = page
		URL_new = URL + r'/page-' + str(page_new-i) + '#comments'
		print('page ' + str(page_new-i))
		soup = get_soup_of(URL_new)

		imgs = soup.select('.view_img_link') # get all class="view_img_link" tags
		srcs = [img.attrs.get('href') for img in imgs] # get all 'src' attrs of imgs
		gifs = [src for src in srcs if src.endswith('.gif')] # get src of all gifs
		for gif in gifs:
			filename = gif.split('/')[-1]
			path = DIR+'\\'+filename
			if(os.path.exists(path)):
				continue # ignore file already exists
			else:
				urllib.request.urlretrieve('http:'+gif, path)
				time.sleep(0.2)

	input('Done')