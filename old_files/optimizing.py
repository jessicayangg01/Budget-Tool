import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize

# Function to calculate sales based on budget allocation
def calculate_sales(budget_allocation, X_poly):
    return -model.predict(poly.transform(np.array([budget_allocation]).reshape(1, -1)))[0]

# Function to minimize
def objective(budget_allocation):
    return calculate_sales(budget_allocation, X_poly)

# Sample data (replace with your actual data)
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Independent variables
Y = np.array([10, 20, 30])  # Sales
budget = 50  # Defined budget

# Scaling the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Polynomial features
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_scaled)

# Fitting the model
model = LinearRegression()
model.fit(X_poly, Y)

# Minimize the objective function
initial_budget_allocation = np.ones(X_poly.shape[1]) * (budget / X_poly.shape[1])  # Initial guess
bounds = [(0, budget)] * X_poly.shape[1]  # Bounds for budget allocation
res = minimize(objective, initial_budget_allocation, bounds=bounds)

optimal_budget_allocation = res.x
optimal_sales = -res.fun

print("Optimal budget allocation:", optimal_budget_allocation)
print("Optimal sales:", optimal_sales)
