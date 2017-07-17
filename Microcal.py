import random

import matplotlib.pyplot as plt
import visa
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import WidgetMain
import WidgetPID
from Nanovolt import WidgetNanoVolt
from Pump import WidgetPump, WidgetPumpCtrl


def plot():
    ''' plot some random stuff '''
    # random data
    data = [random.random() for i in range(100)]

    # instead of ax.hold(False)
    figure.clear()

    # create an axis
    ax = figure.add_subplot(111)

    # discards the old graph
    # ax.hold(False) # deprecated, see above

    # plot data
    ax.plot(data, '+-')

    # refresh canvas
    canvas.draw()

if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create tabwidget
    tab = QtWidgets.QTabWidget()

    # Create pump widgets
    wid = WidgetPump()
    ctrl_wid = WidgetPumpCtrl(wid)

    nvolt_wid = WidgetNanoVolt(visa.ResourceManager())

    pid_wid = QtWidgets.QWidget()
    pid = WidgetPID.Ui_Form()
    pid.setupUi(pid_wid)

    # a figure instance to plot on
    figure = plt.figure()

    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    canvas = FigureCanvas(figure)

    # this is the Navigation widget
    # it takes the Canvas widget and a parent
    toolbar = NavigationToolbar(canvas, pid.widget)

    # set the layout
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(canvas)
    pid.widget.setLayout(layout)

    pid.pushButton_2.clicked.connect(plot)

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

    # Run GUI loop.
    sys.exit(app.exec_())
