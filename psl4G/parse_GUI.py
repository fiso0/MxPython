#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QApplication, QPushButton, QButtonGroup, QRadioButton, \
	QComboBox, QTextEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import parse_lib_o as plo
import time

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
		self.levelCombo.setMinimumWidth(100)
		modLabel = QLabel('log模块')
		self.modCombo = QComboBox()
		self.modCombo.setMinimumWidth(100)
		funLabel = QLabel('功能')
		self.funCombo = QComboBox()
		self.funCombo.setMinimumWidth(100)
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
		# toolBox.addWidget(toolBtn3)
		# toolBox.addWidget(toolBtn4)
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
		file = QFileDialog.getOpenFileName(self, '选择log文件', '')
		filename = file[0]
		self.fileNameEdit.setText(filename)

	def parse_file(self):
		self.please_wait()
		filename = self.fileNameEdit.text()

		start = time.time() # 计时开始

		self.L = plo.Parser(filename)
		for line_no in range(0,self.L.lines): # 遍历所有log
			try:
				self.L.parse_log_level(line_no) # log级别
				self.L.parse_log_mod(line_no) # log模块
				self.L.parse_log_all_func(line_no) # 其他功能
			except Exception as e:
				print(e)
			if line_no%1000 == 0 or line_no == self.L.lines - 1: # 每100行和最后一行执行一次刷新，可大大加快解析速度！
				self.outEdit.setText('解析中，请等待...('+str(line_no)+'/'+str(self.L.lines)+')')
				QApplication.processEvents()

		end = time.time() # 计时结束

		# log级别
		log_levels = self.L.get_levels()
		self.levelCombo.clear()
		self.levelCombo.addItem('全部')
		self.levelCombo.addItems(log_levels.keys())

		# log模块
		log_mods = self.L.get_mods()
		self.modCombo.clear()
		self.modCombo.addItem('全部')
		self.modCombo.addItems(log_mods.keys())

		# log功能
		log_funcs = self.L.get_funcs()
		self.funCombo.clear()
		self.funCombo.addItem('全部')
		self.funCombo.addItems(log_funcs.keys())

		# 输出结果
		print_log = ''
		print_log += '解析时间：%.2fs\n' % (end-start)
		print_log += ('各级别log统计结果：\n')
		for level_name in log_levels.keys():
			print_log += (level_name + ': ' + str(len(log_levels.get(level_name, []))) + '\n')
		print_log += '\n'
		print_log += ('各模块log统计结果：\n')
		for mod_name in log_mods.keys():
			print_log += (mod_name + ': ' + str(len(log_mods.get(mod_name, []))) + '\n')
		print_log += '\n'
		print_log += ('各功能统计结果：\n')
		for func_name in log_funcs.keys():
			print_log += (func_name + ': ' + str(len(log_funcs.get(func_name, []))) + '\n')
		self.parse_result = print_log # 保存解析结果
		self.outEdit.setText(print_log)

	def show_lines(self):
		'''
		筛选框操作后，显示结果
		'''
		selLevel = self.levelCombo.currentText()
		selMod = self.modCombo.currentText()
		selFun = self.funCombo.currentText()

		if(selLevel == '全部' and selMod == '全部' and selFun == '全部'): # 不要显示全部log
			self.outEdit.setText(self.parse_result)
			return

		self.please_wait()

		if (selLevel != '全部'):
			resLevel = self.L.get_log_lines(selLevel)

		if (selMod != '全部'):
			resMod = self.L.get_log_lines(selMod)

		if (selFun != '全部'):
			resFun = self.L.get_log_lines(selFun)

		# 逐行显示
		self.outEdit.clear()
		lines_num = 0
		for i in range(0, self.L.lines):
			if (selLevel != '全部' and i not in resLevel): # 不满足等级筛选条件
				continue
			if (selMod != '全部' and i not in resMod): # 不满足模块筛选条件
				continue
			if (selFun != '全部' and i not in resFun): # 不满足功能筛选条件
				continue
			# i满足所有筛选条件
			self.outEdit.moveCursor(QTextCursor.End) # 使用insertPlainText需保证cursor在末尾
			self.outEdit.insertPlainText(self.L.log[i])
			lines_num = lines_num + 1
			self.show_status('当前' + str(lines_num) + '条')
			QApplication.processEvents()
		self.show_status('共' + str(lines_num) + '条')

	def please_wait(self):
		self.outEdit.setText('解析中，请等待...')
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
		file = QFileDialog.getSaveFileName(self, '保存log文件', '')
		filename = file[0]
		try:
			with open(filename, 'w+') as f:
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
