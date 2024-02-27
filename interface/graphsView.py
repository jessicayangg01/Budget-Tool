import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist


# other classes
from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets

class GraphsView(object):
    def __init__(self):
        axcut = plt.axes([0.9, 0.0, 0.1, 0.075])
        self.button1 = Button(axcut, 'YES', color='red', hovercolor='green')
        self.button1.on_clicked(self._yes)
        
        # adding text
        text  = plt.text(-5, 0.5, "jessicas text", fontsize = 12)
        text.set_visible(False)
        Artist.set_visible(text, True)
        # Artist.remove(text)


        plt.show()


    def showGraph(self, graph, subplot, title, type):
        plt.subplot(subplot)
        print("here")
        # plot = plt.subplot2grid(location1, location2, rowspan= rowSpan, colspan=colSpan) 
        # plt.scatter(graph) 
        if type == "scatter":
            plt.scatter(x =graph[0], y=graph[1])
        else:
            plt.plot(graph)
        
        # plt.xlabel(title) 
        plt.title(title)
        plt.draw()


    # def showWindow(self):
        # plt.show()
 

    
    def _yes(self, event):
        print("button clicked")
        assets.load_dataFiles()


        # maybe add a way you can add multiple files
        readBudget = budgetReader(assets.get_dataFile("DummyData"))
        readBudget.dataClean()


        analyzeBudget = dataAnalysis(readBudget)
        self.plot(readBudget)
       

        # window = GraphsView()
        # self.showGraph(graph, 221, "hi")
        # self.showGraph([2,2,2], 222, "bye")
    

    def plot(self, readBudget):
        n=1
        for col in readBudget.getCol():
            self.showGraph([ readBudget.dataDict["Sales"], readBudget.dataDict[col]], 330+n, col, "scatter")
            n+=1



