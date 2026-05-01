# AI Audit Appendix: Milestone 1

**Team:** [Your Team Name]

**Date:** [Submission date]

## AI Tools Used

- [x] ChatGPT
- [x] GitHub Copilot
- [ ] Claude
- [ ] Other: [Specify]

## Detailed Log

### 1. pandas-datareader FRED API Integration

**Prompt (ChatGPT):**

> "How do I use pandas-datareader to fetch the Federal Funds Rate (FEDFUNDS) from FRED for the date range 2015-01-01 to 2023-12-31?"

**AI Output:**

```python
import pandas_datareader as pdr
from datetime import datetime

start = datetime(2015, 1, 1)
end = datetime(2023, 12, 31)
fedfunds = pdr.DataReader("FEDFUNDS", "fred", start, end)
```

### 2. Creating Visualizations from Cleaned Data Pipeline

**Prompt:**

Create visualizations in guideline with the requirements of Milestone 2. Add the captions written in the text file to each of our graphics.

**Output:**

All code written in `m2_eda_plots.py`. Added captions embedded to the bottom of each visualization.

---

# AI Audit Appendix: Milestone 3

**Team:** Arjun, Daemian, Kade, Isidro

**Date:** 2026-04-20

## AI Tools Used

- [x] ChatGPT
- [x] GitHub Copilot
- [ ] Claude
- [ ] Other: [Specify]

## Detailed Log (Milestone 3)

### 1. Econometric script structure and implementation

**Prompt (GitHub Copilot):**

> "Complete the code according to this readme. Build Milestone 3 with Model A fixed effects, one Model B option, diagnostics, robustness checks, and saved outputs."

**AI Output Summary:**

- Generated `code/capstone_models.py` with required section headers.
- Implemented Model A two-way fixed effects using `linearmodels.PanelOLS`.
- Implemented Model B as ML comparison (`RandomForestRegressor` vs OLS).
- Saved regression outputs and diagnostics into `results/tables/` and `results/figures/`.

**Human Verification / Edits:**

- Verified script runs top-to-bottom with no runtime errors.
- Confirmed output files exist and match milestone deliverable requirements.

### 2. Handling absorbed regressors under fixed effects

**Prompt (GitHub Copilot):**

> "The fixed effects model fails because one variable is absorbed. Fix the code so it runs correctly."

**AI Output Summary:**

- Added `drop_absorbed=True` to PanelOLS specifications.
- Model now automatically drops fully absorbed regressors (e.g., near time-invariant country-level predictors under entity FE).

**Human Verification / Edits:**

- Reviewed warning output and confirmed this behavior is econometrically expected.
- Retained transparent reporting of dropped-variable behavior in interpretation memo.

### 3. Diagnostic interpretation guidance

**Prompt (ChatGPT/GitHub Copilot):**

> "Interpret Breusch-Pagan, VIF, and residual diagnostics for Milestone 3 memo language."

**AI Output Summary:**

- Proposed interpretation framing for p-values near 0.05 in heteroskedasticity testing.
- Suggested VIF threshold language and cautionary interpretation.
- Suggested memo language linking plots to model assumptions.

**Human Verification / Edits:**

- Cross-checked all interpretations against saved CSV outputs.
- Avoided overclaiming significance.
- Marked uncertain conclusions as tentative/cautious.

### 4. Robustness check design

**Prompt (GitHub Copilot):**

> "Add at least three robustness checks that fit this dataset."

**AI Output Summary:**

- Implemented clustered vs unclustered SE comparison.
- Implemented alternative lag robustness (lag 1, 2, 3).
- Implemented outlier-period exclusion (drop year 2020).
- Implemented subgroup estimation (high-crime vs low-crime subsamples).

**Human Verification / Edits:**

- Confirmed all robustness result files are generated and populated.
- Checked that robustness conclusions are consistent with output magnitudes and p-values.

### 5. Dependency suggestions and environment setup

**Prompt (GitHub Copilot):**

> "Resolve missing package errors and make requirements reproducible."

**AI Output Summary:**

- Identified and installed missing packages (`linearmodels`, `scikit-learn`, `pypdf`).
- Updated `requirements.txt` to include econometrics and PDF dependencies.

**Human Verification / Edits:**

- Re-ran the full script after package updates.
- Confirmed successful completion and artifact generation.

## Academic Integrity Statement (Milestone 3)

AI tools were used for coding assistance, debugging, and drafting interpretation language. Final model choices, result interpretation, and all submission decisions were reviewed and approved by team members.
No AI output was accepted without human verification against actual model output files.

# AI Audit Appendix: Milestone 4

**Team:** Arjun-Daemian-Kade-Isidro

**Date:** 5/1/2026

## AI Tools Used

- [ ] ChatGPT
- [x] GitHub Copilot
- [ ] Claude
- [ ] Other: [Specify]

## Detailed Log

### 1. Create

**Prompt:**

I want you to look at the finished dataset and create yout own FE model while excluding 2020 from it. Save the code and run it in capstone_check

**AI Output:**

"""Quick check: Fit two-way FE excluding 2020 and save summaries.

This script is a lightweight runner used to validate the FE estimate
when observations from 2020 are removed. Outputs are written to the
same `TABLES_DIR` used by the main pipeline.
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from fetch_crime_index_code.config_paths import FINAL_DATA_DIR, TABLES_DIR

warnings.filterwarnings("ignore")


def signed_log1p(series: pd.Series) -> pd.Series:
	return np.sign(series) * np.log1p(np.abs(series))


def save_text(path: Path, text: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(text, encoding="utf-8")


def fit_fe_on_df(df: pd.DataFrame, driver_col: str):
	model_df = df[["Country", "Year", "fdi_slog", driver_col, "crime_index", "gepu"]].dropna().copy()
	panel = model_df.set_index(["Country", "Year"]).sort_index()
	y = panel["fdi_slog"]
	X = panel[[driver_col, "crime_index", "gepu"]]

	fe = PanelOLS(y, X, entity_effects=True, time_effects=True, drop_absorbed=True).fit(cov_type="clustered", cluster_entity=True)
	return fe


def main():
	panel_path = FINAL_DATA_DIR / "analysis_panel.csv"
	if not panel_path.exists():
		raise FileNotFoundError(f"Missing final panel file: {panel_path}")

	raw = pd.read_csv(panel_path)
	raw["Year"] = raw["Year"].astype(int)

	df = raw.dropna(subset=["foreign_investment", "cpi_score", "crime_index", "gepu"]).copy()
	df["fdi_slog"] = signed_log1p(df["foreign_investment"])

	# primary lag used in main script
	primary_lag_col = "cpi_score_lag3"
	for lag in [1, 2, 3, 4, 5]:
		df[f"cpi_score_lag{lag}"] = df.groupby("Country")["cpi_score"].shift(lag)

	# Exclude 2020
	df_no_2020 = df[df["Year"] != 2020].copy()

	# Existing lightweight FE run (already prints summary)
	fe_no_2020 = fit_fe_on_df(df_no_2020, primary_lag_col)
	print("\n--- capstone_check: FE (exclude 2020) ---\n")
	print(str(fe_no_2020.summary))

### 2. Creating Visualizations from Cleaned Data Pipeline

**Prompt:**

run the code solely tied to excluding 2020 in the capstone_models file, then print it in the terminal. I want this to be an addition to capstone_check.
**Output:**

# --- Add: run the exact exclude-2020 snippet as in `capstone_models.py` ---
	def fit_fe_model(df_in: pd.DataFrame, driver_col_in: str):
		model_df2 = df_in[["Country", "Year", "fdi_slog", driver_col_in, "crime_index", "gepu"]].dropna().copy()
		panel2 = model_df2.set_index(["Country", "Year"]).sort_index()
		y2 = panel2["fdi_slog"]
		X2 = panel2[[driver_col_in, "crime_index", "gepu"]]

		fe_clustered2 = PanelOLS(
			y2,
			X2,
			entity_effects=True,
			time_effects=True,
			drop_absorbed=True,
		).fit(cov_type="clustered", cluster_entity=True)

		fe_unclustered2 = PanelOLS(
			y2,
			X2,
			entity_effects=True,
			time_effects=True,
			drop_absorbed=True,
		).fit(cov_type="unadjusted")

		return panel2, y2, X2, fe_clustered2, fe_unclustered2

	# Run the capstone_models-style check and print its clustered result
	panel2, y2, X2, fe_clustered2, fe_unclustered2 = fit_fe_model(df_no_2020, primary_lag_col)
	print("\n--- capstone_models-style FE (exclude 2020) ---\n")
	print(str(fe_clustered2.summary))


if __name__ == "__main__":
	main()

**Human Verification / Edits:**

- Compared script outputs to model-produced files in an effort to combat incorrect data within our finalized interpretations
- Confirmed successful data verification and produced M4 memo and capstone presentation using proper data


## Academic Integrity Statement (Milestone 4)

AI tools were used for coding assistance, debugging, and drafting interpretation language. Result interpretation and submission decisions were reviewed and approved by team members.
No AI output was accepted without human verification against actual model files.
