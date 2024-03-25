
from interface.graphsView import GraphsView
from dataProcessing.budgetReader import budgetReader



graphView = GraphsView()
file = budgetReader("./assets/DummyData.csv")
graphView.plot()