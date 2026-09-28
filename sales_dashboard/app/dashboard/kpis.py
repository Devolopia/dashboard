import streamlit as st

def render_kpi_cards(kpis):
    """Render the KPI cards at the top of the dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"{kpis['total_sales']:,.0f}"
        )
        
    with col2:
        st.metric(
            label="Average Daily Sales",
            value=f"{kpis['avg_daily']:,.0f}"
        )
        
    with col3:
        # Assuming maximum days could be calculated, but we just show days_with_data here
        st.metric(
            label="Days with Data",
            value=f"{kpis['days_with_data']}"
        )
        
    with col4:
        st.metric(
            label="Selected Period",
            value="Custom"
        )
