# Guan et al. (2020) Balloon Analog Risk Task

Guan, M., Stokes, R., Vandekerckhove, J., & Lee, M. D. (2020). A cognitive modeling analysis of risk in sequential choice tasks. *Judgment and Decision Making*, 15(5), 823–850. [doi:10.1017/s1930297500007956](https://doi.org/10.1017/s1930297500007956)

Balloon Analog Risk Task, 56 people. Two burst probabilities (.1 and .2), 50 balloons each. **5,600 balloons.**

The original BART method paper is Lejuez et al. (2002): [doi:10.1037/1076-898X.8.2.75](https://doi.org/10.1037/1076-898X.8.2.75).

## Within-participant battery

These 56 people also completed a two-armed bandit, optimal stopping, and a described-gamble task in counterbalanced order. **`participant` IDs 1–56 are the same person** in every Guan et al. (2020) folder. Join on `participant`. Task order is in `taskOrder.csv` (codes: 1 = stopping, 2 = BART, 3 = bandit, 4 = gambling).

These IDs do **not** match the `bart` sample.

| Task | Folder |
|------|--------|
| Two-armed bandit | [guan-et-al-2020-bandit](../guan-et-al-2020-bandit/) |
| BART (this dataset) | [guan-et-al-2020-bart](../guan-et-al-2020-bart/) |
| Optimal stopping | [guan-et-al-2020-optimal-stopping](../guan-et-al-2020-optimal-stopping/) |
| Described gambles (trials not in this repository) | [guan-et-al-2020-described-gambles](../../risky-gamble-choice/guan-et-al-2020-described-gambles/) |

## Files

- `trials.csv` — one row per balloon
- `taskOrder.csv` — order of the four battery tasks

## Columns (`trials.csv`)

- `burstPoint`: pump at which the balloon would burst
- `burst`: 0 = cashed, 1 = balloon burst
- `nPumps`
- `problemOrder`: presentation order of that balloon in the condition
