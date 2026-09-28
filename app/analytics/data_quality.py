import pandas as pd
from datetime import timedelta

def get_missing_dates(df):
    """Identify missing dates within the min-max date range of the dataset."""
    if df is None or df.empty:
        return [], 0, 0
        
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    
    min_date = df_copy['Date'].min()
    max_date = df_copy['Date'].max()
    
    expected_dates = pd.date_range(start=min_date, end=max_date)
    actual_dates = df_copy['Date'].unique()
    
    missing = expected_dates.difference(actual_dates)
    
    return missing.date.tolist(), len(expected_dates), len(actual_dates)

def get_new_combinations(df):
    """Identify new BC + Brand + Nameplate combinations in the current month compared to previous history."""
    if df is None or df.empty:
        return []
        
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy['MonthYear'] = df_copy['Date'].dt.to_period('M')
    
    max_month = df_copy['MonthYear'].max()
    
    current_month_df = df_copy[df_copy['MonthYear'] == max_month]
    previous_months_df = df_copy[df_copy['MonthYear'] < max_month]
    
    if previous_months_df.empty:
        return [] # No previous history to compare against
        
    current_combos = current_month_df[['BC', 'Brand', 'Nameplate']].drop_duplicates()
    prev_combos = previous_months_df[['BC', 'Brand', 'Nameplate']].drop_duplicates()
    
    # Merge to find combos that exist in current but NOT in previous
    merged = current_combos.merge(prev_combos, on=['BC', 'Brand', 'Nameplate'], how='left', indicator=True)
    new_combos = merged[merged['_merge'] == 'left_only'][['BC', 'Brand', 'Nameplate']]
    
    return new_combos.to_dict('records')

def get_detailed_missing_records(df):
    """Find exactly which valid BC+Brand+Nameplate combinations are missing on which expected dates."""
    if df is None or df.empty:
        return pd.DataFrame()
        
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date']).dt.date
    
    min_date = df_copy['Date'].min()
    max_date = df_copy['Date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date).date
    
    # Get all valid combinations that have appeared at least once
    combos = df_copy[['BC', 'Brand', 'Nameplate']].drop_duplicates()
    combo_tuples = [tuple(x) for x in combos.to_numpy()]
    
    expected_list = []
    for d in all_dates:
        for bc, br, np in combo_tuples:
            expected_list.append({'Date': d, 'BC': bc, 'Brand': br, 'Nameplate': np})
            
    expected_df = pd.DataFrame(expected_list)
    
    # Merge with actual data
    actual_df = df_copy[['Date', 'BC', 'Brand', 'Nameplate']].drop_duplicates()
    actual_df['Exists'] = True
    
    merged = pd.merge(expected_df, actual_df, on=['Date', 'BC', 'Brand', 'Nameplate'], how='left')
    
    # Missing records
    missing_detailed = merged[merged['Exists'].isna()][['Date', 'BC', 'Brand', 'Nameplate']]
    
    return missing_detailed
