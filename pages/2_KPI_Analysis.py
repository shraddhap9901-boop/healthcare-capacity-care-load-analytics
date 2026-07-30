import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.helper import load_data

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------

st.set_page_config(
    page_title="KPI Analysis",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

df = load_data()

if df.empty:
    st.error("Dataset could not be loaded.")
    st.stop()

# ----------------------------------------------------------
# Title
# ----------------------------------------------------------

st.title("📈 KPI Analysis Dashboard")
st.markdown("Detailed analysis of Healthcare Capacity & Care Load")

st.divider()

# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

st.sidebar.header("Analysis Filter")

metric = st.sidebar.selectbox(
    "Select KPI",
    [
        "Children apprehended and placed in CBP custody*",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]
)

# ----------------------------------------------------------
# Summary Statistics
# ----------------------------------------------------------

st.subheader("Summary Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average", f"{df[metric].mean():,.2f}")
c2.metric("Maximum", f"{df[metric].max():,.0f}")
c3.metric("Minimum", f"{df[metric].min():,.0f}")
c4.metric("Total", f"{df[metric].sum():,.0f}")

st.divider()

# ----------------------------------------------------------
# Trend Analysis
# ----------------------------------------------------------

st.subheader("Trend Analysis")

fig1 = px.line(
    df,
    x="Date",
    y=metric,
    markers=True,
    title=f"{metric} Over Time"
)

fig1.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------------------------------
# Distribution
# ----------------------------------------------------------

st.subheader("Distribution")

fig2 = px.histogram(
    df,
    x=metric,
    nbins=25,
    title=f"Distribution of {metric}"
)

fig2.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------------
# Box Plot
# ----------------------------------------------------------

st.subheader("Box Plot")

fig3 = px.box(
    df,
    y=metric,
    title=f"Box Plot - {metric}"
)

fig3.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------------

st.subheader("Correlation Matrix")

corr = df[
    [
        "Children apprehended and placed in CBP custody*",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]
].corr()

heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="Blues",
        text=corr.round(2),
        texttemplate="%{text}"
    )
)

heatmap.update_layout(
    height=650
)

st.plotly_chart(heatmap, use_container_width=True)

# ----------------------------------------------------------
# Monthly Average
# ----------------------------------------------------------

st.subheader("Monthly Average Trend")

monthly = df.copy()

monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)

monthly_avg = (
    monthly.groupby("Month")[metric]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    monthly_avg,
    x="Month",
    y=metric,
    title="Monthly Average"
)

fig4.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------------
# Raw Data
# ----------------------------------------------------------

st.subheader("Dataset")

st.dataframe(
    df,
    use_container_width=True
)
