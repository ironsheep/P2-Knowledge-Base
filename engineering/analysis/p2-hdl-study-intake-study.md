# Study — the HDL clean-room study (golden source 0.1.5): what use it is, what it affects, how it becomes trustworthy

**Status:** COMPLETE (report-only) · 2026-09-26 · started 2026-09-26 · report-only (nothing in the tree changes) · owner: Claude (arbiter), for Stephen

## 1. Scope (agreed)

**The question.** What use is the delivery at
`engineering/ingestion/external-inputs/p2-hdl-study/` to the P2 Knowledge Base, what should it
affect, and what would make its content trustworthy enough to carry into our documentation?

Stephen, 2026-09-26: *"this is study and plan only … what should it affect, and how do we make it
trust worthy enough to include in our documentation? … this is an analysis/planning/brainstorming
task."*

**Surface.** All 16 Markdown files of the delivery (1.26 MB, 15,797 lines):

| File | Lines | Holds |
|---|---|---|
| `P2-READING-GUIDE.md` | 32 | index, the three classes, the evidence convention |
| `P2-THEORY-OF-OPERATIONS.md` | 8,336 | the whole-chip account: §1–3 overview/inventory · §4 per-facility · §5 cross-cutting · §5a anti-pattern register · §6 timing · §8 limits · closing sections |
| `P2-ANTI-PATTERN-QUICKREF.md` | 223 | 181 rows: SO 106 · M 36 · O 28 · C 7 · IMP 3 · U 1 |
| `P2-BOUNDS-BY-QUANTITY.md` | 566 | numeric bounds, each marked stated / implied / not settled |
| `P2-MODE-PROGRAMMING-GUIDE.md` | 368 | per smart-pin mode code: engine, hazards, inheritance |
| `aspects/` (10 reports + README) | 6,272 | one smart-pin/pad mechanism each, written for documentation authors |

**Read against** (the comparison set, read from disk): the KB YAML (`deliverables/ai/P2/`), the
Parallax P2 Documentation (`engineering/ingestion/sources/silicon-doc/`), the bench ledgers
(`hardware-verification/P2-EMPIRICAL-FINDINGS.md` EF, `EXTERNAL-HARDWARE-FINDINGS.md` XF), the
corrections register, and the manuals that cover the same ground (I/O & Smart Pins User Guide,
Streamer Guide, Assembly Reference, P2 Errata).

**Excluded, with reason.**
- The HDL itself — not delivered; the study is our only view of it. Claims are checked against what
  *we* hold (documents + bench), never against the HDL.
- `P2-ERRATA.md` and `P2-MATERIAL-NEEDED.md` — named in the reading guide but **not in this
  delivery** (recorded as a finding, not read).
- `.DS_Store` — macOS metadata.
- P2 Errata's already-integrated errata E1–E7 — decided on the bench; used here only as the
  calibration set, not re-audited.

**Clean-room note.** The study's value is that it reads the design *without* our documents. Nothing
from this study is sent back to it; the direction is study → us.

**Severity scale** (for conflicts found): *breaks users* (our published KB/manual says something the
design contradicts, in a way that produces wrong code) · *wrong but contained* · *latent* ·
*hygiene*. Most rows here are **opportunities**, not defects; those carry the class *opportunity*.

**Done means.** Every file inventoried; every section of the Theory of Operations mapped to the KB
area it touches; the anti-pattern quickref triaged row by row (documented / contradicts our docs /
novel); the aspects and bounds checked against the smart-pin YAML and I/O guide; a calibration of the
study against every bench result we hold that overlaps it; and a trust model proposal.

## 2. Read order (fixed before reading; ticked as returned and verified)

| # | Read | Against | Agent | Done |
|---|---|---|---|---|
| R1 | Provenance, method, completeness: reading guide, aspects README, ToO §1–3, the closing-section conventions | — | survey | ☑ |
| R2 | **Calibration** — every EF/XF bench result and Silicon Doc KNOWN BUG that overlaps a study claim | EF, XF, Silicon Doc | survey | ☑ |
| R3a | Anti-pattern quickref, SO rows (106) | Silicon Doc, KB YAML, I/O guide | survey | ☑ |
| R3b | Anti-pattern quickref, M/O/C/IMP/U rows (75) | same | survey | ☑ |
| R4 | Bounds-by-quantity + mode programming guide | smart-pin YAML, Silicon Doc | survey | ☑ |
| R5 | The 10 aspect reports | I/O & Smart Pins guide, smart-pin YAML, Streamer guide | survey | ☑ |
| R6 | ToO §4 per-facility (lines 310–4295) | architecture + PASM2 YAML | survey | ☑ |
| R7 | ToO §5, §5a, §6, §8 and the two closing sections (4295–8336) | architecture YAML, corrections register | survey | ☑ (part d re-dispatched) |
| R7d *(added)* | The 69 "not settled" items, and 40 of 141 "implied" readings | Silicon Doc, KB | survey | ☑ |
| R8 *(added — G4)* | Seeded random sample of 30 quickref rows, searched by programmer-facing name | Silicon Doc, KB, Errata, EF | survey | ☑ + 6 arbiter re-checks |

## 3. Findings register

| # | Severity | Finding | Evidence | Mark | Root cause | Trivially safe? |
|---|---|---|---|---|---|---|
| S-1 | opportunity | The delivery's class-2 volume (181 quickref rows) is an order of magnitude above the roster's planning figure for P2 Anti-Patterns ("tens of items") | quickref row count; `PUBLICATION-ROSTER.md:237` | traced | planning figure predates the delivery | — |
| S-2 | hygiene | Two files the reading guide indexes are not in the delivery | `P2-READING-GUIDE.md` (P2-ERRATA.md, P2-MATERIAL-NEEDED.md); `ls` of the folder | traced | partial hand-off | — |

| S-3 | ~~latent~~ **resolved** (Stephen, 2026-09-26: the study read the Rev C design) | **The delivery does not identify which silicon it describes.** "Golden source 0.1.5" is the study's own version; no chip revision, tapeout id, HDL commit or date appears. It reads the 37-file closure from the design's top file — *what this delivery builds* — and says itself that this does not establish what was fabricated | ToO:3030–3043 (two versions of one colour-space module: "which modulator was fabricated — remains open"); ToO:71,101 | traced | provenance not transmitted with the hand-off | — |
| S-4 | latent | **No claim is locatable below file level.** Every HDL citation is a bare filename; zero `file.sv:NNN` references in 16 files. We cannot check a claim against its source, and neither can a reviewer | `grep -cE '\.sv:[0-9]'` = 0 in every file | traced | study's citation convention | — |
| S-5 | hygiene | One certainty mismatch inside the study: §1's "organizing idea" is stated flat in the body and re-appears nearly verbatim under *What the source implies but does not state* | ToO:42–46 vs ToO:7858–7862 | traced | synthesis written into the body before being classified | — |
| S-6 | hygiene | ToO numbering jumps §6 → §8 (no §7) | ToO:6906, 6964 | traced | — | — |
| S-7 | opportunity | The quickref and ToO §5a are **one register presented twice** (every SO/M/C id resolves both ways); bounds derives from ToO §8. Two copies of a claim are one source, not corroboration | R1 id cross-diff; `P2-BOUNDS-BY-QUANTITY.md:40–49` | traced | — | — |
| S-8 | opportunity | Facility coverage map (ToO §3). Two facilities have **no facility-level YAML**: the **pad cells** (I/O, clock and reset — the only `pad ring/pad cell` hits are two add-on board files) and the **ALU** as a facility (semantics live per instruction only). **Corrected at verification:** R1 also listed HDMI/TMDS, pixel mixer, RNG and the neighbour vector as uncovered — false; they are covered inside instruction and streamer YAMLs (`setpix/setpiv/mulpix.yaml`, `streamer/nco-timing.yaml`, `getrnd.yaml`, `random_generation.yaml`, `streamer/pin-selection.yaml`, `wrpin.yaml`). TMDS is thin (3 files) | ToO §3 (143–309); `grep -rli` over `deliverables/ai/P2` (control: `cordic` → 62 files) | traced for the two absences; *inferred* for "thin" | — | — |
| S-9 | opportunity | **What a mode change inherits** (the X/Y/Z halves an incoming smart-pin engine is handed) is absent from the whole KB and the I/O & Smart Pins guide | `aspects/MODE-SWITCH-INHERITANCE.md`; ToO §4.1.8; R4: `grep -ril "inherit\|carries over\|previous mode\|mode change"` over `architecture/smart-pins/`, `smart_pins.yaml`, the guide's opus-master → no relevant hit | traced (absence, R4) | — | — |
| S-10 | wrong but contained | OUT-override is stated in the KB for only some of the modes the study lists as overriding OUT; not found for `%00100`–`%00111`, `%11100` (no KB text asserts the opposite — a gap, not a conflict) | `P2-MODE-PROGRAMMING-GUIDE.md` per-mode rows; `architecture/smart-pins/*.yaml` | inferred (R4 spot-check, 6 of 10) | — | — |
| S-11 | opportunity | Bounds + mode guide calibration sample: **12 of 445 bounds rows** checked — 8 agree, 3 deepen, **0 contradict**; **32/32 mode codes** agree with the KB's names and numbering | R4 report | traced for the sample; **433 bounds rows unchecked** | — | — |

| S-12 | opportunity | **Calibration — the study's predictions, tested on silicon:** of the study predictions our bench has decided (O1/EF-066, O17/EF-067, O18/EF-068, SO80/EF-069, SO84/EF-070, SO9/EF-071, SO81/EF-073), **all 7 held at the level of the headline behaviour.** Two were facts no Parallax document states (O18 stale `GETCT` upper long; SO9 DAC-mode ADC enable) and **one contradicts Parallax's own published `%TT` table** — the study read the design correctly where the documentation is wrong | EF ledger :1007 (EF-071), and EF-066..070; quickref :27, :96, :100, :174, :190, :191 | traced | — | — |
| S-13 | wrong but contained | **Calibration — one mechanism detail refuted.** SO81 says an early read after a no-wait `RDFAST` returns data "from FIFO contents the new stream has not replaced" (stale). Silicon: **zero**, in all 8,704 wrong reads of 43,008, never stale; the rig pre-registered zero as refuting that detail. The headline (no stall, no flag, silent completion) held | quickref :97 (SO81); EF ledger :1065–1086 (EF-073) | traced | the study reads *which path is gated*; what the gated path then delivers is below what a structural reading reliably settles | — |
| S-14 | latent | **Independent calibration is thin.** Outside the campaign that tested the study's own predictions, only 3 bench facts overlap it (EF-035 GETCT 2-clock overhead — result only, the ledger says the mechanism is *not* proven; XF-002, XF-003 neighbour routing — consistent). Most of the ledger (DEBUG windows, tools, Spin2 patterns, analog windows) is outside an HDL reading's reach. Checked ≈24 of ≈81 ledger entries in depth | R2 report; EF ledger :198 (EF-035 scope note) | traced (for the 24); undetermined for the rest | — | — |

| S-15 | **breaks users** | **KB defect surfaced by the study, confirmed by Parallax — all 8 interrupt return/resume YAMLs misstate their flags.** `reti0–3.yaml` and `resi0–3.yaml` each quote `CALLD … WCZ` in their own `description:` yet say `C: No effect / Z: No effect` and `c: — / z: —`. The Silicon Doc defines every one as `CALLD … WCZ`. A programmer trusting the YAML would not expect `RETIx` to restore C/Z. Not in the corrections register | `deliverables/ai/P2/language/pasm2/re[st]i[0-3].yaml:5–16`; `silicon-doc-text.txt:2306–2317, 5478–5486`; ToO §4.6.2; `P2KB-CORRECTION-FINDINGS.md` (no RETI/RESI flags entry — `:1148` is unrelated) | traced | *(inferred)* flag fields filled from an encoding table that shows `—` for these aliases, never reconciled with the `WCZ` in the same file's description | **Yes** — source-stated, 8 files, the fix wording comes from the Silicon Doc's `CALLD` flag rule; routes via the register (F-471) |
| S-16 | latent | **The readers' NOVEL labels are not a count.** R3a triaged 92 of 106 SO rows by facility/keyword only (`inferred`); it labelled SO9, SO80, SO84 NOVEL though they are P2 Errata **E6, E4, E5**, and SO81 though EF-073 grounds `rdfast.yaml`. Arbiter spot-check of 12 rows labelled NOVEL across R3a/R3b/R6: **11 are documented or already ours** (M23/M24 `MUL` 16×16 & WZ-only — `mul.yaml:6–14`; O12 REP shields interrupts — `silicon-doc-text.txt:775`; O9 BRK re-arm — `debug_interrupt.yaml:34`; M17 event 0 = disabled — `interrupts.yaml:282`; SO69/R6-3 shift count `S[4:0]` — `shr.yaml:21`; the four errata rows; R6-11 = E4). Biased sample (suspicious rows chosen) → an unbiased seeded sample of 30 is R8 | R3a/R3b/R6 reports; cites in this row | traced (the 12); the population rate is R8's | keyword triage cannot see a behaviour documented under its programmer-facing name | — |
| S-17 | wrong but contained | **Clean-room blind spot: software the HDL cannot see.** SO61 says `GETRND` gives "the same sequence … every reset unless the program re-seeds" — true of the HDL's power-up state, but the boot ROM *is* that program: it re-seeds the PRNG fifty times from pin-63 thermal noise. Carried as written, the row would mislead | quickref SO61; `silicon-doc-text.txt:2854` | traced | the study reads the logic, not the ROM's contents or any firmware | — |
| S-18 | opportunity | **Where the study is most valuable: mechanism behind documented warnings, and the smart-pin engines.** Aspect reports: 27 claims checked — 6 agree, 14 deepen, 2 bench-confirmed, 4 new, **0 contradict**. Examples of genuine depth: which X/Y/Z halves an incoming engine inherits (our KB carries only the Silicon Doc's "unpredictable" warning, `smart_pins.yaml:134–158`); async-serial period below 1024 clocks runs at 1024 (formula in `smart-pin-11110-*.yaml` has no such caveat); the scope readback is a live mirror; the USB odd pin holds no logic. Pad-drive claims are already bench-confirmed in the KB (EF-063/064 in `pin-drive-configuration.yaml`) | R5 report; `aspects/*.md` cites therein | traced for the 27; ≈4,500 of 6,272 aspect lines not checked | — | — |
| S-19 | opportunity | **Candidate new programmer-facing facts outside smart pins** (each still to be checked against the Silicon Doc under its programmer name, per S-16): ALTR before CALLPA/CALLPB redirects the forced return write; CORDIC results survive COGSTOP/COGINIT and a new program's GETQX can return the old one's; paired COGINIT can fail with two idle cogs (no compaction); AUGD has no ALTx carve-out (would settle the KB's own open scope note in `augs.yaml`) | ToO §4.3.1, §4.5.5, §4.6.1 (R6) | inferred | — | — |
| S-20 | opportunity | ToO §4 overall (R6, ≈55 headline claims): 6 agree, 30 deepen, 12 labelled new (inflated — S-16), 1 KB contradiction (S-15), **0 contradict the Silicon Doc or the bench** | R6 report | traced for the 55 | — | — |

| S-21 | opportunity | **The study's own open questions — where we can answer back.** 69 "not settled" items (52 ToO + 17 bounds): **2 are settled by the Silicon Doc** (PLL divide 1–64 / multiply 1–1024; the safe clock-switch sequence and its hang warning), ~6 by a jumper-only bench test, ~10 need external instruments, ~50 are unsettleable from software (tapeout identity, analog internals, design intent). 14 of 69 grep-verified; the rest classified from the item's own wording | `silicon-doc-text.txt:2617, 2726`; ToO :7649–7855; bounds "Not settled" | traced for the 14; inferred for the rest | the clean room by design cannot see Parallax's documents | — |
| S-22 | opportunity | **No certainty mismatch found in our own docs.** Of 40 "implied but not stated" readings sampled, none is stated as flat fact by our KB; CORDIC accuracy is already hedged (F-416/F-419) | R7d; `architecture/cordic.yaml` | traced for 40 of 141 | — | — |

| S-23 | opportunity | **Measured novelty rate: about a third.** Seeded random sample of 30 of the 181 anti-pattern rows (seed 20260926), searched under programmer-facing names: R8 table = 8 Parallax-documented · 2 already ours · 2 partial · 1 wrong-frame · 17 new. Arbiter re-check of 6 of the 17: 3 hold (SO14 dither saturates; M35 no framing-error indication; SO5 stale readback after mode 0), 1 partial (O6 — DAC Y capture per period is documented, `silicon-doc-text.txt:3938–3946`; only the NCO's immediate write is new), 2 documented (SO54 — `silicon-doc-text.txt:2367`; SO66 — `fge.yaml:13`). Projected: **≈ 9–11 of 30 genuinely new → ≈ 45–70 of 181 rows**; ≈ 1/3 are documented behaviour the KB may lack (KB-gap work, cited to Parallax, not anti-patterns); the rest partial. Reader summaries miscounted their own tables (R8 said 12, its table says 17) | R8 table; cites in this row | traced (30-row sample + 6 re-checks); the population figure is a **projection** | — | — |
| S-24 | opportunity | **The delivery contains no erratum P2 Errata lacks.** All 6 rows marked [Erratum] (SO9, SO80, SO84, O1, O17, O18) are E6, E4, E5, E2, E1, E3; E7 was found on the bench, not predicted | quickref :27, :96, :100, :174, :190, :191; `p2-errata/creation-guide.md` numbering table | traced | — | — |

## 4. Root-cause groups

**G1 — ~~The delivery cannot be tied to the chip we ship on~~ RESOLVED: the study read the Rev C
design (Stephen, 2026-09-26: "it read the design for the latest RevC chip. There's no question
there.").** S-3 is closed by that statement; the delivery simply did not carry it. What remains is
S-4 — citations are file-level only, so a reviewer cannot check a claim against its line — which
limits *checking*, not *provenance*.

**G2 — Where it can be checked, the study is right about behaviour and weaker on mechanism
detail (S-12, S-13, S-18, S-20, S-11).** 7 of 7 bench-tested predictions held at the headline; one
beat Parallax's own table (EF-071); **zero** contradictions of the Silicon Doc across ≈ 110 claims
checked by five readers. The one miss (SO81 stale vs zero) was *what a gated path delivers* — the
layer below a structural reading. *Consequence:* trust its "this happens / this does not happen";
bench its "and the value you get is …".

**G3 — The clean room cannot see software or documents (S-17, S-21).** It does not know what the
boot ROM does (SO61) or what Parallax already wrote (≈ 1/3 of its anti-patterns are documented;
2 of its open questions are answered in the Silicon Doc). *Consequence:* every row must be checked
against Parallax documentation **by its programmer-facing name** before it is treated as new — and
that check is exactly what our readers did badly (G4).

**G4 — Keyword triage over-reports novelty (S-16, S-23).** Four readers and one careful sampler
all called documented behaviour "new", because the study names internal design signals and the
docs name behaviours ("intervening interrupt events … are ignored"). *Consequence:* the triage of
181 rows is real work with its own method (translate → search three corpora → classify), not a
grep, and its results need arbiter re-checks.

**G5 — The study is a lens on our own KB (S-15, S-10, S-9).** Reading it against the KB surfaced a
Parallax-confirmed defect in 8 YAMLs that no audit had caught, and gaps (mode-change inheritance,
OUT-override coverage). *Consequence:* part of its value is not what it says but what it makes us
re-check.

## 5. Coverage — what was read, and what was not

| Read | Coverage |
|---|---|
| R1 provenance | full for its sections |
| R2 calibration | ≈ 24 of ≈ 81 EF/XF entries in depth — every one overlapping an HDL topic; the rest are tool/DEBUG/Spin2 facts outside an HDL reading |
| R3a / R3b quickref | all 181 rows classified; **only ≈ 25 traced** — the remainder is keyword triage, superseded by R8's measured rate |
| R4 bounds / modes | 12 of 445 bounds rows; 32 of 32 mode codes (names) |
| R5 aspects | 27 claims; ≈ 4,500 of 6,272 lines unread (the seven engine reports' catch sections) |
| R6 ToO §4 | ≈ 55 headline claims of several hundred |
| R7 / R7d | structure 2/2; 69 open questions classified (14 grep-verified); 40 of 141 "implied" readings |
| R8 | 30-row random sample, 6 re-checked by the arbiter |

**Not read:** the bulk of the ToO (≈ 5,000 lines of per-facility and cross-cutting mechanism), the
engine aspect reports' detail sections, 433 bounds rows. **Why this is enough for the question
asked:** the study's question is *what use, what it affects, how to trust it* — answered by
calibration (G2), a measured rate (S-23) and a coverage map (S-8), not by reading every claim.
Reading every claim **is** the intake work the plan would schedule (§7).

## 6. Open questions (for Stephen)

1. **Trust model** — which rule governs carrying study content into the KB and manuals (§7 A, the
   decision everything else depends on).
2. ~~**Provenance**~~ — settled 2026-09-26: the study read the Rev C design (G1).
3. **Feedback to the study** — do we send back what we learned (SO81 refuted detail with EF-073;
   SO61 boot-ROM frame; the 2 doc-settled open questions)? The clean-room rule concerns what the
   study *reads*; sending bench *results* back is how its predictions were built for P2 Errata.
4. **S-15** — green-light the RETI/RESI flags correction (register entry F-471, fix from the
   Silicon Doc) now, as a trivially-safe item?
5. **Missing files** — ask for `P2-ERRATA.md` and `P2-MATERIAL-NEEDED.md`?

## 7. Trust model and plan seeds

### A. Proposed trust model — per claim, not per document

The existing rule (CLASSIFICATION-GUIDANCE, 2026-09-25) already says *nothing is integrated
unproven on silicon*. At ≈ 45–70 genuinely new rows plus hundreds of mechanism claims, bench-proving
everything one test at a time is not a plan. The proposal keeps the rule for what matters and adds
two cheaper routes where the study is only a pointer:

| Tier | The claim is … | What makes it carryable | Cited to reader as |
|---|---|---|---|
| **L — lead** | anything, as delivered | nothing yet — the study stays in `external-inputs/`, never cited (the Titus tier: a source of questions) | — |
| **D — documented** | stated by Parallax under its programmer name (≈ 1/3 of rows) | the Parallax passage itself | Parallax documentation |
| **M — mechanism** | Parallax states the *what*; the study adds the *why* | used only to explain, in our own words, at the programmer's level; **no value, count or timing from the study stated as fact** (G2: the mechanism layer is where it missed) | not cited — explanation |
| **B — bench** | new programmer-visible behaviour (≈ 45–70 rows) | an `EF`/`XF` run that decides it, pre-registered predictions, controls | the bench result |
| **U — unsettled** | cannot be decided from software | never published as fact; may appear as "not specified" | — |

**Scaling tier B:** group rows by engine into campaign rigs, each deciding many rows (one
mode-switch-inheritance rig covers SO5, SO6, SO85, O8, O19–O26; one serial rig covers SO39–41,
SO94–96, M35, O24). Jumper-only rows (the large majority per R3a/R3b/R6) run on P0–P7/P32–P47;
instrument rows go to the partner bench (`VO-P`/`XF`) or are catalogued.

### B. What it should affect (most first)

1. **P2 Anti-Patterns** (not started) — the primary consumer; its roster entry's scale is now ≈
   45–70 candidates, not "tens" (S-1, S-23).
2. **I/O & Smart Pins User Guide + smart-pin YAMLs** — about half of all rows are smart-pin; new
   material on mode-change inheritance (S-9), OUT-override coverage (S-10), serial/scope/USB
   engine facts (S-18).
3. **KB gap-fill from Parallax** (tier D, ≈ 1/3 of rows) — behaviour Parallax documents but our
   YAML may not carry; and KB defects the lens exposes (S-15).
4. **PASM2 instruction YAMLs + Assembly Reference** — flag and interaction facts (S-19).
5. **Verification-opportunities queue** — the tier-B campaigns; the 6 jumper-testable open questions
   (S-21).
6. **P2 Errata** — nothing new from this delivery (S-24).

### C. Plan seeds (for `sprint-plan`)

- **Seed 1 — the trust-model decision** and its recording (CLASSIFICATION-GUIDANCE addendum,
  `AUTHORITATIVE-SOURCES.md` entry for the study at lead tier).
- **Seed 2 — row-by-row intake of the 181 rows** with the G4 method (programmer-name translation,
  three-corpus search, arbiter re-check); output: D / M / B / U per row.
- **Seed 3 — tier-D gap-fill** into the KB via the corrections register.
- **Seed 4 — tier-B campaigns**, engine by engine, smart pins first.
- **Seed 5 — P2 Anti-Patterns stand-up** once enough tier-B rows are decided.
- **Seed 6 — feedback packet to the study** (refutations, doc-settled questions, provenance ask).
- **Trivially-safe now:** S-15 (RETI/RESI flags, 8 YAMLs, Silicon-Doc-sourced).
