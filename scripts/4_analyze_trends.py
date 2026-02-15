import pandas as pd
import os

# 1. Define the Map (Suburb Name Lookup)
SUBURB_MAP = {
    2148: 'Blacktown', 
    2150: 'Parramatta', 
    2750: 'Penrith', 
    2770: 'Mt Druitt',
    2170: 'Liverpool', 
    2560: 'Campbelltown', 
    2144: 'Auburn', 
    2200: 'Bankstown',
    2145: 'Westmead', 
    2760: 'St Marys'
}

# --- PATHS ---
input_path = os.path.join('processed_data', 'clean_rental_time_series.csv')
output_path = os.path.join('processed_data', 'rental_trends_analysis.csv')

def analyze_trends():
    print("--- PHASE 4: TREND ANALYSIS ---")
    
    if not os.path.exists(input_path):
        print(f"CRITICAL ERROR: Input file not found at {input_path}")
        return

    # 1. Load Data
    df = pd.read_csv(input_path)
    df['date'] = pd.to_datetime(df['date'])

    # 2. Safety Sort (Chronological Order)
    df = df.sort_values(['postcode', 'date'], ascending=[True, True])

    results = []

    print(f"Analyzing trends for {len(df['postcode'].unique())} locations...")

    for postcode in df['postcode'].unique():
        sub_df = df[df['postcode'] == postcode]
        
        # Need at least 2 points to draw a line
        if len(sub_df) < 2: continue

        # 3. Dynamic Endpoints
        start_row = sub_df.iloc[0]
        end_row = sub_df.iloc[-1]
        
        # Calculate exact duration in years
        years_diff = (end_row['date'] - start_row['date']).days / 365.25
        
        if years_diff == 0: continue

        # 4. Calculate CAGR
        start_price = start_row['median_rent']
        end_price = end_row['median_rent']
        
        cagr = ((end_price / start_price) ** (1 / years_diff)) - 1
        
        # 5. Map Suburb Name
        suburb_name = SUBURB_MAP.get(postcode, 'Unknown')

        results.append({
            'suburb': suburb_name,
            'postcode': postcode,       # Added Postcode column
            'start_date': start_row['date'].date(),
            'end_date': end_row['date'].date(),
            'start_rent': start_price,
            'current_rent': end_price,
            'total_growth_pct': round(cagr * 100, 2)
        })

    if not results:
        print("WARNING: No valid trends found.")
        return

    # 6. Formatting Final Report
    res_df = pd.DataFrame(results)
    
    # Sort by Growth % (Highest to Lowest)
    res_df = res_df.sort_values('total_growth_pct', ascending=False)
    
    # Save to CSV
    res_df.to_csv(output_path, index=False)
    
    print(f"\nSUCCESS: Trend analysis saved to {output_path}")
    print("\n--- TOP 5 FASTEST GROWING SUBURBS ---")
    
    # Print the Clean Table with BOTH Suburb and Postcode
    print(res_df[['suburb', 'postcode', 'current_rent', 'total_growth_pct']].head().to_string(index=False))

if __name__ == "__main__":
    analyze_trends()