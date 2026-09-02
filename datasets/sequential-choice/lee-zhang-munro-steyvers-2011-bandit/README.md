# Lee, Zhang, Munro, & Steyvers (2011) bandit

Lee, M. D., Zhang, S., Munro, M. N., & Steyvers, M. (2011). Psychological models of human and optimal performance on bandit problems. *Cognitive Systems Research*, 12, 164–174.

Two-armed bandit. 10 people × 3 environments × 2 horizons × 50 games.

Environments (Beta parameters on the two arms):

- `neutral`: A=1, B=1
- `sparse`: A=2, B=4
- `plentiful`: A=4, B=2

Horizons: 8 or 16 trials per game.

Original source filenames used initials. Those were replaced with anonymous `participant` IDs 1–10 (alphabetical order of the original codes).

## Files

- `trials.csv` — 36,000 rows

## Columns

- `participant` 1–10
- `horizon` 8 or 16
- `environment`, `environmentCode` (`A1-B1`, `A2-B4`, `A4-B2`)
- `game`, `trial`
- `choice` 1 = left, 2 = right
- `reward` 0/1
