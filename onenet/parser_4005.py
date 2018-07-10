#!/usr/bin/python3
# -*- coding: utf-8 -*-

Project = '1609'  # 1608 has STEP, 1609 has no STEP

def parser_4005(msg):
	results = [''] * 28
	descs = [''] * 28
	message = msg.strip().replace(' ', '').upper()  # 去掉空格 转为大写
	chrstr = [message[i:i + 2] for i in range(0, len(message), 2)]

	if (Project == '1608'):
		hasStep = True
	elif (Project == '1609'):
		hasStep = False
	else:
		hasStep = False

	results[0] = ''.join(chrstr[0:18])  # 消息头
	descs[0] = '消息头'

	results[1] = ''.join(chrstr[18:20])  # 消息ID
	descs[1] = '消息ID'

	results[2] = ' '.join(chrstr[20:26])  # GPS定位时间
	GPSTime = [str(int(chr, 16)) for chr in chrstr[20:26]]
	GPSTimeDesc = '-'.join(GPSTime[0:3]) + ' ' + ':'.join(GPSTime[3:6])
	descs[2] = 'GPS定位时间:'+GPSTimeDesc

	results[3] = ' '.join(chrstr[26:30])  # 经度
	GPSLat = [int(chr, 16) for chr in chrstr[26:30]]
	GPSLatDesc = str(GPSLat[0] + 0.01 * GPSLat[1] + 0.0001 * GPSLat[2] + 0.000001 * GPSLat[3])
	descs[3] = '经度:'+GPSLatDesc

	results[4] = ' '.join(chrstr[30:34])  # 纬度
	GPSLon = [int(chr, 16) for chr in chrstr[30:34]]
	GPSLonDesc = str(GPSLon[0] + 0.01 * GPSLon[1] + 0.0001 * GPSLon[2] + 0.000001 * GPSLon[3])
	descs[4] = '纬度:'+GPSLonDesc

	results[5] = ''.join(chrstr[34:35])  # 速度
	temp = str(int(chrstr[34], 16))
	descs[5] = '速度:'+temp

	results[6] = ''.join(chrstr[35:36])  # 方向
	temp = str(int(chrstr[35], 16))
	descs[6] = '方向:'+temp

	results[7] = ' '.join(chrstr[36:38])  # 高度
	temp = str(int(chrstr[36] + chrstr[37], 16))
	descs[7] = '高度:'+temp

	results[8] = ''.join(chrstr[38:39])  # 定位状态
	if (chrstr[38] == '10'):
		temp = 'GPS信息有效'
	elif(chrstr[38] == 'F0'):
		temp = 'GPS信息无效或过期'
	elif(chrstr[38] == '0F'):
		temp = 'WiFi定位'
	elif(chrstr[38] == 'FF'):
		temp = '基站加WiFi定位'
	else:
		temp = '未知值'
	descs[8] = '定位状态:'+temp

	results[9] = ''.join(chrstr[39:40])  # 报警状态
	if (chrstr[39] == '00'):
		temp = '普通上传'
	elif(chrstr[39] == '0C'):
		temp = '关机'
	elif(chrstr[39] == '0D'):
		temp = '开机'
	elif(chrstr[39] == '10'):
		temp = '点名上传'
	elif(chrstr[39] == '11'):
		temp = '短信透传'
	else:
		temp = '大于0x80为报警求助 其他未知'
	descs[9] = '报警状态:'+temp

	results[10] = ''.join(chrstr[40:41])  # 电量
	temp = str(int(chrstr[40], 16)) + '%'
	descs[10] = '电量:'+temp

	results[11] = ''.join(chrstr[41:42])  # 经度标志
	if (chrstr[41] == '45'):
		temp = 'E'
	elif(chrstr[41] == '57'):
		temp = 'W'
	else:
		temp = '未知值'
	descs[11] = '经度标志:'+temp

	results[12] = ''.join(chrstr[42:43])  # 纬度标志
	if (chrstr[42] == '4E'):
		temp = 'N'
	elif(chrstr[42] == '53'):
		temp = 'S'
	else:
		temp = '未知值'
	descs[12] = '纬度标志:'+temp

	results[13] = ''.join(chrstr[43:44])  # 预留
	descs[13] = '预留'

	results[14] = ''.join(chrstr[44:46])  # 国别
	descs[14] = '国别:'+'01CC（460，中国）'

	results[15] = ''.join(chrstr[46:47])  # 运营商
	descs[15] = '运营商:'+'00移动 01联通 11电信4G'

	results[16] = ''.join(chrstr[47:49])  # 小区编号
	temp = str(int(chrstr[47]+chrstr[48], 16))
	descs[16] = '小区编号:'+temp

	results[17] = ''.join(chrstr[49:51])  # 基站扇区
	temp = str(int(chrstr[49]+chrstr[50], 16))
	descs[17] = '基站扇区:'+temp

	results[18] = ''.join(chrstr[51:52])  # 预留
	descs[18] = '预留'

	results[19] = ''.join(chrstr[52:53])  # 信号量
	temp = '-'+str(int(chrstr[52], 16))
	descs[19] = '信号量:'+temp

	results[20] = ' '.join(chrstr[53:59])  # 基站时间
	LBSTime = [str(int(chr, 16)) for chr in chrstr[53:59]]
	LBSTimeDesc = '-'.join(LBSTime[0:3]) + ' ' + ':'.join(LBSTime[3:6])
	descs[20] = '基站时间:'+LBSTimeDesc

	results[21] = ''.join(chrstr[59:67])  # IMSI
	temp = ''.join(chrstr[59:67]).replace('A','0')
	descs[21] = 'IMSI:'+temp

	results[22] = ''.join(chrstr[67:69])  # 预留
	descs[22] = '预留'

	results[23] = ''.join(chrstr[69:70])  # 卫星定位方式
	if (chrstr[69] == '00'):
		temp = 'GPS定位'
	elif(chrstr[69] == '01'):
		temp = '北斗定位'
	elif(chrstr[69] == '02'):
		temp = '混合定位'
	else:
		temp = '未知值'
	descs[23] = '卫星定位方式:'+temp

	if (hasStep):
		results[24] = ''.join(chrstr[70:74])  # 步数
		wifiIndex = 74
		temp = str(int(''.join(chrstr[70:74]), 16))
		descs[24] = '步数:'+temp
	else:
		wifiIndex = 70

	if ('FF' in chrstr[wifiIndex:]):
		sepIndex = chrstr[wifiIndex:].index('FF')

	results[25] = ' '.join(chrstr[wifiIndex:wifiIndex + sepIndex])  # 附近wifi数据
	wifiData = [int(chr, 16) for chr in chrstr[wifiIndex:wifiIndex + sepIndex]]
	temp = ''.join([chr(a) for a in wifiData if a != 0])
	descs[25] = '附近wifi数据:'+temp

	results[26] = ''.join(chrstr[wifiIndex + sepIndex:wifiIndex + sepIndex + 1])  # 分隔符
	descs[26] = '分隔符'

	results[27] = ' '.join(chrstr[wifiIndex + sepIndex + 1:])  # 附近基站数据
	lbsData = [int(chr, 16) for chr in chrstr[wifiIndex + sepIndex + 1:]]
	temp = ''.join([chr(a) for a in lbsData if a != 0])
	descs[27] = '附近基站数据:'+temp
	
	return (results, descs)

if __name__=='__main__':
	test='262626260057000000000866888a2a41732640050000000a2e28742a0933275957180000000010003d454e0001cc0010be927b003c110b1c122e29046aaaa684253458000002000000003b3230313731313238313834363431ff002185'
	(results, descs) = parser_4005(test)

	print(test)
	print('=====解析结果=====')
	for i in range(0,28):
		if(results[i] != ''):
			try:
				print(results[i], end='')
			except Exception as e:
				print(e, end='')
			print('\t#', end='')
			try:
				print(descs[i])
			except Exception as e:
				print(e)
			#except UnicodeEncodeError as e:
			#	results[i] = results[i].encode('gbk','ignore').decode('utf-8','ignore')
			#	descs[i] = descs[i].encode('gbk','ignore').decode('utf-8','ignore')
			#	print(results[i]+'\t#'+descs[i])
		
	input()
