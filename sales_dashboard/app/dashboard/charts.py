import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_sales_trend_chart(df):
    """Render the main sales trend line chart with missing data marked."""
    if df is None or df.empty:
        st.info("No data available for the selected filters to generate chart.")
        return
        
    daily_sales = df.groupby('Date', as_index=False)['Sales'].sum()
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
    
    min_date = daily_sales['Date'].min()
    max_date = daily_sales['Date'].max()
    
    # Create complete date range
    all_dates = pd.date_range(start=min_date, end=max_date)
    all_dates_df = pd.DataFrame({'Date': all_dates})
    
    # Merge to find missing dates (they will have NaN in Sales)
    merged = pd.merge(all_dates_df, daily_sales, on='Date', how='left')
    
    # Missing dates
    missing_data = merged[merged['Sales'].isna()].copy()
    
    # Convert dates to strings to force Plotly to use discrete categories (removes time interpolation)
    merged['DateStr'] = merged['Date'].dt.strftime('%Y-%m-%d')
    if not missing_data.empty:
        missing_data['DateStr'] = missing_data['Date'].dt.strftime('%Y-%m-%d')
    
    fig = go.Figure()
    
    # Add actual sales line
    fig.add_trace(go.Scatter(
        x=merged['DateStr'],
        y=merged['Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(shape='linear'),
        connectgaps=False, # Ensures the line breaks on missing days
        hovertemplate='Date: %{x}<br>Sales: %{y:,.0f}<extra></extra>'
    ))
    
    # Add red dots on zero for missing dates
    if not missing_data.empty:
        fig.add_trace(go.Scatter(
            x=missing_data['DateStr'],
            y=[0] * len(missing_data),
            mode='markers',
            name='Missing Data',
            marker=dict(color='red', size=10, symbol='circle'),
            hovertemplate='Missing Data<br>Date: %{x}<br>Sales: 0<extra></extra>'
        ))
        
    fig.update_layout(
        title="Sales Trend",
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(type='category', tickangle=-45) # Enforce discrete categories, angled for readability
    )
    
    st.plotly_chart(fig, use_container_width=True)
