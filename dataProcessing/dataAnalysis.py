import matplotlib.pyplot as plt
import numpy as np
from interface.graphsView import GraphsView


class dataAnalysis(object):
    def __init__(self, budgetReader):
        self.budgetReader = budgetReader

    def plot(self):
        for i in self.budgetReader.getCol():
            print(i)

        # plt.scatter(
        #     x = self.budgetReader.dataDict["TV"],
        #     y = self.budgetReader.dataDict["Sales"],
        #     )
        


        # graph = [1,2,3]

        # window = GraphsView()
        # window.showGraph(graph, 221, "hi")
        # window.showGraph([2,2,2], 222, "bye")
        # window.showWindow()
    

    def randomForest(self):
        return
