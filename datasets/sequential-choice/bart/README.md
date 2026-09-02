# bart

Balloon Analog Risk Task collected as a course assignment at UC Irvine (IRB 4286). Twenty balloons. Burst points follow a fixed generating sequence: 11, 9, 8, 8, 7, 6, 6, 5, 5, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1. Domain-Specific Risk-Taking (DOSPERT) risk-perception items were collected in the same session.

`participant` IDs are anonymous integers, not student IDs, and are **not** a dense 1…N sequence in this file. The same person keeps one ID across quarters and across `gasPrices` and `fishPrices`; `quarter` and `session` distinguish blocks.

## Within-participant tasks

The same people also did a cost-minimizing stopping task (gas-station cover story in W2023; fish-by-weekday in W2024 and F2025). **`participant` IDs match across these folders.** Join on `participant`. `relatedTasks.csv` lists, for each person in this file, how many sessions they have in each task. 187 people also have `gasPrices` data; 317 also have `fishPrices` data. Two people have both stopping cover stories (more than one year).

| Task | Folder |
|------|--------|
| bart (this dataset) | [bart](../bart/) |
| Gas-station stopping (W2023) | [gasPrices](../gasPrices/) |
| Fish-by-weekday stopping (W2024, F2025) | [fishPrices](../fishPrices/) |

These IDs do **not** match the Guan et al. (2020) BART sample.

| Quarter | Sessions | Notes |
|---------|----------|-------|
| W2023 | 212 | Assignment completers; that year’s survey had no separate research-consent item |
| W2024 | 178 | Research-consent filter applied |
| F2025 | 167 | Research-consent filter applied |
| **Total** | **557 sessions, 543 people** | 11,140 balloon trials |

One person appears in two quarters; 13 people have two sessions in the same quarter.

## Files

- `trials.csv` — one row per balloon
- `participants.csv` — one row per session: adjusted pumps, cash/burst counts, DOSPERT subscale means
- `relatedTasks.csv` — session counts for this person on bart, gasPrices, and fishPrices

## Columns (`trials.csv`)

- `quarter`, `session`
- `problem` — balloon number in the generating sequence
- `presentationOrder` — display order when available (missing for W2024)
- `burstPoint` — generating pop point for that problem
- `nPumps` — pumps before cash or burst
- `burst` — 1 if the balloon popped

## Citation

Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., Strong, D. R., & Brown, R. A. (2002). Evaluation of a behavioral measure of risk taking: The Balloon Analogue Risk Task (BART). *Journal of Experimental Psychology: Applied*, 8(2), 75–84. [doi:10.1037/1076-898X.8.2.75](https://doi.org/10.1037/1076-898X.8.2.75)

A published within-subject BART (with bandit and optimal stopping; **different people, different IDs**) is in Guan, Stokes, Vandekerckhove, & Lee (2020): [doi:10.1017/s1930297500007956](https://doi.org/10.1017/s1930297500007956)

DOSPERT subscales: Blais, A.-R., & Weber, E. U. (2006). A Domain-Specific Risk-Taking (DOSPERT) scale for adult populations. *Judgment and Decision Making*, 1(1), 33–47. [doi:10.1017/S1930297500000338](https://doi.org/10.1017/S1930297500000338)
