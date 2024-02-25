from budgetReader import budgetReader
from dataAnalysis import dataAnalysis


readBudget = budgetReader("DummyData.csv")
columns = readBudget.getCol()
for i in columns:
    print(i)
    
analyzeBudget = dataAnalysis(readBudget)
analyzeBudget.plot()
