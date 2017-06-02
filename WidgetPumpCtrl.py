# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetPumpCtrl.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPumpCtrl(object):
    def setupUi(self, WidgetPumpCtrl):
        WidgetPumpCtrl.setObjectName("WidgetPumpCtrl")
        WidgetPumpCtrl.resize(150, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WidgetPumpCtrl.sizePolicy().hasHeightForWidth())
        WidgetPumpCtrl.setSizePolicy(sizePolicy)
        WidgetPumpCtrl.setMinimumSize(QtCore.QSize(150, 0))
        WidgetPumpCtrl.setMaximumSize(QtCore.QSize(16777215, 80))
        self.gridLayout = QtWidgets.QGridLayout(WidgetPumpCtrl)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_infuse = QtWidgets.QPushButton(WidgetPumpCtrl)
        self.btn_infuse.setObjectName("btn_infuse")
        self.gridLayout.addWidget(self.btn_infuse, 1, 0, 1, 2)
        self.ico_state = QtWidgets.QLabel(WidgetPumpCtrl)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ico_state.sizePolicy().hasHeightForWidth())
        self.ico_state.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ico_state.setFont(font)
        self.ico_state.setText("")
        self.ico_state.setObjectName("ico_state")
        self.gridLayout.addWidget(self.ico_state, 0, 0, 1, 1)
        self.lbl_state = QtWidgets.QLabel(WidgetPumpCtrl)
        self.lbl_state.setScaledContents(False)
        self.lbl_state.setObjectName("lbl_state")
        self.gridLayout.addWidget(self.lbl_state, 0, 1, 1, 1)

        self.retranslateUi(WidgetPumpCtrl)
        QtCore.QMetaObject.connectSlotsByName(WidgetPumpCtrl)

    def retranslateUi(self, WidgetPumpCtrl):
        _translate = QtCore.QCoreApplication.translate
        WidgetPumpCtrl.setWindowTitle(_translate("WidgetPumpCtrl", "Form"))
        self.btn_infuse.setText(_translate("WidgetPumpCtrl", "Infuse"))
        self.lbl_state.setText(_translate("WidgetPumpCtrl", "Disconnected"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetPumpCtrl = QtWidgets.QWidget()
    ui = Ui_WidgetPumpCtrl()
    ui.setupUi(WidgetPumpCtrl)
    WidgetPumpCtrl.show()
    sys.exit(app.exec_())

