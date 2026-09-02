# RAVLT recognition (amyloid groups)

Rey Auditory Verbal Learning Test (RAVLT) **old/new recognition**, 200 people aged over 75. Each person studied 15 words and was tested on 30 words (15 old, 15 new). The file is **person-level signal-detection counts**, not trial-level sequences.

A cerebrospinal-fluid measurement classified 100 people as amyloid-negative and 100 as amyloid-positive. Amyloid positivity is used clinically as a pre-symptomatic marker related to Alzheimer’s disease.

This is the extract used in *Twelve Angry Models* (Lee, in preparation) and in the associated JASP files. The original clinical sample was provided by [Embic](https://embic.us/) (formerly Medical Care Corporation). Demographics and identifiers from the larger clinical table are not included.

## Files

- `counts.csv` — one row per person (200 rows)

| amyloidStatus | People |
|----------------|--------|
| negative | 100 |
| positive | 100 |

## Columns

- `participant` — anonymous integer 1–200 (order is amyloid-negative then amyloid-positive)
- `amyloidStatus` — `negative` or `positive`
- `hits`, `misses` — old (studied) words, out of `nOld` = 15
- `falseAlarms`, `correctRejections` — new words, out of `nNew` = 15

## Citation

Task:

Bean, J. (2011). Rey Auditory Verbal Learning Test, Rey AVLT. In J. S. Kreutzer, J. DeLuca, & B. Caplan (Eds.), *Encyclopedia of Clinical Neuropsychology*. Springer. [doi:10.1007/978-0-387-79948-3_1153](https://doi.org/10.1007/978-0-387-79948-3_1153)

Analyses of this extract:

Lee, M. D. (in preparation). *Twelve Angry Models: Using Cognitive Models in JASP*. Hierarchical two-choice SDT: [OSF amyloidMemorySDT.jasp](https://osf.io/2zu3j); hierarchical two-high-threshold: [OSF amyloidMemoryTHT.jasp](https://osf.io/9h7mr).
