#!/usr/bin/python3
# -*- coding: utf-8 -*-


def triangles_func(n):  # n = 0, print [1], n = 1, print [1, 1]
	if n == 0:
		numbers = [1]
	elif n == 1:
		numbers = [1,1]
	else:
		old = triangles_func(n - 1)
		numbers = []
		numbers.append(1)
		for t in range(1,n):
			num = old[t-1] + old[t]
			numbers.append(num)
		numbers.append(1)
	return numbers


print('test triangles_func:')
for m in range(10):
	print(triangles_func(m))


def triangles_func_1(n):  # n = 0, print [1], n = 1, print [1, 1]
	numbers = []
	numbers.append(1)  # first 1
	if n > 1:  # middle numbers
		old = triangles_func_1(n - 1)
		for t in range(1,n):
			num = old[t-1] + old[t]
			numbers.append(num)
	if n > 0:  # last 1
		numbers.append(1)
	return numbers


print('test triangles_func_1:')
for m in range(10):
	print(triangles_func_1(m))


def triangles():
	n = 0
	numbers = [1]
	while True:
		if n > 1:  # middle numbers
			numbers = [1]+[numbers[t-1] + numbers[t] for t in range(1,n)]
		if n > 0:  # last 1
			numbers.append(1)
		yield numbers
		n += 1


print('test triangles:')
n = 0
for t in triangles():
	print(t)
	n += 1
	if n == 10:
		break


def triangles_answers():  # 最佳答案
	L = [1]
	while True:
		yield L
		L.append(0)  # 最后补0
		L = [L[i-1] + L[i] for i in range(len(L))]  # 前两项相加，Python中下标可以是-1