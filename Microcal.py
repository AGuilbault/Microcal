import matplotlib.pyplot as plt
import visa
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import WidgetMain
from TempControl import WidgetPID
from Nanovolt import WidgetNanovolt
from Pump import WidgetPump


class WidgetMain(QtWidgets.QWidget, WidgetMain.Ui_Form):
    def __init__(self):
        # Initialise overloaded classes.
        super().__init__()
        self.setupUi(self)

        # Create widgets
        self.wid_pump = WidgetPump()
        self.wid_nvolt = WidgetNanovolt(visa.ResourceManager())
        self.wid_pid = WidgetPID()

        # Add widgets to main.
        self.group_pump.setLayout(self.wid_pump.layout())
        self.group_nvolt.setLayout(self.wid_nvolt.layout())

        # Create tabwidget
        self.tab = QtWidgets.QTabWidget()
        # Add widgets to tab.
        self.tab.addTab(self, 'Main tab')
        self.tab.addTab(self.wid_pid, 'PID')

        ''' Figure '''
        # Create figure to display temperature.
        self.figure = plt.figure()
        # Create canvas widget to display figure.
        self.canvas = FigureCanvas(self.figure)
        # Create toolbar widget.
        self.toolbar = NavigationToolbar(self.canvas, self.group_graph)
        # Set the layout.
        self.layout_graph.insertWidget(0, self.toolbar)
        self.layout_graph.insertWidget(1, self.canvas)

        # Create empty data lists for graph.
        self.data_x = list()
        self.data_y = list()

        # Add axis.
        self.ax = self.figure.add_subplot(111)

        # Add temperature line.
        self.line_temp, = self.ax.plot(self.data_x, self.data_y, c='b', ls='-')

        self.elapsed = QtCore.QElapsedTimer()
        self.elapsed.start()
        ''' End figure '''

        # Create timer.
        self.timer = QtCore.QTimer()
        # Set interval from the spin box.
        self.timer.setInterval(self.spin_interval.value())
        # If interval changed in spin box, update timer interval.
        self.spin_interval.valueChanged.connect(self.timer.setInterval)
        # At timeout, update pid and graph.
        self.timer.timeout.connect(self.wid_pid.worker.update)
        self.timer.timeout.connect(self.update_graph)
        # Start timer.
        self.timer.start()

        # Open file browser.
        self.btn_browse.clicked.connect(self.browse)
        # Start or stop recording when button pushed.
        self.btn_record.clicked.connect(self.record)

        # Init empty csv file variable.
        self.csvfile = None

    def browse(self):
        # Open file save dialog.
        filename, ext = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 'C:\\', 'CSV files (*.csv)')
        # If file selected.
        if filename != '':
            # Update path in text box.
            self.edit_path.setText(filename)

    def record(self):
        # If file is not open.
        if self.csvfile is None or self.csvfile.closed:
            try:
                self.csvfile = open(self.edit_path.text(), mode='w+t')
                self.edit_path.setEnabled(False)
                self.btn_record.setText('Stop')
                self.lbl_status.setText('Recording')
            except IOError as e:
                QtWidgets.QMessageBox.critical(self, 'Error', e.strerror)
        # If file is open.
        else:
            # Close the file.
            self.csvfile.close()
            self.edit_path.setEnabled(True)
            self.btn_record.setText('Save')
            self.lbl_status.setText('Not recording')

    def update_graph(self):
        # Append timestamp.
        self.data_x.append(self.elapsed.elapsed() / 1000)
        # Append nVolt reading.
        self.data_y.append(self.wid_nvolt.fetch())
        # Update plot.
        self.line_temp.set_data(self.data_x, self.data_y)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.ax.autoscale(enable=True)
        self.canvas.draw()
        self.toolbar.update()
        # Append to csv file if open.
        if self.csvfile is not None and not self.csvfile.closed:
            self.csvfile.write('{0:.3f}, {1}\n'.format(self.data_x[-1], self.data_y[-1]))
            self.csvfile.flush()
            self.lbl_status.setText((self.lbl_status.text() + '.').replace('....', ''))


if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widgets
    main = WidgetMain()

    # Show window.
    mainwind = QtWidgets.QMainWindow()
    mainwind.setCentralWidget(main.tab)

    # Set window title.
    mainwind.setWindowTitle('Microcal station')
    mainwind.setMinimumSize(mainwind.minimumSizeHint())

    # Show window.
    mainwind.show()

    # Run GUI loop.
    sys.exit(app.exec_())
