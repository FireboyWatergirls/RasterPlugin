# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resultView2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(356, 327)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.mapWidget = QtWidgets.QWidget(self.centralwidget)
        self.mapWidget.setObjectName("mapWidget")
        self.gridLayout.addWidget(self.mapWidget, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.actionzoom_in = QtWidgets.QPushButton(self.centralwidget)
        self.actionzoom_in.setText("")
        r = QFileInfo(__file__).absolutePath()
        root = r.replace('/ui', '')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root+"/icon/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_in.setIcon(icon)
        self.actionzoom_in.setObjectName("actionzoom_in")
        self.verticalLayout.addWidget(self.actionzoom_in)
        self.actionzoom_out = QtWidgets.QPushButton(self.centralwidget)
        self.actionzoom_out.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(root+"/icon/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_out.setIcon(icon1)
        self.actionzoom_out.setObjectName("actionzoom_out")
        self.verticalLayout.addWidget(self.actionzoom_out)
        self.actionpan = QtWidgets.QPushButton(self.centralwidget)
        self.actionpan.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(root+"/icon/pan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionpan.setIcon(icon2)
        self.actionpan.setObjectName("actionpan")
        self.verticalLayout.addWidget(self.actionpan)
        self.actionfull_extent = QtWidgets.QPushButton(self.centralwidget)
        self.actionfull_extent.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(root+"/icon/full_extend.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionfull_extent.setIcon(icon3)
        self.actionfull_extent.setObjectName("actionfull_extent")
        self.verticalLayout.addWidget(self.actionfull_extent)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 356, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "处理结果"))
