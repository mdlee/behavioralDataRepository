# Stillman, Krajbich, & Ferguson (2020) mixed gambles

Stillman, P. E., Krajbich, I., & Ferguson, M. J. (2020). Using dynamic monitoring of choices to predict and understand risk preferences. *Proceedings of the National Academy of Sciences*, 117(50), 31738–31747. https://doi.org/10.1073/pnas.2010056117

On each trial the participant accepts a 50/50 gamble (gain and loss, or gain only) or takes a certain amount (usually $0). Data are from the three studies in that paper (third-party; not collected in the Lee lab). Subject IDs may overlap across studies; treat study × subject as the unit of analysis.

## Files

| File | Contents |
|------|----------|
| `trials.csv` | All three studies, gain–loss and gain-only (140,180 trials; 578 unique `subject` values) |
| `study1GainLoss.csv` | Study 1 gain–loss only (148 people × 165 trials = 24,420) |

## Columns (`trials.csv`)

- `study`: `study_1`, `study_2`, `study_3`
- `subject`, `trial`
- `gambleType`: `gain_loss` or `gain_only`
- `gain`, `loss`, `cert`: dollar amounts
- `tookGamble`: 1 = took the gamble, 0 = took the certain amount
