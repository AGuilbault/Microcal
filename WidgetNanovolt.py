# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetNanovolt.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetNanovolt(object):
    def setupUi(self, WidgetNanovolt):
        WidgetNanovolt.setObjectName("WidgetNanovolt")
        WidgetNanovolt.resize(217, 126)
        self.gridLayout = QtWidgets.QGridLayout(WidgetNanovolt)
        self.gridLayout.setObjectName("gridLayout")
        self._label_1 = QtWidgets.QLabel(WidgetNanovolt)
        self._label_1.setObjectName("_label_1")
        self.gridLayout.addWidget(self._label_1, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_channel = QtWidgets.QLabel(WidgetNanovolt)
        self.lbl_channel.setObjectName("lbl_channel")
        self.horizontalLayout.addWidget(self.lbl_channel)
        self.lbl_value = QtWidgets.QLabel(WidgetNanovolt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_value.sizePolicy().hasHeightForWidth())
        self.lbl_value.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.lbl_value.setPalette(palette)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lbl_value.setFont(font)
        self.lbl_value.setObjectName("lbl_value")
        self.horizontalLayout.addWidget(self.lbl_value)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 6)
        self.connect_status = QtWidgets.QLabel(WidgetNanovolt)
        self.connect_status.setText("")
        self.connect_status.setObjectName("connect_status")
        self.gridLayout.addWidget(self.connect_status, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(WidgetNanovolt)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 6)
        self.btn_config = QtWidgets.QPushButton(WidgetNanovolt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_config.sizePolicy().hasHeightForWidth())
        self.btn_config.setSizePolicy(sizePolicy)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout.addWidget(self.btn_config, 2, 1, 1, 5)
        self.combo_port = QtWidgets.QComboBox(WidgetNanovolt)
        self.combo_port.setObjectName("combo_port")
        self.gridLayout.addWidget(self.combo_port, 0, 1, 1, 5)
        self.btn_connect = QtWidgets.QPushButton(WidgetNanovolt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_connect.sizePolicy().hasHeightForWidth())
        self.btn_connect.setSizePolicy(sizePolicy)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout.addWidget(self.btn_connect, 1, 1, 1, 5)

        self.retranslateUi(WidgetNanovolt)
        QtCore.QMetaObject.connectSlotsByName(WidgetNanovolt)

    def retranslateUi(self, WidgetNanovolt):
        _translate = QtCore.QCoreApplication.translate
        WidgetNanovolt.setWindowTitle(_translate("WidgetNanovolt", "Keithley 2182A"))
        self._label_1.setText(_translate("WidgetNanovolt", "Port"))
        self.lbl_channel.setText(_translate("WidgetNanovolt", "CH?:"))
        self.lbl_value.setText(_translate("WidgetNanovolt", "NA"))
        self.btn_config.setText(_translate("WidgetNanovolt", "Config"))
        self.btn_connect.setText(_translate("WidgetNanovolt", "Connect"))

