# AI Audit Appendix: Milestone 1

**Team:** Arjun, Daemian, Kade, Isidro  
**Date:** March 25, 2026  
**Project:** Corruption, Crime, and Foreign Investment Analysis

## AI Tools Used in M1

- [x] ChatGPT (data cleaning / API documentation)
- [x] GitHub Copilot (code completion / debugging)
- [ ] Claude (AI assistant)
- [x] Other: BeautifulSoup for web scraping guidance

## Detailed Log of AI Assistance

### 1. BeautifulSoup Web Scraping (Crime Index)
**Purpose:** Fetch Numbeo crime index data from HTML tables  
**Tool:** ChatGPT + GitHub Copilot  
**Usage:** Asked for guidance on parsing HTML tables with BeautifulSoup  
**Output:** Implemented `fetch_crime_index.py` to parse Numbeo crime index across 2012-2025  
**Impact:** Automated extraction of 963 country-year crime observations

### 2. Excel File Handling (GEPU / Policy Uncertainty)
**Purpose:** Read and process All_Country_Data.xlsx (World Economic Policy Uncertainty)  
**Tool:** GitHub Copilot  
**Usage:** Code completion for `pd.read_excel()` and openpyxl integration  
**Output:** `load_and_clean_policy_data.py` successfully extracts January GEPU values  
**Impact:** Processed monthly data into annual observations (275 rows)

### 3. Data Merging Strategy
**Purpose:** Merge 4 disparate datasets (Crime, FDI, GEPU, CPI) on Country-Year  
**Tool:** ChatGPT (conceptual help)  
**Usage:** Discussed best practices for multi-source panel data alignment  
**Output:** Implemented left-join strategy with country name harmonization  
**Impact:** Created final analysis panel with 280 complete observations (20 countries × 14 years)

### 4. Pandas Data Transformation
**Purpose:** Convert wide-format data (countries × years) to long-format panels  
**Tool:** GitHub Copilot  
**Usage:** Auto-completion for `pd.melt()`, `.str.extract()`, and conditional filtering  
**Output:** Standardized all datasets to (Country, Year, Value) structure for merging  
**Impact:** Enabled consistent merge logic across heterogeneous data sources

### 5. Regex & String Cleaning
**Purpose:** Standardize country names across datasets (US→United States, Czechia→Czech Republic, etc.)  
**Tool:** GitHub Copilot  
**Usage:** Suggested `.str.replace()` and `.replace()` patterns for country mapping  
**Output:** Country name harmonization table in `merge_final_panel.py`  
**Impact:** Reduced country name mismatches from ~40 to 0; achieved 20-country intersection

## Summary of AI Impact

- **Code robustness:** AI assistance improved error handling and edge cases (missing columns, invalid dates)
- **Development speed:** Copilot auto-completion reduced manual typing ~30%
- **Data quality:** Conceptual guidance from ChatGPT improved merging strategy
- **Testing:** Not yet used for test writing; future improvement for M2-M3

## Limitations & Caveats
- All AI-suggested code was manually reviewed and tested before integration
- All core project logic (merge strategy, exclusion criteria) designed by team
- AI used primarily for boilerplate code and exploratory questions
- No AI-generated figures, models, or analysis conclusions

## Files Affected by AI Assistance
- `code/fetch_crime_index_code/fetch_crime_index.py` (scraping logic)
- `code/load_and_clean_policy_data.py` (Excel reading)
- `code/load_and_clean_cpi_data.py` (data cleaning)
- `code/merge_final_panel.py` (merging and harmonization)