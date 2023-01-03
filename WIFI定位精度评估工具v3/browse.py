#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Analysis.Haoservice_Analysis import *
from Analysis.Mapbar_Analysis import *
from Analysis.Heclouds_Analysis import *
from webkit.previewer import *
from PyQt5 import QtGui
import sys

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

