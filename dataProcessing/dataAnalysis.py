# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats

from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm

class dataAnalysis(object):
    def __init__(self, budgetReader):
        self.budgetReader = budgetReader

    # def plot(self):
    #     for i in self.budgetReader.getCol():
    #         print(i)

    #     # plt.scatter(
    #     #     x = self.budgetReader.dataDict["TV"],
    #     #     y = self.budgetReader.dataDict["Sales"],
    #     #     )
        


    #     # window.showWindow()
            
        
    

    def randomForest(self):

        # exclude
        # exclude_keys = ['Sales']
        # X = [value for key, value in self.budgetReader.dataDict.items() if key not in exclude_keys]

        # Split the data into features (X) and target (y)
        X = self.budgetReader.data.drop('Sales', axis=1).reshape(-1, 1)
        Y = self.budgetReader.data["Sales"]

        # Split the data into training and test sets

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        rf = RandomForestClassifier()
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)  
        #https://www.statology.org/valueerror-unknown-label-type-continuous/
        # Note that this doesnt work because Sales value is continuous  

        return
    
    def linearRegression(self, col):
        X = np.array(self.budgetReader.data["Sales"]).reshape((-1, 1))
        # .reshape((1, -1))      

        # predictor
        Y = np.array(self.budgetReader.data[col])
        # slope, intercept, r, p, std_err = stats.linregress(X, Y)

        # values = {}
        # values["slope"] = slope
        # values["intercept"] = intercept
        # values["r"] = r
        # values["p"] = p
        # values["standard error"] = std_err
        
        # return values

        model = LinearRegression().fit(X, Y)
        r_sq = model.score(X, Y)


        X2 = sm.add_constant(X)
        est = sm.OLS(Y, X2)
        est2 = est.fit()
        # print(est2.summary())
        
        

        values = {}
        values["slope"] = model.coef_[0]
        values["intercept"] = model.intercept_
        values["r squared"] = r_sq

        return values

    def predict(self):
        return