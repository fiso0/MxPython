#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyClass():
	name = 'fiso' # 类属性
	# self.age = 20 # ERROR：Unresolved reference 'self'

	def __init__(self):
		self.age = 20 # 实例属性
		gender = 'female' # 无效


if __name__ == '__main__':
	t = MyClass()

	print(t.name) # fiso
	print(MyClass.name) # fiso

	print(t.age) # 20
	# print(MyClass.age) # AttributeError: type object 'MyClass' has no attribute 'age'

	# print(t.gender) # AttributeError: 'MyClass' object has no attribute 'gender'
	# print(MyClass.gender) # AttributeError: type object 'MyClass' has no attribute 'gender'

	input()