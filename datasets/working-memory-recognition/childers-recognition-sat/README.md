# Childers et al. word recognition SAT

Word old/new recognition with speed vs accuracy instructions. Source: Childers et al. OSF project https://osf.io/bsvqe/. Exported from the raw `.data` files.

36 test words per block: 18 old (9 studied three times, 9 studied once) and 18 new. High / low / very-low word frequency. Blocks alternate speed vs accuracy.

## Files

- `trials.csv` — 131,760 rows
- `source_readme.txt` — original column notes from the OSF dump

## Counts

- 41 older adults, 39 younger adults
- 129 trials with `decision = no_response`

## Columns

- `presentation`: `new`, `studied_once`, `studied_three_times`
- `wordFrequency`: `high`, `low`, `very_low`
- `instruction`: `speed` or `accuracy`
- `decision`: `old`, `new`, or `no_response` (raw keycodes 1 = studied, 2 = new)
- `truth`: `old` if studied, `new` otherwise
- `correct`: empty on no-response
- `rtMs`
