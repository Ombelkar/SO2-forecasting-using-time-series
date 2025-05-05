import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import requests
import streamlit as st

# Page config
st.set_page_config(layout="wide")
st.title("🌍 Interactive SO₂ Forecast by State - India")

# Load dataset
df = pd.read_csv("differenced_AQI.csv")
df.columns = df.columns.str.strip()
df['Year'] = pd.to_datetime(df['Year'])
df.set_index('Year', inplace=True)


geo_url = 'https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson'
india_states = requests.get(geo_url).json()


state_name_fix = {
    "Andaman & Nicobar Island": "Andaman & Nicobar Islands",
    "Delhi": "NCT of Delhi",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Orissa": "Odisha",
    "Uttaranchal": "Uttarakhand",
}
df['State'] = df['State'].replace(state_name_fix)


st.subheader("📍 Select a State to Forecast SO₂")

latest_year = df.index.max()
current_data = df[df.index == latest_year].groupby('State')['SO2'].mean().reset_index()


all_states = [state['properties']['NAME_1'] for state in india_states['features']]
full_data = pd.DataFrame({'State': all_states})
current_data = pd.merge(full_data, current_data, on='State', how='left').fillna(0)

# Dropdown for state selection
selected_state = st.selectbox("Select a state", all_states)
months = st.slider("Select number of months to forecast", 1, 36, 6)

if st.button("📈 Show Forecast"):
    if selected_state in df['State'].unique():
        state_df = df[df['State'] == selected_state]['SO2'].resample('M').mean()
        model = ARIMA(state_df, order=(1, 1, 1))
        fit = model.fit()
        forecast = fit.forecast(steps=months)

        forecast_index = pd.date_range(start=state_df.index[-1] + pd.DateOffset(months=1), periods=months, freq='M')
        forecast_df = pd.DataFrame({'Date': forecast_index, 'Forecasted SO2': forecast.values})

        fig = px.line(forecast_df, x='Date', y='Forecasted SO2',
                      title=f"Forecasted SO₂ Levels in {selected_state} for Next {months} Months")
        st.plotly_chart(fig)
    else:
        st.warning(f"No data available for {selected_state}.")

# -# ---------- Forecast Heatmap for All States ----------
st.subheader(f"🗺️ Forecasted SO₂ Heatmap by State ({months} Months Ahead)")

forecast_values = []

for state in all_states:
    if state in df['State'].unique():
        try:
            state_series = df[df['State'] == state]['SO2'].resample('M').mean()
            model = ARIMA(state_series, order=(1, 1, 1))
            fit = model.fit()
            forecast = fit.forecast(steps=months)
            forecast_values.append(forecast.iloc[-1])  # forecast at nth month
        except:
            forecast_values.append(None)
    else:
        forecast_values.append(None)

forecast_map_data = pd.DataFrame({
    'State': all_states,
    f'SO2_{months}m_forecast': forecast_values
})

fig_forecast_map = px.choropleth(
    forecast_map_data,
    geojson=india_states,
    featureidkey="properties.NAME_1",
    locations='State',
    color=f'SO2_{months}m_forecast',
    color_continuous_scale="Oranges",
    title=f"Forecasted SO₂ Levels by State ({months} Months Ahead)"
)
fig_forecast_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_forecast_map)
