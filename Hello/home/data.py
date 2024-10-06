import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Parameters for the dataset
n_samples = 1000  # Number of samples to simulate
age_range = (20, 70)  # Age range
income_range = (30000, 150000)  # Income range
horizon_range = (1, 40)  # Investment horizon in years
risk_tolerance_levels = ['Very Low', 'Low', 'Moderate', 'High']  # Risk tolerance categories

# Asset allocation based on risk tolerance (simplified percentages for stocks and bonds)
allocation_by_risk = {
    'Very Low': {'Stock_Allocation': 10, 'Bond_Allocation': 70, 'Gold_Allocation': 10, 'Real_Estate_Allocation': 10},
    'Low': {'Stock_Allocation': 30, 'Bond_Allocation': 50, 'Gold_Allocation': 10, 'Real_Estate_Allocation': 10},
    'Moderate': {'Stock_Allocation': 60, 'Bond_Allocation': 30, 'Gold_Allocation': 5, 'Real_Estate_Allocation': 5},
    'High': {'Stock_Allocation': 80, 'Bond_Allocation': 10, 'Gold_Allocation': 5, 'Real_Estate_Allocation': 5},
}

# Expected return based on risk tolerance and horizon (simplified for simulation)
expected_return_by_risk = {
    'Very Low': 3.0,
    'Low': 4.5,
    'Moderate': 6.0,
    'High': 7.5
}

# Create a dataframe to store the simulated data
simulated_data = []

for _ in range(n_samples):
    # Randomly generate features
    age = np.random.randint(age_range[0], age_range[1])
    income = np.random.randint(income_range[0], income_range[1])
    investment_horizon = np.random.randint(horizon_range[0], horizon_range[1])
    risk_tolerance = np.random.choice(risk_tolerance_levels)
    
    # Get the corresponding asset allocations and expected return based on risk tolerance
    stock_alloc = allocation_by_risk[risk_tolerance]['Stock_Allocation']
    bond_alloc = allocation_by_risk[risk_tolerance]['Bond_Allocation']
    gold_alloc = allocation_by_risk[risk_tolerance]['Gold_Allocation']
    real_estate_alloc = allocation_by_risk[risk_tolerance]['Real_Estate_Allocation']
    expected_return = expected_return_by_risk[risk_tolerance]
    
    # Append the row to the list
    simulated_data.append([age, risk_tolerance, income, investment_horizon, stock_alloc, bond_alloc, gold_alloc, real_estate_alloc, expected_return])

# Convert the list to a DataFrame
columns = ['Age', 'Risk_Tolerance', 'Income', 'Investment_Horizon', 'Stock_Allocation', 'Bond_Allocation', 'Gold_Allocation', 'Real_Estate_Allocation', 'Expected_Return']
simulated_df = pd.DataFrame(simulated_data, columns=columns)

# Display the first few rows of the simulated dataset
simulated_df.head()
