import streamlit as st
import pandas as pd

st.title("📊 Freelancer Overview Metrics")

# Load dataset
df = pd.read_csv("dataset/freelancer_earnings - freelancer_earnings_vs_skillstack_dataset.csv")

# Clean income column
df["annual_income_usd"] = df["annual_income_usd"].replace('[\$,]', '', regex=True).astype(float)

st.write("### 🧾 Dataset Preview")
st.dataframe(df.head())

st.write("### 🔍 Basic Information")
st.write(df.shape)
st.write(df.describe())

# KPI Section
st.write("## 🧮 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Hourly Rate ($)", round(df["hourly_rate_usd"].mean(), 2))

with col2:
    st.metric("Average Annual Income ($)", round(df["annual_income_usd"].mean(), 2))

with col3:
    st.metric("Total Freelancers", df["freelancer_id"].nunique())

st.write("### 🔢 Experience Level Distribution")
st.write(df["experience_level"].value_counts())
