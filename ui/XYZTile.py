# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XYZTile.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_XYZ_Dialog(object):
    def setupUi(self, XYZ_Dialog):
        XYZ_Dialog.setObjectName("XYZ_Dialog")
        XYZ_Dialog.resize(236, 295)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(XYZ_Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 12, 10, -1)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setHorizontalSpacing(15)
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(XYZ_Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.URI = QtWidgets.QLineEdit(XYZ_Dialog)
        self.URI.setObjectName("URI")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.URI)
        self.label_3 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lyrs = QtWidgets.QLineEdit(XYZ_Dialog)
        self.lyrs.setObjectName("lyrs")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lyrs)
        self.label_4 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.Xvalue = QtWidgets.QLineEdit(XYZ_Dialog)
        self.Xvalue.setObjectName("Xvalue")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Xvalue)
        self.label_5 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.Yvalue = QtWidgets.QLineEdit(XYZ_Dialog)
        self.Yvalue.setObjectName("Yvalue")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Yvalue)
        self.label_6 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.Zvalue = QtWidgets.QLineEdit(XYZ_Dialog)
        self.Zvalue.setObjectName("Zvalue")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Zvalue)
        self.label_8 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.zmin = QtWidgets.QLineEdit(XYZ_Dialog)
        self.zmin.setObjectName("zmin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.zmin)
        self.label_9 = QtWidgets.QLabel(XYZ_Dialog)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.zmax = QtWidgets.QLineEdit(XYZ_Dialog)
        self.zmax.setObjectName("zmax")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.zmax)
        self.verticalLayout.addLayout(self.formLayout)
        self.addXYZTileLayer = QtWidgets.QPushButton(XYZ_Dialog)
        self.addXYZTileLayer.setObjectName("addXYZTileLayer")
        self.verticalLayout.addWidget(self.addXYZTileLayer, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(XYZ_Dialog)
        QtCore.QMetaObject.connectSlotsByName(XYZ_Dialog)

    def retranslateUi(self, XYZ_Dialog):
        _translate = QtCore.QCoreApplication.translate
        XYZ_Dialog.setWindowTitle(_translate("XYZ_Dialog", "WMS参数"))
        self.label.setText(_translate("XYZ_Dialog", "URI:"))
        self.URI.setText(_translate("XYZ_Dialog", "www.google.cn/maps/vt/"))
        self.label_3.setText(_translate("XYZ_Dialog", "lyrs:"))
        self.lyrs.setText(_translate("XYZ_Dialog", "s"))
        self.label_4.setText(_translate("XYZ_Dialog", "x:"))
        self.Xvalue.setText(_translate("XYZ_Dialog", "{x}"))
        self.label_5.setText(_translate("XYZ_Dialog", "y:"))
        self.Yvalue.setText(_translate("XYZ_Dialog", "{y}"))
        self.label_6.setText(_translate("XYZ_Dialog", "z:"))
        self.Zvalue.setText(_translate("XYZ_Dialog", "{z}"))
        self.label_8.setText(_translate("XYZ_Dialog", "zmin:"))
        self.zmin.setText(_translate("XYZ_Dialog", "0"))
        self.label_9.setText(_translate("XYZ_Dialog", "zmax:"))
        self.zmax.setText(_translate("XYZ_Dialog", "12"))
        self.addXYZTileLayer.setText(_translate("XYZ_Dialog", "添加图层"))
