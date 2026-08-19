# Manual Corrections + Retired-Doc Cleanup — Sprint 2 — CLOSEOUT

**Closed:** 2026-08-19 · **Plan:** `MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`
(archived alongside this file) · **Tag:** `manual-corrections-2` · **Tasks:** «#218»–«#239»

> **Closed late.** The sprint's work finished 2026-08-19; the closeout ran the same day but
> **after** the XBYTE sprint had already started and shipped. That gap is itself a finding —
> see *Process findings* below.

---

## 1. Plan audit — every commitment against the artifact

Audited against artifacts, **not** commit messages. Commit-message task citations are unreliable
here (eight of the twenty-one tasks left no commit naming their `«#N»`), which is precisely why
the skill audits the plan.

| # | Task | Commitment | Status | Evidence |
|---|---|---|---|---|
| 1 | «#218» | KB corrections ×8 (F-264 · G-004 · F-265 · F-260 · F-263 · F-266 · F-259 · EF-060) | **SHIPPED** | KB **v1.16.3**, `YAML-HEAD-DASHBOARD.md:19` |
| 2 | «#237» | KB patch release so manuals can cite it | **SHIPPED** | v1.16.3 published ahead of the wave — the F-211/F-245 recurrence fix |
| 3 | «#219» | IOSP ADC power groups (F-261) | **VOID, correctly** | Grounding returned the opposite of the task; stopped rather than executed. F-261 → `RESOLVED-INVALID`, superseded by F-269 |
| 3b | «#239» | P2AN001 power-domain repair (F-269) | **SHIPPED** | P2AN001 **v1.0.4**; `pin-power-domains.yaml` two-layer enrichment |
| 4 | «#220» | Streamer `+`→`\|` ×2 + composition rule (F-259) | **SHIPPED** | Streamer **v1.0.9**; rule stated once in `smart_pins.yaml` |
| 5 | «#221» | Streamer §17.1 — author the protocol (F-260) | **SHIPPED** | Streamer v1.0.9 — §17.1 rewritten, selectivity 1,059,000 vs 430 null |
| 6 | «#222» | deSilva Acknowledgments (F-254) | **SHIPPED** | deSilva **v3.0.6** |
| 7 | «#223» | deSilva Appendix A + line-167 R1 (F-257) | **SHIPPED** | deSilva v3.0.6 |
| 8 | «#227» | XBYTE §15.3 restructure + `set_nz` (F-255/F-256) | **SHIPPED** | KB **v1.16.4**; §15.3 defines `set_nz` + `_RET_ CALL` callout |
| 9 | «#228» | Assembly ch.5 CORDIC — hub I/O out of both loops (F-263) | **SHIPPED** | Assembly **v3.1.6** |
| 10 | «#236» | P2AN002 CORDIC — four artifacts | **SHIPPED** | P2AN002 **v1.0.3** |
| 11 | «#229» | Debug Window FFT channel defaults (F-262) | **SHIPPED** | Debug Window **v1.1.3** |
| 12 | «#231» | Tool-name / codename / cog sweep | **SHIPPED** | across the seven wave elements |
| 13 | «#233» | Front-matter `\markboth{}{}` — Streamer + Debug Window | **SHIPPED** | `fea28f1c` |
| 14 | «#224» | Archive the retired Smart Pins Tutorial | **SHIPPED** | retired 2026-08-16; `CLAUDE.md` work-mode banner |
| 15 | «#225» | Classify 130 references; canonicalise the manual list | **SHIPPED** | — |
| 16 | «#226» | Widen guide-conformance glob to descriptors, drive to zero | **SHIPPED** | `audit-guide-conformance.py` |
| 17 | «#230» | Suppression-at-write-time probe — IOSP first | **SHIPPED** | — |
| 18 | «#238» | F-267 EF-020 collision → EF-061, repoint 3 citations | **SHIPPED** | F-267 `DONE`, now archived |
| 19 | «#232» | Blast radius: changelogs, indexes, register applied-notes | **SHIPPED** | `0c2e8701` |
| 20 | «#234» | ⛔ Review gate — hand Stephen the diff and WAIT | **HONOURED** | `191e5c19` wave audit; opus-master left uncommitted until release |
| 21 | «#235» | Release wave — seven elements, shortest-first | **SHIPPED** | see §2 |

**All 21 commitments SHIPPED or correctly VOID. Plan certified.**

`«#219»` deserves its own note: the task instructed grounding against the domain authority, and
doing so returned the **opposite** of what the task asked us to write. The task was **stopped
rather than executed** — the single best outcome in the sprint, and the reason F-269 exists.

## 2. What shipped

**Seven wave elements, 2026-08-17 → 08-19**, shortest-first:

| Element | Version | Pages |
|---|---|---|
| P2AN001 — ADC Instrumentation | 1.0.4 | 20 |
| P2AN002 — CORDIC for Real Work | 1.0.3 | 15 |
| DeSilva Tutorial | 3.0.6 | 166 |
| Debug Window Manual | 1.1.3 | 168 |
| I/O & Smart Pins User Guide | 1.0.9 | 396 |
| Assembly Language Reference | 3.1.6 | 502 |
| Streamer Programming Guide | 1.0.9 | 76 |

Plus **KB YAML v1.16.3 and v1.16.4**, both published **ahead of** the documents that cite them —
the standing fix for the F-211/F-245 recurrence, where a correction landed in the YAML and never
reached the manuals, twice.

## 3. Exit baseline — GREEN, not worsened

| Gate | Entry (`plan:164-170`) | Exit (2026-08-19) |
|---|---|---|
| `verify-yaml-format.py` | 1129 scanned · 1129 clean · 0 failed | **1129 · 1129 · 0** |
| `validate-crossref-keys.py` | ALL RESOLVED | **ALL RESOLVED** (722 `see_also`, 100 `related_methods`) |
| `validate-dod-release.py` | ALL VALIDATIONS PASSED | **ALL VALIDATIONS PASSED** |

Identical to entry, which was itself identical to Sprint 1's exit — so the assertion compares
like with like across three sprints. **This tree is the protection point the next sprint climbs
from.**

## 4. Carryover — specific, and none of it dropped

**Still open in the register, from this sprint's blast radius:**

- **F-272** — the `%TT` setting for a DAC pin the *streamer* writes is not stated in either
  direction. A **bench** question (chip-gate bucket 1); gates nothing, because the Streamer Guide
  makes no claim about it either way. Belongs to the P2AN001/003/004 cog-DAC re-audits.
  ⚠️ **Carries no status token** — see *Process findings*.
- **F-203** — the 4-manual fan-out audit of quantitative hardware tables. ⚠️ **No status token.**
- **F-207** — `PARTIAL`: manual DONE + HW-verified, KB DONE (v1.15.0), **one manual design
  decision open**.
- **F-268** — `PARTIAL`: KB DONE 2026-08-16, **guide-side sweep owed**.

**Thirteen findings whose fix is applied but whose render is owed** — F-281, F-284, F-286, F-287,
F-289, F-292, F-294, F-295, F-296, F-297, F-298, F-285, F-300. Each reads "source fixed" or "tool
fixed" while its status is still `CONFIRMED`. By this register's own rule a fix applied but not
yet validated is **not** done, so all thirteen stayed out of the archive sweep. They discharge at
their document's next render, **not** by editing a status.

**Not this sprint's, still pending:** «#216» (changelog Class 3 profile — blocked upstream on
central), «#217» (spin2 style gate — `STYLE_GATE_COMMAND` unset, owed not waived).

## 5. Process findings — the sprint's most expensive lessons

1. **The closeout itself was skipped, and the register paid for it.** Central `sprint-closeout`
   §7 runs `punch-list-maintenance` and calls closeout "its defined cadence." Because closeout
   never ran, that sweep never ran: **34 closed findings** accumulated in a register that declares
   it carries open work only, in a **3,559-line** file. Agents miss things in long lists, so a
   skipped closeout does not defer tidying — it degrades every later read. Swept 2026-08-19 (18
   archived under the strict rule); a `sprint-closeout` project overlay now states that a sprint
   is not closed until every archivable doc is swept and `audit-register-hygiene.py` exits 0.
2. **Two findings carry no status token at all** (F-272, F-203) and one carries an **off-legend**
   status — F-256 reads `RESOLVED`, which is not among the register's seven declared statuses.
   Now mechanically detected.
3. **A class-wide sweep amplifies whatever fact it starts with.** F-211 wrote the Edge *board's*
   8-pin LDO grouping into the *chip's* KB file and swept it. Grounding must be **stronger** before
   a sweep than before a single-site fix, and a board document can never establish a silicon fact.
4. **Name coverage is not semantic coverage.** `manual_category_alignment_check.yaml` certified the
   condition category "PERFECT — Complete match" while calling `_RET_` a suffix: it compared the
   list of condition *names*, never their *semantics*.
5. **An app-note correction is not complete until its YAML companion carries it** (F-270 — P2AN001
   v1.0.2 fixed the document five weeks before its companion, so two halves of one released
   deliverable contradicted each other).

## 6. Verification statement

Every element in §2 was **render-verified on the delivered PDF** — page count reconciled, outline
walked, compile log scanned for serious signatures, and for Streamer and XBYTE a page-by-page
pixel comparison against an independent daemon render. That is verification on the canonical
target, not code-complete-awaiting-verification.

The exit baseline in §3 was run at closeout on 2026-08-19 and is reproduced above verbatim.

**Not verified:** F-272 remains a bench question with no rig run, and is reported as such rather
than assumed either way.
