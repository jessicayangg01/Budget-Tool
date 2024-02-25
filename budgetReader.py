import pandas as pd

class budgetReader(object):
    def __init__(self, fileName):
        self.data = pd.read_csv(fileName)
        print(self.data)
        self.dataDict = self.data.to_dict("list")
        print("----------------------------")
    
    def getCol(self):
        return self.data.columns

