# M1 Data Quality Report
**Team:** [Your Team Name]
**Date:** [Submission date]
## 1. Data Sources
### REIT Master Panel
- **Source:** Instructor-provided (CRSP/Ziman)
- **Raw file:** `data/reit_master_raw.csv`
- **Coverage:** [X] REITs, [Y] months ([start month] to [end month])
- **Initial row count:** [X rows before cleaning]
### FRED Economic Indicators
- **Fetched via:** pandas-datareader (FRED API)
- **Series:**
- FEDFUNDS (Effective Federal Funds Rate)
- MORTGAGE30US (30-Year Fixed Mortgage Rate)
- CPIAUCSL (Consumer Price Index, All Urban Consumers)
- UNRATE (Unemployment Rate)
- **Date range:** [start] to [end]
## 2. Data Cleaning Decisions
### Missing Values
- **Returns (ret):** [X%] missing. Decision: [Drop rows / Impute with 0 / Carry
forward last known value]. Justification: [Why this choice makes economic sense]
- **Market cap (mcap):** [X%] missing. Decision: [Your approach]. Justification:
[Why]
- **Sector:** [X%] missing. Decision: [Your approach]. Justification: [Why]
### Outliers
- **Returns > 200% or < -100%:** [X rows]. Decision: [Winsorize at 99th percentile
/ Drop / Keep]. Justification: [Why]
- **Market cap < $10M:** [X rows]. Decision: [Drop per universe definition].
Justification: [Small REITs excluded to match institutional focus]
### Duplicates
- **Duplicate permno-month pairs:** [X rows]. Decision: [Keep first / Average /
Drop]. Justification: [Why]
### Data Type Corrections
- **ym:** Converted from [format] to [pandas datetime / YYYY-MM string]. Method:
[pd.to_datetime()]
- **sector:** Standardized to [X unique sectors]. Merged similar categories:
[e.g., "Retail" and "Shopping Centers" → "Retail"]
## 3. Merge Strategy
### Merge Type
- **How:** [left / inner / outer] join
- **On:** Month (ym in REIT data, DATE in FRED data)
- **Alignment:** FRED data is monthly; matched to REIT month-end observations
### Data Integrity Checks
- **Before merge:** REIT rows = [X], FRED rows = [Y]
- **After merge:** Combined rows = [Z]
- **Verification:** [X = Z confirms no accidental row loss]
- **Missing after merge:** [0 economic indicator NaNs if FRED coverage matches
REIT date range]
## 4. Final Dataset Summary
### Panel Structure
- **Entity variable:** permno (REIT identifier)
- **Time variable:** ym (month)
- **Balanced vs. Unbalanced:** [Unbalanced - REITs enter/exit over time]
- **Final dimensions:** [X unique REITs] × [Y unique months] = [Z observations]
### Sample Statistics (After Cleaning)
| Variable | Mean | Std Dev | Min | Max | Missing (%) |
|----------|------|---------|-----|-----|-------------|
| ret | [X] | [Y] | [Min] | [Max] | [0%] |
| mcap | [X] | [Y] | [Min] | [Max] | [0%] |
| fedfunds | [X] | [Y] | [Min] | [Max] | [0%] |
| mortgage30us | [X] | [Y] | [Min] | [Max] | [0%] |
### Data Quality Flags
- **High-quality data:** [X%] of observations have complete REIT + economic data
- **Concerns:** [Any remaining issues, e.g., "Some REITs have only 12 months of
data; may exclude from panel models if insufficient variation"]
## 5. Reproducibility Checklist
- [ ] Script runs without errors from scratch
- [ ] All file paths are relative (e.g., `data/reit_master_raw.csv`, not
`C:\Users\...`)
- [ ] Output saved to `results/reit_analysis_panel.csv`
- [ ] No manual Excel editing required
- [ ] Metadata documented (this report)
## 6. Ethical Considerations
**What data are we losing?**
- By dropping [small-cap REITs / missing returns / outliers], we may be excluding
[specific segments of the market, e.g., distressed REITs during crises].
- **Implication:** Our analysis will be biased toward [larger, more stable REITs].
This is acceptable for an institutional investment focus but may not capture the
full REIT universe.
**Transparency:** All cleaning decisions are documented and defensible.
Alternative approaches (e.g., imputation vs. deletion) should be tested in
robustness checks (M3).
---
**Sign-off:** [All team member names]