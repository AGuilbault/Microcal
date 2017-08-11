"""
Module controls PHD2000 pump.
Can be executed as standalone or imported to be used as a widget.
"""
import serial
from PyQt5 import QtCore, QtWidgets, QtGui
from serial.tools import list_ports

from WidgetPump import Ui_WidgetPump
from DialogPump import Ui_DialogPump


class WidgetPump(QtWidgets.QWidget, Ui_WidgetPump):
    # Signals to interface thread.
    open = QtCore.pyqtSignal(str, str)
    close = QtCore.pyqtSignal()
    s_run = QtCore.pyqtSignal()
    s_stp = QtCore.pyqtSignal()
    g_tar = QtCore.pyqtSignal()

    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Start serial thread.
        self.thread = QtCore.QThread()
        self.protocol = SerialThread()

        # Move object to thread.
        self.protocol.moveToThread(self.thread)

        # Connect slots and signals.
        self.thread.started.connect(self.protocol.start)

        self.protocol.finished.connect(self.thread.quit)
        self.protocol.updateSignal.connect(self.update_status)
        self.protocol.recTarSignal.connect(self.update_target)

        self.open.connect(self.protocol.open)
        self.close.connect(self.protocol.close)
        self.s_run.connect(self.protocol.send_run)
        self.s_stp.connect(self.protocol.send_stp)
        self.g_tar.connect(self.protocol.get_target)

        # Start thread.
        self.thread.start()

        # List ports.
        for t in list_ports.comports():
            self.combo_port.addItem(t.device)

        # Connect interface slots.
        self.btn_conn.clicked.connect(self.connect)
        self.btn_config.clicked.connect(self.config)
        self.btn_infuse.clicked.connect(self.button_action)

        # Update GUI.
        self.update_status(SerialThread.DISCONNECTED)

        # Set initial state.
        self.connected = False
        self.state = SerialThread.DISCONNECTED

    # Open or close serial port.
    @QtCore.pyqtSlot()
    def connect(self):
        if not self.connected:  # Connect if not connected.
            port = self.combo_port.currentText()
            if port != '':  # If port selected, connect.
                self.open.emit(port, self.combo_baud.currentText())
                self.connected = True
                self.g_tar.emit()
            else:  # If not, show essor message.
                QtWidgets.QMessageBox.critical(self, 'Error', 'No port selected.')
        else:  # If connected close.
            self.close.emit()
            self.connected = False

    # Show configuration dialog.
    @QtCore.pyqtSlot()
    def config(self):
        dialog = DialogPump(self.protocol)
        if dialog.exec_():     # If dialog accepted (configuration sent).
            self.g_tar.emit()  # Get target to update label.

    @QtCore.pyqtSlot()
    def button_action(self):
        # If not running, send run command.
        if self.state == SerialThread.STOPPED or self.state == SerialThread.STALLED:
            self.s_run.emit()
        # Otherwise, send stop command.
        elif self.state == SerialThread.FORWARD:
            self.s_stp.emit()

    # Slot to receive target and update label.
    @QtCore.pyqtSlot(float)
    def update_target(self, tar):
        if tar < 1:  # If less than a ml, show in µl.
            self.lbl_target.setText('{:0.5} µl'.format(tar * 1000))
        else:        # Otherwise, show in ml.
            self.lbl_target.setText('{:0.5} ml'.format(tar))

    # Update GUI with state.
    @QtCore.pyqtSlot(int)
    def update_status(self, status):
        self.state = status

        # Set connection button text.
        self.btn_conn.setText('Connect' if not status else 'Disconnect')

        # Disable combo boxes when connected.
        self.combo_port.setEnabled(not status)
        self.combo_baud.setEnabled(not status)

        # Enable configuration and infusion when connected.
        self.btn_config.setEnabled(status)
        self.btn_infuse.setEnabled(status)

        # Update status label, status icon and action button text.
        if status == SerialThread.DISCONNECTED:
            # Reset target label if disconnected.
            self.lbl_target.setText('NA')

            self.btn_infuse.setText('Infuse')
            self.ico_state.setPixmap(QtGui.QPixmap())
            self.lbl_state.setText('Disconnected')
        elif status == SerialThread.STOPPED:
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

    def __init__(self, protocol):
        # Initialise overloaded classes.
        super().__init__()

        self.setupUi(self)

        self.buttonBox.accepted.connect(self.send_config)

        self.g_rat.connect(protocol.get_rate)
        self.g_dia.connect(protocol.get_diameter)
        self.g_tar.connect(protocol.get_target)

        self.s_rat.connect(protocol.send_rate)
        self.s_dia.connect(protocol.send_diameter)
        self.s_tar.connect(protocol.send_target)

        protocol.recRatSignal.connect(self.set_rate)
        protocol.recDiaSignal.connect(self.spin_diameter.setValue)
        protocol.recTarSignal.connect(self.spin_target.setValue)

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
    """
    Thread class. Used to control the serial port communicating with the pump.
    """

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

    @QtCore.pyqtSlot()
    def close(self):
        # Close serial port.
        self.ser.close()

        # Change state.
        self.updateSignal.emit(SerialThread.DISCONNECTED)

    """ Infuse and stop commands """
    @QtCore.pyqtSlot()
    def send_run(self):
        """
        Sends run command and updates status until pump has stopped.
        """
        self.ser.write(b'RUN\r')
        over = False

        while not over and self.ser.is_open:
            # Send carriage return to receive status.
            self.ser.write(b'\r')
            in_packet = True

            while in_packet and self.ser.is_open:
                # Read all that is there.
                data = self.ser.read(self.ser.in_waiting or 1)

                # For each byte.
                for byte in serial.iterbytes(data):
                    if byte == b':':
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

            # Check if signals require processing.
            QtWidgets.QApplication.processEvents()

    @QtCore.pyqtSlot()
    def send_stp(self):
        self.ser.write(b'STP\r')

    """ Send config commands """
    @QtCore.pyqtSlot(float)
    def send_diameter(self, diameter):
        self.ser.reset_input_buffer()
        self.ser.write('MMD{0:.05}\r'.format(diameter).encode('ascii'))
        self.get_answer(4)  # Wait for answer from the pump.

    @QtCore.pyqtSlot(float, int)
    def send_rate(self, rate, unit):
        self.ser.reset_input_buffer()
        self.ser.write('{1}{0:.05}\r'.format(rate, ('MLM', 'ULM', 'MLH', 'ULH')[unit]).encode('ascii'))
        self.get_answer(4)  # Wait for answer from the pump.

    @QtCore.pyqtSlot(float)
    def send_target(self, target):
        self.ser.reset_input_buffer()
        self.ser.write('MLT{0:.05}\r'.format(target).encode('ascii'))
        self.get_answer(4)  # Wait for answer from the pump.

    """ Get config commands """
    @QtCore.pyqtSlot()
    def get_diameter(self):
        self.ser.reset_input_buffer()   # Clear input buffer.
        self.ser.write(b'DIA\r')        # Send request.
        self.get_answer(1)              # Wait for answer from the pump.

    @QtCore.pyqtSlot()
    def get_rate(self):
        self.ser.reset_input_buffer()   # Clear input buffer.
        self.ser.write(b'RAT\r')        # Send request.
        self.get_answer(2)              # Wait for answer from the pump.

    @QtCore.pyqtSlot()
    def get_target(self):
        self.ser.reset_input_buffer()   # Clear input buffer.
        self.ser.write(b'TAR\r')        # Send request.
        self.get_answer(3)              # Wait for answer from the pump.

    def get_answer(self, requested):
        """
        Function reads the bytes until the requested answer is given.
        
        :param requested: Kind of answer to expect.
            1 = Diameter
            2 = Rate
            3 = Target
        """
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
                elif byte == b'>':
                    self.updateSignal.emit(SerialThread.FORWARD)
                    in_packet = False
                    requested = 0
                elif byte == b'*':
                    self.updateSignal.emit(SerialThread.STALLED)
                    in_packet = False
                    requested = 0
                elif byte == b'\r':
                    if requested == 1:
                        self.recDiaSignal.emit(float(bytes(packet)))
                    elif requested == 2:
                        self.recRatSignal.emit(float(packet[:8]),
                                               [b'ml/mn', b'ul/mn', b'ml/hr', b'ul/hr'].index(bytes(packet[9:])))
                    elif requested == 3:
                        self.recTarSignal.emit(float(bytes(packet)))
                elif in_packet:
                    packet.extend(byte)


if __name__ == "__main__":
    """
    Main to run Pump in standalone.
    """
    import sys

    # Define app.
    app = QtWidgets.QApplication(sys.argv)

    # Create pump widget.
    wid = WidgetPump()

    # Show window.
    wid.show()

    # Run GUI loop.
    sys.exit(app.exec_())
