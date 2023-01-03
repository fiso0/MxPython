#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseAnalysis import *

import traceback

class cMapbar_Analysis(cBaseAnalysis):
    '''四维 分析'''

    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = 'mapx.mapbar.com'
       #字符串占位符前后有双引号，双引号必须特殊处理               singal_strength
       self.dynamic_template = '{{"mac_address":"{mac_address}","signal_strength":{signal_strength},"age":0}}'
       #使用2个大括号，是因为format时，不认为是占位符
       self.request_template = '/GeolocationPro/?data='\
                              '{{"version":"1.0.0","host":"mapx.mapbar.com","access_token":"{key}","radio_type":"gsm",'\
                              '"request_address":"true","address_language":"cn","wifi_towers":[{dynamic_content}]}}'

    def setRequest(self):
        try:
            cBaseAnalysis.setRequest(self)
        except:
            print(traceback.print_exc(1))

    def getResponse(self):
        try:
            #返回格式：{"location":{"address":{"region":"湖北省","county":"洪山区","street":"关山街街道","street_number":"鲁巷","city":"武汉市","country":"中国"},"longitude":"114.39895","latitude":"30.50338","accuracy":"100"},"access_token":"abc9f9be-0d8e-4c90-8c34-8129131cd695"}
            result = self.conn.getresponse().read().decode("utf-8")
            print(result)
            temp = re.findall(r"\d{1,3}\.\d{2,}", result)
            if len(temp) < 2:
                temp = ['0','0']
        except:
            print(traceback.print_exc(1))
            temp=['0','0']
        self.conn.close()
        return (temp[0],temp[1])

    def creatDynamicContent(self, __structBSDataFormat):
        cBaseAnalysis.creatDynamicContent(self, __structBSDataFormat)

    def analysisRawData(self, __rawdata):
        return cBaseAnalysis.analysisRawData(self, __rawdata)
