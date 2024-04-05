import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os

# Get the current working directory
cwd = os.getcwd()

# Construct the file path
file_path = os.path.join(cwd, '.\\old_files\\sales.csv')

# Load the data
data = pd.read_csv(file_path)

# Extract independent variables and dependent variable
independent_vars = ['Advertising', 'Digital Marketing', 'Marketing Research',
                    'Agency Fees', 'Training and Development', 'Promotions and Sponsorships']
X = data[independent_vars].values  # Independent variables
y = data['Sales'].values           # Dependent variable (sales)

# Define polynomial regression model
degree = 2  # Polynomial degree
poly_features = PolynomialFeatures(degree=degree)

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

# Define budget
budget = 50000  # Budget integer

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

print("Optimized Independent Variable Amounts:", optimized_amounts)
print("Predicted Sales with Optimized Amounts:", predicted_sales)

# Print out the allocated amounts for each independent variable
for name, amount in zip(independent_vars, optimized_amounts):
    print(f"Allocated amount for {name}: {amount}")