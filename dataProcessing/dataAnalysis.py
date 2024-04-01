# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm
import pandas as pd

from dataProcessing.polynomialRegOptimizer import PolynomialRegressionOptimizer
from scipy.optimize import minimize

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
        self.data_logger.addtext("")
        self.data_logger.addtext("LINEAR REGRESSION PREDICTION:")
        self.data_logger.addtext("")
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

        self.data_logger.addtext(" ")
        self.data_logger.addtext("Linear Regression Information: ")
        self.data_logger.addtext("Mean absolute error =" + str(round(sm.mean_absolute_error(y_test, y_pred_test), 2))) 
        self.data_logger.addtext("Mean squared error =" + str(round(sm.mean_squared_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Median absolute error =" + str(round(sm.median_absolute_error(y_test, y_pred_test), 2)) )
        self.data_logger.addtext("Explain variance score ="+ str(sm.explained_variance_score(y_test, y_pred_test)))
        self.data_logger.addtext("R2 score ="+ str(sm.r2_score(y_test, y_pred_test)))
        
    

    def recommend_changes(self, coefficients):
        # Sort coefficients by absolute value to identify important features
        sorted_coefficients = sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True)

        # Print the sorted coefficients
        self.data_logger.addtext(" ")
        self.data_logger.addtext("List of coefficients in order from best returns to least: ")
        for feature, coefficient in sorted_coefficients:
            self.data_logger.addtext(f"{feature}: {coefficient}")
    



    ############################# logistic reg
    def polynomial_regression(self, col, deg):
        try:
            Y = np.array(self.budgetReader.data[self.budgetReader.independent_var])
            X = np.array(self.budgetReader.data[col]).reshape((-1, 1))
            
            # Transform the features to polynomial features
            poly_features = PolynomialFeatures(degree=deg)
            X_poly = poly_features.fit_transform(X)
            
            # Fit the polynomial regression model
            model = LinearRegression().fit(X_poly, Y)

            # Generate predictions using the polynomial features
            X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
            X_range_poly = poly_features.transform(X_range)
            Y_pred = model.predict(X_range_poly)

            # Store the results
            values = {}
            values["x_range"] = X_range
            values["y_pred"] = Y_pred
            values["coefficients"] = model.coef_
            values["intercept"] = model.intercept_
            values["r_squared"] = model.score(X_poly, Y)

            return values
            
        except Exception as e:
            error_msg = f"Error occurred during polynomial regression: {str(e)}"
            self.event_logger.addtext(error_msg)
            return None
    

    # def predict_polynomial_reg(self, data_given: dict, deg: int):
    #     self.data_logger.addtext("___________________________________________________________________")
    #     self.data_logger.addtext("")
    #     self.data_logger.addtext("POLYNOMIAL REGRESSION PREDICTION:")
    #     self.data_logger.addtext("")
    #     self.data_logger.addtext("Predicting for values...")
    #     self.data_logger.addtext(str(data_given))

    #     try:
    #         # Extract independent and dependent variables from the dataset
    #         X_train = self.budgetReader.data.drop(columns=[self.budgetReader.independent_var])
    #         y_train = self.budgetReader.data[self.budgetReader.independent_var]

    #         # Transform the independent variables into polynomial features
    #         poly_features = PolynomialFeatures(degree=deg)
    #         X_train_poly = poly_features.fit_transform(X_train)

    #         # Fit the polynomial regression model
    #         model = LinearRegression().fit(X_train_poly, y_train)

    #         # Prepare the input data for prediction
    #         df = pd.DataFrame(data_given, index=[0])
    #         df_poly = poly_features.transform(df)

    #         # Make predictions
    #         predicted_values = model.predict(df_poly)

    #         # Log the predicted values
    #         self.data_logger.addtext("Predicted values: {}".format(predicted_values))

    #         # Log the predicted value of the dependent variable
    #         self.data_logger.addtext("Here is the predicted value of your dependent variable given the independent variables you provided:")
    #         self.data_logger.addtext("- - - - - - - - - - - ")
    #         self.data_logger.addtext(str(predicted_values))
    #         self.data_logger.addtext("- - - - - - - - - - - ")

            
    #         self.evaluate_polynomial_reg(0.2, deg)


    #         ## ADDED
    #         return predicted_values

    #     except Exception as e:
    #         self.event_logger.addtext("ERROR: An error occurred during prediction: {}".format(str(e)))
        
        
    def predict_polynomial_reg(self, data_given: dict, deg: int):
        self.data_logger.addtext("___________________________________________________________________")
        self.data_logger.addtext("")
        self.data_logger.addtext("POLYNOMIAL REGRESSION PREDICTION:")
        self.data_logger.addtext("")
        self.data_logger.addtext("Predicting for values...")
        self.data_logger.addtext(str(data_given))

            # Extract independent and dependent variables from the dataset
        X_train = self.budgetReader.data.drop(columns=[self.budgetReader.independent_var])
        y_train = self.budgetReader.data[self.budgetReader.independent_var]

            # Transform the independent variables into polynomial features
        poly_features = PolynomialFeatures(degree=deg)
        X_train_poly = poly_features.fit_transform(X_train)

            # Fit the polynomial regression model
        model = LinearRegression().fit(X_train_poly, y_train)

            # Prepare the input data for prediction
        df = pd.DataFrame(data_given, index=[0])
        df_poly = poly_features.transform(df)

            # Make predictions
        predicted_values = model.predict(df_poly)

            # Log the predicted values
        self.data_logger.addtext("Predicted values: {}".format(predicted_values))

            # Log the predicted value of the dependent variable
        self.data_logger.addtext("Here is the predicted value of your dependent variable given the independent variables you provided:")
        self.data_logger.addtext("- - - - - - - - - - - ")
        self.data_logger.addtext(str(predicted_values))
        self.data_logger.addtext("- - - - - - - - - - - ")

            
        self.evaluate_polynomial_reg(0.2, deg)


            ## ADDED
        budget = sum(data_given.values())
        self.recommend_changes_polynomial_reg(X_train, y_train, budget, predicted_values)


        return predicted_values


    
    def evaluate_polynomial_reg(self, percent, deg):
        Y = self.budgetReader.data[self.budgetReader.independent_var]
        X = self.budgetReader.data[[i for i in self.budgetReader.data if i != self.budgetReader.independent_var]]
        
        # Split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=percent)

        # Transform the independent variables into polynomial features
        poly_features = PolynomialFeatures(degree=deg)
        x_train_poly = poly_features.fit_transform(x_train)
        x_test_poly = poly_features.transform(x_test)

        # Fit the polynomial regression model
        model = LinearRegression().fit(x_train_poly, y_train)

        # Make predictions on the test set
        y_pred = model.predict(x_test_poly)

        # Evaluate the model using common metrics for regression
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        self.data_logger.addtext("Mean Squared Error:"+ str(mse))
        self.data_logger.addtext("R-squared Score:"+ str(r2))
        
    

    # def recommend_changes_polynomial_reg(self, data_given: dict, deg, budget):
    #     try:
    #         # Predict sales based on the provided independent variables
    #         predicted_sales = self.predict_polynomial_reg(data_given, deg)

    #         # Calculate the contributions of each independent variable to the predicted sales
    #         contributions = {}
    #         for col in data_given:
    #             # Increment the value of the independent variable by a small amount
    #             data_given_incremented = data_given.copy()
    #             data_given_incremented[col] += 1  # Adjust the increment value as needed

    #             # Ensure that the incremented value is non-negative
    #             if data_given_incremented[col] < 0:
    #                 data_given_incremented[col] = 0

    #             # Predict sales with the incremented value of the independent variable
    #             predicted_sales_incremented = self.predict_polynomial_reg(data_given_incremented, deg)

    #             # Calculate the contribution of the variable
    #             contribution = predicted_sales_incremented - predicted_sales
    #             contributions[col] = contribution

    #         # Normalize contributions to sum up to the budget
    #         total_contribution = sum(contributions.values())
    #         normalized_contributions = {col: (contribution / total_contribution) * budget for col, contribution in contributions.items()}

    #         # Check if any contribution is negative and adjust it to zero
    #         for col, allocation in normalized_contributions.items():
    #             if allocation < 0:
    #                 normalized_contributions[col] = 0

    #         # Cap allocations to ensure they don't exceed the budget
    #         total_allocated = sum(normalized_contributions.values())
    #         if total_allocated > budget:
    #             # Calculate the scaling factor to adjust allocations to fit within the budget
    #             scaling_factor = budget / total_allocated
    #             # Apply scaling factor to each allocation
    #             normalized_contributions = {col: allocation * scaling_factor for col, allocation in normalized_contributions.items()}

    #         # Recalculate total_contribution after adjusting allocations
    #         total_contribution = sum(normalized_contributions.values())

    #         # Calculate the new predicted sales value
    #         new_predicted_sales = predicted_sales + total_contribution

    #         # Log the recommendations
    #         self.data_logger.addtext("___________________________________________________________________")
    #         self.data_logger.addtext("")
    #         self.data_logger.addtext("Recommendations for Budget Allocation:")
    #         self.data_logger.addtext("")

    #         for col, allocation in normalized_contributions.items():
    #             self.data_logger.addtext(f"{col}: {allocation}")

    #         self.data_logger.addtext("This will give you a " + str(self.budgetReader.independent_var) + " value of : " + str(new_predicted_sales))
    #         self.data_logger.addtext("Which is a " + str(total_contribution) + " increase from the previous value of " + str(predicted_sales))

    #         # Calculate the percentage increase
    #         percentage_increase = (total_contribution / predicted_sales) * 100
    #         # Convert percentage_increase to a scalar value if it's a numpy array
    #         percentage_increase_scalar = percentage_increase.item() if isinstance(percentage_increase, np.ndarray) else percentage_increase
    #         # Convert percentage_increase to a string with two decimal places
    #         percentage_increase_str = "{:.2f}%".format(percentage_increase_scalar)
    #         # Log the percentage increase
    #         self.data_logger.addtext("Percentage Increase: " + percentage_increase_str)

    #         return normalized_contributions

    #     except Exception as e:
    #         self.event_logger.addtext("ERROR: An error occurred during recommendation: {}".format(str(e)))
        
    def recommend_changes_polynomial_reg(self, X, y, budget, old):
        try:
            allocation, sales = PolynomialRegressionOptimizer(X, y, budget, self.budgetReader.getDependentVar())
            # Log the recommendations
            
            
            self.data_logger.addtext("___________________________________________________________________")
            self.data_logger.addtext("")
            self.data_logger.addtext("Recommendations for Budget Allocation:")
            self.data_logger.addtext("")

            

            new = {}

            for col, amount in zip(self.budgetReader.getDependentVar(), allocation):
                self.data_logger.addtext(f"{col}: {amount}")
                new[col] = amount

            self.data_logger.addtext("Sales value without recommendation: " + str(old))
            self.data_logger.addtext("Sales value with new recommendation: " + str(sales))
            self.data_logger.addtext("Sales increase: " + str(sales-old))
            
            percentage_increase = ((sales - old) / old) * 100
            # Convert percentage_increase to a scalar value if it's a numpy array
            percentage_increase_scalar = percentage_increase.item() if isinstance(percentage_increase, np.ndarray) else percentage_increase
            # Convert percentage_increase to a string with two decimal places
            percentage_increase_str = "{:.2f}%".format(percentage_increase_scalar)
            # Log the percentage increase
            self.data_logger.addtext("Percentage Increase: " + percentage_increase_str)

        except Exception as e:
            self.event_logger.addtext("ERROR: An error occurred during recommendation: {}".format(str(e)))

