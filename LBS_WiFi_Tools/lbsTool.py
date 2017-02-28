#!/usr/bin/python3
# -*- coding: utf-8 -*-

def GaoDe_req(lbs_main,lbs_near):
	GaoDe_req = '''http://apilocate.amap.com/position?accesstype=0&imei=352315052834187&cdma=0&bts=%s&nearbts=%s&output=xml&key=01605561cc68306b74c043db28d9e4db'''%(lbs_main,lbs_near)
	return GaoDe_req