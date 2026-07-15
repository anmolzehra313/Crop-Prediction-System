import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_processing import load_and_preprocess_data
from utils.visualizations import (
    plot_correlation_matrix, plot_label_distribution_count, plot_label_distribution_pie,
    plot_histograms, plot_kde, plot_boxplots, plot_ph_bar, plot_rainfall_pie,
    plot_npk_histogram, plot_min_max_temp
)

# Set page config
st.set_page_config(page_title="🌾 Crop Prediction System", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; }
    .stTextInput>div>input { border-radius: 8px; }
    .stFileUploader>div { border-radius: 8px; }
    .stSidebar { background-color: #212121; }
    h1, h2, h3 { color: #2e7d32; }
    .metric-card { background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# Load and preprocess data
try:
    df, label_encoder, scaler, selector = load_and_preprocess_data('Crops_recommendation (2).csv')
except FileNotFoundError:
    st.error("Dataset file 'Crops_recommendation (2).csv' not found. Please ensure it is in the project directory.")
    st.stop()

# Sidebar
st.sidebar.title("🌱 Crop Prediction System")
st.sidebar.markdown("Navigate through the app to explore data or predict crops.")
page = st.sidebar.radio("Go to", ["Home", "CSV Upload", "Manual Input"])

if page == "Home":
    st.title("🌾 Crop Prediction System")
    st.markdown("""
        Welcome to the **Crop Prediction System**! This application helps farmers predict optimal crops based on soil and environmental conditions. 
        Use the sidebar to:
        - **Explore** dataset insights and visualizations.
        - **Upload** a CSV file for batch predictions.
        - **Input** parameters manually for single predictions.
    """)

    # Dashboard with key metrics
    st.header("📊 Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Samples", df.shape[0])
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Crops", df['label'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Missing Values", df.isnull().sum().sum())
        st.markdown('</div>', unsafe_allow_html=True)

    # EDA Section
    with st.expander("Exploratory Data Analysis (EDA)", expanded=True):
        st.subheader("Dataset Overview")
        st.write("**Column Names:**")
        st.write(df.columns.tolist())
        st.write("**Data Types:**")
        st.write(df.dtypes)
        st.write("**Summary Statistics:**")
        st.dataframe(df.describe())
        st.write("**Missing Values:**")
        st.write(df.isnull().sum().sum())
        st.write("**Standard Deviation:**")
        st.write(df.std(numeric_only=True))
        st.write("**Unique Values:**")
        st.write(df.nunique())
        st.write(f"**Average Nitrogen Ratio:** {df['N'].mean():.2f}")
        st.write(f"**Average Phosphorous Ratio:** {df['P'].mean():.2f}")
        st.write(f"**Average Potassium Ratio:** {df['K'].mean():.2f}")
        st.write(f"**Average Temperature (C):** {df['temperature'].mean():.2f}")
        st.write(f"**Average Humidity:** {df['humidity'].mean():.2f}")
        st.write(f"**Average pH Value:** {df['ph'].mean():.2f}")
        st.write(f"**Average Rainfall:** {df['rainfall'].mean():.2f}")

        # Styled DataFrame
        numeric_columns = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label_encoded']]
        df2 = numeric_columns.groupby('label_encoded').mean()
        st.write("**Mean Values by Label:**")
        st.dataframe(df2.style.background_gradient(cmap='coolwarm'))

    # Visualizations
    with st.expander("Data Visualizations", expanded=False):
        st.subheader("Visual Insights")
        st.write("**Correlation Matrix**")
        fig = plot_correlation_matrix(df)
        st.pyplot(fig)

        st.write("**Label Distribution (Count Plot)**")
        fig = plot_label_distribution_count(df)
        st.pyplot(fig)

        st.write("**Label Distribution (Pie Chart)**")
        fig = plot_label_distribution_pie(df)
        st.pyplot(fig)

        st.write("**Histograms**")
        figs = plot_histograms(df)
        for fig in figs:
            st.pyplot(fig)

        st.write("**Kernel Density Estimation (KDE) Plots**")
        fig = plot_kde(df)
        st.pyplot(fig)

        st.write("**Outlier Detection (Boxplots)**")
        fig = plot_boxplots(df)
        st.pyplot(fig)

        st.write("**Average pH Required for Each Label**")
        fig = plot_ph_bar(df)
        st.pyplot(fig)

        st.write("**Top 5 Crops with Maximum Rainfall**")
        fig = plot_rainfall_pie(df)
        st.pyplot(fig)

        st.write("**Distribution of NPK Nutrient Concentrations**")
        fig = plot_npk_histogram(df)
        st.pyplot(fig)

        st.write("**Minimum and Maximum Temperature Required for Each Crop**")
        fig1, fig2 = plot_min_max_temp(df)
        st.pyplot(fig1)
        st.pyplot(fig2)