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
		outEdit = QTextEdit()
		toolBox = QVBoxLayout()

		mainBox.addLayout(fileBox)
		mainBox.addLayout(menuBox)
		mainBox.addLayout(resBox)
		resBox.addWidget(outEdit)
		resBox.addLayout(toolBox)

		openFileBtn = QPushButton('选择文件')
		self.fileNameEdit = QLineEdit()
		parseFileBtn = QPushButton('开始解析')
		fileBox.addWidget(openFileBtn)
		fileBox.addWidget(self.fileNameEdit)
		fileBox.addWidget(parseFileBtn)

		levelLabel = QLabel('log级别')
		self.levelCombo = QComboBox()
		modLabel = QLabel('log模块')
		self.modCombo = QComboBox()
		self.modCombo.setMinimumWidth(100)
		menuBox.addWidget(levelLabel)
		menuBox.addWidget(self.levelCombo)
		menuBox.addSpacing(15)
		menuBox.addWidget(modLabel)
		menuBox.addWidget(self.modCombo)
		menuBox.addStretch()

		toolBtn1 = QPushButton('')
		toolBtn2 = QPushButton('')
		toolBtn3 = QPushButton('')
		toolBtn4 = QPushButton('')
		toolBox.addWidget(toolBtn1)
		toolBox.addWidget(toolBtn2)
		toolBox.addWidget(toolBtn3)
		toolBox.addWidget(toolBtn4)
		toolBox.addStretch()

		self.setLayout(mainBox)

		# 按钮连接到槽
		openFileBtn.clicked.connect(self.openFile)
		parseFileBtn.clicked.connect(self.parseFile)
		self.levelCombo.activated.connect(self.showLines)
		self.modCombo.activated.connect(self.showLines)

		self.setGeometry(200, 300, 600, 350)
		self.setWindowTitle('log解析工具')
		self.show()

	def openFile(self):
		file = QFileDialog.getOpenFileName(self,'选择log文件','')
		filename = file[0]
		self.fileNameEdit.setText(filename)

	def parseFile(self):
		filename = self.fileNameEdit.text()

		# log级别
		log_levels = [a.name for a in pl.get_log_levels()]
		self.levelCombo.addItem('全部')
		self.levelCombo.addItems(log_levels)

		pl.BASIC(filename, False)

		# log模块
		log_mods = pl.get_log_mods()
		self.modCombo.addItem('全部')
		self.modCombo.addItems(log_mods)


	def showLines(self):
		selLevel = self.levelCombo.currentText()
		selMod = self.modCombo.currentText()
		
		if(selLevel != '全部'):
			resLevel = pl.get_log_lines(selLevel)
		else:
			resLevel = pl.get_all_lines()
			
		if(selMod != '全部'):
			resMod = pl.get_log_lines(selMod)
		else:
			resMod = pl.get_all_lines()

		resLines = set(resLevel).intersection(set(resMod))

		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())