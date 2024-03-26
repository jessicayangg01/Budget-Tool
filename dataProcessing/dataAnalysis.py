# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats
import dataProcessing.datasets as datasets 
from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm
import logging

class dataAnalysis(object):
    def __init__(self, data: datasets):
        self.data = data

    def linearRegression(self, col):
        Y = np.array(self.budgetReader.data["Sales"])
        X = np.array(self.budgetReader.data[col]).reshape((-1, 1))

        model = LinearRegression().fit(X, Y)
        values = {}
        values["slope"] = model.coef_[0]
        values["intercept"] = model.intercept_
        values["r squared"] = model.score(X, Y)
        
        

        return values

    def getXForRegression(self, col):
        return self.data.data[[i for i in self.data.data if i!=col]]

    def getYForRegression(self, col ):
        return self.data.data[col]

    def Predict(self, predict_data, col):
        logging.info(f"Predicting {col}")
        x, y = self.getXForRegression(col), self.getYForRegression(col)
        model = LinearRegression().fit(x, y)

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