#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseAnalysis import *

import traceback


class cZxbd_Analysis(cBaseAnalysis):
    '''中心北斗 分析'''

    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = '61.184.202.101:7000'
       #字符串占位符前后有双引号，双引号必须特殊处理
       self.dynamic_template = '_CID={cell_id}&_LAC={lac}&_MCC={mcc}&_MNC={mnc}'
       #使用2个大括号，是因为format时，不认为是占位符
       self.request_template ='/Service.asmx/locationByLBS?{dynamic_content}&HTTP/1.1'

    def setRequest(self):
        try:
            cBaseAnalysis.setRequest(self)
        except:
            print traceback.print_exc(1)

    def getResponse(self):
        try:
            #返回格式：<?xml version="1.0" encoding="UTF-8"?>\r\n<string xmlns="http://tempuri.org/">30.578369,114.369814,0,,,,0</string>
            result=self.conn.getresponse().read().decode("utf-8")
            print  result
            temp = re.findall(r"\d{1,3}\.\d{2,}",result)
            if len(temp)<2:
                temp=['0','0']
        except:
            print traceback.print_exc(1)
            temp=['0','0']
        self.conn.close()
        return (temp[1],temp[0])# 返回结果 lat 在前；lng在后

    def creatDynamicContent(self, __structBSDataFormat ):
        cBaseAnalysis.creatDynamicContent(self, __structBSDataFormat )

    def analysisRawData(self, __rawdata):
        return cBaseAnalysis.analysisRawData(self, __rawdata )
