"""Helpers for reshaping Crime Index data.

The raw download gives one row per country-year; analysts often prefer a
wide panel with years on the index and countries as columns.  This module
contains utilities to perform that transformation and write a spreadsheet-ready
file.

Example
-------
>>> from transform_crime_index import wide_from_long
>>> df = wide_from_long("data/raw/numbeo_crime_index_2012_2025.csv")
>>> df.loc[2025, "United States"]
67.8
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


def wide_from_long(
    source: Union[str, Path],
    output: Union[str, Path, None] = None,
    fill_value: float = float("nan"),
) -> pd.DataFrame:
    """Convert a long-format crime-index table into a wide panel.

    Parameters
    ----------
    source : str or Path
        Path to a CSV (or anything ``pd.read_csv`` understands) containing at
        least the columns ``['Country', 'Crime Index', 'Year']``.
    output : str or Path, optional
        If provided the resulting wide DataFrame will also be written to this
        location in CSV format.  The parent directory will be created if
        necessary.  If the path ends with ``.xlsx`` the file will be saved as
        an Excel workbook using ``DataFrame.to_excel``; otherwise CSV is used.
    fill_value : float, default NaN
        Value to fill for missing entries in the pivot table.

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame indexed by year with one column per country.
    """
    df = pd.read_csv(source)

    # ensure required columns present
    for col in ["Country", "Crime Index", "Year"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column '{col}' in source data")

    # pivot
    wide = df.pivot_table(
        index="Year",
        columns="Country",
        values="Crime Index",
        aggfunc="first",
    )

    if fill_value is not None:
        wide = wide.fillna(fill_value)

    # optionally write output
    if output is not None:
        outp = Path(output)
        outp.parent.mkdir(parents=True, exist_ok=True)
        if outp.suffix.lower() in [".xlsx", ".xls"]:
            wide.to_excel(outp)
        else:
            wide.to_csv(outp)

    return wide


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Pivot a long crime-index CSV into a wide spreadsheet."
    )
    parser.add_argument("source", help="path to raw crime index CSV")
    parser.add_argument(
        "--out", help="output file path (csv or xlsx)", default=None
    )
    parser.add_argument(
        "--fill", type=float, default=float("nan"),
        help="value to use for missing cells (default=NaN)"
    )
    args = parser.parse_args()

    wide = wide_from_long(args.source, output=args.out, fill_value=args.fill)
    if args.out is None:
        print(wide)
