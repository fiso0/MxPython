#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest
from aliyunsdkiot.request.v20170420 import PubRequest
from aliyunsdkiot.request.v20170420 import RRpcRequest

accessKeyId = '<your accessKey>'
accessKeySecret = '<your accessSecret>'
clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-shanghai')

rrpcRequest = RRpcRequest()
rrpcRequest.setProductKey("...") #设备所属产品的Key
rrpcRequest.setDeviceName("...") #设备名称
# rrpcRequest.setRequestBase64Byte(Base64.encodeBase64String("{\"action\":\unlock\}".getBytes())) #发给设备的数据，要求二进制数据做一次Base64编码
rrpcRequest.setTimeOut(1000) #超时时间，单位毫秒，如果超过这个时间设备没反应则返回"TIMEOUT"
rrpcResponse = client.getAcsResponse(rrpcRequest) #得到设备返回的数据信息
print(rrpcResponse.getPayloadBase64Byte()) #得到的数据是设备返回二进制数据然后再经过Base64编码之后的字符串，需要转换一下才能拿到原始的二进制数据
print(rrpcResponse.getRrpcCode()) #对应的响应码(UNKNOW/SUCCESS/TIMEOUT/OFFLINE/HALFCONN等)