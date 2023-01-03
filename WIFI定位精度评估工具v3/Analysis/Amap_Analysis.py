#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseAnalysis import *

import traceback


class cAmap_Analysis(cBaseAnalysis):
    '''高德 分析'''
    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = 'apilocate.amap.com'
       #字符串占位符前后有双引号，双引号必须特殊处理
       self.dynamic_template = '{mac_address},{signal_strength},{RSSI}'
       #使用2个大括号，是因为format时，不认为是占位符  mcc,mnc,lac,cellid,signal
       self.request_template ='/position?key={key}&accesstype=1&imei=352315052834187&macs={dynamic_content}&output=json'

    def setRequest(self):
        try:
            self.conn = httplib.HTTPConnection(self.domain_name,timeout=1)
            #根据高德请求中基站字符串格式，进行  request_template  改造
            print(str.format(self.request_template, key=self.key, dynamic_content='|'.join(self.dynamic_content)))
            self.conn.request('GET',str.format(self.request_template, key=self.key, dynamic_content='|'.join(self.dynamic_content)))
        except:
            print(traceback.print_exc(1))

    def getResponse(self):
        try:
            #返回格式：{"status":"1","info":"OK","infocode":"10000","result":{"type":"4","location":"114.3690546,30.5695871","radius":"550","desc":"湖北省 武汉市 武昌区 武汉大道 靠近湖北省文物交流信息中心","country":"中国","province":"湖北省","city":"武汉市","citycode":"027","adcode":"420106","road":"武汉大道","street":"东湖路","poi":"湖北省文物交流信息中心"}}
            result=self.conn.getresponse().read().decode("utf-8")
            print(result)
            temp = re.findall(r"\d{1,3}\.\d{2,}",result)
            if len(temp)<2:
                temp=['0','0']
        except:
            print(traceback.print_exc(1))
            temp=['0','0']
        self.conn.close()
        return (temp[0],temp[1])

    def creatDynamicContent(self, __structBSDataFormat ):
        cBaseAnalysis.creatDynamicContent(self, __structBSDataFormat )

    def analysisRawData(self, __rawdata):
        return cBaseAnalysis.analysisRawData(self, __rawdata )