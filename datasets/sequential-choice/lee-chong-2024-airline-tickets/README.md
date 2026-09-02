# Lee & Chong (2024) airline tickets

Lee, M. D., & Chong, S. (2024). Strategies people use buying airline tickets: A cognitive modeling analysis of optimal stopping in a changing environment. *Experimental Economics*, 27, 854–873. [osf.io/nve5b](https://osf.io/nve5b/)

Cost-minimizing optimal stopping: 12 purchase times from 12 months out to 1 day before travel, 50 problems, **46 people, 2,300 problems**. Prices are drawn from distributions that get worse near the flight date.

Session start/stop times from the survey export are not included.

## Files

- `trials.csv` — one row per problem
- `problemValues.csv` — the 50 sequences
- `positions.csv` — labels, generating mean/SD, and optimal thresholds
- `participants.csv` — age and gender

## Columns (`trials.csv`)

- `choicePosition` — 1-indexed purchase time (`1` = 12 months out, `12` = 1 day)
- `cost` — price paid
- `problemOrder` — presentation order for that person
- `value1` … `value12` — the sequence
