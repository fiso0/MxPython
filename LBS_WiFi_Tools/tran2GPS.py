#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("..")
import socket_tool.wifi_test as tool
import xml.etree.ElementTree as ET
import lbsTool
import GaoDeTool

def get_lbs(log, src):
	if src == '数据库':
		db_data = log.split('\t')
		db_data[16]='-'+db_data[16]  # 信号强度前加负号
		lbs_main = ','.join(db_data[12:17])
		# '460,0,28914,51012,-68'
		lbs_near = db_data[21].strip()
		# '460,00,28699,452,-73|460,00,28699,45932,-77|460,00,28699,451,-78|460,00,28699,32286,-83|460,00,28699,10453,-86|460,00,28699,32284,-86'
	elif src == '服务器log':
		srv_data = log.split(' ')
		lbs_main = srv_data[17].replace(':',',')+','+srv_data[19]
		lbs_near = srv_data[25].strip()
		if lbs_near[-1] == '>':  # 去掉最后的>符号
			lbs_near = lbs_near[:-1]
	elif src == '纯数据':
		data = log.split('|',maxsplit=1)
		lbs_main = data[0]  # '460,00,28914,60002,-59'
		lbs_near = data[1]  # '460,00,28914,54642,-72|460,00,28914,56613,-76|460,00,28914,51013,-78|460,00,28914,60053,-78|460,00,28914,52793,-79'
	else:
		lbs_main = ''
		lbs_near = ''
	return (lbs_main, lbs_near)


def get_wifi(log, src):
	if src == '数据库':
		db_data = log.split('\t')
		wifi = db_data[
			20].strip()  # '12:27:1d:1a:59:2e,-45,ap1|02:27:1d:1a:59:2e,-45,ap2|00:27:1d:1a:59:2e,-46,ap3|02:bd:5f:15:b9:dd,-58,ap4|50:bd:5f:15:b9:dd,-58,ap5;20170120090013'
	elif src == '服务器log':
		srv_data = log.split(' ')
		wifi = srv_data[
			24].strip()  # '50:bd:5f:15:b9:dd,-53,ap1|02:bd:5f:15:b9:dd,-53,ap2|00:27:1d:1a:59:2e,-58,ap3|12:27:1d:1a:59:2e,-58,ap4|02:27:1d:1a:59:2e,-58,ap5;20170124095209'
	elif src == '纯数据':
		wifi = log
	else:
		wifi = ''
	wifi = wifi.split(';')
	wifi_data = wifi[0].split('|')
	wifi_data_group = [data.split(',') for data in wifi_data]
	return (wifi_data, wifi_data_group)


def parse_xml(xml_data):
	'''定位类型type值：为0表示没有得到定位结果，为其他数值表示正常获取定位结果'''
	'''[Result text] <?xml version="1.0" encoding="UTF-8"?>
<response><status>1</status><info>OK</info><infocode>10000</infocode><result><type>3</type><location>114.3991021,30.5029384</location><radius>29</radius><desc>湖北省 武汉市 洪山区 民族大道 靠近湖北省测绘工程院</desc><country>中国</country><province>湖北省</province><city>武汉市</city><citycode>027</citycode><adcode>420111</adcode><road>民族大道</road><street>民族大道</street><poi>湖北省测绘工程院</poi></result></response>'''
	'''[Result text] <?xml version="1.0" encoding="UTF-8"?>
<response><status>1</status><info>OK</info><infocode>10000</infocode><result><type>0</type></result></response>'''
	root = ET.fromstring(xml_data)
	info = root.findall(".//info")[0].text
	if info != 'OK':
		print('info:',info)
		return '[错误]'+info
	type = root.findall(".//type")[0].text
	if type == '0':
		print('type:',info)
		return '无定位结果'
	location = root.findall(".//location")[0].text+'\n'
	radius = root.findall(".//radius")[0].text+'\n'
	desc = root.findall(".//desc")[0].text+'\n'
	country = root.findall(".//country")[0].text+'\n'
	province = root.findall(".//province")[0].text+'\n'
	city = root.findall(".//city")[0].text+'\n'
	citycode = root.findall(".//citycode")[0].text+'\n'
	adcode = root.findall(".//adcode")[0].text+'\n'
	road = root.findall(".//road")[0].text+'\n'
	street = root.findall(".//street")[0].text+'\n'
	poi = root.findall(".//poi")[0].text+'\n'
	return location,radius,desc,country,province,city,citycode,adcode,road,street,poi


def transfer(log, src = '数据库', type = 'WiFi'):
	"""
	根据数据来源和数据类型解析GPS结果
	:param log: 数据
	:param src: 数据来源
	:param type: 数据类型
	:return: 请求内容，返回内容
	"""
	if type == 'WiFi':
		wifi_data, wifi_data_group = get_wifi(log, src)
		GaoDe_req = tool.GaoDe_Req(wifi_data)
		print('[Request] %s' % GaoDe_req)

		GaoDe_req = GaoDeTool.GaoDeReq(1,'','','|'.join(wifi_data))
		print('[Request] %s' % GaoDe_req)
		# GaoDe_res = tool.get_res(GaoDe_req)
		# print('[Result text] %s' % GaoDe_res.text)
		#
		# xml_info = parse_xml(GaoDe_res.text)
		# print('[Result] ', xml_info)
		#
		# return GaoDe_req, xml_info
	elif type == 'LBS':
		lbs_main, lbs_near = get_lbs(log, src)
		GaoDe_req = lbsTool.GaoDe_req(lbs_main, lbs_near)

	print('[Request] %s' % GaoDe_req)

	GaoDe_res = tool.get_res(GaoDe_req)
	print('[Result text] %s' % GaoDe_res.text)
	xml_info = parse_xml(GaoDe_res.text)
	print('[Result] ', xml_info)

	return GaoDe_req, xml_info


if __name__ == '__main__':
	lbs, lbs_near = get_lbs('4060	866888020237294	2017-01-28 14:49:31	1999-11-30 00:00:00	113.4465818	30.3695405	0	0	0	15	0	28	460	0	28914	51012	68	2017-01-28 14:49:18	460077171327454	2	0a:18:d6:5f:a4:b5,-77,ap1|48:28:2f:32:71:64,-84,ap2|1a:25:93:8e:5c:65,-88,ap3|0a:25:93:8e:5c:65,-88,ap4|1a:25:93:8e:5c:c9,-88,ap5;20170128144918	460,00,28914,60002,-59|460,00,28914,54642,-72|460,00,28914,56613,-76|460,00,28914,51013,-78|460,00,28914,60053,-78|460,00,28914,52793,-79', '数据库')
	lbs, lbs_near = get_lbs('mx_srv_send_handle[359][4005]:&&&& 353 000000000866888a2a237294 <4005> <00-00-00 000000 0.000000 0.000000 0 0 0 0xff 0x00 28 E N 0x00 460:00:28914:51012 0x00 -68 17-01-28 14:49:18 0x01 0x4a 0a:18:d6:5f:a4:b5,-77,ap1|48:28:2f:32:71:64,-84,ap2|1a:25:93:8e:5c:65,-88,ap3|0a:25:93:8e:5c:65,-88,ap4|1a:25:93:8e:5c:c9,-88,ap5;20170128144918 460,00,28914,60002,-59|460,00,28914,54642,-72|460,00,28914,56613,-76|460,00,28914,51013,-78|460,00,28914,60053,-78|460,00,28914,52793,-79> 00 45 0xd4', '服务器log')


	log = '''#WIFI 78:52:62:17:8f:19,-61,ap1|00:1e:a8:07:71:a0,-71,ap2|b4:30:52:1c:5b:be,-78,ap3|58:1f:28:02:f2:70,-79,ap4'''

	log2 = '''#WIFI 00:1e:a8:07:71:a0,-71,ap2'''

	log_db = '''3763	866888020237229	20 2017 1 09:00:19	30 1999 11 00:00:00	114.3991094	30.5029335	0	0	0	15	0	10	460	0	28730	20736	60	20 2017 1 09:00:13	460078027753510	2	12:27:1d:1a:59:2e,-45,ap1|02:27:1d:1a:59:2e,-45,ap2|00:27:1d:1a:59:2e,-46,ap3|02:bd:5f:15:b9:dd,-58,ap4|50:bd:5f:15:b9:dd,-58,ap5;20170120090013'''

	log_db_gps = '''3676	866888020237229	19 2017 1 18:45:22	30 1999 11 10:45:17	114.40852052936049	30.47561435069056	0	0	0	16	0	48	460	0	28709	54592	86	19 2017 1 18:45:17	460078027753510	2	;20170119184517'''

	log_srv = '''mx_srv_send_handle[337][4005]:&&&& 331 000000000866888a2a237294 <4005> <00-00-00 000000 0.000000 0.000000 0 0 0 0xff 0x00 46 E N 0x00 460:00:28730:20736 0x00 -63 17-01-24 09:52:09 0x00 0x00 50:bd:5f:15:b9:dd,-53,ap1|02:bd:5f:15:b9:dd,-53,ap2|00:27:1d:1a:59:2e,-58,ap3|12:27:1d:1a:59:2e,-58,ap4|02:27:1d:1a:59:2e,-58,ap5;20170124095209 460,00,28730,45271,-90|460,00,28730,45273,-95|460,00,28730,55271,-96|460,00,28730,63401,-98|460,00,28730,46075,-104> 00 05 0x9b'''

	log_srv_gps = '''mx_srv_send_handle[93][4005]:&&&& 87 000000000866888a2a237229 <4005> <00-00-00 234550 114.405016 30.484672 0 0 0 0x10 0x00 71 E N 0x00 460:00:28709:15121 0x00 -72 17-01-17 07:45:49 0x00 0x00 ;20170117074549 > 00 5e 0x51'''

	# wifi_data, wifi_data_group = tool.get_WIFI(log)
	# wifi_data, wifi_data_group = tool.get_WIFI(log2)
	wifi_data, wifi_data_group = get_wifi(log_db, 'db')
	# wifi_data, wifi_data_group = get_wifi(log_db_gps, 'db')
	# wifi_data, wifi_data_group = get_wifi(log_srv, 'srv')
	# wifi_data, wifi_data_group = get_wifi(log_srv_gps, 'srv')

	GaoDe_req = tool.GaoDe_Req(wifi_data)
	print('[Request] %s' % GaoDe_req)

	GaoDe_res = tool.get_res(GaoDe_req)
	print('[Result text] %s' % GaoDe_res.text)

	xml_info = parse_xml(GaoDe_res.text)
	print('[Result] ', xml_info)

	a = input('Done')
