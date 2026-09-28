import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# DATABRICKS APPS CONFIGURATION
# ---------------------------------------------------------
# When deployed on Databricks Apps, local storage is ephemeral.
# To persist your uploads and parquet files, set the DATABRICKS_DATA_PATH 
# environment variable to a Databricks Volume path.
# Example: /Volumes/your_catalog/your_schema/sales_dashboard_data
# ---------------------------------------------------------
env_data_path = os.environ.get("DATABRICKS_DATA_PATH")

if env_data_path:
    DATA_DIR = Path(env_data_path)
else:
    DATA_DIR = BASE_DIR / "data"

# Data Paths
ORIGINAL_DATA_DIR = DATA_DIR / "original"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
UPLOAD_HISTORY_FILE = DATA_DIR / "upload_history.json"

PARQUET_MASTER_FILE = PROCESSED_DATA_DIR / "master_sales.parquet"

# Ensure directories exist
ORIGINAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Data Schema
REQUIRED_COLUMNS = ["Date", "BC", "Brand", "Nameplate", "Sales"]
KEY_COLUMNS = ["Date", "BC", "Brand", "Nameplate"]
