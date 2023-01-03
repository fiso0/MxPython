#!/usr/bin/python
# -*- coding: utf-8 -*-

from .BaseAnalysis import *

import traceback


class cHaoservice_Analysis(cBaseAnalysis):
    '''好服务 分析'''

    def __init__(self, __key):
       cBaseAnalysis.__init__(self, __key)
       self.domain_name = 'api.haoservice.com'
       #字符串占位符前后有双引号，双引号必须特殊处理
       self.dynamic_template = '{{"macaddress":"{mac_address}","time":"0","singalstrength":"{signal_strength}"}}'
       #使用2个大括号，是因为format时，不认为是占位符
       self.request_template = '/api/viplbs?requestdata={{"wifilist":[{dynamic_content}],"mnctype":"gsm"}}&type=0&key={key}'

    def setRequest(self):
        try:
            cBaseAnalysis.setRequest(self)
        except:
            print(traceback.print_exc(1))

    def getResponse(self):
        try:
            #返回格式：{"location":{"address":{"region":"湖北省","county":"洪山区","street":"关山街街道","street_number":"上钱村","city":"武汉市","country":"中国"},"addressDescription":"湖北省武汉市洪山区尖东智能花园关山街街道上钱村湖北省现代技术学校东","longitude":114.393680,"latitude":30.505440,"accuracy":"100"},"access_token":null,"ErrCode":"0"}
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
