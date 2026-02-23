from config_paths import RAW_DATA_DIR, FINAL_DATA_DIR, FIGURES_DIR, TABLES_DIR

df = pd.read_csv(RAW_DATA_DIR / 'my_data.csv')
merged.to_csv(FINAL_DATA_DIR / 'analysis_panel.csv', index=False)
plt.savefig(FIGURES_DIR / 'my_plot.png', dpi=300)

"""
QM 2023 Capstone Project: Milestone 1 Data Pipeline
Team: [Your Team Name]
Members: [List names]
Date: [Submission date]
This script fetches, cleans, and merges REIT and economic data into a tidy panel
structure.
"""
# Section 1: Imports and setup
# Section 2: Load REIT Master Panel
# Section 3: Clean REIT data (missing values, outliers, duplicates)
# Section 4: Fetch FRED economic indicators
# Section 5: Merge REIT + economic data
# Section 6: Reshape to panel structure (Entity=REIT, Time=Month)
# Section 7: Save tidy output and metadata