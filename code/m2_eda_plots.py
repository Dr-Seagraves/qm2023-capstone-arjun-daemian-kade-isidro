import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "final" / "analysis_panel.csv"
FIGURES_DIR = BASE_DIR / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


OUTCOME = "foreign_investment"
DRIVER = "cpi_score"
CONTROLS = ["crime_index", "gepu"]
TIME_COL = "Year"
ENTITY_COL = "Country"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df[TIME_COL] = pd.to_numeric(df[TIME_COL], errors="coerce")

    numeric_cols = [OUTCOME, DRIVER, *CONTROLS]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[TIME_COL, ENTITY_COL, OUTCOME, DRIVER])
    df = df.sort_values([ENTITY_COL, TIME_COL]).reset_index(drop=True)
    return df


def save_figure(fig: plt.Figure, filename: str) -> None:
    outpath = FIGURES_DIR / filename
    fig.tight_layout()
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_1_correlation_heatmap(df: pd.DataFrame) -> None:
    vars_to_plot = [OUTCOME, DRIVER, *CONTROLS]
    corr_matrix = df[vars_to_plot].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        square=True,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.set_title("Plot 1: Correlation Heatmap", fontsize=13)
    save_figure(fig, "plot1_correlation_heatmap.png")


def plot_2_outcome_time_series(df: pd.DataFrame) -> None:
    ts = df.groupby(TIME_COL, as_index=False)[OUTCOME].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ts[TIME_COL], ts[OUTCOME], marker="o", linewidth=2)
    ax.set_title("Plot 2: Time Series of Outcome Variable")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Foreign Investment (USD)")
    ax.grid(alpha=0.3)
    save_figure(fig, "plot2_outcome_time_series.png")


def plot_3_dual_axis_outcome_driver(df: pd.DataFrame) -> None:
    ts = df.groupby(TIME_COL, as_index=False)[[OUTCOME, DRIVER]].mean()

    fig, ax1 = plt.subplots(figsize=(10, 5))
    color_left = "tab:blue"
    color_right = "tab:red"

    ax1.plot(ts[TIME_COL], ts[OUTCOME], color=color_left, marker="o", label=OUTCOME)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Average Foreign Investment (USD)", color=color_left)
    ax1.tick_params(axis="y", labelcolor=color_left)
    ax1.grid(alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(ts[TIME_COL], ts[DRIVER], color=color_right, marker="s", label=DRIVER)
    ax2.set_ylabel("Average CPI Score", color=color_right)
    ax2.tick_params(axis="y", labelcolor=color_right)

    ax1.set_title("Plot 3: Dual-Axis Outcome vs Driver")
    save_figure(fig, "plot3_dual_axis_outcome_driver.png")


def plot_4_lagged_effect(df: pd.DataFrame) -> None:
    lags = [0, 1, 2, 3, 6, 12]
    work = df[[ENTITY_COL, TIME_COL, OUTCOME, DRIVER]].copy()
    work = work.sort_values([ENTITY_COL, TIME_COL]).reset_index(drop=True)

    lag_corrs = []
    for lag in lags:
        lag_col = f"{DRIVER}_lag{lag}"
        work[lag_col] = work.groupby(ENTITY_COL)[DRIVER].shift(lag)
        corr_val = work[OUTCOME].corr(work[lag_col])
        lag_corrs.append(corr_val)

    lag_df = pd.DataFrame({"lag": lags, "correlation": lag_corrs})

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=lag_df, x="lag", y="correlation", color="#4C78A8", ax=ax)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Plot 4: Lagged Effect Analysis")
    ax.set_xlabel("Lag (years)")
    ax.set_ylabel(f"Correlation: {OUTCOME} vs lagged {DRIVER}")
    save_figure(fig, "plot4_lagged_effect_analysis.png")


def plot_5_6_group_or_alternative(df: pd.DataFrame) -> None:
    n_groups = df[ENTITY_COL].nunique()

    if n_groups >= 4:
        # Plot 5: Box plot by group (country)
        top_groups = (
            df[ENTITY_COL]
            .value_counts()
            .sort_values(ascending=False)
            .head(12)
            .index
        )
        box_df = df[df[ENTITY_COL].isin(top_groups)].copy()

        fig5, ax5 = plt.subplots(figsize=(13, 6))
        sns.boxplot(data=box_df, x=ENTITY_COL, y=OUTCOME, ax=ax5)
        ax5.set_title("Plot 5: Outcome Distribution by Country (Top 12)")
        ax5.set_xlabel("Country")
        ax5.set_ylabel("Foreign Investment (USD)")
        ax5.tick_params(axis="x", rotation=45)
        save_figure(fig5, "plot5_group_boxplots.png")

        # Plot 6: Group sensitivity (corr with driver)
        sens = (
            df.groupby(ENTITY_COL)
            .apply(lambda x: x[OUTCOME].corr(x[DRIVER]))
            .dropna()
            .sort_values()
            .rename("sensitivity")
            .reset_index()
        )

        threshold = -0.3
        sens["bucket"] = np.where(sens["sensitivity"] < threshold, "Sensitive", "Resilient")
        palette = {"Sensitive": "#D62728", "Resilient": "#2CA02C"}

        fig6, ax6 = plt.subplots(figsize=(10, 8))
        sns.barplot(
            data=sens,
            y=ENTITY_COL,
            x="sensitivity",
            hue="bucket",
            dodge=False,
            palette=palette,
            ax=ax6,
        )
        ax6.axvline(threshold, color="black", linestyle="--", linewidth=1)
        ax6.set_title("Plot 6: Country Sensitivity to CPI Score")
        ax6.set_xlabel("Correlation with CPI Score")
        ax6.set_ylabel("Country")
        ax6.legend(title="Category")
        save_figure(fig6, "plot6_group_sensitivity.png")
    else:
        # Alternative B: Rolling correlation when meaningful groups are not available
        ts = df.groupby(TIME_COL, as_index=False)[[OUTCOME, DRIVER]].mean()
        ts = ts.sort_values(TIME_COL)
        window = 3 if len(ts) < 12 else 6
        ts["rolling_corr"] = ts[OUTCOME].rolling(window=window).corr(ts[DRIVER])

        fig5, ax5 = plt.subplots(figsize=(10, 5))
        ax5.plot(ts[TIME_COL], ts["rolling_corr"], marker="o")
        ax5.axhline(0, color="black", linewidth=1)
        ax5.set_title("Plot 5/6 Alternative: Rolling Correlation")
        ax5.set_xlabel("Year")
        ax5.set_ylabel(f"Rolling Correlation ({window}-period)")
        ax5.grid(alpha=0.3)
        save_figure(fig5, "plot5_6_alternative_rolling_correlation.png")


def plot_7_control_scatter(df: pd.DataFrame) -> None:
    for control in CONTROLS:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(
            data=df,
            x=control,
            y=OUTCOME,
            scatter_kws={"alpha": 0.6},
            line_kws={"color": "red"},
            ax=ax,
        )
        ax.set_title(f"Plot 7: {OUTCOME} vs {control}")
        ax.set_xlabel(control)
        ax.set_ylabel("Foreign Investment (USD)")
        fname = f"plot7_scatter_{control}.png"
        save_figure(fig, fname)


def plot_8_time_series_decomposition(df: pd.DataFrame) -> None:
    ts = df.groupby(TIME_COL)[OUTCOME].mean().sort_index()

    if len(ts) < 8:
        warnings.warn("Not enough observations for decomposition; skipping Plot 8.")
        return

    # Annual data: conservative period choice to avoid overfitting short samples.
    period = 2 if len(ts) >= 8 else 1
    result = seasonal_decompose(ts, model="additive", period=period, extrapolate_trend="freq")

    fig = result.plot()
    fig.set_size_inches(10, 8)
    fig.suptitle("Plot 8: Time Series Decomposition (Outcome)", y=1.02)
    save_figure(fig, "plot8_time_series_decomposition.png")


def main() -> None:
    sns.set_style("whitegrid")
    df = load_data()

    plot_1_correlation_heatmap(df)
    plot_2_outcome_time_series(df)
    plot_3_dual_axis_outcome_driver(df)
    plot_4_lagged_effect(df)
    plot_5_6_group_or_alternative(df)
    plot_7_control_scatter(df)
    plot_8_time_series_decomposition(df)

    print("EDA plots created in:", FIGURES_DIR)


if __name__ == "__main__":
    main()
