import pandas as pd
import os


SUBURB_MAP = {
    2148: 'Blacktown', 2150: 'Parramatta', 2750: 'Penrith', 2770: 'Mt Druitt',
    2170: 'Liverpool', 2560: 'Campbelltown', 2144: 'Auburn', 2200: 'Bankstown',
    2145: 'Westmead', 2760: 'St Marys'
}
TARGET_POSTCODES = list(SUBURB_MAP.keys())
WAGE_INDEX_FACTOR = 1.142 

input_path = os.path.join('raw_data', '2021Census_G02_NSW_POA.csv')
output_path = os.path.join('processed_data', 'clean_income_data.csv')

def process_income_data():
    print("--- PHASE 1: PROCESSING INCOME DATA ---")
    if not os.path.exists(input_path):
        print(f"ERROR: Not found {input_path}")
        return

    df = pd.read_csv(input_path)
    # Clean headers
    df.columns = [c.strip() for c in df.columns]
    
    target_col = 'Median_tot_hhd_inc_weekly'
    if target_col not in df.columns:
        print(f"ERROR: Missing column '{target_col}'")
        return

    # Rename & Filter
    df = df.rename(columns={'POA_CODE_2021': 'postcode', target_col: 'median_income_2021'})
    df['postcode'] = df['postcode'].astype(str).str.replace('POA', '').astype(int)
    
    western_df = df[df['postcode'].isin(TARGET_POSTCODES)].copy()
    western_df['suburb'] = western_df['postcode'].map(SUBURB_MAP)
    
    # Calculate Current Income
    western_df['est_income_current'] = western_df['median_income_2021'] * WAGE_INDEX_FACTOR
    western_df['est_income_current'] = western_df['est_income_current'].round(2)

    western_df = western_df[['postcode', 'suburb', 'median_income_2021', 'est_income_current']]
    western_df.to_csv(output_path, index=False)
    print(f"Saved income data to {output_path}")

if __name__ == "__main__":
    process_income_data()