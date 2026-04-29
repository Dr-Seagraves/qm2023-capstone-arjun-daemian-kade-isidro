# Milestone 4 Policy Memo

## Project Context

This memo translates our empirical analysis of countries' perceived corruption, crime, geopolitical uncertainty, and foreign direct investment into policy guidance for a government agency or central bank.

Our final panel includes 20 countries and 12 years of annual data, for 237 country-year observations. The main outcome is signed-log foreign direct investment (`fdi_slog`), and the key driver is lagged CPI score (`cpi_score_lag1`), where a higher CPI score means lower perceived corruption.

### Main empirical takeaways

- Two-way fixed effects estimate for `cpi_score_lag1`: coefficient = -0.1135, clustered p-value = 0.4238.
- GEPU is negative but not statistically strong: coefficient = -0.0159, p-value = 0.1876.
- Model fit is weak: within R2 = 0.0149.
- Random Forest offers only a modest predictive gain over OLS: test RMSE 14.64 vs. 15.42, and test R2 0.05 vs. -0.05.
- Robustness checks do not produce a stable, statistically significant CPI effect across alternative lags, exclusion of 2020, or crime-based subsamples.

Interpretation: the data do not support a strong claim that CPI alone explains foreign investment changes in this sample. The safest conclusion is that investment outcomes are shaped by a broader mix of institutional quality, uncertainty, and macro conditions.

## 3.1 Policy Recommendations

### Policy Implication 1: Prioritize broad investment-climate reforms, not CPI alone

Finding: The lagged CPI effect is small, negative, and not statistically significant.

Recommendation: Treat anti-corruption reform as part of a wider investment-climate strategy that also improves contract enforcement, customs efficiency, transparency in procurement, and regulatory consistency.

Rationale: Investors respond to the full risk environment, not just one governance indicator. Even when the CPI effect is weak in our sample, better institutions can still reduce transaction costs, lower uncertainty premia, and improve long-run credibility.

### Policy Implication 2: Target uncertainty-sensitive and high-risk environments with stabilization tools

Finding: GEPU is negative, and the high-crime subsample shows a more negative point estimate than the low-crime subsample, although neither is statistically significant.

Recommendation: In markets with elevated security or geopolitical risk, pair investment promotion with targeted stabilization policies such as political-risk insurance, faster permitting, visible enforcement of business rules, and localized security coordination.

Rationale: The mechanism is not just corruption per se; it is the broader investment risk environment. Equity concerns also matter because high-risk areas may already face weaker capital access, so a targeted intervention helps avoid widening regional gaps.

## 3.2 Scenario Analysis

We model three scenarios for the next 12 months based on governance and uncertainty conditions. Because the estimated effects are weak, the table below should be read as a directional planning exercise rather than a point forecast.

| Scenario | Driver change | Predicted FDI impact | Probability |
|---|---|---:|---:|
| Baseline | CPI and GEPU remain near current levels | Roughly flat | 50% |
| Improvement | CPI rises modestly and GEPU declines | Mild increase in FDI inflows | 30% |
| Stress | CPI weakens and GEPU rises | Mild decline or delay in FDI | 20% |

Expected value: On a normalized impact scale, the weighted average is slightly positive because the improvement scenario is more likely than the stress scenario, but the overall effect remains close to neutral.

Recommendation: Because the downside from uncertainty shocks can materialize quickly while the upside from institutional reform is gradual, a cautious pro-investment stance is warranted. Policy should focus on reducing volatility and signaling predictability rather than promising a large near-term FDI jump.

## 3.3 Risk Assessment

### Model Risks

1. Stable relationship assumption: The FE model assumes the relationship between CPI and FDI is stable over time within countries. If the corruption-FDI linkage changes because of trade shocks, sanctions, or major policy reforms, the estimated coefficient may not generalize.
2. Omitted variable bias: FDI is also influenced by GDP growth, exchange rates, trade openness, labor costs, capital controls, tax policy, and sovereign risk. If these correlate with CPI or GEPU, our estimates may be confounded.
3. External validity: The panel only includes the 20 countries with complete overlapping data. Results may not apply to countries outside this sample or to periods with different global capital-market conditions.

### Domain-Specific Risks

1. Endogeneity and reverse causality: FDI can affect governance quality, not just the other way around. More investment can increase reform pressure or improve institutions, which complicates causal interpretation.
2. Measurement limitations: CPI is perception-based, crime data are country-level survey measures, and GEPU is a broad uncertainty index. These variables may not fully capture the mechanisms that matter for investors.
3. Crisis sensitivity: The 2020 exclusion check shows the estimates are sensitive to crisis-year inclusion, suggesting that global shocks can distort the relationship in short panels.

## 3.4 Caveats and Limitations

1. Fixed effects assumption: Country fixed effects absorb time-invariant differences across countries, but they cannot fully eliminate bias from time-varying omitted factors.
2. Parallel-trends style caution: Although this is not a DiD design, our interpretation still relies on the idea that changes in CPI and FDI are comparable over time. Pre-existing trends or structural breaks may weaken the interpretation.
3. Lag specification: We tested lags of 1, 2, and 3 years. The sign remains negative, but the estimates are not stable enough to support a strong lag choice claim.
4. Measurement error: CPI, crime, and FDI data all include noise from reporting differences, country coverage, and transformation choices. Alternative constructions could change the exact coefficient values.
5. Predictive limits: The Random Forest model slightly outperforms OLS, but the gain is small. The dataset is better suited to cautious interpretation than to high-confidence forecasting.

## 3.5 Future Research Directions

To refine this analysis, future work could:

1. Add macro controls such as GDP growth, inflation, exchange rates, trade openness, and sovereign debt indicators to better isolate the governance channel.
2. Test heterogeneous effects by income group, region, sectoral FDI, or institutional baseline to see whether corruption matters more in some settings than others.
3. Extend the sample with more years or more countries to improve power and check whether the weak CPI result persists in longer panels.
4. Model nonlinearities and threshold effects, since governance risk may matter most once uncertainty or crime crosses a certain level.
5. Use alternative identification strategies, such as instrumental variables or event studies around major reform episodes, to address endogeneity.

## 4. References

1. Transparency International. (2025). Corruption Perceptions Index. Retrieved from https://www.transparency.org/en/
2. World Bank. (2024). Foreign direct investment, net inflows (BoP, current US$). Retrieved from https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD
3. Numbeo. (2025). Crime Index by country. Retrieved from https://www.numbeo.com/crime/
4. Caldara, D., & Iacoviello, M. (2022). Measuring geopolitical risk. American Economic Review, 112(4), 1194-1225. Retrieved from https://www.policyuncertainty.com/gpr.html

## Appendix: AI Audit Summary

### AI Tools Used

- GitHub Copilot
- ChatGPT

Model versions were not always exposed in the original workflow logs. For this project writeup, GitHub Copilot is the primary AI tool used for coding and drafting support.

### Key Verification Examples

#### M1 Example

Prompt: "Help summarize the data cleaning steps for the merged country-year panel and explain why the merge order matters."

Output: A draft summary of the four-source merge, the common-country filter, and the annual alignment strategy.

Verification: We checked the cleaned panel, the country-year coverage, and the saved output file in data/final/analysis_panel.csv.

Critique: The first draft was too generic about the merge strategy, so we replaced it with exact data-source wording and the actual country-year structure.

#### M2 Example

Prompt: "Turn our EDA results into a concise narrative about the relationship between corruption, crime, and foreign investment."

Output: A draft summary highlighting the weak negative CPI relationship, the lagged pattern, and the country heterogeneity.

Verification: We compared the summary against the plots in results/figures and the cleaned panel statistics.

Critique: The AI over-stated the strength of the crime relationship, so we softened that language and emphasized uncertainty.

#### M3 Example

Prompt: "Interpret the fixed effects results for lagged CPI score and GEPU in plain language for the memo."

Output: A draft explanation that a one-point increase in lagged CPI is associated with a -0.1135 change in signed-log FDI, with non-significant p-values.

Verification: We matched the interpretation to the saved regression table and the PanelOLS summary output.

Critique: The AI initially framed the result too causally, so we changed it to cautious associational language and noted the low within R2.

#### M4 Example

Prompt: "Write policy recommendations and scenario analysis for a memo on corruption, crime, geopolitical uncertainty, and FDI."

Output: A draft policy memo structure with recommendation, scenario, risk, limitations, and future research sections.

Verification: We checked the language against the actual model outputs, robustness checks, and data coverage before finalizing the memo.

Critique: The AI wanted to assign stronger confidence than the evidence justified, so we explicitly framed the policy advice as cautious and evidence-limited.

### Responsibility Statement

All code and analysis in this memo has been verified by our team. We used AI as a productivity tool, not as a substitute for understanding. We take full responsibility for the final wording, interpretations, and any remaining errors.