# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetCourant.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetCourant(object):
    def setupUi(self, WidgetCourant):
        WidgetCourant.setObjectName("WidgetCourant")
        WidgetCourant.setEnabled(True)
        WidgetCourant.resize(390, 158)
        self.gridLayout = QtWidgets.QGridLayout(WidgetCourant)
        self.gridLayout.setObjectName("gridLayout")
        self.label_port = QtWidgets.QLabel(WidgetCourant)
        self.label_port.setObjectName("label_port")
        self.gridLayout.addWidget(self.label_port, 0, 0, 1, 1)
        self.line_config = QtWidgets.QLineEdit(WidgetCourant)
        self.line_config.setObjectName("line_config")
        self.gridLayout.addWidget(self.line_config, 3, 1, 1, 1)
        self.btn_config = QtWidgets.QPushButton(WidgetCourant)
        self.btn_config.setEnabled(True)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout.addWidget(self.btn_config, 5, 1, 1, 2)
        self.btn_browse = QtWidgets.QPushButton(WidgetCourant)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_browse.sizePolicy().hasHeightForWidth())
        self.btn_browse.setSizePolicy(sizePolicy)
        self.btn_browse.setObjectName("btn_browse")
        self.gridLayout.addWidget(self.btn_browse, 3, 2, 1, 1)
        self.btn_connect = QtWidgets.QPushButton(WidgetCourant)
        self.btn_connect.setEnabled(True)
        self.btn_connect.setCheckable(False)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout.addWidget(self.btn_connect, 1, 1, 1, 2)
        self.label_config = QtWidgets.QLabel(WidgetCourant)
        self.label_config.setObjectName("label_config")
        self.gridLayout.addWidget(self.label_config, 3, 0, 1, 1)
        self.combo_port = QtWidgets.QComboBox(WidgetCourant)
        self.combo_port.setObjectName("combo_port")
        self.gridLayout.addWidget(self.combo_port, 0, 1, 1, 2)
        self.line = QtWidgets.QFrame(WidgetCourant)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 1, 1, 2)
        self.connect_status = QtWidgets.QLabel(WidgetCourant)
        self.connect_status.setText("")
        self.connect_status.setObjectName("connect_status")
        self.gridLayout.addWidget(self.connect_status, 1, 0, 1, 1)

        self.retranslateUi(WidgetCourant)
        QtCore.QMetaObject.connectSlotsByName(WidgetCourant)

    def retranslateUi(self, WidgetCourant):
        _translate = QtCore.QCoreApplication.translate
        WidgetCourant.setWindowTitle(_translate("WidgetCourant", "Keithley 220"))
        self.label_port.setText(_translate("WidgetCourant", "Port"))
        self.line_config.setText(_translate("WidgetCourant", "C:\\Users\\guia2812\\Desktop\\PRAC_Step.txt"))
        self.btn_config.setText(_translate("WidgetCourant", "Configure"))
        self.btn_browse.setText(_translate("WidgetCourant", "Browse"))
        self.btn_connect.setText(_translate("WidgetCourant", "Connect"))
        self.label_config.setText(_translate("WidgetCourant", "Config"))

