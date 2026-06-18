import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("### Capstone Project")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload E-Commerce Dataset",
    type=["csv"]
)

if uploaded_file:

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------
    df = pd.read_csv(uploaded_file)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # ---------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    # Date Filter
    start_date = st.sidebar.date_input(
        "Start Date",
        df["Order Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        df["Order Date"].max()
    )

    filtered_df = df[
        (df["Region"].isin(region)) &
        (df["Category"].isin(category)) &
        (df["Order Date"] >= pd.to_datetime(start_date)) &
        (df["Order Date"] <= pd.to_datetime(end_date))
    ]

    # ---------------------------------------------------
    # KPIs
    # ---------------------------------------------------
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order ID"].nunique()
    total_customers = filtered_df["Customer ID"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

    col2.metric(
        "📈 Total Profit",
        f"${total_profit:,.0f}"
    )

    col3.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

    col4.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

    st.divider()

    # ---------------------------------------------------
    # SALES TREND
    # ---------------------------------------------------
    st.subheader("📈 Monthly Sales Trend")

    monthly_sales = (
        filtered_df
        .groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = \
        monthly_sales["Order Date"].astype(str)

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------------------
    # REGION & CATEGORY ANALYSIS
    # ---------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:

        region_sales = (
            filtered_df
            .groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            color="Region",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    with col2:

        category_sales = (
            filtered_df
            .groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig_category = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.5
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # ---------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # ---------------------------------------------------
    # CUSTOMER ANALYSIS
    # ---------------------------------------------------
    st.subheader("👥 Top Customers")

    top_customers = (
        filtered_df
        .groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_customer = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        color="Sales"
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

    # ---------------------------------------------------
    # PROFIT ANALYSIS
    # ---------------------------------------------------
    st.subheader("💹 Profit vs Sales")

    fig_profit = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Product Name"],
        template="plotly_white"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    # ---------------------------------------------------
    # DISCOUNT IMPACT
    # ---------------------------------------------------
    if "Discount" in filtered_df.columns:

        st.subheader("🎯 Discount Impact")

        fig_discount = px.scatter(
            filtered_df,
            x="Discount",
            y="Profit",
            color="Category",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_discount,
            use_container_width=True
        )

    # ---------------------------------------------------
    # DATA TABLE
    # ---------------------------------------------------
    st.subheader("📋 Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # ---------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.info("Upload an E-Commerce CSV dataset.")