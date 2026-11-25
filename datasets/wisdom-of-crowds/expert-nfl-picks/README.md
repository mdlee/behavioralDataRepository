# Expert NFL picks

Media commentators, 2015–2017, one database.

**82 commentators**, **768 games**, **24,047 trials**.

| Season | Trials | Where the picks come from |
|---|---:|---|
| 2015 | 3,328 | ESPN panel (13 people) |
| 2016 | 2,304 | ESPN panel (9 people) |
| 2017 | 18,415 | ESPN panel plus the Montgomery and Lee 71, after de-duplication |

`participant` is one integer per person, assigned by sorting the name. The same person keeps that id in every season, including seasons they skip. ESPN files stored a surname. That surname is the Montgomery and Lee full name when exactly one of the 71 ends with it: Matt Bowen, Mike Clay, Mike Golic, Dan Graziano, K.C. Joyner, Lisa Kerney, Mina Kimes, Louis Riddick, Kevin Seifert, Seth Wickersham. Caplan, Hoge, Jaworski, Allen, Carter, Ditka, Jackson, Johnson, Mortensen, and Schlereth are not in the 71, so the name stays the surname. Wingo is the 2017 ESPN panel only. Jonathan Jones and Lindsay H. Jones share a surname and stay two people.

People in more than one season:

| id | Name | Seasons |
|---:|---|---|
| 9 | Caplan | 2015, 2016 |
| 14 | Dan Graziano | 2016, 2017 |
| 23 | Hoge | 2015, 2016 |
| 29 | Jaworski | 2015, 2016 |
| 42 | K.C. Joyner | 2015, 2016, 2017 |
| 44 | Kevin Seifert | 2016, 2017 |
| 51 | Matt Bowen | 2016, 2017 |
| 56 | Mike Golic | 2015, 2016, 2017 |
| 76 | Seth Wickersham | 2015, 2016, 2017 |

## Files

- `participants.csv` — one row per commentator: `participant`, `name`, `season2015`, `season2016`, `season2017`, `seasons`
- `questions.csv` — one row per game. `questionId` is unique: 2015 is 1–256, 2016 is 257–512, 2017 is 513–768, in the same within-year order as the old per-year question files. `gameId` is unchanged.
- `trials.csv` — one row per commentator × game, in the same columns as the IRT expert trials, plus home and away conference and division. `experiment` is the season of that trial.
- `itemBank.csv` — `season` bank, one row per game, with the same `questionId` and `gameId` as `questions.csv`

`gameId` is `{season}-{away}@{home}` (`LAC`, `LAR`, and `WAS` in every season). Option 1 is the home team and option 2 is the away team. `choice` uses that coding. `correct` is 1 or 0, and blank when the game tied. 2016 ties are `2016-SEA@ARI` and `2016-WAS@CIN`.

## Topics

Topic columns are copied from the IRT question rows on `gameId`. They are not a second coding.

`topicId`, `topic`, `divisionTopicId`, `divisionTopic`, `conferenceTopicId`, `conferenceTopic`, `scopeTopicId`, `scopeTopic`, `homeConference`, `homeDivision`, `awayConference`, `awayDivision`

`topic` is the shared division when both teams are in it, and otherwise `AFC`, `NFC`, or `Interconference`. `divisionTopic` is that division or `Cross-division`. `conferenceTopic` is `AFC`, `NFC`, or `Interconference` and includes divisional games. `scopeTopic` is `Divisional`, `Conference`, or `Interconference`.

## Citation

Montgomery, L. E., & Lee, M. D. (2021). Expert and novice sensitivity to environmental regularities in predicting NFL games. *Judgment and Decision Making*, 16, 1370–1391. ESPN commentator names are public.

Lee, M. D., Danileiko, I., & Vi, J. (2018). Testing the ability of the surprisingly popular method to predict NFL games. *Judgment and Decision Making*, 13, 322–333. The 2017 game ids match that survey.
