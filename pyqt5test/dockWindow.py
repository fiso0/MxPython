#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)
        layout = QHBoxLayout()

        # 菜单栏，对于本例中核心内容的展示无影响，可删去
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")

        # 创建可停靠的窗口
        self.dock = QDockWidget("Dockable", self)
        # self.dock.setFeatures(QDockWidget.DockWidgetFloatable)  # 改为只允许float，不允许关闭、移动
        # 特性可选DockWidgetClosable|DockWidgetMovable|DockWidgetFloatable

        # 在停靠窗口内添加QListWidget对象
        self.listWidget = QListWidget()
        self.listWidget.addItem("item1")
        self.listWidget.addItem("item2")
        self.listWidget.addItem("item3")
        self.dock.setWidget(self.listWidget)

        # 是否将可停靠窗口置于浮动状态，默认是False，下面这句删掉不影响显示结果
        self.dock.setFloating(False)

        # 中央控件
        self.setCentralWidget(QTextEdit())

        # 将停靠窗口放在中央控件的右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        self.setLayout(layout)
        self.setWindowTitle("Dock 例子")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    sys.exit(app.exec_())
