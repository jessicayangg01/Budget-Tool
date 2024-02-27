import matplotlib.pyplot as plt

# # Modelling
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
# from sklearn.model_selection import RandomizedSearchCV, train_test_split
# from scipy.stats import randint

# # Tree Visualisation
# from sklearn.tree import export_graphviz
# from IPython.display import Image
# import graphviz


class dataAnalysis(object):
    def __init__(self, budgetReader):
        self.budgetReader = budgetReader

    def plot(self):
        for i in self.budgetReader.getCol():
            print(i)

        
        
        plt.scatter(
            x = self.budgetReader.dataDict["TV"],
            y = self.budgetReader.dataDict["Sales"],
            s = self.budgetReader.dataDict["Radio"],
            c = self.budgetReader.dataDict["Social Media"]
            )
        plt.show()
    

    def randomForest(self):
        return
