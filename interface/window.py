import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.artist import Artist

# from dataProcessing.budgetReader import budgetReader
# from dataProcessing.dataAnalysis import dataAnalysis

class window(object):
    def __init__(self, numPlots, title):
        
        self.numRow = numPlots[0]
        self.numCol = numPlots[1]
        self.fig, self.axs = plt.subplots(self.numRow, self.numCol, figsize=(10, 10), subplot_kw=dict())


        # button and stuff
        self.button1 = Button(self.axs, 'YES', color='red', hovercolor='green')
        self.button1.on_clicked(self._yes)
        
        # adding text
        text  = plt.text(-5, 0.5, "jessicas text", fontsize = 12)
        text.set_visible(False)
        Artist.set_visible(text, True)



    def addPlot(self, plot, location):

        plt.axes(self.axs[location[0], location[1]])
        plt.plot(plot[0], plot[1])
        self.fig.canvas.draw()
        plt.show()

        # self.graphs[location] = self.fig.add_subplot(111)
        # self.graphs[location].plot(plot[0], plot[1])
        # self.fig.canvas.draw() 
        # self.fig.canvas.flush_events() 
    
    def updateAxis(self, xaxis_title, yaxis_title, location):
        self.axs[location[0], location[1]].xlabel(xaxis_title)
        self.axs[location[0], location[1]].ylabel(yaxis_title)
    
    def updateTitle(self, title, location):
       self.axs[location[0], location[1]].set_title(title)
        

myView = window([3,3], "jessica")
myView.addPlot([[1,2,3], [1,2,3]], (0,0))
# myView.addPlot([[2,2,3], [1,2,3]], [0,1])
# myView.addPlot([[1,2,3], [1,2,3]], [0,2])
# myView.addPlot([[2,2,3], [1,2,3]], [2,1])
