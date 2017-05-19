from WidgetPump import Ui_WidgetPump
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import serial
from serial.tools import list_ports


class WidgetPump(QtWidgets.QWidget, Ui_WidgetPump):
    def __init__(self):
        # Initialise overloaded classes.
        super(QtWidgets.QWidget, self).__init__()
        super(Ui_WidgetPump, self).__init__()
        self.setupUi(self)

        # Define serial thread.
        self.protocol = SerialThread()

        # List ports.
        for t in serial.tools.list_ports.comports():
            self.list_port.addItem(t.device)

        # Connect slots.
        self.btn_conn.clicked.connect(self.connect)
        self.list_port.currentItemChanged.connect(self.update_status)
        self.list_baud.currentItemChanged.connect(self.update_status)
        self.protocol.updateSignal.connect(self.update_status)

        # Update GUI.
        self.update_status()

    # Open or close serial port.
    def connect(self):
        # Open if not already open.
        if not self.protocol.state:
            self.protocol.open(self.list_port.currentItem().text(), self.list_baud.currentItem().text())
        # Close it if open.
        else:
            self.protocol.close()

    def update_status(self):
        # Open if not already open.
        if not self.protocol.state:
            self.btn_conn.setText('Connect')
            self.btn_conn.setEnabled(self.list_port.currentItem() is not None and
                                     self.list_baud.currentItem() is not None)
            self.list_port.setEnabled(True)
            self.list_baud.setEnabled(True)
            self.label_port.setText('')
            self.label_baud.setText('')
        # Close it if open.
        else:
            self.btn_conn.setText('Disconnect')
            self.btn_conn.setEnabled(True)
            self.list_port.setEnabled(False)
            self.list_baud.setEnabled(False)
            self.label_port.setText(self.list_port.currentItem().text())
            self.label_baud.setText(self.list_baud.currentItem().text())


class SerialThread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal()

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
        super(QtCore.QThread, self).__init__()

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

    def is_open(self):
        # Check if not disconnected (open).
        return self.state is not SerialThread.DISCONNECTED

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
        self._req.mmd = True

    def get_rate(self):
        self._req.mlm = True

    def get_target(self):
        self._req.mlt = True

    """ Thread execution loop. """
    def run(self):
        # Send update signal (connected).
        self.updateSignal.emit()

        # Init variables.
        error = None
        packet = bytearray()
        in_packet = False

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
                        self._req.run = False
                        in_packet = False
                    elif byte == b'*':
                        self.updateSignal.emit()
                        self.state = self.STALLED
                        self._req.stp = False
                        in_packet = False
                    elif byte == b'\r':
                        in_packet = False
                        self.handle_packet(bytes(packet))  # make read-only copy
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
                elif self._req.dia:
                    self.ser.write(b'DIA\r')
                    self._req.dia = False
                elif self._req.rat:
                    self.ser.write(b'RAT\r')
                    self._req.rat = False
                elif self._req.tar:
                    self.ser.write(b'TAR\r')
                    self._req.tar = False
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


def update_button():
    if wid.protocol.state == wid.protocol.STOPPED:
        btn_inject.setEnabled(True)
        btn_inject.setText('Infuse')
        lbl_state.setText('Stopped')
    elif wid.protocol.state == wid.protocol.FORWARD:
        btn_inject.setEnabled(True)
        btn_inject.setText('Stop')
        lbl_state.setText('Running')
    elif wid.protocol.state == wid.protocol.STALLED:
        btn_inject.setEnabled(True)
        btn_inject.setText('Re-infuse')
        lbl_state.setText('Stalled')
    else:
        btn_inject.setEnabled(False)
        btn_inject.setText('Infuse')
        lbl_state.setText('Disconnected')


def button_action():
    if wid.protocol.state == wid.protocol.STOPPED:
        wid.protocol.send_run()
    elif wid.protocol.state == wid.protocol.FORWARD:
        wid.protocol.send_stp()
    elif wid.protocol.state == wid.protocol.STALLED:
        wid.protocol.send_run()

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create pump widget
    wid = WidgetPump()
    wid.protocol.updateSignal.connect(update_button)

    ctrl_wid = QtWidgets.QWidget()
    gridLayout = QtWidgets.QGridLayout(ctrl_wid)

    lbl_state = QtWidgets.QLabel(ctrl_wid)
    btn_inject = QtWidgets.QPushButton(ctrl_wid)
    btn_inject.clicked.connect(button_action)
    update_button()

    gridLayout.addWidget(lbl_state, 0, 0, 1, 1)
    gridLayout.addWidget(btn_inject, 1, 0, 1, 1)

    # Add widgets to tab.
    tab.addTab(wid, 'Pump')
    tab.addTab(ctrl_wid, 'Ctrl')

    # Show window.
    tab.show()

    tab.setWindowTitle('PHD2000 control')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Run GUI loop.
    sys.exit(app.exec_())
