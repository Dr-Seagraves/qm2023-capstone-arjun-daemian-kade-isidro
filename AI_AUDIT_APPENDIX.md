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
> "How do I use pandas-datareader to fetch the Federal Funds Rate (FEDFUNDS) from
FRED for the date range 2015-01-01 to 2023-12-31?"
**AI Output:**
```python
import pandas_datareader as pdr
from datetime import datetime
start = datetime(2015, 1, 1)
end = datetime(2023, 12, 31)
fedfunds = pdr.DataReader('FEDFUNDS', 'fred', start, end)