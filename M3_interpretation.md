# M3 Interpretation Memo

## Project Context

This memo interprets our Milestone 3 econometric results for the capstone question: how do corruption perceptions and risk conditions relate to foreign direct investment (FDI) across countries?

Outcome variable:
- fdi_slog (signed log transform of foreign investment)

Key driver:
- cpi_score_lag1 (one-year lag of CPI score; higher score indicates lower perceived corruption)

Model A controls:
- crime_index
- gepu

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

### Heteroskedasticity (Breusch-Pagan)

- LM p-value: 0.0560
- F p-value: 0.0557

Interpretation:
At the 5% level, we do not reject homoskedasticity, but p-values are close to the cutoff. Using clustered SEs remains a conservative and appropriate choice.

### Multicollinearity (VIF)

- cpi_score_lag1: 7.18
- crime_index: 6.56
- gepu: 3.73

Interpretation:
No variable exceeds the common VIF concern threshold of 10. Collinearity is moderate but not severe.

### Residual Diagnostics

- Residuals vs fitted: results/figures/M3_residuals_vs_fitted.png
- Q-Q plot: results/figures/M3_qq_plot.png

Interpretation:
These plots support visual checks for nonlinearity, variance patterns, and normality departures, and should be referenced directly in the final report narrative.

## Robustness Checks (Required)

We implemented four robustness checks.

### 1. Clustered vs unclustered standard errors

For cpi_score_lag1:
- Clustered SE: 0.1416 (p = 0.4238)
- Unclustered SE: 0.2278 (p = 0.6189)

Conclusion:
Inference stays non-significant under both covariance assumptions.

### 2. Alternative lag structures

- Lag 1: coef = -0.1135, p = 0.4238
- Lag 2: coef = -0.1149, p = 0.4765
- Lag 3: coef = -0.2444, p = 0.1536

Conclusion:
Sign direction is stable across lags, but estimates remain statistically weak.

### 3. Excluding 2020

- Baseline: coef = -0.1135, p = 0.4238
- Excluding 2020: coef = -0.0010, p = 0.9950

Conclusion:
Results are sensitive to inclusion of the pandemic period, indicating potential crisis-year influence.

### 4. Subsample estimation by crime level

- Low-crime countries: coef = -0.0296, p = 0.9063
- High-crime countries: coef = -0.1367, p = 0.4365

Conclusion:
No subgroup estimate is statistically significant, though point estimates are more negative in high-crime countries.

## Caveats and Identification Limits

1. Absorbed regressor in FE
crime_index is largely time-invariant within countries in this panel and is absorbed by country fixed effects.

2. Omitted-variable risk
FDI is likely influenced by additional macro and institutional variables not included here.

3. Transformation sensitivity
The signed-log transformation improves stability but makes level-based interpretation less direct.

4. External validity
The analysis uses countries with complete data overlap; findings may not generalize to all countries.

## Final Bottom Line

Model A meets the milestone requirements and is correctly specified for panel FE analysis, but lagged CPI and GEPU effects are not statistically strong in this dataset.
Model B shows only a modest predictive improvement from Random Forest over OLS.

Our substantive conclusions should therefore be reported as cautious, with emphasis on methodological completeness, transparency, and clear limitations.
