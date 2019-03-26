#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        # 设置布局方式
        hbox = QHBoxLayout()

        # 创建标签
        self.l1 = QLabel("拖动滑动条去改变颜色")
        self.l1.setFont(QFont("Arial", 16))

        # 创建滚动条
        self.s1 = QScrollBar()
        self.s1.setMaximum(255)
        # ScrollBar的常用信号有两种，valueChanged和sliderMoved，两者的区别在于
        # sliderMoved只在拖动滚动条时有效，而valueChanged则不关心你改变值的方式
        self.s1.valueChanged.connect(self.sliderval)
        self.s2 = QScrollBar()
        self.s2.setMaximum(255)
        self.s2.sliderMoved.connect(self.sliderval)
        self.s3 = QScrollBar()
        self.s3.setMaximum(255)
        self.s3.sliderMoved.connect(self.sliderval)

        # 为布局添加控件
        hbox.addWidget(self.l1)
        hbox.addWidget(self.s1)
        hbox.addWidget(self.s2)
        hbox.addWidget(self.s3)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QScrollBar 例子')

        self.setLayout(hbox)

    # 槽函数，将滚动条的值转化为RGB颜色值
    def sliderval(self):

        palette = QPalette()
        c = QColor(self.s1.value(), self.s2.value(), self.s3.value(), 255)
        palette.setColor(QPalette.Foreground, c)
        self.l1.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Example()
    demo.show()
    sys.exit(app.exec_())