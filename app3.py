import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#page
st.set_page_config(layout="wide")

#data
df = pd.read_csv("train.csv")

#title
st.markdown("<h1 style='text-align: center;'>📊 Sales Performance Dashboard</h1>", unsafe_allow_html=True)
st.write("Interactive dashboard to analyze sales performance.")

#sidebar
city = st.sidebar.selectbox("Select City", df["City"].unique())

#filtered data
filtered_df = df[df["City"] == city]

#KPI
total_sales = filtered_df["Sales"].sum()
st.metric("Total Sales", f"${total_sales:,.0f}")

#category (filtered)
cat_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

#top cities (global)
top_cities = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

#region
selected_region = df[df["City"] == city]["Region"].iloc[0]

region_filtered = df[df["Region"] == selected_region]

region_cat = (
    region_filtered.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

#seçilen city'nin region'ı
selected_region = df[df["City"] == city]["Region"].iloc[0]

#figure
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("Sales by Category", "Top 10 Cities", "Selected Region Breakdown")
)

#Category
fig.add_trace(
    go.Bar(
        x=cat_sales["Category"],
        y=cat_sales["Sales"],
        text=[f"${x:,.0f}" for x in cat_sales["Sales"]],
        textposition="outside",
        name="Category"
    ),
    row=1, col=1
)

#Top Cities
fig.add_trace(
    go.Bar(
        x=top_cities["City"],
        y=top_cities["Sales"],
        text=[f"${x:,.0f}" for x in top_cities["Sales"]],
        textposition="outside",
        name="Cities"
    ),
    row=1, col=2
)

#Region
fig.add_trace(
    go.Bar(
        x=region_cat["Category"],
        y=region_cat["Sales"],
        name=selected_region,
        text=[f"${x:,.0f}" for x in region_cat["Sales"]],
        textposition="outside"
    ),
    row=1, col=3
)

#layout
fig.update_layout(
    template="plotly_white",
    height=500,
    showlegend=True
)

#show
st.plotly_chart(fig, width="stretch")