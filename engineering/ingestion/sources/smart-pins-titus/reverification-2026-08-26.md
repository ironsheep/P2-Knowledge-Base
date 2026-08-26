# smart-pins-titus — re-verification against the completed silicon-doc

**Run:** 2026-08-26, task «#315». **Outcome: nothing needed redoing.** Recorded because a pass that
confirms prior work is worth as much as one that overturns it, and because "we checked and it held"
is not visible unless it is written down.

## Why this was scheduled after silicon-doc

Titus is a **🟡 cross-check** source whose value is corroboration against the authority. Its June
2026 ingestion — and in particular the WRPIN selector conflict — was adjudicated while the Silicon
Doc was **75% ingested and contributing none of its 48 tables**. That adjudication needed re-running
against the complete authority.

## 1. Is the June extraction still adequate? — YES

The current `docx_walk.py` (document-order, cell-recursing, newline-preserving) was run against the
same DOCX and compared with the June artifact:

| | June 2026 | `docx_walk` 2026-08-26 |
|---|---|---|
| lines | 1,731 | 1,732 |
| WRPIN / WXPIN / WYPIN occurrences | 18 / 25 / 21 | 18 / 25 / 21 |
| `%AAAA` · `ADC` | 1 · 83 | 1 · 83 |

**Equivalent.** The character delta (110,693 vs 105,398) is whitespace, not content. **The DOCX
carries 0 tables**, so the cell-hosted-code defect that cost silicon-doc 121 lines **cannot apply
here** — checked rather than assumed. The June extraction stands; re-extracting would have produced
churn and no gain.

## 2. Does the WRPIN selector conflict resolution survive? — YES, re-confirmed

| Source | `x101` | `x111` |
|---|---|---|
| **Silicon Doc** (completed extraction, `silicon-doc-text.txt:3741,3743`) | `relative -3 pin's read state` | `relative -1 pin's read state` |
| **Titus rev 5** (`smart-pins-titus-text.txt:164,166`) | `P37 - 1` | `P37 - 3` |

**Titus has the two swapped**, exactly as recorded in `DOCUMENT-LINEAGE.md`, and reviewer comment
**#21** — anchored inside that very line, visible in the extraction as
`P37 - 1 = P36, pin number minu【CMT#21】s 1` — was right. **The prior adjudication was reached
against the 75% corpus and holds against the complete one.**

**And the KB is correct:** `deliverables/ai/P2/language/pasm2/wrpin.yaml:55,57` carry
`x101: "relative -3"` / `x111: "relative -1"`. A sweep for the swapped (Titus) values across all of
`deliverables/ai/P2/` returns **zero files** — the error never propagated.

## 3. Is the comment harvest complete? — YES, 27/27

`word/comments.xml` holds **27** comments (ids 0–26). The June harvest routes **all 27**, none
missing. *(An initial count said 23; that was a bad regex against a two-table document, not a gap.
Re-counted by parsing the id column.)*

Gap status from that harvest: **G-001, G-003, G-007, G-008 ANSWERED** · G-002, G-004, G-005
PARTIAL · G-006 OPEN. G-002/G-004/G-006 were separately re-tested against the completed silicon-doc
in «#311».

## 4. What remains, and why it is not being done

**~10%: waveform-label OCR debt on 17 figures — WON'T-DO**, detuned 2026-06-22. Reading tick labels
off oscilloscope-style waveform figures yields low-confidence numerals of the exact kind this
project refuses to publish (tesseract misreads digits on this corpus — see the silicon-doc image
catalog). The figures are extracted, catalogued and readable; only their axis labels are
un-transcribed. **Closing this would add risk, not information.**

## Verdict

**No change.** The June ingestion is sound, the conflict adjudication survives the completed
authority, the comment harvest is complete, and the residual is a deliberate won't-do. The
dashboard's ~90% is honest and stays.
