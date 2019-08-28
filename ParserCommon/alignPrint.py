#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 经测试无效
# 重写一个格式对齐函数。函数中推断字符串是否是中文字符串，有的话则加入全角空格补齐，否则加入半角空格补齐。
def myAlign(string, length=0):
	if length == 0:
		return string
	slen = len(string)
	re = string
	if isinstance(string, str):
		placeholder = ' '
	else:
		placeholder = u'　'
	while slen < length:
		re += placeholder
		slen += 1
	return re

# 经测试，在命令行中可以对齐，在PyCharm中有轻微不对齐（可能是字体原因）
# 在string后面补充.，使总长度达到length
def myAlign2(string, length=0):
	if length == 0:
		return string

	# len(string.encode('GBK')) 中文按长度为2，英文长度为1计算
	re = "{label:.<{width}}".format(label=string, width=length-len(string.encode('GBK'))+len(string))
	return re

if __name__ == '__main__':
	s1 = u'我是一个长句子，是的very long的句子。'
	s2 =u'我是短句子'
	print(myAlign(s1, 20) + myAlign(s2, 10))
	print(myAlign(s2, 20) + myAlign(s1, 10))
	print(myAlign2(s1, 40) + (s2))
	print(myAlign2(s2, 40) + (s1))
	input()