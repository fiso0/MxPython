#!/usr/bin/python3
# -*- coding: utf-8 -*-

def get_GPS(log):
	import re
	ptn = r'#GPS (\d{2}):(\d{2}):(\d{2}),([\d\.]+),([\d\.]+)'
	res = re.search(ptn, log)
	if res:
		time_h = int(res.group(1))
		time_m = int(res.group(2))
		time_s = int(res.group(3))
		lon = float(res.group(4))
		lat = float(res.group(5))
		return (time_h,time_m,time_s,lon,lat)
	else:
		return None

def get_WIFI(log):
	import re
	ptn = r'#WIFI (.*)'
	res = re.search(ptn, log)
	if res:
		wifi_data = res.group(1).split('|') # ['a4:fb:8d:00:10:41,-53,ap1', '96:fb:8d:00:10:41,-54,ap2', '8c:79:67:02:68:7c,-86,ap3', '8c:79:67:02:71:42,-80,ap4', '8c:79:67:01:aa:c3,-85,ap5']
		wifi_data_group = [data.split(',') for data in wifi_data] # [['a4:fb:8d:00:10:41', '-53', 'ap1'], ['96:fb:8d:00:10:41', '-54', 'ap2'], ['8c:79:67:02:68:7c', '-86', 'ap3'], ['8c:79:67:02:71:42', '-80', 'ap4'], ['8c:79:67:01:aa:c3', '-85', 'ap5']]
		return (wifi_data,wifi_data_group)
	else:
		return None

def Hao_Req(wifi_data_group):
	# HaoService(ErrorCode:5 超出次数)
	HAO_WIFI = r'{"mac_address":"%s","singal_strength": %s,"age":0}'
	hao_wifi = ','.join([HAO_WIFI%(data[0],data[1]) for data in wifi_data_group])
	HAO_REQ = '''http://api.haoservice.com/api/LocationByWifiData?key=d74ad38060194ac69276eecf1ea40bf9&requestdata=[%s]&type=0'''
	hao_req = HAO_REQ % (hao_wifi)
	return (hao_wifi,hao_req)

def GaoDe_Req(wifi_data):
	# GaoDe
	GaoDe_req = '''http://apilocate.amap.com/position?accesstype=1&imei=352315052834187&macs=%s&output=xml&key=01605561cc68306b74c043db28d9e4db'''%('|'.join(wifi_data))
	return GaoDe_req

def SiWei_Req(wifi_data_group):
	# SiWeiTuXin
	hao_wifi,hao_req = Hao_Req(wifi_data_group)
	SiWei_wifi = hao_wifi
	SiWei_req = '''http://mapx.mapbar.com/GeolocationPro/?data={"version": "1.0.0","host": "mapx.mapbar.com","access_token": "abc9f9be-0d8e-4c90-8c34-8129131cd695","radio_type": "gsm","request_address": "true", "address_language": "cn", "wifi_towers": [%s]}'''%(SiWei_wifi)
	return SiWei_req

def get_res(req):
	import requests
	wb_data = requests.get(req)
	wb_data.encoding = 'utf-8'
	# print('\nstatus:'+str(wb_data.status_code)+'\ntext:\n'+wb_data.text)
	return wb_data

def GaoDe_parser(url_res):
	try:
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(url_res.text,'lxml')
		location = soup.find('location').text
		res_lon,res_lat = location.split(',')
		res_radius = soup.find('radius').text
		return (res_lon,res_lat,res_radius)
	except Exception as e:
		print("Parser Error: "+str(e))
		return (None,None,None)

def SiWei_parser(url_res):
	try:
		js_data = url_res.json()
		res_lon = js_data['location'].get('longitude')
		res_lat = js_data['location'].get('latitude')
		res_accuracy = js_data['location'].get('accuracy')
		return (res_lon,res_lat,res_accuracy)
	except Exception as e:
		print("Parser Error: "+str(e))
		return (None,None,None)

def WiFi_to_GPS(wifi_data,wifi_data_group):
	try:
		Hao_wifi,Hao_req = Hao_Req(wifi_data_group)
		Hao_res = get_res(Hao_req)
		# TODO:HaoService暂无可用次数
		Hao_result = None
	except Exception as e:
		print(e)
		Hao_result = None

	try:
		GaoDe_req = GaoDe_Req(wifi_data)
		GaoDe_res = get_res(GaoDe_req)
		GaoDe_result = GaoDe_parser(GaoDe_res) # GaoDe_lon,GaoDe_lat,GaoDe_radius
	except Exception as e:
		print(e)
		GaoDe_result = None

	try:
		SiWei_req = SiWei_Req(wifi_data_group)
		SiWei_res = get_res(SiWei_req)
		SiWei_result = SiWei_parser(SiWei_res) # SiWei_lon,SiWei_lat,SiWei_radius
	except Exception as e:
		print(e)
		SiWei_result = None

	return (Hao_result,GaoDe_result,SiWei_result)

if 0:
	log = '''
	#GPS 03:21:42,114.393921,30.505411
	#WIFI 02:27:1d:1a:5a:3d,-92,ap1|00:27:1d:1a:5a:3d,-93,ap2|00:19:70:19:6b:40,-85,ap3|12:27:1d:1a:5a:3d,-94,ap4|a2:27:1d:09:0b:1e,-93,ap5
	'''

	data = []

	with open('WIFI实测数据_xsk0902.log') as f:
		for line in f.readlines():
			if line.startswith('#GPS'):
				GPS_result = get_GPS(line) # time_h,time_m,time_s,lon,lat
				continue
			elif line.startswith('#WIFI'):
				wifi_data,wifi_data_group = get_WIFI(line)
				WiFi_results = WiFi_to_GPS(wifi_data,wifi_data_group)
				#TODO: save_results()


	time_h,time_m,time_s,lon,lat = get_GPS(log)
	wifi_data,wifi_data_group = get_WIFI(log)


	hao_wifi,hao_req = Hao_Req(wifi_data_group)
	res_data = get_res(hao_req)


	GaoDe_req = GaoDe_Req(wifi_data)
	GaoDe_res = get_res(GaoDe_req)
	GaoDe_lon,GaoDe_lat,GaoDe_radius = GaoDe_parser(GaoDe_res)


	SiWei_req = SiWei_Req(wifi_data_group)
	SiWei_res = get_res(SiWei_req)
	SiWei_lon,SiWei_lat,SiWei_radius = SiWei_parser(SiWei_res)

if __name__=='__main__':
	log = '''
	#WIFI 78:52:62:17:8f:19,-61,ap1|00:1e:a8:07:71:a0,-71,ap2|b4:30:52:1c:5b:be,-78,ap3|58:1f:28:02:f2:70,-79,ap4
	'''

	wifi_data,wifi_data_group = get_WIFI(log)
	SiWei_req = SiWei_Req(wifi_data_group)
	SiWei_res = get_res(SiWei_req)
	SiWei_lon,SiWei_lat,SiWei_radius = SiWei_parser(SiWei_res)

	GaoDe_req = GaoDe_Req(wifi_data)
	GaoDe_res = get_res(GaoDe_req)
	GaoDe_lon,GaoDe_lat,GaoDe_radius = GaoDe_parser(GaoDe_res)

	input('done')
