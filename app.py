import streamlit as st
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Freelancer Income Dashboard",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# Title & Description
# -----------------------------
st.title("💼 Freelancer Income vs Skills Dashboard & ML App")

st.markdown("""
This interactive dashboard helps you analyze **freelancer earnings** based on  
skills, experience, location, education, and platforms.

Navigate using the sidebar to explore:

👉 Overview Metrics  
👉 Income vs Skills Visualizations  
👉 Country & Region Analysis  
👉 ML Prediction App  
""")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/freelancer_earnings - freelancer_earnings_vs_skillstack_dataset.csv")
    df["annual_income_usd"] = df["annual_income_usd"].replace('[\$,]', '', regex=True).astype(float)
    return df

df = load_data()

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# Quick KPIs
# -----------------------------
st.subheader("⚡ Quick Stats & Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Freelancers", df["freelancer_id"].nunique())

with col2:
    st.metric("Average Hourly Rate ($)", round(df["hourly_rate_usd"].mean(), 2))

with col3:
    st.metric("Average Annual Income ($)", round(df["annual_income_usd"].mean(), 2))

with col4:
    st.metric("Number of Countries", df["country"].nunique())

# -----------------------------
# Footer
# -----------------------------
st.write("---")
st.markdown("""
✅ **Pages are available in the Sidebar**  
📌 Developed with Streamlit  
""")
