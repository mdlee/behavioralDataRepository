# Lee & Courey (2021) mate selection

Lee, M. D., & Courey, K. A. (2021). Modeling optimal stopping in changing environments: A case study in mate selection. *Computational Brain & Behavior*, 4, 1–17. [github.com/mdlee/mateSelectionOptimalStopping](https://github.com/mdlee/mateSelectionOptimalStopping)

Value-maximizing optimal stopping with a mate-choice cover story. 15 ages (18–46), 50 problems in each of two environments (`female`, `male`), **55 people**. A few problems are missing a choice (5,494 rows rather than 5,500).

`gender` in `participants.csv` is `1` = female, `2` = male, `0` = not reported. `environmentOrder` is `1` = female first, `2` = male first. Session timestamps are not included.

## Files

- `trials.csv` — one row per problem
- `problemValues.csv` — sequences, plus the max and optimal positions
- `positions.csv` — age labels, truncated-Gaussian parameters, optimal thresholds
- `participants.csv`

## Columns (`trials.csv`)

- `environment` — `female` or `male`
- `choicePosition` — 1-indexed stop
- `value` — attractiveness of the chosen option
- `value1` … `value15` — the sequence
