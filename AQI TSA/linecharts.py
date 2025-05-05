import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from statsmodels.tsa.arima.model import ARIMA

# Load and preprocess dataset
df = pd.read_csv("differenced_AQI.csv")  # Update with your CSV path
df.columns = df.columns.str.strip()

if 'Year' not in df.columns or 'State' not in df.columns or 'SO2' not in df.columns:
    raise ValueError("CSV must contain 'Year', 'State', and 'SO2' columns.")

# Convert Year to datetime
df['Year'] = pd.to_datetime(df['Year'])  # Automatically handles YYYY-MM-DD
df.set_index('Year', inplace=True)

# GUI function
def forecast_so2():
    try:
        state = state_var.get()
        months = int(month_var.get())

        if state == "" or months <= 0:
            raise ValueError

        # Filter state-wise data
        state_data = df[df['State'] == state]['SO2'].resample('Y').mean().dropna()

        if len(state_data) < 4:
            messagebox.showerror("Not Enough Data", f"Not enough data for '{state}'.")
            return

        # Interpolate to monthly frequency for smoother forecasting
        monthly_data = state_data.resample('M').interpolate()

        # Fit ARIMA
        model = ARIMA(monthly_data, order=(1, 1, 1))
        model_fit = model.fit()

        # Forecast
        forecast = model_fit.forecast(steps=months)
        forecast_index = pd.date_range(start=monthly_data.index[-1] + pd.DateOffset(months=1), periods=months, freq='M')

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(monthly_data, label='Historical SO2')
        plt.plot(forecast_index, forecast, label='Forecasted SO2', color='red', linestyle='--')
        plt.title(f"SO2 Forecast for {state} ({months} months)")
        plt.xlabel("Date")
        plt.ylabel("SO2 Level")
        plt.legend()
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid state and forecast duration.")

# GUI setup
root = tk.Tk()
root.title("SO2 Forecast (ARIMA)")

# State dropdown
tk.Label(root, text="Select State:").grid(row=0, column=0, padx=10, pady=10)
state_var = tk.StringVar()
state_dropdown = ttk.Combobox(root, textvariable=state_var, values=sorted(df['State'].unique()))
state_dropdown.grid(row=0, column=1)

# Months input
tk.Label(root, text="Forecast Duration (months):").grid(row=1, column=0, padx=10, pady=10)
month_var = tk.StringVar()
tk.Entry(root, textvariable=month_var).grid(row=1, column=1)

# Forecast button
tk.Button(root, text="Forecast", command=forecast_so2).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()