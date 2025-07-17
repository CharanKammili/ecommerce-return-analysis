import streamlit as st
import pandas as pd
import os
import os
import subprocess

# Auto-generate the dataset if it doesn't exist
if not os.path.exists("data/processed/final_dataset.csv"):
    try:
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        st.error("❌ Failed to generate processed data. Please check 'main.py'.")
        st.stop()


# Load dataset
DATA_PATH = os.path.join("data", "processed", "final_dataset.csv")

st.set_page_config(page_title="E-commerce Product Return Dashboard", layout="wide")
st.title("📦 E-commerce Product Return Dashboard")

# Load Data
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    # ✅ Standardize column name
    if 'city' in df.columns and 'location' not in df.columns:
        df.rename(columns={'city': 'location'}, inplace=True)

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    category_filter = st.sidebar.multiselect("Filter by Category", df['category'].dropna().unique())

    location_filter = []
    if 'location' in df.columns:
        location_filter = st.sidebar.multiselect("Filter by Location", df['location'].dropna().unique())

    # Apply Filters
    filtered_df = df.copy()
    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    if location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]

    # Metrics
    st.subheader("📊 Return Summary")
    total_orders = len(filtered_df)
    returned_orders = filtered_df["is_returned"].sum()
    return_rate = round((returned_orders / total_orders) * 100, 2) if total_orders > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", total_orders)
    col2.metric("Returned Orders", returned_orders)
    col3.metric("Return Rate", f"{return_rate} %")

    # Returns by Category
    st.subheader("🧺 Returns by Category")
    category_data = filtered_df[filtered_df['is_returned']].groupby("category")["order_id"].count()
    st.bar_chart(category_data)

    # Returns by Location
    if 'location' in filtered_df.columns:
        st.subheader("📍 Returns by Location")
        city_data = filtered_df[filtered_df['is_returned']].groupby("location")["order_id"].count()
        st.bar_chart(city_data)

    # Monthly Trend
    if 'timestamp' in df.columns:
        st.subheader("📆 Monthly Return Trends")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month'] = df['timestamp'].dt.to_period('M')
        trend = df[df['is_returned']].groupby('month')['order_id'].count()
        st.line_chart(trend)

    # Most Returned Products
    if 'product_name' in df.columns:
        st.subheader("📦 Most Returned Products")
        top_products = filtered_df[filtered_df['is_returned']].groupby('product_name')['order_id'].count().sort_values(ascending=False).head(10)
        st.bar_chart(top_products)

    # Risky Customers (3+ returns)
    st.subheader("🚩 Risky Customers")
    risky = filtered_df[filtered_df["is_returned"]].groupby("user_id")["order_id"].count()
    risky = risky[risky > 2].reset_index(name="return_count")
    st.dataframe(risky)

    # Loyal Customers (0 returns)
    st.subheader("🎯 Loyal Customers")
    returned_users = filtered_df[filtered_df["is_returned"] == True]["user_id"].unique()
    loyal_customers = filtered_df[~filtered_df["user_id"].isin(returned_users)]["user_id"].unique()
    st.write("Number of Loyal Customers:", len(loyal_customers))
    st.dataframe(loyal_customers)
else:
    st.error("⚠️ Processed data not found. Run `main.py` to generate 'final_dataset.csv'.")
