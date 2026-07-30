import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helper import load_data, calculate_kpis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Healthcare Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

if df.empty:
    st.error("Dataset could not be loaded.")
    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("📌 Dashboard Filters")

# Metric Toggle
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

# Time Granularity
granularity = st.sidebar.radio(
    "Time Granularity",
    ["Daily", "Monthly"]
)

# Date Filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter Data
if len(date_range) == 2:
    start_date, end_date = date_range

    df = df[
        (df["Date"] >= pd.to_datetime(start_date))
        &
        (df["Date"] <= pd.to_datetime(end_date))
    ]

# Monthly View
if granularity == "Monthly":

    monthly = df.copy()

    monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)

    monthly = (
        monthly
        .groupby("Month")
        .sum(numeric_only=True)
        .reset_index()
    )

    monthly["Date"] = monthly["Month"]

    df = monthly

# ==========================================================
# KPIs
# ==========================================================

if granularity == "Daily":

    kpi = calculate_kpis(df)

else:

    temp = load_data()

    kpi = calculate_kpis(temp)

# ==========================================================
# TITLE
# ==========================================================

st.title("🏥 Healthcare Capacity & Care Load Dashboard")

st.markdown(
"""
Interactive Healthcare Analytics Dashboard for monitoring
CBP custody, HHS care, transfers and discharge trends.
"""
)

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Apprehended",
    f"{kpi['Total Apprehended']:,}"
)

c2.metric(
    "Average CBP",
    f"{kpi['Average CBP']:.2f}"
)

c3.metric(
    "Total Transfers",
    f"{kpi['Total Transfers']:,}"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Average HHS",
    f"{kpi['Average HHS']:.2f}"
)

c5.metric(
    "Total Discharged",
    f"{kpi['Total Discharged']:,}"
)

c6.metric(
    "Peak HHS",
    f"{kpi['Peak HHS']:,}"
)

st.divider()

# ==========================================================
# CHART 1
# ==========================================================

st.subheader("📈 Trend Analysis")

fig1 = px.line(
    df,
    x="Date",
    y=metric,
    markers=True,
    title=f"{metric} Over Time"
)

fig1.update_layout(
    template="plotly_white",
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================================
# CHART 2
# ==========================================================

st.subheader("📊 Recent Activity")

if granularity == "Daily":

    chart_df = df.tail(30)

else:

    chart_df = df

fig2 = px.bar(
    chart_df,
    x="Date",
    y=metric,
    title=f"{metric} Distribution"
)

fig2.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# CHART 3
# ==========================================================

st.subheader("📉 CBP vs HHS Comparison")

fig3 = px.line(
    df,
    x="Date",
    y=[
        "Children in CBP custody",
        "Children in HHS Care"
    ],
    title="CBP Custody vs HHS Care"
)

fig3.update_layout(
    template="plotly_white",
    height=500,
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================================
# MONTHLY SUMMARY
# ==========================================================

st.divider()

st.subheader("📅 Monthly Summary")

summary_df = load_data().copy()

summary_df["Month"] = summary_df["Date"].dt.strftime("%Y-%m")

monthly_summary = (
    summary_df
    .groupby("Month")
    [
        [
            "Children apprehended and placed in CBP custody*",
            "Children in CBP custody",
            "Children transferred out of CBP custody",
            "Children in HHS Care",
            "Children discharged from HHS Care"
        ]
    ]
    .sum()
    .reset_index()
)

st.dataframe(
    monthly_summary,
    use_container_width=True,
    height=300
)

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.divider()

st.subheader("📋 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True,
    height=350
)

# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.divider()

st.subheader("📥 Download Filtered Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Healthcare_Filtered_Data.csv",
    mime="text/csv"
)

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.divider()

st.subheader("📊 Dashboard Summary")

col1, col2 = st.columns(2)

with col1:

    st.info(f"""
### Dataset Information

- **Total Records:** {len(df)}

- **Selected Metric:** {metric}

- **Time Granularity:** {granularity}

- **Start Date:** {date_range[0]}

- **End Date:** {date_range[1]}
""")

with col2:

    st.success("""
### Dashboard Features

✅ KPI Summary Cards

✅ Interactive Charts

✅ Date Range Filter

✅ Metric Toggle

✅ Time Granularity

✅ Monthly Summary

✅ Dataset Preview

✅ Download CSV

✅ Healthcare Trend Analysis
""")

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.divider()

with st.expander("ℹ️ Project Information"):

    st.markdown("""
### Healthcare Capacity & Care Load Analytics Dashboard

This dashboard provides interactive analysis of healthcare capacity,
children in CBP custody, HHS care, transfers and discharge trends.

### Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- Statistics
- ARIMA Forecasting

### Developed For

UMPL Data Analytics Internship
""")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
<div style="text-align:center; padding:15px;">

### 🏥 Healthcare Capacity & Care Load Analytics Dashboard

**Developed using Python, Streamlit, Pandas & Plotly**

**Developer:** Shraddha Patil

**Project:** UMPL Data Analytics Internship

</div>
""",
    unsafe_allow_html=True
)