#!/usr/bin/python3
# -*- coding: utf-8 -*-


# IMEI校验码计算
# IMEI校验码算法：
# (1).将偶数位数字分别乘以2，分别计算个位数和十位数之和
# (2).将奇数位数字相加，再加上上一步算得的值
# (3).如果得出的数个位是0则校验位为0，否则为10减去个位数
# 如：35 89 01 80 69 72 41 偶数位乘以2得到5*2=10 9*2=18 1*2=02 0*2=00 9*2=18 2*2=04 1*2=02,
# 计算奇数位数字之和和偶数位个位十位之和，得到 3+(1+0)+8+(1+8)+0+(0+2)+8+(0+0)+6+(1+8)+7+(0+4)+4+(0+2)=63
# => 校验位 10-3 = 7

while(1):
	imei_14 = input('IMEI:')
	imei_14 = imei_14.strip().replace(' ','')

	if(len(imei_14) != 14):
		print('Length ERROR!')
	else:
		ou = [int(a,10) for a in imei_14[1::2]]
		ji = [int(a,10) for a in imei_14[0::2]]

		ou_2 = [a*2 for a in ou]
		ou_2_he = [int(a/10)+(a%10) for a in ou_2]

		imei_sum = sum(ji) + sum(ou_2_he)
		imei_15 = (10 - imei_sum) % 10

		print('IMEI->'+imei_14+str(imei_15))