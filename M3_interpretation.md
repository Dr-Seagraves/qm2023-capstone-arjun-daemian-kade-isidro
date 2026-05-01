# M3 Interpretation Memo (CORRECTED)

## Project Context

This memo interprets our Milestone 3 econometric results for the capstone question: how do corruption perceptions and risk conditions relate to foreign direct investment (FDI) across countries?

**IMPORTANT CORRECTION (2026-04-29):**
This version corrects three major methodological issues:
1. **Crime_index removed** from FE models (was time-invariant, absorbed by country FE, causing VIF=6.56)
2. **Lag specification corrected** to (1) use M2's identified optimal lag when possible; (2) test all candidate lags including lag 12
3. **Results interpreted with caution** given extreme sensitivity to 2020 inclusion (coef changes from -0.1135 to -0.001 when pandemic year excluded)

Outcome variable:
- fdi_slog (signed log transform of foreign investment)

Key driver:
- cpi_score_lag1 (one-year lag of CPI score; higher score indicates lower perceived corruption)
- *Note: M2 EDA found lag 12 optimal, but only 13 years of data means lag 12 has zero observations; fallback to lag 1*

Model A controls (CORRECTED):
- gepu (only control; crime_index excluded due to time-invariance in FE framework)

## Model A Headline Result (Required Fixed Effects Model)

We estimated a two-way fixed effects model with country and year effects, using clustered standard errors.

Key estimate for cpi_score_lag1:
- Coefficient: -0.1135
- Clustered SE: 0.1416
- p-value: 0.4238

Interpretation:
A 1-point increase in lagged CPI score is associated with a 0.1135 decrease in signed-log FDI, holding country and year fixed effects constant.

Statistical conclusion:
The estimate is not statistically different from zero at conventional thresholds.

Additional result:
- gepu coefficient: -0.0159, clustered p-value = 0.1876

Model fit:
- Within R2: 0.0149
- Model F-test p-value: 0.1832

Overall, within-country explanatory power is low, so most FDI variation is not captured by this baseline specification.

## Economic Mechanisms

Even with weak statistical significance, the underlying economic channels remain plausible:

1. Institutional confidence
Lower perceived corruption can improve investor confidence and reduce governance risk premia.

2. Uncertainty and financing conditions
Higher geopolitical risk can delay investment timing and reduce cross-border capital flows.

3. Transaction and compliance frictions
Higher corruption risk may raise informal costs and contract-enforcement uncertainty.

In this sample, these channels are not strongly identified after fixed effects and controls are included.

## Model B Summary (ML Comparison: Random Forest vs OLS)

Out-of-sample test performance:

- OLS: RMSE = 15.4246, R2 = -0.0530
- Random Forest: RMSE = 14.6389, R2 = 0.0515

Interpretation:
Random Forest provides a modest predictive improvement over OLS, but the gain is small.

Trade-off:
- OLS is easier to interpret economically.
- Random Forest is slightly better for prediction but less transparent for causal interpretation.

## Diagnostics (Required)

### Multicollinearity (VIF) - CORRECTED

**Before removing crime_index:**
- cpi_score_lag1: 7.18 ⚠️ HIGH
- crime_index: 6.56 ⚠️ HIGH
- gepu: 3.73

**After removing crime_index:**
- cpi_score_lag1: 3.48 ✓ IMPROVED
- gepu: 3.48

**Why crime_index was removed:**
In a fixed effects (FE) model with country effects, any time-invariant variable within a country is **absorbed by the country dummy** and becomes collinear with it. Since crime_index is largely constant within each country over our sample period (2012-2024), it cannot be estimated in the FE framework and creates spurious multicollinearity. This is a **specification error**, not a substantive finding about crime's importance.

**Correction:** Crime is retained for robustness checks and supplementary analysis but excluded from the main FE specification.

### Heteroskedasticity (Breusch-Pagan)

- LM p-value: 0.0560 (borderline; not rejected at 5% level)
- F p-value: 0.0557

Interpretation:
At the 5% level, we do not reject homoskedasticity, but p-values are close to the cutoff. Using clustered SEs remains appropriate.

### Residual Diagnostics

- Residuals vs fitted: results/figures/M3_residuals_vs_fitted.png
- Q-Q plot: results/figures/M3_qq_plot.png

Interpretation:
These plots support visual checks for nonlinearity, variance patterns, and normality departures.

## Robustness Checks (Required)

We implemented four robustness checks.

### 1. Clustered vs unclustered standard errors

For cpi_score_lag1:
- Clustered SE: 0.1416 (p = 0.4238)
- Unclustered SE: 0.2278 (p = 0.6189)

Conclusion:
Inference stays non-significant under both covariance assumptions.

### 2. Alternative lag structures (CORRECTED: now includes lag 12)

**Motivation for lag testing:** M2 EDA identified lag=12 as optimal correlation window. However, with only 13 years of data (2012-2024), lag 12 yields zero available observations. Therefore, we test lags 1-3 as feasible alternatives and document lag 12 unavailability.

- Lag 1: coef = -0.1135, p = 0.4238, nobs = 237
- Lag 2: coef = -0.1149, p = 0.4765, nobs = 217
- Lag 3: coef = -0.2444, p = 0.1536, nobs = 197
- Lag 12: coef = NaN (nobs = 0; insufficient data)

Conclusion:
Sign direction stable across feasible lags; all remain statistically weak. **Data limitation prevents testing M2's optimal lag.**

### 3. Excluding 2020 (NEW: explicit crisis sensitivity analysis)

**Critical Finding - Results are highly sensitive to pandemic year:**

- **Baseline (with 2020):** coef = -0.1135, p = 0.4238, nobs = 237
- **Excluding 2020:** coef = -0.0010, p = 0.9950, nobs = 217

**Interpretation:**
The parameter drops by 99% and p-value jumps from 0.42 to 0.99 when 2020 is excluded. This massive swing indicates:
- Results may be driven by pandemic-era FDI shocks rather than stable corruption-investment relationship
- 2020 was anomalous (Russian-Ukrainian War also began in Feb 2022, affecting data)
- Model lacks structural stability across economic regimes
- Caution warranted in interpreting effects as causal

### 4. Subsample estimation by crime level

- Low-crime countries: coef = -0.0296, p = 0.9063, nobs = ~118
- High-crime countries: coef = -0.1367, p = 0.4365, nobs = ~119

Conclusion:
No subgroup estimate is statistically significant. High-crime countries show slightly more negative point estimates, but not robustly so.

## Caveats and Identification Limits

1. **Crime_index specification (CORRECTED)**
Time-invariant regressors in FE models are absorbed by entity dummies and become collinear. Crime was removed from the main FE model to correct this specification error. Previous results claiming a crime effect were spurious.

2. **Data duration and lag specification**
M2 identified lag=12 as optimal for correlation. Our sample (2012-2024, 13 years) cannot support lag=12 analysis. Future work with extended historical data (pre-2012) should revisit this finding.

3. **Pandemic-driven results**
The 2020 robustness check reveals extreme parameter instability (coef: -0.1135 → -0.0010). Results appear driven by COVID/war-era FDI collapse, not stable corruption-investment nexus. Interpretation as causal is premature.

4. **Very low explanatory power**
Within R² = 0.0149 (only 1.5% of variation explained by these variables). Most FDI variation remains unexplained, suggesting:
- Omitted macroeconomic variables (interest rates, exchange rates, commodity prices)
- Structural breaks not captured by year FE
- Measurement error in international FDI data

5. **Omitted-variable risk**
FDI is likely influenced by:
- Macroeconomic policy (monetary, fiscal stance)
- Trade policy and tariff changes
- Natural resources and geographic endowments
- Quality of infrastructure
- Labor costs and human capital

These are only partially captured or absent in current specification.

6. **Transformation sensitivity**
The signed-log transformation improves stability but makes level-based interpretation less direct. Elasticity interpretation requires care.

7. **External validity**
The analysis uses countries with complete data overlap; findings may not generalize to all countries or time periods.

## Final Bottom Line

**Model Specification (Corrected):**
- Main FE model now removes crime_index (was specification error: time-invariant, absorbed by country FE)
- Primary lag = 1 (lag 12 from M2 unattainable with current data; only 13 years available)
- Controls: gepu (geopolitical uncertainty/risk)

**Statistical Finding:**
Lagged CPI coefficient = -0.1135 (p = 0.4238, not significant). Effect is not statistically distinguishable from zero.

**Substantive Concern:**
Results are extremely sensitive to 2020 inclusion/exclusion (coef -0.1135 → -0.0010; p 0.42 → 0.99). This instability suggests the model captures pandemic-era shocks rather than a stable corruption-FDI relationship. Without additional data from normal economic periods, causal interpretation is **not justified**.

**Model B Performance:**
Random Forest provides modest predictive improvement over OLS (RMSE: 14.64 vs 15.42, R²: 0.051 vs -0.053), but gains are marginal and lack interpretability.

**Recommendations:**
1. Accumulate longer historical panel (extend before 2012) to test M2's identified lag-12 window
2. Incorporate additional controls (macroeconomic policy, trade flows, natural resource endowments)
3. Investigate structural breaks around 2020 separately from long-run corruption-FDI relationship
4. Consider alternative estimation (random effects, hierarchical models) if country-level unmeasured heterogeneity dominates

**Reporting Standard:**
Present results as **exploratory and methodologically limited**, not as causal evidence. Emphasize data constraints and instability findings. Consider M3 as a foundation for future work rather than a definitive answer.
