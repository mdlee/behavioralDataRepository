# Guan et al. (2020) described gambles

Guan, M., Stokes, R., Vandekerckhove, J., & Lee, M. D. (2020). A cognitive modeling analysis of risk in sequential choice tasks. *Judgment and Decision Making*, 15(5), 823–850. [doi:10.1017/s1930297500007956](https://doi.org/10.1017/s1930297500007956)

Described left-vs-right gambles, 56 people, two conditions (gains / losses), 40 problems per condition. Each option had a probability and a payoff.

**Trial-level choices for this task are not in the source archive used to build this repository.** `taskOrder.csv` is included so the 56 people can still be aligned with the other battery tasks.

## Within-participant battery

These 56 people also completed a two-armed bandit, BART, and optimal stopping in counterbalanced order. **`participant` IDs 1–56 are the same person** in every Guan et al. (2020) folder. Join on `participant`. Task-order codes: 1 = stopping, 2 = BART, 3 = bandit, 4 = gambling.

| Task | Folder |
|------|--------|
| Two-armed bandit | [guan-et-al-2020-bandit](../../sequential-choice/guan-et-al-2020-bandit/) |
| BART | [guan-et-al-2020-bart](../../sequential-choice/guan-et-al-2020-bart/) |
| Optimal stopping | [guan-et-al-2020-optimal-stopping](../../sequential-choice/guan-et-al-2020-optimal-stopping/) |
| Described gambles (this dataset; trials missing) | [guan-et-al-2020-described-gambles](../guan-et-al-2020-described-gambles/) |

## Files

- `taskOrder.csv` — order of the four battery tasks
