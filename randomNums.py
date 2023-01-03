#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
从1~n中，随机取m个数。1<=m<=n
'''

import random

def randomNums1(n,m):
	l = list(range(1,n+1))
	random.shuffle(l)  # 随机乱序
	return l[:m]


def randomNums2(n,m):
	l = list(range(1,n+1))
	return random.sample(l,m)  # 随机抽样

print(randomNums1(10,3))
print(randomNums2(10,3))