# Lee, Mistry, & Menon (2022) 2-back

Lee, M. D., Mistry, P. K., & Menon, V. (2022). A multinomial processing tree model of the 2-back working memory task. *Computational Brain & Behavior*. [osf.io/esxhf](https://osf.io/esxhf/)

Two human 2-back extracts used in that paper. Simulated data from the OSF project are not included. Original Human Connectome Project identifiers were replaced with anonymous `participant` 1…1091.

| File | People | Trials | Source |
|------|--------|--------|--------|
| `stelterDegner.csv` | 52 | 3,520 | Stelter & Degner (2018), face 2-back |
| `humanConnectome.csv` | 1,091 | 82,871 | HCP n-back (blocks with a recorded decision) |

IDs do **not** match across the two files.

## Columns (trial files)

- `block`, `trial`
- `stimulus` — item code
- `trialType` — 1–4 (see the paper for target / lure coding)
- `decision`, `truth` — 0/1
- `face` — Stelter–Degner only

`humanConnectomeParticipants.csv` has Penn matrices, list-sort, and card-sort scores for the HCP sample.
