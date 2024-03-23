import pandas as pd

class budgetReader(object):
    def __init__(self, fileName):
        self.data = pd.read_csv(fileName)
        print(self.data)
        # self.dataDict = self.data.to_dict("list")
        print("Data loaded successfully.")
    
    def getCol(self):
        return self.data.columns

    def numRows(self):
        return len(self.data)
    
    def dataClean(self):
        print("________________________________________________________ ")
        print("Data cleaning ... ")
        
        print(" ")
        print("Taking out None Data")
        old = self.numRows()
        self.data.dropna(subset=self.getCol(), inplace=True)
        print("Removed ", old - self.numRows(), " rows of None Data.")
        print(self.data)
        # self.dataDict = self.data.to_dict("list")

        print(" ")
        print("Assigning numeric values to string variables")
        # for col in self.dataDict:
        #     if not isinstance(self.dataDict[col][0], float):
        #         print(col, " is a ", type(self.dataDict[col][0]), ". Data cleaning will assign integer values to each variable.")
        #         variables = set(self.dataDict[col])
        #         changeVar = {}

        #         for index, var in enumerate(variables, 1):
        #             changeVar[var] = index
        #             print(var, " will be assigned to the numeric value of : ", index)

        #         # self.dataDict[col] = self.dataDict[col].map(changeVar)
        #         # self.dataDict = self.dataDict.map(changeVar)
        #         for val in range(len(self.dataDict[col])):
        #             self.dataDict[col][val] = changeVar[self.dataDict[col][val]]

        for col in self.data:
            if not isinstance(self.data[col][0], float):
                print(col, " is a ", type(self.data[col][0]), ". Data cleaning will assign integer values to each variable.")
                variables = set(self.data[col])
                changeVar = {}

                for index, var in enumerate(variables, 1):
                    changeVar[var] = index
                    print(var, " will be assigned to the numeric value of : ", index)

                self.data = self.data.reset_index()
                for val in range(len(self.data[col])):
                    self.data.loc[val, col] = changeVar[self.data[col][val]]
        
        print("Data finished cleaning.")


    def delCol(self, colName):
        del self.dataDict[colName]
