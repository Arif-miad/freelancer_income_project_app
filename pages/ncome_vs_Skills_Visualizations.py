import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📈 Income vs Skills Visualizations")

df = pd.read_csv("dataset/freelancer_earnings - freelancer_earnings_vs_skillstack_dataset.csv")
df["annual_income_usd"] = df["annual_income_usd"].replace('[\$,]', '', regex=True).astype(float)

st.write("### 🎯 Select Category")
category = st.selectbox("Choose Category", df["category"].unique())

filtered = df[df["category"] == category]

st.write("### 📌 Filtered Data")
st.dataframe(filtered)

# Plot 1 – Experience vs Hourly rate
st.write("### 📊 Experience vs Hourly Rate")

fig1 = plt.figure()
sns.scatterplot(data=filtered, x="years_experience", y="hourly_rate_usd", hue="experience_level")
st.pyplot(fig1)

# Plot 2 – Experience Level vs Annual Income
st.write("### 💰 Income Across Experience Levels")

fig2 = plt.figure()
sns.boxplot(data=filtered, x="experience_level", y="annual_income_usd")
st.pyplot(fig2)

# Plot 3 – Skill vs Income (text only because high-card)
st.write("### 🛠 Skills Sample")
st.write(filtered[["primary_skills", "annual_income_usd"]].head(10))
