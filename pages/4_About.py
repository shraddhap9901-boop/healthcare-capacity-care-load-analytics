import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("ℹ️ About This Project")

st.markdown("---")

# ==========================================================
# PROJECT DESCRIPTION
# ==========================================================

st.header("🏥 Healthcare Capacity & Care Load Analytics")

st.write("""
This project is an interactive healthcare analytics dashboard developed
using Python and Streamlit.

The dashboard helps monitor healthcare capacity, care load,
patient transfers and future trends using data visualization
and forecasting techniques.
""")

# ==========================================================
# OBJECTIVES
# ==========================================================

st.header("🎯 Project Objectives")

st.markdown("""
- Monitor Healthcare Capacity
- Analyze Care Load
- Track Patient Transfers
- Visualize Healthcare Trends
- Forecast Future Healthcare Demand
""")

# ==========================================================
# TECHNOLOGIES
# ==========================================================

st.header("🛠 Technologies Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### Programming

- Python
- Pandas
- NumPy
- Streamlit
""")

with col2:
    st.markdown("""
### Visualization

- Plotly
- ARIMA Forecasting
- Statistics
- Data Analytics
""")

# ==========================================================
# FEATURES
# ==========================================================

st.header("✨ Dashboard Features")

st.markdown("""
✅ Interactive Dashboard

✅ KPI Analysis

✅ Healthcare Trend Analysis

✅ ARIMA Forecasting

✅ Download Forecast Results

✅ Interactive Charts

✅ Date Filters

✅ Dataset Preview
""")

# ==========================================================
# DEVELOPER
# ==========================================================

st.header("👩‍💻 Developer")

st.info("""
Name : Shraddha Patil

Degree : M.Sc. Statistics

Role : Data Analytics Intern

Project : Healthcare Capacity & Care Load Analytics Dashboard
""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.success(
    "Developed using Python, Streamlit, Plotly and Machine Learning."
)
