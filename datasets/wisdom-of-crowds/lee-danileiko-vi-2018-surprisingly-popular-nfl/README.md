# Lee, Danileiko, & Vi (2018) surprisingly popular NFL

Lee, M. D., Danileiko, I., & Vi, J. (2018). Testing the ability of the surprisingly popular method to predict NFL games. *Judgment and Decision Making*, 13(4), 322–333. [doi:10.1017/s1930297500009207](https://doi.org/10.1017/s1930297500009207) · [OSF `3kjmu`](https://osf.io/3kjmu/)

Mechanical Turk respondents predicted weekly NFL games in the 2017 season. For each game they chose a winner, rated confidence, and estimated what fraction of others would agree (the meta-judgment used by the surprisingly popular algorithm). **1,700 people**, **25,700 game-level predictions** across weeks 1–17 (100 people × 16 or 17 games per week, depending on the slate).

`participant` IDs are unique across weeks (separate MTurk samples each week). Age and gender from the original surveys are not exported.

## Files

- `trials.csv` — one row per person × game
- `participants.csv` — one row per person: `week`, self-rated `knowledge`

## Columns (`trials.csv`)

- `week`, `game`
- `option1`, `option2` — team names (option1 is the first team listed in the survey)
- `prediction` — `1` = option1, `2` = option2
- `confidence` — confidence that the pick is correct
- `meta` — judged proportion of others who agree with the pick
- `truth` — `1` = option1 won, `0` = option2 won; blank if the game was not scored in the archive
- `correct` — `1`/`0` when `truth` is available
