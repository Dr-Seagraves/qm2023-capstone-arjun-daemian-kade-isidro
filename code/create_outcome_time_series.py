import os

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    data_path = "data/final/analysis_panel.csv"
    out_dir = "results/figures"
    out_path = os.path.join(out_dir, "outcome_time_series.png")

    df = pd.read_csv(data_path)

    if "Year" not in df.columns or "cpi_score" not in df.columns:
        raise ValueError("Expected columns 'Year' and 'cpi_score' in analysis_panel.csv")

    # Create a global yearly average of the outcome variable.
    ts = (
        df[["Year", "cpi_score"]]
        .dropna(subset=["Year", "cpi_score"])
        .groupby("Year", as_index=False)["cpi_score"]
        .mean()
        .sort_values("Year")
    )

    # Keep the chart window through 2023.
    ts = ts[ts["Year"] <= 2023]

    os.makedirs(out_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(ts["Year"], ts["cpi_score"], marker="o", linewidth=2)
    plt.title("Time Series of Outcome Variable (CPI Score)")
    plt.xlabel("Year")
    plt.ylabel("Average CPI Score")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Saved outcome time series to: {out_path}")


if __name__ == "__main__":
    main()
