# classes I need
# import myCanvas
from . import myCanvas

# add the plots
import matplotlib
matplotlib.use("Qt5Agg")
# pip install pyqt5
from PyQt5.QtWidgets import QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox
from PyQt5.QtCore import Qt

class ApplicationWindow(QMainWindow):
    def __init__(self):
        # regular settup 
        super().__init__()
        self.setStyleSheet('font-size: 35px;')
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.close, Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)

        # this is the box from 1-10
        # self.spinbox = QSpinBox(minimum=1, maximum=10, singleStep=1, value=1)
        self.spinbox = 1

        # sc = StaticCanvas(self.main_widget)
        sc = myCanvas.StaticCanvas(self.main_widget)


        # self.spinbox.valueChanged.connect(sc.update_figure)
        sc.update_figure(self.spinbox)
        # sc.update_figure(self.spinbox.value())

        # layout.addWidget(self.spinbox)
        
        layout.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)