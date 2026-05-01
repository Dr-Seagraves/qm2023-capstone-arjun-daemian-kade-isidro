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

