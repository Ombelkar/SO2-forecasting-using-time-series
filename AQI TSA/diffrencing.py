import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("C:/Users/BAPS/Desktop/combined AQI.csv")

# Ensure Year column is treated as datetime and SO2 as numeric
df['Year'] = pd.to_datetime(df['Year'], format='%Y')  
df['SO2'] = pd.to_numeric(df['SO2'], errors='coerce')


df_grouped = df.groupby(['Year', 'State'], as_index=False)['SO2'].mean()

# Set Year as the index
df_grouped.set_index('Year', inplace=True)

# Perform Differencing (to make the data stationary)
df_grouped['SO2_diff'] = df_grouped.groupby('State')['SO2'].diff()

# Drop the first row (as differencing introduces NaN for the first entry)
df_grouped = df_grouped.dropna()

# Plot the original and differenced data to check the effect
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(df_grouped['SO2'], label='Original SO2 Data')
plt.title('Original SO2 Data (Before Differencing)')
plt.xlabel('Year')
plt.ylabel('SO2')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df_grouped['SO2_diff'], label='Differenced SO2 Data', color='red')
plt.title('Differenced SO2 Data (After Differencing)')
plt.xlabel('Year')
plt.ylabel('Differenced SO2')
plt.legend()

plt.tight_layout()
plt.show()

# Save the differenced data to a new CSV file
df_grouped.to_csv("C:/Users/BAPS/Desktop/differenced_AQI.csv")
