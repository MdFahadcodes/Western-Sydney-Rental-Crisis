import sqlite3
import pandas as pd
import os


db_path = os.path.join('processed_data', 'western_sydney_housing.db')
income_path = os.path.join('processed_data', 'clean_income_data.csv')
rental_path = os.path.join('processed_data', 'clean_rental_snapshot.csv') 

def build_production_database():
    print("--- PHASE 3: BUILDING DATABASE ---")
    
    if not os.path.exists(income_path) or not os.path.exists(rental_path):
        print("CRITICAL ERROR: Processed datasets missing.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Load Data
        df_income = pd.read_csv(income_path)
        df_rentals = pd.read_csv(rental_path)
        
        df_income.to_sql('staging_income', conn, if_exists='replace', index=False)
        df_rentals.to_sql('staging_rentals', conn, if_exists='replace', index=False)
        print(" - Staging tables loaded.")

        # Build View
        print("Building Analytical Views...", end=" ")
        cur.execute("DROP VIEW IF EXISTS market_affordability_view")
        
        create_view_query = """
        CREATE VIEW market_affordability_view AS
        
        WITH joined_data AS (
            SELECT 
                i.suburb,
                i.postcode,
                r.median_rent_current,
                i.est_income_current
            FROM staging_income i
            INNER JOIN staging_rentals r ON i.postcode = r.postcode
        ),
        
        calculated_metrics AS (
            SELECT 
                *,
                ROUND((median_rent_current / est_income_current) * 100, 2) as rental_stress_rate
            FROM joined_data
        )
        
        SELECT 
            suburb,
            postcode,  
            median_rent_current as rent_2025,
            est_income_current as income_2025,
            rental_stress_rate,
            
            ROUND(AVG(rental_stress_rate) OVER (), 2) as market_avg_stress,
            ROUND(rental_stress_rate - AVG(rental_stress_rate) OVER (), 2) as variance_from_avg,
            RANK() OVER (ORDER BY rental_stress_rate DESC) as risk_rank,
            
            CASE 
                WHEN rental_stress_rate >= 35 THEN 'Severe Risk'
                WHEN rental_stress_rate >= 30 THEN 'High Stress'
                ELSE 'Moderate'
            END as risk_category
            
        FROM calculated_metrics
        ORDER BY risk_rank ASC;
        """
        
        cur.execute(create_view_query)
        print("DONE.")
        
        # Verify
        test_df = pd.read_sql("SELECT * FROM market_affordability_view LIMIT 10", conn)
        print(test_df.to_string())
        
    except Exception as e:
        print(f"\nDATABASE ERROR: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    build_production_database()