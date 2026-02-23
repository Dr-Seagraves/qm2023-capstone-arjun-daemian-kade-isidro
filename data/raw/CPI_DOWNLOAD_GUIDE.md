# Corruption Perceptions Index (CPI) Data - Setup Guide

## Overview
The Corruption Perceptions Index (CPI) is published annually by Transparency International and ranks countries by their perceived level of public sector corruption. This guide explains how to obtain and process CPI data for the project.

## Current Status
- ✅ **Template created:** `CPI_template.csv`
- ✅ **Processing scripts ready:** `src/process_cpi_data.py`
- ⚠️ **Raw data needed:** Must be downloaded manually

## Quick Start

### 1. Download CPI Data

**Option A: Transparency International (Recommended)**
- Visit: https://www.transparency.org/en/cpi/
- Find "Data & Findings" or "Download Data" section
- Download CPI rankings as CSV/Excel for years 2012-present
- Save to: `data/raw/corruption_perceptions_index_raw.csv`

**Option B: World Bank DataBank**
- Visit: https://databank.worldbank.org/
- Search for governance or corruption indicators
- Select countries and years (2012-2024)
- Download as CSV
- Save to: `data/raw/corruption_perceptions_index_raw.csv`

**Option C: Kaggle**
- Visit: https://www.kaggle.com/datasets
- Search: "corruption perceptions index"
- Download and extract dataset
- Save to: `data/raw/corruption_perceptions_index_raw.csv`

### 2. Verify Data Format

The downloaded file should have columns like:
- `Country` (or similar country identifier)
- `Year` 
- `CPI_Score` (or similar corruption metric)
- Optional: `Rank`, `Region`, `Standard_Error`, `Number_of_Sources`

See `CPI_template.csv` for expected format.

### 3. Process the Data

```bash
# From project root directory
python src/process_cpi_data.py
```

This will create:
- `data/processed/corruption_perceptions_index_processed.csv` (long format)
- `data/processed/corruption_perceptions_index_wide.csv` (wide format)

## Data Details

| Aspect | Details |
|--------|---------|
| **Years** | 2012-2024 |
| **Countries** | ~180+ countries |
| **Core Metric** | CPI Score (0-100 scale) |
| **Interpretation** | Higher score = less corruption |
| **Release Frequency** | Annual (usually January) |
| **Data Quality** | Based on expert surveys and governance databases |

## Expected Output Formats

### Long Format (processed)
```
Country,Year,CPI_Score
Afghanistan,2012,25.0
Afghanistan,2013,25.0
Albania,2012,36.0
...
```

### Wide Format (processed)
```
Country,2012,2013,2014,...,2024
Afghanistan,25.0,25.0,27.0,...,24.0
Albania,36.0,36.0,38.0,...,41.0
...
```

## Troubleshooting

**Problem:** "File not found" error when running `process_cpi_data.py`
- **Solution:** Make sure you've downloaded and saved the file to `data/raw/corruption_perceptions_index_raw.csv`

**Problem:** Column name mismatch errors
- **Solution:** Check that your downloaded file has required columns. Edit the script variable names if needed.

**Problem:** Year range doesn't match (e.g., only 2020-2024 instead of 2012-2024)
- **Solution:** Adjust the `year_range` parameter in `process_cpi_data.py` or download data with full range from source.

## Next Steps

After processing CPI data:
1. Merge with FDI data: `python src/merge_fdi_crime.py`
2. Merge all three datasets (FDI, Crime, CPI): Create `merge_all_data.py`
3. Run exploratory data analysis
4. Prepare for statistical modeling

## References

- Transparency International CPI: https://www.transparency.org/en/cpi/
- CPI Methodology: https://www.transparency.org/en/cpi/2023
- World Bank Governance: https://www.worldbank.org/en/topic/governance
- Related Research: Search Google Scholar for "corruption perceptions index foreign investment"

## Questions?

For data-related questions, refer to the main README.md or contact your team lead.
