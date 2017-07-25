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

        # Create tabwidget
        self.tab = QtWidgets.QTabWidget()

        # Create widgets
        self.wid_pump = WidgetPump()
        self.group_pump.setLayout(self.wid_pump.layout())

        self.wid_nvolt = WidgetNanovolt(visa.ResourceManager())
        self.group_nvolt.setLayout(self.wid_nvolt.layout())

        self.wid_pid = WidgetPID()

        # Add widgets to tab.
        self.tab.addTab(self, 'Main tab')
        self.tab.addTab(self.wid_pid, 'PID')

        ''' Figure '''
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

        # Add axis.
        self.ax = self.figure.add_subplot(111)

        # Add temperature line.
        self.line_temp, = self.ax.plot(self.data_x, self.data_y, c='b', ls='-')

        self.elapsed = QtCore.QElapsedTimer()
        self.elapsed.start()
        ''' End figure '''

        # Create timer.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.spin_interval.value())
        self.spin_interval.valueChanged.connect(self.change_interval)
        self.timer.timeout.connect(self.wid_pid.update_pid)

        self.timer.timeout.connect(self.update_graph)
        self.timer.start()

        self.btn_browse.clicked.connect(self.browse)
        self.btn_record.clicked.connect(self.record)

    def browse(self):
        filename, ext = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 'C:\\', 'CSV files (*.csv)')
        if filename != '':
            self.edit_path.setText(filename)

    def record(self):
        try:
            csvfile = open(self.edit_path.text(), mode='w+t')
            csvfile.write('Allo')
            csvfile.close()
            self.edit_path.setEnabled(False)
            self.btn_record.setText('Stop')
        except IOError as e:
            QtWidgets.QMessageBox.critical(self, 'Error', e.strerror)

    def change_interval(self):
        self.timer.setInterval(self.spin_interval.value())

    def update_graph(self):
        self.data_x.append(self.elapsed.elapsed() / 1000)
        self.data_y.append(self.wid_nvolt.fetch())
        self.line_temp.set_data(self.data_x, self.data_y)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.ax.autoscale(enable=True)
        self.canvas.draw()
        self.toolbar.update()


if __name__ == "__main__":
    import sys
    # Define app
    app = QtWidgets.QApplication(sys.argv)

    # Create widgets
    main = WidgetMain()

    # Show window.
    mainwind = QtWidgets.QMainWindow()
    mainwind.setCentralWidget(main.tab)

    mainwind.setWindowTitle('Microcal station')
    mainwind.setMinimumSize(mainwind.minimumSizeHint())

    mainwind.show()

    # Run GUI loop.
    sys.exit(app.exec_())
