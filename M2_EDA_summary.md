# M2 Summary
## Key Findings
- We have revealed a weak negative correlation (r = 0.14) between foreign_investment and cpi_score. This makes sense as foreign investment drops as it becomes more apparent that a government is more corrupt. However, it seems like crime is not an important factor
- The optimal lag for our data is 12 years, as that provides a  larger basis for economic activity and builds trust between nations and companies.
- The most sensitive groups are Singapore, Sweden, and Ireland, as their alterations within the CPI will greatly impact their perception in comparison to the other nations we analyzed.
- Within our analysis for individual groups, it seems like China is an outlier, with a much higher result within the averages when compared with all other nations.
- Our trend is consistent with our initial graph, with seasonal intervals having an obvious pattern.

## Hypotheses
1. Based off of the time series, it is reasonable to assume that there is a correlation between the Corruption Perceptions Index and foreign investment within a country.
2. As a country has a lower CPI, it is expected to be much more difficult to obtain a control premium, whereas in countries with a higher CPI, it is expected to be easier to obtain a control premium.
3. The group heterogeneity can be defended, as our groups are defined by different countries, with different economic situations between them.

## Data Quality Flags
- China seems to be an outlier within the group. Analyzing its values might help us either discover why, or push us to mitigate the outlier's effect. China is also a possible vector for heteroskedasticity, and looking into it might help us resolve the heteroskedasticity.
- Many nations have a form of data for 2025 except for one column. Imputation or omission of the year 2025 would resolve this issue.
