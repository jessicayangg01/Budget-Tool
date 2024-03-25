# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats

from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm

class dataAnalysis(object):
    def __init__(self, budgetReader):
        self.budgetReader = budgetReader

    
    def linearRegression(self, col):
        Y = np.array(self.budgetReader.data["Sales"])
        # .reshape((1, -1))      

        # predictor
        X = np.array(self.budgetReader.data[col]).reshape((-1, 1))
        # slope, intercept, r, p, std_err = stats.linregress(X, Y)

        # values = {}
        # values["slope"] = slope
        # values["intercept"] = intercept
        # values["r"] = r
        # values["p"] = p
        # values["standard error"] = std_err
        
        # return values

        model = LinearRegression().fit(X, Y)
        values = {}
        values["slope"] = model.coef_[0]
        values["intercept"] = model.intercept_
        values["r squared"] = model.score(X, Y)


        # X2 = sm.add_constant(X)
        # est = sm.OLS(Y, X2)
        # est2 = est.fit()
        # print(est2.summary())
        
        

        return values

    def predict(self, predict_data):
        print("predict")
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i!="Sales"]]
        Y = self.budgetReader.data["Sales"]
        print(X)
        model = LinearRegression().fit(X, Y)

        predicted_values = model.predict(predict_data)
        print(predicted_values)
        self.accuracy(0.2)

        return
    
    def accuracy(self, percent):
        Y = self.budgetReader.data["Sales"]
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i!="Sales"]]
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =percent)

        print(x_test)

        model = LinearRegression().fit(x_train, y_train)
        y_pred_test = model.predict(x_test)
        print(y_pred_test)

        print("Mean absolute error =", round(sm.mean_absolute_error(y_test, y_pred_test), 2)) 
        print("Mean squared error =", round(sm.mean_squared_error(y_test, y_pred_test), 2)) 
        print("Median absolute error =", round(sm.median_absolute_error(y_test, y_pred_test), 2)) 
        print("Explain variance score =", round(sm.explained_variance_score(y_test, y_pred_test), 2)) 
        print("R2 score =", round(sm.r2_score(y_test, y_pred_test), 2))
        
        return
    

    # maybe add how to economy is doing with the marketing budget? with stock api?