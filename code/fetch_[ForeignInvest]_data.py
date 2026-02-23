"""Utilities for loading and cleaning World Bank foreign
investment‑inflow data.

The raw file in ``data/raw/WorldForeignDirectInvestmentInflow`` is a
wide-format table where each row corresponds to a country or aggregate and
columns contain years from 1960 through the most recent update.  The first
couple of lines include metadata and must be skipped when reading with
``pandas``.

Functions in this module perform the following steps:

* read the raw CSV file (skipping the preliminary metadata rows)
* drop extraneous columns and any unnamed placeholders
* melt the wide table into a long/panel format with one observation per
  (country, year) pair
* convert types, handle missing values and duplicates
* flag and remove obvious outliers (values more than three standard
deviations from the country mean)

Example
-------
>>> from src import fetch_foreign_investment as ffi
>>> df = ffi.load_foreign_investment()
>>> df.head()
     Entity  Time         Value
0     Aruba  1980  0.000000e+00
1     Aruba  1981  1.087876e+06
...
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


# default locations of raw/processed data (uses configuration)
try:
    from src.config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
except ImportError:  # pragma: no cover - configuration may not be available
    RAW_DATA_DIR = Path("data") / "raw"  # fallback, not strict
    PROCESSED_DATA_DIR = Path("data") / "processed"

DEFAULT_RAW_PATH = RAW_DATA_DIR / "WorldForeignDirectInvestmentInflow"
# where to write cleaned panel when no explicit output is supplied
DEFAULT_PROCESSED_FILENAME = "foreign_investment_long.csv"


def _read_raw(path: Union[str, Path]) -> pd.DataFrame:
    """Load the raw CSV skipping the metadata header rows.

    Parameters
    ----------
    path : str or Path
        Path to the raw input file.  The function does not assume a particular
        file extension because the source file in ``data/raw`` lacks one.

    Returns
    -------
    pd.DataFrame
        Wide-format table with a row for each country/aggregate and a column
        for every year.
    """
    p = Path(path)
    # the first three meaningful lines are metadata; skip them so that
    # pandas sees the proper column names on the first row.
    df = pd.read_csv(p, skiprows=3)
    # drop any columns pandas created for stray delimiters
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]  # type: ignore
    return df


def _melt_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a wide, year‑column table into long panel format.

    Parameters
    ----------
    df : pd.DataFrame
        Output from :func:`_read_raw`.

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns ``['Entity', 'Time', 'Value']``.
    """
    # expect the raw file to have these columns; don't fail loudly if they are
    # missing but rename when present.
    name_col = "Country Name" if "Country Name" in df.columns else "Entity"
    df = df.rename(columns={name_col: "Entity"})

    # identify year columns (they should be convertible to integers)
    year_cols = [c for c in df.columns if c not in ["Entity", "Country Code"]]
    # melt the dataset
    long = df.melt(id_vars=["Entity"], value_vars=year_cols, var_name="Time", value_name="Value")

    # convert types
    long["Time"] = pd.to_numeric(long["Time"], errors="coerce").astype("Int64")
    long["Value"] = pd.to_numeric(long["Value"], errors="coerce")

    return long


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic cleaning rules to a long-format DataFrame.

    * drop rows with missing entity or year
    * remove duplicates
    * drop outliers (more than three standard deviations from the entity mean)
    * drop rows with missing ``Value`` so that the returned table contains
      only observed inflows.  We still do not impute values.
    """
    df = df.dropna(subset=["Entity", "Time"])
    df = df.drop_duplicates()

    # remove outliers without dropping the Entity column; groupby.apply drops the
    # key so we instead compute a mask using group transforms.
    if "Value" in df.columns and df["Value"].dtype.kind in "fi":
        grp = df.groupby("Entity")["Value"]
        mu = grp.transform("mean")
        sigma = grp.transform("std")
        # mask keeps rows where sigma is NaN (e.g. only one value) or zero
        # or where the value is within 3 std devs of the mean
        mask = sigma.isna() | sigma.eq(0) | ((df["Value"] - mu).abs() <= 3 * sigma)
        df = df.loc[mask]

    # drop entries that have no numeric value; this ensures the output file
    # contains only rows with actual inflow numbers.
    if "Value" in df.columns:
        df = df.dropna(subset=["Value"])

    df = df.reset_index(drop=True)
    return df


def load_foreign_investment(
    path: Union[str, Path, None] = None,
    output: Union[str, Path, None] = None,
) -> pd.DataFrame:
    """Public helper that returns a cleaned, long panel of FDI inflows.

    Parameters
    ----------
    path : str or Path, optional
        Location of the raw CSV.  If ``None`` the default path defined by
        ``DEFAULT_RAW_PATH`` is used.
    output : str or Path, optional
        If provided, the cleaned DataFrame will be written to this location
        as a CSV.  If ``None`` the default file
        ``PROCESSED_DATA_DIR/foreign_investment_long.csv`` will be used.  The
        saved table will contain only rows where a numeric ``Value`` is
        available.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``['Entity', 'Time', 'Value']``.
    """
    if path is None:
        path = DEFAULT_RAW_PATH
    df = _read_raw(path)
    df = _melt_to_long(df)
    df = _clean(df)

    # write output if requested (always write by default)
    if output is None:
        outp = PROCESSED_DATA_DIR / DEFAULT_PROCESSED_FILENAME
    else:
        outp = Path(output)
    # ensure directory exists
    outp.parent.mkdir(parents=True, exist_ok=True)
    # use CSV format
    df.to_csv(outp, index=False)

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Load and clean world foreign direct investment inflow data."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(DEFAULT_RAW_PATH),
        help="path to the raw data file",
    )
    parser.add_argument(
        "--out", "-o",
        help="if provided the cleaned long table will be written to this CSV",
    )
    args = parser.parse_args()

    # always save to either the user-supplied path or default processed
    # directory so that downstream steps can rely on a consistent location.
    if args.out:
        save_path = Path(args.out)
    else:
        save_path = PROCESSED_DATA_DIR / DEFAULT_PROCESSED_FILENAME
    save_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(save_path, index=False)
    print(f"cleaned data written to {save_path}")
