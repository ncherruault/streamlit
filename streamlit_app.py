import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 6th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# ============================================================
# YOUR ADDITIONS
# ============================================================

st.write("## Your additions")

# ------------------------------------------------------------
# 1. Dropdown for Category
# ------------------------------------------------------------

st.write("### Select a Category")

category_options = sorted(df["Category"].dropna().unique())

selected_category = st.selectbox(
    "Category",
    category_options
)


# ------------------------------------------------------------
# 2. Multi-select for Sub_Category within selected Category
# ------------------------------------------------------------

category_df = df[df["Category"] == selected_category]

subcategory_options = sorted(
    category_df["Sub_Category"].dropna().unique()
)

selected_subcategories = st.multiselect(
    "Select Sub-Categories",
    subcategory_options,
    default=subcategory_options
)


# ------------------------------------------------------------
# Filter data based on selections
# ------------------------------------------------------------

filtered_df = category_df[
    category_df["Sub_Category"].isin(selected_subcategories)
]


# ------------------------------------------------------------
# 3. Line chart of sales for selected Sub-Categories
# ------------------------------------------------------------

st.write("### Sales Over Time")

sales_selected = (
    filtered_df
    .filter(items=["Sales"])
    .groupby(pd.Grouper(freq="M"))
    .sum()
)

st.line_chart(
    sales_selected,
    y="Sales"
)


# ------------------------------------------------------------
# 4. Metrics: Sales, Profit, Profit Margin
# ------------------------------------------------------------

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

if total_sales != 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0


# ------------------------------------------------------------
# 5. Compare selected profit margin to overall profit margin
# ------------------------------------------------------------

overall_sales = df["Sales"].sum()
overall_profit = df["Profit"].sum()

overall_profit_margin = (
    overall_profit / overall_sales
) * 100

margin_difference = profit_margin - overall_profit_margin


# Display the three metrics side by side

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

with col3:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%",
        delta=f"{margin_difference:.2f}% vs overall"
    )
