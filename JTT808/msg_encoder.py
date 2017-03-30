#!/usr/bin/python3
# -*- coding: utf-8 -*-

from checksum import *
from tran7e import *

# 终端手机号
CELL_NO = '12000187148'
# 省
PROVINCE = 42  # 广东44 湖北42
# 市
CITY = 111  # 龙岗区307 武汉市洪山区111
# 制造商
MANUFAC = '12345'
# 终端型号
DEVICE_TYPE = 'MX1608S'
# 终端ID
DEVIDE_ID = 'MX2017'
# 车牌颜色
LICENSE_COLOR = 1  # 未上牌时，取值为0，蓝色为1
# 车牌标识
CAR_LICENSE = 'AZ1234'  # 机动车号牌



# 标识位
FLAG_FIELD = '7e'

# 消息ID
DEVICE_REGISTER = 0x0100  # 终端注册
DEVICE_REGISTER_RSP = 0x8100  # 终端注册应答
DEVICE_AUTH = 0x0102  # 终端鉴权
PLAT_COMM_RSP = 0x8001  # 平台通用应答


# def Dec2Bcd(a):
# 	return '%d%d' % (int(a/4),(a%4))

# def tran7e(msg):
# 	msg_len = len(msg)
# 	new_msg = msg
# 	i = 0
# 	while(i<msg_len):
# 		if new_msg[i] == '7' and new_msg[i+1] == 'e':
# 			new_msg = new_msg[:i] + '7d02' + new_msg[i+2:]
# 		elif new_msg[i] == '7' and new_msg[i+1] == 'd':
# 			new_msg = new_msg[:i] + '7d01' + new_msg[i+2:]
# 		i += 2
# 	if new_msg != msg:
# 		print('tran7e result: '+new_msg)
# 	return new_msg

class MsgHeader(object):
	g_flow_no = 0  # 全局流水号（类属性）

	def __init__(self,msg_ID,cell_no):
		self.msg_ID = msg_ID  # 消息ID
		self.msg_prop = 0  # 消息体属性
		self.cell_no = cell_no  # 终端手机号
		self.flow_no = MsgHeader.g_flow_no  # 消息流水号
		MsgHeader.g_flow_no = MsgHeader.g_flow_no + 1  # 全局流水号递增
		# 消息包封装项 self.msg_pack = NULL

	def calc_msg_prop(self,msg_body):
		# 计算消息体属性
		msg_len = len(msg_body)
		self.msg_prop = int(msg_len/2)

	def msg(self):
		msg_ID_str = '%04x' % self.msg_ID
		msg_prop_str = '%04x' % self.msg_prop
		cell_no_str = '0'*(12-len(self.cell_no)) + self.cell_no
		flow_no_str = '%04x' % self.flow_no

		message = msg_ID_str+msg_prop_str+cell_no_str+flow_no_str
		return message


class MsgBody_0100(object):  # 终端注册
	def __init__(self):
		self.province_ID = PROVINCE  # 省域ID
		self.city_ID = CITY  # 市县域ID
		self.manufac_ID = MANUFAC  # 制造商ID 5个字节
		self.device_type = DEVICE_TYPE  # 终端型号 20个字节，由制造商自行定义，位数不足时，后补0x00
		self.device_ID = DEVIDE_ID  # 终端ID 7个字节，由大写字母和数字组成，由制造商自行定义，位数不足时，后补0x00
		self.license_color = LICENSE_COLOR  # 车牌颜色 未上牌时，取值为0 蓝色-1
		self.car_license = CAR_LICENSE  # 车辆标识 机动车号牌

	def msg(self):
		province_ID_str = '%04x' % self.province_ID
		city_ID_str = '%04x' % self.city_ID
		manufac_ID_str = ''.join(['%02x' % ord(a) for a in self.manufac_ID])
		device_type_str = ''.join(['%02x' % ord(a) for a in self.device_type])
		device_type_str += '0'*(40-len(device_type_str))
		device_ID_str = ''.join(['%02x' % ord(a) for a in self.device_ID])
		device_ID_str += '0'*(14-len(device_ID_str))
		license_color_str = '%02x' % self.license_color
		car_license_str = ''.join(['%02x' % ord(a) for a in self.car_license])

		message = province_ID_str+city_ID_str+manufac_ID_str+device_type_str+device_ID_str+license_color_str+car_license_str
		return message

if __name__ == '__main__':
	res = tran7e('307e087d55')
	print(res+', '+str(res == '307d02087d0155'))

	print('CELL_NO:'+CELL_NO)
	print('CELL_NO_LEN:',len(CELL_NO))

	msg_ID = DEVICE_REGISTER
	header = MsgHeader(DEVICE_REGISTER,CELL_NO)
	msg_body = MsgBody_0100().msg()
	print('msg_body: '+msg_body)

	header.calc_msg_prop(msg_body)
	msg_header = header.msg()
	print('msg_header: '+msg_header)

	checksum = '%02x' % checksum(msg_header+msg_body)
	print('checksum: '+checksum)

	print('msg without FLAG_FIELD: '+msg_header+msg_body+checksum)

	msg = FLAG_FIELD+tran7e(msg_header+msg_body+checksum)+FLAG_FIELD
	print('msg: '+msg)
