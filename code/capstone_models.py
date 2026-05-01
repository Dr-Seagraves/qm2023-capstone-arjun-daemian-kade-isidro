"""
QM 2023 Capstone: Milestone 3 Econometric Models (CORRECTED)
Team: Arjun, Daemian, Kade, Isidro
Members: Arjun, Daemian, Kade, Isidro
Date: 2026-04-20 (Updated 2026-04-29)

This script estimates panel regression models to identify causal effects of
corruption perception and risk factors on foreign investment.

METHODOLOGY CORRECTIONS (vs. original):
1. Removed crime_index from FE model: time-invariant within countries, absorbed by
   country FE, causing high multicollinearity (VIF=6.56). Kept gepu as external risk.
2. Added 12-year lag specification: M2 EDA identified optimal lag=12; now primary model.
3. Alternative lags (1,2,3,12): robustness tests lag structure vs best EDA finding.
4. Explicit 2020 sensitivity analysis: baseline shows huge parameter shift when 2020
   excluded, indicating model may be driven by pandemic shock rather than stable effects.
5. Clarified outcome transform: signed log handles negative FDI values while reducing
   heteroskedasticity from skewed positively-valued cases.

Model A (required): Two-way fixed effects panel regression (PRIMARY: 12-year lag).
Model B (chosen): Machine learning comparison (Random Forest vs. OLS).

Outputs:
- Regression tables in results/tables/
- Diagnostic plots in results/figures/
"""

from __future__ import annotations

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from fetch_crime_index_code.config_paths import FINAL_DATA_DIR, FIGURES_DIR, TABLES_DIR

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


# -----------------------------------------------------------------------------
# Section 1: Imports and data loading
# -----------------------------------------------------------------------------

def signed_log1p(series: pd.Series) -> pd.Series:
    """Apply a signed log transform so negative FDI values remain valid."""
    return np.sign(series) * np.log1p(np.abs(series))


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_vif_table(X: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, col in enumerate(X.columns):
        vif = variance_inflation_factor(X.values, i)
        rows.append({"Variable": col, "VIF": float(vif)})
    return pd.DataFrame(rows)


def fit_fe_model(df: pd.DataFrame, driver_col: str, include_crime: bool = False):
    """
    Fit two-way FE panel model with clustered and unclustered SE.
    
    CORRECTED: Excludes crime_index by default since it is:
    - Time-invariant within countries
    - Absorbed by country fixed effects
    - Causes high VIF (6.56) and multicollinearity
    
    Only returns crime in diagnostics if include_crime=True (for VIF check only).
    """
    if include_crime:
        model_df = df[[
            "Country",
            "Year",
            "fdi_slog",
            driver_col,
            "crime_index",
            "gepu",
        ]].dropna().copy()
    else:
        model_df = df[[
            "Country",
            "Year",
            "fdi_slog",
            driver_col,
            "gepu",
        ]].dropna().copy()

    panel = model_df.set_index(["Country", "Year"]).sort_index()
    y = panel["fdi_slog"]
    
    if include_crime:
        X = panel[[driver_col, "crime_index", "gepu"]]
    else:
        X = panel[[driver_col, "gepu"]]

    fe_clustered = PanelOLS(
        y,
        X,
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
    ).fit(cov_type="clustered", cluster_entity=True)

    fe_unclustered = PanelOLS(
        y,
        X,
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
    ).fit(cov_type="unadjusted")

    return panel, y, X, fe_clustered, fe_unclustered


# -----------------------------------------------------------------------------
# Section 2: Feature engineering (lags, transforms)
# -----------------------------------------------------------------------------

print("=" * 80)
print("Milestone 3 Econometric Models")
print("=" * 80)

panel_path = FINAL_DATA_DIR / "analysis_panel.csv"
if not panel_path.exists():
    raise FileNotFoundError(f"Missing final panel file: {panel_path}")

raw = pd.read_csv(panel_path)
raw["Year"] = raw["Year"].astype(int)
raw = raw.sort_values(["Country", "Year"]).reset_index(drop=True)

# Keep only rows with core variables available for modeling.
df = raw.dropna(subset=["foreign_investment", "cpi_score", "crime_index", "gepu"]).copy()

# Signed log transform handles potentially negative FDI while reducing skew.
# Motivation: Signed log preserves sign of negative FDI while compressing range,
# reducing heteroskedasticity from large positive values.
df["fdi_slog"] = signed_log1p(df["foreign_investment"])

# Create lagged CPI scores. M2 EDA identified lag=12 as optimal, but we test alternatives.
for lag in [1, 2, 3, 4, 5, 6, 12]:
    df[f"cpi_score_lag{lag}"] = df.groupby("Country")["cpi_score"].shift(lag)

# Group indicator for subgroup robustness check.
median_crime = df["crime_index"].median()
df["high_crime_group"] = (df["crime_index"] >= median_crime).astype(int)

print(f"Loaded rows after cleaning: {len(df)}")
print(f"Countries: {df['Country'].nunique()}, Years: {df['Year'].min()}-{df['Year'].max()}")


# -----------------------------------------------------------------------------
# Section 3: Model A - Fixed Effects regression (required)
# CORRECTED: Uses lag 12 from M2 EDA, then prefers lag 4 before shorter lags.
# Removed crime_index (absorbed by country FE, time-invariant, high VIF).
# -----------------------------------------------------------------------------

primary_lag_col = None
for test_lag in [12, 4, 3, 2, 1]:
    test_col = f"cpi_score_lag{test_lag}"
    test_model_df = df[[
        "Country",
        "Year",
        "fdi_slog",
        test_col,
        "gepu",
    ]].dropna()
    if len(test_model_df) > 30:  # Minimum sample size for FE
        primary_lag_col = test_col
        print(f"\nUsing primary lag specification: cpi_score_lag{test_lag} (n={len(test_model_df)})")
        break

if primary_lag_col is None:
    raise ValueError("Cannot fit model: insufficient observations for any valid lag.")

panel, y, X, fe_clustered, fe_unclustered = fit_fe_model(df, primary_lag_col, include_crime=False)

print("\nModel A (FE, clustered SE) fitted.")
print(f"Specification: {primary_lag_col} + gepu (crime_index EXCLUDED: time-invariant, absorbed by FE)")
print(fe_clustered.summary)

save_text(TABLES_DIR / "M3_modelA_fe_clustered_summary.txt", str(fe_clustered.summary))
save_text(TABLES_DIR / "M3_modelA_fe_unclustered_summary.txt", str(fe_unclustered.summary))

coef_table = pd.DataFrame(
    {
        "variable": fe_clustered.params.index,
        "coef_clustered": fe_clustered.params.values,
        "se_clustered": fe_clustered.std_errors.values,
        "pvalue_clustered": fe_clustered.pvalues.values,
        "coef_unclustered": fe_unclustered.params.reindex(fe_clustered.params.index).values,
        "se_unclustered": fe_unclustered.std_errors.reindex(fe_clustered.params.index).values,
        "pvalue_unclustered": fe_unclustered.pvalues.reindex(fe_clustered.params.index).values,
    }
)
coef_table.to_csv(TABLES_DIR / "M3_modelA_coefficient_table.csv", index=False)

fit_stats = pd.DataFrame(
    [
        {
            "model": "FE_clustered",
            "nobs": int(fe_clustered.nobs),
            "r2_within": float(fe_clustered.rsquared_within),
            "r2_between": float(fe_clustered.rsquared_between),
            "r2_overall": float(fe_clustered.rsquared_overall),
            "f_stat": float(fe_clustered.f_statistic.stat) if fe_clustered.f_statistic is not None else np.nan,
            "f_pvalue": float(fe_clustered.f_statistic.pval) if fe_clustered.f_statistic is not None else np.nan,
        },
        {
            "model": "FE_unclustered",
            "nobs": int(fe_unclustered.nobs),
            "r2_within": float(fe_unclustered.rsquared_within),
            "r2_between": float(fe_unclustered.rsquared_between),
            "r2_overall": float(fe_unclustered.rsquared_overall),
            "f_stat": float(fe_unclustered.f_statistic.stat) if fe_unclustered.f_statistic is not None else np.nan,
            "f_pvalue": float(fe_unclustered.f_statistic.pval) if fe_unclustered.f_statistic is not None else np.nan,
        },
    ]
)
fit_stats.to_csv(TABLES_DIR / "M3_modelA_fit_statistics.csv", index=False)


# -----------------------------------------------------------------------------
# Section 4: Model B - ML comparison (Random Forest vs. OLS)
# -----------------------------------------------------------------------------

ml_df = df[[
    "Year",
    "fdi_slog",
    "cpi_score_lag1",
    "crime_index",
    "gepu",
]].dropna().copy()

# Time-aware split: hold out the most recent two years.
max_year = int(ml_df["Year"].max())
cutoff = max_year - 1
train = ml_df[ml_df["Year"] < cutoff].copy()
test = ml_df[ml_df["Year"] >= cutoff].copy()

feature_cols = ["cpi_score_lag1", "crime_index", "gepu"]
X_train = train[feature_cols]
X_test = test[feature_cols]
y_train = train["fdi_slog"]
y_test = test["fdi_slog"]

ols_model = sm.OLS(y_train, sm.add_constant(X_train)).fit()
ols_pred = ols_model.predict(sm.add_constant(X_test))

rf_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    max_depth=8,
    min_samples_leaf=2,
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

ml_results = pd.DataFrame(
    [
        {
            "model": "OLS",
            "test_rmse": float(np.sqrt(mean_squared_error(y_test, ols_pred))),
            "test_r2": float(r2_score(y_test, ols_pred)),
            "train_n": int(len(train)),
            "test_n": int(len(test)),
        },
        {
            "model": "RandomForest",
            "test_rmse": float(np.sqrt(mean_squared_error(y_test, rf_pred))),
            "test_r2": float(r2_score(y_test, rf_pred)),
            "train_n": int(len(train)),
            "test_n": int(len(test)),
        },
    ]
)
ml_results.to_csv(TABLES_DIR / "M3_modelB_ml_comparison.csv", index=False)

rf_importance = pd.DataFrame(
    {
        "feature": feature_cols,
        "importance": rf_model.feature_importances_,
    }
).sort_values("importance", ascending=False)
rf_importance.to_csv(TABLES_DIR / "M3_modelB_rf_feature_importance.csv", index=False)

plt.figure(figsize=(8, 5))
plt.bar(rf_importance["feature"], rf_importance["importance"])
plt.title("Model B: Random Forest Feature Importance")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_modelB_rf_feature_importance.png", dpi=300)
plt.close()


# -----------------------------------------------------------------------------
# Section 5: Diagnostics (heteroskedasticity, VIF, residual plots)
# -----------------------------------------------------------------------------

# Breusch-Pagan on pooled OLS proxy for FE diagnostics.
proxy_ols = sm.OLS(y, sm.add_constant(X)).fit()
bp_lm, bp_lm_p, bp_f, bp_f_p = het_breuschpagan(proxy_ols.resid, sm.add_constant(X))

bp_table = pd.DataFrame(
    [
        {
            "bp_lm_stat": float(bp_lm),
            "bp_lm_pvalue": float(bp_lm_p),
            "bp_f_stat": float(bp_f),
            "bp_f_pvalue": float(bp_f_p),
            "heteroskedasticity_detected_at_5pct": bool(bp_lm_p < 0.05),
        }
    ]
)
bp_table.to_csv(TABLES_DIR / "M3_diagnostic_breusch_pagan.csv", index=False)

vif_table = build_vif_table(X)
vif_table.to_csv(TABLES_DIR / "M3_diagnostic_vif.csv", index=False)

fitted = np.asarray(fe_clustered.fitted_values).reshape(-1)
resid = np.asarray(fe_clustered.resids).reshape(-1)

plt.figure(figsize=(10, 6))
plt.scatter(fitted, resid, alpha=0.35)
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("M3: Residuals vs Fitted (FE Clustered)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_residuals_vs_fitted.png", dpi=300)
plt.close()

plt.figure(figsize=(8, 6))
stats.probplot(resid, dist="norm", plot=plt)
plt.title("M3: Q-Q Plot (FE Residuals)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "M3_qq_plot.png", dpi=300)
plt.close()


# -----------------------------------------------------------------------------
# Section 6: Robustness checks (>=3 required)
# -----------------------------------------------------------------------------

# Check 1: Clustered vs. unclustered SE already saved in coefficient table.

# Check 2: Alternative lag structures for the key driver (including M2's optimal lag 12).
# CORRECTED: Now tests lag 12 from M2 EDA, excludes crime_index from FE
lag_rows = []
for lag in [1, 2, 3, 4, 5, 6, 12]:
    col = f"cpi_score_lag{lag}"
    try:
        _, _, _, fe_lag_clustered, _ = fit_fe_model(df, col, include_crime=False)
        lag_rows.append(
            {
                "lag": lag,
                "coef": float(fe_lag_clustered.params[col]),
                "se": float(fe_lag_clustered.std_errors[col]),
                "pvalue": float(fe_lag_clustered.pvalues[col]),
                "r2_within": float(fe_lag_clustered.rsquared_within),
                "nobs": int(fe_lag_clustered.nobs),
            }
        )
    except Exception as e:
        lag_rows.append(
            {
                "lag": lag,
                "coef": np.nan,
                "se": np.nan,
                "pvalue": np.nan,
                "r2_within": np.nan,
                "nobs": 0,
            }
        )

pd.DataFrame(lag_rows).to_csv(TABLES_DIR / "M3_robustness_alt_lags.csv", index=False)

# Check 3: Exclude 2020 and re-estimate FE model (tests pandemic/crisis sensitivity).
# CAUTION: Large parameter shifts when 2020 excluded may indicate pandemic-driven results.
no_2020_df = df[df["Year"] != 2020].copy()
_, _, _, fe_no_2020, _ = fit_fe_model(no_2020_df, primary_lag_col, include_crime=False)

exclude_2020 = pd.DataFrame(
    [
        {
            "spec": "baseline",
            "lag": primary_lag_col.replace("cpi_score_lag", ""),
            "coef": float(fe_clustered.params[primary_lag_col]),
            "se": float(fe_clustered.std_errors[primary_lag_col]),
            "pvalue": float(fe_clustered.pvalues[primary_lag_col]),
            "nobs": int(fe_clustered.nobs),
        },
        {
            "spec": "exclude_2020",
            "lag": primary_lag_col.replace("cpi_score_lag", ""),
            "coef": float(fe_no_2020.params[primary_lag_col]),
            "se": float(fe_no_2020.std_errors[primary_lag_col]),
            "pvalue": float(fe_no_2020.pvalues[primary_lag_col]),
            "nobs": int(fe_no_2020.nobs),
        },
    ]
)
exclude_2020.to_csv(TABLES_DIR / "M3_robustness_exclude_2020.csv", index=False)

# Check 4: Subsample check by high/low crime groups.
# CORRECTED: Uses primary_lag_col, excludes crime_index from FE models
subsample_rows = []
for group_value, group_name in [(0, "low_crime"), (1, "high_crime")]:
    group_df = df[df["high_crime_group"] == group_value].copy()
    try:
        _, _, _, fe_group, _ = fit_fe_model(group_df, primary_lag_col, include_crime=False)
        lag_num = primary_lag_col.replace("cpi_score_lag", "")
        subsample_rows.append(
            {
                "group": group_name,
                "lag": lag_num,
                "coef": float(fe_group.params[primary_lag_col]),
                "se": float(fe_group.std_errors[primary_lag_col]),
                "pvalue": float(fe_group.pvalues[primary_lag_col]),
                "nobs": int(fe_group.nobs),
            }
        )
    except Exception:
        lag_num = primary_lag_col.replace("cpi_score_lag", "")
        subsample_rows.append(
            {
                "group": group_name,
                "lag": lag_num,
                "coef": np.nan,
                "se": np.nan,
                "pvalue": np.nan,
                "nobs": 0,
            }
        )

pd.DataFrame(subsample_rows).to_csv(TABLES_DIR / "M3_robustness_subsamples.csv", index=False)


# -----------------------------------------------------------------------------
# Section 7: Save consolidated regression table and completion summary
# -----------------------------------------------------------------------------

consolidated = pd.merge(
    coef_table[["variable", "coef_clustered", "se_clustered", "pvalue_clustered"]],
    coef_table[["variable", "coef_unclustered", "se_unclustered", "pvalue_unclustered"]],
    on="variable",
    how="outer",
)
consolidated.to_csv(TABLES_DIR / "M3_regression_table.csv", index=False)

summary_lines = [
    "=" * 80,
    "Milestone 3 Model Run: CORRECTED VERSION",
    "=" * 80,
    f"Input panel: {panel_path}",
    f"Primary lag specification: {primary_lag_col}",
    f"Model A observations: {int(fe_clustered.nobs)}",
    f"Model B train/test: {len(train)}/{len(test)}",
    "",
    "KEY METHODOLOGICAL CORRECTIONS:",
    "1. Crime_index EXCLUDED from FE models: time-invariant, absorbed by country FE",
    "2. Primary specification prefers lag 12, then lag 4, then 3,2,1",
    "3. Robustness tests include lag 12 and feasible alternatives (1, 2, 3, 4, 5, 6, 12)",
    "4. 2020 sensitivity analysis: tests pandemic-era influence on results",
    "5. Outcome transformation: signed_log reduces heterosk. while preserving sign",
    "",
    f"Tables saved to: {TABLES_DIR}",
    f"Figures saved to: {FIGURES_DIR}",
    "=" * 80,
]
save_text(TABLES_DIR / "M3_run_summary.txt", "\n".join(summary_lines))

print("\n".join(summary_lines))
print("=" * 80)
print("Done.")
