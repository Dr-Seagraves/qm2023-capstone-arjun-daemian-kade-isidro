import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Section 1: Imports and config_paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FINAL_DIR = DATA_DIR / "final"

# Create final directory if it doesn't exist
FINAL_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("Starting Final Panel Merge Process")
print("=" * 80)

# Section 2: Load all processed datasets from data/processed/*
print("\nSection 2: Loading processed datasets...")

# Load crime index data (Year as rows, Countries as columns)
crime_df = pd.read_csv(PROCESSED_DIR / "crime_index_wide.csv")
print(f"Crime index data shape: {crime_df.shape}")

# Load foreign investment data (Country as rows, Years as columns)
fi_df = pd.read_csv(PROCESSED_DIR / "foreign_investment_wide.csv")
print(f"Foreign investment data shape: {fi_df.shape}")

# Load GEPU data (Year, Month, GEPU indices, and countries)
gepu_df = pd.read_csv(PROCESSED_DIR / "january_2012_onwards.csv")
print(f"GEPU data shape: {gepu_df.shape}")

# Section 3: Align time variables
print("\nSection 3: Aligning time variables and restructuring data...")

# Transform crime_index from wide to long format
# Year is already in rows, countries are columns
crime_long = crime_df.melt(id_vars=['Year'], var_name='Country', value_name='crime_index')
crime_long = crime_long.dropna(subset=['crime_index'])
print(f"Crime index (long format): {crime_long.shape}")

# Transform foreign investment from wide to long format
fi_long = fi_df.melt(id_vars=['Country'], var_name='Year', value_name='foreign_investment')
fi_long['Year'] = pd.to_numeric(fi_long['Year'], errors='coerce')
fi_long = fi_long.dropna(subset=['Year', 'foreign_investment'])
fi_long['Year'] = fi_long['Year'].astype(int)
print(f"Foreign investment (long format): {fi_long.shape}")

# For GEPU data: filter for January only (Month == 1.0) to get one entry per year
gepu_january = gepu_df[gepu_df['Month'] == 1.0].copy()
gepu_january['Year'] = gepu_january['Year'].astype(int)

# Melt GEPU data to long format (exclude Year, Month, GEPU indices)
gepu_cols = [col for col in gepu_january.columns if col not in ['Year', 'Month', 'GEPU_current', 'GEPU_ppp']]
gepu_long = gepu_january[['Year'] + gepu_cols].copy()
gepu_long['Year'] = gepu_long['Year'].astype(int)

print(f"GEPU (January only): {gepu_long.shape}")
print(f"GEPU countries: {gepu_cols}")

# Section 4: Merge datasets
print("\nSection 4: Merging datasets...")

# Find common countries across all datasets
crime_countries = set(crime_long['Country'].unique())
fi_countries = set(fi_long['Country'].unique())
gepu_countries = set(gepu_cols)

print(f"Crime index countries: {len(crime_countries)}")
print(f"Foreign investment countries: {len(fi_countries)}")
print(f"GEPU countries: {len(gepu_countries)}")

# Find intersection of countries (only merge if country exists in all datasets)
common_countries = crime_countries.intersection(fi_countries).intersection(gepu_countries)
print(f"Common countries across all datasets: {len(common_countries)}")
print(f"Sample common countries: {sorted(list(common_countries))[:5]}")

# Filter datasets to only include common countries
crime_long = crime_long[crime_long['Country'].isin(common_countries)].copy()
fi_long = fi_long[fi_long['Country'].isin(common_countries)].copy()

# Filter GEPU to only keep common country columns
gepu_common_cols = [col for col in gepu_cols if col in common_countries]
gepu_long = gepu_long[['Year'] + gepu_common_cols].copy()

# Melt GEPU to long format
gepu_long = gepu_long.melt(id_vars=['Year'], var_name='Country', value_name='gepu')
gepu_long = gepu_long.dropna(subset=['gepu'])

print(f"Crime (filtered): {crime_long.shape}")
print(f"FI (filtered): {fi_long.shape}")
print(f"GEPU (filtered): {gepu_long.shape}")

# Merge all datasets on Country and Year (left join on crime as base)
# Start with crime index as the base
panel = crime_long.copy()
panel = panel.rename(columns={'crime_index': 'crime_index'})

# Add foreign investment
panel = panel.merge(fi_long[['Country', 'Year', 'foreign_investment']], 
                    on=['Country', 'Year'], 
                    how='left')

# Add GEPU
panel = panel.merge(gepu_long[['Country', 'Year', 'gepu']], 
                    on=['Country', 'Year'], 
                    how='left')

print(f"Merged panel shape: {panel.shape}")
print(f"Panel columns: {panel.columns.tolist()}")

# Section 5: Verify merge integrity
print("\nSection 5: Verifying merge integrity...")

# Check row counts
print(f"Total rows in merged panel: {len(panel)}")
print(f"Unique countries: {panel['Country'].nunique()}")
print(f"Year range: {panel['Year'].min()} - {panel['Year'].max()}")

# Check for duplicates
duplicates = panel.duplicated(subset=['Country', 'Year'])
print(f"Duplicate rows (Country, Year): {duplicates.sum()}")

if duplicates.sum() > 0:
    print("WARNING: Found duplicate rows!")
    print(panel[duplicates])

# Check for missing values
print(f"\nMissing values by column:")
print(panel.isnull().sum())

# Section 6: Save final panel
print("\nSection 6: Saving final analysis panel...")

# Save the merged panel
output_path = FINAL_DIR / "analysis_panel.csv"
panel.to_csv(output_path, index=False)
print(f"Panel saved to: {output_path}")

# Section 7: Create data dictionary
print("\nSection 7: Creating data dictionary...")

data_dictionary = """# Data Dictionary for analysis_panel.csv

## Overview
This dataset contains merged information from three sources:
- Crime Index (Numbeo)
- Foreign Direct Investment (World Bank)
- Geopolitical Risk Index (GEPU)

Data is structured as a panel dataset with countries as units and years as time periods.

## Columns

### Country
- **Description**: Name of the country
- **Type**: String
- **Values**: Country names (e.g., "United States", "China", "India")
- **Missing**: None

### Year
- **Description**: Year of observation
- **Type**: Integer
- **Range**: 2012-2024 (aligned to January observation for multi-month datasets)
- **Missing**: None

### crime_index
- **Description**: Numbeo Crime Index score
- **Type**: Float
- **Range**: 0-100 (higher values indicate higher crime)
- **Source**: Numbeo Crime Index
- **Note**: Originally from raw/numbeo_crime_index_2012_2025.csv
- **Missing**: Values are present for all Country-Year combinations in the common country set

### foreign_investment
- **Description**: Foreign Direct Investment Inflow
- **Type**: Float
- **Unit**: USD (current)
- **Source**: World Bank
- **Note**: Originally from raw/WorldForeignDirectInvestmentInflow
- **Missing**: May be present for earlier years or countries with sparse data

### gepu
- **Description**: Geopolitical Risk Index (January value)
- **Type**: Float
- **Range**: Continuous scale
- **Source**: Geopolitical Risk Index
- **Note**: Only January values are included to create one observation per year
- **Missing**: May be present for some Country-Year combinations

## Data Quality Notes

### Alignment Strategy
- Crime Index: Available from 2012 onwards
- Foreign Investment: Available from 1960-2024, filtered to common countries
- GEPU: Available from 2012 onwards, January values used for annual representation

### Common Countries
The dataset includes only countries that are present in all three data sources. 
This ensures consistency and enables proper panel analysis.

### Time Period
The analysis panel covers the period from 2012 to 2024, as this is the common 
period across all three sources.

## Data Processing Steps
1. Loaded all three processed datasets
2. Converted all datasets to long format (Country, Year, Values)
3. Filtered datasets to include only common countries across all three sources
4. For GEPU (which has monthly data), selected January values to create annual observations
5. Merged datasets using left join on Country and Year combinations
6. Saved final panel to data/final/analysis_panel.csv

## Generated
{timestamp}
"""

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_dictionary = data_dictionary.format(timestamp=timestamp)

dict_path = FINAL_DIR / "data_dictionary.md"
with open(dict_path, 'w') as f:
    f.write(data_dictionary)

print(f"Data dictionary saved to: {dict_path}")

print("\n" + "=" * 80)
print("Final Panel Merge Process Completed Successfully!")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {output_path}")
print(f"  - {dict_path}")
print(f"\nFinal panel summary:")
print(f"  - Shape: {panel.shape}")
print(f"  - Countries: {panel['Country'].nunique()}")
print(f"  - Years: {panel['Year'].nunique()}")
print(f"  - Year range: {panel['Year'].min()}-{panel['Year'].max()}")