import pandas as pd
import os


SUBURB_MAP = {
    2148: 'Blacktown', 2150: 'Parramatta', 2750: 'Penrith', 2770: 'Mt Druitt',
    2170: 'Liverpool', 2560: 'Campbelltown', 2144: 'Auburn', 2200: 'Bankstown',
    2145: 'Westmead', 2760: 'St Marys'
}
TARGET_POSTCODES = list(SUBURB_MAP.keys())


input_path = os.path.join('raw_data', 'bond_data.xlsx')
output_ts_path = os.path.join('processed_data', 'clean_rental_time_series.csv')
output_snap_path = os.path.join('processed_data', 'clean_rental_snapshot.csv')

def process_bonds():
    print("--- PHASE 2: PROCESSING RENTAL BONDS (2-YEAR TRENDS) ---")
    
    if not os.path.exists(input_path):
        print(f"CRITICAL ERROR: File not found at {input_path}")
        return

    # 1. Load Data 
    print("Loading Excel file...")
    df = pd.read_excel(input_path, engine='openpyxl', dtype=str)

    # 2. Standardize Column Names
    df.columns = [str(c).lower().strip().replace(' ', '_') for c in df.columns]
    
    # Identify key columns
    date_col = next((c for c in df.columns if 'date' in c or 'lodgement' in c), None)
    rent_col = next((c for c in df.columns if 'rent' in c), None)
    postcode_col = next((c for c in df.columns if 'postcode' in c), None)

    if not all([date_col, rent_col, postcode_col]):
        print(f"ERROR: Columns missing. Found: {list(df.columns)}")
        return

    # 3. Clean 'Weekly Rent' (Handle 'U')
    df[rent_col] = pd.to_numeric(df[rent_col], errors='coerce')
    df = df.dropna(subset=[rent_col])

    # 4. Filter for Target Suburbs
    df[postcode_col] = pd.to_numeric(df[postcode_col], errors='coerce')
    df = df[df[postcode_col].isin(TARGET_POSTCODES)].copy()
    
    # 5. Clean Dates
    df['date'] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['date'])

    # 6. Aggregate (Time Series - Quarterly)
    # This will create distinct rows for 2024 and 2025
    print("Aggregating into Quarterly Time Series...")
    df_quarterly = df.groupby([postcode_col, pd.Grouper(key='date', freq='QE')])[rent_col].median().reset_index()
    df_quarterly.columns = ['postcode', 'date', 'median_rent']
    
    # 7. Create Snapshot (Latest 2025 Data)
    df_snapshot = df_quarterly.sort_values('date').groupby('postcode').tail(1).copy()
    df_snapshot = df_snapshot.rename(columns={'median_rent': 'median_rent_current'})
    df_snapshot = df_snapshot[['postcode', 'date', 'median_rent_current']]

    # 8. Save
    df_quarterly.to_csv(output_ts_path, index=False)
    df_snapshot.to_csv(output_snap_path, index=False)
    
    print(f"SUCCESS: Processed {len(df_quarterly)} quarterly records (2024-2025).")

if __name__ == "__main__":
    process_bonds()