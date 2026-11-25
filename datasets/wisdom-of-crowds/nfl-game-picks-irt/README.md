# NFL game picks for topic-expertise IRT

Binary “which team wins?” questions in the same shape as Bennett, Benjamin, Mistry, and Steyvers (2018): one row per question, one row per person × question, `option1` / `option2`, and `correct` when a winner is known.

This folder is the 2017 Mechanical Turk panel.

| Panel | People | Games | Trials |
|---|---:|---:|---:|
| Mechanical Turk participants, 2017 | 1,700 | 257 | 25,700 |

Participants are Lee, Danileiko, and Vi (2018): 100 people each week, each person one week only. Their `participant` numbers are 1–1,700, the same ids as that Danileiko file.

Commentators are not in this folder. ESPN 2015–2017 and the Montgomery and Lee 2017 experts are one database in [`expert-nfl-picks/`](../expert-nfl-picks/), with one id per person. Those ids are not the Mechanical Turk numbers.

These novice trials are kept because they carry division and conference columns. The Danileiko `trials.csv` has `participant`, `week`, `game`, `option1`, `option2`, `prediction`, `confidence`, `meta`, `truth`, and `correct`, and not those topic columns.

## gameId

`gameId` is `{season}-{away}@{home}`, using stable franchise abbreviations (`LAC` and `LAR`; `WAS` for the Washington franchise). Option 1 is always the home team and option 2 is always the away team. `correctOption` is 1 or 2. `choice` on a trial uses the same coding.

The same 2017 `gameId` is used in [`expert-nfl-picks/`](../expert-nfl-picks/). `source` here is `participant`.

`2017-TB@MIA` was on the week-1 slate, postponed, and played in week 11. Participants were asked again in week 11 (100 people each time; 200 trials). Commentators picked it only in week 11. `askedWeek` is when the pick was made. `playedWeek` is when the game was played.

## Topics

`topic` is not the week. Week is only the item bank (`week01` … `week17`), because that is who saw which games.

A game has two teams, so division and conference are coded three ways. Use `topic` for a single factor. Use the other two columns if you want a pure partition.

- `topic` uses the division when both teams are in it (`AFC East`, …, `NFC West`: 12 games in a 256-game season). Otherwise it uses the conference matchup: `AFC` or `NFC` for a same-conference game that is not divisional (48 games each), or `Interconference` (64 games). The participant question file has 65 `Interconference` rows because `2017-TB@MIA` was asked twice. Divisional games are not also labeled with the bare conference, so `AFC` means cross-division AFC games only.
- `divisionTopic` is that shared division, or `Cross-division` for every other game.
- `conferenceTopic` is `AFC`, `NFC`, or `Interconference`, and it does include divisional games.
- `scopeTopic` is `Divisional`, `Conference`, or `Interconference`: the type of game, not which division.

Home and away division and conference are also on each question, if a model should let one game load on both teams’ divisions. The same columns are on the commentator trials in `expert-nfl-picks/`, copied from this coding by `gameId`.

Other groupings that look like topics but are not used as `topic`:

- Early versus late season is a coarsening of week. The record is more informative later, which is already what a difficulty parameter picks up.
- Toss-up versus mismatch, from the teams’ records, is closer to difficulty than to a knowledge domain. Entering wins and losses are columns (`homeWins`, `homeLosses`, `awayWins`, `awayLosses`) as of `askedWeek`. Ties are not counted as wins or losses.
- Dome versus outdoor, prime time, and a short week are plausible, and they are not in these archives.
- Home versus away is a cue, not a domain of knowledge. It is fixed by option 1 being home.

## Outcome

`correct` is 1 when `choice` matches the final score, and blank when the game has no score. There is no `difficultyRating`. Participants have `confidence` (1–5) and `meta` (judged proportion of others who agree). `knowledge` on the participant file is the self-rating from the survey.

2017 winners are the final scores in `nfl2017-regular-season.csv`. The published Mechanical Turk `truth` flag disagrees with the final score on 7 games; these files follow the final score:

`2017-HOU@CIN`, `2017-SF@IND`, `2017-TB@NO`, `2017-WAS@SEA`, `2017-ARI@HOU`, `2017-TEN@SF`, `2017-NE@PIT`.

## Files

- `questions-participants-2017.csv`
- `trials-participants-2017.csv`
- `participants-participants-2017.csv`
- `itemBank-participants-2017.csv`
- `nfl2017-regular-season.csv` — final scores used for `correct`

Rebuild the novice panel with `scripts/build_nfl_game_picks_irt.py`. That script does not write commentator files.

## Citation

Lee, M. D., Danileiko, I., & Vi, J. (2018). Testing the ability of the surprisingly popular method to predict NFL games. *Judgment and Decision Making*, 13, 322–333.
