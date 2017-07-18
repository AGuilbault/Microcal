import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from WidgetPID import Ui_WidgetPID

import random


class WidgetPID(QtWidgets.QWidget, Ui_WidgetPID):
    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Create figure to display temperature.
        self.figure = plt.figure()
        # Canvas widget to display figure.
        self.canvas = FigureCanvas(self.figure)
        # Create toolbar widget.
        self.toolbar = NavigationToolbar(self.canvas, self.wid_graph)
        # Set the layout.
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.wid_graph.setLayout(self.layout)

        self.data_x = list()
        self.data_y = list()

        # Add axis.
        self.ax = self.figure.add_subplot(111)
        self.line_temp, = self.ax.plot(self.data_x, self.data_y, 'r-')

        # Add setpoint line.
        self.line_set = self.ax.axhline(y=self.spin_setpoint.value(), c='0.5', ls=':')

        # Start a timer for graph.
        self.timer = QtCore.QElapsedTimer()
        self.timer.start()

        self.btn_clear.clicked.connect(self.clear_chart)
        self.btn_start.clicked.connect(self.start)
        self.spin_setpoint.valueChanged.connect(self.setpoint_changed)

        self.label_status.setText('⏹ Off')
        self.controlling = False

    def start(self):
        if self.controlling:
            self.label_status.setText('⏹ Off')
            self.btn_start.setText('Start')
            self.controlling = False
        else:
            self.label_status.setText('▶ On')
            self.btn_start.setText('Stop')
            self.controlling = True

    def update_pid(self):
        self.data_x.append(self.timer.elapsed()/1000.0)
        self.data_y.append(10*random.random()+20)
        self.line_temp.set_data(self.data_x, self.data_y)
        self.rescale()

    def clear_chart(self):
        self.data_x.clear()
        self.data_y.clear()
        self.timer.restart()
        self.rescale()

    def setpoint_changed(self):
        self.line_set.set_ydata(self.spin_setpoint.value())
        self.rescale()

    def rescale(self):
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.ax.autoscale(enable=True)
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    # Define app.
    app = QtWidgets.QApplication(sys.argv)

    # Create pid widget.
    wid = WidgetPID()

    # Show window.
    wid.show()
    wid.setWindowTitle('Temperature control')
    wid.setMinimumSize(wid.minimumSizeHint())

    timer = QtCore.QTimer()
    timer.setInterval(200)
    timer.timeout.connect(wid.update_pid)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
