#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class SimpleModel(QWidget):
	def __init__(self):
		super().__init__()
		self.inputText = QTextEdit()
		self.outputText = QTextEdit()
		self.runButton = QPushButton('确认')
		self.init_ui()

	def init_ui(self):
		toolBox = QHBoxLayout()
		toolBox.addStretch()
		toolBox.addWidget(self.runButton)
		toolBox.addStretch()

		layout = QVBoxLayout()
		layout.addWidget(self.inputText)
		layout.addLayout(toolBox)
		layout.addWidget(self.outputText)

		self.runButton.clicked.connect(self.run_btn_clicked)

		self.setLayout(layout)
		self.setGeometry(200, 300, 600, 350)
		self.setWindowTitle('示例模板')
		self.show()

	def run_btn_clicked(self):
		input_str = self.inputText.toPlainText()
		print('输入为%s,这里实现按键功能' % input_str)
		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SimpleModel()
	sys.exit(app.exec_())
