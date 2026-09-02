# Guan et al. (2020) two-armed bandit

Guan, M., Stokes, R., Vandekerckhove, J., & Lee, M. D. (2020). A cognitive modeling analysis of risk in sequential choice tasks. *Judgment and Decision Making*, 15(5), 823–850. [doi:10.1017/s1930297500007956](https://doi.org/10.1017/s1930297500007956)

Two-armed bandit, 56 people. Four conditions: horizon 8 or 16 × environment neutral `Beta(1,1)` or plentiful `Beta(4,2)`. Forty problems per condition. Unused padded trials (horizon 8 stored in a length-16 array) were dropped. **107,520 trials.**

## Within-participant battery

These 56 people also completed BART, optimal stopping, and a described-gamble task in counterbalanced order. **`participant` IDs 1–56 are the same person** in every Guan et al. (2020) folder. Join on `participant`. Task order is in `taskOrder.csv` (codes: 1 = stopping, 2 = BART, 3 = bandit, 4 = gambling).

| Task | Folder |
|------|--------|
| Two-armed bandit (this dataset) | [guan-et-al-2020-bandit](../guan-et-al-2020-bandit/) |
| BART | [guan-et-al-2020-bart](../guan-et-al-2020-bart/) |
| Optimal stopping | [guan-et-al-2020-optimal-stopping](../guan-et-al-2020-optimal-stopping/) |
| Described gambles (trials not in this repository) | [guan-et-al-2020-described-gambles](../../risky-gamble-choice/guan-et-al-2020-described-gambles/) |

## Files

- `trials.csv` — one row per pull
- `taskOrder.csv` — order of the four battery tasks

## Columns (`trials.csv`)

- `choiceRight`: 0 = left, 1 = right
- `pLeft`, `pRight`: generating probabilities
- `reward`, `rewardLeft`, `rewardRight`
- `problemOrder`: presentation order of that problem in the condition
