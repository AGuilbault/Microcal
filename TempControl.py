"""
Module controls cDAQ system and PID.
Can be executed as standalone or imported to be used as a widget.
"""
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PID import PID
from WidgetPID import Ui_WidgetPID

import time


class WidgetPID(QtWidgets.QWidget, Ui_WidgetPID):
    """
    Widget used to display cDAQ values and control the temperature PID settings. Uses CDAQThread class to control the
    cDAQ and update the PID. UI (WidgetPID.ui) made in Qt Designer and converted using pyuic5 command.
    """

    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Create figure and axes.
        # 2 axes with common x axis.
        # Temperature subplot 3 times bigger than output subplot.
        self.figure, (self.ax, self.ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
        self.ax.set_ylabel('Temperature')
        self.ax2.set_ylabel('Output')
        # Create canvas widget to display figure.
        self.canvas = FigureCanvas(self.figure)
        # Create toolbar widget.
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Insert in the layout.
        self.layout_graph.insertWidget(0, self.toolbar)
        self.layout_graph.insertWidget(1, self.canvas)

        # Create empty data lists for graph values.
        self.data_x = list()
        self.data_temp = list()
        self.data_set = list()
        self.data_pid = list()

        # Add lines.
        self.line_temp, = self.ax.plot(self.data_x, self.data_temp, c='r', ls='-')
        self.line_set, = self.ax.plot(self.data_x, self.data_set, c='0.5', ls=':')
        self.line_pid, = self.ax2.plot(self.data_x, self.data_pid, c='g', ls='-')

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
        self.destroyed.connect(self.worker.stop)
        self.thread.started.connect(self.worker.start)
        self.thread.start()

        # Connect signals and slots.
        self.spin_setpoint.valueChanged.connect(self.worker.set_point)
        self.spin_kc.valueChanged.connect(self.worker.set_kp)
        self.spin_ti.valueChanged.connect(self.worker.set_ti)
        self.spin_td.valueChanged.connect(self.worker.set_td)
        self.spin_max.valueChanged.connect(self.worker.set_max)

        # Initialize PID settings using the spinbox signals.
        self.spin_setpoint.setValue(self.spin_setpoint.value())
        self.spin_kc.setValue(self.spin_kc.value())
        self.spin_ti.setValue(self.spin_ti.value())
        self.spin_td.setValue(self.spin_td.value())
        self.spin_max.setValue(self.spin_max.value())

    @QtCore.pyqtSlot()
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

    @QtCore.pyqtSlot(list, list, list)
    def updated(self, names, values, units):
        # Update table widget.
        self.tableWidget.setRowCount(len(names))
        for i in range(len(names)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(names[i]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem('{:0.5f} {}'.format(values[i], units[i])))

        # Append values.
        self.data_x.append(time.time())
        self.data_temp.append(values[0])
        self.data_pid.append(values[-1])
        if self.controlling:
            self.data_set.append(self.spin_setpoint.value())
        else:
            self.data_set.append(np.nan)

        # Update graph.
        self.line_temp.set_data(self.data_x, self.data_temp)
        self.line_set.set_data(self.data_x, self.data_set)
        self.line_pid.set_data(self.data_x, self.data_pid)
        self.rescale()

    @QtCore.pyqtSlot()
    def clear_chart(self):
        # Clear all the graph data.
        self.data_x.clear()
        self.data_temp.clear()
        self.data_set.clear()
        self.data_pid.clear()

        # Update scale.
        self.rescale()

    def rescale(self):
        # Update limits.
        self.ax.relim()
        # Autoscale axes.
        self.ax.autoscale(enable=self.check_autox.isChecked(), axis='x')
        self.ax.autoscale(enable=self.check_autoy.isChecked(), axis='y')
        if self.check_autoy.isChecked():
            self.ax2.set_ylim(-100, 100)
        # Redraw graph.
        self.canvas.draw()
        # Update toolbar home value.
        self.toolbar.update()


class CDAQThread(QtCore.QObject):
    """
    Thread class. Used to read values from the cDAQ system and control the temperature PID.
    """

    finished = QtCore.pyqtSignal()
    updated = QtCore.pyqtSignal(list, list, list)

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
        self.pid = PID(timestamp=self.timer.elapsed())

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
        # Turn off Peltier.
        self.task_do.write([False, False])

        # Stop tasks.
        self.task_ai.stop()
        self.task_co.stop()
        self.task_do.stop()
        self.task_do.control(nidaqmx.constants.TaskMode.TASK_UNRESERVE)
        self.task_co.control(nidaqmx.constants.TaskMode.TASK_UNRESERVE)

        self.finished.emit()

    @QtCore.pyqtSlot()
    def update(self):
        # Read the names.
        names = self.task_ai.channel_names

        # Read the units. (Big and ugly, but it works.)
        units = ['?'] * len(names)
        for i in range(len(names)):
            chan = nidaqmx._task_modules.channels.ai_channel.AIChannel(self.task_ai._handle, names[i])
            if chan.ai_meas_type == nidaqmx.constants.UsageTypeAI.TEMPERATURE_RTD and \
                    chan.ai_temp_units == nidaqmx.constants.TemperatureUnits.DEG_C:
                units[i] = '°C'
            elif chan.ai_meas_type == nidaqmx.constants.UsageTypeAI.VOLTAGE:
                if chan.ai_voltage_units == nidaqmx.constants.VoltageUnits.FROM_CUSTOM_SCALE:
                    units[i] = chan.ai_custom_scale.scaled_units
                elif chan.ai_voltage_units == nidaqmx.constants.VoltageUnits.VOLTS:
                    units[i] = 'V'
            elif chan.ai_meas_type == nidaqmx.constants.UsageTypeAI.CURRENT and \
                    chan.ai_current_units == nidaqmx.constants.CurrentUnits.AMPS:
                units[i] = 'A'

        # Read the input.
        values = self.task_ai.read()

        # Update pid.
        out = self.pid.update(values[0], self.timer.elapsed()) if self.controlling else 0

        # Write the output.
        try:
            if out != 0:
                # HighTime = Out / (100% * 50kHz)
                high = abs(out) / (100 * 50e3)
                # LowTime = (1 / 50kHz) - HighTime
                low = (1/50e3) - high
                # Write output pwm.
                self.task_co.write(nidaqmx.types.CtrTime(high, low))
                # Write direction and enable.
                self.task_do.write([out > 0, True])
            else:
                # self.task_co.write(nidaqmx.types.CtrTime(0, 0.001))
                self.task_do.write([False, False])
        except Exception as err:
            print(err)

        # Return inputs and ouputs.
        self.updated.emit(names + ['Peltier'], values + [out], units + ['%'])

    """All the slots to update de PID class."""
    @QtCore.pyqtSlot(bool)
    def toogle_pid(self, controlling):
        self.controlling = controlling
        if not controlling:
            self.pid.clear(self.timer.elapsed())

    @QtCore.pyqtSlot(float)
    def set_point(self, set_p):
        self.pid.set_point(set_p)

    @QtCore.pyqtSlot(float)
    def set_kp(self, proportional_gain):
        self.pid.set_kp(proportional_gain)

    @QtCore.pyqtSlot(float)
    def set_ti(self, integral_gain):
        # Convert from s to ms.
        self.pid.set_ti(integral_gain * 1000)

    @QtCore.pyqtSlot(float)
    def set_td(self, derivative_gain):
        # Convert from s to ms.
        self.pid.set_td(derivative_gain * 1000)

    @QtCore.pyqtSlot(float)
    def set_max(self, maximum):
        self.pid.set_guard(maximum)


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
    timer.setInterval(1000)
    timer.timeout.connect(wid.worker.update)
    timer.start()

    # Run GUI loop.
    sys.exit(app.exec_())
