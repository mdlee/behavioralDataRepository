# Lee & Dry (2006) uncertain advice

Lee, M. D., & Dry, M. J. (2006). Decision-making and confidence given uncertain advice. *Cognitive Science*, 30, 1081–1095.

Left vs right door. On each trial an advisor says “go left,” “go right,” or “no idea.” Six conditions set the certainty threshold at which advice is offered (50%, 60%, 70%, 80%, 90%, 100%). Higher thresholds mean rarer but more accurate advice. The 100% condition never offers advice.

30 people (text-advice condition only; the paper did not use the face-advice participants). 50 trials per condition. Exported from the original participant files, skipping two header rows in each file. `participant` IDs in `trials.csv` and `conditionOrder.csv` are the same 30 people.

## Files

- `trials.csv` — 9,000 rows
- `conditionOrder.csv` — randomized order of the six conditions

## Columns

- `advice`: −1 left, 0 none, +1 right
- `truth`, `decision`: 0 left, 1 right
- `pLeft`, `pRight`: advisor’s probabilities
- `confidence`: 1–5 (occasional 0)
- `adviceThresholdPercent`: 50–100
- `presentationPosition`: when that condition was done (1 = first)
