#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import PyQt5.QtWidgets
import PayCalc

class DataBreaker(PyQt5.QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.income = PyQt5.QtWidgets.QLineEdit()
		self.tax = PyQt5.QtWidgets.QLineEdit()
		self.outcome = PyQt5.QtWidgets.QLineEdit()
		self.base = PyQt5.QtWidgets.QLineEdit()
		self.init_ui()

	def init_ui(self):
		layout = PyQt5.QtWidgets.QHBoxLayout()
		layout.addWidget(PyQt5.QtWidgets.QLabel("应发工资 I："))
		layout.addWidget(self.income)
		layout.addWidget(PyQt5.QtWidgets.QLabel("税额 T："))
		layout.addWidget(self.tax)
		layout.addWidget(PyQt5.QtWidgets.QLabel("实发薪资 P："))
		layout.addWidget(self.outcome)
		layout.addWidget(PyQt5.QtWidgets.QLabel("（纳税基数=T+P）"))
		layout.addWidget(self.base)

		self.income.textChanged.connect(self.calcP)
		self.outcome.textChanged.connect(self.calcI)
		self.base.setEnabled(False)

		self.setLayout(layout)
		self.setWindowTitle('计算器')
		self.show()

	def calcP(self):
		try:
			I = float(self.income.text())
			P = PayCalc.calc_payment(I)
			T = PayCalc.calc_tax(I)
			B = P+T
			if(self.outcome.hasFocus() == False):
				self.outcome.setText('{:.2f}'.format(P))
			if(self.tax.hasFocus() == False):
				self.tax.setText('{:.2f}'.format(T))
			self.base.setText('{:.2f}'.format(B))
		except Exception as e:
			print(e)

	def calcI(self):
		P = float(self.outcome.text())
		I = '{:.2f}'.format(PayCalc.calc_income(P))
		# T = str(PayCalc.calc_tax(I))
		if(self.income.hasFocus() == False):
			self.income.setText(I)
		# self.base.setText(P+T)
		# if(self.tax.hasFocus() == False):
		# 	self.tax.setText(T)

	# def calcT(self):
	# 	I = float(self.income.text())
	# 	T = str(PayCalc.calc_tax(I))
	# 	P = str(PayCalc.calc_payment(I))
	# 	if(self.income.hasFocus() == False):
	# 		self.income.setText(I)
	# 	if(self.outcome.hasFocus() == False):
	# 		self.outcome.setText(P)

if __name__ == '__main__':
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	ex = DataBreaker()
	sys.exit(app.exec_())
