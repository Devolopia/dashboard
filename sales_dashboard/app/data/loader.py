import pandas as pd

def load_excel_file(uploaded_file):
    """Load an uploaded Excel file into a pandas DataFrame."""
    try:
        return pd.read_excel(uploaded_file)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
