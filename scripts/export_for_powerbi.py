import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
db_path = os.path.join('processed_data', 'western_sydney_housing.db')
output_path = os.path.join('processed_data', 'market_benchmark_table.csv')

def export_view():
    print("--- EXPORTING SQL VIEW TO CSV (FOR POWER BI) ---")
    
    if not os.path.exists(db_path):
        print(f"CRITICAL ERROR: Database not found at {db_path}")
        print("Did you run Script 3?")
        return

    conn = sqlite3.connect(db_path)
    
    try:
        # Query the View (Now includes Postcode!)
        df = pd.read_sql("SELECT * FROM market_affordability_view", conn)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        
        print(f"SUCCESS: Exported {len(df)} rows to {output_path}")
        print("You can now refresh Power BI.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    export_view()