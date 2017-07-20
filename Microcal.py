import matplotlib.pyplot as plt
import visa
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import WidgetMain
from TempControl import WidgetPID
from Nanovolt import WidgetNanoVolt
from Pump import WidgetPump


def change_interval():
    timer.setInterval(main.spinBox.value())

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create widgets
    wid_pump = WidgetPump()

    nvolt_wid = WidgetNanoVolt(visa.ResourceManager())

    pid_wid = WidgetPID()

    main_wid = QtWidgets.QWidget()
    main = WidgetMain.Ui_Form()
    main.setupUi(main_wid)

    main.widget_syringe.setLayout(wid_pump.layout())

    # Add widgets to tab.
    tab.addTab(main_wid, 'Main tab')
    tab.addTab(nvolt_wid, '2182A')
    tab.addTab(pid_wid, 'PID')

    # Show window.
    tab.show()

    tab.setWindowTitle('Microcal station')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(main.spinBox.value())
    main.spinBox.valueChanged.connect(change_interval)
    timer.timeout.connect(pid_wid.update_pid)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
