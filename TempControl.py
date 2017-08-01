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

        # Connect slots.
        self.btn_clear.clicked.connect(self.clear_chart)
        self.btn_start.clicked.connect(self.start)

        # Init status.
        self.label_status.setText('Off')
        self.ico_status.setPixmap(QtGui.QPixmap())
        self.controlling = False

        # Start thread.
        self.thread = QtCore.QThread()
        self.worker = CDAQThread()
        self.worker.moveToThread(self.thread)
        self.worker.updated.connect(self.updated)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.start)
        self.thread.start()

    def start(self):
        if self.controlling:
            # Update GUI.
            self.label_status.setText('Off')
            self.ico_status.setPixmap(QtGui.QPixmap())
            self.btn_start.setText('Start')

            # Update state.
            self.controlling = False
            self.worker.toogle_pid(False)
        else:
            # Update GUI.
            self.label_status.setText('On')
            self.ico_status.setPixmap(QtGui.QPixmap(".\\ico\\tick_red.png"))
            self.btn_start.setText('Stop')

            # Update state.
            self.controlling = True
            self.worker.toogle_pid(True)

    @QtCore.pyqtSlot(list, list)
    def updated(self, names, values):

        self.tableWidget.setRowCount(len(names))
        for i in range(len(names)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(names[i]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('{:0.5f}'.format(values[i])))

        self.data_x.append(self.timer.elapsed()/1000.0)
        self.data_y.append(values[0])
        self.data_p.append(values[-1])
        if self.controlling:
            self.data_s.append(self.spin_setpoint.value())
        else:
            self.data_s.append(np.nan)

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

    def rescale(self):
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.ax.autoscale(enable=True)
        self.canvas.draw()
        self.toolbar.update()


class CDAQThread(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    updated = QtCore.pyqtSignal(list, list)

    @QtCore.pyqtSlot()
    def start(self):
        # Init request flag.
        self.request = False
        self.controlling = False
        self.alive = True

        # Start a timer for PID.
        self.timer = QtCore.QElapsedTimer()
        self.timer.start()

        # Init PID.
        self.pid = PID(timestamp=self.timer.elapsed(), max_out=60.0)

        # Load tasks from NI-MAX.
        self.task_ai = nidaqmx.system.storage.persisted_task.PersistedTask('TaskTemp').load()
        self.task_co = nidaqmx.system.storage.persisted_task.PersistedTask('TaskPow').load()
        self.task_do = nidaqmx.system.storage.persisted_task.PersistedTask('TaskDir').load()

        # Start tasks.
        try:
            self.task_ai.start()
            self.task_do.control(nidaqmx.constants.TaskMode.TASK_RESERVE)
            self.task_co.control(nidaqmx.constants.TaskMode.TASK_RESERVE)
            self.task_do.start()
            self.task_co.start()
        except Exception as err:
            print(err)

    @QtCore.pyqtSlot()
    def stop(self):
        # Stop tasks.
        self.task_ai.stop()
        self.task_co.stop()
        self.task_do.stop()
        self.task_do.control(nidaqmx.constants.TaskMode.TASK_UNRESERVE)
        self.task_co.control(nidaqmx.constants.TaskMode.TASK_UNRESERVE)

        self.finished.emit()

    @QtCore.pyqtSlot()
    def update(self):
        # Read the input.
        names = self.task_ai.channel_names + ['Peltier']
        values = self.task_ai.read()

        # Update pid.
        if self.controlling:
            out = self.pid.update(values[0], self.timer.elapsed())
        else:
            out = np.nan

        # Write the output.
        try:
            if out is not np.nan:
                self.task_co.write(nidaqmx.types.CtrTime(abs(out) / 100000, 0.001 - abs(out) / 100000))
                self.task_do.write([out > 0, out != 0])
            else:
                self.task_co.write(nidaqmx.types.CtrTime(0, 0.001))
                self.task_do.write([False, False])
        except Exception as err:
            print(err)

        # Return inputs and ouputs.
        self.updated.emit(names, values + [out])

    @QtCore.pyqtSlot(bool)
    def toogle_pid(self, controlling):
        self.controlling = controlling

    @QtCore.pyqtSlot(float)
    def set_point(self, set_p):
        self.pid.set_point(set_p)

    @QtCore.pyqtSlot(float)
    def set_kp(self, proportional_gain):
        self.pid.set_kp(proportional_gain)

    @QtCore.pyqtSlot(float)
    def set_ti(self, integral_gain):
        self.pid.set_ti(integral_gain)

    @QtCore.pyqtSlot(float)
    def set_td(self, derivative_gain):
        self.pid.set_td(derivative_gain)


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
    timer.timeout.connect(wid.worker.update)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
