import pandas as pd
import streamlit as st
from pathlib import Path


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    try:

        file_path = Path(__file__).parent.parent / "data" / "data.csv"

        df = pd.read_csv(file_path)

        # Remove spaces from column names
        df.columns = df.columns.str.strip()

        # Convert Date
        df["Date"] = pd.to_datetime(df["Date"])

        # Numeric Columns
        numeric_cols = [
            "Children apprehended and placed in CBP custody*",
            "Children in CBP custody",
            "Children transferred out of CBP custody",
            "Children in HHS Care",
            "Children discharged from HHS Care"
        ]

        for col in numeric_cols:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        df = df.sort_values("Date")

        return df

    except Exception as e:

        st.error(f"Dataset Loading Error : {e}")

        return pd.DataFrame()


# ==========================================================
# KPI Calculation
# ==========================================================

def calculate_kpis(df):

    return {

        "Total Apprehended":
            int(df["Children apprehended and placed in CBP custody*"].sum()),

        "Average CBP":
            round(df["Children in CBP custody"].mean(), 2),

        "Total Transfers":
            int(df["Children transferred out of CBP custody"].sum()),

        "Average HHS":
            round(df["Children in HHS Care"].mean(), 2),

        "Total Discharged":
            int(df["Children discharged from HHS Care"].sum()),

        "Peak HHS":
            int(df["Children in HHS Care"].max())
    }
