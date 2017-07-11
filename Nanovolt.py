from WidgetNanoVolt import Ui_WidgetNanoVolt

from PyQt5 import QtCore, QtWidgets
import visa


class WidgetNanoVolt(QtWidgets.QWidget, Ui_WidgetNanoVolt):
    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        rm = visa.ResourceManager()
        rm.list_resources()

        # List ports.
        for t in rm.list_resources():
            self.list_port.addItem(t)


# nvolt = rm.open_resource('GPIB0::7::INSTR')

# nvolt.write(':TRAC:FEED:CONT NEXT')
# print(nvolt.query(':TRAC:FEED:CONT NEXT ; :TRAC:DATA?'))
