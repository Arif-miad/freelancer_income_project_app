import streamlit as st
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Freelancer Dashboard",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# Top Banner Image
# -----------------------------
# Replace with your own banner image path
banner_image = "image/demo.PNG"  
image = Image.open(banner_image)
st.image(image, use_column_width=True)

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
# Horizontal Navigation
# -----------------------------
st.write("")  # spacing
pages = ["Overview Metrics", "Income vs Skills", "Country & Region Analysis", "ML Prediction App"]
page = st.radio("Navigate", pages, horizontal=True)

# -----------------------------
# Page Logic
# -----------------------------
if page == "Overview Metrics":
    st.header("📊 Overview Metrics")
    st.dataframe(df.head())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Freelancers", df["freelancer_id"].nunique())
    with col2:
        st.metric("Average Hourly Rate ($)", round(df["hourly_rate_usd"].mean(), 2))
    with col3:
        st.metric("Average Annual Income ($)", round(df["annual_income_usd"].mean(), 2))
    with col4:
        st.metric("Number of Countries", df["country"].nunique())

elif page == "Income vs Skills":
    st.header("📈 Income vs Skills Visualizations")
    import seaborn as sns
    import matplotlib.pyplot as plt

    category = st.selectbox("Select Category", df["category"].unique())
    filtered = df[df["category"] == category]

    fig1 = plt.figure(figsize=(8,4))
    sns.scatterplot(data=filtered, x="years_experience", y="hourly_rate_usd", hue="experience_level")
    st.pyplot(fig1)

    fig2 = plt.figure(figsize=(8,4))
    sns.boxplot(data=filtered, x="experience_level", y="annual_income_usd")
    st.pyplot(fig2)

elif page == "Country & Region Analysis":
    st.header("🌍 Country & Region Analysis")
    region = st.selectbox("Select Region", df["region"].unique())
    region_df = df[df["region"] == region]

    st.dataframe(region_df[["freelancer_id", "country", "category", "annual_income_usd"]])

    fig = plt.figure(figsize=(8,4))
    country_income = region_df.groupby("country")["annual_income_usd"].mean().sort_values()
    sns.barplot(x=country_income.values, y=country_income.index)
    st.pyplot(fig)



# -----------------------------
# Footer with Links
# -----------------------------
st.write("---")
st.markdown("""
<div style='text-align:center'>
<p>Developed by <b>Your Name</b></p>
<p>
<a href="https://www.youtube.com/" target="_blank">YouTube</a> |
<a href="https://www.kaggle.com/" target="_blank">Kaggle</a> |
<a href="https://github.com/" target="_blank">GitHub</a>
</p>
</div>
""", unsafe_allow_html=True)
