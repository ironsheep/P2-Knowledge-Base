# Sprint 1 — Guide Normalization — CLOSEOUT

**Closed:** 2026-08-15
**Tag:** `guide-normalization` · 11 tasks `«#205»`–`«#215»` · est. 11h 0m
**Plan:** `engineering/planning/MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`
**Study:** `engineering/planning/VOICE-GUIDE-PROPAGATION-STUDY-2026-08.md`
**Verdict:** **CERTIFIED — all 11 commitments SHIPPED.** No versioned artifact released, by
Stephen's decision at sprint start.

> **The plan is NOT archived, and that is deliberate.** This sprint was carved out of a plan that
> still holds **Sprint 2** — plan sections §1–§5 and §7–§8 are entirely Sprint-2 work, and the
> sequencing block lists them as pending. Archiving the plan here would bury nine live commitments.
> The plan stays in `engineering/planning/`; only this closeout is archived. See *Deviations* below.

---

## What this sprint was

The manual-corrections effort was split in two on 2026-08-15. **Sprint 1 normalizes the guide layer
— the standard.** Sprint 2 does the manual work measured against it (nine targets, seven version
bumps). Sprint 1 had to run first for a blunt reason: **the guides as they stood would have actively
misdirected an author.** Several told authors to delete the very words that make a claim accurate.

**Root cause, stated once:** the rule was written by naming banned **words** instead of naming the
**defect**. Every contradiction in the study traces to that one authoring error.

---

## Commitment audit

Sprint 1's commitments come from the plan's **SETTLED — the voice-guide tree** block, the plan's
**§6** (instrument owed), and study **§00 / §0c / §0d / §0e / §1**.

| # | Commitment | Task | Status | Evidence |
|---|---|---|---|---|
| C1 | Voices catalog states **R1–R4** as their sole home; **R3 promoted** out of the Claude-Voice prose; three structural rules | `«#205»` `add7da6c` | **SHIPPED** | `documentation-voices-catalog.md:89` (R1), `:96` (R2), `:105` (R3), `:119` (R4), `:127` ("R1 is not R3's first row"), `:154` (never restate — adapt), `:167` (reference, never restate) |
| C2 | Guide-layer conformance instrument + `DOC_AUDIT_COMMAND` set | `«#206»` `2fb2be3d` | **SHIPPED** | `engineering/tools/validation/audit-guide-conformance.py` (561 lines); `.claude/skill-conventions.md:63` |
| C3 | **D2** — `pnut_ts` → `pnut-ts` across the guide layer | `«#207»` `e33d9cc8` | **SHIPPED** | 66 occurrences / 15 files; instrument D2 = 0 |
| C4 | **D3/D4/D5** — dead authority paths · codenames · retired-doc pointers | `«#208»` `79695df7` | **SHIPPED** | 62 codenames; instrument D3/D4/D5 = 0 |
| C5 | **DeSilva** gains a thin `voice-guide.md`; the Sprint-2 edit-vs-regenerate gate; the `::: your-turn` fence | `«#209»` `a62a5a40` | **SHIPPED** | `p2-pasm-desilva-style/voice-guide.md` (77 lines), `:47`–`:50` = the R1–R4 ADOPT/ADAPT/REJECT rows with reasons; `:52` = R3 row-by-row |
| C6 | **IOSP + Debug Window** — 11 voice sites *reconciled*, each gaining §3.4 + a shown R1 example | `«#210»` `bf3e14cd` | **SHIPPED** | instrument D1 = 0 on both guides |
| C7 | Debug Window **creation guide** stops teaching the voice its own voice guide forbids | `«#211»` `77d5c33c` | **SHIPPED** | instrument D1 = 0 |
| C8 | **Assembly + Streamer** word blacklists deleted; un-swept cog-casing correction → **D6 added** | `«#212»` `4e6da1c6` | **SHIPPED** | instrument D6 exists and = 0 |
| C9 | The tail — XBYTE · app-note · SSDB · PNut-Term-TS · Architect · Getting Started; **green unit closes** | `«#213»` `3a78a36a` | **SHIPPED** | instrument reports PASS |
| C10 | **Damage investigation** (research only) | `«#214»` `ac7124b9` | **SHIPPED — result NIL** | study `:443` "RESULT — «#214»: NIL. Count 0, severity none." |
| C11 | **Documentation blast radius** + the structural proof | `«#215»` `f18550ec` | **SHIPPED** | plan `:835` outcome table, `:857` carry-forwards; 8 descriptors repaired |

**No PARTIAL, no MISSING, no AMBIGUOUS.**

---

## Audit findings — the cross-reference table's two imprecise rows

`sprint-closeout` §1 requires reconciling the table both directions. Two rows do not survive that
reconciliation cleanly. **Neither changes the verdict**; both are recorded so a future reader is not
misled.

**1. `Plan §6 → «#215»` is a name collision, not a discharge.** Plan §6 "Documentation Blast Radius"
was authored as **Sprint 2's** artifact list — deSilva `CHANGELOG` v3.0.6, the rendered PDF and
`-src.zip`, the deliverables release index, `PUBLICATION-ROSTER` + Freshness Ledger, XBYTE
`CHANGELOG`, `P2-EMPIRICAL-FINDINGS`, `F-254…F-257`. «#215» delivered **Sprint 1's** blast radius
(planning docs, descriptors, the structural proof). Exactly **one** row overlaps: the
`HEAD-DISPATCH-DRAFT.md` check. **Plan §6 remains open for Sprint 2** and must not be read as done.

**2. Plan §6's own header block is stale.** It reads *"`DOC_AUDIT_COMMAND` is unset for this
project — there is no doc-audit instrument yet… `plan-to-tasks` should generate a task to build
one."* That task was generated, ran, and is `«#206»`. Corrected during closeout.

**3. A plan row was factually wrong.** Plan §6 lists `.claude/skills/HEAD-DISPATCH-DRAFT.md` as
*"References the slug; check whether as live or historical."* It does not reference the slug — and
`git log -S 'smart-pins-tutorial'` shows it **never has**. The row was a hand-survey artifact. This
is the fifth time in this effort that a hand pass was wrong where reading was right.

---

## Exit baseline

Compared against the entry baseline recorded in the sprint charter. **Not worsened; one gate added.**

| Gate | Entry | Exit | |
|---|---|---|---|
| `verify-yaml-format.py` | 1129/1129 clean | **1129/1129 clean** | unchanged |
| `validate-crossref-keys.py` | 100% resolved | **ALL RESOLVED** | unchanged |
| `validate-dod-release.py` | ALL PASSED | **ALL PASSED** | unchanged |
| Guide-layer conformance | *no gate existed* | **PASS — 0 findings / 28 files, D1–D6 all zero** | **NEW** |

Sprint 1 touched no YAML, so the first three are a no-regression anchor rather than a gate on the
work. The fourth is the sprint's principal deliverable: **the guide layer had no automated gate
before `«#206»`.**

**Detection trajectory: 176 → 113 → 45 → 43 → 0.** The exit zero is measured against a *strictly
harder* instrument than the entry 176 — three detections were **strengthened** mid-sweep, **D6 was
added outright**, and the scanned file set grew 27 → 28 as the sweep found guides the first glob
missed. **No detection was ever weakened to reach green.** 24 exemptions and 4 roster-Abandoned
exclusions (`p2-smart-pins-tutorial`) are printed by name on every run — a "clean" that names what
it did not look at.

**Structural proof:** `git diff --stat add7da6c^..HEAD -- '*opus-master*'` returns **empty**. Sprint 1
changed 41 files and **not one line of reader-facing manual text**. All seven version bumps remain
Sprint 2's.

**Verification mode:** all four gates are **locally verified** by running them. No claim here rests
on a compile log or a commit message alone. The one behavioral claim — that the guide layer is
conformant — is the instrument's own output, reproduced at closeout.

---

## «#214» — the damage investigation, in full

The sprint's one genuinely open question was whether our own word blacklists had already stripped
calibrated qualifiers out of **released** text. **They had not.**

- **The task's own premise was wrong, and that mattered.** It scoped the search to "since
  `acf3b4a2` (2026-07-20)". `git log -S 'No hedging language'` dates the blacklist to each guide's
  **birth** — Streamer `10bb35d5` (2026-01-22), Assembly `1e51f086` (2025-11-26). `acf3b4a2` was
  the **corrective** (§2.2a), not the cause. Real window: **7–9 months, not 3–4 weeks.** Executed as
  written, the task would have scanned ~1 commit and returned a NIL that meant nothing.
- **Streamer:** no commit *ever* removed a `may`/`might`/`probably`/`typically` line from
  `streamer-body.md`.
- **Assembly:** 19 flagged commits, **all 19 read and adjudicated** → 0 damage.
- **The one live candidate was cleared by opening the file.** `10736d5d` hardened *"may be
  emitted… start **and alignment** will vary"* into *"the relative layout remains constant"* at
  `part-ii/directives.md:776` and `:861`. In the diff that is textbook damage. Both sites are the
  *before*-alignment examples — no `ALIGNL`/`ALIGNW`, contiguous packing, and the next paragraph
  says so. The **original** was the less accurate sentence.
- **Counter-evidence:** `audit/periodic-audit-2026-05-22.md` §F.1 grepped for hedges, found three,
  **kept all three with reasons**, closed **Verified-OK**; the full audit says *"keep the '+' hedge."*
  Every auditor who met the rule read it as calibrated confidence, not a word ban.
- **The mechanism is real but self-corrected once:** `648b424a` hardened a hedge into a false
  auto-alignment claim; `88f19d3a` reverted it four days later. It never shipped.

**No `P2KB-CORRECTION-FINDINGS` entry was filed** — the gate for filing one is real damage, and it
was not met.

---

## Carryover into Sprint 2 — specific, actionable

1. **Suppression at write time — the open question, and the likelier exposure.** «#214» tested
   damage by *removal*, which diffs can see. Qualifiers **never written** are invisible to every
   diff. Density of `may|might|probably|typically` per 1k body lines: **blacklist manuals 1.31**
   (Streamer 0.56 · IOSP 0.82 · Assembly 2.55) vs **5.23 without** (Getting Started 6.28 · Architect
   5.65 · XBYTE 5.58 · DeSilva 5.20 · SSDB 3.42). **Correlation only — confounded by genre, length,
   author and era. NOT a finding; do not promote it to one.** Test at content level: sample claims
   whose evidence is known partial and check whether the shipped sentence states them absolutely.
   **Priority probe: IOSP** — 12 qualifiers across 14,702 lines covering ADC accuracy and
   temperature-dependent analog behavior is the least plausible number in the table.
2. **Instrument coverage gap — proven, not theoretical.** `MANUAL-DESCRIPTOR.md` files and 17 of the
   18 files in `engineering/standards/documentation-standards/` are outside the glob. «#215» found
   D2, D3 and D4 defects in the descriptors **by hand**, including
   `engineering/ingestion/sources/silicon/` — a directory that does not exist — cited as PRIMARY
   authority. **Widening the glob re-opens the atomic green unit «#213» closed**, so it is a
   deliberate Sprint-2 decision and Stephen's call.
3. **Four orphaned extraction-era style guides** in `engineering/standards/documentation-standards/`
   — `desilva-style-guide.md` (207 lines), `pasm2-manual-style-guide.md` (206),
   `smartpins-style-guide.md` (166), `pasm2-spreadsheet-style-guide.md` (143). All untouched since
   **2025-09-01**, referenced by **nothing** in the live tree, superseded by the per-manual copies,
   each carrying a "vs Silicon Doc" section. Archive candidates per
   `feedback_archive_retired_docs_locally` — **Stephen's call**, deliberately not swept.
4. **299 files repo-wide still carry `pnut_ts`/`pnut_term_ts`** — opus-masters, CHANGELOGs, READMEs,
   workflow docs. Out of Sprint 1's charter by design. **The D4 and D6 classes almost certainly
   extend into manual text the same way D2 does**; the instrument only scans the guide layer, and
   pointing it at opus-masters is a Sprint-2 question.
5. **DeSilva master line 167** — study §0e flags it as a live R1 finding in **released** text.
6. **Plan §6 (Sprint-2 blast radius) remains open** — see audit finding 1 above.

---

## Deviations from `sprint-closeout`

- **§8 "Archive the plan" — NOT performed, deliberately.** The plan holds Sprint 2's nine
  commitments. Archiving it would bury live work. The plan's lifecycle marker records Sprint 1
  closed with a pointer here; the plan itself stays in `engineering/planning/`.
- **§9 `build-wrapup` — not applicable.** No build was tagged and no version bumped; Sprint 1 ships
  no versioned artifact by Stephen's decision at sprint start.
- **§4 `baseline-health`** — run as its four constituent validators directly (the project's
  `BUILD_COMMAND` slot names `validate-yaml-syntax.py`, which the sprint charter explicitly
  overrides: it scans `manifests/` + `knowledge-base/` and returns a green that verifies almost
  nothing). `verify-yaml-format.py` is the real gate.

---

## The method note worth carrying forward

**READ, DO NOT GREP.** Hand counting and keyword surveys were wrong **five separate times** across
this effort:

1. The study's original "21 unreconciled sites" hand count — off by an order of magnitude (176).
2. The keyword survey's cadence table — R4 was in **five** guides, not three.
3. The keyword survey's anti-pattern counts for Architect and Getting Started.
4. Plan §6's claim that `HEAD-DISPATCH-DRAFT.md` references the retired slug — it never did.
5. **«#214»'s only candidate finding would have been FALSE** if judged from the diff alone.

`«#206»` exists precisely to replace hand counts with a mechanical one — and its own first run is
what proved the hand count was the wrong order of magnitude. But note the asymmetry the fifth item
shows: **the instrument replaces counting, not reading.** A machine can tell you *where* to look; it
cannot tell you whether a hedge covered partial evidence or a wrong claim.
