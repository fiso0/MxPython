#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GUI(QWidget):
	def __init__(self):
		super().__init__()
		self.ui_init()
		self.show_status()

		self.in_files = [] # 输入文件
		self.out_src = '' # 输出路径
		self.keyword_list = [] # 关键词列表
		self.filt_cond = '' # 过滤条件

	def ui_init(self):
		# 文件设置
		inLabel = QLabel('输入文件：')
		outLabel = QLabel('输出路径：')
		self.fileList = QListWidget()
		self.fileList.setSelectionMode(3)
		self.outSrc = QLineEdit()
		inFileBtn = QPushButton('添加')
		inFileDelBtn = QPushButton('删除')
		inFileResetBtn = QPushButton('清空')
		outSrcBtn = QPushButton('设置')

		# 条件设置
		keywordLabel = QLabel('关键词：')
		self.keyword = QLineEdit()
		self.filtList = QListWidget() # 关键词列表
		condLebel = QLabel('过滤条件：')
		self.filtCond = QLineEdit()

		tool_or = QPushButton('OR')
		tool_and = QPushButton('AND')
		tool_or_not = QPushButton('OR NOT')
		tool_and_not = QPushButton('AND NOT')
		tool_del = QPushButton('重置')

		doBtn = QPushButton('处理')
		self.statusBar = QStatusBar()
		self.statusBar.setEnabled(False)

		# 信号
		inFileBtn.clicked.connect(self.in_file_clicked)
		inFileDelBtn.clicked.connect(self.in_file_del_clicked)
		inFileResetBtn.clicked.connect(self.in_file_reset_clicked)
		outSrcBtn.clicked.connect(self.out_src_clicked)
		tool_or.clicked.connect(self.filt_clicked)
		tool_and.clicked.connect(self.filt_clicked)
		tool_or_not.clicked.connect(self.filt_clicked)
		tool_and_not.clicked.connect(self.filt_clicked)
		doBtn.clicked.connect(self.do_filt)
		tool_del.clicked.connect(self.reset_filt)

		# 布局
		inBox = QHBoxLayout()
		inToolBox = QVBoxLayout()
		outBox = QHBoxLayout()
		toolBox = QHBoxLayout()
		mainBox = QVBoxLayout()

		mainBox.addWidget(inLabel)
		inBox.addWidget(self.fileList)
		inToolBox.addWidget(inFileBtn)
		inToolBox.addWidget(inFileDelBtn)
		inToolBox.addWidget(inFileResetBtn)
		inToolBox.addStretch()
		inBox.addLayout(inToolBox)
		mainBox.addLayout(inBox)
		mainBox.addWidget(outLabel)
		outBox.addWidget(self.outSrc)
		outBox.addWidget(outSrcBtn)
		mainBox.addLayout(outBox)

		toolBox.addWidget(tool_del)
		toolBox.addStretch()
		toolBox.addWidget(tool_or_not)
		toolBox.addWidget(tool_and_not)
		toolBox.addWidget(tool_or)
		toolBox.addWidget(tool_and)

		mainBox.addWidget(keywordLabel)
		mainBox.addWidget(self.keyword)
		mainBox.addLayout(toolBox)
		mainBox.addWidget(self.filtList)
		mainBox.addWidget(condLebel)
		mainBox.addWidget(self.filtCond)
		mainBox.addWidget(doBtn, alignment=Qt.AlignRight)
		mainBox.addWidget(self.statusBar)

		self.setLayout(mainBox)
		self.setFont(QFont('Arial'))
		self.resize(800, 500)
		self.setWindowTitle('文本过滤工具')
		self.show()

	# 打开文件对话框 取一组文件名
	def in_file_clicked(self):
		openFilesPath = "."
		# openFilesPath = "D:\project\MTK6765\gps_solutions\调试"
		files, ok = QFileDialog.getOpenFileNames(self,
		                                         "添加文件",
		                                         openFilesPath,
		                                         "All Files (*);;Text Files (*.txt)")
		for file in files:
			if file not in self.in_files: # 去重
				self.fileList.addItem(QListWidgetItem(file))
				self.in_files.append(file)
		self.show_status()

	def in_file_del_clicked(self):
		items = self.fileList.selectedItems()
		for item in items:
			row = self.fileList.row(item)
			self.fileList.takeItem(row)
			self.in_files.remove(item.text())
		self.show_status()

	def in_file_reset_clicked(self):
		self.fileList.clear()
		self.in_files = []
		self.show_status()

	def out_src_clicked(self):
		directory = QFileDialog.getExistingDirectory(self,
		                                             "设置输出路径",
		                                             self.outSrc.text())
		if directory:
			self.outSrc.setText(directory)
		self.out_src = directory
		self.show_status()

	def filt_clicked(self):
		keyword_cur = self.keyword.text().strip()
		self.keyword_list.append(keyword_cur)
		keyword_cur_idx = len(self.keyword_list)

		# 更新关键词列表
		self.filtList.addItem(QListWidgetItem("%-4d %s"%(keyword_cur_idx, keyword_cur)))

		# 更新过滤条件
		filt_cond_cur = self.filtCond.text().strip()
		if filt_cond_cur == '':
			filt_cond_new = "%s"%(keyword_cur_idx)
		else:
			filt_op = '?'
			if self.sender().text() == 'OR':
				filt_op = '|'
			elif self.sender().text() == 'AND':
				filt_op = '&'
			elif self.sender().text() == 'OR NOT':
				filt_op = '|!'
			elif self.sender().text() == 'AND NOT':
				filt_op = '&!'
			filt_cond_new = "(%s%s%s)"%(filt_cond_cur, filt_op, keyword_cur_idx)
		self.filtCond.setText(filt_cond_new)
		self.filt_cond = filt_cond_new
		self.show_status()

	def get_out_filename(self, file):
		# 输入文件名a.b，输出文件名为a_ed.b
		# 输入文件名a，输出文件名为a_ed
		import re
		if '.' in file:
			res = re.match('(.*)\.(.*)', file)
			out = res.group(1)+'_ed.'+res.group(2)
		else:
			out = file + '_ed'
		return out

	def filt_line(self, line):
		cond_list = [keyword in line for keyword in self.keyword_list]
		num = len(self.keyword_list)
		cond = self.filt_cond
		cond.replace('!', 'not ')
		while num:
			cond = cond.replace(str(num), str(cond_list[num-1]))
			num = num - 1
		return eval(cond) # 计算字符串中的表达式

	def do_filt(self):
		try:
			for file in self.in_files: # 循环处理每一个文件
				out_file = self.get_out_filename(file)
				with open(file, 'r') as f, open(out_file, 'w+') as f_out:
					for line in f.readlines(): # 循环处理每一行
						res = self.filt_line(line)
						if res:
							f_out.write(line)
		except Exception as e:
			self.show_status(e)
		else:
			self.show_status('处理完成')

	def show_status(self, status = ''):
		if status != '':
			self.statusBar.showMessage(status)
			return

		if self.fileList.count() == 0:
			self.statusBar.showMessage('请添加输入文件')
		elif self.outSrc.text().strip() == '':
			self.statusBar.showMessage('请设置输出路径')
		elif self.filtList.count() == 0:
			self.statusBar.showMessage('请添加关键词')
		else:
			self.statusBar.showMessage('点击处理按钮即可输出文件')

	def reset_filt(self):
		self.keyword_list = []  # 关键词列表
		self.filt_cond = ''  # 过滤条件
		self.filtList.clear()
		self.filtCond.clear()
		self.show_status()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = GUI()
	sys.exit(app.exec_())
