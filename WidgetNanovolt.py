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
        WidgetNanovolt.resize(349, 115)
        self.gridLayout = QtWidgets.QGridLayout(WidgetNanovolt)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_connect = QtWidgets.QPushButton(WidgetNanovolt)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout.addWidget(self.btn_connect, 1, 1, 1, 1)
        self._label_1 = QtWidgets.QLabel(WidgetNanovolt)
        self._label_1.setObjectName("_label_1")
        self.gridLayout.addWidget(self._label_1, 0, 0, 1, 1)
        self.lbl_channel = QtWidgets.QLabel(WidgetNanovolt)
        self.lbl_channel.setMinimumSize(QtCore.QSize(30, 0))
        self.lbl_channel.setObjectName("lbl_channel")
        self.gridLayout.addWidget(self.lbl_channel, 3, 0, 1, 1)
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
        self.gridLayout.addWidget(self.lbl_value, 3, 1, 1, 1)
        self.combo_port = QtWidgets.QComboBox(WidgetNanovolt)
        self.combo_port.setObjectName("combo_port")
        self.gridLayout.addWidget(self.combo_port, 0, 1, 1, 1)
        self.btn_config = QtWidgets.QPushButton(WidgetNanovolt)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout.addWidget(self.btn_config, 2, 1, 1, 1)

        self.retranslateUi(WidgetNanovolt)
        QtCore.QMetaObject.connectSlotsByName(WidgetNanovolt)

    def retranslateUi(self, WidgetNanovolt):
        _translate = QtCore.QCoreApplication.translate
        WidgetNanovolt.setWindowTitle(_translate("WidgetNanovolt", "Keithley 2182A"))
        self.btn_connect.setText(_translate("WidgetNanovolt", "Connect"))
        self._label_1.setText(_translate("WidgetNanovolt", "Port"))
        self.lbl_channel.setText(_translate("WidgetNanovolt", "CH?:"))
        self.lbl_value.setText(_translate("WidgetNanovolt", "NA"))
        self.btn_config.setText(_translate("WidgetNanovolt", "Config"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetNanovolt = QtWidgets.QWidget()
    ui = Ui_WidgetNanovolt()
    ui.setupUi(WidgetNanovolt)
    WidgetNanovolt.show()
    sys.exit(app.exec_())

