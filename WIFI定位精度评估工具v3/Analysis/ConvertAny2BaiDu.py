#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseAnalysis import *
import http.client
import copy
import re
import traceback

class cConvertAny2BaiDu(cBaseAnalysis):
    """任何地图坐标转换成百度地图坐标，来源于百度地图服务：http://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
       坐标转换服务每日请求次数上限为10万次
       from 取值为如下： 1：GPS设备获取的角度坐标，wgs84坐标;  3：国测局坐标;5：百度地图采用的经纬度坐标; 7：mapbar地图坐标;
       to 有两种可供选择：5：bd09ll(百度经纬度坐标), 6：bd09mc(百度米制经纬度坐标);"""
    srcCoord = 1

    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = 'api.map.baidu.com'
       #字符串占位符前后有双引号，双引号必须特殊处理
       self.dynamic_template = '{lng},{lat}'
       #使用2个大括号，是因为format时，不认为是占位符
       self.request_template ='/geoconv/v1/?coords={dynamic_content}&from={srcCoord}&to=5&ak={key}'

    def setRequest(self):
        try:
            self.conn = http.client.HTTPConnection(self.domain_name,timeout=5)
            #print str.format(self.request_template,srcCoord=self.srcCoord, key=self.key, dynamic_content=','.join(self.dynamic_content))
            self.conn.request('GET',str.format(self.request_template,srcCoord=self.srcCoord, key=self.key, dynamic_content=';'.join(self.dynamic_content)))
        except:
            traceback.print_exc(1)

    def getResponse(self):
        try:
            #返回格式：{"status":0,"result":[{"x":114.23075249819,"y":29.579081312292},{"x":114.23075006329,"y":29.579083178614}]}
            result=self.conn.getresponse().read().decode("utf-8")
            print(result)
            temp = re.findall(r"\d{1,3}\.\d{2,}",result)
            if len(temp)<2:
                temp=['0','0']
        except:
            temp=['0','0']
        self.conn.close()
        return temp

    def creatDynamicContent(self, __structLLHDataFormat ):
        del self.dynamic_content[:]
        for item  in __structLLHDataFormat[:]:
            self.dynamic_content.append(str.format(self.dynamic_template,
                                                lng=item.lng,
                                                lat=item.lat))

    def analysisRawData(self, __rawdata):
        print(__rawdata)
        #生数据格式：114.3938:30.5053|114.3938:30.5053|114.393830.5053
        __listStructLLHDataFormat=[]
        __array = re.split('[|]',__rawdata)
        for item in __array[:]:
            __array1 = str.split(item,':')
            __structBSDataFormat = structLLHDataFormat()
            __structBSDataFormat.lng = __array1[0]
            __structBSDataFormat.lat = __array1[1]
            __listStructLLHDataFormat.append(__structBSDataFormat)
        return __listStructLLHDataFormat
