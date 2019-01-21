#!/usr/bin/python3
# -*- coding: utf-8 -*-

import parse_lib as pl


if __name__ == '__main__':
	try:
		pl.BASIC()
	except Exception as e:
		pl.my_print(e)
	input()