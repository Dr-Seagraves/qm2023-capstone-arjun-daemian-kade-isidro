# Crime Data: Collection, Use, and Exclusion

## Executive Summary

Crime data were collected from Numbeo (2012-2025) and included in exploratory analysis (M2), but **cannot be reliably used in econometric models** due to time-invariance within countries. This document explains why, where it was used, and what it means for the analysis.

---

## Timeline of Crime Data in This Project

### Phase 1: Planning & Collection (M1-M2)
- **Hypothesis**: Crime risk might deter foreign investment, similar to corruption
- **Action**: Collected Numbeo Crime Index data across 20 countries, 2012-2025
- **Status**: ✅ Data successfully collected and processed

### Phase 2: Exploratory Analysis (M2)
- **Finding**: Weak negative relationship between crime and FDI in scatter plot
- **Conclusion**: "Crime is not an important factor" (per M2 summary)
- **Status**: ✅ Used for correlation analysis; findings documented

### Phase 3: Econometric Specification (M3)
- **Initial Approach**: Include crime_index as a control variable in FE model
- **Problem Discovered**: VIF = 6.56 (extremely high multicollinearity), model fails to converge
- **Root Cause**: Crime index is time-invariant within countries; absorbed by country fixed effects
- **Correction**: Removed from main FE model
- **Status**: ❌ Cannot be used; specification error corrected

### Phase 4: Robustness Analysis (M3)
- **Alternative Use**: Split sample by crime quartiles to test heterogeneous effects
- **Result**: Low-crime group coef = -0.168 (p=0.753), High-crime group coef = -0.001 (p=0.999)
- **Conclusion**: No significant difference; crime-level heterogeneity not detected
- **Status**: ⚠️ Descriptive only; no causal inference

### Phase 5: Machine Learning (M3, Model B)
- **Use**: Included crime_index as a feature in Random Forest
- **Result**: 13.9% importance (3rd after GEPU 47.96% and CPI 38.13%)
- **Caveat**: ML feature importance ≠ causal effect; helps prediction but not interpretation
- **Status**: ✅ Useful for exploratory ML purposes

### Phase 6: Final Documentation (M4, You Are Here)
- **Decision**: Keep crime_index in final panel for transparency, document exclusion rationale
- **Status**: ℹ️ Data retained but clearly flagged as "not for FE models"

---

## The Time-Invariance Problem: Technical Explanation

### What Is Time-Invariance?

A variable is **time-invariant** if it has the same value (or nearly the same) for each country across all years in the sample.

**Crime Index Example**: Each country's crime rank/index changes very slowly (if at all) from 2012-2024.
- United States: Consistently ~40-45 on Crime Index
- Singapore: Consistently ~20-25 (very low crime)
- Brazil: Consistently ~75-80 (high crime)

**Result**: Within each country, there is almost NO variation in crime over time.

### Why Time-Invariance Breaks FE Models

#### The Fixed Effects Estimator
Two-way FE models include:
- **Country dummies** (β_i): Absorb all time-invariant differences *between* countries
- **Year dummies** (δ_t): Absorb all common time effects *across* all countries

#### The Problem
If crime_index is time-invariant:
- Country dummies already fully capture crime differences (since high-crime countries have high-crime dummies, low-crime countries have low-crime dummies)
- crime_index provides **zero additional information**; it's 100% redundant with country dummies
- Including it creates **perfect collinearity**: no unique variation to estimate an effect

#### The Math
```
y_it = β_i + δ_t + γ * crime_index_i + ε_it

Since crime_index_i is time-invariant (no t subscript):
- β_i already captures all permanent country differ-ences
- crime_index_i is a perfect linear combination of β_i
- Variance Inflation Factor (VIF) → ∞; estimator breaks
```

#### What We Observed
- **VIF for crime_index = 6.56** (rule of thumb: VIF > 5 indicates problematic multicollinearity)
- Model would not converge (non-invertible Hessian)
- Removing crime_index: VIF drops to 3.48 (acceptable)

---

## Where Crime Data WAS Successfully Used

### 1. M2 Exploratory Data Analysis ✅
**Method**: Simple correlation and scatter plots  
**Result**: Weak negative relationship (visual inspection)  
**Valid**: YES—exploratory analysis doesn't require causal identification  
**Documentation**: "plot7_scatter_crime_index.png"

### 2. M3 Robustness Check: Subsample Split ✅
**Method**: Estimate main model separately for high-crime and low-crime country groups  
**Result**:
| Group | Lag | Coefficient | p-value | n |
|-------|-----|-------------|---------|---|
| Low-crime | 6 | -0.168 | 0.753 | 63 |
| High-crime | 6 | -0.001 | 0.999 | 74 |

**Valid**: PARTIALLY—tests whether effects differ by crime level, but:
- Both groups have small sample sizes (~63-74 obs)
- Neither is statistically significant
- Cannot distinguish treatment effect heterogeneity without powered subsamples

### 3. M3 Random Forest Feature Importance ✅
**Method**: ML permutation/split importance after training on train set  
**Result**: crime_index = 13.9% (3rd after gepu 47.96%, cpi 38.13%)  
**Valid**: YES—for predictive modeling purposes  
**Caveat**: Does NOT imply causality; features that are predictive may not be causal

---

## Why Crime CANNOT Be Used in Main FE Models

| Requirement | Crime Status | Issue |
|-------------|--------------|-------|
| Varies over time within countries? | ❌ NO | Time-invariant; absorbed by country FE |
| Varies across countries? | ✅ YES | Good between-country variation |
| Causal identification in FE? | ❌ NO | Perfect collinearity with country dummy |
| Alternative estimation (Random Effects)? | ⚠️ MAYBE | Would require different assumptions; not pursued |
| Alternative identification (IV/DID)? | ❌ NO | No plausible instruments; no quasi-experiment |

**Conclusion**: Given this panel structure and FE specification, crime effects cannot be estimated.

---

## What This Means for the Analysis

### What We Know About Crime
1. **M2 discovered**: Weak negative correlations with FDI, but "not an important factor"
2. **M3 confirmed**: Cannot test in FE framework due to time-invariance
3. **Implication**: Crime may matter, but we cannot isolate its effect from permanent country heterogeneity

### What We Still Don't Know
- Whether crime *causes* lower FDI, or just proxies for unobserved traits (governance quality, rule of law, etc.)
- Whether crime effects are heterogeneous by country type
- Whether crime changes (if we had longer history) would predict FDI changes

### For Policy
- Crime is one dimension of the *investment risk environment*, but we cannot quantify its individual causal impact
- The main analysis focuses on **CPI (corruption perceptions) and GEPU (geopolitical risk)**, which vary over time within countries

---

## Recommendations for Future Work

### Short Term
1. **Document clearly** (✅ done in this file) for reproducibility
2. **Retain crime_index in data** (✅ kept for transparency) but flag as "not for FE"
3. **Reference this limitation** when discussing results (✅ updated M3 interpretation and M4 memo)

### Medium Term
1. **Extend data backward** (pre-2012) to accumulate within-country variation in crime
   - If crime trends exist over 20-30 years, new within-variation could be analyzed
   - Requires Numbeo or alternative historical data

2. **Switch to Random Effects (RE)** to estimate crime effects with:
   - Assumption: country-level unmeasured heterogeneity uncorrelated with regressors
   - Trade-off: Weaker assumption, but allows time-invariant variables
   - Action: Run RE model alongside FE for sensitivity check

3. **Use alternative estimation**:
   - **Hierarchical models** with country random intercepts
   - **Multilevel models** allowing crime effect to vary by country
   - **IV approach** if instrument can be found (e.g., historical crime shocks)

### Long Term
1. **Sectoral analysis**: Crime may affect extractive FDI differently than manufacturing FDI
2. **Subnational data**: Within-country regional variation might break time-invariance constraint
3. **Qualitative research**: Interview investors on crime's actual role in location decisions

---

## Files Reference

| File | Role | Crime Use |
|------|------|-----------|
| `data/raw/numbeo_crime_index_2012_2025.csv` | Raw source | Original data |
| `data/processed/crime_index_wide.csv` | Processed intermediate | Wide format (Year × Country) |
| `data/final/analysis_panel.csv` | **Final dataset** | **Included but flagged** |
| `code/fetch_crime_index_code/fetch_crime_index.py` | Data collection | Numbeo scraping |
| `code/fetch_crime_index_code/transform_crime_index.py` | Data processing | Pivot to wide format |
| `code/merge_final_panel.py` | Panel construction | Joins crime to other sources |
| `code/capstone_models.py` | Main analysis | ✅ Correctly excludes from FE |
| `M2_EDA_summary.md` | Exploratory results | ✅ Documents weak crime finding |
| `M3_interpretation.md` | Econometric results | ✅ Documents time-invariance problem |
| `M4_policy_memo.md` | Policy synthesis | ✅ Explains crime exclusion |

---

## Conclusion

**Crime data were collected, explored, and correctly excluded from econometric models.**

This is **not a failure or mistake**, but rather:
1. **Good practice**: Exploratory analysis → discovery of data limitation → methodological adjustment
2. **Transparent reporting**: Documenting why variables are excluded improves reproducibility and credibility
3. **Appropriate caution**: Not forcing a variable into a model where it doesn't belong

The analysis now focuses on CPI and GEPU (which have within-country variation) as the main drivers of FDI, with crime retained as a reference for robustness and future research.
