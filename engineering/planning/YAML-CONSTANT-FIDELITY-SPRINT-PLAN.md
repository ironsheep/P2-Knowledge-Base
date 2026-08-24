# P2KB Constant-Fidelity Sprint — plan

**Head/element:** `yaml:p2kb`
**Authored:** 2026-08-24
**Status:** AWAITING per-decision confirmation (§6). No YAML edited yet.
**Register:** findings live in `engineering/operations/P2KB-CORRECTION-FINDINGS.md`
as **F-321…F-326**. This plan **names** them and their status; it does not restate
their verdicts or evidence — read them there.

---

## 1. Why this sprint exists

An agent consuming the published KB could not work out how to use pull-ups and
pull-downs, and reported conflicts around the smart-pin area (Stephen, 2026-08-24).
The investigation found the KB was not vague about it — it was **wrong**, and wrong
the same way in every file, which is a class of defect nothing in the release
process could see.

The sprint goal, in Stephen's words: **make the YAML more consistent, more usable,
and more reliable.** Concretely that means the KB stops describing hardware the P2
does not have, stops using vocabulary it never defines, and gains a gate that
notices when either starts again.

## 2. Entry baseline — measured 2026-08-24, not assumed

| Gate | Command | Result |
|---|---|---|
| Content YAML parses | `verify-yaml-format.py` | **exit 0** — 0 parse failures |
| Cross-references resolve | `validate-crossref-keys.py` | **exit 0** — all validated |
| Register hygiene | `audit-register-hygiene.py` | **exit 0** — clean, 50 live findings |
| Constant fidelity | `audit-constant-fidelity.py` | **exit 1** — 42 Tier 1, 23 Tier 2 |

The first three are green and **must still be green at exit**. The fourth is the
new instrument; driving it to exit 0 is most of this sprint.

## 3. The scope input — the instrument's first run, not a hand count

`engineering/tools/validation/audit-constant-fidelity.py` was built and calibrated
before any scoping (committed `3053e513`). Its first run **is** the scope input,
per the standing rule that an instrument's first run is a planning input and not
just a gate.

**That rule earned itself again here.** The hand pass that produced F-321 named
**three** files carrying the mislabel. The instrument found **six** — it added
`johnny-mac-documentation-style.yaml` and `spin2-docs-jonnymac.yaml`, both saying
"150K pullup resistor". Every task below is sized from the instrument's output.

**Run one was ~55% false positives**, all three classes fixed before any number
here was trusted; the fixes and the reasoning are in the tool's docstring and the
commit message. Two limitations are stated rather than discovered later: source
definitions written as headings are not yet harvested (1 known false ORPHAN), and
Tier 2's lexicon is fixed — **passing Tier 2 is not a certificate of correctness,
only "not caught by these checks."**

## 4. Scope

**IN**
- The drive-strength mislabel class — 23 sites, 6 files (F-321, F-322, F-323, F-324).
- The 41 constants referenced by the KB and defined nowhere in it (F-325, F-326).
- Landing both gate families in the release process (F-326's structural half).

**OUT — named, so the boundary is deliberate**
- The 26 register findings open before this sprint. Stephen asked to fold "more"
  in; the honest read is that this sprint's own three workstreams already exceed a
  normal sprint, and mixing an unrelated 26 makes the exit gate unreadable. They
  stay in the register and get their own pass. **Say so at closeout rather than
  letting it look like they were swept.**
- Manual/app-note prose. The manuals may repeat the same mislabel; that is a
  class-wide sweep this sprint *feeds*, not one it performs. Route via the register.
- Renaming or re-encoding any constant. Every name is legal (2026-07-01 audit) and
  stays legal. This sprint changes **descriptions and coverage**, never names.

## 5. File table

Nothing is edited until §6 is confirmed.

| File | Action | Scope |
|---|---|---|
| `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` | **EXTEND** | Grow the record catalogue from 68 to cover all 122 referenced constants. It already words them from the source (`description: "Drive high 100μA"`), so this is the file the others become redundant against. |
| `architecture/pin-drive-configuration.yaml` | **CREATE** | The concept page. The 13-bit `%M..M` field with its real sub-fields (drive-high `M[5:3]`, drive-low `M[2:0]`, polarity `M[6]`, sync, DIR/OUT), plus the **idioms** an agent actually searches for — weak pull-up, open-drain, bus release — each as a composition of drive settings, with DIR stated. |
| `language/spin2/concepts/basic-io.yaml` | **DELETE blocks / REPOINT** | Remove `pull_up_modes:` / `pull_down_modes:` and the PINSTART mechanism claim; point at the two files above. Rewrite its 4 broken examples. |
| `language/pasm2/concepts/basic-io.yaml` | **DELETE blocks / REPOINT** | Same, plus fix `bits_M_6_0`. Rewrite its 2 broken examples. |
| `architecture/smart-pins/smart-pin-00000-normal-mode.yaml` | **EDIT** | Rewrite its 2 broken examples (Spin2 + PASM2). |
| `language/spin2/conventions/johnny-mac-documentation-style.yaml` | **EDIT** | 1 site — "150K pullup resistor". Found by the instrument, not by hand. |
| `language/spin2/conventions/spin2-docs-jonnymac.yaml` | **EDIT** | 1 site — same. |
| `language/pasm2/wrpin.yaml` | **EDIT** | Expand or repoint the stubbed `M` field (F-326). |
| `language/spin2/methods/wrpin.yaml` | **CHECK, then EDIT** | Verify whether it carries the same stub shape. |
| `language/spin2/methods/pinfloat.yaml` | **EDIT** | Frames pull-ups as external components only; reconcile with the internal mechanism. |
| `engineering/tools/validation/audit-constant-fidelity.py` | **EXTEND** | Parse heading-form source rows (closes the known false ORPHAN). |
| `.claude/skills/release-yamls/SKILL.md` | **EDIT** | Add the gate to the pre-release validator sequence. |
| `engineering/tools/validate-dod-release.py` | **EDIT** | Same, for the DoD gate. |

**Deletion is the correction, not editing in place.** F-321 and F-323 both exist
because one fact was written in two files. Fixing the text in both preserves the
shape that drifted; removing the duplicate and pointing at one home does not.

## 6. Design decisions to flag — confirm each before edits start

**D1 — where the definitions live. DECIDED 2026-08-24 (Stephen).**
Extend the existing symbol catalogue **and** add one concept page. Rejected: a
single new file holding both (would make the existing correct catalogue the
second-best copy — the two-places-to-drift shape that caused this); per-constant
files (122 files for what is really six tables, and the drive ladder only makes
sense read *as* a ladder).

**D2 — the Tier 1 blocking threshold. OPEN.**
41 UNDEFINED is a true finding *and* would block every release starting now. Does
the gate block on Tier 1 immediately, or report-only until workstream B closes and
block thereafter? A gate that blocks before the backlog it discovered is drained
gets bypassed, and a bypassed gate detects nothing forever.

**D3 — what `P_HIGH_1MA` should say. OPEN.**
Source: "Drive high 1mA". That is a **constant-current source**, not a resistance,
so it does not belong on a kΩ ladder at all. Match the source's wording exactly, or
add a clarifying sub-field? The no-inference rule says match; usability says a
reader needs to know it behaves differently from the three resistive settings.

**D4 — how far the pull-up idiom is stated. OPEN.**
The source gives one idiom (`P_HIGH_15K | P_LOW_FLOAT`). Open-drain, bus release,
and keeper configurations are derivable but **not stated by any source**. The
no-inference rule forbids inventing them. Do we ship only what the source states,
or file a gap (`G-007`) for a hardware-verified idiom set?

## 7. Workstreams

**A — correct the mislabel class.** F-321/322/323/324. 23 sites, 6 files. Bounded:
the instrument locates every site, and re-running it is the check.
*Every example gets `pnut-ts` compiled — legality only, never semantics.*

**B — define the undefined.** F-325/326. 41 constants across 8 families (10 ADC,
12 input-selector routing, 4 DAC, 4 comparator/level, plus counting, serial, REG).
The largest workstream and the one that delivers "more reliable".

**C — land the gates.** Wire into `release-yamls` and `validate-dod-release.py`,
close the heading-form harvest gap, resolve D2.

**Ordering:** A and B both re-run the instrument, so C's wiring lands **last** —
wiring a gate whose backlog is still draining is how D2 becomes urgent under
pressure instead of decided calmly.

## 8. Definition of done

1. `audit-constant-fidelity.py` Tier 1 **exit 0**; every Tier 2 advisory adjudicated
   — fixed, or recorded with the reason it is not a defect. **Not** "advisory, so skipped."
2. The three entry gates still exit 0. A regression against entry baseline is a stop.
3. Every touched example compiles under `pnut-ts` (`-d` where it carries `debug()`).
4. F-321…F-326 carry accurate status tokens, annotated in the same pass as the fix.
   A fix applied but not validated is `PENDING-VALIDATION`, not `DONE`.
5. The gate runs in `release-yamls` and `validate-dod-release.py`, at the threshold D2 sets.
6. Closeout names the 26 deferred findings explicitly as **not** addressed.

## 9. What this sprint does not certify

It certifies that **named constants** carry descriptions matching their source. It
does **not** certify the KB is correct about pin configuration. Prose that discusses
a behaviour without naming a constant is invisible to this instrument, and Tier 2's
lexicon catches the confusions it was built from — not all confusions.

**Name coverage is not semantic coverage, and neither is description coverage.**
Say that at closeout too, or the green exit will be read as a guarantee nobody made.
