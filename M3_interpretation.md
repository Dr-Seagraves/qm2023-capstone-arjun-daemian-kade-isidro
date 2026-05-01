# M3 Interpretation Memo

## Project Context

This memo interprets our Milestone 3 econometric results for the capstone question: how do corruption perceptions and risk conditions relate to foreign direct investment (FDI) across countries?

Outcome variable:
- fdi_slog (signed log transform of foreign investment)

Key driver:
- cpi_score_lag3 (three-year lag of CPI score; higher score indicates lower perceived corruption)

Model A controls:
- crime_index
- gepu

## Model A Headline Result (Required Fixed Effects Model)

We estimated a two-way fixed effects model with country and year effects, using clustered standard errors.

Key estimate for cpi_score_lag3:
- Coefficient: -0.2444
- Clustered SE: 0.1705
- p-value: 0.1536

Interpretation:
A 1-point increase in the three-year lagged CPI score is associated with a 0.2444 decrease in signed-log FDI, holding country and year fixed effects constant.

Statistical conclusion:
The estimate is not statistically different from zero at conventional thresholds.

Additional result:
- gepu coefficient: -0.0145, clustered p-value = 0.2194

Model fit:
- Within R2: 0.0185
- Model F-test p-value: 0.2126

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

- OLS: RMSE = 15.2730, R2 = -0.0324
- Random Forest: RMSE = 15.3130, R2 = -0.0378

Interpretation:
Random Forest does not improve on OLS in this run; both models perform slightly worse than a mean benchmark on the test set.

Trade-off:
- OLS is easier to interpret economically.
- Random Forest is slightly better for prediction but less transparent for causal interpretation.

## Diagnostics (Required)

### Heteroskedasticity (Breusch-Pagan)

- LM p-value: 0.0412
- F p-value: 0.0407

Interpretation:
At the 5% level, we reject homoskedasticity, so clustered standard errors are justified and conservative.

### Multicollinearity (VIF)

- cpi_score_lag3: 7.22
- crime_index: 6.47
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

For cpi_score_lag3:
- Clustered SE: 0.1705 (p = 0.1536)
- Unclustered SE: 0.2734 (p = 0.3727)

Conclusion:
Inference stays non-significant under both covariance assumptions.

### 2. Alternative lag structures

- Lag 1: coef = -0.1135, p = 0.4238
- Lag 2: coef = -0.1149, p = 0.4765
- Lag 3: coef = -0.2444, p = 0.1536

Conclusion:
The short lags are negative, but the pattern is not monotonic. Overall, the lag structure is not robustly identified.

### 3. Excluding 2020

- Baseline: coef = -0.2444, p = 0.1536
- Excluding 2020: coef = -0.2229, p = 0.3151

Conclusion:
Dropping 2020 slightly attenuates the estimate and raises the standard error, but the sign remains negative. The effect is not driven entirely by the pandemic year in this current specification.

### 4. Subsample estimation by crime level

- Low-crime countries: coef = -0.2237, p = 0.5155
- High-crime countries: coef = -0.1991, p = 0.2524

Conclusion:
No subgroup estimate is statistically significant, and the two point estimates are similar in magnitude.

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

Model A meets the milestone requirements and is correctly specified for panel FE analysis, but the lagged CPI and GEPU effects are not statistically strong in this dataset.
Model B does not show a predictive improvement from Random Forest over OLS in the current run.

Our substantive conclusions should therefore be reported as cautious, with emphasis on methodological completeness, transparency, and clear limitations.
