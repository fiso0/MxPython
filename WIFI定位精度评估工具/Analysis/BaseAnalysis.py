#!/usr/bin/python
# -*- coding: utf-8 -*-


import httplib
import re

class cBaseAnalysis:
    """基本分析类，key 和 解析 """

    key=''#授权号

    domain_name=''#http 域名

    dynamic_content=[] #动态内容
    dynamic_template=''#动态模版

    request_template='' #请求模版

    conn=None

    def __init__(self,__key):
       self.key = __key

    def setRequest(self):
        self.conn = httplib.HTTPConnection(self.domain_name,timeout=2)
        print str.format(self.request_template, key=self.key, dynamic_content=','.join(self.dynamic_content))
        self.conn.request('GET',str.format(self.request_template, key=self.key, dynamic_content=','.join(self.dynamic_content)))

    def getResponse(self):
        pass

    def creatDynamicContent(self,__listStructWIFIDataFormat):
       #基站数据格式 mcc: mnc:lac:cid:rssi
        #驻留基站+临近基站
        #Log数据示例:
        #cell_nbr,460:00:28730:20736:-57|460:00:28730:35594:-103|460:00:28968:10222:-103|460:00:28720:15545:-104|460:00:28730:45272:-105|460:00:28730:10404:-105|460:00:28730:45271:-105
        #如果临近基站有6个，表示如下
        #cell|nbr1|nbr2|nbr3|nbr4|nbr5|nbr6
        #460:00:28730:20736:-61|460:00:28720:15545:-93|460:00:28712:11766:-99|460:00:28730:55272:-101|460:00:28730:63401:-107|460:00:28730:45271:-107
        del self.dynamic_content[:]
       # stri=str.format("")
        for item  in __listStructWIFIDataFormat[:]:
            self.dynamic_content.append(str.format(self.dynamic_template,
                                                   mac_address=item.mac_address,
                                                   signal_strength=item.signal_strength,
                                                   RSSI=item.RSSI))

    def analysisRawData(self, __rawdata):
        #生数据格式：#WIFI 00:27:1d:1a:64:35,-93,ap1|ec:26:ca:e1:66:c7,-81,ap2|ec:26:ca:ad:8d:11,-89,ap3|12:27:1d:1a:64:35,-92,ap4|50:bd:5f:15:b9:dd,-62,ap5


        __listStructWIFIDataFormat=[]
        __array = re.split('[\s|]',__rawdata)
        for item in __array[1:]:
            __array1 = str.split(item,',')
            __structWIFIDataFormat = structWIFIDataFormat()
            __structWIFIDataFormat.mac_address = __array1[0]
            __structWIFIDataFormat.signal_strength = __array1[1]
            __structWIFIDataFormat.RSSI = __array1[2]
            __listStructWIFIDataFormat.append(__structWIFIDataFormat)
        return __listStructWIFIDataFormat

class structWIFIDataFormat:
    '''基站数据格式'''
    def __init__(self):
        self.mac_address = ''
        self.signal_strength = ''
        self.RSSI = ''

class structLLHDataFormat:
    '''经纬格式'''
    def __init__(self):
        self.lng = ''     # 经度
        self.lat = ''     # 纬度
