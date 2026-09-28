import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

def generate_demo_data():
    """Generates synthetic sales data for demonstration purposes."""
    
    # Exactly 1 month of data (August 2026)
    start_date = datetime(2026, 8, 1)
    days = 31 
    
    # Expanded Business Centers
    bcs = ["North-East BC", "South-West BC", "Central BC", "Coastal BC", "Mountain BC"]
    
    # Expanded Brands
    brands = ["Titan", "Vanguard", "Apex", "Horizon", "Quantum"]
    
    # Expanded Nameplates (mapping specific nameplates to specific brands for realism)
    brand_nameplates = {
        "Titan": ["T-Rex 500", "Behemoth XL", "Atlas Truck"],
        "Vanguard": ["Cruiser V1", "Cruiser V2", "Sedan Pro"],
        "Apex": ["Racer X", "Sprint 200", "Velocity", "Aero"],
        "Horizon": ["Explorer", "Nomad SUV", "Journey"],
        "Quantum": ["Q-Drive", "Photon Electric", "Electron", "Neutron", "Quark Mini"]
    }
    
    records = []
    
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        
        # Intentionally skip a couple of days to demonstrate missing data feature
        if day_offset in [14, 15]: # Skipping mid-month
            continue
            
        for bc in bcs:
            for brand, nps in brand_nameplates.items():
                # Randomly drop some combinations on certain days for realism
                if random.random() > 0.95:
                    continue
                    
                for np_name in nps:
                    # Base sales logic based on brand
                    base_sales = 500
                    if brand == "Apex": base_sales = 1200
                    if brand == "Quantum": base_sales = 2000
                    
                    noise = np.random.normal(0, base_sales * 0.15)
                    sales = max(0, int(base_sales + noise))
                    
                    records.append({
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "BC": bc,
                        "Brand": brand,
                        "Nameplate": np_name,
                        "Sales": sales
                    })
                
    # Add a new combination on the last day to trigger the "New Combination" alert
    records.append({
        "Date": (start_date + timedelta(days=30)).strftime("%Y-%m-%d"),
        "BC": "Central BC",
        "Brand": "Quantum",
        "Nameplate": "Quantum Future (Prototype)", 
        "Sales": 850
    })
                
    df = pd.DataFrame(records)
    
    # Determine current directory safely (works in both scripts and Databricks notebooks)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()
    
    # Ensure directory exists
    os.makedirs(current_dir, exist_ok=True)
    
    output_path = os.path.join(current_dir, "sample_sales_august_2026.xlsx")
    df.to_excel(output_path, index=False)
    
    print(f"✅ Demo data successfully generated at: {output_path}")
    print(f"Generated {len(df)} records covering {days} days.")
    print(f"Unique Brands: {df['Brand'].nunique()} | Unique Nameplates: {df['Nameplate'].nunique()}")
    print("This file can be uploaded via the Streamlit dashboard.")

if __name__ == "__main__":
    generate_demo_data()
