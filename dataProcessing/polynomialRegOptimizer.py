import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os


def PolynomialRegressionOptimizer(X, y, budget, independent_vars):
        # Define polynomial regression model
        degree = 2  # Polynomial degree
        poly_features = PolynomialFeatures(degree=degree)

        # independent_vars = ['Advertising', 'Digital Marketing', 'Marketing Research',
        #             'Agency Fees', 'Training and Development', 'Promotions and Sponsorships']
        # Fit polynomial regression model
        X_poly = poly_features.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)

        # Objective function to minimize (negative of predicted sales)
        def objective(x, budget):
            X_poly = poly_features.fit_transform([x])
            predicted_sales = model.predict(X_poly)[0]
            return -predicted_sales

        # Constraint: sum of independent variable amounts <= budget
        def constraint(x, budget):
            return budget - np.sum(x)

        # Initial guess for independent variable amounts
        x0 = np.ones(len(independent_vars)) * (budget / len(independent_vars))

        # Optimization
        bounds = [(0, budget) for _ in range(len(independent_vars))]
        constraints = {'type': 'ineq', 'fun': constraint, 'args': (budget,)}
        result = minimize(objective, x0, args=(budget,), bounds=bounds, constraints=constraints)

        # Extract optimized independent variable amounts
        optimized_amounts = result.x

        # Predict sales with optimized amounts
        X_optimized_poly = poly_features.fit_transform([optimized_amounts])
        predicted_sales = model.predict(X_optimized_poly)[0]
        
        return [optimized_amounts, predicted_sales]