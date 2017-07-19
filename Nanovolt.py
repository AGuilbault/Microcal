from WidgetNanoVolt import Ui_WidgetNanoVolt

from PyQt5 import QtCore, QtWidgets, QtGui
import visa
import numpy as np


class WidgetNanoVolt(QtWidgets.QWidget, Ui_WidgetNanoVolt):
    def __init__(self, res_man):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        self.rm = res_man
        self.nvolt = None

        # List ports.
        self.list_port.addItems(filter(lambda k: 'GPIB' in k, self.rm.list_resources()))

        # Connect slots.
        self.btn_connect.clicked.connect(self.connect)
        self.list_port.currentItemChanged.connect(self.update_status)

        # Update GUI.
        self.update_status()

    # Open or close GPIB port.
    def connect(self):
        if self.nvolt is None:
            self.nvolt = self.rm.open_resource(self.list_port.currentItem().text())
        else:
            self.nvolt.close()
            self.nvolt = None
        self.update_status()

    # Update GUI with state.
    def update_status(self):
        # Open if not already open.
        if self.nvolt is None:
            self.btn_connect.setText('Connect')
            self.btn_connect.setEnabled(self.list_port.currentItem() is not None)
            self.list_port.setEnabled(True)
            self.label_port.setText('')

        # Close it if open.
        else:
            self.btn_connect.setText('Disconnect')
            self.btn_connect.setEnabled(True)
            self.list_port.setEnabled(False)
            self.label_port.setText(self.list_port.currentItem().text())

    def fetch(self):
        if self.nvolt is None:
            return np.nan
        else:
            return float(self.nvolt.query(':FETC?'))

# nvolt.write(':TRAC:FEED:CONT NEXT')
# print(nvolt.query(':TRAC:FEED:CONT NEXT ; :TRAC:DATA?'))

if __name__ == "__main__":
    import sys

    def update_value():
        lbl_value.setText(str(nvolt_wid.fetch()))
        pass

    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widgets.
    main_wid = QtWidgets.QWidget()
    nvolt_wid = WidgetNanoVolt(visa.ResourceManager())
    lbl_value = QtWidgets.QLabel()

    # Set font on label.
    font = QtGui.QFont()
    font.setPointSize(20)
    lbl_value.setFont(font)

    # Set the layout.
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(nvolt_wid)
    layout.addWidget(lbl_value)
    main_wid.setLayout(layout)

    # Show window.
    main_wid.show()
    main_wid.setWindowTitle('2182A')

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(100)
    timer.timeout.connect(update_value)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
