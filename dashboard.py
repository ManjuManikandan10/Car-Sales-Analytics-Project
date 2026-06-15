import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Car Sales Real-Time Dashboard", layout="wide")

# Title
st.title("🚗 Car Sales & Service Real-Time Dashboard")
st.markdown("### Interactive visualization of your Final Assignment dataset")

# File path
FILE_PATH = r'd:\sale\CarSalesByModelEnd.xlsx'

if not os.path.exists(FILE_PATH):
    st.error(f"Data file not found at {FILE_PATH}. Please run the data generator first.")
else:
    # Load data from the first sheet
    df = pd.read_excel(FILE_PATH, sheet_name='Sheet1')
    
    # Sidebar logo
    if os.path.exists(r'd:\sale\logo.png'):
        st.sidebar.image(r'd:\sale\logo.png')
        
    # Sidebar Filters
    st.sidebar.header("Filters")
    region_filter = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
    model_filter = st.sidebar.multiselect("Select Model", options=df['Model'].unique(), default=df['Model'].unique())
    
    filtered_df = df[(df['Region'].isin(region_filter)) & (df['Model'].isin(model_filter))]
    
    # Top Metrics
    total_sales = filtered_df['Sale_Price'].sum()
    total_profit = filtered_df['Profit'].sum()
    avg_rating = filtered_df['Customer_Rating'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales Revenue", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Avg. Customer Rating", f"{avg_rating:.1f} / 10")
    col4.metric("Total Records", len(filtered_df))
    
    st.divider()
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Quantity Sold by Dealer ID")
        qty_by_dealer = filtered_df.groupby('Dealer ID')['Quantity Sold'].sum().reset_index()
        fig1 = px.bar(qty_by_dealer, x='Dealer ID', y='Quantity Sold', color='Dealer ID', text_auto=True)
        st.plotly_chart(fig1, width='stretch')
        
    with c2:
        st.subheader("Profit Trend Over Time")
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
        trend_df = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Profit'].sum().reset_index()
        trend_df['Date'] = trend_df['Date'].astype(str)
        fig2 = px.line(trend_df, x='Date', y='Profit', markers=True, line_shape='spline')
        st.plotly_chart(fig2, width='stretch')
        
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Profit by Region")
        rev_by_region = filtered_df.groupby('Region')['Profit'].sum().reset_index()
        fig3 = px.pie(rev_by_region, values='Profit', names='Region', hole=0.4)
        st.plotly_chart(fig3, width='stretch')
        
    with c4:
        st.subheader("Quantity Sold by Model")
        model_counts = filtered_df.groupby('Model')['Quantity Sold'].sum().reset_index()
        fig4 = px.bar(model_counts, x='Quantity Sold', y='Model', orientation='h', color='Quantity Sold', color_continuous_scale='Viridis')
        st.plotly_chart(fig4, width='stretch')

    # Data Table
    with st.expander("View Raw Assignment Data"):
        st.dataframe(filtered_df)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard updated to match your 11/11 Assignment version.")
