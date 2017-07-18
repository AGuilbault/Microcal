import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from WidgetPID import Ui_WidgetPID

import random
from PID import PID


class WidgetPID(QtWidgets.QWidget, Ui_WidgetPID):
    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Create figure to display temperature.
        self.figure = plt.figure()
        # Create canvas widget to display figure.
        self.canvas = FigureCanvas(self.figure)
        # Create toolbar widget.
        self.toolbar = NavigationToolbar(self.canvas, self.wid_graph)
        # Set the layout.
        self.layout_graph = QtWidgets.QVBoxLayout()
        self.layout_graph.addWidget(self.toolbar)
        self.layout_graph.addWidget(self.canvas)
        self.wid_graph.setLayout(self.layout_graph)

        # Create empty data lists for graph.
        self.data_x = list()
        self.data_y = list()
        self.data_s = list()

        # Add axis.
        self.ax = self.figure.add_subplot(111)

        # Add temperature line.
        self.line_temp, = self.ax.plot(self.data_x, self.data_y, c='r', ls='-')

        # Add setpoint line.
        self.line_set, = self.ax.plot(self.data_x, self.data_s, c='0.5', ls=':')

        # Start a timer for PID and graph.
        self.timer = QtCore.QElapsedTimer()
        self.timer.start()

        # Init PID.
        self.pid = PID(timestamp=self.timer.elapsed(),
                       k_p=self.spin_kc.value(),
                       t_i=self.spin_ti.value(),
                       t_d=self.spin_td.value(),
                       max_out=100.0)

        # Connect slots.
        self.btn_clear.clicked.connect(self.clear_chart)
        self.btn_start.clicked.connect(self.start)

        self.spin_setpoint.valueChanged.connect(self.setpoint_changed)

        # Init status.
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
            self.pid.clear(self.timer.elapsed())

    def update_pid(self):
        reading = 10*random.random()+20
        self.data_x.append(self.timer.elapsed()/1000.0)
        self.data_y.append(reading)
        if self.controlling:
            self.data_s.append(self.spin_setpoint.value())
            self.pid.update(reading, self.timer.elapsed())
        else:
            self.data_s.append(np.nan)

        self.line_temp.set_data(self.data_x, self.data_y)
        self.line_set.set_data(self.data_x, self.data_s)
        self.rescale()

    def clear_chart(self):
        self.data_x.clear()
        self.data_y.clear()
        self.data_s.clear()
        self.timer.restart()
        self.rescale()

    def setpoint_changed(self):
        self.pid.set_point(self.spin_setpoint.value())

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

    # Create timer.
    timer = QtCore.QTimer()
    timer.setInterval(500)
    timer.timeout.connect(wid.update_pid)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
