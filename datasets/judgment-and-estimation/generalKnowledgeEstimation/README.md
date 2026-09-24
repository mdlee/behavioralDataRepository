# unpublished general-knowledge estimation

Anchored and unanchored year or quantity estimates collected as a course assignment at UC Irvine (IRB 4286).

`participant` IDs are anonymous integers and match `bart`, `gasPrices`, and `fishPrices` for the same person.

| Quarter | What was estimated | Conditions |
|---------|--------------------|------------|
| W2023 | 10 general-knowledge quantities | `anchor1`, `anchor2` |
| W2024 | 11 event years (Thriller through Pixar) | `anchor1`, `anchor2`, `noAnchor` |
| F2025 | 10 event years (Coachella through Starbucks) | `anchor1`, `anchor2`, `noAnchor` |

W2024 and F2025 use a research-consent filter. W2023 does not have a separate consent item. Firefox’s truth is 2004.

## Columns

- `participant`, `quarter`, `session`, `condition`
- `question`, `questionLabel`, `truth`, `anchor`, `highOrLow`, `estimate`

`highOrLow` is the comparison response: `1` for the higher/later/more side, `2` for the lower/earlier/less side. It is blank in the no-anchor condition. `anchor` is blank when there was no anchor.

## Citation

Unpublished course dataset. The event-year questions are the same family as Lee & Dang (anchoring and the wisdom of the crowd).
