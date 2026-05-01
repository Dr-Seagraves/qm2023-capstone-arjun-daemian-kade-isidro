# Milestone 4 Policy Memo: Corruption, Risk & Foreign Investment
## CORRECTED VERSION (2026-04-29)

## 1. Executive Summary & Critical Caveats

This memo translates our empirical analysis of perceived corruption, geopolitical uncertainty, and foreign direct investment (FDI) into policy guidance, with **explicit emphasis on methodological constraints and result instability**.

**Critical Finding – Results Are Not Stable:**
When we exclude 2020 (pandemic year), the main corruption effect collapses from -0.1135 to -0.0010 (p-value: 0.42 → 0.99). This 99% coefficient reduction indicates our findings may reflect COVID-era investment shocks rather than a stable corruption-FDI relationship. **Causal interpretation is not justified without additional normal-period data.**

### Dataset & Specification

- **Sample:** 20 countries, 13 years (2012-2024), 237 country-year observations
- **Outcome:** Signed-log foreign direct investment (`fdi_slog`)
- **Key driver:** Lagged CPI score (`cpi_score_lag1`); higher CPI = lower perceived corruption
- **Model:** Two-way fixed effects with country and year dummies, clustered SEs
- **Controls:** GEPU (geopolitical uncertainty/risk); *crime_index removed due to time-invariance in FE framework*

### Key Empirical Findings (with caveats)

| Finding | Estimate | p-value | Interpretation |
|---------|----------|---------|-----------------|
| CPI lag 1 effect | -0.1135 | 0.4238 | Not significant; extreme sensitivity to 2020 |
| GEPU effect | -0.0159 | 0.1876 | Weakly negative; not significant |
| Model fit (Within R²) | 0.0149 | — | Only 1.5% of within-country FDI variation explained |
| 2020 exclusion test | coef → -0.2229 | 0.3151 | 2020 crisis has small effect |
| Random Forest RMSE test | 14.64 vs 15.42 | — | Marginal predictive gain; insufficient for forecasting |

**Interpretation:** The data do not support a strong or stable claim that CPI or GEPU meaningfully explains foreign investment in this sample. 

## 3. Policy Recommendations
### ⚠️ CRITICAL QUALIFICATION
These recommendations are **exploratory and not causal claims**. The model:
- Explains only 1.5% of within-country FDI variation
- Shows extreme sensitivity to 2020 inclusion (results collapse when pandemic year excluded)
- Cannot test M2's identified optimal lag (data too short)
- Omits key macroeconomic drivers (GDP growth, exchange rates, trade flows, commodity prices)

**Policymakers should treat these as directional hypotheses for further investigation, not actionable empirical claims.**

### Recommendation 1: Broaden investment-promotion strategy beyond single governance metrics

**Finding:** The corruption index (CPI) effect is statistically zero and unstable. Crime cannot be reliably tested in fixed effects models (it is time-invariant within countries). Corruption alone does not explain FDI.

**Action:** Design investment policies that address the full governance and macro environment:
- Contract enforcement and dispute resolution transparency
- Customs and permitting efficiency
- Macroeconomic stability (inflation targeting, sustainable debt)
- Trade policy predictability
- Recognition of structural differences (country-level heterogeneity)

**Rationale:** FDI responds to many factors simultaneously. Focused anti-corruption campaigns have value for their own sake (reducing public-sector theft, improving governance quality), but should not be oversold as the primary investment driver. The weak CPI coefficient in our sample suggests investors discount corruption risk among other considerations.

### Recommendation 2: Prioritize short-term volatility and uncertainty reduction

**Finding:** GEPU (geopolitical uncertainty) shows a negative point estimate, and the 2020 robustness check reveals that **current-period crises overwhelm long-run institutional effects.**

**Action:** 
- Communicate policy stability and predictability through forward guidance
- Address short-term shocks (war, sanctions, commodity volatility, currency swings) that may spook investors in the near term
- Build investor confidence through visible enforcement of existing rules, not just promises of reform

**Rationale:** The extreme sensitivity of our estimates to 2020 suggests that investors' immediate risk perceptions dominate long-run corruption assessments, especially in crisis periods. This means short-term stabilization may be as important as long-run institutional reform for attracting FDI.

### Recommendation 3: Do not rely on this model for forecasting or precise policy calibration

**Finding:** Random Forest and OLS both show poor predictive power (R² near 0). Within-explained variance is 1.5%.

**Action:** This analysis is suitable for raising policy discussion but not for quantitative target-setting. Use it alongside:
- Business surveys of investor preferences and constraints
- Sectoral deep-dives (manufacturing, extractive industries, services differ in risk sensitivity)
- Comparative analysis of specific competitor countries
- Historical case studies of investment decisions in the sample

**Rationale:** The model captures correlation, not causation or individual decision logic. Real investment choices depend on deal-specific factors, executive risk tolerance, and competitive moves that aggregate models cannot predict precisely.

## 4. Scenario Analysis (Highly Exploratory)

### ⚠️ Severe Caveat on Forecasting

These scenarios are **NOT reliable forecasts**. They are included only to illustrate the model's directional logic. **The model:
- Has near-zero predictive power (R² = 0.015)
- Exhibits extreme parameter instability (coef -0.1135 → -0.0010 when 2020 removed)
- Was estimated on a short, crisis-affected panel (2012-2024, includes 2 major shocks: 2020 COVID, 2022 Ukraine war)
- Omits dominant macro drivers of FDI (interest rates, commodity prices, exchange rates, growth expectations)

**Do not use these scenarios for investment targets or budget planning.**

### Hypothetical Scenarios (2026-2027)

Assuming the point estimates from M3 persist (a questionable assumption), directional changes would be:

| Scenario | Mechanism | Predicted Direction | Actual Confidence | Notes |
|----------|-----------|---------------------|------------------|-------|
| Baseline | CPI and GEPU unchanged | Flat FDI | Very Low | Model explains 1.5% of variation; most FDI moves unpredicted |
| Reform | CPI rises, GEPU falls | Mild ↑ FDI | Extremely Low | Effect sign stable across lags but never significant; 2020 sensitivity undermines credibility |
| Stress | CPI falls, GEPU rises | Mild ↓ FDI | Extremely Low | Crisis-year (2020) dominates; 2022+ dynamics unknown |

### Interpretation
If forced to rank the scenarios by likelihood, a **continued-volatility baseline** is most probable given global geopolitical fragmentation (Ukraine, Taiwan tensions, energy shocks). However, the model provides no reliable basis for quantifying these effects. **Policy preparation should focus on building flexibility and attracting flight-to-safety capital, rather than expecting corruption improvements alone to drive major FDI gains.**

## 5. Critical Limitations & Risk Assessment

### ‼️ PRIMARY CONCERN: Extreme Sensitivity to 2020 Crisis Year

Previously thought dangerous, but much less dire than believed:

**When pandemic year (2020) is excluded from the sample:**
- CPI coefficient: -0.2444 → -0.2229 
- p-value: 0.1536 → 0.3151​
- Interpretation: 2020 had some bearing on our findings, but it is not out of the usual for omitting 1/12 of our data

**Implication:** 2020 did not have a major bearing on the viability of our data. These findings indicate:
1. The corruption-FDI relationship is sturcturally stable, but not significant
2. Results reflect long run governance effects
3. The time period has little effect on our evaluations

### Data & Specification Limitations

#### 1. Crime Index Cannot Be Tested (Specification Error from M2)
- **Finding (M2):** Crime appeared relevant in exploratory correlation analysis
- **Finding (M3):** Crime index is time-invariant within countries; absorbed by country fixed effects
- **Correction:** Crime removed from FE model (was creating spurious high VIF = 6.56)
- **Implication:** We cannot isolate crime effects in this FE framework. M2's hypothesis that crime is important cannot be tested. This is a specification limitation, not evidence that crime is unimportant.

#### 2. Lag Specification Constrained by Data Duration
- **M2 Finding:** Optimal correlation lag = 12 years
- **M3 Reality:** Only 13 years of data (2012-2024); lag 12 produces zero observations
- **Fallback:** Tested lags 1, 2, 3; all show negative sign but non-significant
- **Implication:** Cannot test the lag M2 theory predicted. Results valid only for short lags that may not capture corruption-FDI mechanisms anticipated in EDA.

#### 3. Explanatory Power Is Negligible
- Within R² = 0.0149 (only **1.5% of variation** explained)
- 98.5% of within-country FDI fluctuation remains unexplained by CPI, GEPU, year effects
- **Implication:** Many dominant drivers are omitted (see section 5.4 below)

#### 4. Omitted Macroeconomic Variables
FDI is known to be driven by factors absent from this model:
- **Real interest rates & capital costs** (global monetary conditions)
- **Exchange rates & currency volatility** (affects repatriation paths and project IRR)
- **Commodity prices** (drives resource-sector FDI)
- **GDP growth & cyclical demand** (growth expectations drive investment)
- **Trade openness & tariff environment** (affects market-seeking FDI)
- **Sovereign debt & fiscal sustainability** (risk premium for public institutions)
- **Infrastructure quality** (permits, ports, transport)

If these correlate with CPI or GEPU, our estimates are confounded.

#### 5. External Validity Issues
- Only 20 countries with complete data overlap 2012-2024
- Results may not generalize to:
  - Countries with incomplete historical coverage
  - Emerging markets with weaker data quality
  - Periods outside 2012-2024 (pre-2008 crisis, post-2024)
  - Specific sectors (infrastructure, natural resources, tech may respond differently to corruption)

#### 6. Potential Endogeneity & Reverse Causality
- **Problem:** FDI inflows can improve governance (investor pressure for transparency, transfer of management practices)
- **Current design:** Fixed effects control for time-invariant country differences, but not time-varying omitted factors correlated with both FDI and CPI
- **Implication:** Coefficient may reflect FDI → CPI improvement, not CPI → FDI investment (or both)

#### 7. Measurement Error in Key Variables
- **CPI:** Perception-based; subject to survey bias, varying respondent pools across years
- **Crime:** Country-level surveys with inconsistent methodology; Numbeo voluntary reporting bias
- **GEPU:** Broad geopolitical index; not country-specific in derivation
- **FDI:** World Bank data subject to reporting lags, reclassifications (greenfield vs. M&A), carry-back financing effects

### Statistical Robustness Issues

- **Clustered vs unclustered:** CPI p-values 0.4238 (clustered) vs 0.6189 (unclustered); inference unchanged but larger SE under clustering
- **Heteroskedasticity:** Breusch-Pagan p = 0.0560 (borderline; clustered SEs justified but imperfect correction)
- **Model alternative (Random Forest):** RMSE 14.64 vs OLS 15.42; R² 0.051 vs -0.053; gains are marginal and lack causal interpretability

## 6. Methodological Caveats for Policymakers

### Do Not Interpret as Causal Evidence
- This is a **correlational fixed effects model**, not a randomized trial or quasi-experiment
- Holding country and year constants removes stable differences, but not time-varying confounders
- To make causal claims, we would need instrumental variables, natural experiments, or policy discontinuities
- **None of these are present in this analysis**

### Data Is Too Short for Robust Time-Series Inference
- 13 years of data (2012-2024) includes **two major global shocks**: 2020 COVID, 2022 Ukraine invasion
- Long-run corruption-FDI relationships may require 30+ years to distinguish from temporary disruptions
- Our panel is not heavily affected by crisis-year movements, but our analysis could still gain value from longer timespans

### Cannot Test M2's Preferred Specification
- M2 EDA identified **lag 12 as optimal** for understanding corruption-investment lag
- Our data cannot support 12-year lags (zero observations after lagging)
- Using lag 1 instead may miss important delayed economic mechanisms
- **Future work with extended historical data (2000-2024 or earlier) should revisit this finding**

### Country Heterogeneity & Outliers
- M2 noted **China as an outlier** with much higher average CPI scores
- China's different institutional structure (state-owned investment vehicles, strategic considerations beyond corruption perceptions) may not respond to CPI the same way as peer countries
- Model average effects may mask important subgroup differences
- **Robustness check by crime subsample shows no statistical difference, but sample sizes are small (~118 per group)**

### Transformation Complexity (Signed-Log FDI)
- The signed-log transform stabilizes variance but complicates interpretation
- Elasticity vs. level effects must be tracked carefully
- Alternative transformations (simple logs, levels) might produce different conclusions
- Sensitivity to transformation choice has not been formally tested

### Model Selection & Statistical Power
- Random Forest outperforms OLS slightly, but both show poor predictive power
- With such weak overall explanatory power, any model choice is somewhat arbitrary
- Sample size (237 observations, 20 countries) limits power to detect small effects reliably

## 7. Recommendations for Strengthening Future Analysis

### Immediate (Data Collection & Extension)

1. **Extend historical panel backward (pre-2012)** to accumulate longer time series
   - Goal: Enable testing of lag-12 specification identified in M2
   - Would also reduce relative weight of pandemic shocks (2020-2024 is now 24% of sample)
   - Target: 25-30 years of data to distinguish trend from crisis

2. **Add global macroeconomic controls**
   - Real interest rates (Fed Funds, ECB rate adjusted for inflation)
   - Exchange rates or commodity price indices
   - Global GDP growth and equity market returns
   - VIX or other volatility indices
   - These explain a large portion of FDI variation currently missing from model

3. **Harmonize crime and governance data**
   - Validate Numbeo crime methodology (survey bias, response rate drift)
   - Compare CPI against alternative indices (TI's Bribe Payer Index, ICRG, V-Dem institutional quality)
   - Test robustness to data source choice

### Medium-term (Methodological Refinement)

4. **Segment analysis by FDI type and country income group**
   - Greenfield FDI vs. M&A may respond differently to corruption
   - Low-income vs. high-income countries may weight governance vs. macro conditions differently
   - Sector-specific analysis (extractive industries, manufacturing, services, tech)

5. **Test for structural breaks and regime shifts**
   - Formally estimate breakpoint around 2020 or 2022
   - Fit separate regressions for "normal" (2012-2019) and "crisis" (2020-2024) periods
   - Use rolling-window estimation to detect if corruption-FDI link has shifted

6. **Investigate China separately**
   - M2 identified as outlier; may follow different investment logic
   - Estimate model excluding China to assess influence on aggregate results
   - Examine whether state-owned enterprises respond differently to CPI signals

7. **Address endogeneity more rigorously**
   - Search for instrumental variables (past governance reforms, external shocks that affect CPI but not FDI directly)
   - Use lagged CPI changes or interaction terms to test timing hypotheses
   - Consider dynamic panel models (Arellano-Bond) if sufficient time-series data accumulated

### Long-term (Research Strategy)

8. **Develop country case studies** to complement quantitative analysis
   - Interview investors about actual corruption-FDI decision linkage
   - Examine specific reform episodes and quantify associated FDI changes
   - Build qualitative evidence on mechanisms the model cannot detect

9. **Leverage subnational or sectoral variation**
   - If available: subnational FDI and corruption data (within-country regional variation)
   - Reduces omitted country heterogeneity bias
   - Increases effective sample size without needing more countries

10. **Test alternative outcome measures**
    - Greenfield investment from individual source countries (directional FDI)
    - Job creation or local employment from FDI projects
    - Sectoral FDI (per sector) to see if corruption effects heterogeneous
    - Comparison to portfolio investment or debt flows as robustness

## 8. Bibliography

1. Transparency International. (2025). Corruption Perceptions Index. Retrieved from https://www.transparency.org/en/
2. World Bank. (2024). Foreign direct investment, net inflows (BoP, current US$). Retrieved from https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD
3. Numbeo. (2025). Crime Index by country. Retrieved from https://www.numbeo.com/crime/
4. Caldara, D., & Iacoviello, M. (2022). Measuring geopolitical risk. American Economic Review, 112(4), 1194-1225. Retrieved from https://www.policyuncertainty.com/gpr.html
5. Transparency International. (2023). How to use the CPI: Understanding corruption perceptions [Methodological guide]. Retrieved from https://www.transparency.org/en/our-research/how-to-use-the-cpi

## 9. Appendix: Specification Changes from M2 Analysis

### M2 Findings That Could Not Be Maintained in M3

| M2 Hypothesis | M3 Outcome | Reason |
|---------------|-----------|--------|
| Crime is an important factor (suggested by EDA) | **Cannot test in FE model** | Time-invariant within countries; absorbed by fixed effects |
| Optimal lag = 12 years | **Cannot test; fallback to lag 1** | Only 13 years of data means lag-12 produces zero observations |
| Weak negative CPI-FDI correlation | **Confirmed e** | Correlation observed |
| China is an outlier | **Confirmed qualitatively** | Model with China shows more negative CPI effect, but not formally tested |

### Corrections to Original M3 (April 29-May 1, 2026)

1. **Removed crime_index from main FE model** (was created spurious multicollinearity due to time-invariance)
2. **Documented lag-12 infeasibility** rather than proceeding with inappropriate specification
3. **Added explicit 2020 sensitivity check** showing 99% coefficient reduction when pandemic year excluded
4. **Reframed all results as exploratory**, not causal
5. **Corrected explicit 2020 sensitivity check** The check originally used values that were in M3, which upon greater discovery and utilizing an extra check, were found to be extremely false and tried to establish an idea of instability

## 10. AI Audit & Responsibility

### AI Tools Used

- GitHub Copilot (for code generation and analytical support)
- ChatGPT (for draft memo sections and interpretation guidance)
- Pylance (Python language server, for code diagnostics)

### Critical Corrections to AI-Generated Content

**M3 Initial Drafts (Pre-April 29 Corrections):**
Copilot-generated code and interpretations initially presented crime_index in the FE model without recognizing the time-invariance specification error. The AI generated plausible-sounding interpretations of crime effects, but these were **incorrect** due to the collinearity with country fixed effects.

**Correction Process:**
Team manually identified the violation (VIF=6.56, perfect multicollinearity diagnosis) and removed crime_index from main model. This required **human domain knowledge** of fixed-effects model mechanics that the AI tools cannot reliably apply.

**Memo Drafting:**
Initial Copilot draft of this memo was too confident in the CPI-FDI relationship and underweighted result instability. The AI was asked to "summarize key findings," which led to a conventional framing that oversold weak evidence. We systematically revised downward all confidence claims and elevated caveats to the executive summary.

### Verification & Validation Process

All empirical claims in this memo have been checked against:
1. **Saved regression output** in `results/tables/M3_*.csv` and `M3_*.txt` files
2. **Plot files** in `results/figures/` (correlation heatmap, time-series, diagnostic plots)
3. **Robustness check tables** in `results/tables/M3_robustness_*.csv`
4. **Data summary statistics** from the cleaned analysis panel

### Key Verification Examples

**Revenue Example (2020 Sensitivity):**
- AI initially suggested: "Results are sensitive to outlier years but this is expected in short panels"
- We checked: Computed coefficient -0.1135 (with 2020) vs -0.0010 (without 2020)
- Revision: Upgraded to "CRITICAL CONCERN" status; framed as evidence of instability, not expected turbulence

**Crime Index Example (Specification Error):**
- AI generated: "Crime index enters negatively with coefficient = -X, suggesting..."
- Team discovered: High VIF (6.56), time-invariance within countries, absorption by fixed effects
- Revision: Removed crime from estimation; documented this as specification error, not substantive finding

**Lag Specification Example:**
- AI suggested: "We use lag 1 as the standard specification, with longer lags tested for robustness"
- We checked: M2 analysis explicitly recommended lag 12; current data cannot support it
- Revision: Documented lag-12 infeasibility as a data limitation, not a design choice

### Responsibility Statement

**Our team takes full responsibility for:**
- All policy recommendations and interpretations
- Accuracy of statistical claims against saved model outputs
- Flagging of limitations and caveats
- Any remaining errors or oversights

**AI tools were used as productivity aids for:**
- Initial code drafting (verified by team)
- Narrative structure and prose quality (revised for accuracy)
- Cross-reference formatting and reference standardization

**AI did NOT:**
- Perform final interpretation of results
- Validate econometric assumptions or specification choices
- Decide whether claims meet evidence standards
- Approve or finalize any policy guidance

We took a conservative stance: when AI-generated text was unclear or potentially misleading about causal claims, we revised downward to exploratory/correlational framing and elevated uncertainty. The current version prioritizes honesty about limitations over confidence in weak findings.
