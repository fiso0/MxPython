#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseAnalysis import *

import traceback

class cHeclouds_Analysis(cBaseAnalysis):
    '''中国移动 分析'''

    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = 'api.lbs.heclouds.com'
       #字符串占位符前后有双引号，双引号必须特殊处理
       self.dynamic_template = '{{"mcc":"{mcc}","mnc":"{mnc}","lac":"{lac}","cell":"{cell_id}","ss":"{signalstrength}"}}'
       #使用2个大括号，是因为format时，不认为是占位符
       self.request_template ='/api/lbs?celltowers=[{dynamic_content}]&type=1&apikey={key}'

    def setRequest(self):
        try:
            cBaseAnalysis.setRequest(self)
        except:
            print traceback.print_exc(1)

    def getResponse(self):
        try:
            #返回格式：{\r\n"lng" : 114.39994421137573,\r\n"lat" : 30.51522956077904\r\n}
            result=self.conn.getresponse().read().decode("utf-8")
            print  result
            temp = re.findall(r"\d{1,3}\.\d{2,}",result)
            if len(temp)<2:
                temp=['0','0']
        except Exception,e:
            print traceback.format_exc(1)
            temp=['0','0']
        self.conn.close()
        return (temp[0],temp[1])

    def creatDynamicContent(self, __structBSDataFormat ):
        cBaseAnalysis.creatDynamicContent(self, __structBSDataFormat )

    def analysisRawData(self, __rawdata):
        return cBaseAnalysis.analysisRawData(self, __rawdata )
