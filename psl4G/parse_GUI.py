#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QButtonGroup, QRadioButton, QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import parse_lib as pl

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		mainBox = QVBoxLayout()
		fileBox = QHBoxLayout()
		menuBox = QHBoxLayout()
		resBox = QHBoxLayout()
		self.outEdit = QTextEdit()
		toolBox = QVBoxLayout()

		mainBox.addLayout(fileBox)
		mainBox.addLayout(menuBox)
		mainBox.addLayout(resBox)
		resBox.addWidget(self.outEdit)
		resBox.addLayout(toolBox)

		openFileBtn = QPushButton('1.选择文件')
		self.fileNameEdit = QLineEdit()
		parseFileBtn = QPushButton('2.开始解析')
		fileBox.addWidget(openFileBtn)
		fileBox.addWidget(self.fileNameEdit)
		fileBox.addWidget(parseFileBtn)

		label1 = QLabel('3.筛选：')
		levelLabel = QLabel('log级别')
		self.levelCombo = QComboBox()
		modLabel = QLabel('log模块')
		self.modCombo = QComboBox()
		self.modCombo.setMinimumWidth(100)
		funLabel = QLabel('功能')
		self.funCombo = QComboBox()
		menuBox.addWidget(label1)
		menuBox.addWidget(levelLabel)
		menuBox.addWidget(self.levelCombo)
		menuBox.addSpacing(15)
		menuBox.addWidget(modLabel)
		menuBox.addWidget(self.modCombo)
		menuBox.addSpacing(15)
		menuBox.addWidget(funLabel)
		menuBox.addWidget(self.funCombo)
		menuBox.addStretch()

		toolBtn1 = QPushButton('复制')
		toolBtn2 = QPushButton('保存')
		toolBtn3 = QPushButton('')
		toolBtn4 = QPushButton('')
		self.statusLabel = QLabel('')
		toolBox.addWidget(toolBtn1)
		toolBox.addWidget(toolBtn2)
		toolBox.addWidget(toolBtn3)
		toolBox.addWidget(toolBtn4)
		toolBox.addStretch()
		toolBox.addWidget(self.statusLabel)

		self.setLayout(mainBox)

		# 按钮连接到槽
		openFileBtn.clicked.connect(self.open_file)
		parseFileBtn.clicked.connect(self.parse_file)
		self.levelCombo.activated.connect(self.show_lines)
		self.modCombo.activated.connect(self.show_lines)
		self.funCombo.activated.connect(self.show_lines)

		toolBtn1.clicked.connect(self.copy_result)
		toolBtn2.clicked.connect(self.save_result)

		self.setGeometry(200, 300, 700, 500)
		self.setWindowTitle('log解析工具')
		self.show()

	def open_file(self):
		file = QFileDialog.getOpenFileName(self,'选择log文件','')
		filename = file[0]
		self.fileNameEdit.setText(filename)

	def parse_file(self):
		self.please_wait()
		filename = self.fileNameEdit.text()

		printLog = pl.BASIC(filename, False)
		self.outEdit.setText(printLog)

		# log级别
		log_levels = pl.get_log_levels().keys()
		self.levelCombo.clear()
		self.levelCombo.addItem('全部')
		self.levelCombo.addItems(log_levels)

		# log模块
		log_mods = pl.get_log_mods().keys()
		self.modCombo.clear()
		self.modCombo.addItem('全部')
		self.modCombo.addItems(log_mods)

		# log功能
		log_funcs = pl.get_log_funcs().keys()
		self.funCombo.clear()
		self.funCombo.addItem('全部')
		self.funCombo.addItems(log_funcs)

	def show_lines(self):
		self.please_wait()

		selLevel = self.levelCombo.currentText()
		selMod = self.modCombo.currentText()
		selFun = self.funCombo.currentText()
		
		if(selLevel != '全部'):
			resLevel = pl.get_log_lines(selLevel)
		else:
			resLevel = pl.get_all_lines()
			
		if(selMod != '全部'):
			resMod = pl.get_log_lines(selMod)
		else:
			resMod = pl.get_all_lines()

		if(selFun != '全部'):
			resFun = pl.get_log_lines(selFun)
		else:
			resFun = pl.get_all_lines()

		resLines = set(resLevel).intersection(set(resMod)).intersection(set(resFun))
		resLinesList1 = list(resLines)
		resLinesList = sorted(resLinesList1)
		logs = pl.get_log(resLinesList)
		self.outEdit.setText(''.join(logs)) # show logs in outEdit

		lines_num = len(resLinesList)
		self.show_status('共'+str(lines_num)+'条')

	def please_wait(self):
		self.outEdit.setText('处理中，请等待...')
		QApplication.processEvents()
		self.show_status('')

	def show_status(self, status):
		self.statusLabel.setText(status)
		QApplication.processEvents()

	def copy_result(self):
		clipboard = QApplication.clipboard()
		clipboard.setText(self.outEdit.toPlainText())
		self.show_status('复制成功')

	def save_result(self):
		file = QFileDialog.getSaveFileName(self,'保存log文件','')
		filename = file[0]
		try:
			with open(filename,'w+') as f:
				result = self.outEdit.toPlainText()
				f.write(result)
			self.show_status('保存成功')
		except Exception as e:
			print(e)
			self.show_status('保存失败')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())