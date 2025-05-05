import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("C:/Users/BAPS/Desktop/combined AQI.csv")  # Adjust the path accordingly

# Ensure 'Year' is treated as a datetime object (if not already)
df['Year'] = pd.to_datetime(df['Year'], format='%Y')  # Ensure Year is datetime
df.set_index('Year', inplace=True)

# Function to perform ADF test
def adf_test(series):
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]}")
    print(f"P-value: {result[1]}")
    print(f"Critical Values: {result[4]}")

    if result[1] <= 0.05:
        print("The series is likely stationary (p-value <= 0.05)")
    else:
        print("The series is likely non-stationary (p-value > 0.05)")

# Apply the ADF test to a particular state's SO2 data (e.g., 'Delhi')
state_data = df[df['State'] == 'Maharashtra']['SO2']
adf_test(state_data)
