from budgetReader import budgetReader
from dataAnalysis import dataAnalysis


readBudget = budgetReader("DummyData.csv")
readBudget.dataClean()



# analyzeBudget = dataAnalysis(readBudget)
# analyzeBudget.plot()


# add the plots


import sys
import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox
from PyQt5.QtCore import Qt

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.plot()
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def update_figure(self, f):
        self.axes.cla()
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(f*np.pi*t)
        self.axes.plot(t, s)
        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 35px;')
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.close, Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)

        self.spinbox = QSpinBox(minimum=1, maximum=10, singleStep=1, value=1)

        sc = MyStaticMplCanvas(self.main_widget)

        self.spinbox.valueChanged.connect(sc.update_figure)

        sc.update_figure(self.spinbox.value())

        layout.addWidget(self.spinbox)
        layout.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

app = QApplication(sys.argv)
win = ApplicationWindow()
win.setWindowTitle("Jessica's Thesis")
win.show()
sys.exit(app.exec_())