import os
import json
from datetime import datetime
import pandas as pd
from config import ORIGINAL_DATA_DIR, PARQUET_MASTER_FILE, UPLOAD_HISTORY_FILE
from data.processor import process_upsert

def save_original_file(uploaded_file):
    """Save the uploaded file to the original data directory without modifying it."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = ORIGINAL_DATA_DIR / filename
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return filepath

def load_master_parquet():
    """Load the master parquet file if it exists."""
    if PARQUET_MASTER_FILE.exists():
        try:
            return pd.read_parquet(PARQUET_MASTER_FILE)
        except Exception:
            return None
    return None

def save_master_parquet(df):
    """Save the dataframe to the master parquet file."""
    if df is not None and not df.empty:
        # Ensure standard types before saving
        df_to_save = df.copy()
        df_to_save['Date'] = pd.to_datetime(df_to_save['Date'])
        df_to_save['Sales'] = pd.to_numeric(df_to_save['Sales'])
        df_to_save.to_parquet(PARQUET_MASTER_FILE, index=False)

def delete_upload_and_rebuild(timestamp_to_delete):
    """Deletes an upload by timestamp, removes its original file, and rebuilds the parquet."""
    if not UPLOAD_HISTORY_FILE.exists():
        return
        
    with open(UPLOAD_HISTORY_FILE, "r") as f:
        history = json.load(f)
        
    # Find entry
    entry_to_delete = next((e for e in history if e['timestamp'] == timestamp_to_delete), None)
    if not entry_to_delete:
        return
        
    # Remove file
    if 'saved_filename' in entry_to_delete:
        file_path = ORIGINAL_DATA_DIR / entry_to_delete['saved_filename']
        if file_path.exists():
            os.remove(file_path)
            
    # Remove from history
    history = [e for e in history if e['timestamp'] != timestamp_to_delete]
    
    with open(UPLOAD_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
        
    # Rebuild Parquet
    if PARQUET_MASTER_FILE.exists():
        os.remove(PARQUET_MASTER_FILE)
        
    master_df = None
    for entry in history:
        if 'saved_filename' in entry:
            file_path = ORIGINAL_DATA_DIR / entry['saved_filename']
            if file_path.exists():
                try:
                    df = pd.read_excel(file_path)
                    master_df, _ = process_upsert(master_df, df)
                except Exception as e:
                    print(f"Failed to process {file_path} during rebuild: {e}")
                
    if master_df is not None and not master_df.empty:
        save_master_parquet(master_df)
