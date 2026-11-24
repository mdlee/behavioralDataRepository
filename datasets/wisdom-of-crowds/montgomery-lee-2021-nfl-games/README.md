# Montgomery & Lee (2021) NFL games

Game-level recode of the expert picks in Montgomery and Lee (2021), for pairing with Lee, Danileiko, and Vi (2018). The original heuristic files are unchanged in [`montgomery-lee-2021-nfl/`](../montgomery-lee-2021-nfl/).

Montgomery, L. E., & Lee, M. D. (2021). Expert and novice sensitivity to environmental regularities in predicting NFL games. *Judgment and Decision Making*, 16, 1370–1391. [osf.io/3px5k](https://osf.io/3px5k/)

Lee, M. D., Danileiko, I., & Vi, J. (2018). Testing the ability of the surprisingly popular method to predict NFL games. *Judgment and Decision Making*, 13(4), 322–333.

**71 experts**, **256 games**, **18,156 trials**, 2017 regular season only. Novices are not in this folder.

## Files

- `trials.csv` — one row per expert × game
- `participants.csv` — one row per expert: `participant`, `panel`, `season`, `name`

`name` is the public commentator or outlet name from the scrape. Participant numbers are the same 1–71 ids as `expertPredictions.csv` in the heuristic folder. “Pickwatch Fan Picks” is not included; the published set of 71 already drops that row.

## Columns (`trials.csv`)

`participant,week,game,option1,option2,prediction,confidence,meta,truth,correct,gameId,montgomeryGame`

Same order as the Danileiko `trials.csv`, then two extra columns.

- `option1` is the home team and `option2` is the away team. For every 2017 game this is also the order in the Danileiko survey.
- `week` and `game` are the Danileiko within-week slot for that matchup, so those two columns join the Danileiko file. They are not the season-long game id in the heuristic file.
- `prediction` — `1` = option1, `2` = option2
- `confidence`, `meta` — present so the file stacks with Danileiko. The expert scrape has neither judgment, so both are blank. Nothing was filled in.
- `truth` — `1` = option1 won, `0` = option2 won. No ties in this slate, so `truth` is never blank.
- `correct` — `1` if the picked team won the final score, `0` otherwise
- `gameId` — `2017-{away}@{home}`, same abbreviations as [`nfl-game-picks-irt/`](../nfl-game-picks-irt/) (`LAC`, `LAR`, `WAS`). All 256 ids match the 2017 expert questions in that folder.
- `montgomeryGame` — season-long id (1–256) in `expertPredictions.csv`

## Reconstruction

The heuristic export records agreement with a cue, not a team. The team pick is recovered from the game-level scrape that file was built from (`home`, `away`, `predwinner`, `predhome`, `outcome`).

1. Use `predwinner` when, after trimming space and ignoring case, it is exactly one of the two teams in that game.
2. A fixed alias list maps a misspelling onto a team only when the corrected name is one of those two teams: “New Yorks Giants”, “Bufallo Bills”, “Arizona Cardinas”, “Arizona Carindlas”, “Seattle Sawhawks”, “Seattle Seahawls”, “Washington Football”, “The Washington Redskins”.
3. If the string names neither team, use `predhome`: `1` is the scrape’s home team and `0` is the away team. That is the published home-team heuristic. It recovers one row whose winner string is a third team (Zac Robinson, week 13, Arizona vs Los Angeles Rams, string “New York Giants”, `predhome` 0, so the Rams).

Every one of the 18,099 published home-team rows picks the same team under this rule.

The winner is the final score in `nfl-game-picks-irt/nfl2017-regular-season.csv`, not the scrape’s `outcome` string. Checked for all 256 games: `truth` is 1 exactly when option1’s score is higher.

### Not exported

- **1 pick** could not be turned into a team. Lisa Kerney, week 12, Los Angeles Chargers at Dallas Cowboys: `predwinner` is “K”, and every heuristic flag is missing.
- **19 person-games** have no row in the scrape (71 × 256 = 18,176 possible; 18,156 exported). Eight of those gaps are the same week-15 game.

### Home and away label

Week 14, Buffalo vs Indianapolis, is stored in the scrape with Indianapolis as home. The final score and `nfl-game-picks-irt` have Buffalo home, 13–7, `2017-IND@BUF`. This file uses that `gameId`. The pick is the named team, so the swapped label does not reverse the choice. Danileiko lists Buffalo as option1.

### Where the scrape’s outcome string disagrees with the score

`truth` and `correct` follow the score. On these eight games the scrape names the other team as the winner. The score column is home, then away.

| gameId | Score winner | Home–away |
|---|---|---|
| `2017-ARI@HOU` | Houston Texans | 31–21 |
| `2017-CIN@JAX` | Jacksonville Jaguars | 23–7 |
| `2017-CLE@LAC` | Los Angeles Chargers | 19–10 |
| `2017-DEN@OAK` | Oakland Raiders | 21–14 |
| `2017-LAC@OAK` | Los Angeles Chargers | 16–17 |
| `2017-NYG@ARI` | Arizona Cardinals | 23–0 |
| `2017-NYG@WAS` | Washington Redskins | 20–10 |
| `2017-SEA@LAR` | Seattle Seahawks | 10–16 |

The published heuristic `truth` follows the scrape, so it disagrees with this file on those eight games. The pick itself still matches.

### Danileiko `truth` flag

Danileiko’s published `truth` disagrees with the final score on seven games. This file follows the score, as `nfl-game-picks-irt` does:

`2017-HOU@CIN`, `2017-SF@IND`, `2017-TB@NO`, `2017-WAS@SEA`, `2017-ARI@HOU`, `2017-TEN@SF`, `2017-NE@PIT`.

## Novices

The 1,700 Montgomery novices are the Danileiko 2017 Mechanical Turk sample. All 25,600 novice team picks match that file on participant, week, and the two teams. Danileiko has 100 further trials: the week-1 asking of Miami vs Tampa Bay (week 1, game 4, `truth` blank), which was postponed and is not in the Montgomery novice table. Experts picked that game only in week 11 (game 2, Buccaneers 30, Dolphins 20). Those novice trials are not copied here. Use [`lee-danileiko-vi-2018-surprisingly-popular-nfl/trials.csv`](../lee-danileiko-vi-2018-surprisingly-popular-nfl/trials.csv).

Rebuild with `scripts/build_montgomery_lee_2021_nfl_games.py`.
