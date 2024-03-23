import matplotlib.pyplot as plt
from dataProcessing.dataAnalysis import dataAnalysis



class graph(object):
    def __init__(self, subplot):
        self.graph = plt.subplot(subplot)


    def showGraph(self, graph, title, type):
        # plt.subplot(subplot)
        print("here")
        # plot = plt.subplot2grid(location1, location2, rowspan= rowSpan, colspan=colSpan) 
        # plt.scatter(graph) 
        if type == "scatter":
            self.scatter(x =graph[0], y=graph[1])
        else:
            plt.plot(graph)
        
        # plt.xlabel(title) 
        plt.title(title)
        plt.draw()

    def plot(self, readBudget):
        n=1
        analyzeBudget = dataAnalysis(readBudget)
        for col in readBudget.getCol():
            self.showGraph([readBudget.data["Sales"], readBudget.data[col]], col, "scatter")
            # self.plot(readBudget.data["Radio"], analyzeBudget.linearRegression("Radio"))
            n+=1


