# 🏠 Western Sydney Rental Crisis Analysis (2024-2025)

![Data Pipeline](https://github.com/MdFahadcodes/Western-Sydney-Rental-Crisis/actions/workflows/run_pipeline.yml/badge.svg)
![Live dashboard demonstration:](https://github.com/user-attachments/assets/4fbfa5e0-bf17-4179-ab5a-9aa83d357f98)

## 📌 Project Overview
This end-to-end data analytics project investigates the intensifying rental affordability crisis in Western Sydney. By integrating recent housing costs and modeling them against local incomes, the analysis identifies geographical hotspots where rental stress (the percentage of income spent on rent) exceeds the critical 30% threshold.

## 📊 Data Sources
This analysis integrates two primary datasets to calculate accurate rental stress:
* **NSW Fair Trading Rental Bond Data:** Used for actual median weekly rent prices, dwelling types, and bond lodgement volumes by postcode.
* **ABS Census Data (2021):** Provides the baseline median household income, which is then extrapolated using a 1.15% quarterly wage growth projection.


Moving beyond a static report, this repository features an  automated analytics workflow  that validates data processing every Monday morning.


## 📈 Key Insights & Visualization (Power BI)
* **The "Affordability" Illusion:** The data reveals that while suburbs like Auburn may have lower baseline rents, the lower local incomes push the rental stress peak to a critical 39.7%, highlighting the disparity between flat wage growth and rent hikes.
* **Rental Stress Mapping:** Utilizes Azure Maps to visualize postcodes where low-to-middle income earners are most vulnerable.
* **Trend Velocity Tracking:** Compares historical bond data against modeled current-year projections to identify emerging "hot zones".

 ## 🛠 Technical Workflow & Automation

    1. Data Processing Pipeline (Python) 
The project utilizes a modular Python architecture to ensure clean, reproducible data. The scripts are executed in the following order:
1.  `1_process_income.py`: Models 2024-2025 income data based on quarterly growth trends.
2.  `2_process_bonds.py`: Cleans and standardizes rental bond lodgment data.
3.  `3_create_database.py`: Aggregates disparate datasets into a structured format.
4.  `4_analyze_trends.py`: Calculates statistical measures and rental stress percentages.
5.  `export_for_powerbi.py`: Formats the final dataset for seamless Power BI integration.

 ### 2. Automated Quality Assurance (GitHub Actions)

A CI/CD pipeline (`run_pipeline.yml`) is configured to:

* **Trigger:** Automatically every Monday at 9:00 AM UTC.
* **Environment:** Installs necessary dependencies (`pandas`, `numpy`, `openpyxl`) in a virtual Linux environment.
* **Validation:** Executes the full script sequence to verify that the analytical logic remains functional as libraries or data update.

---

### 3. Data Visualization (Power BI)

The final dashboard provides interactive insights into Western Sydney's rental market:

* **Dynamic DAX Measures:** Developed context-aware headlines and smart narratives to provide real-time insights.
* **UX Design:** Synchronized visuals where scatter plot outliers correspond to map-based geographical hotspots, ensuring a seamless analytical experience.

## 📂 Repository Structure

```text
├── .github/workflows
│   └── run_pipeline.yml        # Automation configuration
├── data
│   ├── raw/                    # Initial datasets (NSW Fair Trading & ABS)
│   └── processed/              # Cleaned output from Python scripts
├── scripts
│   ├── 1_process_income.py
│   ├── 2_process_bonds.py
│   ├── 3_create_database.py
│   ├── 4_analyze_trends.py
│   └── export_for_powerbi.py
├── dashboard
│   └── Exec summary.pbix       # Power BI source file
├── requirements.txt            # Python dependencies
└── README.md
