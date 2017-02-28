#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
读取文件，解析其中GNGGA语句得到经纬度，计算相邻经纬度的距离
"""

from math import radians, asin, sqrt, sin, cos

file=input("input file:")
coordinates=[[0,0]]
#print(coordinates)
f=open(file, 'r', encoding='utf-8')
for line in f.readlines():
	#print(line)
	if 'GNGGA' in line:
		#print(line)
		elements=line.split(',')
		#print(elements)
		lat=float(elements[2])
		lon=float(elements[4])
		#print(lat)
		#print(lon)
		coordinates.append([lat,lon])
		#print(coordinates)
		#wait=input()
#print(len(coordinates))
for i in range(1,len(coordinates)-1):
	gps1=coordinates[i]
	gps2=coordinates[i+1]
	lat_f=gps1[0]
	lon_f=gps1[1]
	lat_t=gps2[0]
	lon_t=gps2[1]
	if lat_f>0 and lon_f>0 and lat_t>0 and lon_t>0:
		radlat1=radians(lat_f)
		radlat2=radians(lat_t)
		a=radlat1-radlat2
		b=radians(lon_f)-radians(lon_t)
		s=2 * asin(sqrt((sin(a / 2)*sin(a / 2)) + cos(radlat1)*cos(radlat2)*(sin(b / 2)*sin(b / 2))))
		s=s*6378137
		print('gps%d: lat=%f lon=%f; gps%d: lat=%f lon=%f' % (i,lat_f,lon_f,i+1,lat_t,lon_t))
		print('distance between gps%d and gps%d is %f meters' % (i,i+1,s))
		wait=input("next...")
f.close()
input()
