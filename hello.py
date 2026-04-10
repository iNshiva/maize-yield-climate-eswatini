# Step 1: Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Load the Excel file
df = pd.read_excel("Data 1.xlsx")  # make sure this is the correct file name

# Step 3: Clean column names
df.columns = df.columns.str.strip()          # remove leading/trailing spaces
df.columns = df.columns.str.lower()          # lowercase all names
df.columns = df.columns.str.replace(' ', '_')  # replace spaces with underscores
df.columns = df.columns.str.replace('(', '')   # remove '('
df.columns = df.columns.str.replace(')', '')   # remove ')'

# Step 6: Correlation analysis
correlation_matrix = df[['yield_per_ha', 'rainfall_mm', 'temperature', 'carbon', 'area_planted_ha']].corr()

# Step 1: Import libraries
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

# Step 2: Load your cleaned dataset
df = pd.read_excel("ETA_Data.xlsx")  # make sure file name matches
df.columns = ['Year', 'Production', 'Area', 'Yield', 'Rainfall', 'Temperature', 'CO2']

# Step 3: Define a function to perform ADF test
def adf_test(series, series_name):
    result = adfuller(series, autolag='AIC')
    print(f'ADF Test for {series_name}:')
    print(f'  Test Statistic : {result[0]}')
    print(f'  p-value        : {result[1]}')
    if result[1] < 0.05:
        print("  → Stationary (reject H0)\n")
    else:
        print("  → Non-stationary (fail to reject H0)\n")

# Step 4: Run ADF test on all numeric variables
numeric_vars = ['Yield', 'Rainfall', 'Temperature', 'CO2', 'Area', 'Production']
for var in numeric_vars:
    adf_test(df[var], var)