import serial
from PyQt5 import QtCore, QtWidgets, QtGui
from serial.tools import list_ports

from WidgetPump import Ui_WidgetPump
from DialogPump import Ui_DialogPump


class WidgetPump(QtWidgets.QWidget, Ui_WidgetPump):
    open = QtCore.pyqtSignal(str, str)
    close = QtCore.pyqtSignal()
    s_run = QtCore.pyqtSignal()
    s_stp = QtCore.pyqtSignal()

    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Define serial thread.
        self.thread = QtCore.QThread()
        self.protocol = SerialThread()

        self.protocol.moveToThread(self.thread)

        self.thread.started.connect(self.protocol.start)

        self.protocol.finished.connect(self.thread.quit)
        self.protocol.updateSignal.connect(self.update_status)
        # self.protocol.recTarSignal.connect(self.update_target)

        self.open.connect(self.protocol.open)
        self.close.connect(self.protocol.close)
        self.s_run.connect(self.protocol.send_run)
        self.s_stp.connect(self.protocol.send_stp)

        self.thread.start()

        # List ports.
        for t in list_ports.comports():
            self.combo_port.addItem(t.device)

        # Connect slots.
        self.btn_conn.clicked.connect(self.connect)
        self.btn_config.clicked.connect(self.config)
        self.btn_infuse.clicked.connect(self.button_action)

        # Update GUI.
        self.update_status(SerialThread.DISCONNECTED)

        self.connected = False
        self.state = SerialThread.DISCONNECTED

    # Open or close serial port.
    def connect(self):
        if not self.connected:
            port = self.combo_port.currentText()
            if port != '':  # If port selected, connect.
                self.open.emit(port, self.combo_baud.currentText())
                self.connected = True
            else:  # If not, show essor message.
                QtWidgets.QMessageBox.critical(self, 'Error', 'No port selected.')
        else:
            self.close.emit()
            self.connected = False
        print('connected')

    def config(self):
        dialog = DialogPump(self)
        if dialog.exec_():
            pass
            #self.protocol.get_target()

    def button_action(self):
        if self.state == SerialThread.STOPPED or self.state == SerialThread.STALLED:
            self.s_run.emit()
        elif self.state == SerialThread.FORWARD:
            self.s_stp.emit()

    def update_target(self, x):
        if x < 1:
            self.lbl_target.setText(str(x * 1000) + ' µl')
        else:
            self.lbl_target.setText(str(x) + ' ml')

    # Update GUI with state.
    @QtCore.pyqtSlot(int)
    def update_status(self, status):
        self.state = status
        print('update : ' + str(status))
        # Open if not already open.
        if not status:
            self.btn_conn.setText('Connect')
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
            self.combo_port.setEnabled(False)
            self.combo_baud.setEnabled(False)

            self.btn_config.setEnabled(True)

            self.btn_infuse.setEnabled(True)
            if status == SerialThread.STOPPED:
                self.btn_infuse.setText('Infuse')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\stop.png"))
                self.lbl_state.setText('Stopped')
            elif status == SerialThread.FORWARD:
                self.btn_infuse.setText('Stop')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\arrow_right.png"))
                self.lbl_state.setText('Running')
            elif status == SerialThread.STALLED:
                self.btn_infuse.setText('Re-infuse')
                self.ico_state.setPixmap(QtGui.QPixmap(".\\ico\\control_pause.png"))
                self.lbl_state.setText('Stalled')


class DialogPump(QtWidgets.QDialog, Ui_DialogPump):
    g_rat = QtCore.pyqtSignal()
    g_dia = QtCore.pyqtSignal()
    g_tar = QtCore.pyqtSignal()

    s_rat = QtCore.pyqtSignal(float, int)
    s_dia = QtCore.pyqtSignal(float)
    s_tar = QtCore.pyqtSignal(float)

    def __init__(self, parent):
        # Initialise overloaded classes.
        super().__init__()

        self.setupUi(self)

        self.wid = parent

        self.buttonBox.accepted.connect(self.send_config)

        self.g_rat.connect(parent.protocol.get_rate)
        self.g_dia.connect(parent.protocol.get_diameter)
        self.g_tar.connect(parent.protocol.get_target)

        self.s_rat.connect(parent.protocol.send_rate)
        self.s_dia.connect(parent.protocol.send_diameter)
        self.s_tar.connect(parent.protocol.send_target)

        parent.protocol.recRatSignal.connect(self.set_rate)
        parent.protocol.recDiaSignal.connect(self.spin_diameter.setValue)
        parent.protocol.recTarSignal.connect(self.spin_target.setValue)

        # Send request to get configuration.
        self.g_rat.emit()
        self.g_dia.emit()
        self.g_tar.emit()

    # Send configuration.
    @QtCore.pyqtSlot()
    def send_config(self):
        self.s_dia.emit(self.spin_diameter.value())
        self.s_rat.emit(self.spin_rate.value(), self.combo_units.currentIndex())
        self.s_tar.emit(self.spin_target.value())

    # Slot for receiving both rate and units in one slot.
    @QtCore.pyqtSlot(float, int)
    def set_rate(self, rate, units_index):
        self.spin_rate.setValue(rate)
        self.combo_units.setCurrentIndex(units_index)


class SerialThread(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    updateSignal = QtCore.pyqtSignal(int)
    recRatSignal = QtCore.pyqtSignal([float, int])
    recDiaSignal = QtCore.pyqtSignal([float])
    recTarSignal = QtCore.pyqtSignal([float])

    # SerialThread possible states.
    DISCONNECTED = 0
    STOPPED = 1
    FORWARD = 2
    STALLED = 3

    @QtCore.pyqtSlot()
    def start(self):
        # Init serial port (not opened).
        self.ser = serial.Serial(parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO)

    @QtCore.pyqtSlot()
    def stop(self):
        self.finished.emit()

    @QtCore.pyqtSlot(str, str)
    def open(self, port, baudrate):
        # Change serial port settings.
        self.ser.port = port
        self.ser.baudrate = baudrate

        # Open serial port.
        self.ser.open()

        # Change state.
        self.updateSignal.emit(SerialThread.STOPPED)

        # self.run()

    @QtCore.pyqtSlot()
    def close(self):
        # Close serial port.
        self.ser.close()

        # Change state.
        self.updateSignal.emit(SerialThread.DISCONNECTED)

    """ Infuse and stop commands """
    @QtCore.pyqtSlot()
    def send_run(self):
        self.ser.write(b'RUN\r')
        in_packet = False
        over = False
        while not over and self.ser.is_open:
            if not in_packet:
                # Check if signals received.
                QtWidgets.QApplication.processEvents()
                # Send carriage return to receive status.
                self.ser.write(b'\r')
                in_packet = True

            # Read all that is there.
            data = self.ser.read(self.ser.in_waiting or 1)

            # For each byte.
            for byte in serial.iterbytes(data):
                if byte == b'\n':
                    in_packet = True
                elif byte == b':':
                    self.updateSignal.emit(SerialThread.STOPPED)
                    over = True
                    in_packet = False
                elif byte == b'>':
                    self.updateSignal.emit(SerialThread.FORWARD)
                    in_packet = False
                elif byte == b'*':
                    self.updateSignal.emit(SerialThread.STALLED)
                    over = True
                    in_packet = False

    @QtCore.pyqtSlot()
    def send_stp(self):
        self.ser.write(b'STP\r')

    """ Send config commands """
    @QtCore.pyqtSlot(float)
    def send_diameter(self, diameter):
        self.ser.reset_input_buffer()
        self.ser.write('MMD{0:.05}\r'.format(diameter).encode('ascii'))
        self.run(4)

    @QtCore.pyqtSlot(float, int)
    def send_rate(self, rate, unit):
        self.ser.reset_input_buffer()
        self.ser.write('{1}{0:.05}\r'.format(rate, ('MLM', 'ULM', 'MLH', 'ULH')[unit]).encode('ascii'))
        self.run(4)

    @QtCore.pyqtSlot(float)
    def send_target(self, target):
        self.ser.reset_input_buffer()
        self.ser.write('MLT{0:.05}\r'.format(target).encode('ascii'))
        self.run(4)

    """ Get config commands """
    @QtCore.pyqtSlot()
    def get_diameter(self):
        self.ser.reset_input_buffer()
        self.ser.write(b'DIA\r')
        self.run(1)

    @QtCore.pyqtSlot()
    def get_rate(self):
        self.ser.reset_input_buffer()
        self.ser.write(b'RAT\r')
        self.run(2)

    @QtCore.pyqtSlot()
    def get_target(self):
        self.ser.reset_input_buffer()
        self.ser.write(b'TAR\r')
        self.run(3)

    def run(self, requested):
        # Init variables.
        packet = bytearray()
        in_packet = False

        # Thread loop. While connected.
        while self.ser.is_open and (requested or in_packet):
            # Read all that is there.
            data = self.ser.read(self.ser.in_waiting or 1)

            # For each byte.
            for byte in serial.iterbytes(data):
                if byte == b'\n':
                    in_packet = True
                    del packet[:]
                elif byte == b':':
                    self.updateSignal.emit(SerialThread.STOPPED)
                    in_packet = False
                    requested = 0
                    print(bytes(packet))
                elif byte == b'>':
                    self.updateSignal.emit(SerialThread.FORWARD)
                    in_packet = False
                    requested = 0
                    print(bytes(packet))
                elif byte == b'*':
                    self.updateSignal.emit(SerialThread.STALLED)
                    in_packet = False
                    requested = 0
                    print(bytes(packet))
                elif byte == b'\r':
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
