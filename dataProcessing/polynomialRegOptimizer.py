import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge


def PolynomialRegressionOptimizer(X, y, budget, independent_vars):
    # Scale the independent variables
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Define polynomial regression model
    degree = 2  # Polynomial degree
    poly_features = PolynomialFeatures(degree=degree)
    
    # Fit polynomial regression model
    X_poly = poly_features.fit_transform(X_scaled)
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # Objective function to maximize sales/independent var ratio
    def objective(x):
        X_poly = poly_features.transform([x])
        predicted_sales = model.predict(X_poly)[0]
        return -predicted_sales / np.sum(x)  # maximize sales/independent var ratio
    
    # Constraint: sum of independent variable amounts <= budget
    def constraint(x, budget):
        return budget - np.sum(x)
    
    # Initial guess for independent variable amounts
    x0 = np.ones(len(independent_vars)) * (budget / len(independent_vars))
    
    # Bounds: independent variable amounts should be between 0 and budget
    bounds = [(0, budget) for _ in range(len(independent_vars))]
    
    # Constraint: independent variable amounts should sum to budget or less
    constraints = {'type': 'ineq', 'fun': constraint, 'args': (budget,)}
    
    # Optimization
    result = minimize(objective, x0, bounds=bounds, constraints=constraints)
    
    # Extract optimized independent variable amounts
    optimized_amounts = result.x
    
    # Transform optimized amounts back to original scale
    optimized_amounts_original_scale = scaler.inverse_transform([optimized_amounts])
    
    # Ensure non-negativity
    optimized_amounts_original_scale[optimized_amounts_original_scale < 0] = 0
    
    # Ensure the sum of optimized amounts does not exceed the budget
    total_allocated = np.sum(optimized_amounts_original_scale)
    if total_allocated > budget:
        # If the sum exceeds the budget, proportionally reduce all amounts
        optimized_amounts_original_scale *= budget / total_allocated
    
    return optimized_amounts_original_scale[0]