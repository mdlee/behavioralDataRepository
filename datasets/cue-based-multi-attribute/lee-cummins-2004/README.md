# Lee & Cummins (2004) cue-based choice

Lee, M. D., & Cummins, T. D. R. (2004). Evidence accumulation in decision making: Unifying the “take the best” and “rational” models. *Psychonomic Bulletin & Review*, 11, 343–352.

People choose which of two “gas” stimuli is better, using six cues. Training has feedback (accuracy); testing has confidence. Critical test pairs are listed below (original paper Table 1 / stimulus codes).

Experiment 2 used a different visual display and is only briefly reported in the paper. Participant 18 has no Experiment 1 training file (`alldec` empty in the source).

Within each experiment, **`participant` IDs match across the training and testing files** (same people). Experiment 1 and Experiment 2 used different people; IDs restart at 1 in Experiment 2 and must not be joined across experiments.

## Files

| File | People | Rows |
|------|--------|------|
| `experiment1Training.csv` | 39 | 4,641 |
| `experiment1Testing.csv` | 40 | 200 |
| `experiment2Training.csv` | 20 | 2,380 |
| `experiment2Testing.csv` | 20 | 120 |

## Columns

- `decision`: −1 left, +1 right
- `leftStimulus`, `rightStimulus`: stimulus IDs (cue patterns in the paper)
- `rt`
- training `accuracy`: −1 incorrect, +1 correct
- testing `confidence`: 5-point scale

## Critical test pairs

- 17 = {Cue 1, Cue 6} vs 18 = {Cue 2, Cue 3}
- 20 = {Cue 1, Cue 5} vs 18 = {Cue 2, Cue 3}
- 23 = {Cue 1, Cue 5, Cue 6} vs 24 = {Cue 2, Cue 3, Cue 4}
- 25 = {Cue 1, Cue 4, Cue 5} vs 24 = {Cue 2, Cue 3, Cue 4}
- 28 = {Cue 1, Cue 4, Cue 5, Cue 6} vs 29 = {Cue 2, Cue 3, Cue 4, Cue 5}
