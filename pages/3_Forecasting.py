import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helper import load_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Forecasting",
    page_icon="📉",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = load_data()

if df.empty:
    st.error("Dataset could not be loaded.")
    st.stop()

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📉 Healthcare Forecasting")
st.markdown("Trend Analysis & Simple Moving Average Forecast")

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Forecast Settings")

metric = st.sidebar.selectbox(
    "Select Metric",
    [
        "Children apprehended and placed in CBP custody*",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]
)

window = st.sidebar.slider(
    "Moving Average Window",
    min_value=3,
    max_value=30,
    value=7
)

forecast_days = st.sidebar.slider(
    "Forecast Days",
    min_value=7,
    max_value=60,
    value=30
)

# --------------------------------------------------
# Prepare Data
# --------------------------------------------------

forecast_df = df[["Date", metric]].copy()

forecast_df["Moving Average"] = (
    forecast_df[metric]
    .rolling(window=window)
    .mean()
)

# --------------------------------------------------
# Trend Chart
# --------------------------------------------------

st.subheader("Historical Trend")

fig1 = px.line(
    forecast_df,
    x="Date",
    y=metric,
    markers=True,
    title=f"{metric} Trend"
)

fig1.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# Moving Average
# --------------------------------------------------

st.subheader("Moving Average")

fig2 = px.line(
    forecast_df,
    x="Date",
    y=["Moving Average", metric],
    title="Actual vs Moving Average"
)

fig2.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# Forecast
# --------------------------------------------------

last_date = forecast_df["Date"].max()

last_average = (
    forecast_df["Moving Average"]
    .dropna()
    .iloc[-1]
)

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=forecast_days
)

future = pd.DataFrame({
    "Date": future_dates,
    "Forecast": [last_average] * forecast_days
})

# --------------------------------------------------
# Forecast Chart
# --------------------------------------------------

st.subheader("Forecast")

fig3 = px.line(
    future,
    x="Date",
    y="Forecast",
    markers=True,
    title=f"Next {forecast_days} Days Forecast"
)

fig3.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# Forecast Table
# --------------------------------------------------

st.subheader("Forecast Data")

st.dataframe(
    future,
    use_container_width=True
)

# --------------------------------------------------
# Download Forecast
# --------------------------------------------------

csv = future.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name="forecast.csv",
    mime="text/csv"
)