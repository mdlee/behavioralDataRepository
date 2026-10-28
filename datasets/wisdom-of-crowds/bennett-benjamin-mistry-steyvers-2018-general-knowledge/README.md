# Bennett, Benjamin, Mistry, & Steyvers (2018) general knowledge

Bennett, S. T., Benjamin, A. S., Mistry, P. K., & Steyvers, M. (2018). Making a wiser crowd: Benefits of individual metacognitive control on crowd performance. *Computational Brain & Behavior*, 1, 90–99. [doi:10.1007/s42113-018-0006-4](https://doi.org/10.1007/s42113-018-0006-4) · [OSF `nhv3s`](https://osf.io/nhv3s/) (data child [`cfqxy`](https://osf.io/cfqxy/))

Binary general-knowledge questions. People either **opt in** to questions they want to answer or are **randomly assigned** questions. The item pool has **12 topics**. Every trial row carries `questionId` / `topicId` / `topic`.

**284 people**, **28,400** person–question rows (everyone rates difficulty on 100 items in their bank; **7,788** answered). Participant IDs are unique across conditions (OSF IDs restart within each condition and are not reused).

## Experiments and conditions

| `experiment` | `itemBank` | `design` | OSF `condition` |
|--------------|------------|----------|-----------------|
| `1a` | `easy` | `partialOptIn` | Self-Selected1 |
| `1a` | `easy` | `control` | Randomly-Assigned1 |
| `1b` | `hard` | `partialOptIn` | Self-Selected2 |
| `1b` | `hard` | `control` | Randomly-Assigned2 |
| `2` | `easy` | `partialOptIn` | Self-Selected3 |
| `2` | `easy` | `control` | Randomly-Assigned3 |
| `2` | `easy` | `fullOptIn` | Self-Selected4 |

Partial opt-in: choose 5 of 20 items in each of five blocks (25 answers). Full opt-in: answer as many of the 100 as desired. Control: 25 randomly assigned answers. Easy and hard banks are 100-item subsets of the 144-item pool (**56-item overlap**), formed from pilot accuracy.

## Files

- `questions.csv` — 144 items with `topic` / `topicId`, options, `correctOption` (1 or 2), pilot accuracy, and `easyQuestion` / `hardQuestion` (1–100 index in that bank, blank if the item is not in the bank)
- `itemBank.csv` — Qualtrics presentation order for the easy and hard banks (`question` 1–100) joined to `questionId` and topic; `qualtricsText` is the wording from Steyvers’ reconstructed Experiment 1 files; `matchScore` is the text-alignment score for that join
- `trials.csv` — one row per person × question in that condition’s 100-item bank
- `participants.csv` — one row per person
- `data.mat` — struct `d` with the same tables

### `trials.csv` columns

- `participant`, `experiment`, `itemBank`, `design`, `condition`
- `question` — index 1–100 within that item bank
- `questionId` — 1–144 in `questions.csv`
- `topicId`, `topic` — the 12 domain labels
- `answered` — 1 if they gave an answer
- `correct` — 1/0 when answered; blank otherwise
- `difficultyRating` — 1–7 rating collected for every item in the bank

### Linking questions to topics

The OSF trial file indexes questions only as 1–100 within the easy or hard bank and omitted the column that maps those indices onto the 144-item list in `Questions.xlsx`. Mark Steyvers reconstructed Experiment 1 from the original Qualtrics files (`Exp1Easy.mat`, `Exp1Hard.mat`, 27 Oct 2026). Those files give question text in presentation order. The text was matched 1–1 onto the OSF item bank (union 144 items, overlap 56). Per-question answer counts in the easy opt-in condition match the OSF `Question Number` exactly, so `question` 1–100 is the Qualtrics order.

Experiment 2 used the easy bank. Steyvers noted that those questions are likely in the same order as Experiment 1; this release uses that mapping for Experiment 2 as well. Experiment 2 question text was not in the reconstructed MATLAB files.

The 12 topics are Space & Universe, Climate change, World Facts, Sports, World History, Psychology, Physical Sciences, Earth Sciences, Life Sciences, Physical geography, Vocabulary, and Maths & Logic.

## Citation

Cite Bennett et al. (2018). Behavioral data from OSF `nhv3s` / `cfqxy`. Question-order reconstruction from Steyvers (personal communication, 2026).
