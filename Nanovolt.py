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

        # Init variable.
        self.nvolt = None

        # List ports and filter for GPIB devices only.
        self.combo_port.addItems(filter(lambda k: 'GPIB' in k, self.rm.list_resources()))

        # Connect slots.
        self.btn_connect.clicked.connect(self.connect)
        self.combo_port.currentIndexChanged.connect(self.update_status)
        self.btn_config.clicked.connect(self.config)

        # Update GUI.
        self.update_status()

    # Open or close GPIB port.
    def connect(self):
        # If closed, open.
        if self.nvolt is None:
            # Open device.
            self.nvolt = self.rm.open_resource(self.combo_port.currentText())
            # Query channel.
            self.lbl_channel.setText('CH' + self.nvolt.query(':SENSE:CHANNEL?')[0] + ':')
        else:
            # Close device.
            self.nvolt.close()
            self.nvolt = None
            self.lbl_channel.setText('CH?:')
        self.update_status()

    def config(self):
        # Show configuration dialog.
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
            # If disconnected, return NaN.
            self.lbl_value.setText('NA')
            return np.nan
        else:
            # If connected, fetch the value.
            value = float(self.nvolt.query(':FETC?'))
            if abs(value) > 100:
                # If out of range, return NaN.
                self.lbl_value.setText('OVERFLOW')
                return np.nan
            else:
                # Format value with units and return value.
                if abs(value) < 0.001:
                    self.lbl_value.setText("{:.3f}".format(value * 1000000) + ' µV')
                elif abs(value) < 1.0:
                    self.lbl_value.setText("{:.3f}".format(value * 1000) + ' mV')
                else:
                    self.lbl_value.setText("{:.3f}".format(value) + ' V')
                return value


class DialogNanovolt(QtWidgets.QDialog, Ui_DialogNanovolt):
    def __init__(self, parent):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Get reference to parent widget.
        self.wid = parent

        # Connect slots.
        self.buttonBox.accepted.connect(self.send_config)
        self.combo_channel.currentIndexChanged.connect(self.channel_changed)

        # Get the configuration from the instruments and update widgets.
        self.get_config()

    def get_config(self):
        # Query function and channel.
        config = self.wid.nvolt.query(':SENSE:FUNCTION?;:SENSE:CHANNEL?')

        # Split function and channel.
        func, chan = re.search(r'"(.*)";(\d)', config).groups()

        # If function is not voltage, warn the user.
        if func != 'VOLT:DC':
            QtWidgets.QMessageBox.warning(self, 'Warning', "Current mode is: " + func +
                                          "\nMode will be changed when accepting configuration dialog.")

        # Set the channel in the combo box.
        self.combo_channel.setCurrentIndex(int(chan) - 1)

        # Get all the configuration.
        config = self.wid.nvolt.query(':SENSE:VOLT:CHAN' + chan + ':RANGE?;' +
                                      ':SENSE:VOLT:CHAN' + chan + ':RANGE:AUTO?;' +
                                      ':SENSE:VOLT:CHAN' + chan + ':LPASS?;' +
                                      ':SENSE:VOLT:CHAN' + chan + ':DFIL?;' +
                                      ':SENSE:VOLT:CHAN' + chan + ':DFIL:COUNT?;' +
                                      ':SENSE:VOLT:CHAN' + chan + ':DFIL:TCON?;' +
                                      ':SYST:LSYNC?;' +
                                      ':SENS:VOLT:NPLC?')

        # Split the configuration.
        config = re.split(r'[;\n]', config)

        # Set range in the combo box.
        if config[1] == '1':
            self.combo_range.setCurrentIndex(self.combo_range.findText('Autoscale'))
        else:
            rang = float(config[0])
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
        self.check_analog.setChecked(config[2] == '1')
        self.check_digital.setChecked(config[3] == '1')

        # Set the filter count.
        self.spin_filter.setValue(int(config[4]))

        # Set the filter mode.
        if config[5] == 'MOV':
            self.radio_moving.setChecked(True)
        elif config[5] == 'REP':
            self.radio_repeating.setChecked(True)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Invalid digital filter mode')

        # Set the line cycle synchronisation.
        self.check_lsync.setChecked(config[6] == '1')

        # Set the rate.
        self.spin_rate.setValue(float(config[7]))

    def send_config(self):
        # Set channel.
        chan = str(self.combo_channel.currentIndex() + 1)

        # Send function and channel.
        self.wid.nvolt.write(':SENS:FUNC "VOLT";' +
                             ':SENS:CHAN ' + chan)

        # Set label in parent widget. TODO: move to parent widget.
        self.wid.lbl_channel.setText('CH' + chan + ':')

        # Send range.
        rang = self.combo_range.currentText()
        if rang == 'Autoscale':
            self.wid.nvolt.write(':SENSE:VOLT:CHAN' + chan + ':RANGE:AUTO 1')
        else:
            # Set range to manual.
            self.wid.nvolt.write(':SENSE:VOLT:CHAN' + chan + ':RANGE:AUTO 0')
            # Split value and units.
            val, units = re.search(r'(\d*).*?(mV|V)', rang).groups()
            if units == 'mV':
                # Send (value / 1000) if units are mV.
                self.wid.nvolt.write(':SENSE:VOLT:CHAN{0}:RANGE {1:0.2f}'.format(chan, float(val) / 1000))
            elif units == 'V':
                # Send value if units are V.
                self.wid.nvolt.write(':SENSE:VOLT:CHAN{0}:RANGE {1}'.format(chan, val))
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Invalid range')

        # Send line cycle synchronization setting.
        self.wid.nvolt.write(':SYST:LSYNC ' + ('1' if self.check_lsync.isChecked() else '0'))

        # Send rate.
        self.wid.nvolt.write(':SENS:VOLT:NPLC ' + str(self.spin_rate.value()))

        # Send analog filter setting.
        self.wid.nvolt.write(':SENSE:VOLT:CHAN' + chan + ':LPASS ' + ('1' if self.check_analog.isChecked() else '0'))

        # Send digital filter settings.
        if self.check_digital.isChecked():
            self.wid.nvolt.write(':SENSE:VOLT:CHAN' + chan + ':DFIL 1;' +
                                 ':SENSE:VOLT:CHAN' + chan + ':DFIL:COUNT ' +
                                 str(self.spin_filter.value()) + ';' +
                                 ':SENSE:VOLT:CHAN' + chan + ':DFIL:TCON ' +
                                 ('MOV' if self.radio_moving.isChecked() else 'REP'))
        else:
            self.wid.nvolt.write(':SENSE:VOLT:CHAN' + chan + ':DFIL 0')

    def channel_changed(self):
        # Save the selected range.
        rang = self.combo_range.currentText()
        # Clear all items in range combo box.
        self.combo_range.clear()
        # Add items available for both channels.
        self.combo_range.addItems(('100 mv', '1 V', '10 V', 'Autoscale'))
        # If selected channel is channel 1.
        if self.combo_channel.currentIndex() == 0:
            # Add items available only for channel 1.
            self.combo_range.insertItem(0, '10 mV')
            self.combo_range.insertItem(4, '100 V')
        # Set range back to the value it was, if possible.
        rang = self.combo_range.findText(rang)
        self.combo_range.setCurrentIndex(rang if rang != -1 else 0)


if __name__ == "__main__":
    import sys

    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widget.
    wid = WidgetNanovolt(visa.ResourceManager())

    # Change label font. (Bigger for standalone app)
    font = QtGui.QFont()
    font.setPointSize(20)
    font.setUnderline(True)
    wid.lbl_value.setFont(font)

    # Show window.
    wid.show()

    # Create timer to fetch data and update label every 500 ms.
    timer = QtCore.QTimer()
    timer.setInterval(500)
    timer.timeout.connect(lambda: wid.fetch())
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
