# 🌍 Interactive SO₂ Forecasting Across Indian States

This project focuses on forecasting sulfur dioxide (SO₂) air pollution levels across different Indian states using time series analysis with ARIMA. The tool is built using Python, Streamlit, and Plotly for interactive forecasting and visualization.

## 📌 Key Features

- Forecast SO₂ levels for up to 36 months using ARIMA models
- Interactive state selection through a Streamlit web app
- Clickable heatmap to visualize future SO₂ levels across states
- Automatically handles missing data and performs differencing for stationarity
- Supports data cleaning and preprocessing steps for real-world datasets

## ⚙️ Tech Stack

- **Python**
- **Pandas**, **NumPy** – Data preprocessing
- **Statsmodels** – ARIMA modeling
- **Plotly Express** – Visualization
- **Streamlit** – Web app interface
- **GeoJSON** – For mapping Indian states

## 📁 Files

- `combined AQI.csv` – 2015 - 2023 combined dataset before differencing
- `differenced_AQI.csv` – Preprocessed and differenced data
- `app.py` – Main Streamlit application
- `pdf_to_csv.py`, `combine.py`, `graphs.py` – Data extraction and visualization scripts

- Data Source: The dataset used in this project was obtained from the official website of the Central Pollution Control Board (CPCB), India – https://cpcb.nic.in/.

## 📈 How it Works

1. The user selects a state and number of months (up to 36) to forecast.
2. The tool runs an ARIMA model on the SO₂ data for that state.
3. Forecasted values are plotted interactively using Plotly.
4. A heatmap shows predicted SO₂ levels across all Indian states.

## 🚀 Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/ombelkar/Interactive-SO2-Forecasting-India.git
