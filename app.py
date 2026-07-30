import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Healthcare Capacity & Care Load Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD CSS
# ==========================================================

#def load_css():
#    with open("assets/style.css") as f:
#      st.markdown(
 #           f"<style>{f.read()}</style>",
  #          unsafe_allow_html=True
  #      )

#load_css()

# ==========================================================
# HOME PAGE
# ==========================================================

st.title("🏥 Healthcare Capacity & Care Load Analytics")

st.markdown("""
## Welcome

This project provides an interactive Healthcare Analytics Dashboard
for monitoring children in CBP custody and HHS care.

### Features

- 📊 Interactive Dashboard
- 📈 KPI Analysis
- 📉 Forecasting (ARIMA)
- 📁 Dataset Explorer
- ℹ️ About Project

👈 Select a page from the sidebar to begin.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info("""
### 🎯 Project Objective

- Monitor Healthcare Capacity
- Analyze Healthcare Trends
- Track Transfers
- Forecast Future Demand
""")

with col2:
    st.success("""
### 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- ARIMA
- Statistics
""")

st.divider()

st.caption("Developed for UMPL Data Analytics Internship")
