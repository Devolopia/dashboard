import streamlit as st
import pandas as pd

def render_filters(df):
    """Render cascading sidebar filters and return the selected values."""
    
    if df is None or df.empty:
        st.sidebar.warning("No data available for filtering.")
        return [], [], [], None, None
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dashboard Filters")
    
    # 1. Brand Filter (Top Level)
    brands = sorted(df['Brand'].dropna().unique().tolist())
    sel_brand = st.sidebar.multiselect("Brand", brands, placeholder="All Brands")
    
    # 2. BC Filter (Cascades from Brand)
    df_bc = df.copy()
    if sel_brand:
        df_bc = df_bc[df_bc['Brand'].isin(sel_brand)]
    bcs = sorted(df_bc['BC'].dropna().unique().tolist())
    sel_bc = st.sidebar.multiselect("Business Center (BC)", bcs, placeholder="All BCs")
    
    # 3. Nameplate Filter (Cascades from Brand and BC)
    df_np = df_bc.copy()
    if sel_bc:
        df_np = df_np[df_np['BC'].isin(sel_bc)]
    nameplates = sorted(df_np['Nameplate'].dropna().unique().tolist())
    sel_nameplate = st.sidebar.multiselect("Nameplate", nameplates, placeholder="All Nameplates")
    
    # 4. Date Range Filter
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)
            
    return sel_brand, sel_nameplate, sel_bc, start_date, end_date
