import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Sales Forecaster", layout="wide")

st.title("📊 AI Sales Forecaster & Analytics")
st.write("Upload your sales data to generate instant forecasts and detect anomalies.")

uploaded_file = st.file_uploader(
    "Upload your Sales CSV (Must have 'Date' and 'Sales' columns)",
    type="csv"
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if not {"Date", "Sales"}.issubset(df.columns):
            st.error("CSV must contain 'Date' and 'Sales' columns.")
            st.stop()

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date", "Sales"])
        df = df.sort_values("Date")
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
        df = df.dropna(subset=["Sales"])
        df.set_index("Date", inplace=True)

        if len(df) < 12:
            st.error("At least 12 data points are required for forecasting.")
            st.stop()

        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.subheader("Historical Data")
            st.line_chart(df["Sales"])

        seasonal_period = 12 if len(df) >= 24 else max(2, len(df) // 2)

        model = ExponentialSmoothing(
            df["Sales"],
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_period
        ).fit(optimized=True)

        steps = 6
        forecast = model.forecast(steps)
        forecast.index = pd.date_range(
            start=df.index[-1] + pd.offsets.MonthEnd(1),
            periods=steps,
            freq="M"
        )

        with col2:
            st.subheader("6-Month Forecast")
            st.dataframe(
                forecast.rename("Projected Sales").to_frame(),
                use_container_width=True
            )

        st.subheader("Visual Projection")
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(df.index, df["Sales"], label="Actual Sales")
        ax.plot(forecast.index, forecast, linestyle="--", label="Forecast")
        ax.fill_between(
            forecast.index,
            forecast * 0.9,
            forecast * 1.1,
            alpha=0.25
        )
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig, use_container_width=True)

        st.success(
            f"### Total Expected Revenue (Next 6 Months): ${forecast.sum():,.2f}"
        )

    except Exception as e:
        st.error("An error occurred while processing the data.")
        st.exception(e)

else:
    st.info("Waiting for CSV upload. Download a sample template if needed.")
