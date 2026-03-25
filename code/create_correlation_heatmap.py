import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    data_path = "data/final/analysis_panel.csv"
    out_dir = "results/figures"
    out_path = os.path.join(out_dir, "correlation_heatmap.png")

    df = pd.read_csv(data_path)

    # Keep only numeric columns for correlation calculation.
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        raise ValueError("Need at least two numeric columns to create a correlation heatmap.")

    corr = numeric_df.corr()

    os.makedirs(out_dir, exist_ok=True)

    plt.figure(figsize=(14, 10))
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 7},
        linewidths=0.5,
        cbar_kws={"label": "Correlation Coefficient"},
    )
    plt.title("Correlation Heatmap - Analysis Panel", pad=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Saved heatmap to: {out_path}")


if __name__ == "__main__":
    main()
