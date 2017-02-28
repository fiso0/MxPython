#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt


class DataBreaker(QWidget):
	def __init__(self):
		super().__init__()
		self.inputText = QTextEdit()
		self.outputText = QTextEdit()
		self.outputText2 = QTextEdit()
		self.runButton = QPushButton('分解')
		self.init_ui()

	def init_ui(self):
		# self.runButton.resize(self.runButton.sizeHint())
		toolBox = QHBoxLayout()
		toolBox.addStretch()
		toolBox.addWidget(self.runButton)
		toolBox.addStretch()

		layout = QVBoxLayout()
		layout.addWidget(QLabel("OneNet数据："))
		layout.addWidget(self.inputText)
		layout.addLayout(toolBox)
		layout.addWidget(QLabel("分段："))
		layout.addWidget(self.outputText)
		layout.addWidget(QLabel("参数部分："))
		layout.addWidget(self.outputText2)

		self.runButton.clicked.connect(self.run_btn_clicked)

		self.setLayout(layout)
		self.setGeometry(200, 300, 500, 350)
		self.setWindowTitle('OneNet数据分解')
		self.show()

	def run_btn_clicked(self):
		input_str = self.inputText.toPlainText()
		if input_str == '':
			sample_input = '262626260019000000000866888a2a2372298001110215000000022b000696'
			self.inputText.setPlainText("示例："+sample_input)
			input_str = sample_input
		front = input_str[:36]
		cmd = input_str[36:40]
		para = insert_blank(input_str[40:-6])
		end = insert_blank(input_str[-6:])
		self.outputText.setPlainText("%s %s %s %s" % (front, cmd, para, end))
		self.outputText2.setPlainText("%s" % para)


def insert_blank(text):
	# 将字符串每两个以空格分开
	import re
	result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", text)
	return result


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = DataBreaker()
	sys.exit(app.exec_())
