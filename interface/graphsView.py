import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class GraphsView(object):
    def __init__(self):
        axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
        self.button1 = Button(axcut, 'YES', color='red', hovercolor='green')
        self.button1.on_clicked(self._yes)
        plt.show()


    def showGraph(self, graph, subplot, title):
        plt.subplot(subplot)
        # plot = plt.subplot2grid(location1, location2, rowspan= rowSpan, colspan=colSpan) 
        plt.plot(graph) 
        plt.xlabel(title) 


    # def showWindow(self):
        # plt.show()

    
    def _yes(self, event):
        print("button clicked")