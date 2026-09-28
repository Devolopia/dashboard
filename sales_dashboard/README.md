# Executive Sales Analytics Dashboard

A professional Streamlit-based Sales Analytics Dashboard designed for management and executive demonstrations.

## 1. Project Structure

```text
sales_dashboard/
├── app/
│   ├── app.py                 # Main Streamlit application
│   ├── config.py              # Configuration and constants
│   ├── data/                  # Data access layer
│   │   ├── loader.py
│   │   ├── validator.py
│   │   ├── processor.py       # Upsert logic
│   │   └── storage.py         # File saving and Parquet storage
│   ├── analytics/             # Business logic and analytics
│   │   ├── sales_analysis.py
│   │   └── data_quality.py    # Missing data & new combinations
│   ├── dashboard/             # UI Components
│   │   ├── filters.py
│   │   ├── charts.py
│   │   ├── kpis.py
│   │   └── tables.py
│   └── utils/
│       └── helpers.py
├── data/
│   ├── original/              # Original uploaded Excel files
│   └── processed/             # Master Parquet dataset
├── demo_data/                 # Independent sample data generator
│   └── generate_demo_data.py
├── requirements.txt
└── README.md
```

## 2. Requirements and Installation

This project uses `uv` for fast environment setup.

```bash
# Change directory
cd sales_dashboard

# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
uv pip install -r requirements.txt
```

## 3. Generating Demo Data

To test the application, you can generate sample Excel data:

```bash
python demo_data/generate_demo_data.py
```
This creates a file `sample_sales_august_2026.xlsx` in the `demo_data/` folder.

## 4. Starting the Application

Run the Streamlit application from the root directory:

```bash
streamlit run app/app.py
```

## 5. Using Real Data

1. Start the application.
2. Expand the "Upload Sales Data (Excel)" section.
3. Upload your `.xlsx` files.
4. The application works exactly the same with real data as with demo data.
5. The `demo_data/` folder can be safely deleted without breaking the app.

## 6. Excel Format Requirements

The uploaded Excel files must contain the following columns exactly as named:
- `Date` (YYYY-MM-DD or readable date format)
- `BC` (Business Center, text)
- `Nameplate` (text)
- `Sales` (numeric)

## 7. How UPSERT Works

When multiple Excel files are uploaded (with overlapping dates), the system uses an UPSERT logic based on a unique key:
`Date + BC + Nameplate`

- If this combination does not exist, a new record is **INSERTED**.
- If this combination already exists, the old record is **UPDATED** with the new `Sales` value.
- Duplicate records are completely avoided.

## 8. Original File Storage

All uploaded Excel files are saved unchanged in `data/original/` with a timestamp to prevent overwriting.

## 9. Parquet Storage

The processed and merged data is stored as a highly optimized `.parquet` file in `data/processed/master_sales.parquet`. The Streamlit dashboard reads from this Parquet file for maximum performance, ensuring it remains fast even with large datasets.

## 10. Data Quality: Missing Data & New Combinations

- **Missing Data:** The app calculates the expected date range (from min to max date in the data) and identifies missing calendar days. It alerts the user rather than assuming zero sales.
- **New Combinations:** The application compares the current month against previous months to detect newly introduced `BC + Nameplate` combinations and highlights them as new entries.
