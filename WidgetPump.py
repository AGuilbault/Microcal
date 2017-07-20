# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetPump.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPump(object):
    def setupUi(self, WidgetPump):
        WidgetPump.setObjectName("WidgetPump")
        WidgetPump.resize(207, 222)
        self.gridLayout = QtWidgets.QGridLayout(WidgetPump)
        self.gridLayout.setObjectName("gridLayout")
        self.combo_baud = QtWidgets.QComboBox(WidgetPump)
        self.combo_baud.setObjectName("combo_baud")
        self.combo_baud.addItem("")
        self.combo_baud.addItem("")
        self.combo_baud.addItem("")
        self.combo_baud.addItem("")
        self.gridLayout.addWidget(self.combo_baud, 1, 1, 1, 1)
        self._label_2 = QtWidgets.QLabel(WidgetPump)
        self._label_2.setObjectName("_label_2")
        self.gridLayout.addWidget(self._label_2, 1, 0, 1, 1)
        self._label_1 = QtWidgets.QLabel(WidgetPump)
        self._label_1.setObjectName("_label_1")
        self.gridLayout.addWidget(self._label_1, 0, 0, 1, 1)
        self.btn_conn = QtWidgets.QPushButton(WidgetPump)
        self.btn_conn.setObjectName("btn_conn")
        self.gridLayout.addWidget(self.btn_conn, 2, 1, 1, 1)
        self.ico_state = QtWidgets.QLabel(WidgetPump)
        self.ico_state.setMinimumSize(QtCore.QSize(44, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ico_state.setFont(font)
        self.ico_state.setObjectName("ico_state")
        self.gridLayout.addWidget(self.ico_state, 6, 0, 1, 1)
        self.line = QtWidgets.QFrame(WidgetPump)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)
        self.btn_infuse = QtWidgets.QPushButton(WidgetPump)
        self.btn_infuse.setObjectName("btn_infuse")
        self.gridLayout.addWidget(self.btn_infuse, 7, 0, 1, 2)
        self.combo_port = QtWidgets.QComboBox(WidgetPump)
        self.combo_port.setObjectName("combo_port")
        self.gridLayout.addWidget(self.combo_port, 0, 1, 1, 1)
        self.lbl_state = QtWidgets.QLabel(WidgetPump)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_state.sizePolicy().hasHeightForWidth())
        self.lbl_state.setSizePolicy(sizePolicy)
        self.lbl_state.setScaledContents(False)
        self.lbl_state.setObjectName("lbl_state")
        self.gridLayout.addWidget(self.lbl_state, 6, 1, 1, 1)
        self.btn_config = QtWidgets.QPushButton(WidgetPump)
        self.btn_config.setObjectName("btn_config")
        self.gridLayout.addWidget(self.btn_config, 3, 1, 1, 1)
        self._label_3 = QtWidgets.QLabel(WidgetPump)
        self._label_3.setObjectName("_label_3")
        self.gridLayout.addWidget(self._label_3, 5, 0, 1, 1)
        self.lbl_target = QtWidgets.QLabel(WidgetPump)
        self.lbl_target.setObjectName("lbl_target")
        self.gridLayout.addWidget(self.lbl_target, 5, 1, 1, 1)
        self._label_2.setBuddy(self.combo_baud)
        self._label_1.setBuddy(self.combo_port)

        self.retranslateUi(WidgetPump)
        self.combo_baud.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(WidgetPump)
        WidgetPump.setTabOrder(self.combo_port, self.combo_baud)
        WidgetPump.setTabOrder(self.combo_baud, self.btn_conn)
        WidgetPump.setTabOrder(self.btn_conn, self.btn_config)
        WidgetPump.setTabOrder(self.btn_config, self.btn_infuse)

    def retranslateUi(self, WidgetPump):
        _translate = QtCore.QCoreApplication.translate
        WidgetPump.setWindowTitle(_translate("WidgetPump", "PHD2000"))
        self.combo_baud.setItemText(0, _translate("WidgetPump", "1200"))
        self.combo_baud.setItemText(1, _translate("WidgetPump", "2400"))
        self.combo_baud.setItemText(2, _translate("WidgetPump", "9600"))
        self.combo_baud.setItemText(3, _translate("WidgetPump", "19200"))
        self._label_2.setText(_translate("WidgetPump", "Baudrate"))
        self._label_1.setText(_translate("WidgetPump", "Port"))
        self.btn_conn.setText(_translate("WidgetPump", "Connect"))
        self.ico_state.setText(_translate("WidgetPump", "⏹"))
        self.btn_infuse.setText(_translate("WidgetPump", "Infuse"))
        self.lbl_state.setText(_translate("WidgetPump", "Disconnected"))
        self.btn_config.setText(_translate("WidgetPump", "Config"))
        self._label_3.setText(_translate("WidgetPump", "Target:"))
        self.lbl_target.setText(_translate("WidgetPump", "NA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetPump = QtWidgets.QWidget()
    ui = Ui_WidgetPump()
    ui.setupUi(WidgetPump)
    WidgetPump.show()
    sys.exit(app.exec_())

