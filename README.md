[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22639674&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

Team Name: Arjun, Daemian, Kade, Isidro

Research Question: How does perceived corruption and crime of a country affect countries foreign investment based on Corruption Perceived Index, Foreign Direct Investment, Crime Index, and Economic Uncertainty worldwide?


## Installation

Install required dependencies:

```bash
pip install pandas requests beautifulsoup4
pip install pytest           # for running tests
```

## Data Sources

### Crime Index Data
- **Source:** Numbeo Crime Index
- **Raw File:** `data/raw/numbeo_crime_index_2012_2025.csv`
- **Processed File:** `data/processed/crime_index_wide.csv`
- **Coverage:** 2012-2025

The crime index data includes perceived crime and safety metrics for countries worldwide.

### Foreign Direct Investment (FDI) Data
- **Source:** World Development Indicators (World Bank)
- **Raw File:** `data/raw/WorldForeignDirectInvestmentInflow`
- **Processed Files:**
  - `data/processed/fdi_countries_x_years.csv` — Countries as rows, years (1960-2024) as columns
  - `data/processed/fdi_transposed_years_x_countries.csv` — Years as rows, countries as columns
- **Coverage:** 1960-2024
- **Metric:** Foreign direct investment, net inflows (BoP, current US$)
- **Countries:** 266 countries/regions

### Corruption Perceptions Index (CPI) Data
- **Source:** Transparency International
- **Raw File:** `data/raw/corruption_perceptions_index_raw.csv` (requires manual download)
- **Template:** `data/raw/CPI_template.csv`
- **Processed Files:**
  - `data/processed/corruption_perceptions_index_processed.csv` — Long format (Country, Year, CPI_Score)
  - `data/processed/corruption_perceptions_index_wide.csv` — Wide format (Countries as rows, years as columns)
- **Coverage:** 2012-present
- **Metric:** Corruption Perceptions Index Score (0-100 scale, higher = less corruption)
- **Countries:** ~180+ countries
- **Status:** ⚠️ Requires manual download from Transparency International

## Fetching and Processing Data

### Crime Index Data

We include a utility module in `src/fetch_crime_index.py` that downloads and parses the Numbeo Crime Index table.

Usage examples:

```bash
# fetch a single year
python -m src.fetch_crime_index --year 2025 \
    --out data/raw/numbeo_crime_index.csv

# fetch a range of years and combine into one file
python -m src.fetch_crime_index --start 2012 --end 2025 \
    --out data/raw/numbeo_crime_index_2012_2025.csv

# disable caching to re-download
python -m src.fetch_crime_index --start 2012 --end 2025 \
    --out data/raw/numbeo_crime_index_2012_2025.csv \
    --no-cache
```

### FDI Data

The FDI data from World Development Indicators is processed using:

```bash
# Transpose to countries-as-rows format
python src/reverse_transpose_fdi.py

# Transpose to years-as-rows format
python src/transpose_fdi_data.py
```

### Corruption Perceptions Index (CPI) Data

CPI data requires manual download from Transparency International since it's not available via API.

**Steps to get CPI data:**

1. Download CPI rankings (2012-present) from one of these sources:
   - **Official:** https://www.transparency.org/en/cpi/ (recommended)
   - **World Bank DataBank:** https://databank.worldbank.org/
   - **Kaggle:** https://www.kaggle.com/datasets (search "corruption perceptions index")

2. Save the downloaded file to: `data/raw/corruption_perceptions_index_raw.csv`

3. Ensure the file has these columns: `Country`, `Year`, `CPI_Score`

4. Process the data:
   ```bash
   python src/process_cpi_data.py
   ```

5. This will generate:
   - `data/processed/corruption_perceptions_index_processed.csv` (long format)
   - `data/processed/corruption_perceptions_index_wide.csv` (wide format)

A template file is available at `data/raw/CPI_template.csv` showing the expected format.


Goal: Establish a relationship between corruption and/or foreign direct investment and crime, which can then be used to address the associated economic effects of corruption.

## Data Specifications

### Crime Index
- **Years:** 2012-2025
- **Observations:** Countries/cities with crime metrics
- **Metrics:** Perceived crime level, safety ratings
- **Format:** Wide (crime_index_wide.csv)

### Foreign Direct Investment
- **Years:** 1960-2024 (65 years)
- **Countries/Regions:** 266
- **Metric:** Net inflows in current US dollars
- **Formats Available:**
  - Wide format: Countries as rows, years as columns (266 × 65)
  - Long-wide format: Years as rows, countries as columns (65 × 266)

### Corruption Perceptions Index
- **Years:** 2012-2024
- **Countries:** ~180+ countries
- **Metric:** CPI Score (0-100 scale, higher = less corruption)
- **Formats Available:**
  - Long format: Country, Year, CPI_Score
  - Wide format: Countries as rows, years as columns
- **Status:** Ready after manual download & processing

## Running Tests

```bash
pytest tests/test_fetch_crime_index.py -v
```

## Configuration

Verify data paths are correctly configured:

```bash
python src/config_paths.py
```

## Next Steps

- [ ] Merge crime index and FDI datasets by country and year
- [ ] Add corruption metrics from another data source
- [ ] Handle missing data and temporal alignment
- [ ] Exploratory data analysis (EDA)
- [ ] Statistical modeling and regression analysis
- [ ] Generate visualizations and summary tables

## Project Structure

```
├── src/                           # Python modules and utilities
│   ├── __init__.py
│   ├── config_paths.py            # Path configuration
│   ├── fetch_crime_index.py       # Crime index web scraper
│   ├── transform_crime_index.py   # Crime index data transformation
│   ├── transpose_fdi_data.py      # FDI data transpose (years→rows)
│   └── reverse_transpose_fdi.py   # FDI data transpose (countries→rows)
├── data/
│   ├── raw/                       # Original data (read-only)
│   │   ├── numbeo_crime_index_2012_2025.csv
│   │   └── WorldForeignDirectInvestmentInflow
│   ├── processed/                 # Cleaned & transformed data
│   │   ├── crime_index_wide.csv
│   │   ├── fdi_countries_x_years.csv
│   │   └── fdi_transposed_years_x_countries.csv
│   └── final/                     # Analysis-ready panel data
├── results/
│   ├── figures/                   # Visualizations
│   ├── tables/                    # Regression tables, summary stats
│   └── reports/                   # Milestone reports & memos
├── tests/                         # Test suite
├── code/                          # Analysis code & notebooks
└── README.md
```

### Key Files

- **config_paths.py** — Centralized path configuration for data import/export
- **fetch_crime_index.py** — Web scraper for Numbeo Crime Index data
- **transform_crime_index.py** — Data cleaning and reshaping for crime index
- **transpose_fdi_data.py** — Converts FDI from countries×years to years×countries format
- **reverse_transpose_fdi.py** — Converts FDI from years×countries back to countries×years format
