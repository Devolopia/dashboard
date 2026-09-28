import pandas as pd
from config import REQUIRED_COLUMNS

def validate_dataframe(df):
    """Validate that the dataframe has the correct schema and data types."""
    errors = []
    
    # Check columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return False, errors
        
    # Check date column
    try:
        pd.to_datetime(df["Date"])
    except Exception:
        errors.append("Date column contains invalid dates.")
        
    # Check numeric sales
    if not pd.api.types.is_numeric_dtype(df["Sales"]):
        try:
            pd.to_numeric(df["Sales"])
        except Exception:
            errors.append("Sales column contains non-numeric values.")
            
    # Check empty fields
    if df["BC"].isnull().any() or (df["BC"] == "").any():
        errors.append("BC column contains empty values.")
        
    if df["Brand"].isnull().any() or (df["Brand"] == "").any():
        errors.append("Brand column contains empty values.")
        
    if df["Nameplate"].isnull().any() or (df["Nameplate"] == "").any():
        errors.append("Nameplate column contains empty values.")
        
    return len(errors) == 0, errors
