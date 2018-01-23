import numpy as np
import visa
from PyQt5 import QtCore, QtWidgets, QtGui



from WidgetCourant import Ui_WidgetCourant

class WidgetCourant(QtWidgets.QWidget, Ui_WidgetCourant):
    def __init__(self, res_man):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)
        self.rm = res_man

        # Init variable.
        self.courant = None

        # List ports and filter for GPIB devices only.
        self.combo_port.addItems(filter(lambda k: 'GPIB' in k, self.rm.list_resources()))

        # Connect slots.
        self.btn_connect.clicked.connect(self.connect)
        self.combo_port.currentIndexChanged.connect(self.update_status)
        self.btn_config.clicked.connect(self.config)
        self.btn_browse.clicked.connect(self.browse)
        self.connect_status.setPixmap(QtGui.QPixmap(".\\ico\\WX_circle_red.png"))

        # Update GUI.
        self.update_status()

    # Open or close GPIB port.
    def connect(self):
        # If closed, open.
        if self.courant is None:
            # Open device.
            self.courant = self.rm.open_resource(self.combo_port.currentText())
        else:
            # Close device.
            self.courant.control_ren(False)
            self.courant.close()
            self.courant = None

        self.update_status()

    # Update GUI with state.
    def update_status(self):
        # Open if not already opened.
        if self.courant is None:
            self.btn_connect.setText('Connect')
            self.btn_connect.setEnabled(self.combo_port.currentIndex() != -1)
            self.combo_port.setEnabled(True)
            self.btn_config.setEnabled(False)
            self.connect_status.setPixmap(QtGui.QPixmap(".\\ico\\WX_circle_red.png"))

        # Close it if open.
        else:
            self.btn_connect.setText('Disconnect')
            self.btn_connect.setEnabled(True)
            self.combo_port.setEnabled(False)
            self.btn_config.setEnabled(True)
            self.connect_status.setPixmap(QtGui.QPixmap(".\\ico\\WX_circle_green.png"))

    def config(self):
        data_config = np.loadtxt("%s" % self.line_config.text(), skiprows = 1)
        print(data_config)
        index = 1
        self.courant.clear()
        for data_set in data_config:
            self.courant.write("B%fL%fV%dI%fW%dX" %(index, index, data_set[0], data_set[1], data_set[2]))
            index += 1

    def browse(self):
        self.line_config.setText(QtWidgets.QFileDialog.getOpenFileName()[0])



if __name__ == "__main__":
    import sys

    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widget.
    wid = WidgetCourant(visa.ResourceManager())

    # Show window.
    wid.show()

    # Run GUI loop.
    sys.exit(app.exec_())