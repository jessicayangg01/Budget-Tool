from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets


assets.load_dataFiles()


# maybe add a way you can add multiple files
readBudget = budgetReader(assets.get_dataFile("DummyData"))
readBudget.dataClean()


analyzeBudget = dataAnalysis(readBudget)
analyzeBudget.plot()


from interface.graphsView import GraphsView


window = GraphsView()

graph = [1,2,3]
# window.showGraph(graph, 221, "hi")
# window.showGraph([2,2,2], 222, "bye")