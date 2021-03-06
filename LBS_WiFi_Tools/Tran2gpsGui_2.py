#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import tran2GPS_2
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, \
	QTextEdit, QComboBox


EXAMPLE_SRVLOG = '''mx_srv_send_handle[337][4005]:&&&& 331 000000000866888a2a237294 <4005> <00-00-00 000000 0.000000 0.000000 0 0 0 0xff 0x00 46 E N 0x00 460:00:28730:20736 0x00 -63 17-01-24 09:52:09 0x00 0x00 50:bd:5f:15:b9:dd,-53,ap1|02:bd:5f:15:b9:dd,-53,ap2|00:27:1d:1a:59:2e,-58,ap3|12:27:1d:1a:59:2e,-58,ap4|02:27:1d:1a:59:2e,-58,ap5;20170124095209 460,00,28730,45271,-90|460,00,28730,45273,-95|460,00,28730,55271,-96|460,00,28730,63401,-98|460,00,28730,46075,-104> 00 05 0x9b'''
EXAMPLE_DB = '''4060	866888020237294	2017-01-28 14:49:31	1999-11-30 00:00:00	113.4465818	30.3695405	0	0	0	15	0	28	460	0	28914	51012	68	2017-01-28 14:49:18	460077171327454	2	0a:18:d6:5f:a4:b5,-77,ap1|48:28:2f:32:71:64,-84,ap2|1a:25:93:8e:5c:65,-88,ap3|0a:25:93:8e:5c:65,-88,ap4|1a:25:93:8e:5c:c9,-88,ap5;20170128144918	460,00,28914,60002,-59|460,00,28914,54642,-72|460,00,28914,56613,-76|460,00,28914,51013,-78|460,00,28914,60053,-78|460,00,28914,52793,-79'''
EXAMPLE_INPUT_LBS = '''460,00,28699,452,-73|460,00,28699,45932,-77|460,00,28699,451,-78|460,00,28699,32286,-83|460,00,28699,10453,-86|460,00,28699,32284,-86'''
EXAMPLE_INPUT_WIFI = '''50:bd:5f:15:b9:dd,-53,ap1|02:bd:5f:15:b9:dd,-53,ap2|00:27:1d:1a:59:2e,-58,ap3|12:27:1d:1a:59:2e,-58,ap4|02:27:1d:1a:59:2e,-58,ap5'''

class Tran2gpsGui(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		input_label = QLabel('原始数据：')

		src_label = QLabel('数据来源')
		self.src_combo = QComboBox()
		self.src_combo.addItems(['服务器log', '数据库','纯WiFi','纯LBS'])

		api_label = QLabel('API')
		self.api_combo = QComboBox()
		self.api_combo.addItems(['高德'])  # 目前仅一个选项
		self.api_combo.setEnabled(False)

		run_btn = QPushButton('转换')
		clr_btn = QPushButton('清空结果')

		lb_wifi = QLabel('纯WiFi：')
		lb_lbs = QLabel('纯LBS：')
		lb_mix = QLabel('混合：')
		lb_wifi.setFixedWidth(40)
		lb_lbs.setFixedWidth(40)
		lb_mix.setFixedWidth(40)

		hBox = QHBoxLayout()
		hBox.addWidget(src_label)
		hBox.addWidget(self.src_combo)
		hBox.addStretch()
		hBox.addWidget(api_label)
		hBox.addWidget(self.api_combo)
		hBox.addStretch()
		hBox.addWidget(run_btn)
		hBox.addWidget(clr_btn)

		self.in_text = QTextEdit()
		self.in_text.setAcceptRichText(False)

		self.req_wifi_text = QTextEdit()
		self.req_wifi_text.setAcceptRichText(False)
		self.req_wifi_text.setReadOnly(True)
		self.out_wifi_text = QTextEdit()
		self.out_wifi_text.setAcceptRichText(False)
		self.out_wifi_text.setReadOnly(True)
		hbox_wifi = QHBoxLayout()
		hbox_wifi.addWidget(lb_wifi)
		hbox_wifi.addWidget(self.req_wifi_text)
		hbox_wifi.addWidget(self.out_wifi_text)

		self.req_lbs_text = QTextEdit()
		self.req_lbs_text.setAcceptRichText(False)
		self.req_lbs_text.setReadOnly(True)
		self.out_lbs_text = QTextEdit()
		self.out_lbs_text.setAcceptRichText(False)
		self.out_lbs_text.setReadOnly(True)
		hbox_lbs = QHBoxLayout()
		hbox_lbs.addWidget(lb_lbs)
		hbox_lbs.addWidget(self.req_lbs_text)
		hbox_lbs.addWidget(self.out_lbs_text)

		self.req_mix_text = QTextEdit()
		self.req_mix_text.setAcceptRichText(False)
		self.req_mix_text.setReadOnly(True)
		self.out_mix_text = QTextEdit()
		self.out_mix_text.setAcceptRichText(False)
		self.out_mix_text.setReadOnly(True)
		hbox_mix = QHBoxLayout()
		hbox_mix.addWidget(lb_mix)
		hbox_mix.addWidget(self.req_mix_text)
		hbox_mix.addWidget(self.out_mix_text)

		self.req_wifi_text.setPlainText('WiFi请求')
		self.out_wifi_text.setPlainText('WiFi结果')
		self.req_lbs_text.setPlainText('LBS请求')
		self.out_lbs_text.setPlainText('LBS结果')
		self.req_mix_text.setPlainText('WiFi+LBS请求')
		self.out_mix_text.setPlainText('WiFi+LBS结果')
		self.req_wifi_text.setEnabled(False)
		self.out_wifi_text.setEnabled(False)
		self.req_lbs_text.setEnabled(False)
		self.out_lbs_text.setEnabled(False)
		self.req_mix_text.setEnabled(False)
		self.out_mix_text.setEnabled(False)

		vBox = QVBoxLayout()
		vBox.addWidget(input_label)
		vBox.addWidget(self.in_text)
		vBox.addLayout(hBox)
		vBox.addLayout(hbox_wifi)
		vBox.addLayout(hbox_lbs)
		vBox.addLayout(hbox_mix)

		run_btn.clicked.connect(self.runButtonClicked)
		clr_btn.clicked.connect(self.clrButtonClicked)

		self.setLayout(vBox)
		self.setWindowTitle('LBS/WiFi位置查询')
		self.show()

	def runButtonClicked(self):
		self.req_wifi_text.setEnabled(True)
		self.out_wifi_text.setEnabled(True)
		self.req_lbs_text.setEnabled(True)
		self.out_lbs_text.setEnabled(True)
		self.req_mix_text.setEnabled(True)
		self.out_mix_text.setEnabled(True)
	
		src = self.src_combo.currentText()

		log = self.in_text.toPlainText()
		if log == '':
			if src == self.src_combo.itemText(0):
				self.in_text.setPlainText('[示例数据]' + EXAMPLE_SRVLOG)
				log = EXAMPLE_SRVLOG
			elif src == self.src_combo.itemText(1):
				self.in_text.setPlainText('[示例数据]' + EXAMPLE_DB)
				log = EXAMPLE_DB
			elif src == self.src_combo.itemText(2):
				self.in_text.setPlainText('[示例数据]' + EXAMPLE_INPUT_WIFI)
				log = EXAMPLE_INPUT_WIFI
			elif src == self.src_combo.itemText(3):
				self.in_text.setPlainText('[示例数据]' + EXAMPLE_INPUT_LBS)
				log = EXAMPLE_INPUT_LBS

		try:
			req, res = tran2GPS_2.transfer(log, src, 'WiFi')
			self.req_wifi_text.setPlainText(''.join(req))
			self.out_wifi_text.setPlainText(''.join(res))
		except Exception as e:
			print(e)
			self.req_wifi_text.setPlainText('错误')
			self.out_wifi_text.setPlainText('错误')

		try:
			req, res = tran2GPS_2.transfer(log, src, 'LBS')
			self.req_lbs_text.setPlainText(''.join(req))
			self.out_lbs_text.setPlainText(''.join(res))
		except Exception as e:
			print(e)
			self.req_lbs_text.setPlainText('错误')
			self.out_lbs_text.setPlainText('错误')

		try:
			req, res = tran2GPS_2.transfer(log, src, 'mix')
			self.req_mix_text.setPlainText(''.join(req))
			self.out_mix_text.setPlainText(''.join(res))
		except Exception as e:
			print(e)
			self.req_mix_text.setPlainText('错误')
			self.out_mix_text.setPlainText('错误')

	def clrButtonClicked(self):
		self.in_text.setPlainText('')

		self.req_wifi_text.setPlainText('WiFi请求')
		self.out_wifi_text.setPlainText('WiFi结果')
		self.req_lbs_text.setPlainText('LBS请求')
		self.out_lbs_text.setPlainText('LBS结果')
		self.req_mix_text.setPlainText('WiFi+LBS请求')
		self.out_mix_text.setPlainText('WiFi+LBS结果')
		self.req_wifi_text.setEnabled(False)
		self.out_wifi_text.setEnabled(False)
		self.req_lbs_text.setEnabled(False)
		self.out_lbs_text.setEnabled(False)
		self.req_mix_text.setEnabled(False)
		self.out_mix_text.setEnabled(False)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Tran2gpsGui()
	sys.exit(app.exec_())
