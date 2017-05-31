from Pump import WidgetPump, WidgetPumpCtrl
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create pump widgets
    wid = WidgetPump()
    ctrl_wid = WidgetPumpCtrl(wid)

    # Add widgets to tab.
    tab.addTab(ctrl_wid, 'Main tab')
    tab.addTab(wid, 'PHD2000')

    # Show window.
    tab.show()

    tab.setWindowTitle('Microcal station')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Run GUI loop.
    sys.exit(app.exec_())
