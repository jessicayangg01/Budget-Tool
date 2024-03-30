# from interface.graphsView import GraphsView
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy import stats

from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn.metrics as sm

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

class MarketDataAnalysis(object):
    def __init__(self):
        None

    
    def linearRegression(self, X, Y):
        Y = np.array(Y)
        # X = np.array(self.data["X"].reshape((-1, 1)))
        X = np.array(X).reshape(-1, 1)
        model = LinearRegression().fit(X, Y)
        return model

    def randomForestRegression(self, Y, X, Z):
        # Assuming X, Y, Z are your arrays
        X = np.column_stack((X, Z))  # Stack X, Y, Z horizontally to create feature matrix
        y = np.array(Y).ravel()
        # y = np.array(Y).reshape(-1, 1)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Random Forest Regressor model
        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, y_pred)

        prediction_variance = np.var([tree.predict(X_test) for tree in model.estimators_], axis=0)

        output = {"y_test": y_test, "y_pred": y_pred, "mse": mse, "model": model, "prediction_variance": prediction_variance}
        return output



    def correlation_analysis(self, X, Y):
        correlation_coefficient = np.corrcoef(X, Y)[0, 1]
        return correlation_coefficient



    
