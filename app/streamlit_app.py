import streamlit as st
import pandas as pd
import os
# Only load the file. Don't attempt to run main.py via subprocess
DATA_PATH = os.path.join("data", "processed", "final_dataset.csv")

st.set_page_config(page_title="E-commerce Product Return Dashboard", layout="wide")
st.title("📦 E-commerce Product Return Dashboard")

# ---------------- CONFIG ---------------- #
DATA_PATH = os.path.join("data", "processed", "final_dataset.csv")
st.set_page_config(
    page_title="E-commerce Product Return Dashboard",
    layout="wide",
    page_icon="📦",
)

# ---------------- HEADER ---------------- #
st.markdown("<h1 style='color:#F5A623;'>📦 E-commerce Product Return Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='color:#CCCCCC;'>Analyze return trends, customer behavior, and product performance in one glance.</h5>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- LOAD DATA ---------------- #
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    if 'city' in df.columns and 'location' not in df.columns:
        df.rename(columns={'city': 'location'}, inplace=True)

    # Sidebar Filters
    with st.sidebar:
        st.markdown("### 🔍 Filter Options")
        category_filter = st.multiselect("Filter by Category", df['category'].dropna().unique())
        location_filter = []
        if 'location' in df.columns:
            location_filter = st.multiselect("Filter by Location", df['location'].dropna().unique())

    # Apply Filters
    filtered_df = df.copy()
    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    if location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]

    # Return Summary
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

    # Monthly Return Trends
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

    # Risky Customers
    st.subheader("🚩 Risky Customers (3+ returns)")
    risky = filtered_df[filtered_df["is_returned"]].groupby("user_id")["order_id"].count()
    risky = risky[risky > 2].reset_index(name="return_count")
    st.dataframe(risky)

    # Loyal Customers
    st.subheader("🎯 Loyal Customers (0 returns)")
    returned_users = filtered_df[filtered_df["is_returned"] == True]["user_id"].unique()
    loyal_customers = filtered_df[~filtered_df["user_id"].isin(returned_users)]["user_id"].unique()
    st.write("Number of Loyal Customers:", len(loyal_customers))
    st.dataframe(loyal_customers)

else:
    st.error("⚠️ Processed data not found. Run `main.py` to generate 'final_dataset.csv'.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built by Charan Kammili • Source on <a href='https://github.com/CharanKammili/ecommerce-return-analysis' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
