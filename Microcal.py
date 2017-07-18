import random

import matplotlib.pyplot as plt
import visa
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import WidgetMain
from TempControl import WidgetPID
from Nanovolt import WidgetNanoVolt
from Pump import WidgetPump, WidgetPumpCtrl

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create widgets
    wid = WidgetPump()
    ctrl_wid = WidgetPumpCtrl(wid)

    nvolt_wid = WidgetNanoVolt(visa.ResourceManager())

    pid_wid = WidgetPID()

    main_wid = QtWidgets.QWidget()
    main = WidgetMain.Ui_Form()
    main.setupUi(main_wid)

    main.widget_syringe.setLayout(ctrl_wid.layout())

    # Add widgets to tab.
    tab.addTab(main_wid, 'Main tab')
    tab.addTab(wid, 'PHD2000')
    tab.addTab(nvolt_wid, '2182A')
    tab.addTab(pid_wid, 'PID')

    # Show window.
    tab.show()

    tab.setWindowTitle('Microcal station')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(500)
    timer.timeout.connect(pid_wid.update_pid)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
