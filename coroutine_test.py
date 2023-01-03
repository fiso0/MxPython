#!/usr/bin/python3
# -*- coding: utf-8 -*-

def consumer():
    r = ''
    while True:
        n = yield r # 预激时，会执行表达式的右边（yield r），但不会执行表达式的左边（n = yield）
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None) # 预激，执行到n = yield r后暂停，此处返回值为''
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)
c.close()
input()