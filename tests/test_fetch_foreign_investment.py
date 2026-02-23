import importlib.util
from pathlib import Path

import pandas as pd
import pytest


def _import_module():
    # dynamic import because filename contains characters invalid for normal
    # imports
    path = Path("code") / "fetch_[ForeignInvest]_data.py"
    spec = importlib.util.spec_from_file_location("ffi", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


RAW_TEXT = """this,is,ignored
metadata,line,foo
more,meta,bar
Country Name,Country Code,1960,1961
A,AAA,100,200
B,BBB,300,400
"""


def test_load_basic(tmp_path, monkeypatch):
    mod = _import_module()

    # create fake raw file
    infile = tmp_path / "raw.csv"
    infile.write_text(RAW_TEXT)

    # redirect processed directory
    monkeypatch.setattr(mod, "PROCESSED_DATA_DIR", tmp_path / "processed")

    # load, letting default output path be used
    df = mod.load_foreign_investment(path=infile)

    # expect two rows and columns Entity, Time, Value
    assert list(df.columns) == ["Entity", "Time", "Value"]
    assert df.shape == (4, 3)  # 2 countries * 2 years
    # no missing values in output
    assert df.Value.notna().all()

    # file should exist in processed directory with default name
    outpath = tmp_path / "processed" / mod.DEFAULT_PROCESSED_FILENAME
    assert outpath.exists()
    df2 = pd.read_csv(outpath)
    assert set(df2.Entity.unique()) == {"A", "B"}


def test_explicit_output(tmp_path):
    mod = _import_module()

    infile = tmp_path / "raw2.csv"
    infile.write_text(RAW_TEXT)

    out = tmp_path / "myout.csv"
    df = mod.load_foreign_investment(path=infile, output=out)
    assert out.exists()
    df2 = pd.read_csv(out)
    assert df2.shape == (4, 3)

    # ensure returned df matches contents (allow for dtype differences)
    pd.testing.assert_frame_equal(df.reset_index(drop=True), df2, check_dtype=False)


def test_missing_values_are_dropped(tmp_path, monkeypatch):
    """Rows where the numeric inflow is empty should be removed."""
    mod = _import_module()
    raw = tmp_path / "raw3.csv"
    # create a file with the usual three metadata rows followed by header
    # row; the loader skips the first three lines, so our data begins on line 4.
    raw.write_text("""meta line 1
meta line 2
meta line 3
Country Name,Country Code,1960,1961
X,XXX,,500
""")
    monkeypatch.setattr(mod, "PROCESSED_DATA_DIR", tmp_path / "proc")
    df = mod.load_foreign_investment(path=raw)
    assert df.shape == (1, 3)
    assert df.Value.notna().all()
