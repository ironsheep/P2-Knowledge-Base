# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): the project's
  `REGISTER-CONSULTATION` protocol (agent-side; not shipped with this repo).

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `PENDING-VALIDATION` (the fix is fully applied; only its validation — a render, a release, a re-test — is owed. Added 2026-08-21: the rule below already described this state and there was no token for it, so nine findings sat as `CONFIRMED` with "render owed" prose and tripped the hygiene gate on every run) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head) · **`RESOLVED`** (the defect is gone AND its validation has landed — the render/release/re-test was RUN and the artifact READ; a fix applied but unvalidated is `PENDING-VALIDATION`, never this. **Added to this legend 2026-08-25 («#302»): it was already the file's MOST-USED token — 31 of 82 entries — and the legend had never defined it, so a third of the register could not be classified by the very vocabulary this line exists to declare**) · `PARTIALLY CONFIRMED` (a ONE-OFF variant used only by F-202, where part of the claim is grounded in a source and part awaits silicon; it classifies as **`CONFIRMED` — open** — do not spread it).

⚠️ **`RESOLVED` entries are CLOSED and are awaiting the next archive sweep, not awaiting work.** **31 of the 82 live entries are `RESOLVED`, so "how many are outstanding?" is 51, not 82** (measured 2026-08-25, «#302»). The hygiene gate deliberately does NOT treat `RESOLVED` as closed-but-live (only `DONE` / `WONTFIX` / `RESOLVED-INVALID` trip check 3), which is why they accumulate silently between sweeps.

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-548`** · gap IDs are **not allocated here** — `engineering/ingestion/KNOWLEDGE-GAPS.md` owns the `G-` allocator and declares its own counter. (This line previously carried `Next gap ID: G-008`, stale by fourteen against that register's actual G-022; two registers claiming one allocator is the collision `audit-register-hygiene.py` exists to catch. Retired 2026-08-26 — see F-352 for the earlier, smaller instance of the same drift.)

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-08-19 (18 findings: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273) → `correction-sweeps/2026-08-19-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-09-10 (1 finding: F-415, `RESOLVED-INVALID`) → `correction-sweeps/2026-09-10-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-01 (24 findings: F-449, F-450, F-451, F-452, F-462, F-463, F-464, F-465, F-466, F-467, F-468, F-469, F-470, F-471, F-472, F-473, F-474, F-475, F-476, F-477, F-478, F-480, F-481, F-482) → `correction-sweeps/2026-10-01-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-03 (45 findings: F-440, F-445, F-446, F-447, F-448, F-483…F-505, F-506…F-520, F-522) → `correction-sweeps/2026-10-03-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 (4 findings: F-400, F-523, F-526, F-540) → `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the manual releases (2 findings: F-521, F-524) → `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Debug Window v1.1.4 release (1 finding: F-531) → `correction-sweeps/2026-10-04-debug-window-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Streamer Guide v1.1.3 release (2 findings: F-539, F-479) → `correction-sweeps/2026-10-04-streamer-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the XBYTE Guide v1.1.1 release (2 findings: F-537, F-538) → `correction-sweeps/2026-10-05-xbyte-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the I/O & Smart Pins v1.0.11 release (4 findings: F-533, F-534, F-535, F-536) → `correction-sweeps/2026-10-05-iosp-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the Assembly Reference v3.1.11 release (4 findings: F-527 `RESOLVED-INVALID`, F-528, F-530, F-541) → `correction-sweeps/2026-10-05-assembly-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the deSilva v3.0.9 release (3 findings: F-529, F-532, F-276) → `correction-sweeps/2026-10-05-desilva-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 by the register reconciliation «#386» (130 findings verified closed against the tree and the release tags; 63 emptied section headings moved with them) → `correction-sweeps/2026-10-05-register-reconciliation-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-19** per `punch-list-maintenance`, as **rename-then-trim** (the archive is a
> git-tracked rename of the original; both files are subtractions from a preserved copy — see the
> skill's project overlay for why building the output loses content). 18 findings archived, 3,559 →
> 2,478 lines. **Classified by STATUS TOKEN only.** Sixteen findings whose headline reads "source
> fixed"/"tool fixed" **stayed open**, because their status is still `CONFIRMED` and most say
> "render owed" — this file's own rule is that a fix applied but not yet validated is NOT done. A
> first pass that trusted the prose would have archived all sixteen. Verified with
> `audit-register-hygiene.py --sweep-check`, which reads the pre-sweep revision out of git.
>
> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---




## Found during the 2026-10 manual releases and the register reconciliation (2026-10-04/05) — F-546, F-547

### F-547 — six comparison-operator entries describe themselves only as "Signed/unsigned compare", and one documents an operator that does not exist (`+<=>`) — `CONFIRMED` (next KB release)
Found 2026-10-05 re-verifying F-443 («#386»). `language/spin2/operators/op_addlt.yaml` (`+<`), `op_addgt.yaml`
(`+>`), `op_addlteq.yaml` (`+<=`), `op_addgteq.yaml` (`+>=`), `op_lteqgt.yaml` (`<=>`) and `op_addlteqgt.yaml`
(`+<=>`) each carry the one-line description `Signed/unsigned compare`, which tells an agent nothing about which.
Spin2 v55 (`spin2-v55-text.txt:473-488`): `+<`, `+<=`, `+>=`, `+>` are **unsigned** less/less-or-equal/
greater-or-equal/greater (return 0 or -1); `<=>` is a **signed** three-way comparison returning -1, 0 or 1, CON
only. **`+<=>` is in no Parallax source and the compiler rejects it** (pnut-ts 1.55.8: `a = 3 +<=> 5` → "Expected a
constant, unary operator, or (", while `a = 3 <=> 5` compiles). Its only origin is our own derived
`engineering/ingestion/sources/spin2-v51/complete-spin2-operators.md:25, :164`, which is also where the
"Signed/unsigned compare" label comes from. **Fix:** state each operator's signedness and return values from
v55; delete `op_addlteqgt.yaml` (no fabricated names in the KB — redirect any `related:` that points to it
to `op_lteqgt.yaml`, Sacred Rule #7); mark the derived v51 table's `+<=>` row as not a real operator.

### F-546 — `instruction_skipping.yaml`'s absolute-CALL rule cites only the Silicon Doc; EF-092 proves it on silicon — `CONFIRMED` (low; next KB release)
`language/pasm2/concepts/instruction_skipping.yaml:112` (rule) and `:121` (its source line). EF-092
(2026-10-04): under XBYTE, a relative `call #` before a line the pattern skips corrupted the VM (4 of 5
results wrong); the absolute `call #\` ran it right. **Fix:** add EF-092 to the `:121` source line
(hardware-verified, Rev C, cog execution under XBYTE); no content change. Held for the next KB release
so no committed-unreleased YAML blocks the manual releases under way (`kb-content-released`).

## Full impact audit: every fact KB v1.23.0 and v1.23.1 changed, against every live document (2026-10-04, «#378») — F-526 … F-541, plus F-542 … F-545 (seen verifying v1.23.1 and writing the MCP filter handoff)

**Method.** The fact inventory was built from the diffs (`v1.22.0..v1.23.1`, `deliverables/ai/P2/`), not
from this register: **69 net fact changes** (843d6fac: 43 — C6 net-reversed by a0ebdd21; a0ebdd21 +
522bc105: 26). v1.23.1 changed no fact (structurally verified in «#376»). Every fact × every live
document — the 18 published plus P2 Errata — was read by five read-only agents, each with a 69-row
denominator per document (all 18 sum to 69). **Every non-CONSISTENT verdict was re-read by the arbiter
against the manual file and against the YAML AND the Silicon Doc on disk.** Rejected after reading:
D16 Single-Step (a Spin2 `GETCT()` example; the 2-clock figure is PASM2-only by design), D10 I/O &
Smart Pins (the guide is right — see F-526), C10 I/O & Smart Pins and P2AN001 (rule + taught `WRPIN #0`
exception = the KB's; P2AN001 changes input select, not mode), C32 Assembly (a valid PLL bring-up), C13
XBYTE (echoes the Silicon Doc's own "cog/LUT only!"), C21 XBYTE (see F-540). Excluded: AI Privacy Guide
(no P2 facts), Donna-Manuscript (private), the layout torture test (instrument). Already in flight, not
re-filed: Streamer GETXACC (F-479); Architect's Guide and P2AN007 mailbox (F-524/F-521 — widened by this
audit, see their notes).

| Document | Update needed | Findings |
|---|---|---|
| Assembly Reference | **yes** | F-527, F-528, F-529, F-530, F-541 |
| DeSilva Tutorial | **yes** | F-529, F-532 |
| I/O & Smart Pins | **yes** | F-533, F-534, F-535, F-536 |
| DEBUG Window | **yes** | F-530, F-531 |
| XBYTE Guide | **yes** | F-537, F-538 |
| Streamer Guide | **yes** | F-539 (+ F-479 open) |
| Architect's Guide · P2AN007 | in «#377» | F-524, F-521 (widened, re-staged) |
| Getting Started · Single-Step · PNut-Term-TS · P2 Errata · P2AN001-P2AN006 | no | — |
| *the KB itself* | **yes** | F-526, F-540 |

F-526 (sync TX primes in reset, EF-090) and F-540 (`##` takes a skip-pattern bit, EF-091) are DONE and archived — `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`.

### F-542 — `guides/pasm2-getting-started.yaml` teaches a wrong register map and P1 instructions — `CONFIRMED`
Seen 2026-10-04 reading the served entry while verifying v1.23.1. Against the Silicon Doc
(`silicon-doc-text.txt:452` "$1F6 RAM / PA"; :664 `SETS`; the CALL entry) and the file's own
`size_checking.why_1F8`:
- `register_model.special_registers` numbers PA 496, PB 497, PTRA 498, PTRB 499, DIRA 500 … INB 505.
  Actual: PA `$1F6`, PB `$1F7`, PTRA `$1F8`, PTRB `$1F9`, DIRA `$1FA`, DIRB `$1FB`, OUTA `$1FC`, OUTB
  `$1FD`, INA `$1FE`, INB `$1FF`. PA/PB "Return address A/B" is wrong too (PA/PB are CALLD/CALLPA/LOC
  registers).
- `core_instructions.data_movement` lists `MOVS`/`MOVD` (P1); the P2 has `SETS`/`SETD`.
- `branching.CALL` "saves return in PA", `RET` "jumps to PA", and `critical_gotchas` "RET uses PA
  register (set by CALL)" — CALL pushes the return onto the hardware stack.
- `TJNZ` / `TJZ` "… decrement D" — they test only; `DJNZ` decrements.
- `assembler_directives.FIT` example "FIT $1F0 (496 longs)" contradicts the file's own corrected
  `size_checking` ($1F8).
**Fix:** re-derive those blocks from the per-instruction YAMLs and the Silicon Doc register table. A
beginner guide is the most-copied page in the set.

### F-544 — the delivery filter deleted a line of the Edge modules' boot-pin note: a wrapped prose line began `sources:` — `PENDING-VALIDATION` (served in v1.23.3, verified 2026-10-04 via p2kb_get; closes when the MCP filter roll's acceptance probe shows the line intact)
Found 2026-10-04 writing the MCP filter handoff, by comparing the shipped filter's output with a
structural strip of the same nine keys across all 1,131 files (8 differed). In
`hardware/edge-32mb-module.yaml` and `hardware/edge-standard-module.yaml`, the folded
`pin_mapping.boot_pin_direction_note` wrapped so that a line began `sources: flash SPI CLK on P60 and
flash SPI CS on P61, but microSD CS on P60`; the line rule took it for a provenance key and deleted it,
so script consumers received the P60/P61 role swap without its first half. **Fixed:** re-wrapped ("the
two / boot sources:"), parsed text identical to HEAD, the shipped note now whole. Same comparison:
`architecture/io_pin_timing.yaml` had its `source:` line indented into the `description: |` block
(YAML read it as description prose; the filter dropped it as provenance) → moved to a top-level
`source:` key, the rest of the file unchanged. The other six differences are correct or cosmetic: a
flow mapping `{source: "cog registers"}` and list items `- source: "CON …"` are content the line rule
rightly keeps; three are a block scalar's final newline. **Gate:** `validate_metadata_filter` now also
compares the payload with YAML's own reading and fails on any content line the filter deleted
(negative control: the pre-fix edge file is caught; the flow-mapping collision stays silent). **Why it
matters for the MCP roll:** the MCP does not yet apply this filter, so MCP consumers still had the
line; rolling the MCP filter before this fix would have spread the loss.

### F-545 — provenance ships under keys the delivery filter does not list (`last_verified`, `extraction_status`, `authority_tier`, `grounding`, …) — `NEEDS-VERIFICATION` (classify, then move into the existing keys)
Measured 2026-10-04 on the shipped payload (keys surviving the filter): `extraction_status` 131 files,
`last_verified` 131, `last_author_extraction` 113, `last_complete_extraction` 73,
`last_author_re_extraction` 29, `authority_tier` 92 lines / 15 files, `grounding` 28 / 10,
`extraction_metadata` 13, `provenance` 10, `extraction_date` 9, `primary_sources` 7, `authority` 7,
`derived_from` 7 / 4, `cite` 18 / 2, `cross_check_sources` 4, `source_document` 3 (outside the
code-example schema), `range_source` 12, `rescrape_source` 17, `import_source` 12,
`original_archiver_name` 6, and others. These reach every consumer (scripts and MCP alike). **Rule
(Stephen, 2026-10-04): the filter's key list does not grow** — "let's make sure we're using existing
keys the way we should and not inventing new keys." So the fix is on the KB side, key by key:
provenance moves into `source:` / `sources:` (or the existing metadata keys), content stays. **To do:**
classify each key (provenance vs content — e.g. `resources`, `reference_links`, `source_code`,
`event_sources` are content; `original_archiver_name` may be attribution a consumer should see), then a
sweep with the «#376» verification method (structural checker, word diffs, gates). Also add a gate that
fails on a NEW key name containing source/extract/verified/provenance/authority that is not in the
list, so the drift cannot recur.

### F-543 — `spin2/methods/pinstart.yaml` flash-FS example puts a clock-pin selector in X for sync TX/RX — `CONFIRMED`
`examples` (P2-FLASH-FS): `PINSTART(SPI_MOSI, P_SYNC_TX | P_OE, SPI_CLK<<24 | 8, 0)` and the same for
`P_SYNC_RX`. For `%11100`/`%11101` X.[5..0] is the mode and word size (`smart-pin-11100` x_register;
Silicon Doc); bits 24+ of X do nothing, and the clock is routed by the mode word's B field (a
relative-pin selector, e.g. `P_PLUS1_B`). `8` in X.[4..0] selects 9-bit words. The example cannot clock.
**Fix:** route the clock in the mode word (pins 56-59: MOSI 57 takes CLK 56 as `P_MINUS1_B`; MISO 58 as
`P_MINUS2_B`), X = `%1_00111` (or the intended word size), compile-check.

## Impact survey — v1.23.2 (`release-yamls` §8, run 2026-10-04)

v1.23.2 changed two facts, both decided on the bench (EF-090, EF-091). Sync serial TX primes its first
word in reset: the I/O & Smart Pins guide already teaches this (ch11:292-296), and F-533's fix text
carries it; no other live document teaches `%11100` ordering (the «#378» audit's per-document reads).
A `##` operand's AUGS takes a skip-pattern bit: the XBYTE guide already teaches it (xbyte-body.md:321-328);
the Assembly Reference states no skip-pattern AUGS rule («#378» G1: NOT-TAUGHT). **No document is
flagged.** Published state verified from raw.githubusercontent.com (both new sentences served); the
running p2kb-mcp needs a restart before F-526/F-540 can flip to `DONE`.

## Impact survey — v1.23.1 (`release-yamls` §8, run 2026-10-03)

v1.23.1 changed no fact: every edit moved a citation or a provenance key out of the shipped text
(F-523, F-400). No live document teaches a fact this release changed, so **no document is flagged.**
Published state verified from outside (raw.githubusercontent.com): `guides/pasm2-getting-started.yaml`
served = HEAD blob, sha256 = the published index entry, `v55:` shorthand absent. The running p2kb-mcp
refused it ("verification failed") — its boot-time index snapshot predates the release; F-523 and F-400
flip to `DONE` on the first served probe after an MCP restart.

## Impact survey — v1.23.0 (`release-yamls` §8, run 2026-10-03)

v1.23.0 changed facts (not only wording) in areas these live documents teach. Each flag is a
**re-audit-against-HEAD** signal for that document's next pass; the grep that located each
concrete site is the evidence, and the audit decides the fix.

| Document | What changed in the KB | Located in the manual |
|---|---|---|
| Architect's Guide | latest-wins mailbox handshake is load-bearing (F-507) | `architect-guide-body.md:919` states the disproven claim — **F-524** |
| P2AN007 | the re-check-the-sequence option is unsafe (F-521) | `P2AN007.md:214` (and the Tip below it) — owed under F-521 |
| Streamer Guide | GETXACC clears only during a Goertzel burst (F-506); streamer-DAC pin needs `P_CHANNEL` (F-513) | GETXACC: already open as F-479 |
| DEBUG Window Manual | SCOPE_XY DOTSIZE / SCOPE LINESIZE half-pixels (F-508); PLOT/MIDI COLOR, BITMAP SET, RATE un-freeze (F-516, F-518); DEBUG_TIMESTAMP stale-window caveat (F-514) | 6 files mention DOTSIZE/LINESIZE units — check each |
| I/O & Smart Pins | PINSTART Yval lost in trigger/serial modes (F-509); NCO Y = 0 (F-510); %10010 restart (F-511); DAC TT bit 0 (F-512); WRPIN pin-first (F-522) | no PINSTART-with-trigger-Yval site found (grep); the rest to the audit |
| P2AN003 | DAC smart-pin modes: OUT runs the ADC only with TT bit 0 (F-512) | to the audit |
| Assembly Reference | DEBUG_TIMESTAMP stale-window caveat (F-514); GETCT pair overhead (F-515, already stated as 2 in ch. 4) | 4 DEBUG_TIMESTAMP sites — check against the caveat |

No other live document's subject intersects the v1.23.0 fact changes; the F-519 id strip changes
no fact.

F-524 (the Architect's Guide mailbox claim) is DONE and archived — `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`.

## The bench ledger audited against the KB (2026-10-03, «#374», fixed «#375») — F-506 … F-523, F-525

Every hardware run we hold — **EF-001…EF-089 (84 entries) and XF-001…004 (4)**, 88 in all — was
checked against the YAML on disk, not against its ledger "Grounds" line (only 28 of the 84 name a
YAML there, and 9 have none). Read-only fan-out over six slices; **every non-clean verdict was
re-checked by the arbiter against the YAML file and the ledger text** before entering here.

**Verdicts, 88 of 88:** 67 in the KB and correct · 4 in the KB and **wrong** (EF-038, EF-041,
EF-056, EF-069 — three defects) · 8 incomplete · 3 missing · 2 needing verification · 4 not KB
facts (EF-016 not observed; EF-045, EF-046 PNut v55 tool defects — the KB records intent, not
per-version tool bugs; XF-004 an SD-protocol count). One agent verdict was overruled: EF-034's
"2 clk/long" is a short-burst average that includes the hub sync, measured with a 2-clock-resolution
rig, and agrees with the KB's "one long per clock after sync" — clean. Two KB-wide findings rode
along (F-519, F-520). Fix through `yaml-knowledge-base-maintenance`; ship in one `release-yamls`.

F-506…F-524 are DONE and archived (`correction-sweeps/2026-10-03-…` and the two `2026-10-04` archives); F-525 stays open below.

F-523 (repo locators in shipped text) is DONE and archived — `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`.

### F-525 — `flash-loader-case-study.yaml` tells the reader to read a narrative the KB does not ship — `NEEDS-VERIFICATION`
Found 2026-10-03 while sweeping F-523. `code-examples/flash-loader-case-study.yaml` `how_to_use_this_entry`:
"Read Flash-Loader-Theory-of-Operations.md (companion narrative) for the full walkthrough". The file lives in
this repo at `engineering/ingestion/sources/flash-loader/` and is not in the KB tree, so a consuming agent
cannot fetch it by that name. Not a citation (it is a reading instruction), so F-523's move does not
apply, and rewording it changes what the entry tells the reader. **To decide:** whether the narrative
is published anywhere a reader can reach (e.g. the PNut-TS repository, where its subject
`src/ext/flash_loader.spin2` lives). If it is, name that location; if not, either carry its substance
into the KB (a code-example companion) or drop the instruction and keep "read flash_loader.spin2 itself".

## Impact survey — v1.22.0 (`release-yamls` §8, run 2026-10-01)

The v1.22.0 delta (21 YAMLs: the P2 Errata silicon findings — `rdfast` + hub read/write family,
`setq`/`wmlong`/`setq_block_ops`, `augs`, `getct` + Spin2 `getct`/`getms`/`getsec`, `getxacc`,
`brk`, `muldiv64`, `wrpin`, `architecture/hub` and `smart_pins`) was intersected against every live
manual's declared sources, then each intersecting master was grepped for the statements the delta
contradicts (capture-and-clear GETXACC, conditional BRK, signed MULDIV64, `address & 7` slicing,
no-wait RDFAST use, GETSEC "long-duration").

- **Streamer Guide — DEFECT FOUND → F-479** (GETXACC capture-and-clear, §10.6 and §17.1).
- **Assembly Reference and deSilva — carried by «#352»** (its body names every entry: GETCT, GETXACC,
  RDFAST and the hub read/write family, SETQ, AUGS, BRK, Appendix J).
- **Architect Guide, Getting Started, I/O & Smart Pins, Single-Step Debugger, XBYTE — intersect, no
  contradicted statement found** by the targeted grep; re-audit against HEAD at each one's next pass
  (IOSP: the DAC-mode `TT` rule and §16.3's MULDIV64 ratio; Single-Step: its BRK material). XBYTE checked: every `RDFAST` it
  shows is `rdfast #0, …` — the waiting form — so E7 does not reach it.
- **No impact:** Debug Window, PNut-TS Terminal Guide. P2 Errata grounds on the silicon itself.

## Impact survey — v1.21.0 (`release-yamls` §8, run 2026-09-22)

The v1.21.0 delta (38 files: `hardware/`, `architecture/smart-pins|streamer|locks`,
`language/pasm2`, `language/spin2`, one app note) was intersected against every live manual's
`MANUAL-DESCRIPTOR.md` declared sources. **Two manuals intersect; eight do not.**

- **Assembly Reference — intersects `language/pasm2/`, `language/spin2/`, and is ALREADY ALIGNED.**
  Every flag-field correction this release shipped (`SUMC`/`SUMNC`/`SUMZ`/`SUMNZ` true-sign,
  `INCMOD`'s wrap, `RCR`'s shifted-out bit, `GETCT`'s WC-as-selector) was applied to the manual in
  «#348» *before* the YAML caught up, so the two trees now agree — verified in `appendix-a`
  (4 / 1 / 8 occurrences). **One row lags and is already recorded:** `LOC` moved to `category: Branch`
  here, and the manual still groups it under Arithmetic. That is on
  `workspace/p2-assembly-language-manual/PUNCH-LIST.md` with an expiry of the next Assembly release,
  including the note that Appendix C's per-category counts must be recomputed when the row moves.
  **No new flag needed.**
- **deSilva Tutorial — intersects `language/pasm2/`, `language/spin2/`; flag recorded here** because
  that manual has no punch list of its own. **Re-audit against HEAD at its next pass**, specifically
  for: the `SUM*`/`INCMOD`/`RCR` flag effects, `GETCT`'s WC (a selector, not a flag write), `LOC`'s
  category, and — most likely to bite a tutorial — the Spin2 `||` operator, which on P1 meant
  absolute value and on P2 means logical OR. A tutorial aimed at P1 refugees is exactly where that
  one does damage.
- **No impact:** Architect Guide, Debug Window, Getting Started, I/O & Smart Pins, Single-Step
  Debugger, Streamer Guide, XBYTE Guide, PNut-TS Terminal Guide. Recorded so the survey is visibly
  done rather than skipped.

## ✅ YAML-HEAD DRAIN GATE — evaluated 2026-09-22 («#351»): **GREEN**

The gate (`document-audit` §2) asks one question: are there **actionable** pending YAML corrections —
information not reaching the agents that consume this KB live? It had never been evaluated. All 61
open findings were classified, each **verified against the tree rather than read off its status**,
because the register lags reality and a stale `CONFIRMED` is indistinguishable from a live defect.

**Result: no actionable YAML correction remains open. The gate is GREEN.**

| Classification | n | Meaning |
|---|--:|---|
| **Landed this pass** | 13 | F-449, F-450, F-451, F-452, F-453, F-387, F-392(part), F-393, F-394, plus F-454…F-459 from «#350» |
| **Already done, status was lagging** | 8 | F-382, F-383, F-386(part), F-388, F-329, F-348, F-374, F-352 |
| **Blocked on external — parked, does NOT gate** | 7 | F-372, F-354, F-400, F-336, F-337, F-202, F-208 |
| **Not YAML — outside this gate's scope** | 15+ | tooling (F-405, F-439, F-376, F-389, F-381), ingestion (F-421, F-367, F-332, F-344, F-341), manuals (F-356, F-274, F-276, F-278, F-280, F-424, F-207, F-203, F-218), platform/PDF (F-316, F-317, F-300, F-301, F-299, F-319) |

**Why the parked set does not gate, individually:**
- **F-372** (`%11011` says a new WRPIN needs no reset, against the same document's general rule) —
  settles only on a bench: configure a USB pair, WRPIN with DIR high, observe. Jumper-only, so it is
  a *runnable* test, not an out-of-scope one. Class B periphery.
- **F-354** — six of eight items need an acquisition this repo does not hold (a level-shifter
  datasheet, ISP HUB75 driver docs, the #64013 and #64006 schematics, OBEX `psram.spin2` docs). Two
  of the eight have since resolved themselves via the HUB75 official-specs ingestion.
- **F-400** — a definition call on citation shorthand, Stephen's ruling. Worth knowing: expanding
  every shorthand is now **15 sites in 2 files**, not the 55 the entry was written against.
- **F-336, F-337, F-202, F-208** — bench or Chip Gracey. These are the hardware periphery.

⚠️ **Three things this pass proved about the register itself, which matter more than any single row:**
1. **Eight findings were already fixed and still read `CONFIRMED`.** A register whose statuses lag
   the tree invites re-chasing work that is done. Every row touched here was re-verified and flipped
   in the same pass.
2. **One finding's sub-claim was REFUTED** (F-394's C/Z entry condition, which is absent from the
   source it cites). A register entry is a claim like any other.
3. **`p2an006` cited `cogspin.yaml` for figures `cogspin.yaml` had no source for** (F-392). Two
   files agreeing is not provenance; it is a loop.

## Content-trust study: what the Aug/Sep change set lost (2026-09-22, «#350») — F-454 … F-459

All six surfaced by the content-trust study
(`engineering/analysis/2026-09-22-p2kb-content-trust-study.md`), which classified 660 of 660
deleted/replaced hunks since 2026-08-01. **The headline is that the window did NOT weaken the KB**
— 0 of 518 replacements were weaker, and 380 were verified stronger. These are the exceptions.

**F-454 through F-457 are all collateral of ONE commit — the hardware-tree purge.** The language
and architecture trees lost nothing across 94 delete-only hunks. The purge was mostly right (it
removed fabricated electricals, and 27 of its 48 hunks were delete-then-repopulate-with-citations
inside the same file); it took four real facts with it. All four were confirmed verbatim in sources
already held, so restoring them was transcription, not research.

### F-454 — `edge-standard-module.yaml` lost its revision history, leaving a VIN maximum that destroys Rev A/B boards — `PARTIAL — applied 2026-09-22; the gate this entry names as owed (an absolute maximum stated without its board revision) is not built (re-verified 2026-10-05 «#386»)`

> **SEVERITY: BREAKS USERS (hardware damage).** The purge deleted the board's revision history. What
> remained read `input_voltage: "5-16 VDC"` and `ratings.vin: "5 V recommended, 16 V maximum"` with
> **no revision qualifier**. Per the Product Guide's Revision History
> (`edge-standard-module-narrative.txt:519-549`), VIN maximum was **5.5 V on Rev A and Rev B** and
> was "increased from 5.5V to 16V" only at **Rev C**. A user holding a Rev B module was being told
> by the shipped KB that 16 V is acceptable — roughly three times their board's maximum.
>
> **Applied 2026-09-22:** both fields now carry the revision scope, and a `board_revisions:` block
> restores the full Rev B / Rev C / Rev D deltas (copper 1.5→2 oz, microSD added, crystal→TCXO,
> 2 A→3 A, 2.5 MHz→750 kHz, 4→6 layers) with the source locator.
>
> ⭐ **THE MECHANISM IS NEW AND DESERVES ITS OWN GATE.** This is F-348's shape (a figure beyond an
> absolute maximum) reached by a different route: **not a fabricated number, but a CORRECT
> current-revision number stripped of the revision scope that made it correct.** Deleting a revision
> history silently converts a true claim into a destructive one, and no instrument we have looks for
> it. A gate that flags a shipped absolute-maximum stated without its board revision is owed.

## Two release-path defects, one root cause — F-440, F-441

### F-441 — v1.19.1 published an index the integrity check could not verify — `PARTIAL — v1.19.2, 2026-09-19; published state re-verified against raw.githubusercontent.com; the owed index-sha256-vs-committed-blob gate is not built (re-verified 2026-10-05 «#386»)`

v1.19.1's index carried the **pre-change** SHA-256 for the two files that release edited, so the
MCP refused to serve them: *"Content for 'p2kbPasm2Xinit' is temporarily unavailable — verification
failed."* The release was live and broken for `p2kbPasm2Xinit` and `p2kbArchOverview`.

**Cause: step ordering.** `release-yamls` §6b regenerates derived artifacts **against the committed
state**, and it is a separate step for exactly this reason — the generator hashes the **git blob**,
so an index built while the edits are still uncommitted records the OLD hashes. This pass collapsed
6a/6b and regenerated before committing content. The gates could not catch it: `validate-dod-release`
checks index/gzip parity and structure, not whether each entry's sha256 matches its committed blob.

**Same root cause as F-440**, one release apart: both are *reading from what I had done rather than
from what was committed* — once into a release note, once into a derived artifact. The first was
caught by auditing claims against the tree; the second by the consumer's own integrity check, which
is the only reason it surfaced at all.

**Fixed and verified on the artifact, not the gate:** index regenerated post-commit, then every
entry's sha256 compared against `git cat-file blob HEAD:<path>` — **0 of 1131 mismatch**. Published
state confirmed from outside: `raw.githubusercontent.com` serves the corrected `xinit.yaml`, its
sha256 equals the published index's entry, and the content carries the fix.

**Owed — the gate that would have caught it:** a release check asserting every index entry's sha256
matches the committed blob it names. Cheap (one `git cat-file` per entry), and it makes the
6a→6b ordering self-enforcing rather than a rule someone has to remember. Pairs with F-440's
CHANGELOG-vs-diff check; both belong in `validate-dod-release.py`.

**Not a defect, recorded so it is not chased:** `p2kb-mcp` still reports the failure in this session
after the fix. It serves a boot-time snapshot and does not reload on republish — a stale read needs
an MCP restart, not `p2kb_refresh`.

F-440 (the CHANGELOG claim that was never applied) is archived — `correction-sweeps/2026-10-03-P2KB-CORRECTION-FINDINGS-archive.md`.

## The provenance strip reaches two of its three consumers — F-439

### F-439 — the MCP serves provenance the fetch scripts no longer send — `CONFIRMED — found 2026-09-19 at the v1.19.0 publish verification; the fix is in the MCP server, not this repo`

v1.19.0 stripped provenance at delivery: `source`, `sources`, `source_reference`, `verified_against`
and provenance comments, joining the five metadata fields already filtered. Both fetch scripts were
updated and the release gate now runs the shipped filter over all 1131 files.

**It does not reach MCP consumers.** Verified against the live server immediately after the
release, which returned `p2kbHwAddonMotorDriverAddonMotorDriver` carrying four intact `source: >-`
blocks, including:

```
engineering/ingestion/sources/p2-universal-motor-driver/complete-p2-universal-motor-driver-content.md:138-152
```

— a path that exists only inside this repository, delivered to an agent that cannot open it. That is
precisely the class the strip exists to remove, still live on the path most consumers actually use.

**Why it was missed, which is the part worth keeping.** There are **three** implementations of one
filter: `fetch-kb-file.sh`, `fetch-kb-file.ps1`, and the MCP server's `filter/filter.go`. The
release gate compares the first two and has no knowledge of the third — the server is built from a
different repository, so nothing in this one can run it. A rule with three implementations and two
gated will drift at the ungated one, every time.

**Done here:** `engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md` §Content Filtering — the
contract the server is built from — now carries the full field set, the comment pattern, the
indentation-aware rule with the measured reason (a line-based strip breaks 50 files), and a standing
note that this server is the ungated third implementation.

**Owed, and it is not in this repo:** rebuild the MCP server against the updated spec. Until then
MCP consumers receive provenance; script consumers do not. Worth considering at that rebuild:
whether the server should apply the strip at fetch (as now) or whether the gate should reach it,
since a contract in a document is exactly the enforcement tier this project distrusts.

## Two upstream P2KB update requests, probed 2026-09-17 — F-435, F-436, F-437, F-438

Both arrived as documents in `engineering/ingestion/external-inputs/p2kb-update-requests/`. An
upstream request is a **lead, never an authority** (D3), so each claim below was re-derived from
sources this project holds before anything was applied. The two requests came out differently, and
the difference is the point: one was confirmed by our own sources and applied; one was held.

### F-436 — the `map_caveat` retraction is confirmed on the released compiler; applied — `PARTIAL — map_caveat applied 2026-09-19 and shipped; the two unreproduced byte pairs this entry says were dropped are still in object-image-dedup.yaml (:75, :99) (re-verified 2026-10-05 «#386»)`

`language/spin2/concepts/object-image-dedup.yaml` `map_caveat` tells readers the multi-instance
`.map`'s instance-name/source-name columns are unreliable and to *"do NOT trust those labels."* The
upstream request retracts that: the bug was fixed at 1.55.4, three further defect classes were fixed
for 1.55.8, and 15/15 verification cases pass. The retraction is very likely correct — **and the
replacement text must not be applied as written.** Two reasons, neither about whether the compiler
was fixed:

1. **Shape.** The proposed replacement is a three-era build history — *"Through 1.55.3 … 1.55.4
   through 1.55.7 … From 1.55.8 …"*. This project ruled on exactly this (Stephen, 2026-08-21):
   **cite the EDITION, never the BUILD** ([[reference_kb_is_always_latest_no_version_citations]]).
   The KB ships one edition — the current one — and that memory names **this very file** as the one
   found carrying a rotting build stamp (*"re-verify on a compiler version bump"* pinned at v1.55.0
   while v1.55.3 was installed). Replacing one build stamp with three build ranges is more of the
   shape that ruling removed. An agent reading the entry cannot tell which compiler its user runs,
   so a version-ranged caveat gives it no decidable answer.
2. **We could not reproduce it.** The measurements were against an unreleased *"pre-1.55.8 sprint
   build"* in the upstream repo, via a script that lives there (`npm run p2kb-verify`), while this
   container had **v1.55.5**.

**RESOLVED 2026-09-19 — reason 2 evaporated and reason 1 still decided the text.** The 1.55.8
release landed in `.devcontainer/` (`pnut-ts-linux-arm64-015508.zip`); installed for session use and
**every claim re-measured here, on fixtures built from this entry's own prose, reading the `.map`
rather than any changelog:**

- **The format did change.** No `Objects:` line. `SUMMARY` states it directly — *"The top object and
  2 OBJ declarations became 3 instances, built from 2 images; 1 image is shared by more than one
  instance."*
- **The entry's mechanism cases reproduce exactly.** identical overrides (100,100) → 2 images, one
  shared · differing (100,200) → 3 images, none shared · differing-but-unreferenced → 2 images,
  silently merged, **and the two binaries are md5-identical** (`ae060796…` both ways), which is the
  entry's own md5 claim · a top override through a forwarding chain forks every tier below it while
  the un-overridden sibling keeps its own chain · the mirror trap: one declaration overridden and
  its sibling not costs **536** Code/DAT bytes against **420** when both are overridden and the
  images are shared.
- **The four shapes the caveat was written about are fixed.** Identical copies with nested children
  get four distinct, correctly-nested VAR bases (LEFT `$54`, LEFT.LG `$60`, RIGHT `$74`, RIGHT.LG
  `$80`) · an `OBJ` array gives every element its own row and VAR base with the shared image's
  Instances cell reading `D[0..2]` · an `OBJ` declared after an array gets its own image, its own
  source file and its own address · a DAT-layout fork shows per-image DAT addresses (MARKER at
  `$00090` in one image, `$0016C` in the other) with an `ADDRESS INDEX` naming the owning image.

**What was applied is not the request's text.** `map_caveat` now states what the `.map` contains and
that its labels are reliable, names 1.55.8 **once** as the release where the format changed — an
edition fact a reader needs to explain a differently-shaped file, not a build stamp — and closes
with one sentence for anyone on a compiler old enough to print `Objects:`. The three-era bug history
is not carried. `verification.method` now says to read the `SUMMARY` count and the `MEMORY LAYOUT` /
`OBJECT DETAILS` addresses.

**Evidence-scoping, since the request offered more than was taken.** Two absolute byte pairs the
entry carried (348/216 and 372/240) were **dropped rather than restated**: they belong to fixtures
nobody still has, the request itself says they are not expected to match, and neither it nor this
pass reproduced them. What replaced them is the *relation* — forked costs more than shared — which
was measured here. The mechanism claims, `THE RULE`, `singleton_rule`, `forking_a_dat_region`, the
two silent traps and `cascade_through_tiers` were not touched; this release changed only how the
`.map` reports the result.

## The two ROM listings are different BUILD TARGETS, and F-123's grounding plan names the FPGA one (2026-09-10, ROM-asset mining) — F-421

### F-421 — `ROM_Booter.lst` is an FPGA build; only `rom_booter_v33_01j.lst` is the Prop2 silicon ROM — `PARTIAL` (re-verified 2026-10-05 «#386»: the grounding plan is annotated; nine shipped KB files still cite ROM_Booter.lst unlabelled)

Found 2026-09-10 while scoping the ROM-facility mining Stephen asked for. The corpus holds two ROM
listings in `engineering/ingestion/sources/rom-booter/` and nothing says which is the chip.

**They are the same SOURCE and different TARGETS.** Both changelogs are byte-identical — 76 lines
each, both ending `RR20180527 v141 proposed final SD & Monitor` / `PBJ20180527 Added SD and FAT32
routines`. So neither is a newer revision of the other. The build target is selected by a single
active `ver` constant, and every other candidate is commented out:

| file | active `ver` | target |
|---|---|---|
| `ROM_Booter.lst` (7,296 lines) | `ver = "A"` | `Prop123-A9 / BeMicro-A9, 8 cogs, 64 smart pins` — **an FPGA board** |
| `rom_booter_v33_01j.lst` (7,356 lines) | `ver = "G"` | **`Prop2 Silicon v2`** |

Read directly: `ROM_Booter.lst:118` has `ver = "A"` uncommented with `B`-`F` commented;
`rom_booter_v33_01j.lst:125-131` has `A`-`F` ALL commented and `ver = "G"` active. The A-file has no
`"G"` line at all.

The difference is not cosmetic — 835 hunks across ~3,300 lines once CRLF is normalised (the silicon
listing is CRLF, the FPGA one LF, which is why a naive `diff` reports every line as changed and
tells you nothing). Sampled divergences are exactly what a silicon-vs-FPGA build implies: the FPGA
build computes `delay5us = _cpufreq / 200_000` from live `_clockmax`/`_clockfreq`/`_clockfpga`
constants, while the silicon build comments those out and hardcodes `(20_000_000 / 100_000 / 2) - 2`
for 20 MHz; a `spare` reserved long in the FPGA build is `_AA55` ("used to store $AA55 to validate
MBR/VOL/FSI") in silicon; and the SD entry is reorganised — `_Start_SDcard` calls `_SDcard_Init`
then separately `_readMBR`/`_readDIR`/`_readFILE` in the FPGA build, versus a single
`_SDcard_Init0` doing "Init/CSD/CID/MBR/VOL/FSI/FAT" in silicon.

**The defect: F-123's grounding plan names the wrong file.** F-123 says *"mine `ROM_Booter.lst`"*,
and its 2026-08-25 re-verification note calls `rom_booter_v33_01j` "the mined edition" only because
E-005 cites it — a citation, not a build-target analysis. Mining `ROM_Booter.lst` would document a
ROM **that is not in the chip**: FPGA clock constants, a different SD call structure, and a reserved
long that silicon uses for MBR validation.

**Correction:** all ROM-facility and ROM-technique mining reads `rom_booter_v33_01j.lst`.
`ROM_Booter.lst` is retained as the FPGA-era comparison point and must be labelled as such wherever
it is referenced. F-123's plan text is annotated accordingly.

**F-403 is unaffected and stays RESOLVED.** Its measurement was run against BOTH listings (its table
carries a column for each) and returned 0 for `font`, `glyph`, `sine`/`sin_` and `log2` in both, so
its conclusion does not rest on the file this finding re-picks.

## The manuals were audited against the v1.18.0 delta at the FACT level, not the path level, and eight corrections were located that the path intersection could not see (2026-09-09, post-release manual sweep, applied 2026-09-10) — F-408…F-419

**How this surfaced.** `release-yamls` Step 8 recorded a **path intersection** — each document's
`MANUAL-DESCRIPTOR.md` declared sources against the release's changed files — and returned
*"INTERSECTS"* for 17 of 20 documents. Stephen asked for the list we would actually work from. A
path intersection cannot produce one: it says a document touches changed ground, never that it
restates a changed fact. Re-run at the fact level — 31 probes over all **126 live master files**,
every hit read in context — the answer is **9 documents with work and 7 with none**.

**Range extended to F-416 on 2026-09-10** as the sweep was applied: F-416 is a KB defect
(`cordic.yaml`) that this sweep *surfaced* rather than a manual correction, and it is kept under this
header because that is where its provenance is legible. **F-415 was rejected on the evidence** — see
its entry — so the header's "eight corrections" is seven applied plus one that was not a defect.

**Full located list, with the negatives that keep the sweep from re-deriving them:**
`engineering/analysis/2026-09-09-v1.18.0-manual-update-list.md`.

**Verified clean, so nothing below is a sweep target:** the `150 mA` per-pin scalar never reached
any manual (every drive figure reads 30 mA); no document carries TTL `VIL`/`VIH`/`VOL`/`VOH`
figures; ALM's interrupt vector map is correct (`$1F0=IJMP3` … `$1F5=IRET1`); `WRLUT` operand order
and LUT-sharing direction are both correct in ALM; `LOCKTRY` acquires everywhere; no fabricated
mnemonics (`RDCOGID`, `RDLUTS`, `NIXINT0`, `TRGINT0`) appear anywhere; no boot-ROM font or math-table
claim survives; no document states a `WAITMS` ceiling; and **of 95 shipped `examples-library/*.spin2`
files, none carries a pull idiom or a `-1` cog launch.**

### F-418 — the layout torture test is built on 44 constant names that exist in no Parallax source — `CONFIRMED` (scope decision owed)

`p2-layout-torture-test/opus-master/P2-Layout-Torture-Test.md`. Measured 2026-09-10 against **every**
ingested source under `engineering/ingestion/sources/` plus the published KB: of **63** `P_*`/`X_*`/
`EVENT_*` symbols the document uses, **19 are real and 44 appear nowhere**.

**Fixed in this pass (6 sites), because these claimed to be a symbol reference:**
- §6.2 *"Long Unbreakable Tokens"* — all three rows were invented at 30-32 characters. **The longest
  constant that actually exists in the P2 symbol set is 24 characters** (`X_2ADC8_16P_4DAC8_WFLONG`),
  so the section was calibrating the width allocator against an input no real document can produce,
  leaving the true worst case untested. That is a **validity** defect in the instrument, not a
  cosmetic one. Now the three longest real symbols (24 / 23 / 23), and `X_2ADC8_16P_4DAC8_WFLONG` is
  the right target for a second reason: it is the symbol that printed ON TOP of its own value in the
  released Assembly manual, the defect behind the tables filter's token-fit branch.
- §6.1 and two mode-table rows — `X_RFBYTE_1P_1ADC` / `X_RFBYTE_1P_1ADCb` → real analogues.
- Two **PASM2 code** sites — `xinit ##X_RFLONG_32P` → `X_RFLONG_32P_4DAC8`. A constant that does not
  exist inside a code listing is the least defensible instance of the class.

**Still open — 44 names, and it is a scope decision, not a defect to fix silently.** The rest sit in
the instrument's wide synthetic mode tables, whose cells are layout fodder ("HDMI and VGA framebuffer
scan-out"). The document is an **instrument**, never published to readers, and it is *"engineered to
reproduce every known layout defect"*. Against that, changing 44 symbols shifts column widths and
would invalidate the `VerifiedBox` claims throughout — each of which was verified against a specific
numbered render. **The question for the register's owner:** does the no-fabricated-names rule reach
an instrument's test fixtures, or stop at documents a reader can obtain? Answer that once and it
settles the whole table set; do not re-derive it per row.

**And F-356's own repair changed shape.** §1.24 settled that calling `P_HIGH_15K` a "15 kΩ pull-up"
is *acceptable vocabulary*; the KB stopped policing a word its own authority uses. What F-356 owes
is **the `DIR` caveat plus a source for the `P_HIGH_15K | P_LOW_FLOAT` composition**, not deletion of
the word. Anyone scoping F-356 off its original wording will do the wrong repair.

---


## The index and its gzip drifted apart again and the release validator sat red in committed history for four days — F-357's defect, recurred (2026-09-09, ledger re-derivation) — F-405

### F-405 — `validate-dod-release.py` exits 1 on a stale gzip, and nothing in this project makes it run — `PARTIAL`

**Location:** `deliverables/ai/p2kb-index.json` / `deliverables/ai/p2kb-index.json.gz`, and the absence of any trigger for `engineering/tools/validate-dod-release.py`.

**What was measured.** Run at `b0057ec1` before any repair, the release validator reported **`❌ Gzip Compression: FAIL — Gzip content does not match JSON file`** and exited **1** (*VALIDATION FAILURES - DO NOT RELEASE*). The other ten checks passed.

**Why.** Derived from `git log` on the two paths, not recalled:

| | `p2kb-index.json` | `p2kb-index.json.gz` |
|---|---|---|
| last regenerated | `da896073` (2026-09-05) | **`b753a29d` (2026-08-30)** |
| commits touching it since `9ab0433b` | `d55b6c7f`, `da896073` | **none** |

The 2026-09-05 findability pass regenerated the JSON **twice** and the gzip **neither time**. **This is F-357 recurring while F-357 reads `RESOLVED`** — which is what makes it a regression rather than an open item.

**A second, unrelated staleness in the same artifact.** The index was generated on 09-05 and the 09-08 boot-ROM pass (F-403) committed content afterwards. Regenerating updated exactly **two** entries — `p2kbArchBootRomContents` and `p2kbArchIndex` (`architecture/boot-rom/_index.yaml`), mtime and sha256 both — and added or removed none; the count stayed at 1,133. So the pair was *inconsistent* **and** the index was *stale*, and those are two different defects with two different remedies.

**Repaired 2026-09-09.** Both regenerated together, in the required order (the index stores the git blob sha256, so it must be rebuilt after the content commit). `gzip -cd … | cmp -` is clean and the validator is green at 11 of 11.

**Why this is `PARTIAL` and not `RESOLVED`.** The drift is gone; **the reason it happened is not.** The instrument worked — it caught the drift on its first run. What failed is that **nothing invokes the instrument**: a red release gate lived in committed history for four days and was found only because the change ledger was being re-derived. That is the same sentence F-360 has been carrying about the duplicate-key gate, now with a demonstration attached instead of a prediction.

**What closes it — two checks, one wiring pass** (task «#339», block H):
1. Wire `audit-yaml-duplicate-keys.py` into `validate-dod-release.py` as a blocking gate (F-360's open half).
2. Add an **index-freshness** check: run `generate-p2kb-index.py`, then `git diff --quiet` on the pair. The pair-*consistency* check already exists and just proved itself; **freshness** is the one that is missing, and it is what would have caught the two stale boot-ROM entries.

**The generalisable shape, stated so it is not relearned:** *a defect closed by a one-time repair, with no gate wired to the release path, is a defect scheduled to come back.* F-357 is the proof — repaired 2026-08-26, recurred 2026-09-05.

---

## The hardware selection guide ships 2025 US retail prices as data, in a set with no mechanism to age them (2026-08-30, release fix pass step 1) — F-398

### F-398 — ~15 USD price sites across `p2-hardware-selection-guide.yaml`; needs a policy call, not a citation — `CONFIRMED`

**Not fixed. Registered for a definition call, and it is the sibling of F-374.**

`p2-hardware-selection-guide.yaml` states prices as first-class data — `cost_estimate: "$150-200"`
(6 sites), `total_investment` (2), `cost` (4), `additional_cost` (2), `total_cost` (3),
`"PropPlug programmer required (+$30)"`, `cost_difference: "$30-50"` — under `last_updated:
"2025-09-06"`. No source is cited and none could be: a Parallax guide does not carry retail price,
and the web store's price is a moving target the KB has no mechanism to track.

**Why it is a finding and not a style note.** It fails the same two tests F-374 applies. Nothing
sources it. And the consumer cannot act on it safely: an agent reading `$150-200` states it as
fact to a user who may be reading a year later in another currency, and a KB that is wrong about
money is wrong in a way the reader can check — which is the kind of wrong that costs trust in
everything else on the page. It is also the `feedback_durable_mechanism_over_perishable_catalog`
shape: **vendor facts rot, and this set has no expiry mechanism.**

**Why it is NOT being swept in this pass.** The disposition is a judgement with a real cost either
way — deleting every price guts a guide whose entire purpose is budget-tiered selection, and the
relative ordering (mini breakout cheapest, full add-on set dearest) is durable even when the
absolute numbers are not. That is a definition call of exactly F-374's kind, and this register's
own rule is that a call belonging to Stephen is not made by the agent that found it.

**The options, for whoever takes the call:** (a) delete every absolute figure and keep the relative
tiering; (b) keep them behind an explicit `as_of: 2025-09-06, retail USD, verify at parallax.com`
qualifier on every site; (c) replace the whole cost axis with a pointer to the web store. **(a) is
the recommendation** — it is the only one that cannot go stale, and the guide's decision tree turns
on ordering, not amounts.

---

## The whole top-level cog stack is missing from the KB — no entry says cog 0 has one, where it starts, which way it grows, or that nothing checks it (2026-08-30, debug/stack research) — F-392

### F-392 — the KB documents `cogspin`/`TASKSPIN` stacks and is silent on the stack every Spin2 program already has; the sizing numbers it does ship are unsourced and are cited back as authority — `PARTIAL — the circular-authority half fixed 2026-09-22 («#351»); the top-level-stack documentation is carved out with an expiry`

> **The dangerous half is fixed.** `language/spin2/methods/cogspin.yaml`'s `stack_requirements`
> shipped `minimum: "32 longs"` and `typical: "64-128 longs"` with no source, and
> `application-notes/p2an006-sizing-cog-task-stacks.yaml:77` cited **this file** back as the
> authority for them — a closed loop in which a heuristic became a specification by being written
> down twice. Verified 2026-09-22: **Spin2 v55 contains no `_STACK`, no `_FREE`, and no stack-sizing
> guidance of any kind.** Both sites now mark the figures as heuristics explicitly, say that no
> Parallax document states them, name the circularity, give the high-water-mark measurement as the
> only way to settle a size, and record that P1's `_STACK`/`_FREE` do not exist in Spin2 and have no
> effect if written.
>
> ⏳ **CARVED OUT, expiry: the next Spin2-interpreter ingestion.** Documenting the stack that every
> Spin2 program already has (the top-level cog's, its `DBASE` frame and the 6-long *Drop anchor*
> entry) requires reading the interpreter listing, and **the copy in this repo is v51 while the
> shipped KB targets v55**. Writing v51 internals as current v55 behaviour is precisely the
> tier-mismatch this register exists to prevent, so it waits for a v55 interpreter source rather
> than being guessed. That is the named expiry, not an open-ended deferral.

**Class: OMISSION + UNSOURCED CLAIM.**

**Measured against the shipped set, 2026-08-30:** grepping 1133 files for `top-level object` +
stack, `main cog`, `cog 0.*stack`, `interpreter.*stack` returns **zero** entries describing the
top-level cog's stack. `application-notes/p2an006-sizing-cog-task-stacks.yaml` and its published note
cover `cogspin` and `TASKSPIN` buffers only — grepping the P2AN006 master for `main cog|cog 0|
top-level|default stack` returns nothing.

**All of the following is available in ground-truth sources and none of it is in the KB.**

1. **Cog 0 has a stack, and the compiler places it.** `DBASE` is the stack base and it sits
   immediately after VAR space: the interpreter's launch block computes
   `var_longs = (@test_dbase - @test_vbase) >> 2` and does `setq dbase_init` / `coginit #hubexec,
   ##launch_spin`, which passes `DBASE` into the new cog's `PTRA`
   (`Spin2_interpreter.spin2` v55, launch block). Confirmed against `pnut_ts -m`: a program whose map
   reports `VAR SPACE $0001C-$0005F` has its stack base at `$00060`.
   Spin2 v55 shows the same pair in the DEBUG INIT line — *"the Spin2 interpreter is launched from
   `$00D6C` with its stack space starting at `$010BC`"* (`spin2-v55-text.txt:1036`).
2. **It grows UPWARD, without a bound.** Push is `wrlong v,ptra++`, pop is `rdlong y,--ptra`
   throughout the interpreter. There is **no comparison of `PTRA` against any limit anywhere in the
   interpreter** — the only trace of the idea is the author's own note on line 1 of the source:
   *"TESTT add registers stack_start (on launch) and stack_max (on call or return) to track stack size
   for allocation need."* Nothing detects overflow; it writes forward into whatever is next.
3. **A call frame costs exactly 6 longs, plus the method's locals.** The interpreter's *Drop anchor*
   block pushes `v / pbase / vbase / dbase / mrecv / msend` (`setq #6-1` + `wrlong v,ptra++`), then
   `callgo`'s `.clear` pushes the method's local longs. `launch_spin` lays the same 6-long header at
   the base of **every** Spin2 stack, cog 0 and `cogspin` alike. So the floor for any Spin2 cog stack
   is 6 longs before one parameter is stored — and Spin2 v55:279 permits **64KB of locals in a single
   method**, which is the deep-frame hazard stated in the language's own terms.
4. **What it runs into.** Free hub RAM above the program image, up to `$7FFFF` — or up to `$7BFFF`
   when DEBUG is enabled, because the debugger takes `$7C000..$7FFFF` (see F-393).
5. **What is OBSERVABLE about it, and what is not.** A `cogspin`/`TASKSPIN` stack is an ordinary hub
   buffer, so **any** cog can inspect it — that is what makes cross-cog stack supervision possible at
   all. But `PTRA` is a cog register and *"each cog has its own RAM"*
   (`sources/silicon-doc/silicon-doc-text.txt:137`, `:284`), so **no cog can read another cog's live
   stack pointer.** A supervisor therefore measures the **high-water mark** left in the fill pattern,
   never the instantaneous depth. The only route to another cog's live `PTRA`/PC is `COGBRK` issued
   from inside a debug ISR with the target's `%I` bit armed (`:2520-2524`) — which is precisely the
   escalation path the debug interrupt exists to provide, and worth cross-linking from here.

**The unsourced numbers.** `cogspin.yaml:39` and its `stack_requirements` block ship
`minimum: "32 longs"` / `typical: "64-128 longs"` under `documentation_source: enhanced`. No Parallax
source states either figure — Spin2 v51/v55 give no stack-size guidance at all. `p2an006`'s
`cog_stack_defaults` then cites **`cogspin.yaml`** for "cog stack floor ~32 longs, typical 64-128",
so a published application note rests on a KB value that rests on nothing. Either derive the floor
from the interpreter's frame arithmetic and cite that, or mark both as heuristics and say so.

**Also absent: P1's mechanism is gone and nothing says so.** P1 reserved stack with `_STACK` /
`_FREE` (`p1-propeller-manual-v1.2-layout-text.txt:1272`, `:7002-7014`, and the whole *The Need for
Stack Space* section at `:2682-2726`). **Spin2 has no such symbol.** Proven with `pnut_ts` v1.55.4:
`_STACK = 100` and `_FREE = 100` in a `CON` block each compile to a binary **byte-identical** to the
same program without them (md5 `1e7165f1…` for all three). They are inert user constants. A P1
migrant will reach for them and be silently ignored.

**Correction:** add a top-level-cog stack entry carrying (1)-(4) above with the interpreter and
Spin2-doc citations; re-source or re-label `cogspin.yaml`'s sizing numbers; state the `_STACK`/`_FREE`
non-existence on the P1-differences surface, and carry (5)'s observability split — inspectable hub
buffer, private `PTRA`, high-water not live depth.

**The technique answer, corrected 2026-08-30 by the reporter's actual rig.** An earlier draft of this
entry said "move deep work into a `cogspin` cog whose buffer you own" — i.e. get off cog 0. **That is
the wrong lesson from (1)-(3).** The rig in use is a driver in a back cog with several front cogs
exercising it, and **cog 0 is kept alive deliberately as the supervisor**: it watches the front cogs'
stack buffers and is still able to report when they lock up. Cog 0 earns that role *because* of this
finding, not despite it — it is the one cog whose stack cannot be sized or guarded, so it is the one
cog you keep **trivially shallow by construction** (flat loop, no nesting, no large method locals),
which also makes it the likeliest survivor. Parking cog 0 (`org` / `jmp #$` / `end`, F-394) is not the
pattern; it is a **control applied to a suspect cog**, and in this topology the suspect is a front
cog. The page must not imply that cog 0 is a place to evacuate.

---

## DEBUG's cost to the running application is nowhere in the KB: 16KB of hub gone, the protection LOCKED until reset, `LOCK[15]` taken, two pins consumed (2026-08-30, debug/stack research) — F-393

### F-393 — the KB documents DEBUG's syntax and display commands and not one of the resources DEBUG takes away from the application — `PARTIAL — the load-bearing residue applied 2026-09-22 («#351»); the protected-region layout ($FEA00/$FF1A0) is still absent from the KB (re-verified 2026-10-05 «#386»)`

> Most of this had already landed (`debug-strategy-guide.yaml:77-94` carries the hub `$7C000..$7FFFF`
> reservation, `LOCK[15]`, P62/P63, the HUBSET `L`-bit lock, the ≥10 MHz crystal requirement and the
> per-cog debug interrupt). **Two residues were still open and are now applied:**
>
> 1. ⭐ **The interrupt-retrigger hazard, which is the one that does not look like a timing cost.**
>    `spin2-v55-text.txt:1070-1071`: an interrupt requested during a DEBUG command runs after the
>    DEBUG completes, but the response can be skewed so far that the ISR's own RETRIGGER SETUP does
>    not happen — and the interrupt cycling then stops **permanently**, not merely late.
>    High-frequency cyclical smart-pin interrupts are the prone case (an ISR doing `AKPIN` to drop
>    INA/INB so the next edge re-arms it can miss the window). CT-based interrupts are immune. The
>    fail-safe — issue DEBUG only from cogs not running background ISRs — is carried with it. A
>    working ISR that simply ceases is the hardest DEBUG symptom to attribute, which is why this
>    item mattered more than its size suggests.
> 2. **The cross-link from `LOCKNEW`.** An agent reading `language/spin2/methods/locknew.yaml` was
>    never told a DEBUG build takes one of the sixteen locks before the program runs. It now points
>    at the debug-build cost list.
>
> ⏳ **Not done, low value, expiry: the next DEBUG touch** — the protected-region layout
> (`$FC000`/`$FEA00`/`$FF1A0`/`$FFC00`) is still absent from `architecture/debug_interrupt.yaml`
> and `architecture/hub.yaml`.

**Class: OMISSION — every item here changes what an application may legally do, and each one fails
silently when violated.**

**Measured 2026-08-30:** across the shipped set, `debugger occupies|reserves|allocated by the
debugger` returns **0 files**; `top 16|last 16` returns only two lines, neither of which says the
region becomes unavailable; the ≥10 MHz-crystal precondition appears in no file.
`LOCK[15]` appears once, at `language/spin2/statements/debug.yaml:93`, and only as a note that `DLY`
*releases* it — the KB never says the debugger **holds** it.

**The full set, from Spin2 v55 *Things to know about the DEBUG system*
(`spin2-v55-text.txt:897-930`) and the debugger's own source (`Spin2_debugger.spin2` v51):**

| resource | fact | source |
|---|---|---|
| hub RAM | *"The debugging program occupies the top 16 KB of hub RAM, remapped to `$FC000..$FFFFF` and write-protected. The hub RAM at **`$7C000..$7FFFF` will no longer be available**."* | v55:900 |
| protection lock | the debugger issues `HUBSET $2003_00FF` — `L=1`, so write-protect and the per-cog enables **cannot be changed again until reset** | `Spin2_debugger.spin2:172`, `:121`; format at `silicon-doc-text.txt:2749-2752` |
| `LOCK[15]` | the debugger allocates **all 16** locks then returns 14..0, *"leaves lock[15] allocated"*, and each debug ISR does `locktry #15` / `lockrel #15` | `Spin2_debugger.spin2:77-82`, `:201`, `:235` |
| P62 | DEBUG serial TX, 2 Mbaud 8-N-1 | v55:907 |
| P63 | held in **long-repository mode** carrying `clkfreq`; **must be rewritten on every clock change** or the debugger's baud goes wrong | v55:926, and the worked `clock_change` snippet at v55:1061 |
| clock | *"you must configure at least a 10 MHz clock derived from a crystal or external input. You cannot use RCFAST or RCSLOW."* | v55:899 |
| interrupts | DEBUG skews ISR cycle-frame timing; a smart-pin ISR that re-arms on INA/INB **rise** can miss its retrigger and **stop cycling altogether**. CT interrupts are immune. | v55:1071 |
| DEBUG record cap | 255 `DEBUG()` statements (`BRK #1..255`) | v55:909 |

**The exact protected-region layout is also available and unrecorded** — `Spin2_debugger.spin2:20-49`
maps it: `$FC000` DEBUG data · `$FEA00` cog N reg `$010..$1F7` buffer · `$FF1A0` debugger + overlays ·
`$FFC00..$FFFFF` the eight per-cog `$000..$00F` buffer/ISR pairs whose addresses are *fixed in
silicon* (Silicon Doc Table 25, `silicon-doc-text.txt:2442-2477`).

**Why each is an instability source, not trivia:** a program that keeps a buffer at the top of hub
works undebugged and has its writes **silently dropped** under DEBUG; `LOCKNEW` returns one fewer
lock under DEBUG, so a program that allocates a fixed count fails only when debugged; a `HUBSET`
clock change without the P63 repository update leaves the debugger emitting garbage that reads as a
dead application; and the interrupt-skew item makes a working smart-pin ISR stop for good.

**Correction:** one *DEBUG system requirements and resource cost* entry carrying the table above, with
`aliases` written as symptoms (*"works without debug fails with debug"*, *"debug output stopped after
clock change"*, *"lock count differs under debug"*, *"top of hub RAM not writable"*), cross-linked
from `architecture/hub.yaml`, `architecture/debug_interrupt.yaml`, `locknew.yaml`, and the DEBUG
statement pages. This overlaps F-383's DEBUG-budget finding — file the two together so the reader
gets cost and limits on one page.

---

## The DEBUG budget: we ship all three limits and none of what they cost (2026-08-30, P2KB-GAPS-RUNNING-LOG GAP-4) — F-383

### F-383 — `p2kbSpin2DbgDebugStrategyGuide` lists three peer numbers, and the one that mutes a board is not marked — `PARTIAL` (re-verified 2026-10-05 «#386»: parts (a)(c)(e)(g) shipped; the stale "hit first" bullet, the byte column, the DEBUG_MASK per-object limit and the coalesce mapping remain)

**Class: MIXED — parts (a)(c)(e)(f) are BEHAVIOUR to be proven by test; parts (d)(g) are TECHNIQUE and
need their conditions stated. Part (b) is an editorial correction.**

**START WITH THE CREDIT, because it changes what is being asked for.** The guide already documents all
three hard limits, and the reporter confirmed one of them exactly: **255 debug statements compile, 256
fails** with the compiler's own text *"DEBUG data is too long: too many records: max 255"* (measured
2026-08-28, pnut-ts). `unique_debug_records: 255` is **right**. The guide's compile-time vs runtime
split is also right, including the `reduces_record_count` column correctly marking `DEBUG_COGS` and
`debug IF()` as no help to the record budget. **This entry is not a complaint about that table.**

**(a) The 16 KB cap's failure mode is a silent mute board, and nothing says so.** Verified here: the
guide states *"All debug records combined cannot exceed 16,384 bytes"* and says **nothing** about what
crossing it does. Measured by the reporter 2026-08-27: over the cap **the debug subsystem is dead at
load and the program prints nothing at all** — not even a banner placed before every other statement —
and **pnut-ts emits no error and no warning.** On hardware that is indistinguishable from a dead
board. It cost their bench an evening; every mechanical check they ran passed, because none of them
can see this. ⭐ **The contrast is the finding:** the 255-record limit fails **loudly at build time
with a named error** and can never mute a board; the 16 KB limit fails **silently, at load, on
hardware**. We list them side by side as three peer numbers with the dangerous one unmarked.

**(b) Our headline claim is the opposite of their experience.** The guide says twice that the
255-record limit is *"the one you'll hit first"*, and its entire `decision_guide` is keyed to statement
**count**. They hit the **byte** cap first and not narrowly — 18,077 bytes while still under 255
records. A vehicle whose diagnostics are long formatted lines burns bytes far faster than slots.
**A reader following our decision table monitors the limit that would have warned them and stays blind
to the one that mutes the board.**

**(c) What the 16 KB counts is never stated.** Measured: it counts `debug()` **format strings** across
the whole program plus per-statement overhead, and ⭐ **does NOT count DAT strings.** That one sentence
is what makes the budget manageable and it appears nowhere in the KB.

**(d) ⭐⭐ THE REMEDIES TARGET DIFFERENT BUDGETS, AND APPLYING THE WRONG ONE ACHIEVES NOTHING.**
Verified here: `mechanisms_overview.table` carries `reduces_record_count` and **no byte column at
all**, so a reader over the byte cap finds a table that cannot answer their question.

⭐ **ONE SOURCE, NOT TWO — and it changes how this table should be read.** The gaps log is not a
third-party field report: it is **Stephen's own practitioner experience, recorded by an agent he
directs on a project he drives.** He taught that agent these techniques. So the document and the
conversation are the same source in two formats, and any entry here that reads as *"the reporter
measured X, and separately Stephen asserted Y"* is describing a distinction that does not exist.

**Stephen, 2026-08-30:** `zstr_()`, in-memory formatting, `DEBUG_MASK`, and **coalescing strings so
fewer `zstr_()` calls are needed** are all things he *"over time had to be taught to the agents having
issues"* — repeatedly, to different agents, because none of it is written down anywhere they can
reach. **A technique that must be re-taught to every agent by the person who knows it is the exact
content this knowledge base exists to carry.** And his governing point: **they work against different
limits.**

**The technique set, with what is measured separated from what is asserted:**

| technique | targets | status |
|---|---|---|
| move prose into `DAT`, emit with `zstr_()` | **BYTES** — DAT is not counted by the 16 KB cap | **MEASURED**, with the measurement recorded |
| merge statements — format several values into one line, emit once | **RECORDS** — the 255 slots | **MEASURED**, with the measurement recorded |
| `DEBUG_MASK = 0` in a child object | **BOTH** — zero bytes *and* zero records | **MEASURED**, see (e) |
| **coalesce strings so fewer `zstr_()` calls are needed** | ⚠ **mapping owed — see below** | **IN PRODUCTION USE** |
| **in-memory formatting** — build the line in a buffer, emit once | ⚠ **mapping owed — see below** | **IN PRODUCTION USE** |

⚠ **WHAT IS ACTUALLY MISSING IN THE LAST TWO ROWS, corrected 2026-08-30.** An earlier draft of this
entry marked them "not yet tested" and treated them as weaker than the first three. **That was wrong,
and the reason was bad**: all five come from the same project, and these two were discounted only
because they arrived in conversation rather than inside the log document. That is a distinction of
channel, not of evidence. **Both are in active production use in a driver whose correctness that team
measures to the SCK edge count.**

**The genuine gap is narrower and it is ours.** The *budget each one targets* was never stated by the
source — an earlier draft **inferred** it and then presented the inference as the source's unproven
claim. That inference has been removed. Since this section's whole point is that applying the wrong
remedy achieves nothing, **the mapping is the load-bearing content and must come from the
practitioner or from a measurement, never from us reasoning about how the compiler probably works.**

**Two ways to close it, cheapest first:** ask the practitioner which limit each technique addresses —
he taught them and knows; or run the two-compile subtraction from (g) against a vehicle at a known
byte and record count, which additionally yields a magnitude the KB can quote. **The mapping is what
is owed here, not proof that the techniques work.**

⛔ **And every one of them needs its boundary.** A workaround exists because of a limit and stops
working somewhere; a technique published without the condition that bounds it is how the next
generation of wrong entries is made. `DEBUG_MASK`'s boundary is already known — see (f): it cannot
be overridden at instantiation, and the `-D` that drives it is global.

**A team that learns only the DAT technique sheds bytes for weeks and never moves the record count,
and will not understand why.** The reverse holds too. **This is the most useful thing in the report
and we have no equivalent.**

**(e) ~2,945 bytes are gone before the first `debug()` — 18% of the budget.** Measured twice: a bare
vehicle with no driver reads 2,945; a minimal vehicle **plus the entire driver** reads 2,945. Two facts
in one measurement — fixed subsystem overhead takes ~18% before you write anything, and **a child
object compiled with `DEBUG_MASK = 0` contributes zero BYTES, not merely zero records.** We state the
record half for `DEBUG_DISABLE`; the byte half is unstated and it is the half that decides whether a
large library is safe to include.

**(f) `DEBUG_MASK` cannot be overridden at object instantiation.** Every example defines it as a `CON`
in the file that uses it and nothing says a parent cannot set a child's mask. It cannot. **Their
workaround, worth publishing with the gap:** derive `DEBUG_MASK` from an ordinary `CON` and drive that
`CON` from the build with `-D`. ⚠ **Condition that must travel with it:** `-D` in pnut-ts is **global**
— it reaches every object in the compile, which is what makes the technique work and also what makes
it blunt.

**(g) We tell readers to monitor the budget and never say how.** *"Use regular debug() but monitor your
count"*, with no method. **The method is two compiles and a subtraction:** build once without `-d`,
once with `-d`, subtract the binary sizes — the difference IS the debug data. Deliberately dumb, and
that is its virtue: nothing to drift from what the compiler actually did. ⚠ **Condition:** an earlier
attempt to estimate the same quantity by regex-counting literals and subtracting from a measured total
produced a confident wrong answer. A subtraction between a measured quantity and an estimated one is
an estimate and will be read as a measurement unless labelled.

⛔ **WHAT WE MUST NOT DO WITH THIS ENTRY.** The reporter has **not** verified that 16,384 is the true
byte ceiling. Their gate is **13,332** (*"the highest value MEASURED to work… a known-good point, not a
proven ceiling"*) and **17,821** is measured to fail. **The ceiling is un-bisected between those**, and
our 16,384 sits inside that interval uncontradicted. Only `255` is confirmed. Any rewrite that presents
all three numbers as confirmed launders an assumption into a fact.

**Correction.** (1) State what exceeding `total_debug_data` does, beside the number, and mark it the
silent one against the record limit's loud one. (2) Re-scope the which-limit-hits-first claim.
(3) State what the 16 KB counts, and the fixed overhead. (4) Add a byte column to
`mechanisms_overview` plus the DAT/`zstr_()` and statement-merging pair. (5) Give the two-compile
subtraction as the method. (6) State that `DEBUG_MASK` is per-object with the `CON`+`-D` workaround and
the global-`-D` caveat. (7) Make the page reachable — see **F-389**.

---

## An improvement to the general smart-pin page made a contradiction with the mode page SHARPER (2026-08-30, P2KB-GAPS-RUNNING-LOG AMBIGUOUS-5) — F-386

### F-386 — `p2kbArchSmartPins` now warns by name against the call `p2kbArchSmartPin01110CountAEdgesOptionalBDec` demonstrates twice — `PARTIAL — the named page fixed and verified 2026-09-22 («#351»); the class sweep is owed`

> **The named page is done, verified in the tree 2026-09-22.**
> `architecture/smart-pins/smart-pin-01110-count-a-edges-optional-b-dec.yaml:64-65` now runs `dirh`
> before `wypin` with the comment `' Count A only - Y AFTER DIRH`; `:70-83` adds a
> `configuration_order:` block stating the universal order and recording "(This page previously
> showed WYPIN before DIRH.)"; `:77-83` explains that `%01110` is a counting rather than a trigger
> mode, so the general page's exclusion does not apply, and marks the immunity question as NOT
> STATED by any source we hold.
>
> ⏳ **OWED, with a named expiry — the next smart-pin touch:** the finding also required sweeping
> the other ~30 mode pages under `architecture/smart-pins/` for the same shape (`wypin` before
> `dirh`, and `pinstart(...)` used in a trigger mode). That sweep has NOT been run. It is
> mechanical and bounded; it is not a blocker for the current release because the demonstrated
> defect is fixed, but it is exactly the "whole family, not the site you tripped over" rule and it
> must not be left to be rediscovered.

**Class: AMBIGUITY — and a regression created by a good change, which is the notable part.**

**Verified here 2026-08-30.** `architecture/smart_pins.yaml:115` now states:
*"**PINSTART()/pinstart() writes Y before raising DIR, so it is NOT safe for** the trigger modes — use
the explicit sequence below for those."* Meanwhile
`architecture/smart-pins/smart-pin-01110-count-a-edges-optional-b-dec.yaml` still shows
`pinstart(counter_pin, P_COUNT_RISES | P_PLUS1_B, 0, 1)` at **`:47` and `:56`**, and its PASM example
still runs `wypin` at `:64` before `dirh` at `:65`.

**Before, two pages disagreed. Now one page explicitly warns against what the other page demonstrates
twice.** For `%01110` the consequence is probably benign — `Y[0]=0` is the reset default — **but a
reader cannot know that from either page**, and the general page's whole argument is that one order is
always right.

**The lesson for the sweep discipline:** strengthening a general page without sweeping its mode pages
converts a quiet inconsistency into a loud one. This is the class the register's own class-wide-sweep
rule exists to prevent, arriving from the direction of an improvement rather than a defect.

**Correction.** Make the per-mode examples follow the universal order, or state on the mode page why
this one differs and that it is safe. Then sweep every other mode page for the same shape.

---

## `||` means logical OR in P2 and absolute value in P1, and the page that flags exactly this hazard twice does not flag it (2026-08-30, P2KB-GAPS-RUNNING-LOG AMBIGUOUS-6) — F-387

### F-387 — `language/spin2/concepts/operators.yaml` annotates `~` and `~~` as P1 differences and leaves `||` unmarked — `PARTIAL — the `||` note applied 2026-09-22 («#351»); the P1-changed-operator class sweep is owed`

> **Applied 2026-09-22.** The `["||", "OR"]` entry now carries the same shape of note the `~`/`~~`
> entries already had: *"P2 Spin2 semantics; not P1 absolute value. In P1 '||' was the Absolute
> Value operator. For absolute value on P2 use ABS."*
> **Sources:** P1 `p1-propeller-manual-v1.2-layout-text.txt:5417-5419` ("The Absolute Value
> operator… returns the absolute value (the positive form) of a number"); P2
> `spin2-v55-text.txt:491` (`||, OR … Logical OR`).
> ⚠ **A caveat was raised and resolved before writing:** v55's `ABS` row (`:432`) is annotated
> "CON only *", which looked like it barred recommending ABS. It does not — that column's header is
> **"Floating-Point Operator"** (`:427`), so the marker scopes the operator's FLOATING-POINT
> behaviour to CON blocks. `-` (negate) and `*` (signed multiply) carry the identical marker. ABS is
> an ordinary runtime operator.
>
> ⏳ **OWED, expiry: the next Spin2 operator touch** — the finding's second half asks for the full
> class of operators that changed meaning from P1 (`=>`, `=<` and others) to be swept and annotated.
> Only `||` was done.

**Class: AMBIGUITY, with a near-miss cost recorded.**

**Verified here 2026-08-30.** `:288` and `:294` each carry *"P2 Spin2 semantics; **not P1
sign-extend**. For sign-extend use SIGNX."* — on `~` and `~~`. `||` at `:101` is listed correctly as
*"Logical OR"* and carries **no P1 note at all**.

**`||` is the more dangerous of the three**, because a P1 habit meaning "absolute value" becomes a
boolean inside an arithmetic expression. The reporter got lucky: `||(a - b)` failed to parse. **A P1
habit that *does* parse — `||` between two non-zero values yielding `-1` instead of a magnitude —
compiles clean and produces a wrong number**, in their case in a driver where a wrong phase pad means
silent whole-sector write corruption.

**It joins a family we have already paid for:** P1's `=>` / `=<` versus P2's `>=` / `<=` — same shape,
an operator existing in both languages with different meaning, documented correctly for P2 and never
flagged as changed.

**Correction.** Add a P1-difference note on `||` matching the ones on `~` and `~~`, naming `ABS` as the
P2 spelling. Then author an *"operators that changed meaning from P1"* section — **two hits are
unlikely to be the only two, and this should be a class sweep, not a single edit.**

---

## The index returns partial results by construction: 27 of 60 debug files reachable, and nine DEBUG-window pages carry no searchable trace of the word (2026-08-30, measured; corroborates P2KB-GAPS-RUNNING-LOG FINDABLE-1/2/3) — F-389

### F-389 — key generation abbreviates and drops path components, so whole subtrees vanish from the term that names them — `PARTIAL` (re-verified 2026-10-05 «#386»: alias vocabulary added in places; the generator still abbreviates and has no component-survival check)

**Class: FINDABILITY — a defect in the index generator, not in any entry's content.**

**Measured 2026-08-30 against the live index (1133 files, 2082 aliases):**

| | |
|---|---|
| files reachable by searching **"debug"** (key or alias) | **27** |
| files with substantial debug content (≥5 mentions) | **60** |
| **substantial debug files UNREACHABLE by "debug"** | **33** |

**Three mechanisms, all visible in one directory listing:**

1. **Abbreviation in the generated key.** `debug-commands/c-z.yaml` → `p2kbSpin2Dbg**CZ**`. "debug"
   does not substring-match "Dbg", so `c-z`, `dly`, `pc_key`, `pc_mouse` are invisible — while
   `debug-formatters-binary.yaml` → `p2kbSpin2Dbg**Debug**FormattersBinary` **is** reachable, only
   because its filename repeats the word. **Within one directory, some files return and some do not,
   decided by whether the filename happened to say "debug" twice. That is the partial-results failure
   mode, exactly.**
2. **A whole directory dropped from the key.** Every file in `debug-displays/`: `scope.yaml` →
   `p2kbSpin2Scope`, `plot.yaml` → `p2kbSpin2Plot`, likewise `logic`, `bitmap`, `fft`, `midi`,
   `spectro`, `term`, `scope_xy`. **Nine DEBUG window pages, and the word "debug" appears in none of
   their keys.**
3. **Debug content not *named* debug.** `brk.yaml` (35 mentions, the breakpoint instruction),
   `getbrk.yaml`, and the preprocessor files `ifdef`, `define`, `external-symbols`,
   `preprocessor-overview` — **which are how you turn debug statements on and off**, the exact thing
   the reporter went looking for.

**The reporter's independent corroboration**, from the user side:

| query | result |
|---|---|
| `p2kb_find "debug data too long"` — **the compiler's own error text** | **0 results** |
| `p2kb_find "16KB debug limit board prints nothing"` — the symptom | **0 results** |
| `p2kb_find "smart pin measure time"` | **0 results**, while `category:"smart_pins_timing"` returns 8 keys |
| `p2kb_get "smart pin AAAA input selector relative neighbor pin read state"` | 20 suggestions, and **`p2kbArchSmartPins` — the page holding the AAAA table — was not among them** |

**Neither the error a compiler prints nor the symptom a developer sees reaches the page that explains
both.** And `p2kbSpin2DbgDebugStrategyGuide` is titled *"Managing the 255-Record Limit"*, so a reader
hunting a **byte** cap has no reason to open it.

**Why this is systemic and predictable.** `generate-p2kb-index.py` builds keys from paths, abbreviating
some components and dropping others. **Any directory whose name is abbreviated or dropped loses its
whole subtree from the term that names it.** `debug-displays` is the instance found; it will not be
the only one — that is mechanically checkable by testing, for every path component in the corpus,
whether it survives into the keys beneath it.

**A third instance, found while filing this entry — and it is the sharpest one yet, because the
content is excellent.** The reporter named the 16-long inline-PASM ceiling as *"the one we would most
like documented somewhere findable"*, having redesigned around it twice. **It is documented, and
documented well**: `language/spin2/constructs/inline_pasm.yaml` carries a `variable_limit` block —
`total_longs: 16`, with the breakdown *"First 16 long variables (params + result + locals) are copied
to cog registers $1E0..$1EF. This 16-long limit applies to VARIABLES ONLY — not to the PASM code
itself"* — plus a separate `code_size_limit` that correctly distinguishes the two. It even lists
*"What's the size limit on an inline PASM block?"* among its own questions.

Probed against the live index 2026-08-30:

| query | result |
|---|---|
| `"Local variable must be LONG and within first 16 longs"` — **the compiler's exact error text** | **MISS** |
| `"inline PASM variable limit"` | **MISS** |
| `"16 long variable limit"` | **MISS** |
| `"how many locals can inline PASM use"` | **MISS** |
| `"inline pasm"` | substring hit only |

**Only someone who already knows the feature's name can reach it.** A developer meets this limit as a
compiler error, and the error text reaches nothing. This is the strongest argument in the entry for
alias vocabulary built from **symptoms and compiler strings** rather than feature names: the page needs
no content work at all, and it is still effectively unreachable by the person who needs it.

**Related, and it generalises the fix.** FINDABLE-1 records that *"`TESTP` on a smart pin returns the
flag, not the level"* is stated **per mode**, so a reader must already suspect it to go looking. The
reporter's phrasing is the principle this finding turns on: *"That is the difference between documented
and discoverable."*

**Correction.** Three separable pieces. (1) Repair the key generator so a path component is not
silently lost or abbreviated below searchability — with a negative control proving a dropped component
is detected. (2) Run the component-survival check corpus-wide and publish the hole list. (3) Add
aliases carrying the **task and symptom vocabulary**, not only the name of the thing — compiler error
strings among them. **92% of shipped files carry zero aliases** (1048 of 1132), so (3) is a corpus-wide
programme, not an edit; it should be scoped from the hole list rather than started blind.

---

## Citing ONE block in a wholly-uncited file turns its other blocks Tier-1 RED — 32 uncited quantity blocks across 24 files are structurally invisible to the blocking gate (2026-08-29, «#334», proved by accident) — F-381

### F-381 — the Tier-2 advisory class is not "reviewed and accepted", it is "no control available" — `CONFIRMED`

**How this was proved, rather than argued.** «#334» added silicon-limit citations to three clock
files. `audit-yaml-claim-sourcing.py` went from **0 Tier-1 violations to 12** — not because
anything was broken, but because the three files had previously cited *nothing anywhere*, which
put every quantity block in them in **Tier 2 (advisory, non-blocking)**. Adding one real citation
made each file "a file that cites", and the gate's own Tier-1 rule then applied:

> block `X` states N quantities with no source; **this file DOES cite elsewhere — its own other
> sections are the control**

All 12 blocks had been uncited the whole time. Nothing changed about them. What changed is that
they became *visible*.

**The measurement, taken at HEAD after «#334» closed.** 32 advisory blocks across **24 files**:

| area | files | note |
|---|---|---|
| `architecture/decomposition/` | 5 | the reasoning layer — Hz/ms budgets in worked derivations |
| `architecture/smart-pins/` | 8 | mode pages: `detailed_description`, `code_examples`, `notes` |
| `community/obex/objects/` | 3 | object metadata (MHz, Mbps) — community-sourced provenance |
| `hardware/` | 2 | `hardware-compatibility-matrix` (V, mA, Hz), `p2-hardware-selection-guide` (A, V, mA) |
| `language/` clock + timing | 6 | `hubset`, `asmclk`, `clkset`, `waitct`, `clkfreq`, `single_communication` |

Each is one citation away from turning that file's remaining blocks red.

**Measured 2026-08-30 — the count is exactly 32, and this entry originally said otherwise.** It
first claimed 32 was only what the gate could *name* and that the true number was larger, reasoning
from the «#334» sample where 3 files yielded 12 blocks. A simulation settles it: insert one
recognised citation into each of the 24 files, run the gate, count that file's blocking rows,
restore. The total is **32**, identical to the advisory count, and the «#334» sample was consistent
all along — those three files held **16** advisory blocks, of which 12 surfaced as blocking and 4
were covered by the citations added. **The blind spot is real; its size was never underreported.**
Full measurement in `engineering/analysis/2026-08-30-yaml-defect-census.md` §2, with the per-file
breakdown.

**Why this is a gate-design finding and not just a backlog.** The tool's banner says Tier 2 is
"advisory by design, non-blocking, and its population is not zero", which reads as a considered
exemption. It is not one. The exemption exists because the gate judges a block against **its own
file's other sections as the control**, and a wholly-uncited file supplies no control. That is a
sound reason to avoid a false positive and an unsound reason to conclude the block is fine —
`audit-constant-fidelity` has the same shape and the same banner ("name coverage is not semantic
coverage"). The practical consequence: **the least-sourced files in the corpus are the ones the
blocking gate cannot block on.**

**Related and distinct.** F-353 counted in-scope blocks that returned cited. F-375 is the delivery
filter stripping citations that ARE present. This one is about blocks that were never cited and
cannot be reported as blocking. F-340/F-373 are the cross-reference analogue — a gate printing
green over sites it does not read.

**Not started.** Deciding whether all 24 get cited, or whether some areas carry a declared
exemption (OBEX object metadata is community-sourced and may not have a Parallax citation to give;
the decomposition layer is a reasoning layer, not an extraction), is a scope call, not a repair to
start unasked. What «#334» fixed is only the three files it touched.

---

## Two residues the gates cannot see: a citation re-anchor that translated line numbers, and an eighth fabricated-provenance file (2026-08-27, «#325» verification) — F-377

### F-377 — F-365's re-anchor left locators that are in range and point at nothing; `io_pin_timing.yaml` cites a silicon-doc part file that does not exist — `PARTIAL` (re-verified 2026-10-05 «#386»: part 2 fixed; clock_system.yaml still cites spin2-v55-text.txt:1718 and :1716-1725 for text that sits at :1711 and :1709)

**DISCHARGED 2026-08-30 by F-399.** Part 1 (the translated-locator class) is closed the only way it can be: all **721** citation locators in the shipped set were opened at their cited lines and read. 22 were repaired — 18 pointing at content that does not support the claim, of which **10 were exactly this carry-over shape** in `pin-capture.yaml` and `pin-selection.yaml`; the two named in this entry (`dds-goertzel.yaml`) are among them. A corpus-wide carry-over detector now returns **zero** across all 222 `silicon-doc-text.txt` citations. Part 2 (`io_pin_timing.yaml`'s fabricated `part3-pins.txt`) was repaired earlier and its replacement locators were re-read in the F-399 sweep. **See F-399 for the method, the totals, and the two instrument defects that had to be fixed before any of it could be trusted.**

**Part 1 — the re-anchor residue.** F-365 moved 23 shipped citations from the superseded
`p2-documentation.txt` to `silicon-doc-text.txt`, and its own instruction was explicit: *verify each
against the new artifact; never translate line numbers.* Some were translated anyway.

`architecture/streamer/dds-goertzel.yaml:74` cites `silicon-doc-text.txt:1565 and :4062-4095`.
**`:1565` is correct** — it carries *"S[19:0] supplies a 20-bit value which is used to configure the
DDS/Goertzel mode"*. **`:4062` is a blank line.** The same file's `:303` cites `:1636` (`' Setup`,
plausible) and `:4289-4305`, where `:4289` reads `[t34 r3c1] %0000` — a table-cell marker, not the
mode/data longs claimed. `application-notes/p2an002…:103` carries two more of the same shape.

**No instrument can catch this, and that is the point.** A class-wide range check over every
`silicon-doc-text.txt:NNN` citation in the shipped set — **113 citations, file is 5626 lines** —
returns **0 out of range**. A translated locator lands inside the file and reads as valid to
anything that checks bounds. Only opening the line catches it. The suspect set is bounded and
small: the 23 citations F-365 moved.

**Fix.** Re-verify those 23 by *reading* each cited line and confirming it carries the content the
citing block claims — the discipline F-365 stated and did not fully execute. Where it does not,
locate the content in the artifact; do not adjust the number.

**Two more of the same shape, found by «#326» and confirmed by the arbiter — and note they are NOT
F-365 residue, which widens the class.** `architecture/clock_system.yaml`
`anti_patterns.conflicting_definitions.source` cites `spin2-v55-text.txt:1716-1725` for the
sentence *"These symbols must be defined in one of the following combinations"* — that sentence is
at **`:1709`**; `:1716` is the `_rcslow` table row. And `anti_patterns.missing_crystal_frequency.source`
cites `:1718` for the verbatim *"Selects XI/XO-crystal-plus-PLL mode, assumes 20 MHz crystal"* —
that is the `_clkfreq`-alone row at **`:1711`**; `:1718` reads *"No symbol and not DEBUG mode"*.
Both quotes are accurate, both locators point at a different row. `«#326»` also found the same
shape in the differential-read artifact it was handed (a datasheet footnote given as `:2205`, the
`Cin` Mode 3 row, where footnote 2 is at `:2209`).

**So the class is wider than F-365's 23.** Any citation written by translating a number rather than
locating content has this shape, whatever pass wrote it. The sweep should cover every
`spin2-v55-text.txt:` and `p2-datasheet-text.txt:` locator in the shipped set, not only the
re-anchored ones.

**Part 2 — an eighth fabricated-provenance file.** F-359 named seven `architecture/` files carrying
headers that cite silicon-doc part files which have never existed; one was purged and «#323»
re-derived the other six. **`architecture/io_pin_timing.yaml` is an eighth and was never in the
list.** It carries `# Silicon Doc Reference: part3-pins.txt, pages 5-8` at `:2` and
`"part3-pins.txt, Pin Timing Specifications"` at `:193`. The silicon-doc folder contains
`part3-end.txt`, `part3-interrupts.txt`, `part3-pages-37-38.txt`, `part4-locks.txt` and
`part4-smart-pins.txt` — **there is no `part3-pins.txt`**. Same defect, same mechanism: the header
satisfies the citation regex, so the sourcing gate reads the file as cited.

**Fix.** Re-derive it against `silicon-doc-text.txt` exactly as «#323» did the six, and collect
anything that cannot be re-derived rather than deleting it.

**Also repaired on the spot during this verification** (not deferred, one line):
`architecture/interrupts.yaml:27` asserted *"Each interrupt level has its own set of shadow
registers"* while `:43` of the same file, rewritten by «#323» from the source, states *"There are
no shadow register banks."* «#323» corrected the detailed block and left the summary paragraph
contradicting it. The summary now points at `automatic_state_save` instead of restating it.
A prose self-contradiction is invisible to every gate here — the encoding check that verified this
file cannot read sentences.

## The delivery filter strips `documentation_source:` from every file it serves, and 706 of those values are real citations (2026-08-26, «#324» verification) — F-375

### F-375 — a remote agent receives 383 of our files with their source line deleted, and the gate that checks the filter cannot see it — `PARTIAL — gate half RESOLVED 2026-09-11; the 383-file rename remains Stephen's scope call`

**The mechanism.** Both delivery paths run the same five-pattern line filter:
`engineering/tools/p2kb/fetch-kb-file.sh:189` and the `FilterMetadata` contract recorded in
`engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`, designed in
`engineering/tools/p2kb/METADATA-FILTER-DESIGN.md`, which describes `documentation_source` as
*"Original doc reference"* — internal bookkeeping not worth shipping.

**That premise is false for the overwhelming majority of them.** Measured 2026-08-26 across all
1133 shipped files:

> **706 `documentation_source:` / `enhancement_source:` values are citation-shaped** — they name a
> document, an edition, a page or a line. **47 are the bare internal tokens the filter was designed
> for** (`enhanced` 16, `original` 15, `p2_datasheet` 8, `code_analysis` 2, and three singletons).
> The citation-shaped values sit in **383 distinct files**.

Examples of what is deleted on the way out:

| File | Value stripped in delivery |
|---|---|
| `language/spin2/assembly-directives/alignl.yaml` | `PASM2 Manual 2022/11/01 Pages 31-147` |
| `language/spin2/registers/pr-registers.yaml` | `PASM2 Manual 2022/11/01 Page 118` |
| `language/spin2/debug-commands/pc_key.yaml` | `Spin2 v51 (debug-section.txt) + PNut v55 directive matrix` |
| `language/spin2/statements/debug.yaml` | `PNut v55 compiler source (p2com.asm: check_word_chr_initial/check_word_chr @8888, debug_symbols table @19335, parse_debug_string, symbol_size_limit=30); hardware-isolated on real silicon 2026-07-27` |

**Why this is the sharpest form of a defect this project already knows.** The shipped set carries
the **agent-consumer** bar — *cite or omit*, because a remote agent cannot weigh a hedge and a
wrong fact becomes silently authoritative in generated code. The filter takes files that satisfy
that bar on disk and delivers them **not satisfying it**. Every gate we run reads the tree; the
consumer reads the filtered stream; nothing compares the two. The KB is cited. What we *serve* is
not.

**Second half, and it is why this was never caught.** `validate-dod-release.py`'s
`validate_metadata_filter` (lines 352-396) checks *which line-patterns the filter removes* and
never re-parses the filtered payload — there is no `yaml.safe_load` and no type comparison anywhere
in the function. «#324» proved the consequence: a block whose only child is `documentation_source:`
is delivered as `null`, and the check passes clean. **The filter is indentation-blind, so it can
destroy a block outright**, and the gate that exists to watch it is measuring the wrong thing.
*A gate must read the artifact* — this one reads the pattern list.

**Fix (two parts).**
1. **Filter:** stop deleting `documentation_source:` / `enhancement_source:` wholesale. Either
   deliver them, or delete only the 47 bare-token values and keep every citation-shaped one. The
   cleanest form is the one the project already uses everywhere else — rename the real ones to
   `source:` and let the filter keep its narrow meaning. That is 383 files, so it is a task.
2. **Gate:** `validate_metadata_filter` must re-parse the filtered payload and compare top-level
   types against the on-disk file, with a negative control that proves it fires. The `shape_probe`
   case from «#324» is a ready-made control.

**How this surfaced.** «#324» was measuring whether 34 YAML shape changes break any consumer. They
do not. But running the real fetch script against the real tree — rather than reading it — showed
what the delivery path does to files that were never part of the shape question at all.

---


**GATE HALF RESOLVED 2026-09-11 (block I «#340»).** The structural complaint — *every gate reads the tree, the consumer reads the stream, nothing compares them* — is answered where it mattered: `validate_metadata_filter` now `yaml.safe_load`s the DELIVERED payload and fails on any key that collapsed to `None`, proven with an independently-built negative control (block H, `75911edb`).

**Delivery-strip numbers re-derived and recorded** in the change ledger (now `2026-09-11-yaml-release-change-ledger.md` §1.5 — see the note below) so they reach Stephen's visual read: `filter_metadata` strips five fields; `documentation_source` is **396 values across 395 files**, of which **363 (91%) are real provenance** and only 33 are bookkeeping tokens (`enhanced` 16, `original` 15, `code_analysis` 1, `redirect_stub` 1). So the set satisfies cite-or-omit ON DISK and is delivered NOT satisfying it, and nine tenths of what the filter removes is the provenance the project's own rule requires. Filing drift noted rather than smoothed: the entry said 397/396, today measures 396/395.

**REMAINS OPEN:** the 383-file rename is a scope call Stephen owns and was explicitly out of block I.

⚠ **Ledger correction 2026-09-11.** These numbers were first appended as §1.26 to `2026-08-27-yaml-release-change-ledger.md`. That ledger was **spent** — its declared range `v1.17.0..b0057ec1` shipped on 2026-09-10 as v1.18.0/v1.18.1 — so it could not gate an unshipped release. Stephen caught it. The append was reverted, that ledger archived byte-identical to its last committed revision, and the content re-derived against the correct `v1.18.1..HEAD` range in `2026-09-11-yaml-release-change-ledger.md`. **A release ledger expires the moment its range ships, and nothing in the process was checking that.**
## Our USB smart-pin entry states as fact a sentence the DOCX edition dropped, and it contradicts the general WRPIN rule (2026-08-26, «#320» citation re-anchor) — F-372

### F-372 — `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite — `CONFIRMED`

**How this surfaced.** F-365's re-anchoring reads each stale citation's old target and finds that
content in the new artifact. Twenty-two of twenty-three matched. **One did not exist in the new
artifact at all**, which looked like an extraction defect and is not one.

**What the two editions actually say.** Both are labelled *Propeller 2 Documentation v35 (Rev B/C)*.

| | |
|---|---|
| **PDF-derived capture** `p2-documentation.txt:8886` | *"…will disable output drive and effectively create a USB 'sniffer'. **A new WRPIN can be done to effect such a change without resetting the smart pin.** NOTE: In Propeller 2 emulation on an FPGA…"* |
| **DOCX capture** `silicon-doc-text.txt:4579` | *"…will disable the output drive and effectively create a USB 'sniffer'. NOTE: In Propeller 2 emulation on an FPGA…"* — **the sentence is absent** |

The DOCX paragraph is not merely shorter; it is **differently written**, and it *adds* material:
`%HHH_LLL` drive modes are overridden alongside OUT, and *"The lower pin in the pair is DM, while
the upper pin is DP, per USB naming convention"* — neither of which the PDF version carries. The
heading differs too (`%11011 = USB host/device` vs `%11011 = USB host or device, full-speed
(12Mbps) or low-speed (1.5Mbps)`). **These are two revisions of one document, both claiming v35.**

**Why it matters beyond bookkeeping.** The dropped sentence **contradicts the general rule** this
same document states at `silicon-doc-text.txt:3856` and that «#319» just applied to
`architecture/smart_pins.yaml` as F-369: a WRPIN issued while DIR is high remaps 126 bits of state
underneath a running mode, producing *"unpredictable and quite certainly useless behavior"*, which
is why modes are configured only while DIR is low.

Two readings, and **documents cannot separate them**:

1. **USB is a genuine exception** — the sniffer change is a drive-enable flip rather than a mode
   change, so the multiplexing hazard does not apply, and the DOCX simply lost the sentence.
2. **The sentence was removed because it was wrong**, and the general rule governs `%11011` like
   everything else.

**Reached our KB?** **Yes — as settled fact.**
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` `configuration.wrpin_data` ends with
the sentence verbatim, with no caveat, cited to the PDF-derived capture that is now superseded.

**Applied here:** the claim keeps its place — it may well be right, and deleting a plausible
documented behaviour is its own kind of damage — but it now carries the conflict, cites both
editions, and points at the gap. **Routed to `KNOWLEDGE-GAPS` as G-027: bench-testable and
jumper-only** — configure a USB pair, issue a new WRPIN with DIR high, and observe whether the pin
continues or breaks. That is the only thing that settles it.

## Two same-named Silicon Doc DOCX copies disagree, and the KB garbled a flag semantic from that passage (2026-08-26, «#314» pre-flight) — F-367 · F-368 · F-369

### F-367 — `external-inputs/p2/` and `sources/silicon-doc/` hold DIFFERENT documents under the same filename — `CONFIRMED`

**How this surfaced.** «#314» went looking for a PASM2 DOCX and found `external-inputs/p2/` holds
DOCX originals for several sources — **including a second copy of the Silicon Doc**, same filename,
different size (4,919,444 vs 4,814,991 bytes).

**Measured, not assumed.** Both carry 48 tables and 34 media, so a structural check calls them
identical. Extracting text from each and diffing says otherwise: **972 characters differ across 4
sites.**

| Site | `sources/` (the copy used for the 2026-08-26 re-extraction) | `external-inputs/` |
|---|---|---|
| GETBRK WZ | `Z = 1 if no … pattern queued (D = 0) or **0** if pattern queued (D <> 0)` | `… or **1** if pattern queued (D <> 0)` |
| smart-pin reset | **carries a full paragraph**: *"Once a smart pin is configured via WRPIN and then started by making its DIR bit high, it can be reset at any time by making its DIR bit low. It does not lose its configuration…"* | **paragraph absent** |
| PWM dither rationale | *"a maximum of only two adjacent 8-bit DAC levels are set for every 2…"* | *"a maximum of only two transitions occur for every 256 clocks"* |
| typo | `cog regis+ters:` | `cog registers:` |

**Which is right, and why it is decidable without a third source.** The `external-inputs/` GETBRK
line sets **Z = 1 in both branches**, which makes `WZ` useless and cannot be what the silicon does;
`sources/` gives `Z = 1 / Z = 0`, which is also the conventional Z semantic (`D = 0 → Z = 1`).
**The copy used for the re-extraction is the correct one**, and it additionally carries a paragraph
the other lacks. No prior work is invalidated.

**Why it still matters.** Two files with one name, differing on a flag semantic, is a silent
corruption waiting for whoever opens the wrong one. `external-inputs/p2/` is not a source folder and
carries no dashboard row, no audit and no trust tier — it is a staging area that has quietly become
a second, unlabelled copy of the corpus. **Disposition is Stephen's:** label `external-inputs/p2/`
as staging-only with a pointer to the canonical `sources/` copies, or reconcile the copies. Recorded
as **needs Stephen's accept-or-fix**.

**Also found there and NOT blocked as previously reported:** `Propeller 2 Questions & Answers.xlsx`
— the `p2-qa-spreadsheet` row sits at 80% and was listed in this sprint's plan as having *no primary
document staged*. It has one. That plan line is wrong and is corrected in «#318».

## The COG register map's PA/PB row lost the return-vs-parameter distinction, and its index dangles 13 of 16 pointers (2026-08-26, silicon-doc DOCX re-extraction) — F-363 · F-364

### F-364 — the same index advertises 16 register files; 13 of the pointers do not exist — `PARTIAL` (re-verified 2026-10-05 «#386»: pointers removed and shipped; the gate reading `yaml_file:` is not built)

**What was measured.** Every `yaml_file:` pointer in
`complete-system-registers-index.yaml`, resolved against its own directory:

| | |
|---|---|
| pointers declared | **16** |
| resolve | **3** |
| **dangle** | **13** (11 distinct filenames) |

Missing: `dual-ijmp3` · `dual-iret3` · `dual-ijmp2` · `dual-iret2` · `dual-ijmp1` ·
`dual-iret1` · `dual-pa` · `dual-pb` · `ptrb-register` · `outa-outb-registers` (×2) ·
`ina-inb-registers` (×2). The directory contains exactly three files:
`complete-system-registers-index.yaml`, `dira-dirb-registers.yaml`, `ptra-register.yaml`.

**Why no gate caught it.** `validate-crossref-keys.py` exits 0 on this tree and has throughout.
It validates `related:` keys; **`yaml_file:` is a different pointer field and nothing checks
it.** So an index can promise thirteen files that were never written and every instrument stays
green — the same shape as F-362 (a register gate reporting CLEAN on entries it never read) and
F-359 (headers citing sources that do not exist). An agent following `yaml_file: dual-pa-register.yaml`
to resolve F-363's own defect would find nothing there.

**Disposition owed — this is a scope call, not a mechanical fix.** Either the eleven files get
written (they are real registers and deserve entries), or the pointers are removed and the index
carries the content inline. **Removing a pointer is not automatically Sacred Rule #7's forbidden
delete** — that rule protects a `related:` link to a concept documented *elsewhere*, and here
there is no elsewhere. But which way to go is {{USER_NAME}}'s call and is recorded as
**needs Stephen's accept-or-fix**, not decided here.

🟢 **RESOLVED 2026-08-26 («#323») — the thirteen dangling pointers were removed; the content
stays inline.** Writing eleven thin files would have put one fact in two homes, which is the
defect class this project keeps finding. **The index already holds everything a per-register file
would need** — address, normal use, special function, description, access, category and key
features — for every register it lists; that is now stated in `metadata.per_register_files`, so
anyone who later wants per-register files can generate them from this file without new research.
The three pointers that resolve (`ptra-register.yaml`, `dira-dirb-registers.yaml` ×2) were left
untouched.

Measured after: `yaml_file:` pointers across all of `deliverables/ai/P2/` — **3 declared, 3
resolve, 0 dangle**. The resolver was shown to be live by pointing one of the three at a
non-existent file, which it reported as DANGLE before being restored.

**Instrument gap, still filed:** whatever the disposition, `yaml_file:` pointers should be
resolved by a gate. Today nothing in the shipped tool set reads them — the resolution above was
done by an ad-hoc walker, not by an armed check. With 3/3 resolving, arming it is cheap now.

Status: `PARTIAL` (2026-10-05: the `yaml_file:` gate is still owed) — 13 dangling pointers removed, content kept inline, 3/3 remaining pointers
resolve. The instrument gap (no gate reads `yaml_file:`) remains open.

## `pin-selection.yaml` printed the streamer's sub-pin table with the wrong bit weights, and shipped the EF-065 trap as its worked example (2026-08-26, found while composing the streamer pin-capture page) — F-361

- **F-361 — Two defects in `deliverables/ai/P2/architecture/streamer/pin-selection.yaml`: a
  `sub_pin_selection` table that contradicts both the Silicon Doc and the bench, and a
  `pin_base_encoding` example that is the EF-065 misalignment trap written out for a reader to
  copy.** — `PENDING-VALIDATION` (both fixed 2026-08-26; a direct bench check of the sub-pin
  weights is arm B of VO-J-005 and has not been run)

  **Defect 1 — the sub-pin table.** The block stated `field: "D[19:17] within mode config"` and then
  gave a **dense slot** mapping: for 2-pin modes `%001 = Pins 3..2`, `%010 = Pins 5..4` … `%111 =
  Pins 15..14`; for 4-pin modes `%001 = Pins 7..4` … `%111 = Pins 31..28`. Both columns are wrong,
  and wrong in a way that matters: they imply a 4-pin capture can be based anywhere in a 32-pin
  window, which is exactly the belief that produces a misaligned base.

  **What the sources say.** Propeller 2 Documentation v35: *"In every mode, the three %ppp bits in
  D[22:20] select the pin group, in 8-pin increments"*
  (`engineering/ingestion/sources/silicon-doc/p2-documentation.txt:3606`) and *"For modes which
  involve less than 8 pins, lower-order %p bit(s) in D[19:19..17] are used to further resolve the
  pin number(s)"* (`:3653`). So the pin number is ONE six-bit field at D[22:17] — `pin << 17` —
  and D[19:17] is `pin & 7`, not a slot index. The Spin2 v55 streamer symbol table states the same
  thing per mode, as the bit templates themselves:
  `X_1P_1DAC1_WFBYTE %1100_DDDD_WPPP_PPPA`, `X_2P_2DAC1_WFBYTE %1101_DDDD_WPPP_PP0A`,
  `X_4P_4DAC1_WFBYTE %1110_DDDD_WPPP_P00A`, `X_8P_4DAC2_WFBYTE %1110_DDDD_WPPP_0110`
  (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1608-1613`). The fixed zeros at
  D[17] and D[18:17] ARE the alignment rule, stated by encoding.

  **The bench already agreed with the sources, in two mode families.** EF-064: a 1-pin mode with
  `20<<17` drove **P20 exactly**. EF-065: an 8-pin mode with `+ 20<<17` drove **P24..P31** — the
  carry model, not the slot model. Under the table's dense reading neither result follows.

  **Defect 2 — the worked example.** `pin_base_encoding.example` read
  `mode := X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + count`: an **8-pin** mode at a base that is not
  a multiple of 8, composed with `+`. That is EF-065 verbatim, in a third mode family, printed as
  the line a reader copies. Assembled with `pnut-ts` v1.55.3 to check rather than assert:

  ```
  X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + $FFFF   ->  $A0B6_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (16<<17) | $FFFF ->  $A0AE_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (20<<17) | $FFFF ->  $A0AE_FFFF
  ```

  `$A0B6_FFFF` is D[19:16] = `%0110` (**X_RFBYTE_8P_4DAC2**, a different mode) at D[22:20] = `%011`
  (**P24..P31**, a different group). And the third line is the other half of EF-065: with `|` the
  misaligned base is **byte-identical** to base 16 — it does not carry, it silently vanishes. Both
  compile clean.

  **Applied 2026-08-26.** `sub_pin_selection` rewritten to state the rule and the per-width free
  bits by encoding, with a worked mapping only for the 1-pin case (the one width where all three
  bits are free and no mode caveat applies), plus a `what_a_misaligned_base_does` pointer.
  `pin_base_encoding` now carries the alignment rule, the composition rule, an **aligned** example,
  and both failure modes with their assembled words. `common_configs` re-composed with `|` and each
  base annotated with the rule it satisfies. The file also gained a `source:` (it had none) and the
  capture-path facts this sprint's Section B added.

  **What is still owed.** A bench confirmation of the 2-pin/4-pin sub-field weights specifically.
  EF-064/EF-065 cover the 1-pin and 8-pin families; the 4-pin family is **arm B of VO-J-005**
  (`engineering/ingestion/external-sources/hardware-verification/VERIFICATION-OPPORTUNITIES.md`),
  which captures at base 12 against two distinct static pin patterns and names the reversing
  outcome: if the buffer returns the P8..P11 pattern rather than the P12..P15 pattern, this finding
  is backwards and must be reverted before anything built on it ships.

## The bulk-generation commit wrote FABRICATED PROVENANCE HEADERS, and those headers are what make seven `architecture/` files look cited (2026-08-25, Stephen's question at the release review) — F-359

- **F-359 — Seven `architecture/` files carry a provenance header citing source files that have
  never existed and datasheet pages beyond the end of the datasheet; the header itself satisfies
  the citation regex, so six of the seven still pass the gate today.** — `PARTIAL` (re-verified 2026-10-05 «#386»: six files re-derived and shipped; 5 of the 8 non-derivable claims are still in the tree and their delete-or-keep call is undecided)

  **How it surfaced.** Stephen asked whether `io_pin_timing.yaml`'s content might have come from
  our own I/O & Smart Pins manual rather than a Parallax source — i.e. whether the provenance was
  circular. **The answer is no, and the truth is worse.**

  **The timeline rules the manual out.** `io_pin_timing.yaml` was created **2025-11-29** in
  `e271cab0`; the IOSP manual's first commit is **2026-01-25**, nearly two months later. Causality
  therefore runs **KB → manual**, not manual → KB. Where that manual repeats the drive-strength
  mislabel (F-356), it most likely **inherited it from this file**, which inverts the assumption
  behind the post-release manual review.

  **Nor did it come from what it cites. Every citation in the header is false:**

  | Header line | Reality |
  |---|---|
  | `Silicon Doc Reference: part3-pins.txt` | **no such file has ever existed** (nor `part1-cog.txt`, nor `part3-smartpins.txt`, nor `part2-cog.txt`) |
  | `Datasheet Reference: pages 42-45` | those pages are the **PASM2 instruction listing** |
  | `Datasheet Reference: … 76-78` | **the datasheet is 50 pages** |
  | `Layer 1: Direct extraction from Silicon Doc v35 and P2 Datasheet` | the values (`2.5/3.5/5.0 ns`, the mA ladder, "slew") appear **zero times** in any ingested source |

  **It is a class of seven, and we purged one.** All seven were written in the same commit —
  `e271cab0`, 2025-11-29, *"Implement DOD v3.0"*, which touched **1,323 files and 973 YAMLs in a
  single commit**. Each carries the same header shape, each names a non-existent silicon-doc file,
  and **each cites a second datasheet range beyond page 50**:

  | File | Cites | Impossible page range | Quantities today |
  |---|---|---|---|
  | `architecture/io_pin_timing.yaml` | `part3-pins.txt` | 76-78 | purged this sprint |
  | `architecture/cog_attention.yaml` | `part1-cog.txt` | 73 | 0 |
  | `architecture/debug_interrupt.yaml` | `part1-cog.txt` | — | 0 |
  | `architecture/event_system.yaml` | `part1-cog.txt` | 74-75 | **6** |
  | `architecture/interrupts.yaml` | `part1-cog.txt` | 71-72 | **2** |
  | `architecture/locks.yaml` | `part1-cog.txt` | 82 | 0 |
  | `architecture/lookup_ram.yaml` | `part1-cog.txt` | 67-68 | **1** |

  🔴 **THE MECHANISM — the fabricated header IS the citation that silences the gate.** Measured
  against `audit-yaml-claim-sourcing.py`'s own regex: all three header forms return
  `INLINE_CITE = True`, because the matcher fires on the tokens *"Silicon Doc"* and *"Datasheet"*
  wherever they appear. **A header that invents its sources reads to the instrument exactly like a
  header that names real ones.** This is F-335's pattern — the citation side matching on the
  presence of a token rather than on whether the sentence attributes the block to a document —
  applied to the KB's original sin rather than to a later edit.

  **Consequence for the release, stated plainly:** at least **9 quantities** across three of these
  files stand under a header citing a file that does not exist, and the current `0 Tier 1` does not
  contradict that — the gate is satisfied by the fabrication. `io_pin_timing.yaml` was caught only
  because it *also* had blocks with no header coverage at all.

  **The "lack" this traces to.** Nothing checked generated content against a source at creation
  time, and **the citation header was generated along with the content it claims to source**. A
  fabricated citation is not an error in sourcing; it is the signature of never having sourced.
  973 YAMLs in one commit is the scale at which that becomes invisible.

  **NOT FIXED — this is a scope decision Stephen owns**, raised at the release review he called
  for. Purging six more files is a widening at the gate, and the release is his call. Options are
  his: purge the class now, ship and schedule it, or re-derive those six from the real sources.
  What must NOT happen is shipping while believing the `0 Tier 1` covers them.

  🟢 **RESOLVED 2026-08-26 («#323») — the third option was taken: all six re-derived from the
  real sources.** The silicon doc is now fully extracted, which is what made this tractable;
  every claim below was read off `sources/silicon-doc/silicon-doc-text.txt` or
  `sources/p2-datasheet/p2-datasheet-text.txt` live, and every citation written into the six
  files was then re-read at the line it names.

  **What the re-derivation actually found is worse than the header.** The fabricated citation was
  the signature, not the extent. Across the six files:

  | | Before | After |
  |---|---|---|
  | `- instruction:` entries carrying an `encoding:` | 47 | 45 |
  | encoding **verbatim-identical** to the silicon doc's PASM2 encoding table | **2** (`RDLUT`, `SETSE1`) | **45** |
  | encoding **wrong** | **41** | **0** |
  | mnemonic **not in the encoding table at all** | **4** | **0** |

  The four absent mnemonics are `RDCOGID`, `RDLUTS`, `NIXINT0` and `TRGINT0`. Each was checked
  three ways: absent from `silicon-doc-text.txt`, absent from every other file under
  `deliverables/ai/P2/`, and not accepted as an instruction by pnut-ts v1.55.3 (`nixint0` and
  `trgint0` assemble to a zero-byte binary because the compiler reads them as labels; `rdcogid`
  and `rdluts` are hard errors). The four RETIx encodings come from this knowledge base's own
  `language/pasm2/reti0..3.yaml`, since RETIx are CALLD aliases and appear in the silicon doc as
  alias definitions (`:5483-5486`) rather than as encoding-table rows.

  Plus these semantic inversions, each of which a code-generating agent would have acted on:
  * `interrupts.yaml` had the **IJMPx/IRETx address map inverted** — it called `$1F0` IJMP1 where
    three authorities (silicon-doc `:2296-2301`, datasheet `:558-563`, and the RETIx alias
    definitions at silicon-doc `:5483-5485`) all say `$1F0` is IJMP3.
  * `interrupts.yaml` claimed **per-level shadow registers** for PA/PB/PTRA/PTRB/Q. There are
    none; the CALLD dispatch saves the return address and C/Z into IRETx and nothing else
    (silicon-doc `:2294`, `:2359`).
  * `lookup_ram.yaml` had **LUT sharing backwards** — it described reading the neighbour's LUT.
    Sharing is a WRITE path into the paired cog's LUT (silicon-doc `:491-500`). It also had
    **WRLUT's operands reversed** (D is the data, S is the address).
  * `locks.yaml` carried a `LOCKTRY (WC mode)` entry meaning "check the owner without acquiring".
    LOCKTRY always attempts to take, and C=1 means *taken* (silicon-doc `:3688`); the query form
    is LOCKREL with WC and a register D (`:3700`).
  * `cog_attention.yaml` had **ATN as event 15**; it is event 14 (`:2053`, `:2290`), and both
    SETINTx examples used the wrong number. Its `setup_for_event` configured SETSE1 for
    attention, which SETSEn cannot select at all (`:2246-2260`).
  * `debug_interrupt.yaml` invented three **"configuration registers"** (BRK as a register with a
    `[31:20]` flags field, plus SKIP and SKIPF as debug registers). BRK is an instruction whose D
    operand is `%aaaaaaaaaaaaaaaaeeee_LKJIHGFEDCBA` (`:2498-2517`), and GETBRK reads cog status
    in three forms rather than reading back a break configuration (`:2527-2593`).
  * `event_system.yaml` carried an invented event taxonomy ("Edge-detect", "IN-rise",
    "CORDIC-done") in place of the sixteen the source enumerates (`:2037-2054`), and its
    pattern-match example selected **mismatch** mode while its comment said match — SETPAT reads
    C and Z as inputs, and takes no WC/WZ effect (confirmed against pnut-ts).

  **The header was replaced in both places it lived** — the leading comment block AND
  `extraction_metadata.source_documents`, which carried the same `part1-cog.txt` and the same
  impossible page ranges. Each file now names the real document, the real section, and a live
  line range, and carries a `re_derivation_note` stating what was corrected.

  ⚠️ **THE GATE IS STILL NOT THE EVIDENCE.** `audit-yaml-claim-sourcing.py` read `0 Tier 1`
  before this work and reads `0 Tier 1` after it, because none of the six carries a
  unit-bearing quantity block. That green says nothing about whether these files are cited; the
  evidence is that every `<file>:<line>` written into them was re-read at the line it names. The
  instrument was separately shown to be live on these files: a planted two-quantity block in
  `locks.yaml` produced `TIER 1 ... 1 violation` and exit 1, and removing it returned exit 0.

  **Eight claims could NOT be re-derived and were NOT deleted — deletion is Stephen's.** Each was
  searched for in the silicon doc, the datasheet and this KB's own per-instruction YAMLs before
  being listed:
  1. `locks.yaml` `architecture.state_bits: 4` with the comment "3 bits COG ID + 1 bit owned
     flag". No source gives a lock any internal bit-width; both authorities say only "16
     semaphore bits" (silicon-doc `:3674`, datasheet `:878`).
  2. `lookup_ram.yaml` `performance_characteristics.power_consumption` (active "similar to COG
     RAM access", idle "static power only"). Zero hits for LUT power in either document.
  3. `lookup_ram.yaml` `bandwidth.streaming: "32 bits per clock (via streamer)"`. That figure is
     the **hub RAM** rate (silicon-doc `:2999`, `:3003`); nothing states it for a LUT-sourced
     streamer.
  4. `lookup_ram.yaml` `bandwidth.internal: "32 bits per 2-3 clocks"` — a restatement of the
     RDLUT/WRLUT timings as a bandwidth, which no source makes.
  5. `debug_interrupt.yaml` `memory_usage.trace_buffer: "Typically 4KB-16KB in hub"`.
  6. `debug_interrupt.yaml` `memory_usage.debug_state: "~100 longs for full state capture"` —
     the source describes 16 longs saved by the ROM routine and 64 bytes per cog per area.
  7. `debug_interrupt.yaml` `limitations.streamer_interaction: "Debug can disrupt streamer
     operations"`. The source makes the opposite kind of claim about the hub FIFO — the scheme
     runs in cog register space precisely so it does *not* disturb it (`:2484`) — and says
     nothing about the streamer.
  8. `cog_attention.yaml` `performance_characteristics.response_latency.waiting: "0 clocks after
     signal arrives"`. The datasheet gives WAITATN as `2+` (`:1914`).

  Not listed above, and deliberately: the `programming_patterns`, `common_applications`,
  `best_practices` and `debugging_tips` sections of all six files are authored guidance rather
  than source claims. They were corrected wherever they encoded one of the defects above (wrong
  event number, fabricated mnemonic, inverted sharing direction, mismatch-mode SETPAT), and
  otherwise left alone.

  **Fabricated NAMES were deleted rather than escalated**, under Stephen's standing rule *"no
  fabricated names in the KB tree -- delete invalid names outright"* — the same rule this
  sprint's C3 applies to the invented part numbers. The four mnemonics were checked three ways
  first: absent from the silicon doc, absent from every other file in `deliverables/ai/P2/`, and
  not accepted as instructions by pnut-ts v1.55.3.

  Status: `PARTIAL` (2026-10-05: 5 of the 8 non-derivable claims still stand, call undecided) — all six re-derived and cited against live sources; eight non-derivable
  claims listed above are left in place for Stephen's delete-or-keep call.

---
## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## The "masters are clean of the drive-strength mislabel" measurement is wrong (2026-08-25, «#301») — F-356

### F-356 — the drive-strength mislabel is alive in the IOSP master at 23 sites, including the one composition this sprint forbids by name — `PARTIAL`

**How this surfaced.** «#301» was told, as a *measured result and not an assumption*, that a
class-wide sweep on 2026-08-24 found the manual and app-note masters **clean** of this sprint's
defect class (the drive-strength mislabel, the fabricated ladder, pin slew-rate claims) — which is
why Plan §3 excludes manual prose from that class. Working F-251 required reading the deSilva Ch.1
LED aside, whose closing sentence turned out to state the mislabel outright. One site is an
anomaly; the sweep it implied is what produced this finding.

**What was measured.** A sweep of every `opus-master/` body and CHANGELOG across all manuals and all
seven app notes (excluding `archived-2025/` scaffolding and the non-P2 `Donna-Manuscript`) for
pull-up / pull-down language, then each hit graded by hand as *external component* (correct) or
*`P_HIGH_*`/`P_LOW_*` glossed as a bias resistor* (wrong):

| Site class | Count | Where |
|---|---|---|
| A `P_HIGH_*`/`P_LOW_*` constant glossed as a **pull-up/pull-down resistor** | **23 lines** | IOSP `appendix-b-p-constants.md` ×7 · `chapter-12-digital-input.md` ×5 · `chapter-02-enhanced-direct-io.md` ×7 · `chapter-06-digital-output.md` ×2 · `appendix-a-intent-index.md:56` · `part-5-appendices/index.md:221` |
| **"internal pull-up/pull-down"** asserted as a P2 feature | **5 lines** | `chapter-06-digital-output.md:137`, `:144`, `:441` · `chapter-02-enhanced-direct-io.md:431`, `:479` |
| The composition this sprint says to **never** write | **4 sites** | `chapter-02-enhanced-direct-io.md:94`, `:399`, `:439`, `:480` — `P_HIGH_15K \| P_LOW_FLOAT` |

**Why each class is wrong.** A pull-up is active whenever the pin is *not* driven; a drive-strength
selector applies **only while the pin drives that direction** — DIR high, per the Pin Mode Legend
(`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:41-43`, `:166-171`; P2 Datasheet
2022/11/01 p.24). This is F-321's reasoning exactly, and F-321 was applied to
`deliverables/ai/P2/` and **only** there. `chapter-02-enhanced-direct-io.md:53` is the cleanest
example: it prints `| P_HIGH_15K | %010 | Resistive | ~200µA / 15kΩ | **Pull-up resistor** |` — a
component the chip does not have, in a table of things it does. `:441`'s
*"Open-drain + internal pull-up"* is the F-322 inversion in a summary row. And
`P_HIGH_15K | P_LOW_FLOAT` is the composition whose "high side weak, low side floated" variant
`pin-drive-configuration.yaml:250-252` records as having **no Parallax documentary statement and no
empirical record** — the manual teaches it four times, once as a recipe headed **"Pull-Up
Resistor:"**.

**Scope note — this is filed, NOT fixed, and the distinction is deliberate.** Plan §3 puts this
defect class out of scope for manual prose in this sprint, and «#301» was told scope is Stephen's.
So the correct act is to **falsify the measurement the exclusion rests on** and hand it over, not to
widen a roster. The two sites «#301» *did* fix are the ones inside its own roster's findings:
deSilva `COMPLETE-OPUS-MASTER.md:294` (inside F-251's aside), and `:2881` was checked and left
because it is already **correct** (*"No pullup/pulldown by default — Use external resistors or
configure smart pin modes"*).

**PARTIAL 2026-09-10 — the MECHANISM half is applied across IOSP and deSilva; the SOURCING half is
not, and it is tracked by F-336.** Worked as part of the v1.18.0 sweep, under §1.24's reframing.

⚠️ **§1.24 changed what the repair is, and this entry's own site counts must be read through it.**
Calling `P_HIGH_15K` a "15 kΩ pull-up" is now *acceptable vocabulary* — the Silicon Doc uses it for
these same rungs, and the KB deliberately carries `pull-up`/`pull-down` **aliases** so a coder
asking the real question lands on the real answer. So the "23 mislabel sites" are no longer 23
defects. **What was owed, and is now delivered, is the DIR caveat and the mechanism at every place
the constants are presented:**
- `chapter-02` — a passage before the drive tables stating the P2 has no separate pull resistors,
  that these are drive strengths, and that every rung needs `DIR = 1`; a second note governing the
  *Common Drive Configurations* block (those lines are mode words only); and `PINHIGH` added to the
  two bare-`WRPIN` pull-up recipes at `:94` and `:399`.
- `chapter-06` — `:144` now says this is an open-drain *substitute* whose high side drives rather
  than floats, and sends a genuine multi-master bus to `P_HIGH_FLOAT` + an external pull-up; `:441`'s
  summary row is retitled *"Weak-high / strong-low (open-drain substitute)"* (that row is **F-417(b)**).
- `appendix-b` — the *Drive Strength - High* table now opens with the DIR/OUT rule, and the button
  recipe carries its `PINHIGH` step.
- `deSilva :2881` — **re-adjudicated and rewritten.** This entry records it as "already correct",
  and against the framing of 2026-08-25 it was; under §1.24 *"no pullup/pulldown **by default**"*
  implies a non-default internal pull, and it sent the reader to smart-pin modes when the mechanism
  is drive strength. It now gives the answer first.
- `part-5-appendices/index.md:221` — the index sent a reader looking up "Pull-up" to Ch. 6, when the
  mechanism and the constant tables are in Ch. 2. Now "Ch. 2, 6", and it names them as drive-strength
  rungs. `appendix-a-intent-index.md:56` was read and **left**: an intent-index row using the
  vocabulary a reader actually types is the findability behaviour the KB's own aliases exist for.

**STILL OPEN — the sourcing half.** `P_HIGH_15K | P_LOW_FLOAT` still has no Parallax documentary
statement and no bench result; the manual now explains the mechanism correctly but cannot *cite* the
composition. That is **F-336**, which owns it, and it closes with a source or a silicon run — not
with prose. This entry stays `PARTIAL` until F-336 resolves.

**What would settle it.** Nothing further to establish — the mechanism is closed (F-321 applied, the
Pin Mode Legend cited, the idioms hardware-verified in
`pin-drive-configuration.yaml:203-239`). What is needed is a decision on **when** the IOSP master
takes the correction, because it is not a token substitution: two constant tables, a chapter section
heading (*"### Button Input with Internal Pull-Up"*), four worked recipes and an intent-index row all
have to be restated in drive-strength terms, and the four `P_LOW_FLOAT` recipes need a form that has
a source behind it. That is a chapter-scale pass on Chapters 2, 6 and 12 plus two appendices, not a
sweep.

**Related:** F-321 (same mislabel, KB side, applied) · F-322 (the disable-the-drive inversion) ·
F-325 (the ladder absent from the shipped KB) · F-336 (`P_HIGH_15K | P_LOW_FLOAT` has neither a
Parallax statement nor a bench result) · F-341 (the same mislabel in our own derived analysis docs) ·
`SOURCE-ERRATA.md` E-004 and **E-010** (Parallax's own guides state it).

> 🔴 **F-341 IS SHARPER THAN "LATENT" — THOSE FILES INVENT PARALLAX PART NUMBERS. Confirmed by
> Stephen 2026-08-26.**
>
> Asked whether our board coverage was complete, the inventory turned up three part numbers with
> **zero occurrences in any ingested source directory** — i.e. in any actual captured Parallax
> document. They exist only in the loose analysis files at `engineering/ingestion/sources/`:
>
> | Invented | Where it appears | What it actually is |
> |---|---|---|
> | **#64025 "LED Board"** | `p2-hardware-validation-checklist.md:102`, `p2-board-power-analysis-matrix.md` | **does not exist** — the real board is **#64006C LED Matrix** |
> | **#64026 "7-Segment Display"** | `p2-hardware-validation-checklist.md:150` | **does not exist** |
> | **#64027 "Switches Board"** | `p2-hardware-validation-checklist.md:191` | **does not exist** — switches are on the **#64006A Control** add-on |
>
> **Stephen, asked directly: "LED board, no. 7-segment, no. Switches, no."**
>
> **Why this is worse than a wrong name.** The inventions are *plausible* — they describe real
> capabilities (LEDs, a display, switches) that map onto real boards, at part numbers adjacent to
> the real #64019/#64020/#64029 range. And `#64027`'s validation section is headed **"Test 1:
> Pull-up Test"**, so the fabricated board carries the fabricated mechanism. A reader has nothing to
> catch it with.
>
> **None of the four files names a Parallax document anywhere.** Their headers are
> *"Comprehensive testing procedures…"*, *"Complete power budget calculations…"*, *"Complete
> cross-reference for automatic code generation"* — authored analysis, with no provenance, sitting
> in the directory reserved for captured sources. **Location is doing the work of attribution.**
>
> 🟢 **CONTAINMENT VERIFIED: zero leakage.** `grep -rl` for all three across `deliverables/ai/P2/`
> returns **0 files**. The shipped KB never carried them, and «#305» had already excluded loose
> root files from the fidelity tool's truth side. The damage is confined to the ingestion tree.
>
> **Still open, and it is a scope call:** the four files remain where sources live, they still assert
> the pull-up mislabel, and the compatibility/power matrices cross-reference boards that do not
> exist — so anything derived from them is derived from fiction. Options: correct them in place and
> relabel as analysis, relocate them out of `sources/`, or retire them. **Not actioned pending
> Stephen's decision.**
>
> 🟢 **THE INVENTED-PART-NUMBER HALF IS CLOSED 2026-08-26 («#323»).** Stephen's standing rule —
> *"no fabricated names in the KB tree, delete invalid names outright"* — settled the disposition
> without needing a further decision, so it was executed. **Every `#64025` / `#64026` / `#64027`
> site in the repository was worked**, which was more than the three the finding names:
>
> | File | What was there | What was done |
> |---|---|---|
> | `sources/p2-hardware-validation-checklist.md` | three validation sections (`:102`, `:150`, `:191`), incl. the `#64027` "Pull-up Test" that carries the F-321 mislabel | sections deleted, dated removal note left in place |
> | `sources/p2-board-power-analysis-matrix.md` | three power-analysis sections, two `case` arms in worked code, five Quick-Reference rows | all deleted, removal note left |
> | `sources/p2-complete-signal-flow-matrix.md` | three signal-path sections, a VIO-load `case`, three `ADDON_*` constants, an impedance-detect routine returning two of the invented boards | all deleted, removal note left |
> | `sources/p2-board-addon-compatibility-matrix.md` | three grid rows, five detailed configurations across two boards, three power rows, three `case` arms | all deleted, removal notes left |
> | `plans/quick-bytes-ingestion-plan.md` | `parallax_id: "64025"` against **"P2 RTC Add-on Board"** | **corrected to `64013`** — the real part number, from `sources/edge-breakout-board/edge-breakout-board-narrative.txt:137` |
> | `knowledge-base/P2-support/extractors/hardware-specs-extractor.py` | a YAML **generator** with all three baked in, emitting them under `source: P2 Documentation Collection` | the three entries deleted, note left |
>
> **Deleted rather than relabelled, deliberately.** The nearest real boards are the **#64006C LED
> Matrix** (an 8×7 Charlieplexed grid driven on 8 pins) and the **#64006A Control** add-on (four
> buttons and four LEDs); there is no 7-segment board in the #64006 series at all. The removed pin
> maps, currents and test procedures described none of those, so relabelling would have attached
> fabricated numbers to real boards — a worse defect than the one being fixed.
>
> After: `grep -rn '64025\|64026\|64027'` across the repository returns **no hit that presents a
> board**. Every surviving occurrence is one of four kinds: a dated removal note at the site the
> content was cut from, the `#64013` correction comment, the sprint plan's task row, or this
> register's own documentation above. Deliberately stated as classes rather than a count — the
> count changes every time this register is edited, and a self-referential tally is stale the
> moment it is written. (Arbiter check, «#323»: the figure first written here was 11; the live
> number was already 15, because writing the table above added hits to the thing being counted.)
>
> **Two halves remain open**, both unchanged by this pass: the four files still sit at
> `sources/` top level asserting the pull-up mislabel (the relocate-or-repair-or-retire call), and
> the *same class* of unverified part numbers survives in them — `#64028` "Buttons Board",
> `#64029` relabelled "Switches and LEDs Combo", `#40003` "Protoboard", `#40007` "Digital I/O
> Board". Those four were left strictly alone because Stephen confirmed three numbers, not seven,
> and «#323» would have been widening its own scope to act on them.

Status: `PARTIAL` — the mechanism/DIR-caveat half is applied across IOSP and deSilva (2026-09-10, in the v1.18.0 sweep, shipping in IOSP v1.0.10); the sourcing half for `P_HIGH_15K | P_LOW_FLOAT` is still owed and is tracked by F-336.

---

## Five defects surfaced while ending the drive-strength mislabel class (2026-08-25, «#296» §5) — F-342…F-346

> **Origin.** All five were found while correcting F-321…F-324 — three of them only because
> R8 forces a **semantic read** of every example after it compiles. Three are fixed in that same
> pass and marked so; two are not this task's repair and are filed for the head that owns them.
> Every line number below was read off disk on 2026-08-25.

### F-344 — the derived board extract contradicts itself in one sentence about switch polarity — `CONFIRMED`

> **Where:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:9-11`
> — *"each **active-high** push-button has a **470 Ω series resistor** so the I/O pin is **driven
> low** while the button is asserted."*
>
> **Active-high and driven-low-when-asserted cannot both be true of the same switch.** The rest of
> that same file says active high in the pin map (`:20-23`), and the shipped
> `hardware/addon-control-board.yaml:16-20` says *"the I/O pin reads high while the button is
> pressed"* — so the KB already resolved it the other way. The extract's own summary sentence is
> the outlier.
>
> **Ingestion-tree defect, not a YAML edit** — this file is derived source-research and is frozen
> to KB maintenance. Same class as **F-341** (our own derived documents inside the truth root).
> **What is owed:** re-read the #64006A Product Guide v2.0 page and correct the extract's summary
> sentence, or record why the guide itself says both.

## Provenance holes the repopulation could not fill (2026-08-25, «#299» Plan §8 part 2) — F-352

> **Origin.** «#299» rebuilt `architecture/`, `language/`, `guides/` and `application-notes/` from
> the repaired sources, source-first. Forty-five of F-347's sixty blocks came back cited. Two did
> not, for the same reason — the KB was their only home — and the rule set had no branch for that
> once the purge had already removed them. Line numbers below were read off disk 2026-08-25.

### F-352 — two shipped KB areas are authored-here content with NO upstream anywhere in the ingestion tree, and once their blocks were purged the promotion filter's sub-rule P had no branch left for them — `CONFIRMED`

> **Found:** 2026-08-25 by «#299», working the sources tree-by-tree rather than the removal list.
> Two of F-347's 60 rows could not be returned source-first, for the same underlying reason, and
> «#298»'s sub-rule P (*presence before removal*) does not cover the case because the removal has
> **already happened**.
>
> | Where | «#298» disposition | What «#299» found |
> |---|---|---|
> | `architecture/click_module_integration.yaml` `best_practices` | **ACTIONABLE** | **No ingested source states any of it.** The file's own `documentation_source: code_analysis` points at `engineering/ingestion/sources/code-analysis/`, which holds exactly three files — `bldc-motor-control-analysis.md`, `debugger-analysis.md`, `flash-loader-analysis.md` — and `grep -rln -i "click\|mikrobus"` over that directory returns **nothing**. The MikroBUS pinout, the P2 Eval Click Adapter offsets and the "three adapter positions" claim the block depends on have no upstream at all. **Recorded as a GAP, not restored.** |
> | `architecture/io_pin_timing.yaml` `best_practices` | **CORRECT BUT NOT ACTIONABLE** | Generic PCB-layout lore — match trace lengths, 22-33 Ω source termination, ~1 ns rise per 10 pF. `grep -rn "22-33\|150 ps\|150ps\|source termination\|match_trace"` over `engineering/ingestion/sources/` returns **zero**. **Held out, and deliberately NOT written to the ingestion tree.** |
>
> 🔴 **Why the io_pin_timing block was not "written to the ingestion tree first".** The C6 instruction
> offers that as the fix for a not-actionable block with no ingestion home. It is the wrong move here,
> and the reason generalises: **`engineering/ingestion/sources/` mirrors INGESTED SOURCE DOCUMENTS.**
> Writing authored-here electronics lore into it would manufacture a Parallax-tier authority out of
> nothing — and that tree is inside `audit-constant-fidelity.py`'s declared *Parallax documentary*
> truth root, which is precisely the defect F-341 already files against six of our own derived
> analysis documents sitting at that tree's root. Curing a provenance hole by inventing provenance is
> worse than the hole. The block stays out; git holds it at `15c84de5^` for anyone who wants it.
>
> **The generalizable half — sub-rule P needs a fourth branch, not a third.** «#298»'s *Sharpening*
> §3 already added *"authored-here content with no upstream at all — stays, and say why"*. That
> branch assumes the block is still **in** the KB, where "stays" is an available answer. Once a purge
> has removed it, "stays" is gone and the only choices are *invent an upstream* or *record the
> absence*. The rule wants: **authored-here, no upstream, ALREADY REMOVED → record it as a gap with
> the acquisition that would close it; never manufacture the source.**
>
> **What would settle each:**
> - *Click*: ingest the Parallax **P2 Eval Click Adapter** product documentation (the MikroBUS
>   offset map and the adapter's base-pin positions). That single ingestion would ground both this
>   block and the `p2_adapter_mapping` offsets the file already ships uncited.
> - *io_pin_timing*: nothing Parallax can settle — it is not a P2 fact. It closes by staying closed.
>
> ⚠️ **Also found while filing:** this register's header reads **`Next gap ID: G-007`**, but
> `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates **G-007** (Smart Pins / ADC, ANSWERED
> 2026-08-24). The counter is stale by one and the next free gap ID is **G-008**. «#299» allocated no
> G-number rather than collide; the header is left for whoever owns that ledger to correct
> deliberately.

---

## `hardware/` repopulated from the board guides — the return record, and the wrong scalars the source-first read exposed (2026-08-25, «#307» Plan §8 part 2) — F-353 · F-354

> **Origin.** «#294» removed 59 quantitative blocks from `deliverables/ai/P2/hardware/` (F-334, two
> records: 48/16 files and 11/6 files). «#298» dispositioned every one. «#307» worked the **board
> guides**, not the removal list, and wrote back what each guide states. One of the 11 —
> `language/spin2/methods/getct.yaml description` — is outside this tree and belongs to «#299», so
> **58** were in scope here. Every line number below was read off disk 2026-08-25.

### F-354 — seven content-level holes inside blocks that DID come back, and one held block whose content is only three-quarters in the ingestion tree — `CONFIRMED`

> **Why these are not "gaps" in the three-number sense.** Every ACTIONABLE block returned. What did
> not return is *material inside* those blocks — figures the KB shipped that no ingested source
> states. Each is recorded in the YAML itself, at the point of use, with what would settle it, so a
> reader meets the hole where the fact would have been rather than in a register they may not open.
>
> | Hole | Where it is recorded | What would settle it |
> |---|---|---|
> | HUB75 max clock **40 MHz (35 MHz reliable)** and **13 ns propagation delay** | `hub75_adapter.yaml` `specifications.gap_max_clock` | A level-shifter datasheet, or a measured result in `P2-EMPIRICAL-FINDINGS.md`. ⚠️ The manufacturer's own capture says **70 MHz** (`p2-hub75-adapter-official-specs.md:22`) — the two differ by ~2x and the KB now carries only the sourced figure. |
> | HUB75 **clock/latch/OE pulse-width minimums** (15 ns / 200 ns / 100 ns) and the 3-bit/8-bit refresh table | `hub75_adapter.yaml` `software_features.gap_pulse_widths` | Ingesting the ISP HUB75 driver's own documentation into `engineering/ingestion/sources/`. |
> | HUB75 **"maximum 3 chains"** and **"driver does not use the P2 streamer"** | `hub75_adapter.yaml` `notes.gap_chain_limit` | Same ingestion. The pinout capture argues the opposite for the second (`p2-hub75-adapter-complete-pinout.md:90`, "6-bit parallel data perfect for P2 streamer"). |
> | HUB75 **board current 35 mA @ 35 MHz** and the per-panel typical currents | `hub75_adapter.yaml` `power_requirements` is HELD, but its ingestion home states **under 50 mA** and **1-2 A** where the KB said 35 mA and 1.5 A (`p2-hub75-adapter-official-specs.md:126`, `:131-136`) | Same ingestion. The held block's numbers are NOT the ingestion tree's numbers — a re-check before anyone quotes the removed values from git. |
> | **"One cog consumed by the PSRAM driver"** on the 32 MB module | `edge-32mb-module.yaml` `development_workflow.psram_driver_note` | The #P2-EC32MB guide neither ships nor describes a PSRAM driver. Ingesting the OBEX `psram.spin2` driver documentation would ground it (and the API already sitting in that file's `code_patterns`). |
> | Whether the **#64013 RTC board carries its own SDA/SCL pull-ups** | `addon-rtc.yaml` `pin_mode_tip.scl_pull_up_caveat` | The #64013 board schematic (referenced by the guide, not ingested). |
> | Numeric **PCB dimensions for the #64006 add-on boards** | `addon-goertzel-touch.yaml` `specifications.pcb_size_class` | The guide gives only a drawing and a three-size classification (`p2-eval-add-on-boards-text.txt:45-46`, `:381-396`); the drawing was never resolved to numbers. Re-cutting that page, or the board schematics. |
> | `addon-serial-device.yaml` `specifications` — **the "3.3 V supply" item** | held block | `grep -n -i "3\.3 *v\|3v3"` over the whole #64006 guide and all eight per-board captures returns **one** hit, and it is the A/V board's audio tip. The mounting-hole figures (3.2 mm / 5 mm / 9.5 mm) ARE in the ingestion tree at `:39-42`; the supply voltage is not. Three-quarters held, one quarter a gap. What would settle it: the #64006 board schematics. |
>
> Status: `CONFIRMED`.

---

## The `architecture/`/`language/`/`guides/`/`application-notes/` uncited-block purge — the removal record «#293» owed and did not write (2026-08-25, arbiter) — F-347

> **Why this exists.** «#293»'s own PROTECTION POINT required *"every removal recorded with its
> origin so «#299» can work from a list rather than from git archaeology."* It was not written —
> its executor mirrored only the `io_pin_timing.yaml` portion into the register and left the rest
> in its transcript, which does not survive. **The arbiter verified that task green without
> checking that specific deliverable; that is the miss, and it is the arbiter's, not the
> executor's.** Caught at «#298»'s entry, because «#298» population 2 and «#299» both consume this
> list.
>
> **Reconstructed mechanically** from `git show --unified=0 15c84de5 -- deliverables/ai/P2/`,
> taking every removed line that begins a top-level YAML key. Nothing is lost — the purge is fully
> recoverable from git — but recoverable is not the same as recorded, and a list nobody can find
> is a list that gets re-derived under time pressure.
>
> ⚠️ **COUNT DISCREPANCY, STATED RATHER THAN SMOOTHED: this reconstruction yields 60 top-level key
> deletions; the executor reported 59 blocks.** The likely cause is one key counted differently
> (a `description:` removed as part of a larger block, or a nested key at column 0). «#298» and
> «#299» should work the 60 and treat any that resolves to "was never a block" as a no-op rather
> than assume the reconstruction is wrong. Do not reconcile to 59 by deleting a row.
>
> **Sibling records:** «#294»'s two are in F-334 above (48 blocks / 16 files, and 11 / 6).
>

- **F-347 — «#293»'s removal record was never written, so 60 removed blocks existed only in a git
  diff and in a transcript that does not survive.** — `PARTIAL`

  > **Headline corrected `PENDING-VALIDATION` → `PARTIAL` 2026-08-25 («#302»), to agree with this
  > entry's own Disposition line.** `PENDING-VALIDATION` asserts the fix is fully applied and only
  > its validation is owed; that is not this entry's state. The Disposition sets the closing
  > condition as *"every row carries a returned/not-returned outcome"*, and **the reconstructed
  > table below still has four columns — File · block · pre-removal line · span — and no outcome
  > column at all.** «#299» did execute against it (F-352: *"Forty-five of F-347's sixty blocks came
  > back cited. Two did not"*), so **47 of the 60 rows are accounted for in narrative** — but the
  > record itself carries no outcome column, and the remaining **13 rows are not accounted for by
  > that sentence** (whether each is held in the ingestion tree or simply unstated was NOT
  > determined here — that determination is part of the work this entry still owes). Writing the
  > outcomes onto the rows is **work**, not validation. This disagreement was invisible to check 10 for the same
  > reason as F-355's: the entry declares its status as an indented `Disposition.`/`Status:` line
  > rather than a column-0 `**Status:**`.

  «#293» removed 59-60 uncited quantitative blocks from `architecture/`, `language/`, `guides/`
  and `application-notes/`, and its PROTECTION POINT required that every removal be recorded with
  its origin *"so «#299» can work from a list rather than from git archaeology."* The executor
  mirrored only the `io_pin_timing.yaml` portion into the register. The remainder was left in its
  transcript.

  **The arbiter passed that task green without checking that deliverable.** The other protection
  criteria — the four entry gates, the zero Tier-1 count, the crossref clean — were all verified
  and all held; the *record* was the one criterion nobody re-ran, because it is the only one with
  no instrument behind it. That is the generalizable lesson: **a protection-point criterion that
  no tool can check is the criterion that silently does not happen**, and it needs a named,
  eyes-on verification step rather than inheriting the confidence of the gates around it.

  Reconstructed mechanically at «#298»'s entry (the first task to consume it) from
  `git show --unified=0 15c84de5 -- deliverables/ai/P2/`. The table above is that reconstruction.
  Nothing was lost — a purge is fully recoverable from git — but *recoverable* is not *recorded*,
  and a list nobody can find is a list that gets re-derived under time pressure by whoever needs
  it next.

  **EXECUTED 2026-08-25 by «#299». Every one of the 60 rows now carries an outcome, and the
  count is stated in four numbers rather than one total:**

  | Outcome | Count | What it means |
  |---|---|---|
  | **restored with a trace** | **45** | The repaired source states it and it is ACTIONABLE. Every returned block carries a `source:` naming the document and a `file:line`. |
  | **held out — no ingestion home** | **1** | `architecture/io_pin_timing.yaml best_practices` (generic PCB-layout advice). CORRECT-BUT-NOT-ACTIONABLE per «#298»; see F-352 for why it was not written to the ingestion tree either. |
  | **gap** | **1** | `architecture/click_module_integration.yaml best_practices` — ACTIONABLE per «#298», but no ingested source states any of it. See F-352 for what would settle it. |
  | **never returns (UNSOURCED)** | **13** | The F-327 fabrication family, ruled by «#298». Re-verified absent at HEAD: all nine `io_pin_timing.yaml` keys and all four `basic-io.yaml` twins return `grep -c` = 0, and `grep -rn "150mA\|75mA\|~2000Ω\|3-7ns\|pull_up_modes\|pull_down_modes"` over `deliverables/ai/P2/` returns **0**. |

  45 + 1 + 1 + 13 = 60. **The dispatch's own numbers were checked against disk:** the body's "65
  blocks" is wrong (it is 60, as this entry already recorded), and the register header's
  **`Next gap ID: G-007` is stale** — `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates
  G-007 (Smart Pins / ADC, ANSWERED 2026-08-24). No G-number was allocated by «#299» for that
  reason; its gap is filed as F-352 instead.

  Two blocks were returned **corrected rather than verbatim**, as C4 required: both
  `internal_pull_resistors` blocks now teach the hardware-verified `P_HIGH_15K` + DIR-high /
  `P_LOW_15K` + DIR-low form from `architecture/pin-drive-configuration.yaml idioms` (EF-063,
  EF-064), and neither reintroduces a `pull_up_modes:` / `pull_down_modes:` key. Both
  `pin_architecture` blocks returned without the `drive_strength: 1.5mA to 150mA` line.

  `PENDING-VALIDATION` — the record is written and executed against; only the YAML release is owed.

### Removal record — «#293», reconstructed by the arbiter 2026-08-25

| File | Top-level block removed | pre-removal line | span |
|---|---|---|---|
| `application-notes/p2an001-single-pin-instrumentation-adc.yaml` | `gotchas` | 92 | 16 |
| `application-notes/p2an002-cordic-for-real-work.yaml` | `gotchas` | 102 | 14 |
| `application-notes/p2an003-dac-analog-signal-generation.yaml` | `key_parameters` | 91 | 13 |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `gotchas` | 97 | 16 |
| `architecture/boot-rom/_index.yaml` | `boot_timing` | 25 | 6 |
| `architecture/boot-rom/_index.yaml` | `boot_paths_summary` | 155 | 18 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `boot_time_clock_state` | 64 | 27 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `pin_triple_duty` | 64 | 27 |
| `architecture/boot-rom/spi-flash-boot.yaml` | `boot_pattern_trigger` | 29 | 7 |
| `architecture/click_module_integration.yaml` | `best_practices` | 185 | 25 |
| `architecture/clock_system.yaml` | `configuration_constants` | 22 | 34 |
| `architecture/clock_system.yaml` | `configuration_rules` | 22 | 34 |
| `architecture/clock_system.yaml` | `pll_system` | 98 | 65 |
| `architecture/clock_system.yaml` | `hubset_configuration` | 98 | 65 |
| `architecture/clock_system.yaml` | `clock_modes` | 98 | 65 |
| `architecture/clock_system.yaml` | `stabilization_timing` | 175 | 6 |
| `architecture/clock_system.yaml` | `clock_specifications` | 253 | 15 |
| `architecture/clock_system.yaml` | `anti_patterns` | 279 | 21 |
| `architecture/io_pin_timing.yaml` | `description` | 10 | 6 |
| `architecture/io_pin_timing.yaml` | `timing_specifications` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `clock_relationships` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `drive_strength_configurations` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `slew_rate_control` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `input_characteristics` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `special_timing_modes` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `protocol_timing_examples` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `compensation_techniques` | 359 | 33 |
| `architecture/io_pin_timing.yaml` | `best_practices` | 359 | 33 |
| `architecture/pin-power-domains.yaml` | `description` | 16 | 15 |
| `architecture/pin-power-domains.yaml` | `board_power_grouping` | 43 | 9 |
| `architecture/serial_loader.yaml` | `boot_sequence` | 11 | 26 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `operation` | 21 | 6 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pin_behavior` | 55 | 7 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pwm_characteristics` | 189 | 5 |
| `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | `detailed_description` | 8 | 13 |
| `architecture/smart_pin_patterns.yaml` | `notes` | 251 | 9 |
| `architecture/smart_pins.yaml` | `input_routing` | 148 | 19 |
| `architecture/smart_pins.yaml` | `related_components` | 405 | 7 |
| `architecture/smart_pins.yaml` | `electrical_limits` | 504 | 4 |
| `guides/pasm2-getting-started.yaml` | `file_structure` | 48 | 66 |
| `language/pasm2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `control_registers` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `drive_strength_configuration` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `internal_pull_resistors` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `timing_considerations` | 371 | 6 |
| `language/pasm2/concepts/streamer_smartpin_control.yaml` | `protocol_client_code_note` | 480 | 8 |
| `language/pasm2/setxfrq.yaml` | `common_values` | 53 | 13 |
| `language/spin2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `control_registers` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `drive_strength_configuration` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `internal_pull_resistors` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `timing_considerations` | 339 | 8 |
| `language/spin2/debug-commands/pc_key.yaml` | `description` | 4 | 5 |
| `language/spin2/debug-commands/pc_key.yaml` | `usage_rules` | 15 | 8 |
| `language/spin2/methods/getct.yaml` | `pitfalls` | 120 | 19 |
| `language/spin2/methods/waitms.yaml` | `notes` | 84 | 13 |
| `language/spin2/methods/waitms.yaml` | `limitations` | 84 | 13 |
| `language/spin2/methods/waitus.yaml` | `notes` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `limitations` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `clock_frequency_impact` | 92 | 20 |

**60 top-level blocks across 25 files.**

> **Disposition.** `PARTIAL` — the record exists now and is usable; it closes when «#299» has
> executed against it and every row carries a returned/not-returned outcome.

---

## WRPIN D-operand field map: three field descriptions wrong in the YAML, ten mode numbers footnote-fused in an ingestion artifact (2026-08-24, `KNOWLEDGE-GAPS` pass-6 catch-up) — F-331, F-332

> **Origin.** The pass-6 gap-ledger catch-up read the WRPIN bit-field map in both 2026-08-24
> repaired captures (P2 Datasheet pp.23-25, P2 Hardware Manual Tables 16-25) to close
> `KNOWLEDGE-GAPS.md` **G-001** and **G-008**. Both defects below were found while doing that
> reading. **Nothing is fixed in this filing.**

### F-332 — the P2 Hardware Manual's table artifact carries ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note — `CONFIRMED`

**Location:** `engineering/ingestion/sources/p2-hardware-manual/complete-tables-reference.md:287-314`
(Table 25) and the same table in
`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1030-1036, 1053, 1054, 1056`.

**Ten values, each a 5-bit mode with its superscript footnote `¹` fused on:** `001001` `001011`
`001101` `001111` `010001` `010011` `010101` `110111` `111001` `111101` — correctly
`%00100¹` `%00101¹` `%00110¹` `%00111¹` `%01000¹` `%01001¹` `%01010¹` `%11011¹` `%11100¹`
`%11110¹`, footnote 1 being *"OUT signal overridden"* (the artifact carries that footnote
immediately below the table).

**This is a known, already-adjudicated class — and the adjudication is in the wrong file.** The
`p2-datasheet` artifact names the identical defect as reconciliations **R1** and **R2**
(`sources/p2-datasheet/complete-tables-reference.md:49-50`), decided by three of four extraction
paths plus a visual read of the rendered pp.34-35, and its **R8** even records that "The Hardware
Manual's DOCX (Table 9) carries the identical fusion, so this reconciliation applies to both
sources" — for Table 9's `INA`/`INB` only. **No such note exists anywhere in the Hardware
Manual's own artifact** (a case-insensitive search of that file for *footnote*, *superscript*,
*reconcil*, and *OUT signal overridden* returns nothing).

**KB impact: NONE today — recorded so it stays that way.** No fused value reached
`deliverables/ai/P2/` (grepped for all ten; the only near-hits are COGINIT mode bits in
`spin2/patterns/implementation/spin2_cog_management.yaml`, unrelated). The exposure is forward:
an agent deriving smart-pin YAML from the Hardware Manual artifact alone gets `%001001` for
pulse/cycle output.

**Proposed correction (ingestion head, not a YAML edit):** add the R1/R2 reconciliation note to
`sources/p2-hardware-manual/complete-tables-reference.md` beside Table 25, in the form the
datasheet artifact already uses. **Wider question worth one pass:** the DOCX walk drops
superscript markers into the adjacent numeral generally — Table 9's `INA1`/`INB2` is the same
mechanism, so Table 25 is unlikely to be the only other instance.

---


## Six defects surfaced while building the single constant-definition home (2026-08-25, «#295» phase 2) — F-336…F-341

> **Origin.** All six were found while implementing «#295» — promoting the drive ladder into the
> KB and collapsing two `P_*` definition homes into one. Two are fixed in that same pass and are
> marked so; four are not this task's repair and are filed for the task that owns them. Every
> number below was measured against disk on 2026-08-25, not carried from the design.

### F-336 — the weak-drive idiom set is one composition wide: `P_HIGH_15K | P_LOW_FLOAT` has neither a Parallax statement nor a bench result, and the ladder has never been swept against a load — `CONFIRMED`

> **This is a GAP, filed instead of content.** Read the arbiter's F-322 attribution correction in
> the section below first — it settles where the `P_HIGH_15K | P_LOW_FLOAT` string comes from
> (`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:284-287`, our own derived
> catalog extract) and it is not re-filed here.
>
> **What is missing, stated positively.** Spin2 v55 — the current edition — defines both constants
> individually (`spin2-v55-text.txt:1504` `P_HIGH_15K | Drive high 15kΩ`; `:1519` `P_LOW_FLOAT |
> Float low`) and composes them into **no idiom at all**. The empirical ledger carries the
> *other* composition: EF-063 and EF-064 both use `P_HIGH_15K` / `P_LOW_15K` with **DIR high** and
> **never** `P_LOW_FLOAT` (`P2-EMPIRICAL-FINDINGS.md:827,840`). So the one-sided variant — weak on
> one side, floating on the other, which is what an open-drain-style idiom actually needs — is
> asserted by nothing.
>
> **What is owed, and it is a bench item.** Extend the EF-063/EF-064 rig
> (`campaigns/2026-08-manual-corrections/tests/test-f272-streamer-dac-tt.spin2:212-220` is the
> routine) to (a) run `P_HIGH_15K | P_LOW_FLOAT` with DIR high against a known load and record
> whether it behaves as a one-sided weak drive, and (b) sweep all eight ladder rungs on both sides
> against the same load, so the KB can say what each rung does rather than only what the legend
> calls it. Until then `architecture/pin-drive-configuration.yaml` ships the two verified idioms
> and names this omission in its own `idioms.not_documented_here:` block.
>
> **«#296» must not ship the `P_HIGH_15K | P_LOW_FLOAT` string as sourced.**

### F-337 — the P2 Datasheet and the P2 Hardware Manual agree with each other and contradict the Silicon Doc on `%TT` in DAC_MODE, and the shipped YAML follows the minority source — `PARTIAL` (re-verified 2026-10-05 «#386»: EF-071 settles the smart-mode row; the smart-pin-off DAC_MODE %TT=00 row has no bench result)

> **Two disagreements, both in the `(T) Pin DIR/OUT Control` table, both about whether it is the
> DAC or the ADC that gets enabled.**
>
> | Context | Datasheet 2022/11/01 + Hardware Manual 2022/11/01 | Silicon Doc v35 |
> |---|---|---|
> | smart pin off, DAC_MODE, `%TT = 00` | **`DIR enables DAC`**, M[7:0] sets DAC level | **`OUT enables ADC`**, M[7:0] sets DAC level |
> | DAC smart-pin modes (`%SSSSS = %00001..%00011`), `0x` | `OUT enables **DAC** in DAC_MODE`, M[7:0] overridden | `OUT enables **ADC** in DAC_MODE`, M[7:0] overridden |
>
> **Verbatim locations, all four read this session:**
> `engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1175` and `:1183` ·
> `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:897` and `:905` ·
> `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:83` and `:98`.
>
> **Where the KB stands.** `deliverables/ai/P2/architecture/smart_pins.yaml`
> `configuration_format.fields.tt.behavior_by_context` carries the **Silicon Doc** wording in both
> places (`dac_mode."%00": "OUT enables ADC, M[7:0] sets DAC level"` and
> `dac_smart_pin_modes.adc_control: "0x=OUT enables ADC..."`). Two agreeing 2022/11/01 sources say
> otherwise, and this is the field an agent reads to work out why a DAC will not drive.
>
> **Not resolved here, and not guessable.** EF-054/EF-055 already probed this bit family
> empirically (they established that `%01` switches the DAC's *source*), so the ledger may already
> settle it or be one short rig away from settling it. Empirical outranks both documentary
> sources; that is the route, not picking the majority.

### F-341 — six of our own derived analysis documents sit at the root of `engineering/ingestion/sources/`, repeat the pull-up mislabel F-321 exists to kill, and are inside the fidelity gate's declared *Parallax documentary* truth root — `PARTIAL`

> 🔴 **THE LATENT DISARM WENT ACTIVE, EXACTLY AS THIS FINDING PREDICTED — and is now closed
> at the instrument (2026-08-25, «#305»).** This entry says the disarm is "a shape away, not a
> policy away". «#305» changed the shape (the harvest had to read the current-edition v55
> table, whose rows put the name in column 2), and with the repaired parser and no guard,
> `p2-complete-signal-flow-matrix.md:100` — a **signal-flow** table whose last cell happens to
> hold a constant name — defined `P_PWM_SAWTOOTH` as **"P38"**, the pin number in the
> neighbouring cell. One of our own derived documents teaching the instrument our own
> inference, in the first run after the shape changed.
>
> **Closed structurally, not by a list of six names.** An ingested source **is a directory**:
> every real source under `sources/` lives in its own folder because that is what the ingestion
> process creates, so a loose file at the root of a truth root was put there by something else
> and is not an ingested source document (`MIN_DEPTH_BELOW_ROOT`). That rule excludes all
> **twelve** loose files at `sources/` top level, not just these six, and it catches the next
> stray file without an edit. A second, independent guard bounds the name cell to the first two
> columns — a constant in the last column is a *use*, not a definition. Both carry negative
> controls, including the exact `P_PWM_SAWTOOTH | P38` row.
>
> **`TRUTH_ROOTS` was NOT widened or narrowed** — the roots are unchanged; only what counts as
> a file inside them is now defined.
>
> **Still open, and it is the half this finding actually asked for:** the six documents remain
> at `sources/` top level, still asserting a 15 kΩ internal pull-up the P2 does not have. The
> instrument can no longer be misled by them; a reader still can. Relocating them to a derived/
> analysis area, or repairing them against the Datasheet legend, is unchanged and unowned.
>
> Status: `PARTIAL` — instrument disarm closed and controlled; the invented-part-number half
> is closed at every site in the repository (2026-08-26, «#323» — see the boxed note under
> F-356); the content relocation, and the four further unverified part numbers those files
> carry (#64028, #64029-as-combo, #40003, #40007), are owed.

> **The six**, all at `engineering/ingestion/sources/` top level, all self-describing as
> generated cross-references rather than Parallax publications:
> `p2-board-addon-compatibility-matrix.md` · `p2-complete-signal-flow-matrix.md` ·
> `p2-hardware-validation-checklist.md` · `p2-board-power-analysis-matrix.md` ·
> `p2-board-pin-mapping-knowledge.md` · `p2-addon-board-circuit-knowledge.md`.
> Their own subtitles give them away — *"Complete cross-reference for automatic code generation"*,
> *"Comprehensive testing procedures"*, *"Knowledge Base"*. No Parallax document is named on any
> of them.
>
> **What they assert.** The F-321 mislabel, verbatim and repeatedly:
> `p2-complete-signal-flow-matrix.md:127` *"WRPIN(pin, P_HIGH_15K) ' 15kΩ pull-up"*, `:62`
> *"Input Type: Digital with internal pull-up"*, `:65` *"220µA through pull-up when pressed"*;
> `p2-board-power-analysis-matrix.md:79` *"Internal pull-up: 15kΩ to 3.3V"*;
> `p2-board-addon-compatibility-matrix.md:84` *"8 × 220µA pull-up current = 1.76mA"*;
> `p2-hardware-validation-checklist.md:198` *"Enable internal pull-ups"*. The P2 has no such
> component — `P_HIGH_15K` selects **drive strength**, per the Datasheet p.24 Pin Mode Legend
> (`p2-datasheet-text.txt:1139-1147`). The 220 µA and 1.76 mA figures are stated by no Parallax
> source.
>
> **Why it is more than stale prose.** `audit-constant-fidelity.py` scopes its truth side to
> `TRUTH_ROOTS = [ingestion/sources, ingestion/smart-pins-catalog]` with a comment explaining that
> an unauthoritative source does not add a wrong answer, it **DISARMS the check** — that is why
> `external-inputs/` was excluded. These six are unauthoritative and are *inside* the root.
> **Measured today: they contribute 0 entries to the truth table**, because their pull-up lines do
> not happen to match `ROW_RE` or `BULLET_RE`. The disarm is latent, not active — a shape away, not
> a policy away.
>
> **What is owed.** Decide what these files are and put them where that is true: relocate to a
> derived/analysis area outside `sources/`, or repair them against the Datasheet legend and label
> their provenance. Either way they must stop reading as Parallax documentary sources.
> **Same class as the arbiter's F-322 correction** — a derived extract inside the ingestion tree
> mistaken for the source it was derived from. Two instances in two days makes it a class, not an
> accident: an audit of what actually lives under `ingestion/sources/` is owed.

---

## `object-image-dedup.yaml`'s map_caveat goes stale when pnut-ts 1.55.4 ships (2026-08-22) — F-320

### F-320 — `p2kbSpin2ObjectImageDedup`'s `map_caveat` warns readers off .map labels that 1.55.4 makes correct, while the limitation that SURVIVES the fix is documented nowhere. `PARTIAL — the hold's conditions are met (pnut-ts 1.55.8; map_caveat rewritten and shipped); the SYMBOL INDEX per-source-file limitation is still documented nowhere and unmeasured on 1.55.8 (re-verified 2026-10-05 «#386»)`

**Origin.** `engineering/ingestion/external-inputs/p2kb-update-requests/P2KB-map-caveat-retraction-1.55.4.md`
— an upstream request from the pnut-ts side proposing an amendment. Treated as **input, not
authority** ([[feedback_upstream_input_docs_not_authority]]): its finding was checked here, its
proposed text was not adopted.

**The site.** `deliverables/ai/P2/language/spin2/concepts/object-image-dedup.yaml:123-126` — the only
copy. Four other files reference the entry (`method-pointers`, `object_archetypes`, `OBJ`,
`shared-bus-replication`) but none duplicate the caveat.

### Measured HERE on pnut-ts 1.55.3, 2026-08-22 — the "before" baseline

Rebuilt the entry's own `cascade_through_tiers` fixture and read it as `verification.method` says
to. **The label defect reproduces, and is worse than the request describes:**

```
  case4  (1 methods)
      +-- A : casc_mid
      |   \-- LEAF : object_3          <- placeholder name
      |       \-- child_0 : object_4   <- a tier that DOES NOT EXIST
      \-- B : casc_leaf                <- wrong SOURCE FILE (B is casc_mid)
```

B's real child is absent and an extra tier is invented. **Send upstream as a 1.55.4 regression
check** if their fixtures do not already cover the invented-tier and wrong-source-file shapes.

Two things confirmed independently of the fix, and they are why the entry is otherwise sound:

- **`Objects: 5`** — exactly the entry's measured value. The count IS reliable, as the caveat says.
- **`SYMBOL INDEX` carries ONE `MTAG` ($00034) and ONE `LTAG` ($00048)** while `MEMORY LAYOUT`
  shows two images of each source. The second image's DAT addresses appear nowhere in that section.
  This is **structural — symbols are stored per source file — so it is NOT version-coupled and
  survives the 1.55.4 fix.** It is documented in no punch list here despite the request saying it is
  tracked, so this entry is also that gap's only record.

### The proposed text is REJECTED — it reinstates the shape PL-004 just stripped from this file

The request asks for prose reading *"Fixed in pnut-ts 1.55.4. Through 1.55.3 the multi-instance .map
could show… As of 1.55.4…"*, and offers a `verification.method` line *"confirmed correct at pnut-ts
1.55.4"* as an alternative anchor. **Both are build stamps.**

`[[reference_kb_is_always_latest_no_version_citations]]` — *cite the EDITION, never the BUILD* — uses
**this exact file** as its worked example: it said *"re-verify on a compiler version bump"* pinned at
v1.55.0 while v1.55.3 was installed; the bump had happened and the re-verify had not. PL-004 removed
the `toolchain:` field for that reason, and `verification.method` now carries the durable
replacement: *"Compiler-coupled behaviour: re-measure rather than assume if a result surprises you."*

The request understood half of it — it dropped its own `toolchain:` proposal as moot — then moved the
build numbers into prose. Same rot, different field.

### Amendment to apply (current-state only, nothing to maintain at the next bump)

```yaml
  map_caveat: |
    SYMBOL INDEX reports one row per SOURCE FILE, so when an override forks a file into
    several images only the first image's DAT address appears there. For per-instance DAT
    addresses read MEMORY LAYOUT or ADDRESS INDEX, which list every image. The Objects:
    count is reliable.
```

Nothing else in the entry needs changing: `description`, THE RULE, `singleton_rule`,
`forking_a_dat_region`, `the_silent_trap`, `the_other_silent_trap`, `cascade_through_tiers`,
`completeness_rule` and `verification.measured` all re-read clean against the request's own
re-measurement.

### Why it is HELD, and what releases it

**Sequencing is the whole reason.** On 1.55.3 the labels genuinely ARE wrong — measured above — so
dropping the warning while readers are still on 1.55.3 publishes guidance that is wrong for them.
The amendment is only correct once 1.55.4 is what people have.

Release conditions, both required:

1. **pnut-ts 1.55.4 is in this devcontainer**, so the fix can be verified here rather than taken on
   the request's word. The container is on 1.55.3 (`Build date: 8/9/2026`) as of filing.
2. **The compiler side's test source set is in hand** — offered 2026-08-22 and expected to evidence
   the new map details directly, so the fixtures do not have to be reconstructed from the entry's
   prose. Re-run the "before" shapes above against it; every one should invert.

Then: apply the amendment, and record the result in `verification.measured` **without a build
number**.

> ### GAP RECORDED 2026-08-25 («#300») — the HELD decision stands, and both release conditions were MEASURED
>
> This finding was on «#300»'s roster and **closes this sprint as a recorded gap, not as work**. Stephen's
> 2026-08-22 decision to hold it was **not re-opened, not re-argued, and the amendment was not applied.**
> The only thing done here was to check — rather than assume — whether the two release conditions this entry
> names have since been met. **Both are still unmet:**
>
> 1. **pnut-ts 1.55.4 is NOT in this devcontainer.** `pnut-ts --version` → **`PNut-TS: v1.55.3`**. The
>    compiler that makes the amended text true is still not the one installed, so publishing the amendment
>    now would hand 1.55.3 readers guidance that is wrong *for them* — the exact sequencing risk this entry
>    was held on.
> 2. **The compiler side's test source set is NOT in hand.**
>    `engineering/ingestion/external-inputs/p2kb-update-requests/` contains only the originating request,
>    `P2KB-map-caveat-retraction-1.55.4.md`. No fixture set accompanied it.
>
> **What would settle it:** both conditions together — 1.55.4 installed here, plus the fixtures — after which
> the entry's own "before" shapes (placeholder name, invented tier, wrong source file) are re-run and every
> one should invert. **Until then this is a gap, and the KB text stays as it is.**
>
> **The half that is NOT version-coupled remains this entry's only record**, and is unaffected by the hold:
> `SYMBOL INDEX` stores symbols **per source file**, so a forked file's second image has no row there. That
> survives 1.55.4 and is documented nowhere else.

## An ADC comparator example still states the input threshold in fixed volts, in the manual F-412 just repaired (2026-09-11) — F-424

### F-424 — IOSP §2.5's ADC comparator example quotes `~1.65V` as an input threshold without the supply-fraction caveat the same manual now carries everywhere else — `CONFIRMED`

Found 2026-09-11 while **validating F-412 on the released PDF** — which is the point worth
recording: the validation pass for one finding is where the residual sites of its class surface,
because it is the only pass that reads the whole artifact looking for that exact shape.

`P2-IO-and-Smart-Pins-User-Guide.pdf` **page 59** (§2.5 ADC modes), in the worked example:

```
' Detect when analog input exceeds ~1.65V (mid-scale)
WRPIN(adc_pin, P_ADC_1X)
PINFLOAT(adc_pin)
```

**Why this is the F-412 class and not a duplicate of it.** F-412 named
`chapter-12-digital-input.md:25` and `:95` and was repaired there — p184 now states the threshold
as a fraction of `Vxxyy` (0.3 / 0.5 / 0.7), calls it a band rather than a point, and ends
*"Quote 1.65 V as the typical value at 3.3 V, never as the switching point."* This site is a
**different chapter** and states a comparator trip point as a fixed voltage with no supply
reference at all. `(mid-scale)` carries the fraction implicitly for a reader who already knows
the rule; the reader who meets this page first does not.

**It is genuinely wrong off-nominal, which is what makes it a finding rather than a style note.**
`Vxxyy` is specified 3.15 V - 3.45 V, so mid-scale spans roughly 1.58 V - 1.73 V, and pin groups
on different supplies do not share a threshold. The manual states this itself at p184 and again at
p187 (*"the fraction is what the level fixes"*) and p195 (*"Levels below assume Vxxyy = 3.3V;
scale them to your I/O supply"*) — three sites carry the caveat and this one does not.

**Fix.** One line, in
`engineering/document-production/workspace/p2-io-and-smart-pins-user-guide/opus-master/` §2.5:
state the trip point as mid-supply and give 1.65 V as the value at a nominal 3.3 V, matching the
vocabulary p184 already established. Do not delete the number — the reader needs a figure to
aim at; it needs the supply attached to it.

**Class sweep owed with the fix** (`feedback_classwide_sweep_on_every_finding`): re-read every
site in the IOSP that names an input threshold or comparator trip point in volts and confirm each
carries the supply. This entry records only the site the F-412 validation pass happened to cross.

---

## YAML→Manual impact survey — KB v1.16.3 (2026-08-16, `release-yamls` §8)

Delta: `spin2/methods/wrpin.yaml` · `architecture/smart_pins.yaml` ·
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` · `architecture/cordic.yaml` ·
`architecture/streamer/overview.yaml` · `architecture/streamer/dds-goertzel.yaml` ·
`pasm2/getxacc.yaml` · `spin2/integration/spin2-pasm2-integration.yaml` ·
`spin2/special-symbols/at.yaml`.

Intersected against every live manual's `MANUAL-DESCRIPTOR.md` declared sources. **Survey done, not
skipped.** Most intersections are already owned by an in-flight Sprint 2 task, so no duplicate flag
is raised for them; the ones that are **not** covered are flagged below.

| Element | Intersects on | Disposition |
|---|---|---|
| Streamer Guide | streamer, dds-goertzel, getxacc, DEBUG_COGS | **covered** — «#220» «#221» |
| IOSP | `architecture/smart-pins/`, smart_pins | **covered** — «#219» (and the F-264 %TT material rides its v1.0.9 pass) |
| Assembly Reference | cordic, streamer | **covered** — «#228» |
| P2AN002 | cordic | **covered** — «#236» |
| XBYTE Guide | streamer | **covered** — «#227» (§15.3 restructure); see the F-268 flag below |
| **P2AN001 / P2AN003** | wrpin | **⚑ FLAG — re-audit against v1.16.3.** These two were read site-by-site and taken OUT of the release wave, but that read answered **F-259's** question (does every executable example carry `\| P_OE`?). **F-264 is a different fact** — that `%TT` is context-dependent and that adding `P_OE`/`P_CHANNEL` to a **non-smart-pin cog DAC** kills it. Any cog-DAC or `P_DAC_*` configuration in these app notes was never checked against that. Do not treat the wave exclusion as covering it. |
| **P2AN004** | wrpin | **⚑ FLAG — same class as above**, and it was never in the wave at all. |
| **Architect's Guide** | CORDIC, streamer | **⚑ FLAG — re-audit against v1.16.3.** Not in the release wave. Declares both sources; the CORDIC hub-in-loop rule (F-263) and the `DEBUG_COGS` streamer caveat (F-266) are new since its last pass. |
| **DeSilva Tutorial** | CORDIC | **⚑ FLAG — re-audit against v1.16.3.** It *is* in the wave, but for §1/§2 (Acknowledgments, Appendix A) only — its CORDIC material is untouched by «#222»/«#223» and unexamined against F-263. |
| All elements showing PASM fragments | `spin2-pasm2-integration.yaml` | **⚑ FLAG — F-268 class sweep**, filed below and deliberately not folded into a correction task. |

These flags are the drift signal `document-audit` drains on each element's next pass. They are
**not** Sprint 2 scope and must not be pulled into it silently — surface them to Stephen as a scope
decision.

---

## Spin2/PASM2 boundary defect promoted from the empirical ledger (2026-08-16) — F-268

### F-268 — inside a Spin2 object, `##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address. `PARTIAL — KB DONE 2026-08-16; guide-side sweep owed`

**Origin:** EF-060, which had no F-number and no KB entry. Surfaced while getting the F-256/EF-058
rig working, so it is a by-product rather than a target — and it is the broadest-reach item the
2026-08 campaign produced.

**The fact.** A PASM fragment that is correct in a **standalone** PASM file reads **interpreter
memory** when pasted into a Spin2 object's `DAT` block: `##hubsym` resolves against `$400` rather
than the object's load address. Measured on real P2 silicon: `@disp` = `$1AF9` from Spin2 versus
`##disp` = `$0651` from PASM in the same object — **5,288 bytes apart**, and the `##` form returned
garbage.

**Why it matters more than its size suggests.** It bites anyone who copies a PASM fragment out of a
guide or reference into a Spin2 object — which is how most P2 code is written. It assembles, it
runs, and it reads the wrong memory. **Workaround:** pass hub addresses in from Spin2 with `@`, or
address through PTRA/PTRB.

> **KB APPLIED 2026-08-16 («#218»).**
> `language/spin2/integration/spin2-pasm2-integration.yaml` →
> `integration_rules.hub_address_resolution`: the rule, where it is instead correct (standalone
> PASM), why it bites, the workaround, and the measurement. Findability: a matching one-line pointer
> added to `language/spin2/special-symbols/at.yaml` `notes:`, since `@`'s
> object-relative-vs-absolute entry is exactly where a reader chasing this lands — that file already
> documented the Spin2 side of the same boundary and had no route to the PASM side.
> Source trace: EF-060.

**Still owed (manual head, NOT tasked in Sprint 2):** our guides present standalone-PASM fragments
without saying so. A class-wide sweep of `##hubsym`-style fragments across the live manual set is
the durable fix; scope it as its own item rather than folding it into a correction task.

> **KB + KB-GUIDE HALVES RE-VERIFIED ON DISK 2026-08-25 («#300») — both clean; only the MANUAL sweep remains.**
>
> - **KB half — DONE, confirmed at the file.**
>   `deliverables/ai/P2/language/spin2/integration/spin2-pasm2-integration.yaml:427-436` carries
>   `integration_rules.hub_address_resolution` complete: the rule, `correct_in` (standalone PASM),
>   `why_it_bites`, the `workaround` (pass `@` in from Spin2, or address through PTRA/PTRB), the
>   `measured` figures (`@disp` `$1AF9` vs `##disp` `$0651`, 5,288 bytes apart) and
>   `source: … P2-EMPIRICAL-FINDINGS.md EF-060 (2026-08-14)`. The findability pointer is live at
>   `language/spin2/special-symbols/at.yaml:219`.
> - **KB-guide half — NOTHING OWED, and this was measured rather than assumed.** Swept
>   `deliverables/ai/P2/guides/` for `##`-prefixed hub-symbol fragments: **zero hits**. The KB's guide layer
>   does not present any standalone-PASM fragment that would carry this defect, so there is no guide-side
>   sweep to run.
> - **What is left is the MANUAL set only** — the class-wide sweep named above, which is «#301»'s scope,
>   not a KB item. Status stays `PARTIAL` for that reason alone.

---

## Stephen's review of the Sprint 2 gate release (2026-08-16, «#234») — F-276…F-283

> **Full dispositions and reasoning:** `engineering/planning/SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md`.
> Eight observations (V-1…V-8) worked one at a time against the gate commit `fea28f1c`. Four became
> findings; the rest were scope and structure decisions recorded in that file.
>
> **All four are tasked into the voice-conformance family «#240»–«#248» and are absorbed into the
> per-manual pass rather than applied as point fixes** — applying them first and conformance-checking
> after would write the same prose twice and have the second pass judge what the first just wrote.
>
> **Two of these were found by the review, not by the sprint's own sweeps**, and that is the useful
> part: F-277's site sits in body text no Sprint 2 task touched. A findings-driven sweep sees the
> diff; it does not see the document.

### F-280 — `pnut_ts` survives in 16 masters as a command that does not run. `PARTIAL — the whole declared sweep APPLIED in opus-master 2026-08-25 («#301»); publication owed, per document`

**Found:** 2026-08-17 during the P2AN001/P2AN002 voice pass («#247»), by checking the compiler name
the two notes hand the reader against the name of the binary that exists.

**This was already adjudicated and only half-swept.** Commit `c203fa52` (2026-08-11) established the
finding on its merits: `command -v pnut_ts` finds nothing, the installed binary is `pnut-ts`, and the
tool's own usage banner reads *"PNut-TS: Usage: pnut-ts [optons] filename"*. SSDB and the PNut-Term-TS
guide were corrected then — 21 sites — and both voice guides were amended so it could not come back.
**The rest of the set was never swept.** Thirty-three occurrences remain across eighteen files, against
thirty-nine correct ones — a near-even split, so the set currently teaches both.

**Fixed in this pass (2 sites, the two notes being touched):** `P2AN001/opus-master/CHANGELOG.md:37`
and `P2AN002/opus-master/CHANGELOG.md:35`. Both are reader-facing — an app-note CHANGELOG is promoted
to the published `p2anNNN-changelog.md` beside its PDF.

**Remaining (31 sites, 16 files) — the class-wide sweep this finding owns:**

| Element | Sites |
|---|---|
| Getting Started Guide | `getting-started-body.md` ×1 — **highest reader risk**: a beginner's first compile |
| Architect's Guide | `architect-guide-body.md` ×1, `CHANGELOG.md` ×2 |
| ~~Assembly Language Manual~~ | ~~`CHANGELOG.md` ×1~~ — **CLEAR, verified 2026-08-22**: `pnut_ts` appears nowhere in `opus-master/`. (Its three *process* docs carried 10 tool-invocation uses; corrected the same day. The remaining hits in `audit/`, `archive/` and `code-validation/` are frozen records, and `external-inputs/pnut_ts_facts/` is a real path — all correctly left alone.) |
| PNut-Term-TS Guide | `CHANGELOG.md` ×1 (the body was swept at `c203fa52`; its CHANGELOG was missed) |
| deSilva | `archived-2025/README-COMBINED-MASTER.md` ×3 — **archived scaffolding, not shipped; excluded** |
| P2AN003 – P2AN007 | body ×17, `CHANGELOG.md` ×5 |

**Not swept here on purpose.** Conform-on-touch: these elements are not being touched by Sprint 2, and
pulling sixteen masters into a voice pass is the big-bang sweep the rule exists to avoid. Each takes it
at its next visit — this row is what makes sure the visit knows.

**The correction is one substitution** — `pnut_ts` → `pnut-ts` — with no prose consequence. Check each
site is the *command*; the project name in running text is properly **PNut-TS**.

> **SWEEP APPLIED 2026-08-25 («#301»). The conform-on-touch deferral above is discharged: the visit
> came.** All 27 reader-facing occurrences substituted across **14 files**, line counts unchanged
> (4,907 before and after), diff is exactly 27 insertions / 27 deletions.
>
> **⚠️ The row header's own arithmetic was wrong, and re-measuring it is how the extra defect turned
> up.** It reads *"Remaining (31 sites, 16 files)"*; the table under it sums to **30 sites / 15
> files**, because the `~~Assembly Language Manual~~ CHANGELOG ×1` row was struck through as CLEAR on
> 2026-08-22 and the header was never re-totalled. Measured on disk today: **30** occurrences across
> **15** files under `opus-master/`, of which **3** in **1** file are the excluded deSilva
> `archived-2025/README-COMBINED-MASTER.md` — leaving **27 in 14**, which is what was fixed. The
> table's per-element counts were all correct: Getting Started ×1, Architect body ×1 + CHANGELOG ×2,
> PNut-Term-TS CHANGELOG ×1, P2AN003–007 body ×17 + CHANGELOG ×5.
>
> **A second wrong name rode along on one of the lines, and is fixed with it.**
> `pnut-term-ts-user-guide/opus-master/CHANGELOG.md:106` carried *"`pnut_ts` + `pnut_term_ts`"* —
> **both** underscore forms, in the guide whose own `MANUAL-DESCRIPTOR.md:28` and `voice-guide.md:83`
> declare *"the underscore forms `pnut_ts` / `pnut_term_ts` are wrong and no such executable is
> installed."* `command -v pnut-term-ts` finds nothing under that spelling either; the installed
> binary is `/usr/local/bin/pnut-ts`. Corrected to `pnut-term-ts` in the same pass — leaving it would
> have fixed half a sentence.
>
> **Every site was checked for sense, not just substituted** — this finding requires it ("check each
> site is the *command*"). Counted off the pre-edit backups: **23 of the 27 are inside backticks**
> (13 as `` `pnut_ts -d` ``, 10 as bare `` `pnut_ts` ``), unambiguously the command. The **other 4**
> are the compound adjective *"pnut_ts-verified"* — `architect-guide/CHANGELOG.md:102` and `:114`,
> `architect-guide-body.md:19`, `getting-started-body.md:17`. Those are the one shape where this
> finding says **PNut-TS** might be proper instead; they were still taken to `pnut-ts` because
> "verified by running it" names the *binary*, and that is the form already shipping in running text
> at `p2-assembly-language-manual/opus-master/CHANGELOG.md:196` ("348 code examples audited with
> pnut-ts v1.51.7"). Two of the four (`architect-guide-body.md:19`,
> `getting-started-body.md:17`) sit inside the masters' `<!-- CONVENTIONS -->` authoring comments and
> reach no reader — corrected anyway, because a convention block that names a non-existent binary is
> how the next author reintroduces it. The result matches the form P2AN001/P2AN002 already ship
> (`P2AN001/opus-master/P2AN001.md:622`, `P2AN002/opus-master/P2AN002.md:357`), so the set no longer
> teaches both spellings. `grep -c pnut_ts` over `manuals/*/opus-master/` + `app-notes/*/opus-master/`
> is now **0** outside `archived-2025/`.
>
> **Deliberately NOT swept, and why:** the 3 sites in
> `p2-pasm-desilva-style/opus-master/archived-2025/README-COMBINED-MASTER.md` — archived scaffolding
> that ships to nobody, excluded by this finding's own table. Frozen records under `audit/`,
> `archive/` and `code-validation/`, and the real path `external-inputs/pnut_ts_facts/`, are likewise
> untouched.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on all
> 14 files. **No occurrence was inside a code fence** — verified by mapping every changed line number
> against the files' fence ranges — so no example file changed, byte-identity is untouched, and
> `pnut-ts` compilation does not apply to this finding.
>
> **What remains is publication, not authorship.** Nine reader-facing documents now carry the
> correction in source and none of them has been re-released: Getting Started, Architect's Guide,
> PNut-Term-TS Guide, and P2AN003–P2AN007. Each ships it at its next release. **This is not a render
> gate** — a token substitution has no layout consequence — so «#302» need not look at it; it is a
> release-wave item.

## Published PDFs carry no machine-readable rights (2026-08-21) — F-316

### F-316 — every published PDF states CC BY-SA 4.0 and a joint copyright on its own page, and carries neither in its metadata. `PARTIAL — mechanism DONE and PROVEN 2026-08-22; adoption is per document`

**How it surfaced.** Stephen, reading the Streamer v1.1.0 metadata at the «#287» gate, asked whether
the PDF's rights should name both companies. The `Author` field is correct as written — Iron Sheep
Productions is the author, and authorship is not copyright — but the question exposed that the
copyright and licence are **absent from the metadata entirely**.

**Measured on the returned v1.1.0 PDF:**

```
Title:            P2 Streamer Programming Guide
Subject:          Comprehensive Reference for Propeller 2 Streamer Hardware
Author:           Iron Sheep Productions, LLC
Custom Metadata:  no
Metadata Stream:  no          <- no XMP at all
```

while `front-matter.md:112` reads *"Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc."*
and the page below it grants **CC BY-SA 4.0**. Nothing in
`platform/templates/p2kb-platform-foundation.sty` sets `pdfkeywords`, and `hyperxmp` is not loaded,
so no `dc:rights` is emitted.

**Why it matters more than its size suggests.** CC BY-SA exists to be machine-readable. An
aggregator, a search index or a model crawler reading these files sees a document with no licence —
so a deliberately-open set reads as unlicensed, which is the opposite of the intent.

**The split is real, and the fix must respect it.** Surveyed 2026-08-21 across every manuscript:

| Population | Count | Copyright line |
|---|---|---|
| Manuals, guides and all 7 app notes | 17 | Iron Sheep Productions, LLC **and Parallax Inc.** |
| `pnut-term-ts-user-guide` | 1 | Iron Sheep Productions, LLC **only** |
| `Donna-Manuscript` | 1 | private, separate author — out of scope |
| `p2-layout-torture-test` | 1 | instrument, no copyright page — out of scope |

So the string **must be single-sourced per document from `request.json`**, never hardcoded in the
platform. A platform constant would silently attribute Parallax to the one document they have no
part in — precisely the class of defect the metadata single-sourcing work («#283») was built to end.

**Proposed correction.** Two new `request.json` metadata keys (`copyright`, `license`), consumed the
way `\DocTitle` / `\DocAuthor` already are. Emit through `\hypersetup{pdfkeywords=…}`, which needs no
new package; add XMP `dc:rights` via `hyperxmp` **only if** the Forge's TeX Live carries it — that is
unverifiable from the container and must be probed on the interactive daemon rather than discovered
in a production build.

**Sequencing — IN THIS WAVE. Stephen's call, 2026-08-21, overriding a first recommendation to
defer it.** The initial reasoning was that a platform change invalidates the built Streamer PDF and
everything queued behind it. That is true and it is the wrong trade: **this wave is the metadata wave
by design** — «#283» converted identity strings to platform single-sourcing and this release is the
first time the full metadata set reaches the documents. Deferring rights to a later adoption round
means a SECOND metadata round-trip for every document, and an interval in which every published PDF
carries half its metadata. One round-trip, complete, is cheaper and correct. Get it right the first
time it ships.

**Not a manuscript defect.** Every copyright page is already correct and states both parties where
both apply. Nothing in any master needs editing.

**Status:** `PARTIAL — the mechanism is DONE and PROVEN on a returned PDF; the other 17 documents adopt at their next render.`

> **PROVEN 2026-08-22 on the returned Streamer v1.1.0 PDF — read from the artifact, not the log.**
> `Keywords` now reads *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
> under CC BY-SA 4.0"*. `\DocCopyright`/`\DocLicense` join the `\Doc*` family, fed per document
> from its own `request.json`.
>
> **The build is byte-stable**: 91 pages, 24,737 words, and **ZERO pages whose text differs**
> from the pre-rights build — which is what a guarded metadata-only platform change should
> produce, and is now measured rather than assumed.
>
> **Two defects were caught by arming the gate against the returned build**, both mine, and both
> would have shipped: the first emitted string read *"Parallax Inc.. Licensed under"* because the
> template appended a full stop to a value that already ended in one (now a semicolon, fixed in
> the platform so none of the 17 documents still to adopt inherits it); and the gate itself was
> checking only that SOMETHING rights-shaped was present, never that the declared values actually
> arrived. It now verifies each one round-tripped. That is the second time in one day this gate
> passed on intent rather than artifact — worth remembering as a shape, not an incident.
>
> **Owed:** the other 17 documents, tracked in `PLATFORM-FEATURE-ADOPTION.md`'s new Rights column;
> and XMP `dc:rights`, which needs `hyperxmp` and stays gated on confirming that package exists in
> the Forge's TeX Live rather than assuming it. `Keywords` is the carrier today.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302»).** `pdfinfo` over all 15 files in
> `deliverables/documents/DOCs/`: **2 carry a rights `Keywords` string, 13 carry none.**
>
> - **Assembly Reference** — *"Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.;
>   licensed under CC BY-SA 4.0"*
> - **Streamer Guide** — *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
>   under CC BY-SA 4.0"*
> - **EMPTY:** Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide ·
>   XBYTE · P2AN001…P2AN007
>
> Both adopted strings use the **semicolon** form, so the *"Parallax Inc.. Licensed under"*
> double-stop defect is confirmed absent from everything that has shipped — the platform fix held,
> and none of the 13 still to adopt can inherit it.
>
> **The `pnut-term-ts-user-guide` split is intact and is the reason this must never become a
> platform constant:** its row is ✅ in the adoption table with the ISP-only string, distinct from
> the 17 joint-copyright documents.
>
> **Two things remain owed, and NEITHER can be discharged in this container:**
> 1. **13 published documents adopt at their next render** on `EXEC_ENV_CANONICAL`.
> 2. **XMP `dc:rights` stays gated on whether `hyperxmp` exists in the Forge's TeX Live** — a probe
>    on the interactive daemon, Stephen's side. Until then `Keywords` is the carrier and
>    `Metadata Stream: no` is expected, not a defect. **Do not "fix" this by loading `hyperxmp`
>    speculatively in a production build.**

---

## Nine documents carry a request.json subtitle their own cover contradicts (2026-08-22) — F-317

### F-317 — the subtitle in `request.json` disagrees with the printed cover in 9 of 15 published documents, and adopting metadata single-sourcing is what makes that visible. `PARTIAL` (re-verified 2026-10-05 «#386»: deSilva and Debug Window now agree; seven app-note subtitles still contradict their covers) — **all 9 re-measured 2026-08-25 («#302»): unchanged, still drifting, none adopted**

**How it surfaced.** Stephen: *"fix README if needed, always."* Sweeping the public index's
subtitle lines against the PDFs found 10 apparent mismatches — but checking them against
`request.json` was the wrong comparison, because **`request.json` only reaches the PDF for a
document that has ADOPTED metadata single-sourcing**, and only three have. Re-run against the
**printed cover**, the picture inverted: the README was right in almost every case, and it is
`request.json` that is out of step.

**The real defect, and it is latent rather than shipped.** For an unadopted document
`request.json`'s subtitle reaches nothing, so the disagreement is invisible. The moment that
document adopts — `\DocSubtitle` → `pdfsubject` — that string **becomes the PDF's Subject** and
contradicts the subtitle printed on its own cover. **This already happened once**: «#283» hit it
on the Streamer Guide, and the rule recorded then is **the cover wins**.

| Document | `request.json` subtitle | printed cover says |
|---|---|---|
| `p2-pasm-desilva-style` | Build, Experiment, and Master the Propeller 2 | A Human-Centered Approach to Parallel Processing |
| `p2-debug-window-manual` | See What Your Program Is Doing — Nine Display Windows for the Propeller 2 | See What Your Program Is Doing |
| P2AN001 | Application Note P2AN001 — No External ADC | Measure an Absolute Voltage in Microvolts on a P2 Pin |
| P2AN002 | Application Note P2AN002 — Hardware Math on the P2 | CORDIC for Real Work |
| P2AN003 | Application Note P2AN003 — No External DAC | Generate Analog Waveforms and Audio on a P2 Pin |
| P2AN004 | Application Note P2AN004 — No External Counter or ADC | Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin |
| P2AN005 | Application Note P2AN005 — Run Several Jobs in One Cog | Cooperative Multitasking with Spin2 TASK Methods |
| P2AN006 | Application Note P2AN006 — Size Every Stack, Catch Every Overflow | Sizing Cog & Task Stacks |
| P2AN007 | Application Note P2AN007 — STRUCT Records, Shared Safely Across Cogs | Data Structures with the New Language Facilities |

**Correction.** Before each document adopts metadata single-sourcing, bring its `request.json`
subtitle to the string its cover prints — **the cover wins**, per «#283». Doing it at adoption
time is the natural moment: that is the render where the value first matters, and
`audit-pdf-metadata.py` will compare the Subject against `request.json` on the returned PDF, so a
wrong value fails the gate rather than shipping. For the seven app notes, note their cover puts a
*descriptive line* under the title — decide per document whether that line or the catalog tagline
is the subtitle, rather than sweeping one reading across all seven.

**Also fixed here (2026-08-22):** the public index's bold line for the Streamer Guide read *"A
Guide to the Propeller 2 Streamer, Its Modes and Function"* while the document it links to prints
*"Comprehensive Reference for Propeller 2 Streamer Hardware"*. That one WAS shipped drift — the
catalog misdescribing the download — and is corrected. Every other index line was verified against
its cover and is correct; the app notes deliberately use `Application Note P2ANxxx · <topic>` as an
index label while their **heading** carries the cover's title, which is a consistent scheme, not
drift.

> **RE-MEASURED 2026-08-25 («#302») — all nine `request.json` subtitles read off disk: every one is
> UNCHANGED from the table above. The drift is intact, and none of the nine has adopted.** So the
> defect is still latent rather than shipped, exactly as recorded — but see the sharpening below,
> which changes when it stops being latent.
>
> ⚠️ **`pdfsubject` IS wired, so "latent until adoption" now means "fires at the very next
> adoption".** This entry was written while F-300 step 4 said *"Do NOT wire `pdfsubject`"*. The two
> adopted PDFs measured today both carry a populated `Subject` (Assembly: *"Complete PASM2
> Instruction Set Documentation"*; Streamer: *"Comprehensive Reference for Propeller 2 Streamer
> Hardware"* — the **cover** string, i.e. «#283»'s cover-wins rule already applied). Neither is in
> the drift table, which is why nothing has shipped wrong yet. **That is luck of ordering, not a
> guard.** The next of the nine to render will publish its `request.json` subtitle as the PDF
> Subject and contradict its own cover.
>
> **So the correction is now a PRE-RENDER step, not a same-render one:** bring the `request.json`
> subtitle to the cover string **before** staging that document, and let `audit-pdf-metadata.py`
> confirm it on the returned PDF. The seven app-note rows still need the per-document decision this
> entry calls for (cover descriptive line vs catalog tagline) — **do not sweep one reading across
> all seven.**

**Status:** `PARTIAL — resolve each document's subtitle to its printed cover BEFORE the render that adopts metadata single-sourcing; 2 of 9 resolved (deSilva, Debug Window), the seven app notes still drifting (re-verified 2026-10-05 «#386»).`

## Open — enhancement proposals (new content, not corrections)

- **ENH-03 — a gating compile step for every code block in `deliverables/ai/P2/`.** *Filed 2026-08-21;
  Stephen's call, and he asked for it in these words: "we must, for all code in YAML files, compile
  that code and assure ourselves that it compiles correctly. We do not publish a release unless all
  the code publishes correctly."* Nothing in this project compiles KB code examples, which is how
  F-311…F-313 and F-315 shipped. **Census: 1913 code-shaped blocks across 438 files; only 118 are
  complete programs, so 1795 need a synthesized context.** Design points already settled:
  - **The blocker is not the compiler, it is that the KB never declares which strings are code.** A
    heuristic sweep pulled 166 of 541 PASM2-shaped blocks out of *prose* fields. So the first
    deliverable is a per-block marker — `compile: program` / `compile: fragment` /
    `compile: never` + reason — not a runner. A guessing gate cries wolf, and a gate that cries wolf
    gets ignored.
  - **`compile: never` must be ASSERTED TO FAIL**, not skipped. The KB teaches anti-patterns; a
    wrong-code example that quietly starts compiling means the wrongness was edited away.
  - **It proves LEGALITY, not correctness**, and must never be cited otherwise. F-312 is the proof:
    fixing `qvector y_val` so it assembles would have left X and Y still swapped.
  - **No build stamps** (PL-004). The gate runs against whatever compiler is installed; a bump that
    breaks something turns the release red, which is the gate working. That is also what makes the
    surviving `re-verify on a compiler version bump` notes deletable.
  - Prototype validated 2026-08-21: it asks the compiler which identifiers are declarable rather than
    carrying a keyword list that would rot. 4/4 known-bad caught, 4/4 known-good passed. Its known
    weakness is auto-declaration colliding with symbols a block defines itself, which produced
    `Symbol is already defined` on blocks that compile correctly by hand — fix that before trusting
    any pass-rate number from it.
  - Hooks: `release-yamls` as a hard gate (~0.8 s/block, ~25 min full sweep), and
    `yaml-knowledge-base-maintenance` on touched files so it fails at edit time, not release time.

- **ENH-02 — make the platform fail loudly on a code line that cannot fit.** *Filed 2026-08-21 when F-281 closed.* F-281's three over-wide lines were fixed and v1.1.3 shipped margin-clean, but **nothing stops the class recurring**: `p2kb-platform-code-coloring.lua` emits `\begin{Verbatim}[xleftmargin=-10pt]` with no break options at all ten sites, and the `breaklines=true` at `p2kb-platform-foundation.sty:317` is a pre-existing `\lstset` that the Verbatim path never consults. So an over-long line silently runs off the page and the compile log stays clean — the exact shape of every render defect this project has shipped. The source-side `audit-code-line-length.py` gate catches most of it, and `audit-pdf-margin-overflow.py` catches it after the fact; what is missing is the platform refusing to typeset it. Not a defect in any document — an absent guard.

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** `TRACKED → ingestion` Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).
  > **Routing re-verified 2026-08-25 («#300») — still live, and one of its two inputs is missing.** The
  > routing target resolves: the grounding plan exists at the path above, and the first input is in hand —
  > `engineering/ingestion/sources/rom-booter/ROM_Booter.lst` **and** `rom_booter_v33_01j.lst` are both
  > present (the `v33_01j` copy is the one E-005 cites, so it is the mined edition). **The second input is
  > NOT in hand:** no `TAQOZ*.spin2` exists anywhere in the repo, so the *"verify vs Peter Jakacki's
  > `TAQOZ.spin2`"* half cannot run today. **What would settle it:** obtain Jakacki's `TAQOZ.spin2` source;
  > until then the ROM-monitor half is groundable from `ROM_Booter.lst` alone and the Forth-vocabulary half
  > is not. Stays `TRACKED → ingestion` — the preliminary web-research material
  > (`taqoz-web-research-preliminary.md`) remains community-tier and is still not citable.
  >
  > 🔴 **CORRECTED 2026-09-10 by F-421 — this plan names the WRONG listing.** *"mine
  > `ROM_Booter.lst`"* points at the **FPGA** build (`ver = "A"`, Prop123-A9/BeMicro-A9).
  > The chip's ROM is `rom_booter_v33_01j.lst` (`ver = "G"`, Prop2 Silicon v2) — same source
  > version v141, different build target. Mine THAT one; the FPGA listing carries FPGA clock
  > constants, a different SD call structure, and a reserved long that silicon uses for MBR
  > validation. Keep `ROM_Booter.lst` only as the labelled FPGA comparison point.

---

## ADC gain-mode input ranges framed ground-referenced, not centered on VIO/2 (2026-07-07) — F-202

### F-202 — IOSP §16.2 ADC input-mode table (and 5 propagated sites) frame the gain ranges as ground-referenced `0V–ceiling` — `PARTIAL — the KB and the IOSP ch16/appendix-c windows ship as measured; two stale phrases still say the windows are "being characterized on hardware" (IOSP ch16 :532, appendix-d :192) (re-verified 2026-10-05 «#386»)`
> **Source of report:** community reviewer (2026-07-07, relayed by Stephen): *"the ranges are totally
> wrong… they are centred around 1.65V."* Community-tier input (Titus-tier): challenges our work, is not
> itself a citable source.
> **TRUST-CHAIN DISCIPLINE (Stephen, 2026-07-07):** the **P2AN\*** app notes are derived from the SAME
> ingested sources as the manuals — a **peer derivation, NOT an authority**. Do not justify manual content
> against P2AN001/§16.3; ground only against trusted **ingested** sources (Silicon Doc) or **empirical**
> hardware (EF ledger). This finding was re-grounded on that basis.
> **What the Silicon Doc (trusted ingested) DOES ground:**
> - **GIO/VIO are calibration sources, not input-range modes** — *"Delta-sigma ADC with 5 ranges, 2
>   **sources**, and **VIO/GIO calibration**."* The §16.2 table mislabels them as ranges (`GIO = 0V–3.3V`,
>   `VIO = VIO-relative`). WRONG per a trusted source.
> - **The ADC has a ~mid-supply bias point** — Rev C note: FLOAT mode "useful for determining the
>   **floating bias point of the ADC**." So the gain window sits around mid-supply, **not up from 0 V** —
>   the table's ground-referenced framing is wrong.
> - Tell-tale of how it happened: the table's ceilings (`1.04V / 330mV / 104mV / 33mV`) equal `3.3V ÷ gain`
>   — correct range **widths** placed at `[0, width]` (generic unipolar-PGA assumption) instead of around
>   the mid-supply bias. (§16.7 L469 and §16.3 already describe the bias/references correctly — but those
>   are peer manual sections, cited here only as internal-inconsistency evidence, not as authority.)
> **RESOLUTION — nominal transfer characteristic (releasable-correct without hardware):**
> The exact endpoints are a **nominal / definitional** quantity, not a measured one: the mid-supply
> reference is grounded (Silicon Doc float-bias-point) and the gain factors are grounded (Silicon Doc
> "5 ranges" + image catalog), so the window `= 1.65 V ± (1.65 V / gain)` about mid-supply is **DERIVED**
> (like the Ohm's-law drive currents and `clkfreq/2³²` NCO resolution we already print), NOT AT_RISK —
> **provided it is labelled *nominal* and carries the calibration caveat** (exact endpoints vary with device
> tolerance + VIO; for absolute work calibrate against GIO/VIO, §16.3). This mirrors the manual's already-correct
> nominal-vs-measured handling of resolution ([[F-201]]). This is the distinction I initially over-collapsed:
> a *measured precision spec* needs silicon; the *nominal transfer characteristic* does not. So §16.2 prints the
> nominal windows (labelled) — correct, complete, hardware-independent.
> **Verification split (per VERIFICATION-OPPORTUNITIES.md):**
> - **VO-J-001 (jumper-only — we do it):** on-chip DAC → jumper → ADC pin sweep confirms the centering + √10
>   window scaling on silicon (upgrades nominal → silicon-confirmed). Task #172. NOT a release blocker.
> - **VO-X-001 (external-hardware — cataloged, not committed):** calibrated external reference + precision meter
>   for tolerance-bounded absolute endpoints. Benefit: nominal → datasheet-grade. Deferred.
> **Propagated sites (all same root), IOSP opus-master `part-3-input-modes/chapter-16-adc.md` unless noted:**
> §16.2 table (L39–46) · §16.2 prose (L50–60) · §16.2 example "0-100mV sensor → 30x" (L64–66) ·
> §16.7 Example 4 thermocouple "0-50mV → 100x" (L505–517) · §16.7 quick-ref table (L636–640) ·
> `part-5-appendices/appendix-d-mode-comparison-charts.md` (L195–198). The **examples are the worst**:
> they feed a ground-referenced small-signal sensor (0-100 mV, 0-50 mV thermocouple, mic, strain gauge)
> into a 1.65 V-centered gain mode with **no mid-rail bias network** — they would not work as written.
> **NOT affected (checked, don't over-correct):** §16.3 ratiometric (correct) · §16.7 float note L469
> (correct) · **DAC ranges ch10** `0–3.3V`/`0–2.0V` (correct — DAC is genuinely unipolar 0-to-Vfs,
> matches Silicon Doc drive-level table). Defect is **specific to ADC gain modes**.
> **Secondary check:** `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` L144–145 calls
> GIO/VIO "Ground-referenced input / VIO-referenced input" — loose (they're calibration references);
> tighten wording, and confirm no range claim depends on the ground-referenced framing.
> **SILICON-CONFIRMED 2026-07-07 (EF-024) — supersedes the nominal formula.** VO-J-001 ran on real P2:
> gain modes ARE centered on mid-supply (~1.64 V measured) [structural, definitive], but the **derived
> `1.65 ± 1.65/gain` (3.3 V/gain width) was WRONG** — measured widths are ~1.4× wider (≈4.55 V/gain), √10-laddered.
> Measured representative windows (N=1): 3.16× 0.93–2.36 V · 10× 1.41–1.87 V · 31.6× 1.57–1.71 V · 100× 1.61–1.66 V.
> **Fold into IOSP v1.0.4** (staged): (a) GIO/VIO reclassified [APPLIED]; (b) mid-supply framing + examples
> fixed [APPLIED]; (c) **print the MEASURED windows** (table above) across §16.2 + Appendix B + Appendix C,
> labelled *measured on real P2 silicon, representative single-sample* (per the citation convention), NOT the
> derived formula; rebuild the two examples on the measured centering [PENDING apply]. With (c), F-202 is
> **CLOSED for release** and now hardware-grounded (not merely derived). VO-X-001 (absolute tolerance across
> parts) remains the optional datasheet-grade upgrade.

> ### KB-SIDE SECONDARY CHECK DISCHARGED 2026-08-25 («#300») — and this entry's HEADLINE is stale
>
> 🔴 **Read the headline against this block.** The heading still says *"exact centered endpoints UNVERIFIED
> (no trusted numeric source) → **hardware campaign required**"*. **That campaign already ran.** The
> `SILICON-CONFIRMED 2026-07-07 (EF-024)` note immediately above is the result, and
> `VERIFICATION-OPPORTUNITIES.md:38` records **VO-J-001 → DONE → EF-024**. A top-down reader stops at the
> heading and concludes this is blocked on silicon we cannot reach; it is not. **This is exactly the failure
> mode REGISTER-CONSULTATION §1 exists for** — the status sits at the end, and here the end supersedes the
> front. The heading is left in place rather than rewritten because the entry is mid-flight on the manual
> side, but nothing downstream should quote it.
>
> **KB FIX APPLIED — the "Secondary check" line above, now discharged.**
> `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`:
> - `:143-151` — `adc_input_modes` no longer calls GIO/VIO input ranges. `P_ADC_GIO` / `P_ADC_VIO` now read
>   *"…calibration reference to the ADC (a calibration **SOURCE**, not an input range)"*, and `P_ADC_FLOAT`
>   states its actual purpose. Grounded in-file on **Silicon Doc `p2-documentation.txt:452`** — *"Delta-sigma
>   ADC with 5 ranges, 2 **sources**, and **VIO/GIO calibration**"* — with the mode-name glosses cited to
>   **`spin2-v55-text.txt:1466-1473`** (*"ADC GIO → IN"* / *"ADC VIO → IN"* / *"ADC FLOAT → IN"*), and
>   `P_ADC_FLOAT`'s bias-point role to **`p2-documentation.txt:188-190`** (Rev C: *"…but floats the ADC input.
>   This mode is now useful for determining the floating bias point of the ADC."*).
> - `:168-169` — **the range claim that depended on the ground-referenced framing is gone.** The old note
>   *"ADC input modes (GIO/VIO/gain) affect voltage range and sensitivity"* lumped the calibration sources in
>   with the gain ladder as if all of them set a range. It now separates them, and a second note carries the
>   structural EF-024 result: *"The gain-mode window is **CENTERED ON MID-SUPPLY (~VIO/2)**, not referenced up
>   from 0V … centered at ~1.64V for every gain (EF-024). A ground-referenced small-signal source needs a
>   mid-rail bias network before it can be read through a gain mode"* — which is the trap that made this
>   finding's worked examples unrunnable.
> - **Only the structural half of EF-024 was carried into the KB, deliberately.** EF-024 grades the centering
>   as *[structural, definitive]* but its window endpoints as a **representative single sample (N=1)**. The
>   centering is stated; **the N=1 endpoint numbers are NOT printed in the KB**, because a bare table there
>   would read as a specification. Printing them, labelled, is step (c) above — **manual-side, «#301»**.
> - Verified after the edit: `validate-crossref-keys.py` 3161 refs / 0 unresolved ·
>   `audit-yaml-claim-sourcing.py` 0 Tier-1, Tier-2 unchanged at 78 · `verify-yaml-format.py` clean.
>
> **THE GAP THAT ACTUALLY REMAINS — and it is NOT the centering.** It is **VO-X-001**, cataloged at
> `VERIFICATION-OPPORTUNITIES.md:51`: *tolerance-bounded **absolute** endpoints across parts and
> temperatures.* **What would settle it:** a calibrated, traceable external voltage reference plus a
> precision meter, exercised across several parts — **external hardware, which this container cannot reach**
> and which is `CATALOGED`, not committed. Its own entry says it is *"not needed for correctness."*
> **No endpoint number was supplied here, and none should be** — the measured N=1 windows in EF-024 are the
> only figures with evidence behind them, and they are labelled as such at their source.

---

## XBYTE technique-mining sweep — reference implementations expose two doc defects (2026-07-14) — F-217, F-218

> **Origin.** Stephen asked for a per-processor "what will hurt when you emulate this" table in the XBYTE
> Guide, and proposed we ground it by studying **live, working emulators** rather than reasoning from ISA
> facts. The study immediately surfaced two defects. Full evidence ledger:
> `engineering/document-production/manuals/p2-xbyte-programming-guide/TECHNIQUE-MINING.md`
> (per-source, because the techniques enter the manual body *anonymously* — the ledger is the only place
> the lineage lives). **Note the path:** it lives at the manual **root**, not in `audit/`, because
> `.gitignore:175` ignores `manuals/*/audit/` — a durable source-of-record cannot live there.

### F-218 — `SingleStep-Debugger-Theory-of-Operations.md` §6.4 mislabels `GETBRK` D[25] as "C,Z affected by XBYTE" — `CONFIRMED` — **VERIFIED against the Silicon Doc 2026-08-25 («#300»); the KB was already correct, so no KB work is owed**

**Our own ingested doc says:**

> *"Displayed as 3 hex digits. A checkmark glyph appears if **bit 25** of `mBRKC` is set (**C,Z affected by
> XBYTE**)."*

**The Silicon Doc says otherwise.** Per P2KB `p2kbPasm2Getbrk`, `GETBRK D WC` returns:

| Field | Meaning (Silicon Doc) |
|---|---|
| D[27] | 1 = SKIP · 0 = SKIPF/EXECF/XBYTE |
| D[26] | LUT sharing enabled |
| **D[25]** | **XBYTE pending on next `_RET_`/`RET`** |
| D[24:16] | the 9-bit XBYTE mode |

"C,Z affected by XBYTE" is the **F bit**, which is the *low bit of the mode operand* — i.e. **D[16]**, not
D[25]. The two are different facts about different bits, and our doc appears to have conflated them.

- **NOT SETTLED, and deliberately not fixed.** The checkmark's meaning is decided by the **host-side**
  display code (PNut / term-ts), not by Chip's P2-side debug stub — `Spin2_debugger.spin2` only calls
  `getbrk` and ships the word to the host. So the P2-side source **cannot** adjudicate this. Settling it
  needs the host display source or Chip.
- **Two possible truths:** (i) our gloss is simply wrong and D[25] means "XBYTE pending"; or (ii) the
  debugger's checkmark genuinely reflects the F bit and our doc attributed it to the wrong bit index. Either
  way **the doc as written is wrong**; only the repair differs.
- **Consumer risk:** the XBYTE Guide is about to gain a "Debugging XBYTE" section citing `GETBRK` fields.
  It will cite **the Silicon Doc layout**, not this doc, until this is resolved.
- **Wider lesson (already a standing rule, freshly demonstrated):** our own ingested derivations are **peer
  tier, not authority**. This was caught only because the field layout was cross-checked against P2KB
  instead of being trusted.

> ### ✅ VERIFICATION PERFORMED 2026-08-25 («#300») — this entry's `NEEDS-VERIFICATION` is discharged
>
> The original entry rested on **P2KB** (`p2kbPasm2Getbrk`), which is circular inside this project — the KB
> is what we publish. So it was re-grounded on the **Silicon Doc primary extraction**, and both halves of
> the claim were checked independently. **What could have come back the other way:** had the Silicon Doc's
> own `D[25]` line read *"C,Z affected by XBYTE"*, the finding would have become `RESOLVED-INVALID` and the
> doc would have been right. It does not.
>
> **Half 1 — what D[25] actually is.** `engineering/ingestion/sources/silicon-doc/part3-interrupts.txt:445-446`,
> verbatim, under `GETBRK D WC`:
>
> > `D[25] = 1 if top of stack = $001FF, indicating XBYTE will execute on next _RET_/RET`
> > `D[24:16] = 9-bit XBYTE mode, established by '_RET_ SETQ/SETQ2' when top of stack = $001FF`
>
> **Half 2 — where "C,Z affected by XBYTE" really lives.** It is the `%F` bit, and `%F` is the **LSB of the
> 9-bit mode**, so it lands at **D[16]**. `silicon-doc/p2-documentation.txt:2196-2202`, verbatim:
>
> > *"The %F bit of the SETQ/SETQ2 {#}D value enables C and Z to receive bits 1 and 0 of the index field of
> > the bytecode."* — with the table `%xxxxxxxx0` = *"Do not affect flags on XBYTE"* · `%xxxxxxxx1` =
> > *"Write the bytecode's index LSBs to C and Z"*.
>
> **VERDICT: `CONFIRMED`.** D[25] and D[16] are different bits with different meanings, and §6.4 fuses them.
> The entry's premise holds on the primary source, not merely on P2KB.
>
> **A SECOND SITE, same root cause, found by sweeping the doc (class-wide rule).** The same file's field-map
> row contradicts its own body: `SingleStep-Debugger-Theory-of-Operations.md:1298` states
> *"XBYTE (bits 25..16)"* — a **ten**-bit field that swallows D[25] into the mode — while `:763` computes the
> field as `DebuggerMsg[mBRKC] >> 16 AND $1FF`, i.e. **D[24:16]**, which is correct. `:765` is the §6.4
> sentence this finding names. So the defect is **two sites plus a self-contradiction**, not one sentence.
>
> **🟢 NO KB WORK IS OWED — verified on disk, not assumed.**
> `deliverables/ai/P2/language/pasm2/getbrk.yaml:33` already reads
> *"…D[26] = LUT sharing enabled, **D[25] = XBYTE pending on next `_RET_`/`RET`**, D[24:16]…"* — correct, and
> matching the Silicon Doc. No published manual carries the wrong gloss either (swept: zero hits for
> `C,Z affected` across `manuals/*/opus-master/`). **The defect never reached anything we ship**, which is
> why this closes without a KB edit rather than being left open for one.
>
> **RESIDUAL GAP — narrowed, not closed, and it is not ours.** Which of the two repairs §6.4 needs still
> depends on the **host display source**: if PNut/term-ts really tests bit 25, the *caption* is wrong; if it
> tests bit 16, the *bit index* is wrong. **What would settle it:** the host-side display routine that draws
> the XBYTE checkmark (PNut Pascal or the term-ts mirror), which this repo does not hold — `REF/` under
> `p2-single-step-debugger-manual` carries only the user manual, a screenshot and an audit, no Pascal.
> **This is an upstream document defect with no consumer here**, so it is routed, not worked: the bit
> semantics above are now settled and citable regardless of which repair is chosen.
>
> **Not relocated to `SOURCE-ERRATA.md`, deliberately.** That register's own test is *"if **Parallax** fixed
> their document tomorrow, would this entry disappear?"* — and all nine of its entries are Parallax
> documents. This document is the **pnut-ts side's** (`external-inputs/pnut_ts_facts/`, not a registered
> ingested source), so it fails that test. It is also not a `PNUT-TS-PUNCH-LIST.md` item — that list is
> compiler-behaviour items carrying a runnable repro, not documentation defects. Flagged here as the record.

## Render-verification wave — defects found by READING the generated PDFs (2026-08-17/19) — F-284…F-294, F-299…F-301

**Origin.** Verifying the six generated wave PDFs page by page rather than reading their compile
logs. Every finding below was invisible to a clean log: LaTeX ate an operator, a filter split a
line, a glyph printed nothing, a gate skipped the blocks it was built to check. F-295…F-298 closed
at the XBYTE sprint closeout and are archived.

> **These sat under the wrong header until 2026-08-21.** The 2026-08-19 sweep archived
> F-259…F-263 but left their `## Community bench review — refaQtor` header in place, so all
> fourteen read as part of a third party's bench review. That header is now in the archive with
> the findings it introduced. Detected by `audit-register-hygiene.py` check 9.

### F-301 — the cross-ref filter's adopt-at-next-release rule was passed over about a dozen times, because nothing read the tracker. `PARTIAL` (re-verified 2026-10-05 «#386»: the structural fix landed; only P2AN003, P2AN005 and P2AN006 still lack the cross-ref filter) — **detected 2026-08-19 by comparing the tracker against every `request.json`**

**The rule, written into `CROSSREF-FILTER-ADOPTION.md` when the filter shipped 2026-06-26:**
*"The next time each manual is released (for any reason), its release MUST add
`p2kb-platform-crossref` to that manual's `request.json` `lua_filters` and visually audit the
rendered PDF."* The tracker even names its own consumer — *"`release-manual` Phase 1/Phase 4
**should** consult this tracker."*

**Measured, not assumed.** Every workspace `request.json` read directly against the tracker's rows:

| Document | Tracker | In `request.json`? | Releases since the rule |
|---|---|---|---|
| Assembly | ⏳ pending, at v3.1.0 | **no** | v3.1.1 → v3.1.6 |
| DeSilva | ⏳ pending, at v3.0.1 | **no** | v3.0.2 → v3.0.6 |
| Debug Window | ⏳ pending, at v1.0.1 | **no** | v1.0.2 → v1.1.3 |
| Getting Started | ⏳ pending, at v1.0.0 | **no** | v1.0.1 → v1.0.3 |
| Architect | ⏳ "in development" | **no** | released v1.0.3 |
| XBYTE | **absent from the table** | **no** | v1.0.0, v1.1.0 |
| 7 app notes | **absent from the table** | **no** | 20+ |
| IOSP | 🔧 adopting (pilot) | yes, ordering correct | audit never recorded |
| Streamer | ✅ adopted + audited | yes, ordering correct | — |

**Only two of fifteen ever adopted.** IOSP's row still reads "awaiting Stephen's regen + visual
audit" although it has released three times since, so its filter has certainly rendered — the
**audit** is what is unrecorded, and that half is the half that matters (a mis-fired auto-link is
exactly what the audit exists to catch).

**The statuses are not wrong. Nothing read them.** Every row above is an accurate record of a
decision that was then never consulted at the moment a release happened. This is the same failure
as [[F-281]]'s «#250» in a different costume — a correct record that is not where the decision gets
made — and it is why adoption state moved into `PLATFORM-FEATURE-ADOPTION.md`, which
`prepare-manual` consults on every prepare rather than "should" consult on release.

**FIX — structural, landed 2026-08-19:** one per-document × per-feature matrix
(`PLATFORM-FEATURE-ADOPTION.md`), seeded from **detected** state rather than from what each tracker
claimed, plus a `prepare-manual` check that surfaces a document's outstanding ⏳ features as work
owed **this** release. `CROSSREF-FILTER-ADOPTION.md` keeps the mechanism (including the mandatory
crossref-before-tables ordering) and its status table is frozen as history.

**Still owed per document:** the adopt + visual audit itself, at each document's next release —
that has not been shortcut, only made visible. **ssdb and pnut-term-ts release next and both sit at
⏳**, so they are the first two chances to stop the count growing.

> **RE-MEASURED 2026-08-25 («#302») — read out of every workspace `request.json`, not off the
> tracker, and the two agree row for row.** `p2kb-platform-crossref` present in the `lua_filters`
> list:
>
> | | Documents |
> |---|---|
> | **ADOPTED (4)** | Assembly Reference · I/O & Smart Pins · Streamer Guide · **PNut-Term-TS User Guide** |
> | **⏳ still owed (11 P2 documents)** | Architect's Guide · Debug Window · Getting Started · DeSilva · XBYTE · Single-Step Debugger · P2AN001…P2AN007 |
> | out of scope | `ai-privacy-guide`, `Donna-Manuscript` (private, non-P2), `p2-layout-torture-test` (instrument) |
>
> **The count stopped growing, which is the first evidence the structural fix works.**
> `pnut-term-ts-user-guide` was one of the two "first chances" this entry named, and it **took**
> the feature — adopted **and audited 27 of 27 on the returned PDF** (2026-08-23), the audit half
> that IOSP's pilot row never recorded. The other named chance, **Single-Step Debugger, is still
> ⏳** and is the next test of it.
>
> **This stays `CONFIRMED` because the per-document work is genuinely outstanding, not because
> anything is unknown.** Two things ride every future adoption and must not be dropped:
> **`p2kb-platform-crossref` MUST sit between `figures` and `tables`** (`tables` flattens each cell
> to a string and would leave table-borne refs dead — verified ordering in all four adopted
> `request.json`s), and **the visual audit on the returned PDF is the half that matters**, because
> a mis-fired auto-link is exactly what it exists to catch.

### F-300 — every published PDF in the set ships with empty Title and Author properties. `PARTIAL` — **MECHANISM LANDED + PROVEN 2026-08-19; 10 of the 17 published PDFs have adopted, 7 owed at their next render (re-measured 2026-09-21, «#344»)**

> **RE-MEASURED ON THE RELEASED ARTIFACTS 2026-09-21** («#344») — `pdfinfo` over every PDF in
> `deliverables/documents/DOCs/`, read from the shipped files themselves, not from a render log and
> not from this register. **10 of 17 now carry both Title and Author** (all `Iron Sheep Productions,
> LLC`), against 2 of 15 at the 2026-08-25 measurement. The set grew by two documents in the
> interval, so the denominator moved as well as the numerator.
>
> **Still empty, and each resolves at that document's next render — this is the expected shape of
> this finding, not debt:** `P2AN003` · `P2AN005` · `P2AN006` · `P2AN007` ·
> `P2-Architect-Guide` · `P2-Debug-Window-Manual` · `P2-XBYTE-Programming-Guide`.
>
> Status stays open deliberately: it is manual-head and per-document, so it cannot close until the
> last of those seven re-renders. It is `PARTIAL` rather than `PENDING-VALIDATION` because the
> mechanism is proven and adopting is now routine — what remains is render scheduling, not
> validation.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302») — `pdfinfo` over every file in
> `deliverables/documents/DOCs/`, not read off the tracker.**
>
> | State | Count | Which |
> |---|---|---|
> | **Title + Author + Subject + Keywords populated** | **2** | Assembly Reference (`P2 Assembly Language Reference Manual` / `Iron Sheep Productions, LLC`), Streamer Guide (`P2 Streamer Programming Guide` / same) |
> | **all four fields still EMPTY** | **13** | Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide · XBYTE · P2AN001…P2AN007 |
>
> The mechanism is also proven on two documents that are **not yet published to `DOCs/`**
> (Single-Step Debugger, PNut-Term-TS User Guide), so four conversions exist in total.
>
> **This stays `PENDING-VALIDATION`, and it closes per document, on a render — never on an edit
> here.** Each of the 13 adopts by rendering on `EXEC_ENV_CANONICAL`; there is no container-side
> action that can advance it. Per-document state is `PLATFORM-FEATURE-ADOPTION.md`, which
> `prepare-manual` consults, and the measurement above agrees with it row for row.
>
> ⚠️ **`pdfsubject` IS being populated**, contrary to this entry's step 4 (*"Do NOT wire
> `pdfsubject`"*): both adopted PDFs carry a `Subject`. That does not misreport either of them —
> neither appears in **F-317**'s drift table — but it means F-317 is **live at every adoption**, not
> deferred, and each of the 13 must have its `request.json` subtitle reconciled to its printed cover
> **before** it renders.

> **RESOLUTION (2026-08-19).** The fix is **not** the one-line `pdfusetitle` this entry proposed —
> that would have populated the info dictionary and left the cover as a second hand-maintained copy
> of the same five strings, and would have shipped *wrong* titles on 9 of 15 (see the template table
> below). What landed instead: **every identity string lives once, in the document's `request.json`
> metadata, and reaches both the PDF info dictionary and the cover page from there**, via
> `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` defined in
> `p2kb-platform-foundation.sty` (§ DOCUMENT METADATA). The macros carry the *value*; the cover keeps
> its *presentation*.
>
> **Proven on the interactive daemon, four round-trips, by reading the rendered PDF** — not the
> success flag. Both first converts (Single-Step Debugger, PNut-Term-TS User Guide) came back with
> compile logs clean on every serious signature and Title/Author/Subject populated for the first
> time, covers rendered and looked at. Commit `09958b0a`.
>
> **Unconverted documents are safe:** the foundation `\providecommand`s all five macros empty, so a
> template that has not opted in writes exactly what it wrote before. **Per-document adoption state
> is `PLATFORM-FEATURE-ADOPTION.md`**, and `prepare-manual` now reads it. The analysis below stands
> as the record of how the fix was found; only the proposed one-liner is superseded.

**Surfaced by** the Streamer v1.0.9 release verification — reading the delivered PDF's metadata
dictionary, then checking whether it was a Streamer regression. It is not: **all 15 PDFs in
`deliverables/documents/DOCs/` report `(empty)` for both `title` and `author`** — eight manuals and
seven app notes. Only `creator` (`LaTeX with hyperref`) and `producer` (`xdvipdfmx`) are set.

**What a reader sees.** A PDF viewer's title bar and Document Properties fall back to the *filename*
instead of the document's name, and anything indexing the file — a search tool, a library, a
citation manager — finds no title or author to key on.

**The mechanism, traced end to end.** The `.latex` template sets `\title{P2 Streamer Programming
Guide}` (generated `.tex` line 31), and `p2kb-platform-foundation.sty:259` sets a `\hypersetup`
block — but that block configures **only** link colors and bookmarks. It never sets `pdftitle` or
`pdfauthor`, and **hyperref does not derive them from `\title{}` on its own**; that requires either
`pdfusetitle` or explicit keys. So the title exists in the document body and never reaches the PDF
info dictionary.

**FIX (one line, in the shared platform):** add `pdfusetitle` — or explicit
`pdftitle={...}, pdfauthor={...}` — to the `\hypersetup` block at
`p2kb-platform-foundation.sty:259`. **Zero layout risk**: it writes the PDF info dictionary only and
cannot reflow a page. This is what distinguishes it from [[F-299]], which is parked because it
*does* move type.

**Corrects a claim in our own process doc.** The `prepare-manual` skill states that a `request.json`
metadata change "feeds PDF properties, not just the build." For this manual-production path that is
**not true** — the template hardcodes `\title{}`, and nothing carries `request.json`'s
`metadata.{title,author,version}` into the PDF info dictionary. Re-staging `request.json` on a
document switch is still mandatory for a different and real reason (input/template/filters), so the
rule stands; only its stated justification about PDF properties is wrong. Fix that sentence when the
platform fix lands.

**Sequencing.** No manual should re-render just for this. Let it ride with the next render each
document takes anyway, and take it in the same set-wide sweep as [[F-299]] — one `forge-test` pass,
two set-wide render changes.

> **Stale reference removed 2026-08-19.** This sentence named the fancyvrb `breaklines` work «#250»
> as a third member of the sweep. That work was **REJECTED 2026-08-17** on the round-trip evidence
> (see [[F-281]]); the reference was written after the rejection and never checked against it. The
> sweep is F-300 + F-299, and F-299 is polish. There is no breaklines work to schedule.

⚠️ **TRAP FOR WHOEVER TAKES THIS FIX — the two title sources already disagree.** Because nothing
consumes `request.json`'s metadata today, nobody has had to keep it in step with the cover, and it
has drifted. On the Streamer: the **cover** reads *"Comprehensive Reference for Propeller 2 Streamer
Hardware"* while `request.json` reads *"Comprehensive Reference for the Propeller 2 Streamer"*. The
moment `pdftitle`/`pdfsubject` start being populated, whichever source the fix wires up becomes
reader-visible, and a stale one ships silently. **Before adopting: audit cover-vs-`request.json`
across all 15 documents and reconcile, then decide which source is authoritative** (the cover is
what a reader actually sees, so it should win). Do not wire the metadata through without that pass.

**THAT AUDIT IS NOW MEASURED (2026-08-19), and the drift is systemic, not a Streamer typo.** Comparing
each master's cover block (`\fontsize{36}…\bfseries` title + `{\Large\itshape …}` subtitle) against
its `request.json` `metadata.subtitle`, over the 15 published documents:

| Verdict | Count | Which |
|---|---|---|
| **SAME** | 3 | Architect, Assembly, Getting Started |
| **DRIFT** | 8 | Debug Window, Streamer, P2AN001, P2AN002, P2AN003, P2AN004, P2AN005, P2AN007 |
| **cover block not matched by this scan** | 4 | IOSP, deSilva, XBYTE, P2AN006 — a different cover shape, **unresolved, not clean** |

**Two of the drifts are kinds of drift, not typos, and they change what the fix has to decide:**
1. **The app notes disagree structurally.** `request.json` carries a *catalog label* — "Application
   Note P2AN001 — No External ADC" — while the cover carries a *reader subtitle*: "No external ADC —
   a single-pin instrumentation ADC…". Neither is a stale copy of the other. Wiring the cover through
   verbatim drops the P2AN00N designator from the PDF's Title; wiring `request.json` through gives
   every app note a title that is not what its cover says. **Decide this before touching the
   platform** — likely `pdftitle` = title + designator, `pdfsubject` = the reader subtitle.
2. **Cover strings contain LaTeX.** PNut-Term-TS's cover subtitle carries a literal `\\` line break.
   PDF info-dictionary fields are plain text, so any such markup must be stripped, not passed through
   — one more reason `pdfusetitle` (which takes `\title{}` as-is) is not automatically the right
   mechanism for the subtitle half.

Truncation was not checked: two of these subtitles run past 50 characters and the register scan
compared full strings, so the counts above are exact for equality but say nothing about length limits.

---

**⚠️ THE SUBTITLE DRIFT IS NOT THE GATE. The gate is the templates, and nobody had looked at them
(traced 2026-08-19).** `pdfusetitle` populates `pdftitle` from `\title{}` and `pdfauthor` from
`\author{}` — it never touches the subtitle. So the drift table above gates only a `pdfsubject` we do
not have to wire. What actually decides whether this fix can be turned on and left to ride is what
each template declares, and **9 of the 15 declare something wrong:**

| Template `\title{}` | Documents | Verdict |
|---|---|---|
| `P2 Application Note` (hardcoded, SHARED) | **all 7 app notes** | **BROKEN** — `pdfusetitle` gives seven distinct documents one identical title. Worse than empty in a library or index. |
| `P2 XBYTE Programming Guide` | XBYTE | **STALE** — the released v1.1.0 cover reads *"P2 Interpreters & Emulators Guide"*. The template kept the pre-retitle name. |
| *(no `\title` and no `\author` at all)* | deSilva | **EMPTY** — would stay broken after the fix. |
| correct, matches cover | Architect, Assembly, Debug Window, Getting Started, IOSP, Streamer | ready |

`\author{Iron Sheep Productions, LLC}` is correct in every live template **except deSilva's**, which
has none.

**The one fact that makes all of this safe: `\title{}` is never rendered.** Every cover in the set is
hand-built in the master's `front-matter.md` (`\fontsize{36}{42}\selectfont\bfseries …`). There is no
`\maketitle` anywhere in the published set — the only one in the tree is in `ai-privacy-guide`, which
is not a published document. **So `\title{}` is metadata-only, and changing it cannot move a single
point of type on any page.** That is what turns this from a render-risk change into a ride-along.

**REVISED PLAN — prep in one commit, no renders, then ride:**
1. **Switch every live template from a hardcoded `\title{…}` to `\title{$title$}` / `\author{$author$}`.**
   `request.json` becomes the single source and a template can never go stale against its document
   again — this is what fixes the seven app notes and XBYTE at once, and it is durable rather than a
   catalog of literals to maintain. Verified safe: **`request.json` `metadata.title` equals the cover
   title for 14 of 15**, including all seven app notes (the cover carries the designator on its own
   eyebrow line — *"Propeller 2 • Application Note P2AN006"* — above the title, so nothing is lost).
2. **deSilva is the one real conflict, and it is BOTH fields.** Released cover: *"P2 Assembly
   Programming"* / *"A Human-Centered Approach to Parallel Processing"*. `request.json`:
   *"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"*. The cover wins →
   update `request.json`, then give `p2kb-desilva.latex` the same `$title$`/`$author$` pair.
3. **Add `pdfusetitle`** to the `\hypersetup` at `p2kb-platform-foundation.sty:259`.
4. **Do NOT wire `pdfsubject`.** Leaving it out defers the whole subtitle question above at zero cost;
   revisit it as its own item whenever someone wants Subject populated.
5. **Add a `PLATFORM` ledger line and let each document absorb it at its next natural render.**
   Precedent for the standing: the 2026-07-13 mnemonic-bold line — *live-but-benign, not outstanding
   debt*. No manual re-renders for this.

**One `forge-test` still confirms three things before adoption**, none of them layout: that `$title$`
substitution actually reaches `\title{}` on this path, that `&` survives into the info dictionary
(IOSP *"P2 I/O & Smart Pins User Guide"*, P2AN006 *"Sizing Cog & Task Stacks"*), and that `pdfauthor`
lands. Read the output PDF's metadata dictionary, not the compile log.

### F-299 — wide `tblr` tables overhang the right text edge by ~5–6pt, in the platform, not the manual. `CONFIRMED` — **POLISH, NOT A GATE FAILURE: it is inside the project's own 20pt tolerance (re-graded 2026-08-19, same day, see the correction at the end)**

**Surfaced by** the Streamer v1.0.9 daemon pre-verify — a whole-document margin measurement of the
rendered PDF (every text span's `x1` against the 540pt text edge), not by the compile log, which was
clean on every serious signature in both the v1 and v2 renders.

**The defect.** Two of the Streamer's wide mode-reference tables push their rightmost column past
the text block: §6.2 *RDFAST → Pins/DACs* by **6.1pt** (`DAC Bits` header) and §8.x *Pins/DACs →
Hub* by **5.3pt** (`Hub Write` header). Visible as the table's horizontal rules extending past the
running-header rule directly above them. The compile log reports these as `Overfull \hbox
(26.6406pt too wide)` — the larger number is the whole `tblr` box including padding; the visible
overhang is the 5–6pt the measurement above reports.

**Why it is the platform's, not the manual's.** The column widths are computed by
`p2kb-platform-tables.lua`, which every manual in the set loads. Nothing in the Streamer's markdown
sets a width. A manual-side "fix" would mean hand-tuning a table the filter is supposed to own.

**NOT the two tables an earlier note predicted.** The Streamer release note expected the
`p2kb-platform-tables.lua` column fix to absorb "2 over-wide `Constant | Value | Description`
tables". These two are **6-column** `Mode | Symbol | Type | Pins | DAC Channels | DAC Bits` tables —
a different shape the fix does not reach. The prediction was not wrong about its own targets; it
was applied to the wrong pair. **A status note naming a fix is not evidence the fix covers what you
are looking at** — measure the artifact ([[feedback_status_line_is_not_evidence]]).

**Deliberately not fixed in this release.** A column-width change in
`p2kb-platform-tables.lua` reflows tables in **every** manual, so adopting it while Streamer is
mid-render means re-verifying the whole set against a changed table model for 6pt of rule overhang.
Schedule it when no manual is mid-render, and expect the absorbing manual's next render to shift
table layout. **Pair it with [[F-300]]** — both are set-wide render changes whose failure mode is a
page that looks fine in the log, and both want one `forge-test` sweep across the set rather than two.

> **Stale reference removed 2026-08-19.** This paragraph cited the fancyvrb `breaklines` work «#250»
> as the precedent it followed and the partner to pair with. That work was **REJECTED 2026-08-17**
> ([[F-281]]) — before this entry was written. The scheduling rule it borrowed is sound and stands on
> its own; the partner is F-300.

**Scope when taken:** measure every manual, not just the Streamer — the filter is shared, so any
manual with a 6-column table is a candidate.

---

⚠️ **CORRECTION, same day, before this entry could mislead anyone — I RE-GRADED MY OWN FINDING.**

I measured this with a hand-rolled PyMuPDF scan at a **4pt** threshold. **The project already has a
sanctioned instrument for exactly this** — `engineering/tools/validation/audit-pdf-margin-overflow.py`
— and I did not use it. Run against the shipped v1.0.9 PDF it reports:

```
text-block right edge: prose 540.0pt, code 540.0pt   (tolerance 20pt)
CLEAN  nothing crosses the margin (76 pages measured)
```

**The gate's tolerance is 20pt by design. These tables are 6.1pt and 5.3pt — comfortably inside it.**
So both statements are true and the second is the one that sets priority: the overhang is real and
visible if you look for it (the table rule extends a hair past the running-header rule), and it is
**not** something the project's own margin gate would ever block on.

There is direct precedent for accepting far more: the IOSP v1.0.9 PUBLISH line accepts a chart
bleeding **~24pt** past the text block on evidence — zero overlapping spans measured, every cell
readable — with the explicit note that *magnitude is never the verdict*. A 6pt rule overhang with no
overlap is a smaller version of the same accepted case.

**Re-grade: this is POLISH, not a defect owed.** Still worth taking in the set-wide sweep with
[[F-300]] because the fix is cheap once the platform is open anyway — but it must not be
described as a defect blocking anything, and no manual should re-render for it.

**The transferable lesson — the one worth more than the finding.** Reach for the project's own
instrument before hand-rolling a measurement. Mine was not wrong, but it carried **no calibrated
threshold**, so it reported a number without the judgement that makes the number mean something, and
I very nearly filed a tolerance-conformant table as a defect owed. A raw measurement is not a
verdict; the tolerance IS the verdict ([[feedback_validation_tool_verdict_is_a_claim]] — the inverse
case, where the tool PASSES and the hand-rolled scan is the one overstating).

> ### DISPOSITION CONFIRMED 2026-08-25 («#300») — the re-grade stands; nothing re-measured, nothing re-argued
>
> Carried on «#300»'s roster and **closed here as POLISH, per the same-day correction above.** The 6.1pt and
> 5.3pt overhangs sit inside this project's **20pt** margin tolerance, so
> `audit-pdf-margin-overflow.py` — the sanctioned instrument — reports the shipped v1.0.9 PDF **CLEAN across
> all 76 pages**. **The tolerance IS the verdict.**
>
> **Deliberately NOT re-measured.** A disposition already made on evidence does not get re-litigated by a
> later agent hoping for a different number; re-running the hand-rolled 4pt scan would only reproduce the
> mistake the correction above documents. **No PDF was re-graded and no manual re-rendered for this.**
>
> **Not a gap and not a defect owed** — it is scheduled work with no blocker: take it in the set-wide
> `p2kb-platform-tables.lua` sweep, paired with **F-300**, when no manual is mid-render. Nothing in this
> sprint is waiting on it, and **no document may cite it as blocking**.
