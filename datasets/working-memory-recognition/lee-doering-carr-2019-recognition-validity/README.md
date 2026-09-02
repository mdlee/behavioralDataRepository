# Lee, Doering, & Carr (2019) recognition validity

Lee, M. D., Doering, S., & Carr, A. (2019). A model for understanding recognition validity. *Computational Brain & Behavior*, 2, 49–63. [osf.io/ftj3d](https://osf.io/ftj3d/)

Paired items: which name is recognized, and (when collected) which item is judged higher on the domain criterion. **270 people** in a shared `participant` ID space; not everyone did every domain.

| Domain | People | Pairs |
|--------|--------|-------|
| actors | 198 | 9,900 |
| athletes | 198 | 9,504 |
| cities | 198 | 9,900 |
| companies | 198 | 9,900 |
| hotels | 109 | 2,834 |
| March Madness 2016 | 98 | 2,744 |
| airplanes | 161 | 12,075 |

## Files

Each domain has `*Stimuli.csv` (item name and criterion) and `*Trials.csv`.

## Columns (`*Trials.csv`)

- `itemA`, `itemB` — 1-indexed into that domain’s stimulus file
- `recognizedA`, `recognizedB` — `0`/`1` (`2` = unsure, rare)
- `aLarger` — `1` if A’s criterion is strictly larger
- `choiceA` — present for hotels and airplanes only (`1` = chose A, `0` = chose B). Other domains in the source dump are recognition + criterion, without a stored inference choice.
