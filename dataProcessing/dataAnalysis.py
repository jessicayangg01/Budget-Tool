# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats

from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm
import pandas as pd

class dataAnalysis(object):
    def __init__(self, budgetReader, data_logger, event_logger):
        self.budgetReader = budgetReader
        self.data_logger = data_logger
        self.event_logger = event_logger

    
    def linearRegression(self, col):
        try:
            Y = np.array(self.budgetReader.data[self.budgetReader.independent_var])
            X = np.array(self.budgetReader.data[col]).reshape((-1, 1))
            
            model = LinearRegression().fit(X, Y)
            
            values = {}
            values["slope"] = model.coef_[0]
            values["intercept"] = model.intercept_
            values["r squared"] = model.score(X, Y)
            
            return values
            
        except Exception as e:
            error_msg = f"Error occurred during linear regression: {str(e)}"
            self.event_logger.addtext(error_msg)
            return None

    def predict(self, data_given:dict):
        self.data_logger.addtext("___________________________________________________________________")
        self.data_logger.addtext("Predicting for values...")
        self.data_logger.addtext(str(data_given))
        

        try:
            X = self.budgetReader.data.drop(columns=[self.budgetReader.independent_var])
            Y = self.budgetReader.data[self.budgetReader.independent_var]
            model = LinearRegression().fit(X, Y)

            df = pd.DataFrame(data_given, index=[0]) 
            df = df[X.columns] 
            predicted_values = model.predict(df)
            self.data_logger.addtext("Predicted values: {}".format(predicted_values))
        
        except Exception as e:
            self.event_logger.addtext("ERROR: An error occurred during prediction: {}".format(str(e)))
            return

        
        self.data_logger.addtext("Here is the predicted value of your dependent variable given the independent variables you provided:")
        self.data_logger.addtext("- - - - - - - - - - - ")
        self.data_logger.addtext(str(predicted_values))
        self.data_logger.addtext("- - - - - - - - - - - ")
        

        coefficients = dict(zip(self.budgetReader.data.columns, model.coef_))
        


        self.accuracy(0.2)
        self.recommend_changes(coefficients)
    
    def accuracy(self, percent):
        Y = self.budgetReader.data[self.budgetReader.independent_var]
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i!=self.budgetReader.independent_var]]
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =percent)

        model = LinearRegression().fit(x_train, y_train)
        y_pred_test = model.predict(x_test)


        # self.data_logger.addtext(str(y_pred_test))
        self.data_logger.addtext(" ")
        self.data_logger.addtext("Linear Regression Information: ")
        self.data_logger.addtext("Mean absolute error =" + str(round(sm.mean_absolute_error(y_test, y_pred_test), 2))) 
        self.data_logger.addtext("Mean squared error =" + str(round(sm.mean_squared_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Median absolute error =" + str(round(sm.median_absolute_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Explain variance score ="+ str(round(sm.explained_variance_score(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("R2 score ="+ str(round(sm.r2_score(y_test, y_pred_test), 2)))
        
    

    def recommend_changes(self, coefficients):
        # Sort coefficients by absolute value to identify important features
        sorted_coefficients = sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True)

        # Print the sorted coefficients
        self.data_logger.addtext(" ")
        self.data_logger.addtext("List of coefficients in order from best returns to least: ")
        for feature, coefficient in sorted_coefficients:
            self.data_logger.addtext(f"{feature}: {coefficient}")

