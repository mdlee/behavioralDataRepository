# Lee & Stark (2023) mnemonic similarity task

Lee, M. D., & Stark, C. E. L. (2023). Bayesian modeling of the Mnemonic Similarity Task using multinomial processing trees. *Behaviormetrika*, 50, 517–539. [doi:10.1007/s41237-023-00193-3](https://doi.org/10.1007/s41237-023-00193-3); [github.com/mdlee/mpt4mst](https://github.com/mdlee/mpt4mst)

21 people completed both old/new and old/similar/new **study–test** MST. Each task: 128 studied images, then 192 test images (64 old, 64 new, 64 lure). Lures have five mnemonic-similarity bins (1 = most similar). **`participant` IDs match across the two files.**

| File | Responses | People | Trials |
|------|-----------|--------|--------|
| `studyTestON.csv` | old / new | 21 | 4,032 |
| `studyTestOSN.csv` | old / similar / new | 21 | 4,032 |

Stimulus images are not included. `stimulus` is a numeric item code.

## Columns

- `itemType`: `target`, `lure`, or `foil`
- `lureBin`: 1–5
- `truth` / `decision` for old/similar/new: 1 = old, 2 = new, 3 = similar
- `truth` / `decision` for old/new: 1 = old, 2 = new. Lures are still `itemType = lure`; the correct response is **new**
- Missing responses: empty `decision`, `decisionLabel`, and `correct`
- `studyPosition`, `gap` — study-list position and study–test gap
