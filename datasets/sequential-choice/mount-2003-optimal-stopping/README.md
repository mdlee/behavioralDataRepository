# Mount (2003) optimal stopping

Mount, C. E. (2003). *Individual differences in the secretary problem.* Unpublished honours thesis, University of Adelaide.

50 people, three problem lengths (5, 10, 20) in a within-subject design, 40 problems each. Sequences are values on 0–100; the participant stops on one position.

## Files

- `trials.csv` — 6,000 rows
- `participants.csv` — Raven’s Advanced Progressive Matrices score

## Columns (`trials.csv`)

- `participant`, `problemLength`, `problem`
- `choicePosition` 1-indexed
- `confidence` (9-point scale in the thesis materials)
- `presentationOrder`
- `value1` … `valueL` — the sequence (shared across participants for a given problem)
