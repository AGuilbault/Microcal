import serial
from PyQt5 import QtCore, QtWidgets, QtGui
from serial.tools import list_ports

from WidgetPump import Ui_WidgetPump
from DialogPump import Ui_DialogPump


class WidgetPump(QtWidgets.QWidget, Ui_WidgetPump):
    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Define serial thread.
        self.protocol = SerialThread()

        # List ports.
        for t in list_ports.comports():
            self.combo_port.addItem(t.device)

        # Connect slots.
        self.btn_conn.clicked.connect(self.connect)
        self.btn_config.clicked.connect(self.config)
        self.btn_infuse.clicked.connect(self.button_action)

        self.combo_port.currentIndexChanged.connect(self.update_status)
        self.combo_baud.currentIndexChanged.connect(self.update_status)

        self.protocol.updateSignal.connect(self.update_status)
        self.protocol.recTarSignal.connect(self.update_target)

        # Update GUI.
        self.update_status()

    # Open or close serial port.
    def connect(self):
        # Open if not already open.
        if not self.protocol.state:
            self.protocol.open(self.combo_port.currentText(), self.combo_baud.currentText())
            self.protocol.get_target()
        # Close if open.
        else:
            self.protocol.close()

    def config(self):
        dialog = DialogPump(self)
        if dialog.exec_():
            self.protocol.get_target()

    def button_action(self):
        if self.protocol.state == self.protocol.STOPPED:
            self.protocol.send_run()
        elif self.protocol.state == self.protocol.FORWARD:
            self.protocol.send_stp()
        elif self.protocol.state == self.protocol.STALLED:
            self.protocol.send_run()

    def update_target(self, x):
        if x < 1:
            self.lbl_target.setText(str(x * 1000) + ' µl')
        else:
            self.lbl_target.setText(str(x) + ' ml')

    # Update GUI with state.
    def update_status(self):
        # Open if not already open.
        if not self.protocol.state:
            self.btn_conn.setText('Connect')
            self.btn_conn.setEnabled(self.combo_port.currentIndex() != -1 and
                                     self.combo_baud.currentIndex() != -1)
            self.combo_port.setEnabled(True)
            self.combo_baud.setEnabled(True)

            self.btn_config.setEnabled(False)

            self.lbl_target.setText('NA')

            self.btn_infuse.setEnabled(False)
            self.btn_infuse.setText('Infuse')
            self.ico_state.setText('')
            self.ico_state.setPixmap(QtGui.QPixmap())
            self.lbl_state.setText('Disconnected')
        # Close it if open.
        else:
            self.btn_conn.setText('Disconnect')
            self.btn_conn.setEnabled(True)
            self.combo_port.setEnabled(False)
            self.combo_baud.setEnabled(False)

            self.btn_config.setEnabled(True)

            self.btn_infuse.setEnabled(True)
            if self.protocol.state == self.protocol.STOPPED:
                self.btn_infuse.setText('Infuse')
                self.ico_state.setText('⏹')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\stop.png"))
                self.lbl_state.setText('Stopped')
            elif self.protocol.state == self.protocol.FORWARD:
                self.btn_infuse.setText('Stop')
                self.ico_state.setText('⏩')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\arrow_right.png"))
                self.lbl_state.setText('Running')
            elif self.protocol.state == self.protocol.STALLED:
                self.btn_infuse.setText('Re-infuse')
                self.ico_state.setText('⏸')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\control_pause.png"))
                self.lbl_state.setText('Stalled')


class DialogPump(QtWidgets.QDialog, Ui_DialogPump):
    def __init__(self, parent):
        # Initialise overloaded classes.
        super().__init__()

        self.setupUi(self)

        self.wid = parent

        self.buttonBox.accepted.connect(self.send_config)

        self.wid.protocol.recRatSignal.connect(self.set_rate)
        self.wid.protocol.recDiaSignal.connect(self.spin_diameter.setValue)
        self.wid.protocol.recTarSignal.connect(self.spin_target.setValue)

        self.get_config()

    # Send request to get configuration.
    def get_config(self):
        self.wid.protocol.get_rate()
        self.wid.protocol.get_diameter()
        self.wid.protocol.get_target()

    # Send configuration.
    def send_config(self):
        self.wid.protocol.send_rate(self.spin_rate.value(),
                                    ('MLM', 'ULM', 'MLH', 'ULH')[self.combo_units.currentIndex()])
        self.wid.protocol.send_diameter(self.spin_diameter.value())
        self.wid.protocol.send_target(self.spin_target.value())

    # Slot for receiving both rate and units in one slot.
    def set_rate(self, rate, units_index):
        self.spin_rate.setValue(rate)
        self.combo_units.setCurrentIndex(units_index)


class SerialThread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal()
    recRatSignal = QtCore.pyqtSignal([float, int])
    recDiaSignal = QtCore.pyqtSignal([float])
    recTarSignal = QtCore.pyqtSignal([float])

    # SerialThread possible states.
    DISCONNECTED = 0
    STOPPED = 1
    FORWARD = 2
    STALLED = 3

    """ Requests queue. """
    class Requests:
        def __init__(self):
            self.mmd = False    # Set diameter.
            self.mlm = False    # Set rate.
            self.mlt = False    # Set target.
            self.stp = False    # Send stop command.
            self.run = False    # Send run command.
            self.dia = False    # Get diameter.
            self.rat = False    # Get rate.
            self.tar = False    # Get target.

            self.diameter = 4.78    # Default diameter.
            self.rate = 120         # Default rate.
            self.rate_unit = 'ULM'  # Default rate unit.
            self.target = 0.005     # Default target.

    def __init__(self):
        # Init QThread class.
        super().__init__()

        # Init serial port (not opened).
        self.ser = serial.Serial(parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO)

        # Set default state.
        self.state = self.DISCONNECTED
        self._req = self.Requests()

    def open(self, port, baudrate):
        # Change state.
        self.state = self.STOPPED

        # Change serial port settings.
        self.ser.port = port
        self.ser.baudrate = baudrate

        # Open serial port.
        self.ser.open()

        # Start thread.
        self.start()

    def close(self):
        # Change state.
        self.state = self.DISCONNECTED

        # Wait until thread finishes.
        self.wait()

        # Close serial port.
        self.ser.close()

    """ Infuse and stop commands """
    def send_run(self):
        self._req.run = True

    def send_stp(self):
        self._req.stp = True

    """ Send config commands """
    def send_diameter(self, diameter):
        self._req.diameter = diameter
        self._req.mmd = True

    def send_rate(self, rate, unit):
        self._req.rate = rate
        self._req.rate_unit = unit
        self._req.mlm = True

    def send_target(self, target):
        self._req.target = target
        self._req.mlt = True

    """ Get config commands """
    def get_diameter(self):
        self._req.dia = True

    def get_rate(self):
        self._req.rat = True

    def get_target(self):
        self._req.tar = True

    """ Thread execution loop. """
    def run(self):
        # Send update signal (connected).
        self.updateSignal.emit()

        # Init variables.
        error = None
        packet = bytearray()
        in_packet = False
        requested = 0

        # Thread loop. While connected.
        while self.ser.is_open and self.state:

            # Try reading.
            try:
                # Read all that is there.
                data = self.ser.read(self.ser.in_waiting)
            except serial.SerialException as e:
                # Probably some I/O problem such as disconnected USB serial adapters.
                error = e
                # Exit thread.
                break
            else:
                # For each byte.
                for byte in serial.iterbytes(data):
                    if byte == b'\n':
                        in_packet = True
                        del packet[:]
                    elif byte == b':':
                        self.updateSignal.emit()
                        self.state = self.STOPPED
                        self._req.stp = False
                        in_packet = False
                    elif byte == b'>':
                        self.updateSignal.emit()
                        self.state = self.FORWARD
                        in_packet = False
                    elif byte == b'*':
                        self.updateSignal.emit()
                        self.state = self.STALLED
                        self._req.stp = False
                        in_packet = False
                    elif byte == b'\r':
                        in_packet = False
                        if requested == 1:
                            self.recDiaSignal.emit(float(bytes(packet)))
                        elif requested == 2:
                            self.recRatSignal.emit(float(packet[:8]),
                                                   [b'ml/mn', b'ul/mn', b'ml/hr', b'ul/hr'].index(bytes(packet[9:])))
                        elif requested == 3:
                            self.recTarSignal.emit(float(bytes(packet)))
                        requested = 0
                        print(bytes(packet))
                    elif in_packet:
                        packet.extend(byte)

            # If not in packet, write pending commands.
            if not in_packet:
                in_packet = True
                if self._req.stp and self.state is self.FORWARD:
                    self.ser.write(b'STP\r')
                elif self._req.mmd and self.state is not self.FORWARD:
                    self.ser.write('MMD{0:.05}\r'.format(self._req.diameter).encode('ascii'))
                    self._req.mmd = False
                elif self._req.mlm and self.state is not self.FORWARD:
                    self.ser.write('{1}{0:.05}\r'.format(self._req.rate, self._req.rate_unit).encode('ascii'))
                    self._req.mlm = False
                elif self._req.mlt and self.state is not self.FORWARD:
                    self.ser.write('MLT{0:.05}\r'.format(self._req.target).encode('ascii'))
                    self._req.mlt = False
                elif self._req.run and self.state is not self.FORWARD:
                    self.ser.write(b'RUN\r')
                    self._req.run = False
                elif self._req.dia:
                    self.ser.write(b'DIA\r')
                    self._req.dia = False
                    requested = 1
                elif self._req.rat:
                    self.ser.write(b'RAT\r')
                    self._req.rat = False
                    requested = 2
                elif self._req.tar:
                    self.ser.write(b'TAR\r')
                    self._req.tar = False
                    requested = 3
                elif self.state is self.FORWARD:
                    self.ser.write(b'\r')
                else:
                    in_packet = False

        # Thread finishing (disconnected)
        self.state = self.DISCONNECTED

        # Send update signal (disconnected).
        self.updateSignal.emit()

        # If disconnected because of an error, print it.
        if error is not None:
            self.connection_lost(error)


if __name__ == "__main__":
    import sys
    # Define app.
    app = QtWidgets.QApplication(sys.argv)

    # Create pump widget.
    wid = WidgetPump()

    # Show window.
    wid.show()

    # Run GUI loop.
    sys.exit(app.exec_())
