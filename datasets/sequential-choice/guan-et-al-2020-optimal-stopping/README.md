# Guan et al. (2020) optimal stopping

Guan, M., Stokes, R., Vandekerckhove, J., & Lee, M. D. (2020). A cognitive modeling analysis of risk in sequential choice tasks. *Judgment and Decision Making*, 15(5), 823–850. [doi:10.1017/s1930297500007956](https://doi.org/10.1017/s1930297500007956)

Secretary-style optimal stopping, 56 people. Four conditions: sequence length 4 or 8 × environment neutral or plentiful. Forty problems per condition. **8,960 problems.**

Related modeling of this task family: Guan & Lee (2018) [doi:10.1037/dec0000081](https://doi.org/10.1037/dec0000081); Lee (2006) [doi:10.1207/s15516709cog0000_69](https://doi.org/10.1207/s15516709cog0000_69).

## Within-participant battery

These 56 people also completed a two-armed bandit, BART, and a described-gamble task in counterbalanced order. **`participant` IDs 1–56 are the same person** in every Guan et al. (2020) folder. Join on `participant`. Task order is in `taskOrder.csv` (codes: 1 = stopping, 2 = BART, 3 = bandit, 4 = gambling).

These IDs do **not** match the `gasPrices` / `fishPrices` samples.

| Task | Folder |
|------|--------|
| Two-armed bandit | [guan-et-al-2020-bandit](../guan-et-al-2020-bandit/) |
| BART | [guan-et-al-2020-bart](../guan-et-al-2020-bart/) |
| Optimal stopping (this dataset) | [guan-et-al-2020-optimal-stopping](../guan-et-al-2020-optimal-stopping/) |
| Described gambles (trials not in this repository) | [guan-et-al-2020-described-gambles](../../risky-gamble-choice/guan-et-al-2020-described-gambles/) |

## Files

- `trials.csv` — one row per problem
- `taskOrder.csv` — order of the four battery tasks

## Columns (`trials.csv`)

- `choicePosition`: 1-indexed stop position
- `value1` … `valueL`: presented sequence (`L` is 4 or 8)
- `problemOrder`: presentation order of that problem in the condition
