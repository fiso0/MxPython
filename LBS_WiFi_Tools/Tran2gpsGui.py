#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import tran2GPS
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, \
	QTextEdit, QComboBox


EXAMPLE_INPUT = '''mx_srv_send_handle[337][4005]:&&&& 331 000000000866888a2a237294 <4005> <00-00-00 000000 0.000000 0.000000 0 0 0 0xff 0x00 46 E N 0x00 460:00:28730:20736 0x00 -63 17-01-24 09:52:09 0x00 0x00 50:bd:5f:15:b9:dd,-53,ap1|02:bd:5f:15:b9:dd,-53,ap2|00:27:1d:1a:59:2e,-58,ap3|12:27:1d:1a:59:2e,-58,ap4|02:27:1d:1a:59:2e,-58,ap5;20170124095209 460,00,28730,45271,-90|460,00,28730,45273,-95|460,00,28730,55271,-96|460,00,28730,63401,-98|460,00,28730,46075,-104> 00 05 0x9b'''

class Tran2gpsGui(QWidget):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		src_label = QLabel('数据来源')
		self.src_combo = QComboBox()
		self.src_combo.addItems(['服务器log', '数据库','纯数据（以|间隔）'])

		type_label = QLabel('数据类型')
		self.type_combo = QComboBox()
		self.type_combo.addItems(['WiFi', 'LBS'])  # TODO: 基站类型待实现

		api_label = QLabel('API')
		self.api_combo = QComboBox()
		self.api_combo.addItems(['高德'])  # 目前仅一个选项

		run_btn = QPushButton('开始转换')
		clr_btn = QPushButton('清空')

		hBox = QHBoxLayout()
		hBox.addWidget(src_label)
		hBox.addWidget(self.src_combo)
		hBox.addStretch()
		hBox.addWidget(type_label)
		hBox.addWidget(self.type_combo)
		hBox.addStretch()
		hBox.addWidget(api_label)
		hBox.addWidget(self.api_combo)
		hBox.addStretch()
		hBox.addWidget(run_btn)
		hBox.addWidget(clr_btn)

		self.in_text = QTextEdit()
		self.in_text.setAcceptRichText(False)
		self.req_text = QTextEdit()
		self.req_text.setAcceptRichText(False)
		self.req_text.setReadOnly(True)
		self.out_text = QTextEdit()
		self.out_text.setAcceptRichText(False)
		self.out_text.setReadOnly(True)

		vBox = QVBoxLayout()
		vBox.addWidget(self.in_text)
		vBox.addLayout(hBox)
		vBox.addWidget(self.req_text)
		vBox.addWidget(self.out_text)

		run_btn.clicked.connect(self.runButtonClicked)
		clr_btn.clicked.connect(self.clrButtonClicked)

		self.setLayout(vBox)
		self.show()

	def runButtonClicked(self):
		self.req_text.setPlainText('转换中')
		self.out_text.setPlainText('转换中')

		log = self.in_text.toPlainText()
		if log == '':
			self.in_text.setPlainText('[示例数据]'+EXAMPLE_INPUT)
			log = EXAMPLE_INPUT

		src = self.src_combo.currentText()
		type = self.type_combo.currentText()

		try:
			req, res = tran2GPS.transfer(log, src, type)
			self.req_text.setPlainText(''.join(req))
			self.out_text.setPlainText(''.join(res))
		except:
			self.req_text.setPlainText('错误')
			self.out_text.setPlainText('错误')

	def clrButtonClicked(self):
		self.in_text.setPlainText('')
		self.req_text.setPlainText('')
		self.out_text.setPlainText('')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = Tran2gpsGui()
	sys.exit(app.exec_())
