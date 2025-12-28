import streamlit as st
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Freelancer Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Dark/Light Theme Toggle
# -----------------------------
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp { background-color: #111; color: #eee; }
        </style>
        """, unsafe_allow_html=True
    )

# -----------------------------
# Top Banner Image
# -----------------------------
banner_image = "image/demo.PNG"  # Replace with your image path
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

    category = st.selectbox("Select Category", df["category"].unique())
    filtered = df[df["category"] == category]

    st.write("### Experience vs Hourly Rate")
    fig1 = plt.figure(figsize=(8,4))
    sns.scatterplot(data=filtered, x="years_experience", y="hourly_rate_usd", hue="experience_level")
    st.pyplot(fig1)

    st.write("### Experience Level vs Annual Income")
    fig2 = plt.figure(figsize=(8,4))
    sns.boxplot(data=filtered, x="experience_level", y="annual_income_usd")
    st.pyplot(fig2)

elif page == "Country & Region Analysis":
    st.header("🌍 Country & Region Analysis")

    region = st.selectbox("Select Region", df["region"].unique())
    region_df = df[df["region"] == region]

    st.dataframe(region_df[["freelancer_id", "country", "category", "annual_income_usd"]])

    st.write("### Average Income by Country")
    fig = plt.figure(figsize=(8,4))
    country_income = region_df.groupby("country")["annual_income_usd"].mean().sort_values()
    sns.barplot(x=country_income.values, y=country_income.index)
    st.pyplot(fig)

    st.write("### Platform-wise Average Income")
    fig2 = plt.figure(figsize=(8,4))
    platform_income = region_df.groupby("primary_platform")["annual_income_usd"].mean().sort_values()
    sns.barplot(x=platform_income.values, y=platform_income.index)
    st.pyplot(fig2)

elif page == "ML Prediction App":
    st.header("🤖 ML Prediction App")

    le = LabelEncoder()
    for col in ["category", "experience_level", "region", "education", "primary_platform", "country"]:
        df[col] = le.fit_transform(df[col])

    X = df[["years_experience", "hourly_rate_usd", "category", "region", "experience_level"]]
    y = df["annual_income_usd"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    st.subheader("Enter Your Details")
    years = st.number_input("Years of Experience", 0.0, 40.0, 3.0)
    hourly = st.number_input("Hourly Rate ($)", 1.0, 400.0, 50.0)
    category_input = st.selectbox("Category", df["category"].unique())
    region_input = st.selectbox("Region", df["region"].unique())
    exp_level_input = st.selectbox("Experience Level", df["experience_level"].unique())

    input_data = pd.DataFrame([[years, hourly, category_input, region_input, exp_level_input]],
                              columns=["years_experience", "hourly_rate_usd", "category", "region", "experience_level"])

    if st.button("Predict Annual Income"):
        pred = model.predict(input_data)[0]
        st.success(f"💰 Predicted Annual Income: ${round(pred,2)}")

# -----------------------------
# Footer with Social Icons
# -----------------------------
st.write("---")
st.markdown("""
<div style='text-align:center'>
<p>Developed by <b>Your Name</b></p>
<p>
<a href="https://www.youtube.com/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/1384/1384060.png" width="24"/> YouTube
</a> &nbsp; | &nbsp;
<a href="https://www.kaggle.com/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/196/196566.png" width="24"/> Kaggle
</a> &nbsp; | &nbsp;
<a href="https://github.com/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/25/25231.png" width="24"/> GitHub
</a>
</p>
</div>
""", unsafe_allow_html=True)
