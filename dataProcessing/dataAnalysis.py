# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats

from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm

class dataAnalysis(object):
    def __init__(self, budgetReader, data_logger):
        self.budgetReader = budgetReader
        self.data_logger = data_logger

    
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
        self.data_logger.addtext("predict")
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i!="Sales"]]
        Y = self.budgetReader.data["Sales"]
        model = LinearRegression().fit(X, Y)

        predicted_values = model.predict(predict_data)

        self.data_logger.addtext(str(predicted_values))
        self.accuracy(0.2)

        return
    
    def accuracy(self, percent):
        Y = self.budgetReader.data["Sales"]
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i!="Sales"]]
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =percent)

        model = LinearRegression().fit(x_train, y_train)
        y_pred_test = model.predict(x_test)


        # self.data_logger.addtext(str(y_pred_test))

        self.data_logger.addtext("Mean absolute error =" + str(round(sm.mean_absolute_error(y_test, y_pred_test), 2))) 
        self.data_logger.addtext("Mean squared error =" + str(round(sm.mean_squared_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Median absolute error =" + str(round(sm.median_absolute_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Explain variance score ="+ str(round(sm.explained_variance_score(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("R2 score ="+ str(round(sm.r2_score(y_test, y_pred_test), 2)))
        
        return
    

    # maybe add how to economy is doing with the marketing budget? with stock api?