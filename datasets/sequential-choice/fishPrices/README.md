# unpublished fish prices

Secretary-style **cost minimization** with a fish-by-weekday cover story. Collected as a course assignment at UC Irvine (IRB 4286). Students see a sequence of seven daily prices (Monday–Sunday) and stop on one. Sunday is forced if they have not stopped. The mean and SD of the price distribution are described in the instructions.

Even vs odd student ID assigned high vs low variance. W2024 and F2025 used the same task. People who appear in more than one quarter (or who submitted twice) share one `participant` ID; `quarter` and `session` distinguish blocks. IDs are anonymous integers, not student IDs, and are **not** a dense 1…N sequence in this file.

## Within-participant tasks

The same people also did bart. **`participant` IDs match across these folders.** Join on `participant`. `relatedTasks.csv` lists, for each person in this file, how many sessions they have in each task. 317 of 344 people here also have bart data. Two people also appear in `gasPrices` (an earlier year).

| Task | Folder |
|------|--------|
| unpublished bart | [bart](../bart/) |
| unpublished gas prices (W2023) | [gasPrices](../gasPrices/) |
| unpublished fish prices (this dataset, W2024 and F2025) | [fishPrices](../fishPrices/) |

These IDs do **not** match Guan et al. (2020) optimal stopping.

| Quarter | Variance | Generating distribution | Sessions (complete 20 problems) |
|---------|----------|-------------------------|--------------------------------|
| W2024 | high | N(500, 200²) | 105 |
| W2024 | low | N(500, 50²) | 73 |
| F2025 | high | N(500, 200²), problems shuffled | 106 |
| F2025 | low | N(500, 50²) | 63 |
| **Total** | | | **347 sessions, 344 people, 6,940 problems** |

Only participants who consented to research use are included. No one in this extract completed both W2024 and F2025; three people have two sessions in the same quarter.

F2025 high-variance problems were presented in shuffled order (see `problemValues.csv`, stimulus set `high_F2025`).

## Files

- `trials.csv` — one row per problem
- `problemValues.csv` — generating sequences
- `relatedTasks.csv` — session counts for this person on bart, gasPrices, and fishPrices

## Columns (`trials.csv`)

- `quarter` — W2024 or F2025
- `session` — 1-indexed block for that participant
- `variance` — `high` or `low`
- `problem`, `nPositions` (7)
- `choicePosition` — 1-indexed day (1 = Monday)
- `cost` — price paid
- `value1` … `value7` — the sequence that person saw

## Citation

This course dataset is unpublished. The same cost-minimization / high-vs-low environment design is studied in:

Guan, M., & Lee, M. D. (2018). The effect of goals and environments on human performance in optimal stopping problems. *Decision*, 5(4), 339–361. [doi:10.1037/dec0000081](https://doi.org/10.1037/dec0000081)

Threshold models of the broader task family:

Lee, M. D. (2006). A hierarchical Bayesian model of human decision-making on an optimal stopping problem. *Cognitive Science*, 30(3), 555–580. [doi:10.1207/s15516709cog0000_69](https://doi.org/10.1207/s15516709cog0000_69)
