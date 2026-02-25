"""Utilities for downloading and parsing crime-index data from online sources.

The canonical source we currently support is Numbeo's Crime Index (https://www.numbeo.com/crime/),
which publishes a table of country crime-index scores and historically provides CSV downloads.

The functions here are intentionally generic so that you can adapt them to a new source in the future.

Example
-------
>>> from fetch_crime_index import fetch_numbeo_crime_index
>>> df = fetch_numbeo_crime_index()
>>> df.head()
   Country  Crime Index  Year
0  Armenia         58.07  2025
...  

"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

# these imports are optional; tests will warn if they're missing
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    requests = None  # type: ignore
    BeautifulSoup = None  # type: ignore

# default URL for Numbeo crime index rankings by country
NUMBEO_CRIME_URL = "https://www.numbeo.com/crime/rankings_by_country.jsp"


# ---------------------------------------------------------------------------
# parsing helpers
# ---------------------------------------------------------------------------

def _parse_numbeo_table(html: str) -> pd.DataFrame:
    """Extract country crime data from Numbeo HTML.

    Parameters
    ----------
    html : str
        Raw HTML containing a Numbeo "rankings_by_country" table.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``['Country', 'Crime Index']``.

    Notes
    -----
    This is intentionally simple; if the page structure changes you may need to
    update the selector or column logic.  Only non-header rows are returned.
    """
    if BeautifulSoup is None:
        raise RuntimeError("BeautifulSoup is required to parse HTML; install bs4")

    soup = BeautifulSoup(html, "html.parser")

    # Numbeo doesn't mark the crime table with an explicit class; the current
    # page simply contains a generic <table> whose header row includes
    # "Crime Index".  Find the first such table.
    table = None
    for tbl in soup.find_all("table"):
        ths = [th.get_text(strip=True) for th in tbl.find_all("th")]
        if any("Crime Index" in t for t in ths):
            table = tbl
            break

    if table is None:
        raise ValueError("Unable to locate crime-index table in HTML")

    # gather column headers from the discovered table
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        texts = [cell.get_text(strip=True) for cell in cells]
        # skip header row, which replicates headers
        if texts == headers:
            continue
        rows.append(texts)

    df = pd.DataFrame(rows, columns=headers)

    # standardize names
    if "Country" not in df.columns or "Crime Index" not in df.columns:
        raise ValueError("Expected columns 'Country' and 'Crime Index' not found")

    df = df.loc[:, ["Country", "Crime Index"]].copy()
    df["Crime Index"] = pd.to_numeric(df["Crime Index"], errors="coerce")
    return df


# ---------------------------------------------------------------------------
# public functions
# ---------------------------------------------------------------------------

def fetch_numbeo_crime_index(
    year: Optional[int] = None,
    cache_path: Optional[Path] = None,
    url: str = NUMBEO_CRIME_URL,
) -> pd.DataFrame:
    """Retrieve crime index values for all countries from Numbeo.

    Parameters
    ----------
    year : int, optional
        If supplied, the returned DataFrame will include a ``Year`` column with
        this value (the Numbeo page does not embed the year).
    cache_path : Path, optional
        If provided and the file exists, the cached CSV will be read instead of
        making a network request.  When the network fetch succeeds the CSV will
        also be written to this path for future use.
    url : str
        The URL to download; defaults to ``NUMBEO_CRIME_URL``.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``['Country', 'Crime Index', 'Year']`` (year may
        contain ``NaN`` if ``year`` was not specified).

    Raises
    ------
    RuntimeError
        If ``requests`` or ``bs4`` are not installed when a network fetch is
        attempted.

    Notes
    -----
    Numbeo does not provide an official public API.  This function performs a
    simple HTTP GET and parses the HTML table; use responsibly and follow the
    site's terms of service.  Consider caching results to avoid repeated
    downloads.
    """
    if cache_path is not None and cache_path.exists():
        df = pd.read_csv(cache_path)
        if year is not None:
            df["Year"] = year
        return df

    if requests is None:
        raise RuntimeError("`requests` library is required to fetch online data")

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = _parse_numbeo_table(resp.text)
    if year is not None:
        df["Year"] = year
    else:
        df["Year"] = pd.NA

    if cache_path is not None:
        try:
            df.to_csv(cache_path, index=False)
        except Exception:
            pass

    return df


def save_crime_index_csv(
    path: Path, *, year: Optional[int] = None, **fetch_kwargs
) -> None:
    """Fetch data and save it to ``path`` as CSV.

    This is a thin wrapper around :func:`fetch_numbeo_crime_index` that
    guarantees the parent directory exists.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df = fetch_numbeo_crime_index(year=year, **fetch_kwargs)
    df.to_csv(path, index=False)


def fetch_numbeo_crime_index_range(
    start_year: int,
    end_year: int,
    cache_dir: Optional[Path] = None,
    url: str = NUMBEO_CRIME_URL,
) -> pd.DataFrame:
    """Download crime-index tables for a range of years.

    Parameters
    ----------
    start_year, end_year : int
        Inclusive bounds of years to fetch.  ``start_year`` may be greater than
        ``end_year`` but the resulting DataFrame will always be sorted by year.
    cache_dir : Path, optional
        Directory in which to store per-year CSV caches.  If provided the
        function will write ``<cache_dir>/crime_<year>.csv`` files and reuse
        them on subsequent invocations.  A ``None`` value disables caching.
    url : str
        Base URL to pass through to :func:`fetch_numbeo_crime_index`.

    Returns
    -------
    pd.DataFrame
        Concatenated frame containing all years in the requested range.  The
        result will always contain a ``Year`` column.
    """
    frames = []
    yrs = list(range(start_year, end_year + 1))
    for y in yrs:
        cache = None
        if cache_dir is not None:
            cache_dir = Path(cache_dir)
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache = cache_dir / f"crime_{y}.csv"
        df = fetch_numbeo_crime_index(year=y, cache_path=cache, url=url)
        frames.append(df)
    result = pd.concat(frames, ignore_index=True)
    return result


# allow command‑line usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download Numbeo Crime Index and write to CSV."
    )
    parser.add_argument(
        "--year", type=int, help="year to assign to all rows (e.g. 2025)"
    )
    parser.add_argument(
        "--start", type=int, help="first year to fetch (inclusive)"
    )
    parser.add_argument(
        "--end", type=int, help="last year to fetch (inclusive)"
    )
    parser.add_argument(
        "--out", type=Path, default=Path("data/raw/numbeo_crime_index.csv"),
        help="output CSV path",
    )
    parser.add_argument(
        "--no-cache", dest="cache_path", action="store_const", const=None,
        help="don't use a cache file even if output path already exists",
    )
    parser.add_argument(
        "--url", type=str, default=NUMBEO_CRIME_URL,
        help="URL to download (overrides default)"
    )
    args = parser.parse_args()

    if args.start is not None and args.end is not None:
        # fetch a range of years and concatenate
        df = fetch_numbeo_crime_index_range(
            args.start, args.end,
            cache_dir=args.out.parent if args.cache_path is not None else None,
            url=args.url,
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.out, index=False)
    else:
        save_crime_index_csv(
            args.out, year=args.year, cache_path=args.cache_path, url=args.url
        )
