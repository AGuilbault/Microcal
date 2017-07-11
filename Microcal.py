from Pump import WidgetPump, WidgetPumpCtrl
from Nanovolt import WidgetNanoVolt

from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create pump widgets
    wid = WidgetPump()
    ctrl_wid = WidgetPumpCtrl(wid)

    nvolt_wid = WidgetNanoVolt()

    group = QtWidgets.QGroupBox()
    group.setTitle('Syringe pump')
    group.setLayout(ctrl_wid.layout())
    # group.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    group.setMaximumHeight(group.sizeHint().height())

    # Add widgets to tab.
    tab.addTab(group, 'Main tab')
    tab.addTab(wid, 'PHD2000')
    tab.addTab(nvolt_wid, '2182A')

    # Show window.
    tab.show()

    tab.setWindowTitle('Microcal station')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Run GUI loop.
    sys.exit(app.exec_())
