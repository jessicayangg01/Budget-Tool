import pandas as pd

class budgetReader(object):
    def __init__(self, fileName):
        self.data = pd.read_csv(fileName)
        print(self.data)
        self.dataDict = self.data.to_dict("list")
        print("----------------------------")
    
    def getCol(self):
        return self.data.columns
    
    def dataClean(self):
        print("________________________________________________________ ")
        print("Data cleaning ... ")
        for col in self.dataDict:
            if not isinstance(self.dataDict[col][0], float):
                print(col, " is a ", type(self.dataDict[col][0]), ". Data cleaning will assign integer values to each variable.")
                variables = set(self.dataDict[col])
                changeVar = {}

                for index, var in enumerate(variables, 1):
                    changeVar[var] = index
                    print(var, " will be assigned to the numeric value of : ", index)

                # self.dataDict[col] = self.dataDict[col].map(changeVar)
                # self.dataDict = self.dataDict.map(changeVar)
                for val in range(len(self.dataDict[col])):
                    self.dataDict[col][val] = changeVar[self.dataDict[col][val]]
        
        # for i in self.dataDict:
        #     print(i)
        #     print(self.dataDict[i][0])
        print("Data finished cleaning.")

