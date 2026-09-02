# gasPrices

Secretary-style **cost minimization** with a gas-station cover story. Collected as a course assignment at UC Irvine (IRB 4286), Winter 2023. Students see a sequence of 10 prices and stop on one. The last station is forced if they have not stopped. The mean and SD of the price distribution are described in the instructions.

Even vs odd student ID assigned high vs low variance. `participant` IDs are anonymous integers, not student IDs, and are **not** a dense 1…N sequence in this file.

## Within-participant tasks

The same people also did bart. **`participant` IDs match across these folders.** Join on `participant`. `relatedTasks.csv` lists, for each person in this file, how many sessions they have in each task. 187 of 196 people here also have bart data. Two people also appear in `fishPrices` (a later year).

| Task | Folder |
|------|--------|
| bart | [bart](../bart/) |
| Gas-station stopping (this dataset, W2023) | [gasPrices](../gasPrices/) |
| Fish-by-weekday stopping (W2024, F2025) | [fishPrices](../fishPrices/) |

These IDs do **not** match Guan et al. (2020) optimal stopping.

| Variance | Generating distribution | People (complete 20 problems) |
|----------|-------------------------|-------------------------------|
| high | N(550, 200²) | 107 |
| low | N(550, 50²) | 89 |
| **Total** | | **196 people, 3,920 problems** |

That year’s survey had no separate research-consent item; these rows are students who finished the assignment.

## Files

- `trials.csv` — one row per problem
- `problemValues.csv` — generating sequences (`high` and `low`)
- `relatedTasks.csv` — session counts for this person on bart, gasPrices, and fishPrices

## Columns (`trials.csv`)

- `quarter` — W2023
- `session` — 1-indexed block if the same person submitted more than once
- `variance` — `high` or `low`
- `problem`, `nPositions` (10)
- `choicePosition` — 1-indexed station
- `cost` — price paid
- `value1` … `value10` — the sequence that person saw

## Citation

This course dataset is unpublished. The same cost-minimization / high-vs-low environment design is studied in:

Guan, M., & Lee, M. D. (2018). The effect of goals and environments on human performance in optimal stopping problems. *Decision*, 5(4), 339–361. [doi:10.1037/dec0000081](https://doi.org/10.1037/dec0000081)

Threshold models of the broader task family:

Lee, M. D. (2006). A hierarchical Bayesian model of human decision-making on an optimal stopping problem. *Cognitive Science*, 30(3), 555–580. [doi:10.1207/s15516709cog0000_69](https://doi.org/10.1207/s15516709cog0000_69)
