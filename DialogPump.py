# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogPump.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogPump(object):
    def setupUi(self, DialogPump):
        DialogPump.setObjectName("DialogPump")
        DialogPump.resize(240, 182)
        self.gridLayout = QtWidgets.QGridLayout(DialogPump)
        self.gridLayout.setObjectName("gridLayout")
        self._label_1 = QtWidgets.QLabel(DialogPump)
        self._label_1.setObjectName("_label_1")
        self.gridLayout.addWidget(self._label_1, 0, 0, 1, 2)
        self.spin_rate = QtWidgets.QDoubleSpinBox(DialogPump)
        self.spin_rate.setDecimals(4)
        self.spin_rate.setMaximum(1999.0)
        self.spin_rate.setObjectName("spin_rate")
        self.gridLayout.addWidget(self.spin_rate, 1, 0, 1, 1)
        self.combo_units = QtWidgets.QComboBox(DialogPump)
        self.combo_units.setObjectName("combo_units")
        self.combo_units.addItem("")
        self.combo_units.addItem("")
        self.combo_units.addItem("")
        self.combo_units.addItem("")
        self.gridLayout.addWidget(self.combo_units, 1, 1, 1, 1)
        self._label_2 = QtWidgets.QLabel(DialogPump)
        self._label_2.setObjectName("_label_2")
        self.gridLayout.addWidget(self._label_2, 2, 0, 1, 2)
        self.spin_diameter = QtWidgets.QDoubleSpinBox(DialogPump)
        self.spin_diameter.setDecimals(4)
        self.spin_diameter.setMaximum(1999.0)
        self.spin_diameter.setObjectName("spin_diameter")
        self.gridLayout.addWidget(self.spin_diameter, 3, 0, 1, 2)
        self._label_3 = QtWidgets.QLabel(DialogPump)
        self._label_3.setObjectName("_label_3")
        self.gridLayout.addWidget(self._label_3, 4, 0, 1, 2)
        self.spin_target = QtWidgets.QDoubleSpinBox(DialogPump)
        self.spin_target.setDecimals(4)
        self.spin_target.setMaximum(100.0)
        self.spin_target.setSingleStep(0.005)
        self.spin_target.setObjectName("spin_target")
        self.gridLayout.addWidget(self.spin_target, 5, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogPump)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(219, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self._label_1.setBuddy(self.spin_rate)
        self._label_2.setBuddy(self.spin_diameter)
        self._label_3.setBuddy(self.spin_target)

        self.retranslateUi(DialogPump)
        self.buttonBox.accepted.connect(DialogPump.accept)
        self.buttonBox.rejected.connect(DialogPump.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPump)

    def retranslateUi(self, DialogPump):
        _translate = QtCore.QCoreApplication.translate
        DialogPump.setWindowTitle(_translate("DialogPump", "Dialog"))
        self._label_1.setText(_translate("DialogPump", "Infuse rate"))
        self.combo_units.setItemText(0, _translate("DialogPump", "ml/min"))
        self.combo_units.setItemText(1, _translate("DialogPump", "µl/min"))
        self.combo_units.setItemText(2, _translate("DialogPump", "ml/hr"))
        self.combo_units.setItemText(3, _translate("DialogPump", "µl/hr"))
        self._label_2.setText(_translate("DialogPump", "Diameter"))
        self.spin_diameter.setSuffix(_translate("DialogPump", " mm"))
        self._label_3.setText(_translate("DialogPump", "Target infusion"))
        self.spin_target.setSuffix(_translate("DialogPump", " ml"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogPump = QtWidgets.QDialog()
    ui = Ui_DialogPump()
    ui.setupUi(DialogPump)
    DialogPump.show()
    sys.exit(app.exec_())

