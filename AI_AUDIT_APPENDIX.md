# AI Audit Appendix: Milestone 1

**Team:** [Your Team Name]

**Date:** [Submission date]

## AI Tools Used

- [x] ChatGPT
- [x] GitHub Copilot
- [ ] Claude
- [ ] Other: [Specify]

## Detailed Log

### 1. pandas-datareader FRED API Integration

**Prompt (ChatGPT):**

> "How do I use pandas-datareader to fetch the Federal Funds Rate (FEDFUNDS) from FRED for the date range 2015-01-01 to 2023-12-31?"

**AI Output:**

```python
import pandas_datareader as pdr
from datetime import datetime

start = datetime(2015, 1, 1)
end = datetime(2023, 12, 31)
fedfunds = pdr.DataReader("FEDFUNDS", "fred", start, end)
```

### 2. Creating Visualizations from Cleaned Data Pipeline

**Prompt:**

Create visualizations in guideline with the requirements of Milestone 2. Add the captions written in the text file to each of our graphics.

**Output:**

All code written in `m2_eda_plots.py`. Added captions embedded to the bottom of each visualization.

---

# AI Audit Appendix: Milestone 3

**Team:** Arjun, Daemian, Kade, Isidro

**Date:** 2026-04-20

## AI Tools Used

- [x] ChatGPT
- [x] GitHub Copilot
- [ ] Claude
- [ ] Other: [Specify]

## Detailed Log (Milestone 3)

### 1. Econometric script structure and implementation

**Prompt (GitHub Copilot):**

> "Complete the code according to this readme. Build Milestone 3 with Model A fixed effects, one Model B option, diagnostics, robustness checks, and saved outputs."

**AI Output Summary:**

- Generated `code/capstone_models.py` with required section headers.
- Implemented Model A two-way fixed effects using `linearmodels.PanelOLS`.
- Implemented Model B as ML comparison (`RandomForestRegressor` vs OLS).
- Saved regression outputs and diagnostics into `results/tables/` and `results/figures/`.

**Human Verification / Edits:**

- Verified script runs top-to-bottom with no runtime errors.
- Confirmed output files exist and match milestone deliverable requirements.

### 2. Handling absorbed regressors under fixed effects

**Prompt (GitHub Copilot):**

> "The fixed effects model fails because one variable is absorbed. Fix the code so it runs correctly."

**AI Output Summary:**

- Added `drop_absorbed=True` to PanelOLS specifications.
- Model now automatically drops fully absorbed regressors (e.g., near time-invariant country-level predictors under entity FE).

**Human Verification / Edits:**

- Reviewed warning output and confirmed this behavior is econometrically expected.
- Retained transparent reporting of dropped-variable behavior in interpretation memo.

### 3. Diagnostic interpretation guidance

**Prompt (ChatGPT/GitHub Copilot):**

> "Interpret Breusch-Pagan, VIF, and residual diagnostics for Milestone 3 memo language."

**AI Output Summary:**

- Proposed interpretation framing for p-values near 0.05 in heteroskedasticity testing.
- Suggested VIF threshold language and cautionary interpretation.
- Suggested memo language linking plots to model assumptions.

**Human Verification / Edits:**

- Cross-checked all interpretations against saved CSV outputs.
- Avoided overclaiming significance.
- Marked uncertain conclusions as tentative/cautious.

### 4. Robustness check design

**Prompt (GitHub Copilot):**

> "Add at least three robustness checks that fit this dataset."

**AI Output Summary:**

- Implemented clustered vs unclustered SE comparison.
- Implemented alternative lag robustness (lag 1, 2, 3).
- Implemented outlier-period exclusion (drop year 2020).
- Implemented subgroup estimation (high-crime vs low-crime subsamples).

**Human Verification / Edits:**

- Confirmed all robustness result files are generated and populated.
- Checked that robustness conclusions are consistent with output magnitudes and p-values.

### 5. Dependency suggestions and environment setup

**Prompt (GitHub Copilot):**

> "Resolve missing package errors and make requirements reproducible."

**AI Output Summary:**

- Identified and installed missing packages (`linearmodels`, `scikit-learn`, `pypdf`).
- Updated `requirements.txt` to include econometrics and PDF dependencies.

**Human Verification / Edits:**

- Re-ran the full script after package updates.
- Confirmed successful completion and artifact generation.

## Academic Integrity Statement (Milestone 3)

AI tools were used for coding assistance, debugging, and drafting interpretation language. Final model choices, result interpretation, and all submission decisions were reviewed and approved by team members.
No AI output was accepted without human verification against actual model output files.


