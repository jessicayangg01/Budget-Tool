
# add the plots
import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        # axes
        self.axes = fig.add_subplot(111) # 111 is the number of axes
        self.axes.plot()
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class StaticCanvas(Canvas):
    """Simple canvas with a sine plot."""
    def update_figure(self, f): # change the input
        self.axes.cla()
        # t = np.arange(0.2, 3.0, 0.01)
        # s = np.sin(f*np.pi*t)
        x = [1,2,3,4]
        y = [1,2,3,4]
        self.axes.plot(x, y)
        self.draw()


