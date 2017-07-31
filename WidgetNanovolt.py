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
        WidgetNanovolt.resize(231, 126)
        self.formLayout = QtWidgets.QFormLayout(WidgetNanovolt)
        self.formLayout.setObjectName("formLayout")
        self._label_1 = QtWidgets.QLabel(WidgetNanovolt)
        self._label_1.setObjectName("_label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._label_1)
        self.combo_port = QtWidgets.QComboBox(WidgetNanovolt)
        self.combo_port.setObjectName("combo_port")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.combo_port)
        self.btn_connect = QtWidgets.QPushButton(WidgetNanovolt)
        self.btn_connect.setObjectName("btn_connect")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_connect)
        self.btn_config = QtWidgets.QPushButton(WidgetNanovolt)
        self.btn_config.setObjectName("btn_config")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.btn_config)
        self.line = QtWidgets.QFrame(WidgetNanovolt)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line)
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
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)

        self.retranslateUi(WidgetNanovolt)
        QtCore.QMetaObject.connectSlotsByName(WidgetNanovolt)

    def retranslateUi(self, WidgetNanovolt):
        _translate = QtCore.QCoreApplication.translate
        WidgetNanovolt.setWindowTitle(_translate("WidgetNanovolt", "Keithley 2182A"))
        self._label_1.setText(_translate("WidgetNanovolt", "Port"))
        self.btn_connect.setText(_translate("WidgetNanovolt", "Connect"))
        self.btn_config.setText(_translate("WidgetNanovolt", "Config"))
        self.lbl_channel.setText(_translate("WidgetNanovolt", "CH?:"))
        self.lbl_value.setText(_translate("WidgetNanovolt", "NA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetNanovolt = QtWidgets.QWidget()
    ui = Ui_WidgetNanovolt()
    ui.setupUi(WidgetNanovolt)
    WidgetNanovolt.show()
    sys.exit(app.exec_())

