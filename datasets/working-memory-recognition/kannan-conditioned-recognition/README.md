# Kannan conditioned recognition

Vijayakumar, K. S. O. M. (2024). *The memory remains: Monetary and social rewards in retroactive enhancement of memory* (Doctoral dissertation). University of California, Irvine. [escholarship.org/uc/item/5vj0f34g](https://escholarship.org/uc/item/5vj0f34g)

Old/new recognition of words with confidence, plus a condition type (`condType`) and phase. 44 people, 10,560 trials.

This extract is used in *Twelve Angry Models* (Lee, in preparation). Multiple-choice SDT: [OSF conditionedRecognition.jasp](https://osf.io/xfbtq); two-choice SDT: [OSF conditionedRecognitionTwoChoice.jasp](https://osf.io/gpvd2/files/ztkqx).

## Files

- `trials.csv`

## Columns

- `subject`, `cond`, `stimulus` (word)
- `recall`: 1 or 2 (old/new response in the original coding)
- `confidence` 1–11
- `presented`: 1 = studied, 0 = new
- `phase` 0–3
- `condType` e.g. `money_animal`
