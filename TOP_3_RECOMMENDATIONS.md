# Top 3 Recommended Data Additions for M2+

**Date:** March 25, 2026  
**Status:** Ready to implement  
**Priority:** HIGH (significantly strengthen analysis)

---

## 🎯 Overview

These three datasets directly address gaps in your current analysis and enable critical robustness checks for Milestones 2 and 3.

| # | Dataset | Source | Why Important | Status |
|---|---------|--------|---------------|--------|
| 1 | GDP + Population | World Bank WDI | Normalize FDI; compare across country sizes | ✅ Script ready |
| 2 | World Governance Indicators | World Bank | Cross-validate corruption; control for institutions | ✅ Script ready |
| 3 | Democracy Index | V-Dem Institute | Explain *why* corruption affects FDI | 📋 Instructions provided |

---

## 1️⃣ GDP & Population (Highest Priority)

### Why Add It?
Your current analysis has a **hidden bias**: you're comparing FDI in the US ($500B) to Pakistan ($1B) directly—but the US has 4× the population and 20× the GDP. This confounds the corruption-FDI relationship.

### What It Enables
✓ **FDI as % of GDP** — Normalized measure (compare apples to apples)  
✓ **FDI per capita** — Individual-level economic impact  
✓ **Development controls** — Account for size/wealth differences in regression models

### Example Analysis
```
Current (biased):  Does corruption reduce FDI? (confounded by country size)
With GDP/pop:      Does corruption reduce FDI as % of GDP? (controls size effect)
```

### Implementation
```bash
# Install required package
pip install wbgapi

# Run fetch script
python code/fetch_world_bank_data.py

# This downloads:
# - GDP (constant 2015 US$)
# - GDP per capita (current US$)
# - Population
```

**Script:** `code/fetch_world_bank_data.py` ✅ Ready  
**Output:** `data/raw/world_bank_indicators.csv`

---

## 2️⃣ World Governance Indicators (High Priority)

### Why Add It?
**Your hypothesis test has a flaw:** You measure corruption via CPI (Transparency International's business expert surveys), but CPI is perception-based, not actual corruption. WGI's "Control of Corruption" is an independent measure from multiple sources—if both correlate with FDI, your finding is robust.

### What It Enables
✓ **Validation:** Do WGI corruption findings match your CPI findings?  
✓ **Multi-indicator approach:** Show CPI + WGI + WB corruption measures all point same direction  
✓ **Institutional controls:** Rule of Law as control variable (is it rule of law, not corruption, driving FDI?)  
✓ **Robustness check:** Political stability may explain some FDI variation

### The Three WGI Measures
| Indicator | Scale | Meaning |
|-----------|-------|---------|
| Control of Corruption | -2.5 to +2.5 | How much is corruption controlled? |
| Rule of Law | -2.5 to +2.5 | How strong is legal system? |
| Political Stability | -2.5 to +2.5 | How stable is political environment? |

### Implementation
```bash
# Run fetch script
python code/fetch_world_governance_indicators.py

# This downloads all three WGI measures 2012-2025
```

**Script:** `code/fetch_world_governance_indicators.py` ✅ Ready  
**Output:** `data/raw/world_governance_indicators.csv`

---

## 3️⃣ Democracy Index (Medium Priority)

### Why Add It?
**Final mechanism test:** Your key hypothesis is that corruption reduces FDI. But *why*? Is it:
- Because corrupted countries are undemocratic? (institutions)
- Because democracy strengthens rule of law? (legal)
- Because democracies are more transparent? (perception)

Democracy Index answers this by measuring extent of democratic institutions.

### What It Enables
✓ **Mechanism testing:** Is effect via institutional quality or corruption per se?  
✓ **Subsample analysis:** Does relationship differ in democracies vs. autocracies?  
✓ **Interaction effects:** Does democracy × corruption matter?

### Implementation (Manual Download)
V-Dem Democracy Index cannot be fetched via API easily. Instead:

1. **Go to:** https://www.v-dem.net/
2. **Download:** Data download → Select variables:
   - `v2x_polyarchy` (Electoral democracy index)
   - `v2x_libdem` (Liberal democracy index)
3. **Filter:** Countries in your dataset, years 2012-2025
4. **Save to:** `data/raw/vdem_democracy_index.csv`

**Alternative simpler measure:**  
Use "Elections" as proxy from Wikipedia Democracy Index (simpler, less detailed)

---

## 📊 Integration Workflow (M2)

### Step 1: Download All Three (15 minutes)
```bash
# Run scripts in sequence
python code/fetch_world_bank_data.py
python code/fetch_world_governance_indicators.py

# For Democracy Index: Manual download from V-Dem (5 min)
# Save to data/raw/vdem_democracy_index.csv
```

### Step 2: Merge Into Analysis Panel (create new script)
Update `code/merge_final_panel.py` to include:
```python
# Load new datasets
wdi_df = pd.read_csv('data/processed/world_bank_indicators_clean.csv')
wgi_df = pd.read_csv('data/processed/world_governance_indicators_clean.csv')
dem_df = pd.read_csv('data/processed/vdem_democracy_index_clean.csv')

# Merge with existing panel on Country + Year
final_panel = analysis_panel.merge(wdi_df, on=['Country', 'Year'], how='left')
final_panel = final_panel.merge(wgi_df, on=['Country', 'Year'], how='left')
final_panel = final_panel.merge(dem_df, on=['Country', 'Year'], how='left')

# Create normalized FDI variables
final_panel['fdi_as_pct_gdp'] = (final_panel['foreign_investment'] / final_panel['gdp_constant_2015_usd']) * 100
final_panel['fdi_per_capita'] = final_panel['foreign_investment'] / final_panel['population']
```

### Step 3: New Analysis Panel (30 variables)
Result: `analysis_panel_with_all_indicators.csv`
- Original 6 variables
- Plus 18 derived variables (already created)
- Plus 3-4 new WDI variables (GDP, population)
- Plus 3 WGI variables (corruption, rule of law, stability)
- Plus 2-3 derived normalized variables (FDI/GDP, FDI per capita)
- **Total: ~30-35 variables for M2 regression**

---

## 🧪 M2 Regression Models Enabled

### Model 1: Baseline (Current Analysis)
```python
fdi ~ corruption + crime + uncertainty
```

### Model 2: With Normalization (GDP Control)
```python
fdi_as_pct_gdp ~ corruption + crime + uncertainty + log(gdp)
fdi_per_capita ~ corruption + crime + uncertainty + log(population)
```

### Model 3: Validated Corruption (WGI + CPI)
```python
fdi ~ cpi_corruption + wgi_corruption + wgi_rule_of_law + crime + uncertainty
# Test: do both corruption measures matter?
```

### Model 4: Mechanism Test (Institutions)
```python
fdi ~ corruption + democratic_index + rule_of_law + crime + uncertainty
# Test: is corruption or democracy the key factor?
```

### Model 5: Full Model (All Controls)
```python
fdi_as_pct_gdp ~ cpi_corruption + wgi_corruption + rule_of_law + 
                 political_stability + democracy + crime + uncertainty + 
                 log(gdp) + log(population) + time_trend
```

---

## 📈 Expected Outcomes

| Dataset | Outcome if Robust | Outcome if Not Robust |
|---------|-------------------|----------------------|
| **WDI (GDP/Pop)** | FDI/GDP effect stable across models | Effect disappears (was just size) |
| **WGI (Governance)** | CPI + WGI both negative on FDI | Only CPI matters (WGI spurious) |
| **V-Dem (Democracy)** | Democracy captures some corruption effect | Corruption is sole driver |

---

## 📋 Implementation Timeline

### Week 1 (Now): 
- ✅ Create `fetch_world_bank_data.py`
- ✅ Create `fetch_world_governance_indicators.py`
- 📋 Manual download V-Dem democracy data

### Week 2:
- 📋 Run both scripts
- 📋 Create cleaning scripts for each
- 📋 Update `merge_final_panel.py`
- 📋 Generate new enhanced panel

### Week 3:
- 📋 Create derived variables (FDI/GDP, FDI per capita)
- 📋 Run 5 regression models above
- 📋 Compare coefficients across models

---

## ✅ Files Ready

| File | Status | Purpose |
|------|--------|---------|
| `code/fetch_world_bank_data.py` | ✅ Created | Download GDP, population |
| `code/fetch_world_governance_indicators.py` | ✅ Created | Download WGI corruption, rule of law, stability |
| **Manual:** V-Dem | 📋 Instructions | Download democracy index (cannot automate) |

---

## 🚀 Next Steps

1. **Install dependency:**
   ```bash
   pip install wbgapi
   ```

2. **Test World Bank fetch:**
   ```bash
   python code/fetch_world_bank_data.py
   ```

3. **Test WGI fetch:**
   ```bash
   python code/fetch_world_governance_indicators.py
   ```

4. **Create cleaning scripts** for both new datasets (similar to existing `load_and_clean_*.py`)

5. **Update merge script** to include new data sources

6. **Generate M2 regression results** with all 5 models above

---

## 💡 Questions to Answer in M2 Report

With these datasets, you can now answer:

1. **Is corruption the problem, or country size?** (GDP normalization test)
2. **Do multiple corruption measures agree?** (CPI vs. WGI test)
3. **Is it corruption or institutions?** (Rule of Law control test)
4. **Does democracy explain the effect?** (Democracy mechanism test)
5. **How robust are findings to data sources?** (Multivariate specification test)

---

**Created:** March 25, 2026  
**Next Milestone:** M2 (Regression Analysis with All Controls)
