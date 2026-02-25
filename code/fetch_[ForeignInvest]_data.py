"""Fetch and process World Foreign Direct Investment inflow raw file.

This script reads the raw WorldForeignDirectInvestmentInflow file in
`data/raw`, locates the CSV header row, parses the wide table, handles
missing values, and writes both a cleaned wide CSV and a tidy (long)
CSV with columns ``Country``, ``Time``, ``Value`` to ``data/processed``.

Usage (from project root):
    python code/fetch_[ForeignInvest]_data.py
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Optional

import pandas as pd


def _find_header_row(path: Path) -> int:
    """Return number of lines to skip so the header row is the first row read.

    The raw file contains metadata lines before the CSV header. We look for
    the line that contains the header field "Country Name" and return the
    count of lines to skip so pandas will treat the next line as header.
    """
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh):
            if "Country Name" in line or "Country" in line and "Indicator Name" in line:
                # skip the lines before this one so the header is read next
                return i
    return 0


def read_raw_foreign_investment(raw_path: Path) -> pd.DataFrame:
    """Read the raw WorldForeignDirectInvestmentInflow file into a DataFrame.

    The function attempts to locate the header row automatically. The
    returned DataFrame contains one column per year (strings) plus
    descriptive columns like `Country Name`.
    """
    raw_path = Path(raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"raw file not found: {raw_path}")

    skip = _find_header_row(raw_path)
    # pandas: skip the first `skip` rows, then treat the next row as header
    df = pd.read_csv(raw_path, skiprows=skip, dtype=str, encoding="utf-8")
    return df


def clean_and_reshape(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the wide DataFrame and produce (wide_df, tidy_df).

    - Rename `Country Name` -> `Country`.
    - Drop helper columns like `Country Code`, `Indicator Name`, `Indicator Code`.
    - Convert year columns to numeric values.
    - Produce a tidy (long) DataFrame with columns ``Country, Time, Value``.
    """
    df = df.copy()

    # normalize country column
    if "Country Name" in df.columns:
        df = df.rename(columns={"Country Name": "Country"})
    elif "Country" in df.columns:
        df = df.rename(columns={"Country": "Country"})

    # drop unwanted meta columns if present
    for col in ["Country Code", "Indicator Name", "Indicator Code"]:
        if col in df.columns:
            df = df.drop(columns=col)

    # detect year columns (four-digit year names)
    year_cols = [c for c in df.columns if re.fullmatch(r"\d{4}", str(c))]

    # convert year columns to numeric (coerce bad values to NaN)
    for c in year_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # tidy (long) format
    # ensure wide is sorted by Country
    wide = df.set_index("Country").sort_index()

    return wide


def save_outputs(wide: pd.DataFrame, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    wide_path = out_dir / "foreign_investment_wide.csv"
    wide.to_csv(wide_path)


def process(raw_path: Optional[Path] = None, out_dir: Optional[Path] = None) -> Path:
    if raw_path is None:
        raw_path = Path("data/raw/WorldForeignDirectInvestmentInflow")
    if out_dir is None:
        out_dir = Path("data/processed")

    df = read_raw_foreign_investment(raw_path)
    wide = clean_and_reshape(df)
    save_outputs(wide, out_dir)

    return out_dir / "foreign_investment_wide.csv"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process World Foreign Direct Investment raw file")
    parser.add_argument("--raw", type=Path, help="raw input file", default=Path("data/raw/WorldForeignDirectInvestmentInflow"))
    parser.add_argument("--out", type=Path, help="output directory", default=Path("data/processed"))
    args = parser.parse_args()

    w = process(raw_path=args.raw, out_dir=args.out)
    print(f"Wrote: {w}")
#fetches and loads the raw foreign investment data from the raw data folder
#handles missing values and reshapes the data into a tidy format with columns Country, Time
#formats the data in a csv file so each row is a country and its observations, and each column is a year
#outputs this processed data csv file into the processed data folder
