import pandas as pd

def filter_data(df, brands, nameplates, bcs, start_date, end_date):
    """Apply filters for Brand, Nameplate, BC, and Date Range to the dataframe."""
    if df is None or df.empty:
        return df
        
    filtered = df.copy()
    filtered['Date'] = pd.to_datetime(filtered['Date']).dt.date
    
    if brands and len(brands) > 0:
        if isinstance(brands, str) and brands != "All":
            filtered = filtered[filtered['Brand'] == brands]
        elif isinstance(brands, list) and "All" not in brands:
            filtered = filtered[filtered['Brand'].isin(brands)]
            
    if nameplates and len(nameplates) > 0:
        if isinstance(nameplates, str) and nameplates != "All":
            filtered = filtered[filtered['Nameplate'] == nameplates]
        elif isinstance(nameplates, list) and "All" not in nameplates:
            filtered = filtered[filtered['Nameplate'].isin(nameplates)]
            
    if bcs and len(bcs) > 0:
        if isinstance(bcs, str) and bcs != "All":
            filtered = filtered[filtered['BC'] == bcs]
        elif isinstance(bcs, list) and "All" not in bcs:
            filtered = filtered[filtered['BC'].isin(bcs)]
        
    if start_date:
        filtered = filtered[filtered['Date'] >= start_date]
        
    if end_date:
        filtered = filtered[filtered['Date'] <= end_date]
        
    return filtered

def calculate_kpis(df):
    """Calculate key performance indicators based on filtered data."""
    if df is None or df.empty:
        return {
            "total_sales": 0,
            "avg_daily": 0,
            "days_with_data": 0
        }
        
    total_sales = float(df['Sales'].sum())
    days_with_data = df['Date'].nunique()
    avg_daily = total_sales / days_with_data if days_with_data > 0 else 0
    
    return {
        "total_sales": total_sales,
        "avg_daily": avg_daily,
        "days_with_data": days_with_data
    }
