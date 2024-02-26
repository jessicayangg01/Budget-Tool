from budgetReader import budgetReader
from dataAnalysis import dataAnalysis


readBudget = budgetReader("DummyData.csv")
readBudget.dataClean()



# analyzeBudget = dataAnalysis(readBudget)
# analyzeBudget.plot()
