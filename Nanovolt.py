import numpy as np
import re
import visa
from PyQt5 import QtCore, QtWidgets, QtGui

from WidgetNanovolt import Ui_WidgetNanovolt
from DialogNanovolt import Ui_DialogNanovolt


class WidgetNanovolt(QtWidgets.QWidget, Ui_WidgetNanovolt):
    def __init__(self, res_man):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        self.rm = res_man
        self.nvolt = None

        # List ports.
        self.combo_port.addItems(filter(lambda k: 'GPIB' in k, self.rm.list_resources()))

        # Connect slots.
        self.btn_connect.clicked.connect(self.connect)
        self.combo_port.currentIndexChanged.connect(self.update_status)
        self.btn_config.clicked.connect(self.config)

        # Update GUI.
        self.update_status()

    # Open or close GPIB port.
    def connect(self):
        if self.nvolt is None:
            self.nvolt = self.rm.open_resource(self.combo_port.currentText())
        else:
            self.nvolt.close()
            self.nvolt = None
        self.update_status()

    def config(self):
        dialog = DialogNanovolt(self)
        dialog.exec_()

    # Update GUI with state.
    def update_status(self):
        # Open if not already open.
        if self.nvolt is None:
            self.btn_connect.setText('Connect')
            self.btn_connect.setEnabled(self.combo_port.currentIndex() != -1)
            self.combo_port.setEnabled(True)
            self.btn_config.setEnabled(False)

        # Close it if open.
        else:
            self.btn_connect.setText('Disconnect')
            self.btn_connect.setEnabled(True)
            self.combo_port.setEnabled(False)
            self.btn_config.setEnabled(True)

    def fetch(self):
        if self.nvolt is None:
            self.lbl_value.setText('NA')
            return np.nan
        else:
            ret = float(self.nvolt.query(':FETC?'))
            self.lbl_value.setText(str(ret) + ' V')
            return ret


class DialogNanovolt(QtWidgets.QDialog, Ui_DialogNanovolt):
    def __init__(self, parent):
        # Initialise overloaded classes.
        super().__init__()

        self.setupUi(self)

        self.wid = parent

        self.buttonBox.accepted.connect(self.send_config)
        self.combo_channel.currentIndexChanged.connect(self.channel_changed)

        self.get_config()

    def get_config(self):
        # Query function and channel.
        temp = self.wid.nvolt.query(':SENSE:FUNCTION?;:SENSE:CHANNEL?')

        # Split function and channel.
        func, chan = re.search(r'"(.*)";(\d)', temp).groups()

        # If function is not voltage, warn the user.
        if func != 'VOLT:DC':
            QtWidgets.QMessageBox.warning(self, 'Warning', "Current mode is: " + func +
                                          "\nMode will be changed when accepting configuration dialog.")

        # Set the channel in the combo box.
        self.combo_channel.setCurrentIndex(int(chan)-1)

        # Get the configuration.
        temp = self.wid.nvolt.query(':SENSE:VOLT:CHAN' + chan + ':RANGE?;' +
                                    ':SENSE:VOLT:CHAN' + chan + ':RANGE:AUTO?;' +
                                    ':SENSE:VOLT:CHAN' + chan + ':LPASS?;' +
                                    ':SENSE:VOLT:CHAN' + chan + ':DFIL?;' +
                                    ':SENSE:VOLT:CHAN' + chan + ':DFIL:COUNT?;' +
                                    ':SENSE:VOLT:CHAN' + chan + ':DFIL:TCON?;' +
                                    ':SYST:LSYNC?;' +
                                    ':SENS:VOLT:NPLC?')

        # Split the configuration.
        temp = re.split(r'[;\n]', temp)

        # Set range in the combo box.
        if temp[1] == '1':
            self.combo_range.setCurrentIndex(self.combo_range.findText('Autoscale'))
        else:
            rang = float(temp[0])
            if rang <= 0.01:
                self.combo_range.setCurrentIndex(self.combo_range.findText('10 mV'))
            elif rang <= 0.1:
                self.combo_range.setCurrentIndex(self.combo_range.findText('100 mV'))
            elif rang <= 1:
                self.combo_range.setCurrentIndex(self.combo_range.findText('1 V'))
            elif rang <= 10:
                self.combo_range.setCurrentIndex(self.combo_range.findText('10 V'))
            elif rang <= 100:
                self.combo_range.setCurrentIndex(self.combo_range.findText('100 V'))

        # Set the filter checkboxes.
        self.check_analog.setChecked(temp[2] == '1')
        self.check_digital.setChecked(temp[3] == '1')

        self.spin_filter.setValue(int(temp[4]))

        print(temp[5])
        if temp[5] == 'MOV':
            self.radio_moving.setChecked(True)
        else:
            self.radio_repeating.setChecked(True)

        self.check_lsync.setChecked(temp[6] == '1')

        self.spin_rate.setValue(float(temp[7]))

    def send_config(self):
        self.wid.nvolt.write(':SENS:FUNC "VOLT";' +
                             ':SENS:' + self.combo_channel.currentText())

    def channel_changed(self):
        self.combo_range.clear()
        self.combo_range.addItems(('100 mv', '1 V', '10 V', 'Autoscale'))
        if self.combo_channel.currentIndex() == 0:
            self.combo_range.insertItem(0, '10 mV')
            self.combo_range.insertItem(4, '100 V')
            self.combo_range.setCurrentIndex(0)

if __name__ == "__main__":
    import sys

    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widgets.
    wid = WidgetNanovolt(visa.ResourceManager())

    # Set font on label.
    font = QtGui.QFont()
    font.setPointSize(20)
    wid.lbl_value.setFont(font)

    # Show window.
    wid.show()

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(500)
    timer.timeout.connect(lambda: wid.fetch())
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
