  🏠 Western Sydney Rental Crisis Analysis (2024-2025)

PowerBI: https://github.com/user-attachments/assets/4fbfa5e0-bf17-4179-ab5a-9aa83d357f98

   📊 Project Overview
This project provides a comprehensive data analytics solution to track and visualize the rental affordability crisis in Western Sydney. By integrating multiple datasets, the analysis identifies "Crisis Hotspots" where rental stress (rent-to-income ratio) exceeds the critical 30% threshold.

Moving beyond a static report, this repository features an  automated analytics workflow  that validates data processing every Monday morning.




Key Analytics Insights
Rental Stress Peak:  Identified key suburbs like  Auburn  reaching rental stress levels of  39.7% .
The Wage-Rent Gap:  While the model assumes a conservative  1.15% quarterly wage growth  (benchmarked against ABS Wage Price Index), rental prices have significantly outpaced local earnings.
Trend Velocity:  Analysis of "Max Rent Growth ('24-'25)" reveals accelerated price surges in specific Western Sydney postcodes post-pandemic.


   🛠 Technical Workflow & Automation

    1. Data Processing Pipeline (Python)
The project utilizes a modular Python architecture to ensure clean, reproducible data. The scripts are executed in the following order:
1.  `1_process_income.py`: Models 2024-2025 income data based on quarterly growth trends.
2.  `2_process_bonds.py`: Cleans and standardizes rental bond lodgment data.
3.  `3_create_database.py`: Aggregates disparate datasets into a structured format.
4.  `4_analyze_trends.py`: Calculates statistical measures and rental stress percentages.
5.  `export_for_powerbi.py`: Formats the final dataset for seamless Power BI integration.

    2. Automated Quality Assurance (GitHub Actions)
A CI/CD pipeline (`run_pipeline.yml`) is configured to:
* Trigger automatically every  Monday at 9:00 AM UTC .
* Install necessary dependencies (`pandas`, `numpy`, `openpyxl`) in a virtual Linux environment.
* Execute the full script sequence to verify that the analytical logic remains functional as libraries or data update.



    3. Data Visualization (Power BI)
*  Dynamic DAX Measures:  Developed context-aware headlines and smart narratives.
*  UX Design:  Synchronized visuals where scatter plot outliers correspond to map-based geographical hotspots.



   📂 Repository Structure
```text
├── .github/workflows
│   └── run_pipeline.yml        Automation configuration
├── data
│   ├── raw/                    Initial datasets
│   └── processed/              Output from Python scripts
├── scripts
│   ├── 1_process_income.py
│   ├── 2_process_bonds.py
│   ├── 3_create_database.py
│   ├── 4_analyze_trends.py
│   └── export_for_powerbi.py
├── dashboard
│   └── Exec summary.pbix       Power BI source file
├── requirements.txt            Python dependencies
└── README.md
