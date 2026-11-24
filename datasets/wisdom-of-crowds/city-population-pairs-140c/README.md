# City population pairs (Cognitive Science 140C)

Unpublished coursework from Cognitive Science 140C at the University of California, Irvine. Each student received one monthly workbook and, for every city pair, marked which city has the larger population (1 or 2) and whether they recognized each city (1 = yes, 0 = no). This release keeps the trials that pass the course parser's checks and lays them out in the same person–item style as Bennett, Benjamin, Mistry, and Steyvers (2018).

The assignment is the classic two-city population comparison used to teach the recognition heuristic. These spreadsheets are course submissions, not a published experiment. Fall 2017 is excluded: that term replaced cities with hotel chains and airlines.

## Task

Four countries are the topics (the expertise domains). A person may know one country better than another.

| Topic | Cities in the course list | Pairs on each sheet |
|-------|---------------------------|---------------------|
| German Cities | 83 | 41 |
| US Cities | 74 | 37 |
| Italian Cities | 49 used (149 in the full list) | 24 |
| UK Cities | 66 | 33 |

A complete workbook has 135 pairs (41 + 37 + 24 + 33). Pairings are a matching: each selected city appears once on that sheet. One city is left out of the German list (83 cities, 82 used) and one is left out of the 49 Italian cities (48 used). US and UK lists are fully paired.

There are 12 monthly matchings (Jan–Dec). Everyone with the same term and month saw the same pairs, in the same order. The random seed changes by year, so a `questionId` in one term is not the same item as that number in another term or another month. Match items by the two city names. The seeds do not make the pairings disjoint: the release contains 4,526 distinct unordered city pairs, 2,527 of them appear in more than one term, and 727 appear in more than one month of the same term.

## Anonymity

`participant` is an anonymous integer, unique across the whole release, starting at 1. Numbers run in term order (2012S, 2012F, 2013F, 2014F, 2015F, 2016F), then month, then filename order so the export can be regenerated. Filenames, UCINetIDs, and student names are not in any file.

Each workbook that yielded at least one valid country sheet is a separate participant. The same student can appear more than once if they turned in more than one file. Those duplicates cannot be removed without using the filenames as identity, so possible resubmissions are left in.

## Files

- `questions.csv` — one row per pair a student could be shown (term × month × country × pair)
- `itemBank.csv` — the same pairs, as the monthly bank joined to `questionId`
- `trials.csv` — one row per person × pair on each country sheet that passed the validity checks
- `participants.csv` — one row per workbook

`itemBank` is the month (Jan–Dec). That is the shared item set, analogous to an easy/hard bank. The month is not a topic. `topic` is the country. `design` is `assigned` (the month's pairs were assigned, not chosen). `condition` is `140C`. There is no difficulty rating. Recognition is stored as `recognize1` and `recognize2`, not as a difficulty score.

### `questions.csv`

| Column | Meaning |
|--------|---------|
| `questionId` | 1..N in this dataset |
| `term` | 2012S, 2012F, 2013F, 2014F, 2015F, or 2016F |
| `itemBank` | Month of the matching |
| `question` | 1..nq row on that country sheet |
| `topicId`, `topic` | 1 German Cities, 2 US Cities, 3 Italian Cities, 4 UK Cities |
| `questionText` | "Which city has the larger population?" |
| `option1`, `option2` | City names from the course list |
| `correctOption` | 1 or 2 |
| `city1Id`, `city2Id` | 1-based index into that country's city list |
| `population1`, `population2` | Population (`FeatureEnvironments` criterion) |

`correctOption` is 1 when `option1` has the larger population and 2 when `option2` does. That is the stored `q.truth` flag (true when column-1's city is larger). It matches the population criterion for every pair in every term and month. A trial is correct when the person's choice equals `correctOption`, the same rule as the course parser `(choice − 1) == (1 − truth)`.

City names are the labels stored with the course list, with trailing spaces removed. The accented name `Forlì` is kept as stored. `L’Aquila` is city 76 on the full Italian list and is not part of any pair.

### `trials.csv`

| Column | Meaning |
|--------|---------|
| `participant`, `term`, `itemBank`, `design`, `condition` | Person and the month they were assigned |
| `question` | 1..nq on that country sheet |
| `questionId`, `topicId`, `topic` | Join keys to `questions.csv` |
| `answered` | 1 if the choice is 1 or 2; 0 otherwise |
| `correct` | 1 or 0 when answered; blank when not |
| `choice` | 1 or 2; blank when missing |
| `recognize1`, `recognize2` | 0 or 1 for option 1 and option 2 |

If a country sheet passed the checks, every pair on that sheet is included. A sheet that failed is omitted, and the other countries from the same workbook are kept.

### `participants.csv`

`participant`, `term`, `itemBank`, `design`, `condition`, `nQuestions` (trial rows), `nAnswered`, `nCorrect`.

### `itemBank.csv`

`term`, `itemBank`, `question`, `questionId`, `topicId`, `topic`. `question` restarts at 1 on each country sheet, so it is unique within a month only together with `topic`.

## Counts

1,260 files were in the six submission folders. 965 became participants. 114,063 trials, 9,720 questions (6 terms × 12 months × 135 pairs).

| Term | Files seen | Participants | Files dropped |
|------|------------|--------------|---------------|
| 2012S | 184 | 145 | 39 |
| 2012F | 208 | 153 | 55 |
| 2013F | 215 | 164 | 51 |
| 2014F | 250 | 187 | 63 |
| 2015F | 208 | 167 | 41 |
| 2016F | 195 | 149 | 46 |

693 participants have valid sheets for all four countries, which is all 135 pairs. 671 of them answered every pair (choice was 1 or 2 on each one).

Answered trials: 113,936. Overall accuracy on answered trials: 0.611.

| Topic | Answered trials | Accuracy |
|-------|-----------------|----------|
| German Cities | 31,417 | 0.580 |
| US Cities | 31,673 | 0.679 |
| Italian Cities | 20,409 | 0.608 |
| UK Cities | 30,437 | 0.573 |

Participants by month (columns are terms, in the order above):

| Month | 2012S | 2012F | 2013F | 2014F | 2015F | 2016F |
|-------|-------|-------|-------|-------|-------|-------|
| Jan | 13 | 11 | 7 | 10 | 10 | 10 |
| Feb | 13 | 8 | 14 | 15 | 10 | 14 |
| Mar | 14 | 14 | 14 | 15 | 10 | 14 |
| Apr | 11 | 16 | 14 | 22 | 18 | 15 |
| May | 10 | 11 | 10 | 11 | 17 | 19 |
| Jun | 16 | 9 | 18 | 18 | 15 | 7 |
| Jul | 8 | 16 | 11 | 19 | 12 | 9 |
| Aug | 5 | 10 | 17 | 17 | 20 | 8 |
| Sep | 15 | 7 | 13 | 16 | 14 | 10 |
| Oct | 16 | 19 | 18 | 20 | 15 | 11 |
| Nov | 11 | 21 | 18 | 12 | 13 | 13 |
| Dec | 13 | 11 | 10 | 12 | 13 | 19 |

31 participants were dated from a full month name or `Sept` in the filename rather than from `Jan`–`Dec` alone.

## Exclusions

A file is dropped for one reason. Sheet counts below are for workbooks that opened and had an identified month; a workbook can contribute several sheet failures and still become a participant if another country passed.

| File reason | Files |
|-------------|-------|
| unsupported format (pdf, zip, numbers, ods, xlsb, csv, other) | 43 |
| month not identified in the filename | 173 |
| more than one month token in the filename | 1 |
| workbook could not be opened | 0 |
| opened, but no country sheet passed the validity checks | 78 |

Unsupported extensions: .ods 14, .numbers 12, .zip 11, .pdf 4, .csv 1, .xlsb 1.

| Sheet reason | Sheets |
|--------------|--------|
| sheet name not found | 56 |
| sheet empty in columns C–E | 418 |
| non-numeric entries in columns C–E (words, city names, or other text) | 121 |
| not exactly nq complete numeric rows (too few, holes, or extra rows through row 100) | 115 |
| all zeros | 0 |
| recognition codes outside {0,1} and not exactly {1,2} | 63 |

The parser follows `parsecitycomparisons_v3.m`: month from the filename; sheets `German Cities`, `US Cities`, `Italian Cities`, `UK Cities` (matched ignoring case and extra spaces, so `UK CIties` counts); columns C–E from row 2; keep a sheet only when it has exactly `q(env).nq` numeric rows and three columns, is not all zeros, and recognition values lie in {0,1} or are exactly {1,2}. Values of {1,2} are recoded to {0,1} by subtracting 1 (64 sheets). Sheets whose recognition codes were a single value inside {0,1} are kept (44 sheets); the original MATLAB script required both codes to appear. Words such as yes/no or A/B were not recoded into 0/1 or 1/2. No opened sheet was a complete numeric block of zeros; blank country sheets are the empty-sheet count above.

## Data notes

The Italian generator comment sets `d(3).nobjs = 49` and describes those cities as the ones over 100,000. The stored list has 149 cities. Pair indices in every monthly file fall in 1–49, and those populations were checked against `q.truth`. Two of the 49 are just under 100,000: Udine (99,627), Cesena (97,056). The other 100 cities are smaller and are not used in any pair.

Some workbooks coded recognition as 1/2 instead of 0/1. Those sheets were recoded, as in the course script. Choice stays 1 or 2.

Correctness was checked two ways. Stored `q.truth` agrees with "larger population" for every pair. `correctOption` in `questions.csv` is that same bit, written as 1 or 2.

Trailing spaces on many US, Italian, and UK names in the MATLAB labels were removed. The names are otherwise as stored.

## Citation

Cognitive Science 140C, University of California, Irvine, city-comparison assignment (terms 2012S, 2012F, 2013F, 2014F, 2015F, and 2016F). Unpublished course data. Pairings and the population list are the `CityComparisons_<Mon>.mat` and `FeatureEnvironments.mat` files stored with each term's assignment, not a regenerated matching.
