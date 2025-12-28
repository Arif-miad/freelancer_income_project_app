import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🌍 Country & Region Income Analysis")

df = pd.read_csv("dataset/freelancer_earnings - freelancer_earnings_vs_skillstack_dataset.csv")
df["annual_income_usd"] = df["annual_income_usd"].replace('[\$,]', '', regex=True).astype(float)

# Region dropdown
region = st.selectbox("Select Region", df["region"].unique())
region_df = df[df["region"] == region]

st.write("### 🗺 Freelancers in Selected Region")
st.dataframe(region_df[["freelancer_id", "country", "category", "annual_income_usd"]])

# Bar chart: country vs income
st.write("### 💵 Average Income by Country")

country_income = region_df.groupby("country")["annual_income_usd"].mean().sort_values()

fig1 = plt.figure()
sns.barplot(x=country_income.values, y=country_income.index)
st.pyplot(fig1)

# Platform comparison
st.write("### 🧑‍💻 Platform-wise Income")

platform_income = region_df.groupby("primary_platform")["annual_income_usd"].mean().sort_values()

fig2 = plt.figure()
sns.barplot(x=platform_income.values, y=platform_income.index)
st.pyplot(fig2)
