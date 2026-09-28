import pandas as pd
from config import KEY_COLUMNS

def process_upsert(existing_df, new_df):
    """
    Upsert logic: Update existing records and insert new ones based on Date, BC, Nameplate.
    """
    # Normalize dates and types
    new_df = new_df.copy()
    new_df['Date'] = pd.to_datetime(new_df['Date']).dt.date
    new_df['Sales'] = pd.to_numeric(new_df['Sales'], errors='coerce')
    
    # Drop exact duplicates within the new dataframe itself, keeping the last one
    new_df = new_df.drop_duplicates(subset=KEY_COLUMNS, keep='last')
    
    if existing_df is None or existing_df.empty:
        stats = {
            "records_received": len(new_df),
            "new_records": len(new_df),
            "updated_records": 0,
            "duplicate_ignored": 0
        }
        return new_df, stats
        
    existing_df = existing_df.copy()
    existing_df['Date'] = pd.to_datetime(existing_df['Date']).dt.date
    existing_df['Sales'] = pd.to_numeric(existing_df['Sales'], errors='coerce')
    
    # We will use set index for easy update
    existing_indexed = existing_df.set_index(KEY_COLUMNS)
    new_indexed = new_df.set_index(KEY_COLUMNS)
    
    # Find intersecting records (updates/duplicates)
    updates_idx = existing_indexed.index.intersection(new_indexed.index)
    
    # Find new records (inserts)
    inserts_idx = new_indexed.index.difference(existing_indexed.index)
    
    # To count exact duplicates vs actual updates, we can compare values
    # but for simplicity, we treat all intersections as updates
    
    # Update existing
    existing_indexed.update(new_indexed)
    
    # Append new
    if not inserts_idx.empty:
        combined = pd.concat([existing_indexed, new_indexed.loc[inserts_idx]])
    else:
        combined = existing_indexed
        
    combined = combined.reset_index()
    
    stats = {
        "records_received": len(new_df),
        "new_records": len(inserts_idx),
        "updated_records": len(updates_idx),
        "duplicate_ignored": 0 # Handled in initial drop_duplicates implicitly
    }
    
    return combined, stats
