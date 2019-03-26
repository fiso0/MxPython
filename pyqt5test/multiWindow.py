#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
import sys


class TrainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.resize(180, 60)
        self.setWindowTitle('训练')

        self.btn_back = QPushButton('返回')

        # 界面布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_back)
        self.setLayout(vbox)

        self.btn_back.clicked.connect(self.back)

    def back(self):
        self.close()


class TestWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.resize(180, 60)
        self.setWindowTitle('测试')

        self.btn_back = QPushButton('返回')

        # 界面布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_back)
        self.setLayout(vbox)

        self.btn_back.clicked.connect(self.back)

    def back(self):
        self.close()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(120, 80)

        self.btn_train = QPushButton('训练')
        self.btn_test = QPushButton('测试')

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_train)
        hbox.addWidget(self.btn_test)

        self.setLayout(hbox)

        self.btn_train.clicked.connect(self.tab_1)
        self.btn_test.clicked.connect(self.tab_2)
        self.show()

    # 打开训练界面
    def tab_1(self):
        self.TrainWindow = TrainWindow()
        self.TrainWindow.show()

    # 打开测试界面
    def tab_2(self):
        self.TestWindow = TestWindow()
        self.TestWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()

