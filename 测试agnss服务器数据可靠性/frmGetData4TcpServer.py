# -*- coding:utf-8 -*-

import tkinter
import socket
import ctypes
import traceback
import sys
import time
import _thread
import datetime
import logging

HTTP_REQ = "GET /v1/device/agnss?client_id=cmcc-mxt535&device_id=56674060511518&protocol=whmx&data_type=eph&gnss=gps%2Cbds&pos=30.50%2C114.39 HTTP/1.1\r\n\r\n"

# 窗口类,获取服务器上面的数据
class frmGetData4TcpServer(tkinter.Frame):
    def __init__(self, master=None):
        """
        构造函数
        """
        tkinter.Frame.__init__(self, master)
        self.text_address = tkinter.Text(self, width=50, height=1)
        self.button_link = tkinter.Button(self, width=5, height=1)
        self.text_info = tkinter.Text(self, width=250, height=100)
        self.pack()
        self.initcomponents()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('%s.log' % __name__)
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(handler)

    def initcomponents(self):
        """
        初始化控件
        """
        self.text_address.grid({"row": "0", "column": "0"})
        self.text_address.insert(1.0, '27.17.32.34:32101')
        # self.hi_there.pack({"side": "left"})

        self.button_link["text"] = "连接"
        self.button_link["fg"] = "red"
        self.button_link["command"] = self.loop
        self.button_link.grid({"row": "0", "column": "1"})

        # self.button_quit.pack({"side": "left","ipadx":"100"})
        self.text_info.grid({"row": "1", "column": "0", "columnspan": "2"})

    def loop(self):
        """
        使用线程调用真正的功能函数
        """
        _thread.start_new(self.linkTcpServer, ())

    def linkTcpServer(self):
        """
        功能函数
        """
        while True:
            tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            buf = ""
            starttime = ""
            endtime = ""
            errinfo = ""
            try:
                # 解析服务器ip地址，并连接服务器，下发指令
                if self.text_address.get(1.0) != "":
                    address = self.text_address.get(1.0, 2.0)
                    address = address.strip()
                    ip, port = address.split(':')
                    try:
                        tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        #tcpclient.settimeout(10)
                        starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        tcpclient.connect((ip, int(port)))
                        tcpclient.send(bytes(HTTP_REQ, 'utf-8'))
                        while True:
                            recv = tcpclient.recv(1024)
                            buf = buf + str(recv, 'utf-8')
                            if len(recv) == 0:
                                break
                            else:
                                time.sleep(0.1)
                        endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    except Exception as e:
                        endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        self.logger.error("网络错误;starttime=%s;endtime=%s;buf=%s" % (starttime, endtime, len(buf)), exc_info=True)
                    finally:
                        # 打印接收数据到界面
                        self.text_info.delete(0.0, 50.0)
                        time.sleep(1)
                        self.text_info.insert(1.0, buf)
                        i = buf.find('$')
                        if i > 0:
                            datalen = len(buf) - i
                            self.text_info.insert(30.0, "数据长度=%d\r\n" % datalen)
                            bufs = buf.split('\n')
                            if bufs[2].find(str(datalen)) > -1:
                                self.text_info.insert(31.0, "数据长度匹配\r\n"+endtime)
                                self.logger.info("数据长度匹配;starttime=%s;endtime=%s;len1=%s;len2=%s" % (starttime, endtime,bufs[2],datalen ))
                            else:
                                self.text_info.insert(31.0, "数据长度不匹配，已经保存记录")
                                file_name = starttime.replace(':','-') + '.log'
                                f = open(file_name, 'wb')
                                f.write(buf)
                                f.close()
                                self.logger.info("数据长度不匹配;starttime=%s;endtime=%s;len1=%s;len2=%s" % (starttime, endtime,bufs[2],datalen ))
            except Exception as e:
                self.logger.error("其他异常", exc_info=True)
            finally:
                tcpclient.close()
                time.sleep(5)
