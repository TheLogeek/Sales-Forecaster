import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# page config
st.set_page_config(page_title="Sales Forecaster Pro", layout="wide")

st.title("📊 AI Sales Forecaster & Analytics")
st.write("Upload your sales data to generate instant forecasts and detect anomalies.")

# file uploader
uploaded_file = st.file_uploader("Upload your Sales CSV (Must have 'Date' and 'Sales' columns)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    #layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Historical Data")
        st.line_chart(df['Sales'])

    # forecasting logic
    model = ExponentialSmoothing(df['Sales'], trend='add', seasonal='add', seasonal_periods=12).fit()
    forecast = model.forecast(6)
    
    with col2:
        st.subheader("6-Month Forecast")
        st.write(forecast)

    # main chart
    st.subheader("Visual Projection")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['Sales'], label="Actual Sales", color="#1f77b4")
    ax.plot(forecast.index, forecast, label="Forecast", color="#ff7f0e", linestyle="--")
    ax.fill_between(forecast.index, forecast*0.9, forecast*1.1, color='orange', alpha=0.2)
    ax.legend()
    st.pyplot(fig)

    # business insights
    st.success(f"### Total Expected Revenue (Next 6 Months): ${forecast.sum():,.2f}")
    
else:
    st.info("Waiting for CSV upload. Download a sample template if needed.")