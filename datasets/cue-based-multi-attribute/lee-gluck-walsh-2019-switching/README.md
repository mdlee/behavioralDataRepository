# Lee, Gluck, & Walsh (2019) strategy switching

Lee, M. D., Gluck, K. A., & Walsh, M. M. (2019). Understanding the complexity of simple decisions: Modeling multiple behaviors and switching strategies. *Decision*, 6, 335–368. [osf.io/s9u5x](https://osf.io/s9u5x/)

Two-alternative, four-cue choices. 38 people, 120 trials (a few trials have no recorded decision: **4,557 rows**). Between-subjects `aloud` (19 people, with verbal reports) vs `silent` (19 people).

Cue validities are 0.80, 0.75, 0.70, 0.69.

## Files

- `trials.csv` — one row per choice
- `searches.csv` — cue-opening order and times
- `layouts.csv` — which cue sat in which display slot
- `reports.csv` — verbal reports in the aloud condition
- `cues.csv` — validity and log-odds

## Columns (`trials.csv`)

- `decision` / `reward` — `1` or `2` (alternative)
- `correct`
- `trialStartSec` — time from the start of the session
