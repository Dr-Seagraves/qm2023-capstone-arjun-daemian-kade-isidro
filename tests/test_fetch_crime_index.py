"""Unit tests for :mod:`fetch_crime_index`."""

from pathlib import Path
import pandas as pd
import pytest

from src import fetch_crime_index as fc


SAMPLE_HTML = """
<html><body>
<table>
<tr><th>Rank</th><th>Country</th><th>Crime Index</th></tr>
<tr><td>1</td><td>Testland</td><td>42.5</td></tr>
<tr><td>2</td><td>Examplestan</td><td>77</td></tr>
</table>
</body></html>
"""


def test_parse_numbeo_table_basic():
    df = fc._parse_numbeo_table(SAMPLE_HTML)
    assert list(df.columns) == ["Country", "Crime Index"]
    assert df.shape == (2, 2)
    assert df.loc[0, "Country"] == "Testland"
    assert df.loc[1, "Crime Index"] == 77


def test_fetch_with_cache(tmp_path, monkeypatch):
    # create a fake cache file
    cache_file = tmp_path / "cached.csv"
    pd.DataFrame({"Country": ["A"], "Crime Index": [1.0]}).to_csv(cache_file, index=False)

    # ensure fetch returns cached data
    df = fc.fetch_numbeo_crime_index(year=2020, cache_path=cache_file)
    assert df.loc[0, "Country"] == "A"
    assert df.loc[0, "Year"] == 2020

    # monkeypatch requests to ensure network is not called
    monkeypatch.setattr(fc, "requests", None)

    df2 = fc.fetch_numbeo_crime_index(year=2021, cache_path=cache_file)
    assert df2.loc[0, "Year"] == 2021


def test_fetch_network(monkeypatch):
    # simulate requests.get returning SAMPLE_HTML
    class DummyResp:
        text = SAMPLE_HTML
        def raise_for_status(self):
            pass
    monkeypatch.setattr(fc, "requests", type("R", (), {"get": staticmethod(lambda url, timeout: DummyResp())}))

    df = fc.fetch_numbeo_crime_index(year=2019, cache_path=None)
    assert "Testland" in df["Country"].values
    assert df.loc[0, "Year"] == 2019


def test_save_crime_index_csv(tmp_path, monkeypatch):
    # monkeypatch fetch_numbeo_crime_index to return a simple df
    monkeypatch.setattr(fc, "fetch_numbeo_crime_index", lambda **kwargs: pd.DataFrame({"Country":["X"],"Crime Index":[5],"Year":[2022]}))

    out = tmp_path / "out.csv"
    fc.save_crime_index_csv(out, year=2022)
    df = pd.read_csv(out)
    assert df.loc[0, "Country"] == "X"
    assert df.loc[0, "Year"] == 2022


def test_fetch_range(tmp_path, monkeypatch):
    # make the base fetch return a one-row DataFrame with the requested year
    def fake_fetch(*, year=None, **kwargs):
        return pd.DataFrame({"Country":["Y"], "Crime Index":[10], "Year":[year]})

    monkeypatch.setattr(fc, "fetch_numbeo_crime_index", fake_fetch)

    df = fc.fetch_numbeo_crime_index_range(2020, 2022, cache_dir=tmp_path)
    # should have three rows, years 2020, 2021, 2022
    assert set(df.Year) == {2020, 2021, 2022}
    assert df.shape[0] == 3

    # the real implementation writes caches; our fake fetch doesn't, so we
    # only assert the directory was created.
    assert tmp_path.exists() and tmp_path.is_dir()


def test_wide_from_long(tmp_path):
    # create a fake long CSV
    data = pd.DataFrame({
        "Country": ["A", "B", "A"],
        "Crime Index": [1.0, 2.0, 1.5],
        "Year": [2020, 2020, 2021],
    })
    src = tmp_path / "long.csv"
    data.to_csv(src, index=False)

    # import helper from module directly
    from src import transform_crime_index as tci
    wide = tci.wide_from_long(src)
    # should have two columns A and B, two rows 2020 and 2021
    assert list(wide.index) == [2020, 2021]
    assert set(wide.columns) == {"A", "B"}
    assert wide.loc[2020, "A"] == 1.0
    assert wide.loc[2021, "A"] == 1.5
