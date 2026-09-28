import streamlit as st

def render_data_table(df):
    """Render the underlying actual data table below the chart."""
    if df is None or df.empty:
        return
        
    st.subheader("Actual Data")
    
    # Format the dataframe for display
    display_df = df.copy()
    display_df['Date'] = display_df['Date'].astype(str)
    display_df = display_df.sort_values(by=['Date', 'BC', 'Brand', 'Nameplate'], ascending=[False, True, True, True])
    
    # Ensure columns order
    cols = ['Date', 'BC', 'Brand', 'Nameplate', 'Sales']
    display_df = display_df[cols]
    
    # Using st.dataframe for interactive table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Sales": st.column_config.NumberColumn(
                "Sales",
                format="%.0f"
            )
        }
    )
