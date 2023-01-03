#!/usr/bin/python3
# -*- coding: utf-8 -*-

# MEID校验码计算
# MEID校验码算法：
# (1).将偶数位数字分别乘以2，分别计算个位数和十位数之和，注意是16进制数
# (2).将奇数位数字相加，再加上上一步算得的值
# (3).如果得出的数个位是0则校验位为0，否则为10(这里的10是16进制)减去个位数
# 如：AF 01 23 45 0A BC DE 偶数位乘以2得到F*2=1E 1*2=02 3*2=06 5*2=0A A*2=14 C*2=18 E*2=1C,
# 计算奇数位数字之和和偶数位个位十位之和，得到 A+(1+E)+0+2+2+6+4+A+0+(1+4)+B+(1+8)+D+(1+C)=64
# => 校验位 10-4 = C

meid_14 = input('MEID:')
meid_14 = meid_14.strip().replace(' ','')

if(len(meid_14) != 14):
	print('Length ERROR!')
else:
	ou = [int(a,16) for a in meid_14[1::2]]
	ji = [int(a,16) for a in meid_14[0::2]]

	ou_2 = [a*2 for a in ou]
	ou_2_he = [((a&0x1F)>>4)+(a&0x0F) for a in ou_2]

	meid_sum = sum(ji) + sum(ou_2_he)
	meid_15 = hex((0x10 - meid_sum) & 0xF)[-1]

	print('MEID:'+meid_14+meid_15)