import matplotlib.pyplot as plt
import visa
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import WidgetMain
from TempControl import WidgetPID
from Nanovolt import WidgetNanovolt
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
    wid_nvolt = WidgetNanovolt(visa.ResourceManager())

    pid_wid = WidgetPID()

    main_wid = QtWidgets.QWidget()
    main = WidgetMain.Ui_Form()
    main.setupUi(main_wid)

    main.group_pump.setLayout(wid_pump.layout())
    main.group_nvolt.setLayout(wid_nvolt.layout())

    # Add widgets to tab.
    tab.addTab(main_wid, 'Main tab')
    tab.addTab(pid_wid, 'PID')

    ''' Figure '''
    # Create figure to display temperature.
    figure = plt.figure()
    # Create canvas widget to display figure.
    canvas = FigureCanvas(figure)
    # Create toolbar widget.
    toolbar = NavigationToolbar(canvas, main.widget_2)
    # Set the layout.
    layout_graph = QtWidgets.QVBoxLayout()
    layout_graph.addWidget(toolbar)
    layout_graph.addWidget(canvas)
    main.widget_2.setLayout(layout_graph)

    # Create empty data lists for graph.
    data_x = list()
    data_y = list()

    # Add axis.
    ax = figure.add_subplot(111)

    # Add temperature line.
    line_temp, = ax.plot(data_x, data_y, c='b', ls='-')

    elapsed = QtCore.QElapsedTimer()
    elapsed.start()
    ''' End figure '''

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(main.spinBox.value())
    main.spinBox.valueChanged.connect(change_interval)
    timer.timeout.connect(pid_wid.update_pid)

    def update_graph():
        data_x.append(elapsed.elapsed()/1000)
        data_y.append(wid_nvolt.fetch())
        line_temp.set_data(data_x, data_y)
        ax.relim()
        ax.autoscale_view(True, True, True)
        ax.autoscale(enable=True)
        canvas.draw()
        toolbar.update()
    timer.timeout.connect(update_graph)
    timer.start()

    # Show window.
    tab.show()

    tab.setWindowTitle('Microcal station')
    tab.setMinimumSize(tab.minimumSizeHint())

    # Run GUI loop.
    sys.exit(app.exec_())
