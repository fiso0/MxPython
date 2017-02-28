#!/usr/bin/python3
# -*- coding: utf-8 -*-

def GaoDeReq(access_type,lbs_main,lbs_near,wifi):
	'''
	:param access_type: 1表示wifi接入，否则为0
	:param lbs_main: 接入基站信息
	:param lbs_near: 周边基站信息
	:param wifi: wifi列表中mac信息
	:return:
	'''
	if access_type == 1 and wifi == '':
		print('Error')
		return ''
	if access_type == 0 and lbs_main == '':
		print('Error')
		return ''
	GaoDe_req = '''http://apilocate.amap.com/position?accesstype=%d&imei=352315052834187&cdma=0&bts=%s&nearbts=%s&macs=%s&output=xml&key=01605561cc68306b74c043db28d9e4db'''%(access_type,lbs_main,lbs_near,wifi)
	return GaoDe_req


def GetRes(req):
	import requests
	wb_data = requests.get(req)
	wb_data.encoding = 'utf-8'
	# print('\nstatus:'+str(wb_data.status_code)+'\ntext:\n'+wb_data.text)
	return wb_data