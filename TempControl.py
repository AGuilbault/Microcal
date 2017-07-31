import random
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PID import PID
from WidgetPID import Ui_WidgetPID


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
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Set the layout.
        self.layout_graph.insertWidget(0, self.toolbar)
        self.layout_graph.insertWidget(1, self.canvas)

        # Create empty data lists for graph.
        self.data_x = list()
        self.data_y = list()
        self.data_s = list()
        self.data_p = list()

        # Add axis.
        self.ax = self.figure.add_subplot(111)

        # Add temperature line.
        self.line_temp, = self.ax.plot(self.data_x, self.data_y, c='r', ls='-')
        # Add setpoint line.
        self.line_set, = self.ax.plot(self.data_x, self.data_s, c='0.5', ls=':')
        # Add pid line.
        self.line_pid, = self.ax.plot(self.data_x, self.data_p, c='g', ls='-')

        # Start a timer for PID and graph.
        self.timer = QtCore.QElapsedTimer()
        self.timer.start()

        # Init PID.
        self.pid = PID(timestamp=self.timer.elapsed(),
                       k_p=self.spin_kc.value(),
                       t_i=self.spin_ti.value(),
                       t_d=self.spin_td.value(),
                       max_out=60.0,
                       set_point=self.spin_setpoint.value())

        # Connect slots.
        self.btn_clear.clicked.connect(self.clear_chart)
        self.btn_start.clicked.connect(self.start)

        self.spin_setpoint.valueChanged.connect(self.setpoint_changed)
        self.spin_kc.valueChanged.connect(self.setpoint_changed)
        self.spin_ti.valueChanged.connect(self.setpoint_changed)
        self.spin_td.valueChanged.connect(self.setpoint_changed)

        # Init status.
        self.label_status.setText('Off')
        self.ico_status.setPixmap(QtGui.QPixmap())
        self.controlling = False

        self.task_ai = nidaqmx.system.storage.persisted_task.PersistedTask('TaskTemp').load()

        names = self.task_ai.channel_names
        values = self.task_ai.read()
        length = len(names)

        self.tableWidget.setRowCount(length)

        for i in range(length):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(names[i]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('{:0.5f}'.format(values[i])))

        self.tableWidget.resizeColumnsToContents()

    def start(self):
        if self.controlling:
            self.label_status.setText('Off')
            self.ico_status.setPixmap(QtGui.QPixmap())

            self.btn_start.setText('Start')
            self.controlling = False
        else:
            self.label_status.setText('On')
            self.ico_status.setPixmap(QtGui.QPixmap(".\\ico\\tick_red.png"))

            self.btn_start.setText('Stop')
            self.controlling = True
            self.pid.clear(self.timer.elapsed())

    def update_pid(self):
        values = self.task_ai.read()

        for i in range(len(values)):
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('{:0.5f}'.format(values[i])))

        reading = values[0]
        self.data_x.append(self.timer.elapsed()/1000.0)
        self.data_y.append(reading)
        if self.controlling:
            self.data_s.append(self.spin_setpoint.value())
            out = self.pid.update(reading, self.timer.elapsed())
            self.data_p.append(out)
        else:
            self.data_s.append(np.nan)
            self.data_p.append(np.nan)

        self.line_temp.set_data(self.data_x, self.data_y)
        self.line_set.set_data(self.data_x, self.data_s)
        self.line_pid.set_data(self.data_x, self.data_p)
        self.rescale()

    def clear_chart(self):
        self.data_x.clear()
        self.data_y.clear()
        self.data_s.clear()
        self.data_p.clear()
        # self.timer.restart()
        self.rescale()

    def setpoint_changed(self):
        self.pid.set_point(self.spin_setpoint.value())
        self.pid.set_kp(self.spin_kc.value())
        self.pid.set_ti(self.spin_ti.value())
        self.pid.set_td(self.spin_td.value())

    def rescale(self):
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.ax.autoscale(enable=True)
        self.canvas.draw()
        self.toolbar.update()

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
