# Data Dictionary for analysis_panel.csv

## Overview
This dataset contains merged information from four sources:
- Crime Index (Numbeo)
- Foreign Direct Investment (World Bank)
- Geopolitical Risk Index (GEPU)
- Corruption Perceptions Index (Transparency International)

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
- **Range**: 2012-2025 (aligned to January observation for multi-month datasets)
- **Missing**: None

### crime_index
- **Description**: Numbeo Crime Index score
- **Type**: Float
- **Range**: 0-100 (higher values indicate higher crime)
- **Source**: Numbeo Crime Index
- **Note**: Originally from raw/numbeo_crime_index_2012_2025.csv
- **Status**: ⚠️ **PRESENT IN DATASET BUT NOT USED IN MAIN ANALYSIS** (see below)
- **Missing**: Values are present for all Country-Year combinations in the common country set

#### Why Crime Index Is Not Used in Main Models

**Finding**: Crime_index is time-invariant (or nearly time-invariant) within each country. 

**Implication in Fixed Effects (FE) Framework**: 
- In two-way FE models with country dummies, time-invariant variables are absorbed by country fixed effects
- This creates perfect collinearity: crime_index and the country indicator perfectly predict each other
- Results: VIF = 6.56 (extremely high), model fails to estimate crime effects

**What This Means**:
- Crime data was collected and included in exploratory analysis (M2 EDA)
- M2 found "crime is not an important factor" in correlation analysis
- M3 attempted to use crime as a control but discovered it's time-invariant
- **Crime is retained in the dataset for transparency and future robustness checks, but is excluded from main FE models**

**Where Crime Was Actually Used**:
1. **M2 (Exploratory)**: Scatter plot showing weak negative relationship with FDI
2. **M3 (Robustness)**: Split sample analysis (low-crime vs. high-crime countries, ~63-74 obs per group; no significant differences)
3. **M3 (ML Model)**: Random Forest feature importance (~13.9% importance, 3rd after GEPU and CPI)

**Future Research**:
If more years of data are obtained, crime variation within countries could also be explored. Currently, adding 15+ years of history (pre-2012) would allow testing whether crime changes correlate with FDI changes.

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

### cpi_score
- **Description**: Corruption Perceptions Index score
- **Type**: Float
- **Range**: 0-100 (higher values indicate lower perceived corruption)
- **Source**: Transparency International CPI 2025 Results (includes historical years)
- **Note**: Converted from country-level wide format into Country-Year format
- **Missing**: May be present for some Country-Year combinations due to country-name mismatches or unavailable observations

## Data Quality Notes

### Alignment Strategy
- Crime Index: Available from 2012 onwards
- Foreign Investment: Available from 1960-2024, filtered to common countries
- GEPU: Available from 2012 onwards, January values used for annual representation
- CPI: Available from 2012-2025, transformed from yearly columns to annual panel rows
- Country names: Harmonized using a shared mapping before merges (e.g., US→United States, UK→United Kingdom, Korea→South Korea)

### Common Countries
The dataset includes only countries that are present in all three data sources. 
This ensures consistency and enables proper panel analysis.

### Time Period
The analysis panel covers the period from 2012 to 2024, as this is the common 
period across all three sources.

## Data Processing Steps
1. Loaded all four processed datasets
2. Converted all datasets to long format (Country, Year, Values)
3. Filtered crime/FDI/GEPU datasets to include only common countries across those three sources
4. For GEPU (which has monthly data), selected January values to create annual observations
5. Converted CPI yearly score columns into a Country-Year `cpi_score` variable
6. Merged datasets using left join on Country and Year combinations
7. Saved final panel to data/final/analysis_panel.csv

## Generated
2026-02-25 20:34:41
