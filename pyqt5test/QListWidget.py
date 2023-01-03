#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""
考虑以下三种signal：
currentItemChanged
itemSelectionChanged
itemClicked

初始显示时，触发：
currentItemChanged

鼠标点击时，触发：
currentItemChanged
itemSelectionChanged
itemClicked

按键盘上下时，触发：
itemSelectionChanged
currentItemChanged

执行clearSelection()时，触发：
itemSelectionChanged
"""

class GUI(QWidget):
	def __init__(self):
		super().__init__()
		self.ui_init()

	def ui_init(self):
		self.listW = QListWidget()
		self.listW.addItems([str(i) for i in range(0,10)])  # 填入数据0~9
		self.listW.setSelectionMode(3)  # 支持使用shift/ctrl多选
		# self.listW.clearSelection()  # 无效
		# self.listW.setFocusPolicy(Qt.NoFocus)  # 去掉选中项的虚线框，会导致不接受键盘事件

		# 改用按键实现上下显示，不使用这几个signal
		# self.listW.currentItemChanged.connect(self.listWcurrentItemChanged)
		# self.listW.itemSelectionChanged.connect(self.listWitemSelectionChanged)
		# self.listW.itemClicked.connect(self.listWitemClicked)

		btn_up = QPushButton('up')
		btn_down = QPushButton('down')
		btn_up.clicked.connect(self.up_clicked)
		btn_down.clicked.connect(self.down_clicked)

		btn1 = QPushButton('test 1')
		btn2 = QPushButton('test 2')
		btn1.clicked.connect(self.btn1_clicked)
		btn2.clicked.connect(self.btn2_clicked)

		# 布局
		mainBox = QVBoxLayout()
		mainBox.addWidget(self.listW)
		mainBox.addWidget(btn_up)
		mainBox.addWidget(btn_down)
		mainBox.addWidget(btn1)
		mainBox.addWidget(btn2)
		self.setLayout(mainBox)

		self.resize(200, 300)
		self.setWindowTitle('QListWidget')
		self.show()

	def up_clicked(self):
		idx = self.listW.currentIndex().row()
		new_idx = idx - 1
		if new_idx < 0:
			new_idx = 0
		self.listW.setCurrentRow(new_idx)

	def down_clicked(self):
		idx = self.listW.currentIndex().row()
		new_idx = idx + 1
		if new_idx > self.listW.count():
			new_idx = self.listW.count()
		self.listW.setCurrentRow(new_idx)

	def btn1_clicked(self):
		a = self.listW.selectedIndexes()
		print('selectedIndexes len=%d' % len(a))
		print('selectedIndexes row=%s' % ', '.join([str(u.row()) for u in a]))
		b = self.listW.selectedItems()
		print('selectedItems len=%d' % len(b))
		print('selectedItems text=%s' % ', '.join([str(u.text()) for u in b]))
		print('')
		pass

	def btn2_clicked(self):
		self.listW.clearSelection()
		pass

	def listWcurrentItemChanged(self):
		print('listW.currentItemChanged')
		pass

	def listWitemSelectionChanged(self):
		print('listW.itemSelectionChanged')
		pass

	def listWitemClicked(self):
		print('listW.itemClicked')
		pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = GUI()
	sys.exit(app.exec_())
