#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'previewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWebKit, QtWebKitWidgets
from Analysis.Haoservice_Analysis import *
from Analysis.Mapbar_Analysis import *
from Analysis.Heclouds_Analysis import *
from Analysis.Amap_Analysis import *
from Analysis.ConvertAny2BaiDu import *
from .coordTransform_utils import *
from Analysis.BaseAnalysis import *
from Analysis.Zxbd_Analysis import *

import re
import time
import csv
import collections
import datetime
import copy
import traceback

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    '''不包含菜单的用户界面'''
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(866, 688)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.webView = QtWebKit.QWebView(self.groupBox)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("baidu.htm")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout_2.addWidget(self.webView)
        self.groupBox_2 = QtGui.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.table = QtGui.QTableWidget(1,10,self.groupBox_2)
        self.table.setObjectName(_fromUtf8("table"))
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.verticalLayout.addWidget(self.table)
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(_fromUtf8("PushButton"))

        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.splitter)
        self.retranslateUi(Form)
        #self.pushButton.clicked.connect( self.on_PushButton_click)
        #self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self ,QtCore.SLOT("on_PushButton_click()"))


    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "百度地图", None))
        self.groupBox_2.setTitle(_translate("Form", "经纬度对比", None))
        self.pushButton.setText(_translate("Form", "地图显示数据", None))



class Previewer(QtGui.QWidget, Ui_Form):
    '''没有菜单的用户界面封装成QWidget，方便装入mainwindow'''
    def __init__(self, parent=None):
        super(Previewer, self).__init__(parent)
        self.setupUi(self)
        #self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self ,QtCore.SLOT("on_PushButton_click()"))
        #self.pushButton.clicked.connect(self.on_PushButton_click)



class MainWindow(QtGui.QMainWindow):
    '''包含了菜单+用户功能界面的窗口'''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        self.centralWidget = Previewer(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.pushButton.addAction(self.openAct)
        self.connect(self.centralWidget.pushButton, QtCore.SIGNAL("clicked()"), self ,QtCore.SLOT("on_PushButton_click()"))

    @QtCore.pyqtSlot()
    def on_PushButton_click(self):
        self.centralWidget.webView.page().mainFrame().evaluateJavaScript('clearMarkers();');
        for i,__colIndex in enumerate([1,3,6,9,12,15,18,21,24,27]): #pyqt table 中有效的经纬度列索引
            if __colIndex<self.centralWidget.table.columnCount():
                self.drawingMarsMarker(__colIndex,i)#火星到地球坐标转换
            time.sleep(0.2)

    def drawingMarsMarker(self,__colIndex,__index):
        __lngs = []
        __lats = []
        __selrowsrange=self.centralWidget.table.selectedRanges()

        for __rowIndex in range(0, self.centralWidget.table.rowCount()-1):
            isvalidrow=False
            if len(__selrowsrange)>0:
                for __rangeIndex in range(0,len(__selrowsrange)):
                    top=__selrowsrange[__rangeIndex].topRow()
                    bottom=__selrowsrange[__rangeIndex].bottomRow()
                    if __rowIndex>=top and __rowIndex<=bottom:
                        isvalidrow=True
                        break;
            if isvalidrow==False:
                continue;

            if str(self.centralWidget.table.item(__rowIndex,__colIndex).text())=='0'or str(self.centralWidget.table.item(__rowIndex,__colIndex+1).text())=='0':
                continue
            if (len(__lngs)+1) % 3!=0:#百度 地图 api addmarker一次只能绘制10个点
                __lngs.append(str(self.centralWidget.table.item(__rowIndex,__colIndex).text().toUtf8()))
                __lats.append(str(self.centralWidget.table.item(__rowIndex,__colIndex+1).text().toUtf8()))
            else:
                __lngs.append(str(self.centralWidget.table.item(__rowIndex,__colIndex).text().toUtf8()))
                __lats.append(str(self.centralWidget.table.item(__rowIndex,__colIndex+1).text().toUtf8()))
                #坐标转换
                baiduLLH = convertAny2Baidu(__colIndex,__lngs,__lats)
                __lngs=baiduLLH[0]
                __lats=baiduLLH[1]
                __js=str.format('lngs=[%s];lats=[%s]; addMarkers(lngs,lats,%s);' % (",".join(__lngs).encode('utf-8'),",".join(__lats).encode('utf-8'),str(__index)))
                #print __js
                if len(__lngs) > 0:
                    self.centralWidget.webView.page().mainFrame().evaluateJavaScript(__js)
                __lngs = []
                __lats = []
        #坐标转换
        baiduLLH = convertAny2Baidu(__colIndex,__lngs,__lats)
        __lngs=baiduLLH[0]
        __lats=baiduLLH[1]
        __js=str.format('lngs=[%s];lats=[%s]; addMarkers(lngs,lats,%s);' % (",".join(__lngs).encode('utf-8'),",".join(__lats).encode('utf-8'),str(__index)))
        print(__js)
        if len(__lngs) > 0:
            self.centralWidget.webView.page().mainFrame().evaluateJavaScript(__js)


    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open Log file", triggered=self.open0)
                
        self.openAct1 = QtGui.QAction("Haoservice", self,
                statusTip="Open Log file", triggered=self.open1)
        self.openAct2 = QtGui.QAction("Mapbar", self,
                statusTip="Open Log file", triggered=self.open2)
        self.openAct3 = QtGui.QAction("Heclouds", self,
               statusTip="Open Log file", triggered=self.open3)
        self.openAct4 = QtGui.QAction("Amap", self,
                statusTip="Open Log file", triggered=self.open4)

        self.openAct5 = QtGui.QAction("Haoservice", self,
                statusTip="Open Log file", triggered=self.open5)
        self.openAct6 = QtGui.QAction("Mapbar", self,
                statusTip="Open Log file", triggered=self.open6)
        self.openAct7 = QtGui.QAction("Heclouds", self,
               statusTip="Open Log file", triggered=self.open7)
        self.openAct8 = QtGui.QAction("Amap", self,
                statusTip="Open Log file", triggered=self.open8)

        self.maskAct = QtGui.QAction("&Mask some cols", self,checkable=True,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="隐藏一些列", triggered=self.mask)
        self.exitAct = QtGui.QAction("E&xit", self,
                shortcut=QtGui.QKeySequence.Quit,
                statusTip="Exit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.openMenu1 = self.fileMenu.addMenu("&Open1")
        #self.openMenu2 = self.fileMenu.addMenu("&Open2")
        self.fileMenu.addAction(self.maskAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        
        self.openMenu1.addAction(self.openAct1)
        self.openMenu1.addAction(self.openAct2)
        #self.openMenu1.addAction(self.openAct3)
        self.openMenu1.addAction(self.openAct4)

        #self.openMenu2.addAction(self.openAct5)
        #self.openMenu2.addAction(self.openAct6)
        #self.openMenu2.addAction(self.openAct7)
        #self.openMenu2.addAction(self.openAct8)
        
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def about(self):
        QtGui.QMessageBox.about(self, "About Previewer",
                "The <b>Previewer</b> example demonstrates how to view HTML "
                "documents using a QtWebKit.QWebView.")

    def open(self, __type):
        __openfileName = QtGui.QFileDialog.getOpenFileName(self,filter="Log (*.Log)")
        if __openfileName:
            self.centralWidget.table.clear()
            for i in range(self.centralWidget.table.rowCount()-1,0,-1):
                self.centralWidget.table.removeRow(i-1)
            self.workThread=workThread()
            self.workThread.openfileName=str(__openfileName.toUtf8()).decode("utf-8")
            self.workThread.parent=self
            self.workThread.type=__type
            self.workThread.start(QtCore.QThread.LowestPriority)
    
    def open0(self):
        self.open(0)#4种web 服务 验证
    def open1(self):
        self.open(1)#haoservice web 服务验证
    def open2(self):
        self.open(2)#mapbar web 服务验证
    def open3(self):
        self.open(3)#heclouds web 服务验证
    def open4(self):
        self.open(4)#amap web 服务验证     

    def open5(self):
        self.open(5)#haoservice 与 中心北斗  web 服务验证
    def open6(self):
        self.open(6)#mapbar 与 中心北斗  web 服务验证
    def open7(self):
        self.open(7)#heclouds 与 中心北斗 web 服务验证
    def open8(self):
        self.open(8)#amap 与 中心北斗 web 服务验证

    def mask(self):
        if self.maskAct.isChecked():
            for __colIndex in [3,4,6,7,9,10,12,13,15,16,18,19,21,22,24,25,27,28]: #pyqt table 中有效的经纬度列索引
                if __colIndex<self.centralWidget.table.columnCount():
                    self.centralWidget.table.setColumnHidden(__colIndex,True)
            for __colIndex in [5,8,11,14,17,20,23,26]: #pyqt table 中有效的经纬度 差值列 索引
                if __colIndex<self.centralWidget.table.columnCount():
                 self.centralWidget.table.setColumnHidden(__colIndex,False)
        else:
            for __colIndex in [3,4,6,7,9,10,12,13,15,16,18,19,21,22,24,25,27,28]: #pyqt table 中有效的经纬度列索引
                if __colIndex<self.centralWidget.table.columnCount():
                    self.centralWidget.table.setColumnHidden(__colIndex,False)
            for __colIndex in [5,8,11,14,17,20,23,26]: #pyqt table 中有效的经纬度 差值列 索引
                if __colIndex<self.centralWidget.table.columnCount():
                 self.centralWidget.table.setColumnHidden(__colIndex,True)

    def setItems2Table(self, __rowcount, __dict):
        if __rowcount==0 or len(__dict)>self.centralWidget.table.columnCount():# 修改行 title
            self.centralWidget.table.setColumnCount(len(__dict))
            __horHeader=QtCore.QStringList()
            for key in list(__dict.keys()):
                __horHeader.append(str(key))
            self.centralWidget.table.setHorizontalHeaderLabels(__horHeader)

        self.centralWidget.table.insertRow(self.centralWidget.table.rowCount())

        _col=0
        for key, value in list(__dict.items()):
            __tableitem = QtGui.QTableWidgetItem()
            __tableitem.setData(0,value)    #For numerical sortiing, set the data as integers, not as text:
            self.centralWidget.table.setItem(__rowcount,_col,__tableitem)
            _col+=1

class workThread(QtCore.QThread):
    def __int__(self):
        super(workThread,self).__init__()

    def run(self):
        self.parent.centralWidget.table.setSortingEnabled(False)
        if self.type==0:
            processLogFile(self.openfileName ,self.parent)
        elif self.type >= 1 and self.type <= 4:
            processLogFile1(self.openfileName ,self.parent, self.type)
        else:
            processLogFile2(self.openfileName ,self.parent, self.type)
        self.parent.centralWidget.table.setSortingEnabled(True)

def processLogFile(__logfilepath,__parent):
    #文件格式：
    ##GPS 08:16:54,114.393862,30.505299
    #WIFI 00:27:1d:1a:64:35,-93,ap1|ec:26:ca:e1:66:c7,-81,ap2|ec:26:ca:ad:8d:11,-89,ap3|12:27:1d:1a:64:35,-92,ap4|50:bd:5f:15:b9:dd,-62,ap5
    #str1='cell_nbr,460:00:28730:55272:-60|460:00:28734:42184:-72|460:00:28730:55270:-77|460:00:28730:45272:-77|460:00:28730:9983:-80|460:00:28730:55271:-83|460:00:28721:15113:-86'
    __str1 = ''
    __log = open(__logfilepath,'r')

    try:
        __result=[]
        __dict = collections.OrderedDict()
        __rowcount=0
        __lines = __log.readlines()
        for (i,__row) in enumerate(__lines):
            if __row.count('WIFI') == 0 or i == 0 :
                    continue
            else:
                __temp = re.findall(r'\d+\.+\d{6}', __lines[i - 1])
                if len(__temp) != 2:
                    continue
                else:
                    __dict.clear()
                    __time=re.findall(r'\d{2}:\d{2}:\d{2}',__lines[i-1])
                    if len(__time) == 1:
                        __dict['time']=__time[0]
                    else:
                        __dict['time']='99:99:99'
                    __temp1 = wgs84togcj02(float( __temp[0]),float(__temp[1]))
                    __temp[0]=str(__temp1[0])
                    __temp[1]=str(__temp1[1])
                    #print (__temp[0],__temp[1])
                    __dict['std_lng']=__temp[0]
                    __dict['std_lat']=__temp[1]
                    __str1 = str.replace(__row,'\n','')
                    #print (i, __str1)
                    try:
                        objHaoservice_Analysis = cHaoservice_Analysis('f6563df4a8794636a8653c8a42029cfb')
                        processedData = objHaoservice_Analysis.analysisRawData(__str1)
                        objHaoservice_Analysis.creatDynamicContent(processedData)
                        objHaoservice_Analysis.setRequest()
                        lng,lat = objHaoservice_Analysis.getResponse()
                        __dict['Hao_lng']=lng
                        __dict['Hao_lat']=lat
                        __dict['Hao_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                    except Exception as e:
                        pass
                    time.sleep(0.1)

                    try:
                        objMapbar_Analysis_ = cMapbar_Analysis('abc9f9be-0d8e-4c90-8c34-8129131cd695')
                        processedData = objMapbar_Analysis_.analysisRawData(__str1)
                        objMapbar_Analysis_.creatDynamicContent(processedData)
                        objMapbar_Analysis_.setRequest()
                        lng,lat = objMapbar_Analysis_.getResponse()
                        __dict['Mapbar_lng']=lng
                        __dict['Mapbar_lat']=lat
                        __dict['Mapbar_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                    except Exception as e:
                        pass
                    time.sleep(0.1)

                    try:
                        objAmap_Analysis = cAmap_Analysis('01605561cc68306b74c043db28d9e4db')
                        processedData = objAmap_Analysis.analysisRawData(__str1)
                        objAmap_Analysis.creatDynamicContent(processedData)
                        objAmap_Analysis.setRequest()
                        lng,lat = objAmap_Analysis.getResponse()
                        __dict['Amap_lng']=lng
                        __dict['Amap_lat']=lat
                        __dict['Amap_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                    except Exception as e:
                        pass
                    time.sleep(0.1)

                    __result.append(copy.copy(__dict))
                    #__parent.centralWidget.table.setColumnCount(len(__dict))
                    __parent.setItems2Table(__rowcount,__dict)
                    __rowcount+=1
    finally:
        __log.close()
        with open(str.format('WIFI定位数据_%s.csv' % datetime.datetime.now().strftime('%Y%m%d %H%M%S %f')[:-3] ).decode('utf-8'), 'w') as csvfile:
            fieldnames=list(__dict.keys())
            dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(__result)  # rows就是表单提交的数据

def processLogFile1(__logfilepath,__parent, __type):
    #文件格式：
    ##GPS 08:16:54,114.393862,30.505299
    # WIFI 00:27:1d:1a:64:35,-93,ap1|ec:26:ca:e1:66:c7,-81,ap2|ec:26:ca:ad:8d:11,-89,ap3|12:27:1d:1a:64:35,-92,ap4|50:bd:5f:15:b9:dd,-62,ap5
    #str1='cell_nbr,460:00:28730:55272:-60|460:00:28734:42184:-72|460:00:28730:55270:-77|460:00:28730:45272:-77|460:00:28730:9983:-80|460:00:28730:55271:-83|460:00:28721:15113:-86'
    __str1 = ''
    __log = open(__logfilepath,'r')

    try:
        __result=[]
        __dict = collections.OrderedDict()
        __rowcount=0
        __lines = __log.readlines()
        fieldnames=[]
        for (i,__row) in enumerate(__lines):
            if __row.count('WIFI') == 0 or i == 0 :
                    continue
            else:
                __temp = re.findall(r'\d+\.+\d{6}', __lines[i - 1])
                if len(__temp) != 2:
                    continue
                else:
                    __dict.clear()
                    __time=re.findall(r'\d{2}:\d{2}:\d{2}',__lines[i-1])
                    if len(__time) == 1:
                        __dict['time']=__time[0]
                    else:
                        __dict['time']='99:99:99'
                    __temp1 = wgs84togcj02(float( __temp[0]),float(__temp[1]))
                    __temp[0]=str(__temp1[0])
                    __temp[1]=str(__temp1[1])
                    #print (__temp[0],__temp[1])
                    __dict['std_lng']=__temp[0]
                    __dict['std_lat']=__temp[1]
                    __str1 = str.replace(__row,'\n','')
                    #print (i, __str1)
                    if __type==1:
                        try:
                            objHaoservice_Analysis =cHaoservice_Analysis('f6563df4a8794636a8653c8a42029cfb')
                            processedData = objHaoservice_Analysis.analysisRawData(__str1)
                            
                            objHaoservice_Analysis.creatDynamicContent(processedData)
                            objHaoservice_Analysis.setRequest()
                            lng,lat = objHaoservice_Analysis.getResponse()
                            __dict['Hao_lng_M']=lng
                            __dict['Hao_lat_M']=lat
                            __dict['Hao_delta_M']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objHaoservice_Analysis.creatDynamicContent(_temp)
                            objHaoservice_Analysis.setRequest()
                            lng,lat = objHaoservice_Analysis.getResponse()
                            __dict['Hao_lng_S']=lng
                            __dict['Hao_lat_S']=lat
                            __dict['Hao_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            for (j, item) in enumerate(processedData):
                                try:
                                    __templist=[]
                                    __templist.append(item)
                                    objHaoservice_Analysis.creatDynamicContent(__templist)
                                    objHaoservice_Analysis.setRequest()
                                    lng,lat = objHaoservice_Analysis.getResponse()
                                    __dict[str.format('Hao_lng_%s' % j)]=lng
                                    __dict[str.format('Hao_lat_%s' % j)]=lat
                                    __dict[str.format('Hao_delta_%s' % j)]=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                                    time.sleep(0.1)
                                except:
                                    pass
                        except Exception as e:
                            pass
                        time.sleep(0.1)
                        
                    if __type==2:
                        try:
                            objMapbar_Analysis_ = cMapbar_Analysis('abc9f9be-0d8e-4c90-8c34-8129131cd695')
                            processedData = objMapbar_Analysis_.analysisRawData(__str1)
                            objMapbar_Analysis_.creatDynamicContent(processedData)
                            objMapbar_Analysis_.setRequest()
                            lng,lat = objMapbar_Analysis_.getResponse()
                            __dict['Mapbar_lng']=lng
                            __dict['Mapbar_lat']=lat
                            __dict['Mapbar_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objMapbar_Analysis_.creatDynamicContent(_temp)
                            objMapbar_Analysis_.setRequest()
                            lng,lat = objMapbar_Analysis_.getResponse()
                            __dict['Mapbar_lng_S']=lng
                            __dict['Mapbar_lat_S']=lat
                            __dict['Mapbar_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            for (j, item) in enumerate(processedData):
                                try:
                                    __templist=[]
                                    __templist.append(item)
                                    objMapbar_Analysis_.creatDynamicContent(__templist)
                                    objMapbar_Analysis_.setRequest()
                                    lng,lat = objMapbar_Analysis_.getResponse()
                                    __dict[str.format('Mapbar_lng_%s' % j)]=lng
                                    __dict[str.format('Mapbar_lat_%s' % j)]=lat
                                    __dict[str.format('Mapbar_delta_%s' % j)]=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                                    time.sleep(0.1)
                                except:
                                    print(traceback.format_exc())
                                    pass
                        except Exception as e:
                            pass
                        time.sleep(0.1)

                    if __type==4:
                        try:
                            objAmap_Analysis = cAmap_Analysis('01605561cc68306b74c043db28d9e4db')
                            processedData = objAmap_Analysis.analysisRawData(__str1)
                            objAmap_Analysis.creatDynamicContent(processedData)
                            objAmap_Analysis.setRequest()
                            lng,lat = objAmap_Analysis.getResponse()
                            __dict['Amap_lng']=lng
                            __dict['Amap_lat']=lat
                            __dict['Amap_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objAmap_Analysis.creatDynamicContent(_temp)
                            objAmap_Analysis.setRequest()
                            lng,lat = objAmap_Analysis.getResponse()
                            __dict['Amap_lng_S']=lng
                            __dict['Amap_lat_S']=lat
                            __dict['Amap_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            for (j, item) in enumerate(processedData):
                                try:
                                    __templist=[]
                                    __templist.append(item)
                                    objAmap_Analysis.creatDynamicContent(__templist)
                                    objAmap_Analysis.setRequest()
                                    lng,lat = objAmap_Analysis.getResponse()
                                    __dict[str.format('Amap_lng_%s' % j)]=lng
                                    __dict[str.format('Amap_lat_%s' % j)]=lat
                                    __dict[str.format('Amap_delta_%s' % j)]=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                                    time.sleep(0.1)
                                except Exception as e:
                                    print(traceback.format_exc())
                                    pass
                        except Exception as e:
                            pass
                        time.sleep(0.1)

                    __result.append(copy.copy(__dict))
                    #__parent.centralWidget.table.setColumnCount(len(__dict))
                    __parent.setItems2Table(__rowcount,__dict)
                    __rowcount+=1
            if len(__dict)>len(fieldnames):
                fieldnames=list(__dict.keys())
    finally:
        __log.close()
        with open(str.format('单基站定位数据_%s.csv' % datetime.datetime.now().strftime('%Y%m%d %H%M%S %f')[:-3] ).decode('utf-8'), 'w') as csvfile:

            dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(__result)  # rows就是表单提交的数据

def processLogFile2(__logfilepath,__parent, __type):
    #文件格式：
    ##GPS 08:16:54,114.393862,30.505299
    # WIFI 00:27:1d:1a:64:35,-93,ap1|ec:26:ca:e1:66:c7,-81,ap2|ec:26:ca:ad:8d:11,-89,ap3|12:27:1d:1a:64:35,-92,ap4|50:bd:5f:15:b9:dd,-62,ap5
    #str1='cell_nbr,460:00:28730:55272:-60|460:00:28734:42184:-72|460:00:28730:55270:-77|460:00:28730:45272:-77|460:00:28730:9983:-80|460:00:28730:55271:-83|460:00:28721:15113:-86'
    __str1 = ''
    __log = open(__logfilepath,'r')

    try:
        __result=[]
        __dict = collections.OrderedDict()
        __rowcount=0
        __lines = __log.readlines()
        fieldnames=[]
        for (i,__row) in enumerate(__lines):
            if __row.count('WIFI') == 0 or i == 0 :
                    continue
            else:
                __temp = re.findall(r'\d+\.+\d{6}', __lines[i - 1])
                if len(__temp) != 2:
                    continue
                else:
                    __dict.clear()
                    __time=re.findall(r'\d{2}:\d{2}:\d{2}',__lines[i-1])
                    if len(__time) == 1:
                        __dict['time']=__time[0]
                    else:
                        __dict['time']='99:99:99'
                    __temp1 = wgs84togcj02(float( __temp[0]),float(__temp[1]))
                    __temp[0]=str(__temp1[0])
                    __temp[1]=str(__temp1[1])
                    #print (__temp[0],__temp[1])
                    __dict['std_lng']=__temp[0]
                    __dict['std_lat']=__temp[1]
                    __str1 = str.replace(__row,'\n','')
                    #print (i, __str1)
                    if __type==5:
                        try:
                            objHaoservice_Analysis =cHaoservice_Analysis('f6563df4a8794636a8653c8a42029cfb')
                            processedData = objHaoservice_Analysis.analysisRawData(__str1)

                            objHaoservice_Analysis.creatDynamicContent(processedData)
                            objHaoservice_Analysis.setRequest()
                            lng,lat = objHaoservice_Analysis.getResponse()
                            __dict['Hao_lng_M']=lng
                            __dict['Hao_lat_M']=lat
                            __dict['Hao_delta_M']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objHaoservice_Analysis.creatDynamicContent(_temp)
                            objHaoservice_Analysis.setRequest()
                            lng,lat = objHaoservice_Analysis.getResponse()
                            __dict['Hao_lng_S']=lng
                            __dict['Hao_lat_S']=lat
                            __dict['Hao_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            objZxbd_Analysis =cZxbd_Analysis('')
                            objZxbd_Analysis.creatDynamicContent(_temp)
                            objZxbd_Analysis.setRequest()
                            lng,lat = objZxbd_Analysis.getResponse()
                            lng,lat=wgs84togcj02(float(lng),float(lat))
                            __dict['Zxbd_lng_S']=lng
                            __dict['Zxbd_lat_S']=lat
                            __dict['Zxbd_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)
                        except Exception as e:
                            pass
                        time.sleep(0.1)

                    if __type==6:
                        try:
                            objMapbar_Analysis_ = cMapbar_Analysis('abc9f9be-0d8e-4c90-8c34-8129131cd695')
                            processedData = objMapbar_Analysis_.analysisRawData(__str1)
                            objMapbar_Analysis_.creatDynamicContent(processedData)
                            objMapbar_Analysis_.setRequest()
                            lng,lat = objMapbar_Analysis_.getResponse()
                            __dict['Mapbar_lng']=lng
                            __dict['Mapbar_lat']=lat
                            __dict['Mapbar_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objMapbar_Analysis_.creatDynamicContent(_temp)
                            objMapbar_Analysis_.setRequest()
                            lng,lat = objMapbar_Analysis_.getResponse()
                            __dict['Mapbar_lng_S']=lng
                            __dict['Mapbar_lat_S']=lat
                            __dict['Mapbar_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            objZxbd_Analysis =cZxbd_Analysis('')
                            objZxbd_Analysis.creatDynamicContent(_temp)
                            objZxbd_Analysis.setRequest()
                            lng,lat = objZxbd_Analysis.getResponse()
                            lng,lat=wgs84togcj02(float(lng),float(lat))
                            __dict['Zxbd_lng_S']=lng
                            __dict['Zxbd_lat_S']=lat
                            __dict['Zxbd_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)
                        except Exception as e:
                            pass
                        time.sleep(0.1)

                    if __type==8:
                        try:
                            objAmap_Analysis = cAmap_Analysis('01605561cc68306b74c043db28d9e4db')
                            processedData = objAmap_Analysis.analysisRawData(__str1)
                            objAmap_Analysis.creatDynamicContent(processedData)
                            objAmap_Analysis.setRequest()
                            lng,lat = objAmap_Analysis.getResponse()
                            __dict['Amap_lng']=lng
                            __dict['Amap_lat']=lat
                            __dict['Amap_delta']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])

                            _temp=[findMaxSignal_Strength(processedData)]
                            objAmap_Analysis.creatDynamicContent(_temp)
                            objAmap_Analysis.setRequest()
                            lng,lat = objAmap_Analysis.getResponse()
                            __dict['Amap_lng_S']=lng
                            __dict['Amap_lat_S']=lat
                            __dict['Amap_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)

                            objZxbd_Analysis =cZxbd_Analysis('')
                            objZxbd_Analysis.creatDynamicContent(_temp)
                            objZxbd_Analysis.setRequest()
                            lng,lat = objZxbd_Analysis.getResponse()
                            lng,lat=wgs84togcj02(float(lng),float(lat))
                            __dict['Zxbd_lng_S']=lng
                            __dict['Zxbd_lat_S']=lat
                            __dict['Zxbd_delta_S']=mx_base_calc_distance(lng,lat,__temp[0],__temp[1])
                            time.sleep(0.1)
                        except Exception as e:
                            pass
                        time.sleep(0.1)

                    __result.append(copy.copy(__dict))
                    #__parent.centralWidget.table.setColumnCount(len(__dict))
                    __parent.setItems2Table(__rowcount,__dict)
                    __rowcount+=1
            if len(__dict)>len(fieldnames):
                fieldnames=list(__dict.keys())
    finally:
        __log.close()
        with open(str.format('对比基站定位数据_%s.csv' % datetime.datetime.now().strftime('%Y%m%d %H%M%S %f')[:-3] ).decode('utf-8'), 'w') as csvfile:

            dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(__result)  # rows就是表单提交的数据

def findMaxSignal_Strength( __processedData):
    __structWIFIDataFormat=structWIFIDataFormat()
    __structWIFIDataFormat.signal_strength=-999
    for (j, item) in enumerate(__processedData):
        if int(item.signal_strength) > int(__structWIFIDataFormat.signal_strength) :
            __structWIFIDataFormat=item
    return __structWIFIDataFormat

def convertAny2Baidu(__srcCoord, __lngs,__lats):#srcCoord 表示源坐标的代码=0时，wgs84坐标，非0时，国测局坐标
    if len(__lngs)==0 or len(__lats)==0:
        return ((),())
    objConvertAny2BaiDu = cConvertAny2BaiDu('kSawRGwppT4aGXg3B67zq5zlWb2Bzd3P')
    if __srcCoord==0:
        objConvertAny2BaiDu.srcCoord=3
    else:
        objConvertAny2BaiDu.srcCoord=3
    #构成生数据格式：114.3938:30.5053|114.3938:30.5053|114.3938:30.5053
    __temp=[]
    for i in range(0,len(__lngs)):
        __temp.append(str.format('{lng}:{lat}',lng=__lngs[i],lat=__lats[i]))
    processedData = objConvertAny2BaiDu.analysisRawData('|'.join(__temp))
    objConvertAny2BaiDu.creatDynamicContent(processedData)
    objConvertAny2BaiDu.setRequest()
    result = objConvertAny2BaiDu.getResponse()
    return (result[::2],result[1::2])

def mx_base_calc_distance(lat1,lon1,lat2,lon2):
    EARTH_RADIUS = 6378*1000 # meters
    PI = 3.141592654
    radLat1=0
    radLat2=0
    a=0
    b=0
    s=0
    radLat1 = float(lat1) * PI / 180.0
    radLat2 = float(lat2) * PI / 180.0
    a = radLat1 - radLat2;
    b = float(lon1) * PI / 180.0 - float(lon2) * PI / 180.0
    s = 2 * math.asin(math.sqrt((math.sin(a / 2)*math.sin(a / 2)) + math.cos(radLat1)*math.cos(radLat2)*(math.sin(b / 2)*math.sin(b / 2))))
    s = s * EARTH_RADIUS

    return float(str.format('%.1f' % s))


