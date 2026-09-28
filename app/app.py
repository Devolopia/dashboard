import streamlit as st
import pandas as pd
from datetime import datetime

from data.loader import load_excel_file
from data.validator import validate_dataframe
from data.processor import process_upsert
from data.storage import save_original_file, load_master_parquet, save_master_parquet, delete_upload_and_rebuild
from utils.helpers import save_upload_history, get_upload_history
from analytics.sales_analysis import filter_data, calculate_kpis
from analytics.data_quality import get_missing_dates, get_new_combinations, get_detailed_missing_records
from dashboard.filters import render_filters
from dashboard.kpis import render_kpi_cards
from dashboard.charts import render_sales_trend_chart
from dashboard.tables import render_data_table

st.set_page_config(
    page_title="Executive Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", 
    ["Dashboard", "Data Upload"],
    key="nav_page"
)

if page == "Data Upload":
    st.title("📥 Upload & Manage Data")
    
    uploaded_files = st.file_uploader(
        "Upload Excel files", 
        type=['xlsx'], 
        accept_multiple_files=True
    )
    
    if st.button("Process Uploads") and uploaded_files:
        master_df = load_master_parquet()
        
        total_stats = {
            "files_processed": 0,
            "records_received": 0,
            "new_records": 0,
            "updated_records": 0,
            "duplicate_ignored": 0,
            "invalid_records": 0
        }
        
        with st.spinner("Processing files..."):
            for file in uploaded_files:
                # Load
                df = load_excel_file(file)
                if df is None:
                    st.error(f"Failed to read {file.name}")
                    continue
                    
                # Validate
                is_valid, errors = validate_dataframe(df)
                if not is_valid:
                    st.error(f"Validation failed for {file.name}:")
                    for err in errors:
                        st.write(f"- {err}")
                    total_stats["invalid_records"] += len(df)
                    continue
                    
                # Save original
                saved_filepath = save_original_file(file)
                
                # Get missing dates for this specific file
                missing_dates, exp, act = get_missing_dates(df)
                
                # Upsert
                master_df, stats = process_upsert(master_df, df)
                
                # Save master
                save_master_parquet(master_df)
                
                # Update stats
                total_stats["files_processed"] += 1
                total_stats["records_received"] += stats["records_received"]
                total_stats["new_records"] += stats["new_records"]
                total_stats["updated_records"] += stats["updated_records"]
                total_stats["duplicate_ignored"] += stats["duplicate_ignored"]
                
                # Save history
                save_upload_history({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": file.name,
                    "saved_filename": saved_filepath.name,
                    "stats": stats,
                    "missing_dates": [str(d) for d in missing_dates],
                    "expected_days": exp,
                    "actual_days": act
                })
                
            # Show Summary
            st.success("Processing Complete!")
            st.write("### Upload Processing Summary")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Files Processed", total_stats["files_processed"])
            col1.metric("Records Received", total_stats["records_received"])
            col2.metric("New Records Added", total_stats["new_records"])
            col2.metric("Existing Records Updated", total_stats["updated_records"])
            col3.metric("Duplicate Records Ignored", total_stats["duplicate_ignored"])
            col3.metric("Invalid Records", total_stats["invalid_records"])

    # --- UPLOAD HISTORY ---
    st.write("---")
    st.subheader("📜 Upload History & Management")
    history = get_upload_history()
    if history:
        for i, entry in enumerate(reversed(history)):
            with st.expander(f"📄 {entry['filename']} (Uploaded: {entry['timestamp']})"):
                st.write(f"**Original File path:** `data/original/{entry.get('saved_filename', 'Unknown')}`")
                st.write(f"**Parquet Data path:** `data/processed/master_sales.parquet`")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Data Info:**")
                    if 'stats' in entry:
                        st.write(f"- Records Received: {entry['stats'].get('records_received', 0)}")
                        st.write(f"- New Records Added: {entry['stats'].get('new_records', 0)}")
                        st.write(f"- Records Updated: {entry['stats'].get('updated_records', 0)}")
                
                with col2:
                    st.write("**Missing Dates in File:**")
                    missing = entry.get('missing_dates', [])
                    if missing:
                        st.warning(f"{len(missing)} missing days out of {entry.get('expected_days', 0)} expected.")
                        st.caption(", ".join([str(d) for d in missing[:10]]) + ("..." if len(missing)>10 else ""))
                        
                    else:
                        st.success("No missing dates in this file.")
                        
                if st.button("🗑️ Remove this Data", key=f"del_{entry['timestamp']}_{i}"):
                    delete_upload_and_rebuild(entry['timestamp'])
                    st.rerun()
    else:
        st.write("No upload history available.")

elif page == "Dashboard":
    st.title("Executive Sales Analytics")

    # --- LOAD DATA FOR DASHBOARD ---
    df = load_master_parquet()

    if df is None or df.empty:
        st.info("No data available. Please go to the 'Data Upload' page to upload Excel files and get started.")
        st.stop()
        
    # --- FILTERS ---
    sel_brand, sel_nameplate, sel_bc, start_date, end_date = render_filters(df)

    # --- APPLY FILTERS ---
    filtered_df = filter_data(df, sel_brand, sel_nameplate, sel_bc, start_date, end_date)

    # --- KPIs ---
    kpis = calculate_kpis(filtered_df)
    st.write("---")
    render_kpi_cards(kpis)

    # --- CHARTS AND TABLES ---
    st.write("---")
    render_sales_trend_chart(filtered_df)
    render_data_table(filtered_df)
    
