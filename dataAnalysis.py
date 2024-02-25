import matplotlib.pyplot as plt
from scipy import stats


class dataAnalysis(object):
    def __init__(self, budgetReader):
        self.budgetReader = budgetReader

    def plot(self):
        for i in self.budgetReader.getCol():
            print(i)

        plt.scatter(
            self.budgetReader.dataDict
            )
        return