[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22639674&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

Team Name: Arjun, Daemian, Kade, Isidro

Research Question: How does perceived corruption and crime of a country affect countries foreign investment based on Corruption Percentage Index, Foreign Direct Investment, Crime Index, and Economic Uncertainty worldwide?


## Fetching Crime Index Data

We include a utility module in ``src/fetch_crime_index.py`` that can download
and parse the Numbeo Crime Index table.  The script is generic enough that you
can point it at any similar HTML table.

Install the dependencies before running:

```bash
pip install pandas requests beautifulsoup4
pip install pytest           # for running tests
```

Usage examples::

    # fetch a single year
    python -m src.fetch_crime_index --year 2025 \
        --out data/raw/numbeo_crime_index.csv

    # fetch a range of years and combine into one file
    python -m src.fetch_crime_index --start 2012 --end 2025 \
        --out data/raw/numbeo_crime_index_2012_2025.csv

    # provide a cache directory to avoid repeated downloads
    python -m src.fetch_crime_index --start 2012 --end 2025 \
        --out data/raw/numbeo_crime_index_2012_2025.csv \
        --no-cache  # disable caching if you really want to re-download

The resulting CSV can then be loaded from ``data/raw`` and filtered for the
years 2012–2025 as needed.


Goal: We  want to establish a relationship between corruption and/or foreign direct investment and crime, which can then be used to address the associated economic effects of corruption.

## Project Structure

- **src/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python src/config_paths.py` to verify paths.