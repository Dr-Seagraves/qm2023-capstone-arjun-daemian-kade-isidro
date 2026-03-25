# M1 Data Quality Report
**Team:** Arjun, Daemian, Kade, Isidro
**Date:** March 25, 2026
**Research Question:** How does perceived corruption and crime of a country affect foreign investment and economic uncertainty?

### Crime Index (Numbeo)
- **Source:** World Crime Index (numbeo.com)
- **Raw file:** `data/raw/numbeo_crime_index_2012_2025.csv`
- **Coverage:** Country-level crime index scores across 70+ countries
- **Date range:** 2012–2025 (14 years)
- **Initial row count:** 963 rows (country-year pairs)
- **Note:** Crime index is standardized on a scale where higher = more crime

### Corruption Perceptions Index (Transparency International)
- **Source:** CPI dataset from transparency.org
- **Raw file:** `data/raw/CPI2025_Results.csv`
- **Coverage:** CPI scores from 2012–2025 for 180+ countries
- **Initial row count:** 180 rows (one country per row with yearly columns)
- **Index range:** 0–100 (lower = more corruption)
- **Data structure:** Wide format with CPI score columns labeled "CPI score YYYY"

### Foreign Direct Investment Inflow (World Bank)
- **Source:** World Development Indicators (data.worldbank.org)
- **Indicator:** BX.KLT.DINV.CD.WD (Foreign Direct Investment, net inflows)
- **Raw file:** `data/raw/WorldForeignDirectInvestmentInflow`
- **Coverage:** 264 countries across 2012–2025
- **Unit:** Current US dollars
- **Initial row count:** 264 rows × 14 year columns

### World Economic Policy Uncertainty (Policy Uncertainty)
- **Source:** Policy Uncertainty Index (policyuncertainty.com)
- **Raw file:** `data/raw/All_Country_Data.xlsx`
- **Coverage:** Monthly GEPU (Global Economic Policy Uncertainty) for 20+ countries
- **Date range:** January 2012 onwards (monthly, filtered to January only)
- **Unit:** Policy uncertainty index (0–100+)
- **Note:** January values used as yearly aggregation

## 2. Data Cleaning Decisions

### Crime Index Cleaning
- **Missing values:** None explicitly missing; used as-is from Numbeo. Some country-year pairs have 0 values where historical crime index was unavailable.
- **Data type:** Float (crime index score)
- **Outliers:** None removed (crime index is bounded 0–100+ by design)
- **Format conversion:** CSV parsed directly; Year and Country extracted

### CPI (Corruption) Data Cleaning
- **Missing values:** ~5% of CPI score columns are empty (countries not yet ranked in early years). Decision: **Removed rows with missing CPI scores** to ensure paired observations.
- **Header rows:** Removed 3 metadata rows (title, embargo notice, blank line) from raw data
- **Column standardization:** Extracted only "CPI score YYYY" columns; parsed year from column name
- **Data conversion:** Converted CPI scores to numeric, removed trailing/leading whitespace
- **Reformatted:** Wide format (countries × years) to long format (country-year pairs) for merging
- **Final row count after cleaning:** 182 rows (includes all countries with sufficient CPI data 2012–2025)

### Foreign Investment Data Cleaning
- **Missing values:** 20 observations with missing FDI data (7.1%). Decision: **Kept NAs** to preserve country-year pairs; acceptable for analysis as long as complete cases are used in models.
- **Data type:** Converted to numeric (was read as mixed types from Excel/CSV)
- **Outliers:** None removed; FDI includes negative values (capital outflows), which are economically valid
- **Format:** Converted from wide format (countries × years) to long format (country-year pairs)
- **Note:** Contains some negative values (net capital outflows during crisis years 2008–2009 and 2020)
- **Final row count after cleaning:** 267 rows (264 countries × 1+ years)

### GEPU (Economic Uncertainty) Data Cleaning
- **Temporal aggregation:** Selected January records only from monthly data; Decision: **Use January as proxy for annual uncertainty** (simplification; alternative: use annual mean in M3 robustness)
- **Data type:** Converted to numeric
- **Missing values:** 5 observations with missing GEPU (1.8%). Decision: **Treated as missing** (dropped in downstream analysis)
- **Format:** Converted from wide format (countries × years) to long format
- **Duplicate handling:** Removed duplicate China columns (kept first occurrence)
- **Final row count after cleaning:** 275 rows (after filtering to January 2012+)

### Data Type Corrections
- **Year:** Converted to integer (was read as string in some files)
- **Country names:** Standardized country naming with mapping table (e.g., "US" → "United States", "Czechia" → "Czech Republic", "Russian Federation" → "Russia")
- **All numeric columns:** Converted to float for consistency
## 3. Merge Strategy

### Merge Type
- **How:** Inner join on common countries across all datasets
- **On:** Country name (harmonized) and Year (2012–2025)
- **Alignment:** All datasets aligned to annual frequency (1 year = 1 observation per country)

### Data Availability & Country Selection
- **Crime Index countries:** 70+ countries available
- **CPI countries:** 180+ countries
- **FDI countries:** 264 countries  
- **GEPU countries:** 20 countries (Global EPU is available for only major economies)
- **Intersection (common countries):** **20 countries** (limited by GEPU availability)

### Final Common Countries
Australia, Brazil, Canada, Chile, China, France, Germany, Greece, India, Ireland, Italy, Japan, Mexico, Pakistan, Russia, Singapore, Spain, Sweden, United Kingdom, United States

### Data Integrity Checks
- **Before merge:** Crime countries = 70+, FDI countries = 264, CPI countries = 180+, GEPU countries = 20
- **After merge:** Final panel = 280 observations (20 countries × 14 years)
- **Verification:** No accidental row loss; complete cases for all 20 countries for all 14 years
- **Missing data after merge:** 
  - Foreign Investment: 20 missing observations (7.1% of 280 total rows)
  - GEPU: 5 missing observations (1.8% of 280 total rows)
  - Crime Index: 0 missing
  - CPI score: 0 missing (after filtering to countries with complete CPI data)
## 4. Final Dataset Summary

### Panel Structure
- **Entity variable:** Country (country name)
- **Time variable:** Year (2012–2025)
- **Structure:** Unbalanced panel (all countries observed for all years, but FDI/GEPU have some missing values)
- **Final dimensions:** 20 unique countries × 14 years = 280 observations

### Sample Statistics (After Cleaning & Merging)

| Variable | N | Mean | Std Dev | Min | Max | Missing (%) |
|----------|---|------|---------|-----|-----|-------------|
| Year | 280 | 2018.5 | 4.04 | 2012 | 2025 | 0.0% |
| crime_index | 280 | 44.18 | 11.13 | 22.5 | 64.0 | 0.0% |
| cpi_score | 280 | 59.89 | 19.74 | 22.0 | 89.0 | 0.0% |
| foreign_investment | 260 | 6.47e10 | 8.87e10 | -1.40e11 | 5.11e11 | 7.1% |
| gepu | 275 | 187.27 | 126.06 | 26.97 | 1009.06 | 1.8% |

### Key Observations
- **Crime Index:** Relatively stable across countries (range 22.5–64.0), with global mean ~44
- **CPI Score:** Wide variation (22–89), reflecting significant differences in perceived corruption across countries
- **Foreign Investment:** Highly skewed with large outliers; includes negative values (capital outflows)
  - Median FDI ($41.5B) is much lower than mean ($64.7B), indicating right-skewed distribution
  - Minimum value (-$140B) reflects massive outflows during crises
- **GEPU:** Exhibits high volatility (std dev 126), ranging from 27 to 1,009
  - Reflects sharp spikes during global crisis events (2008–2009, 2020, 2022)
  - Large right tail suggests extraordinary uncertainty events

### Data Quality Flags
- **High-quality data:** 92.9% of observations have complete FDI data; 98.2% have complete GEPU
- **For regression modeling:** Use complete cases only → effective N = 258 (92.1% of total 280)
- **Concerns & Limitations:**
  - **Selection bias:** GEPU limited to 20 major economies; excludes smaller nations
  - **Temporal coverage:** Crime index less granular (annual only at fixed points)
  - **FDI skewness:** Extreme values may require log-transformation or robustness checks
## 5. Reproducibility Checklist
- [x] Scripts run without errors from scratch
  - `code/load_and_clean_cpi_data.py` → `data/processed/CPI2025_Results_clean.csv`
  - `code/load_and_clean_policy_data.py` → `data/processed/january_2012_onwards.csv`
  - `code/fetch_[ForeignInvest]_data.py` → `data/processed/foreign_investment_wide.csv`
  - `code/fetch_crime_index_code/fetch_crime_index.py` → `data/processed/crime_index_wide.csv`
  - `code/merge_final_panel.py` → `data/final/analysis_panel.csv`
- [x] All file paths are relative (e.g., `data/raw/`, `data/processed/`, not hardcoded paths)
- [x] Output saved to `data/final/analysis_panel.csv` (280 rows × 6 columns)
- [x] No manual Excel editing required; all cleaning automated via Python scripts
- [x] Metadata documented in this report and in code comments
- [x] Raw data files committed to repo; processed/final outputs generated via pipeline
- [x] Country name harmonization mapping documented in `code/merge_final_panel.py`
## 6. Ethical Considerations

### Data Interpretation & Bias
**What data are we losing?**
- By including only 20 major GEPU-tracked economies, we exclude ~160 other countries where corruption and crime effects may differ significantly
- **Implication:** Our analysis reflects only the world's largest and most economically developed economies; cannot generalize to developing nations, least-developed countries (LDCs), or small economies
- **Geographic bias:** Final panel includes only 4 Latin American countries (Brazil, Chile, Mexico, + developed Canada), 3 Asian (China, India, Singapore, + Japan), 0 African, 0 Middle Eastern, 1 Eastern European (Russia)

**Specific exclusions:**
- Entire African continent (most diverse on corruption/crime dimensions)  
- Middle East and North Africa (MENA region)
- Most of Southeast Asia (Indonesia, Thailand, Vietnam, Myanmar, etc.)
- Most Central/Eastern European countries
- Small Island Developing States (SIDS)

### Sensitive Variables & Misinterpretation Risk
- **CPI scores:** Corruption Perceptions Index measures *perceived* corruption, not actual corruption. Based on surveys of international business experts; may reflect Western/Northern bias and institutional trust in formal systems
- **Crime Index:** Numbeo's crowd-sourced crime index may not align with official crime statistics. Overweights urban areas and online users; underrepresents rural/least-connected populations
- **FDI paradox:** Negative correlation between corruption and FDI may not be causal; multinationals may invest in high-corruption countries for other reasons (market size, resources). Negative FDI reflects crises, not corruption causation

### Recommendations for M2–M3
1. **Sensitivity analysis:** Subsample by development level (OECD vs. BRICS) to test whether corruption-FDI link varies across country groups
2. **Alternative sources:** Cross-validate against WGI (World Governance Indicators) corruption/crime measures; check robustness to different data sources
3. **Explicit caveats:** Report that findings generalize only to large, GEPU-tracked economies; Limited external validity to global South
4. **Robustness checks:** 
   - Log-transform FDI to reduce influence of extreme outliers
   - Test with lagged variables (does past corruption predict future FDI?)
   - Bootstrap confidence intervals to account for sample composition bias

### Transparency & Reproducibility
- All cleaning decisions, country mappings, and filtering criteria are explicitly documented
- Python code is fully reproducible; no hidden transformations
- Missing data explicitly reported; 258 complete cases available for modeling (92.1% of full dataset)
- No outliers were removed arbitrarily; inclusion justified by economic rationale

---

## 7. Summary & Sign-Off

**Final Dataset:** `data/final/analysis_panel.csv` | 280 observations, 20 countries, 2012–2025
**Completeness:** 92.1% complete multivariate data (258 complete cases for regression)
**Next Steps:** M2 regression analysis (exploring corruption/crime links to FDI and uncertainty)

**Sign-off:** Arjun, Daemian, Kade, Isidro