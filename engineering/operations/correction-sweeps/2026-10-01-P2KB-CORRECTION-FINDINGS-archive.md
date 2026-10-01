# P2KB Correction Findings — ARCHIVE, swept 2026-10-01

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 24 findings carrying a `DONE` status token: F-449, F-450, F-451, F-452, F-462,
> F-463, F-464, F-465, F-466, F-467, F-468, F-469, F-470, F-471, F-472, F-473, F-474, F-475,
> F-476, F-477, F-478, F-480, F-481, F-482 — the KB v1.22.0 pass (the P2 Errata silicon
> findings and the divide-by-zero measurement) and the v1.21.x findings whose statuses had
> been flipped and left live.
>
> Swept by rename-then-trim (Stephen, 2026-10-01: "yes, will full audit to ensure only the
> expected changes are made"): the register was `git mv`'d here and copied back, then this
> copy was cut to the 24 findings' sections by a delete-only script, and the live copy had the
> same sections removed. Every entry below is the pre-sweep text (commit 15d69136), verbatim,
> in its original order; the lines `audit-register-hygiene.py --sweep-check 15d69136` proves
> are all accounted for. `RESOLVED` entries were not part of this sweep.

## The QDIV and QFRAC examples did not assemble, or overflowed (2026-10-01, found building the divide-by-zero test) — F-481, F-482

### F-481 — `qfrac.yaml`'s first three examples overflow the 32-bit quotient or do not assemble, and its description promises an integer.fraction result — `DONE` 2026-10-01
**Where:** `language/pasm2/qfrac.yaml` examples 1-3 and `long_description`. QFRAC divides {D:Q} by S
(Silicon Doc DIVIDE :3333-3340); the quotient is 32 bits, so it fits only while D < S. `{5:0.75}/2`
and `{1000:0}/3` overflow; the 16.16 example's arithmetic does not give 100.5/3.25 (its 0.5 sits in
the low long, worth 2^-32 units, not 2^-16); `#$C0000000` and `#$34000` exceed the 9-bit immediate
without `##`. **Applied:** replaced by `QFRAC #1,#3` → $5555_5555 r 1 and `SETQ ##$8000_0000` /
`QFRAC #1,#4` → $6000_0000 r 0 (compiled clean, pnut-ts 1.55.8; values from the documented operation);
the description now says QFRAC yields a fraction of 2^32 and points to QDIV for quotients ≥ 1. The
percentage example (QMUL then QFRAC of the product) was correct and stays. Confirmed on silicon
(EF-089 controls): QFRAC 1/3 = `$5555_5555` r 1 exactly; the SETQ example's operation was exercised
by `SETQ $8000_0000`/QFRAC 1/7 = `$36DB_6DB6` r 6 and 2/7-with-SETQ controls.

### F-482 — `qdiv.yaml`'s first two examples use immediates that need `##`, and its 64-bit example's quotient overflows — `DONE` 2026-10-01
**Where:** `language/pasm2/qdiv.yaml` examples 1-2: `QDIV #1000000,#3` and `SETQ #$12345678` /
`QDIV #$9ABCDEF0,#1000` — immediates above 511 do not assemble without `##`, and
$123456789ABCDEF0 / 1000 does not fit a 32-bit quotient. **Applied:** `MOV x,##1_000_000` /
`QDIV x,#3` → 333333 r 1, and `SETQ #2` / `QDIV #0,#3` → $AAAA_AAAA r 2, with the rule that the
SETQ value must stay below the divisor (compiled clean). The remainder-check and scaling examples
were correct and stay. Confirmed on silicon (EF-089 controls): 1000/3 = 333 r 1 and 64-bit SETQ
divides exact.

## What a CORDIC divide by zero returns is stated nowhere (2026-10-01, found researching F-470) — F-480

### F-480 — `qdiv.yaml` says "Division by zero produces undefined results" with no source, and MULDIV64 (which divides via QDIV) inherits the gap — `DONE` 2026-10-01 (settled on the bench, EF-089)
> **Applied 2026-10-01 («#372»), Stephen: "why don't we settle the divide issues with a bench test
> before we wrap this?"** VO-J-026 measured it: quotient = NOT (upper long of the numerator),
> remainder = lower long, deterministic, normal timing, no stall, next op unaffected (100 of 100
> cases). `qdiv.yaml` and `qfrac.yaml` now carry a `divide_by_zero` statement in place of
> "undefined"; `muldiv64.yaml` states MULDIV64(a,b,0) = NOT (upper long of a×b) — so the removed
> "returns 0" was wrong, not merely unsourced (it returns `$FFFF_FFFF` whenever a×b < 2^32); the
> Spin2 `/`, `//`, `+/`, `+//`, `FRAC` operator entries carry their measured results, and their
> one-line "Divide/float/modulo/unsigned" stubs were replaced by the v55 operator-table wording.

**Where:** `language/pasm2/qdiv.yaml`:122. **Searched:** Silicon Doc DIVIDE section (:3328-3346),
PASM2 manual QDIV/QFRAC rows (:11655, :11667), Spin2 v51/v55, the interpreter source, the bench
ledger — no statement of the zero-divisor quotient or remainder. "Undefined" may be right, or the
silicon may return a fixed value (it is deterministic hardware).
**To settle:** a short jumper-free bench test — QDIV and QFRAC by 0 with several numerators,
and Spin2 `MULDIV64(m1, m2, 0)` and `/` by 0 — then state the measured result, or keep
"undefined" with that measurement behind it. Until then: no claim about the value in either YAML.

## A no-wait `RDFAST` releases the next `RDLONG`/`WRLONG`, and their entries do not say so (2026-10-01, EF-084) — F-478

### F-478 — the hub read/write entries give no caution for a no-wait `RDFAST` before them: within 16 clocks a read returns the previous hub read's data with that data's flags, and a write can be lost — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** all six entries now carry `silicon_errata.after_no_wait_rdfast`
> (rdlong/wrlong beside their SETQ note): the specific symptom per instruction (stale value with
> that value's C/Z and `PTRA++` stepping for reads; lost write when a read follows at once for
> writes; the SETQ block outcome on `rdlong`), the rule (waiting form, or ≥ 16 clocks, e.g.
> `WAITX #12`) and EF-084/086/087/088, pointing to `rdfast.yaml` for the full account. **Widened:**
> none of the six had a `related:` block; each now links its width siblings and `rdfast.yaml`
> (findability).

**Where:** `language/pasm2/rdlong.yaml`, `rdword.yaml`, `rdbyte.yaml`, `wrlong.yaml`, `wrword.yaml`,
`wrbyte.yaml` — none mentions the FIFO.
**What silicon does (EF-084, Rev C, 200 MHz, run once, every repetition identical):** after a no-wait
`RDFAST`, the next `RDLONG` returned the previous hub read's long in 43 of 64 hub alignments (flags:
EF-086, below); a `WRLONG` was released before it landed and lost
when an immediate `RDLONG` followed (43 of 64), and landed when nothing followed. From 16 clocks
(7 non-hub instructions) after the `RDFAST` every read was correct, and with the waiting form every
read and write (EF-084's write runs were at the next instruction only); **writes of every width at
16 clocks (`WAITX #12` after the no-wait `RDFAST`) correct in 1,024/1,024 with an immediate
read-back: EF-088**. This is P2 Errata **E7** (the planned E8, merged 2026-10-01); F-472 carries the `rdfast.yaml` side.
**Correction:** add to each entry a caution naming the hazard, the rule (no hub-memory instruction
within 16 clocks of a no-wait `RDFAST`, or use the waiting form) and the E7 reference, citing
EF-084. **Extended by EF-086 (2026-10-01):** `RDBYTE`/`RDWORD`/`WRBYTE`/`WRWORD` are released in the
same cells; a released `RDBYTE`/`RDWORD` returns the previous read's long seen through its own
size and offset; a released read writes C and Z from the value it returns (`WC`/`WZ` do not
reveal the failure); `RDLONG … PTRA++` still steps the pointer; a `SETQ` block `RDLONG` either
wrote one wrong long and overwrote cog registers outside its destination, or the cog did not
finish (EF-087), and the same rule protects it — the `rdlong.yaml` caution names it; a no-wait
`WRFAST` releases nothing. Cite EF-084, EF-086, EF-087 and EF-088 in all six entries.

## A condition-false `BRK` still breaks, and the KB teaches it as conditional (2026-10-01, found while building the SO109 test) — F-477

### F-477 — `brk.yaml` teaches a conditional `BRK` as "break only when condition met"; Parallax documents that a `BRK` breaks whatever its condition — `DONE` 2026-10-01 (YAML); the Assembly manual's BRK entry rides «#352»
> **Applied 2026-10-01 («#372»):** `brk.yaml` — the example now puts the opposite condition on
> `SKIP #1` before an unconditional `BRK` (compiled clean, pnut-ts 1.55.8; v55 :62-63), a new
> `condition_behavior` states :2491 and EF-085, and the "Zero code means unconditional break"
> note is **replaced** by what the sources say about code 0: a plain DEBUG compiles to `BRK #0` and
> launches or updates the debugger, DEBUG() uses codes 1..255 as record indexes (v55 :1056, :1067).
> Searched: Silicon Doc :2491-2493, PASM2 manual :3746 and r4c2 ("unconditionally trigger BRK
> interrupt" — regardless of condition, nothing about the code), v55, `debug_interrupt.yaml`,
> `getbrk.yaml`; no source ties conditionality to the code, so the old wording was wrong, not
> merely unsourced. **Widened:**
> the old example's comparison was also backwards (`CMP value, limit WC` sets C when value is
> BELOW limit, so `if_c brk` broke on the wrong side); the new one states the sense. Added a
> `related:` block (getbrk, skip, conditional-debug, debug_interrupt) and symptom aliases.

**Where:** `language/pasm2/brk.yaml` — example "Conditional Breakpoint" ("Break only when condition
met": `cmp value, limit wc` then `if_c brk #LIMIT_EXCEEDED`), and its note "Zero code means
unconditional break". The Assembly Language Manual's BRK entry
(`p2-assembly-language-manual/opus-master/part-ii/instructions-b.md`, `## BRK {#brk}`) states no
condition caveat at all.
**Against:** `silicon-doc-text.txt`:2491 (P2 Documentation, BRK in the debugging section) —
"Regardless of the execution condition, the BRK instruction will trigger a debug interrupt, if
enabled. The execution condition only gates the writing of the 8-bit code". The KB already says
so in `architecture/debug_interrupt.yaml`:148-150, so `brk.yaml` contradicts the KB's own
architecture entry. Spin2 v55 :61-64 adds the compiler's side: "a condition has no effect, though
an _RET_ will execute normally. In order to make the BRK instruction conditional, an
opposite-condition SKIP instruction is placed before it" — which
`language/pasm2/conditional-debug.yaml` already describes correctly.
**Compiler (legality only), 2026-10-01:** `pnut-ts` 1.55.8 compiles `if_c debug("hi")` to
`if_nc skip #1` + `brk #1` (`$3D640231`, `$FD640236`) and leaves a hand-written `if_z brk #$42`
conditional as written (`$AD648436`), without a warning — so `debug()` users are protected and a
hand-written conditional `BRK`, the shape this example teaches, is not.
**The note:** "Zero code means unconditional break" has no source. Spin2 v55 :1056 says a plain
`DEBUG` resolves to `BRK #0` (and `DEBUG()` to `BRK #1..255`); nothing states a zero code changes
whether the break is taken. `NEEDS-VERIFICATION` for that line alone: find a source or remove it.
**Correction:** replace the example with the documented form (the condition on an opposite-condition
`SKIP #1`, or on a `JMP` around an unconditional `BRK`), and state in `brk.yaml` (and, through «#352»,
the Assembly manual's BRK entry) what the P2 Documentation says: the debug interrupt is triggered
whatever the condition, and the condition gates only the writing of the 8-bit code — so a
condition-false `BRK` shows the debug ISR the previous code. Cite :2491, with v55 :62-63 for the
compiler's `SKIP`. **Not an erratum:** the part does what its own documentation says, so under
`p2-errata/CLASSIFICATION-GUIDANCE.md` this is documented behaviour and stays out of P2 Errata.
**Measured (EF-085, 2026-10-01, Rev C):** three condition-false `BRK`s each entered the debug ISR
and showed the previous condition-true code; a `SKIP` before and a taken `JMP` before cancelled
both effects, and both idioms delivered a wanted break with its own code. The correction now
stands on silicon as well as on :2491; cite EF-085 beside it.

## A manual release published KB content without its index (2026-09-28) — F-476

### F-476 — nothing stops a push while KB content sits past the last KB tag, and pushed content without its index is unverifiable — `DONE` 2026-09-28 (release half v1.21.1; gate half b0e7bce5)

**What happened:** F-475's content commits (09-26) were pushed to `main` on 09-28 by the Streamer
and Architect manual releases — every commit on `main` goes with a manual release's push. No KB
release had run, so the published index still carried the v1.21.0 `sha256` for the five changed
files. The MCP verifies a fetched body against that hash and refuses a mismatch: an uncached
client asking for `p2kbSpin2KwDAT` got *"Content for 'p2kbSpin2KwDAT' is temporarily unavailable —
verification failed"* (reproduced 2026-09-28 by flushing the local cache). Cached clients kept
serving v1.21.0's text. Same symptom as F-441, different cause: F-441 regenerated the index
before the content commit; here no index was regenerated at all.
**Why no gate saw it:** `audit-unpushed-releases.py` checks that release TAGS reach the remote; it
does not ask whether `deliverables/ai/P2/` has commits past the latest KB tag. Every manual release
runs it as an advisory, so the check was in the right place and asked the wrong question.
**Release half — DONE:** v1.21.1 published F-475 with a post-commit index; the five entries verify again.
**Gate half — DONE (b0e7bce5):** `audit-unpushed-releases.py` now reports KB content commits after
the latest `vX.Y.Z` tag on the branch (default report, so the session-start check sees it too) and
answers that question alone with `--kb-content` (local history, no network). The manual-release
runner runs `--kb-content` as the BLOCKING release-phase gate `kb-content-released`; the project's
`release-manual` overlay says what to do when it is RED (run `release-yamls` first, never push around
it). Proven both ways: GREEN on the v1.21.1 tree, RED with both F-475 commits named on a worktree at
ebe15d12, the state that broke.

## DAT is class state, VAR is instance state — the keyword entries never said so (2026-09-26) — F-475

### F-475 — `DAT.yaml` / `VAR.yaml` did not state the class/instance model or how to choose, and `blocks.yaml` advised DAT for "shared buffers (mailboxes, queues)" unqualified — `DONE` 2026-09-26

**Where:** `language/spin2/keywords/DAT.yaml`, `VAR.yaml`, `language/spin2/constructs/blocks.yaml:142`,
`language/fundamentals/variable-scoping-best-practices.yaml` `dat_scope`.
**What was wrong:** the model lived only in `object-image-dedup.yaml` and `variable-scoping`; the
keyword entries an agent reaches first said nothing about instances (DAT) or gave no choice rule
(VAR), and `blocks.yaml` listed mailboxes as a reason to use DAT. A mailbox for a cog EACH
instance starts is instance state — in DAT, a second instance overwrites the first's. Surfaced by
Stephen, 2026-09-26, correcting a P2 Errata style-audit finding that read the central authoring
guide's §3.6 ("shared buffers MUST use DAT") literally: *"Think of `dat` variables as class
variables and `var` variables as instance variables."*
> **Applied 2026-09-26:** `instance_model` + aliases (class/instance variables, singleton state…)
> added to `DAT.yaml` and `VAR.yaml`, each linking the other, `object-image-dedup.yaml` and
> `variable-scoping`; `blocks.yaml`'s DAT reason #2 now says a mailbox belongs in DAT only when
> ONE worker cog serves every instance, else VAR, and its example comment says so;
> `variable-scoping`'s `dat_scope` carries the per-compiled-image nuance; `object-image-dedup`
> links back. **Source trace:** Spin2 v55 (`sources/spin2-v55/spin2-v55-text.txt:181` "each
> instance of this object will have its own VAR memory", `:238`); `object-image-dedup.yaml` (DAT
> shared per compiled image, measured). **Extended the same day** (Stephen: *cog code and registers
> are loaded into the cog before being run — do not confuse them with normal named registers*):
> `DAT.yaml` `instance_model` now says a PASM block and its register longs are an IMAGE that
> `COGINIT` copies into each started cog's RAM, that a cog's register writes never reach the hub
> DAT or another cog, and that cog registers are distinct from hub variables and from the named
> special registers; links `pasm2/coginit.yaml` (whose description grounds the copy: "load code
> from Hub RAM to be executed within Reg/LUT RAM"). Verified: `verify-yaml-format.py` clean on the 5 files,
> `validate-crossref-keys.py` all resolve. The central guide's §3.6 wording is a nomination for
> central (skill-evolution candidates), not a KB defect.
> **Released v1.21.1 (2026-09-28). The family was not finished there** — reading the served
> `blocks.yaml` after that release showed `common_patterns.cog_communication` still calling a
> single DAT mailbox "DAT mailbox for COG communication", unqualified, two screens below the
> reason F-475 had narrowed. A KB-wide sweep (every mailbox declared in a DAT block without an
> instance qualifier nearby) found one more: `constructs/inline_pasm.yaml` `with_communication`,
> whose cog code even hard-codes `##@command`. Both now state the condition — one mailbox for the
> ONE worker cog every instance shares; a cog each instance starts takes its own in VAR, address
> passed in PTRA — in the description and a code comment, linking `DAT.yaml` `instance_model`.
> The sweep's other hits are right as written: `cogid.yaml` / `longfill.yaml` declare a table of
> eight mailboxes indexed by cog (chip-wide state every instance must share — F-475's own DAT
> case), and the shared-bus broker is one resident cog serving all. Released v1.21.2.

## The errata fixes are now proven on silicon (2026-09-26, EF-075..077) — F-474

### F-474 — the KB's `silicon_errata` entries for E3, E4/E5 and E7 should give the fix that ran on silicon, not an unproven workaround — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** each `silicon_errata` workaround now states the proven form, its
> kind and its EF: `getct.yaml` the keeper cog (one-time startup; EF-075, waiting keeper EF-078,
> or wait out one wrap), with the untested "pass the upper long through hub RAM" alternative not
> carried; `getxacc.yaml` the burst_sums helper routine step by step (EF-076); `rdfast.yaml` the
> rule at each use (waiting form or 16 clocks; EF-077, EF-084..088).

**Where:** the `silicon_errata` entries F-462..466 (GETCT, GETXACC) and F-472 (RDFAST) ask to add, in
`language/pasm2/getct.yaml`, `getxacc.yaml`, `rdfast.yaml`.
**What silicon does:** each fix P2 Errata v0.2.0 prints ran byte for byte, beside a positive control
that reproduced the erratum in the same run. **EF-075** (E3): a keeper cog started in cog 7 as the first
line of `main()` (`coginit(KEEPER_COG, @keeper, 0)`, keeper = `jmp #keeper`) — cogs 4–7 started after
one and two wraps read D = 0. **EF-076** (E4, E5): the `burst_sums` routine (zero burst, idle read,
burst, zero burst, idle read, subtract; SINC1) returned exactly N·C in 60 of 60 calls, N = 1..1001.
**EF-077** (E7): `WAITX #12` after the no-wait `RDFAST` (≥ 16 clocks to the blocking one) read correctly
in 1,024 of 1,024 trials across every hub alignment.
**Correction:** when those entries land, each `workaround`/`fix` field states the proven form, cites its
EF, and names its kind (one-time startup fix / helper routine / rule at each use). The E3 entry drops
the untested "read the upper long in cogs 0–3 and pass it through hub RAM" alternative, or marks it
untested; P2 Errata v0.2.0 dropped it for that reason.

## Three KB statements the second errata bench session decides (2026-09-25, EF-071..074) — F-471, F-472, F-473

### F-471 — the KB states the DAC-smart-mode `%TT` rule unqualified; on silicon `OUT` enables the ADC only while `TT` bit 0 enables the output — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** published rules kept; `smart_pins.yaml`
> `dac_smart_pin_modes.silicon_errata.out_needs_tt_bit0_to_run_adc` added (EF-071, TT %00/%01 only),
> and `wrpin.yaml` case 4 carries a one-line pointer to it.

**Where:** `architecture/smart_pins.yaml:408-410` (`condition: "%SSSSS = %00001..%00011"`,
`enable_bit: "x0=disabled regardless of DIR…"`, `adc_control: "0x=OUT enables ADC, 1x=OTHER enables
ADC"`) and `language/spin2/methods/wrpin.yaml:59-60` (the same two rules, as case 4). Both faithfully
repeat the P2 Documentation's table (`p2-documentation.txt:7652-7657`).
**What silicon does (EF-071, Rev C, run twice):** with `TT` = `%00` raising `OUT` runs **nothing** —
the pin's read state stays 0, as with `OUT` low; with `TT` = `%01` `OUT` runs the ADC and the fast DAC
drives the pin. So the two published rules do not combine as written.
**Correction:** keep the published rules and add a `silicon_errata` entry to `smart_pins.yaml` (and a
one-line pointer in `wrpin.yaml` case 4): in the DAC smart modes the ADC runs only while `TT` bit 0 is
set, which also enables the fast DAC's drive; `TT` = `%00` with `OUT` high runs neither. Cite EF-071.
Tested `TT` = `%00`/`%01` only; the `OTHER` forms (`%1x`) untested. → P2 Errata **E6**.

### F-472 — `rdfast.yaml` gives the no-wait requirement no number and no consequence, and omits the no-wait `RDFAST` erratum (P2 Errata E7, which absorbed the planned E8 on 2026-10-01) — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `rdfast.yaml` notes now give the waiting form's 10-17 clocks
> and the no-wait FIFO-read number (first correct read 8-15 clocks; allow ≥ 15, e.g. `WAITX #11`;
> an earlier read returns zero) from EF-073, and a new
> `silicon_errata.no_wait_rdfast_releases_next_hub_op` carries condition, every symptom, the rule,
> what is not affected (no-wait WRFAST; blocking first RDFAST), what is untested, and
> EF-074/077/084/086/087/088. Symptom aliases added. The description was tightened to keep the
> entry within its line budget. SOURCE-ERRATA E-015 is not cited in the YAML (a comment thread is
> not a citable source).

**Where:** `language/pasm2/rdfast.yaml` — "D[31]=1 for no-wait mode (doesn't stall for FIFO fill)"
(:70), with no minimum distance and nothing on what an early read returns.
**What silicon does (EF-073, EF-074, Rev C, run twice):** (1) a blocking `RDFAST` alone keeps its
promise (3,072/3,072, 10–17 clocks); (2) after a no-wait `RDFAST`, a read is safe from **15 clocks**
(8..15 by hub alignment; `WAITX #11`), and a read before that returns **zero** with no flag; (3) no
unsafe distance for a no-wait `WRFAST` write; (4) **erratum:** a blocking `RDFAST` issued while a
no-wait one is still arming can skip its wait (2 clocks) and the next read returns zero — one gap
per alignment within 8..15 clocks; correct from 16 clocks on.
**And (EF-084, 2026-10-01, Rev C):** (5) **erratum:** a `RDLONG` issued within 16 clocks of a no-wait
`RDFAST` is released before its own read in most hub alignments (43 of 64 at the next instruction)
and returns the **previous hub read's long**; a `WRLONG` there is released before it lands and is
**lost** if a hub read follows at once; nothing reports either; from 16 clocks (7 non-hub
instructions) on, and with the waiting form, both are correct (reads EF-084; writes at 16 clocks
EF-088, 2026-10-01 — EF-084's own write runs were at the next instruction only). The window coincides with (4): one
release, acting on whatever hub instruction is waiting. (6) Making the first `RDFAST` blocking also
removes (4) (18,432/18,432). The Spin2 interpreter uses only the blocking form.
**Correction:** add the measured no-wait rules — FIFO reads safe from 15 clocks (the zero read is an
anti-pattern, also routed to P2 Anti-Patterns), and **no hub-memory instruction within 16 clocks
of a no-wait `RDFAST`** (or use the waiting form) — and `silicon_errata` entries for (4) → P2 Errata
**E7** (workarounds: 16 clocks `RDFAST` to `RDFAST`, or a blocking first `RDFAST`; F-474 carries the
E7 fix wording) and (5) → also **E7** (merged 2026-10-01: one trigger, one window, one workaround — `p2-errata/CLASSIFICATION-GUIDANCE.md`). Cite EF-073/EF-074/EF-084/EF-088; note SOURCE-ERRATA E-015 (Chip's
unexplained "Yes") as plausibly (4). **Scope as proven (EF-084, EF-086):** every hub read and write
width (`RDBYTE`/`RDWORD`/`RDLONG`, `WRBYTE`/`WRWORD`/`WRLONG`) and a blocking `RDFAST`; a `SETQ`
block `RDLONG` in the window either wrote one wrong long, left seven unwritten and overwrote cog
registers `$000`–`$001`, or the cog did not finish (EF-086, EF-087), and the rule protects it
(the waiting form and 16/18/20 clocks clean, EF-087); a
no-wait `WRFAST` does **not** release a following hub instruction (state it, so readers do not
over-apply the rule); `RETA` and interrupts in the window are not measured; hub execution cannot
use `RDFAST` (P2 Documentation). The same caution goes to the read/write entries (F-478).

### F-473 — `getxacc.yaml`'s `sinc2_constraint` can now state its mechanism: SINC2's running first stage read across windows of unequal length (NOT the one-clock carry — corrected 2026-09-26) — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»), with F-469:** `sinc2_constraint` rewritten — the Silicon Doc note
> quoted as the source, the measured mechanism (SINC2's running first stage across unequal
> windows, not the one-clock lag), both proven workarounds (power-of-two count; XZERO), SINC1 off
> by at most one term, classed as documented behaviour, citing EF-072. The old "~30-60 ms" and
> "under ~20 ms" figures (Chip Gracey's forum report, `ingestion/external-inputs/forum-threads/
> ProblemGoertzelSINC2mode/INGEST.md` :43, :49) are **superseded by the bench**: the entry states
> EF-072's measurement — a corrupted pair at every window-length change and never otherwise; XZERO
> clean at 10.24 µs, 100 µs and 25 ms — and does not mention the forum figures (Stephen,
> 2026-10-01: "the results should supersede"). History: a first pass removed them as "no Parallax
> source" (wrong — they were Chip's), a second restored them framed as designer guidance, a third
> replaced them with the measurement, all before the push.

**Where:** `language/pasm2/getxacc.yaml` `sinc2_constraint` (F-469 held the rest of this entry "until
VO-J-013 runs" — it has run).
**What silicon does (EF-072, run twice):** Chip's SINC2 corruption reproduces exactly (odd-length
windows corrupt that sample and the next, then correct; SINC1 off by one term at most; XZERO clean;
one clock of read jitter → 75 % of samples off by ≥ 1,000 terms), and the accumulator model predicts
every sample, clean and corrupted, value for value.
**Correction:** apply F-469's citation fix, then state the mechanism: in SINC2 the first stage is a
running integral that `GETXACC` does not clear, so a window one clock longer or shorter than its
neighbours moves one first-stage value between two adjacent samples (the current and the next), then
self-corrects. Keep Chip's workarounds (power-of-two count, or XZERO) and cite EF-072. **Do not**
attribute it to the one-clock lag (F-464/EF-070): the rig's model shows the lag's share is not
separable (it shifts every first-stage value by one term, which the fit absorbs), and the same pairs
follow without it.
**Classification (corrected 2026-09-26):** documented behaviour — the P2 Documentation's *NOTE ABOUT
GOERTZEL SINC2 MODE (2024.12.16)* states it — so not an erratum and **not part of P2 Errata E5**
(the earlier text here said E5 covered it). E5 mentions it only as a scope note on its SINC1 fix.

## Two KB statements contradicted by our own sources, found while building the SINC2 test (2026-09-25, VO-J-013) — F-469, F-470

### F-469 — `getxacc.yaml`'s `sinc2_constraint` says Chip's SINC2 note is "not yet in the released Silicon Doc"; the Silicon Doc carries it — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** "not yet in the released Silicon Doc" removed; the note is cited
> as NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16). The rest of the entry landed via F-473.

**Where:** `language/pasm2/getxacc.yaml` `sinc2_constraint` — "Reported by Chip Gracey (P2 designer),
2024-12-16; not yet in the released Silicon Doc."
**Against:** `silicon-doc-text.txt` ≈ :1704 — "NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16) It has just
been discovered that the Goertzel SINC2 mode generates periodic problematic GETXACC readings when the
number of iterations in a Goertzel cycle varies …". The note is in the document we ingested.
**Correction:** cite the Silicon Doc note as the source (Tier 1) and drop "not yet in the released
Silicon Doc". **Hold the rest of the entry** until VO-J-013 runs: whether this constraint is a silicon
erratum or a documented behaviour is being decided on the bench and by the clean-room classification.

### F-470 — `muldiv64.yaml` calls every parameter "32-bit signed"; Spin2 v55 says MULDIV64 is an unsigned operation — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** description, the three parameters, the return and the notes
> now say unsigned, quoting v55 :566. **Widened:** "Division by zero returns 0" had no source (v55
> says nothing of a zero divisor) — removed. `related:` bare names QLOG/QEXP redirected to full
> paths. **Sweep:** no manual or app note teaches a signed MULDIV64; P2AN001 already calls its
> ratio unsigned. **Divide-by-zero search (re-done properly after Stephen's challenge):** Spin2
> v51/v55 text, the v51 interpreter analysis, the interpreter source (`Spin2_interpreter.spin2`
> `muldiv64_`: QMUL, then the shared CORDIC divide path — so its zero-divisor result is QDIV's),
> the Silicon Doc DIVIDE section, the PASM2 manual QDIV/QFRAC rows, the bench ledger — none states
> the result. Removal stands; QDIV's own zero-divisor behaviour is F-480.

**Where:** `language/spin2/methods/muldiv64.yaml` — lines 10, 13, 16 ("32-bit signed") and 40 ("All
parameters are 32-bit signed").
**Against:** `spin2-v55-text.txt:566` — "MULDIV64(mult1,mult2,divisor) : quotient | Divide the 64-bit
product of 'mult1' and 'mult2' by 'divisor', return quotient (**unsigned operation**)."
**Correction:** state unsigned operands and quotient, citing v55. **Sweep** the manuals and app notes
that teach MULDIV64 (fixed-point and CORDIC material) for the signed claim — a signed reading changes
results for any operand with bit 31 set.

## Two hub-FIFO facts the KB states wrongly, found while building the RDFAST readiness test (2026-09-25, VO-J-012) — F-467, F-468

### F-467 — `architecture/hub.yaml` says a hub slice is `address & 7`; the Silicon Doc says each slice holds every 8th long (address bits [4:2]) — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `hub.yaml` `slicing` now quotes the Silicon Doc and states slice
> = (address >> 2) & 7 on the 8-cog part; `slice_assignment` rewritten in long addresses. **Sweep:**
> no other YAML or manual carries the `address & 7` claim; the Assembly Reference (ch. 1) already
> says "every eighth long".

**Where:** `architecture/hub.yaml` `slicing.concept` — "Each slice corresponds to addresses where
(address & 7) equals slice number" — and the `slice_assignment` block beneath it ("Addresses ending
in 000 binary" …).
**Against:** `silicon-doc-text.txt` §THE COG -to- HUB RAM INTERFACE (≈ :2999) — "Each RAM slice holds
every single/2nd/4th/8th/16th (depending on number of cogs) set of 4 bytes". A slice is a **long**
granularity: slice = address bits [4:2] on the 8-cog part, not bits [2:0]. `address & 7` would put
the four bytes of one long in four different slices.
**Correction:** state slice = `(address >> 2) & 7` (bits [4:2]) on the P2X8C4M64P, rewrite
`slice_assignment` in terms of long addresses, cite the Silicon Doc. **Sweep** for the same claim in
the other hub/egg-beater YAMLs and the manuals (Architect's Guide, Assembly Reference hub chapter).

### F-468 — `pasm2/rdfast.yaml` lists FBLOCK as "Wait for FIFO block wrap"; FBLOCK sets the next start address and block count — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `rdfast.yaml` FBLOCK line now reads "Set the next start address
> and 64-byte block count, taken when the current blocks are fully read (2 clocks, never waits)"
> (:3022, :3045). `wrfast.yaml` and `fblock.yaml` checked: neither carries the wrong wording.

**Where:** `language/pasm2/rdfast.yaml:68` — "FBLOCK: Wait for FIFO block wrap".
**Against:** `silicon-doc-text.txt` :3022 — "The FBLOCK instruction provides a way to set a new start
address and a new 64-byte block count for when the current blocks are fully read or written"; and
:3045 "FBLOCK doesn't need to wait for anything, so it always takes two clocks."
**Correction:** replace with FBLOCK's actual role (queue the next start address and block count,
taken at the next wrap; 2 clocks, never waits), citing the Silicon Doc; check `wrfast.yaml` and
`fblock.yaml` for the same wording.

## Five silicon errata decided on the bench, and what they change in the KB (2026-09-25, P2 Errata campaign) — F-462 … F-466

All five predictions of the P2 Errata campaign held on real silicon (EF-066 … EF-070,
`hardware-verification/P2-EMPIRICAL-FINDINGS.md`; VO-J-007..011). Each finding below is what that
evidence requires of a shipped YAML. **Evidence tier:** EF — the top of the authority order, above
the Silicon Doc; each is a structural yes/no result, so N=1 is dispositive. **The counter above read
`F-460` while F-460 and F-461 were already allocated (2026-09-22)** — corrected to `F-467` in this pass.

### F-462 — `getxacc.yaml` says `GETXACC` clears the accumulators and that values hold until a new streamer command; silicon does neither outside a Goertzel burst — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `getxacc.yaml` description, `reading_protocol` and `notes` now
> say the clear acts only during a Goertzel burst and an idle read returns and keeps the running
> total, keeping the Silicon Doc's statement as the documented one; new
> `silicon_errata.clear_only_during_goertzel_burst` (EF-069). The read-before-and-after,
> take-the-difference rule kept, now with its reason.

**Where:** `language/pasm2/getxacc.yaml` — `description` ("Capture the streamer's Goertzel
accumulators into holding registers and clear them … SUBSEQUENT GETXACC INSTRUCTIONS RETURN THE SAME
CAPTURED VALUES UNTIL A NEW STREAMER COMMAND EXECUTES"), `reading_protocol` ("captured and cleared at
the GETXACC … until a new streamer command executes"), `notes` ("captured into holding registers and
cleared by GETXACC").
**What silicon does (EF-069):** with the streamer idle, or running any non-Goertzel mode, `GETXACC`
returns the live accumulator and **clears nothing** — 50 of 50 reads equal the prior value, including
reads taken right after `XINIT` of a new non-Goertzel command; the accumulator keeps growing from one
burst to the next. The clear acts only **during** a Goertzel burst, and there it partitions the burst
exactly (read + next read = one unread burst; 8 of 8).
**Correction:** state that `GETXACC` clears only while the streamer is running in Goertzel mode, that
an idle read returns and preserves the running total, and that a new streamer command does not reset
it. **Keep** the read-before-and-after, take-the-difference rule — it is exactly what this behaviour
requires, and now has its reason. Add a `silicon_errata` entry citing EF-069.

### F-463 — `getct.yaml` omits the stale upper long a four-cog group reads after missing a counter wrap — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»), including the 2026-09-27 extension:** `pasm2/getct.yaml` — the
> "full 64-bit value" sentence qualified, and `silicon_errata.stale_upper_long_after_missed_wrap`
> added (condition for both groups, the band closing in one wrap, what is affected and what is not,
> the keeper/wait-one-wrap workarounds; EF-068, 075, 078..083). `spin2/methods/getms.yaml` and
> `getsec.yaml` carry the same note (EF-080, 082), `getsec.yaml`'s "Good for long-duration timing"
> qualified, and their bare `related:` names redirected to full paths; `spin2/methods/getct.yaml`
> notes that GETCT() itself is unaffected (EF-082). Symptom aliases added to `pasm2/getct.yaml`.

**Where:** `language/pasm2/getct.yaml` — no `silicon_errata`; the description presents `GETCT WC`
then `GETCT` as reading "the full 64-bit value" with no condition.
**What silicon does (EF-068):** cogs 0–3 and 4–7 each read their own copy of the counter. A group's
upper long advances only at a wrap of the lower long while at least one cog of that group is running;
a cog started in a group that missed wraps reads an upper long behind by one per missed wrap until its
group runs through the next wrap. From reset only cog 0 runs, so a program's first cog in 4–7, started
after the first wrap (2³² clocks, ~21.5 s at 200 MHz), reads a wrong 64-bit time. Measured D = 1, 0,
2 in the three predicted states; D = 0 throughout with the group kept running.
**Correction:** add a `silicon_errata` entry (condition, effect, workaround: keep one cog of each group
in use running from before the first wrap, or take the upper long from a group-0 cog) citing EF-068,
and qualify the "full 64-bit value" sentence. **Also check** `language/spin2/methods/getct.yaml` and
any KB text that builds 64-bit time from `GETCT WC` in a cog of 4–7.
> **Extended 2026-09-27 (EF-078..080) — still `CONFIRMED`, not yet applied; the entry now covers
> five facts and three more YAMLs.** Verified on disk the same day: `pasm2/getct.yaml`,
> `spin2/methods/getct.yaml`, `getms.yaml`, `getsec.yaml` carry nothing of it.
> 1. **It is a bounded window (the band), not a lasting state:** it closes at the FIRST wrap the
>    group runs through, in one step, whatever the lag — measured from 1 (EF-068), 2 (EF-079) and
>    8 (EF-080). An interval timed across the closing wrap is too long by the missed wraps × 2³²
>    clocks (cog 4 stepped 0 → 9 across one wrap, EF-080). So the workaround list gains *wait one
>    wrap after the group's first cog starts before trusting a 64-bit time there*.
> 2. **Both groups:** with every cog of 0–3 stopped (cog 0 included), cogs 0–3 show the same band
>    and the same one-wrap close (EF-079). The "take the upper long from a group-0 cog" workaround
>    holds only while a cog of 0–3 keeps running.
> 3. **A waiting cog counts as running:** a keeper held in `WAITATN` or in `WAITX` at the wrap kept
>    its group current (EF-078). Spin2 `WAITCT()`/`WAITMS()`/`WAITUS()` are a `GETCT` polling loop in
>    the interpreter (v55 `pwct`), so a Spin2 cog in them is executing anyway.
> 4. **Spin2 `GETMS()` and `GETSEC()` are affected exactly as `GETCT WC` is:** the interpreter computes
>    both from the calling cog's `GETCT WC` + `GETCT` ÷ `clkfreq` (v55 `getms_`); in the band a cog 5
>    read `GETMS` 18,819 beside cog 0's 190,617 (EF-080). `spin2/methods/getms.yaml` and `getsec.yaml`
>    need the same `silicon_errata` note, and `getsec.yaml`'s "Good for long-duration timing" needs it
>    beside it. (`MULDIV64` does not read the counter — not affected.)
> 5. The condition to state: *in a cog of a four-cog group that has had no running cog at one or more
>    wraps of the lower long, until that group runs through its next wrap.* The P2 Errata manual's E3
>    chapter carries the same five facts (v0.2.0).

### F-464 — `getxacc.yaml` omits the one-clock lag that leaves each Goertzel burst's last term for the next burst — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `getxacc.yaml` `silicon_errata.last_term_lands_in_next_burst`
> (EF-070), with the burst_sums workaround shared with F-462; the SINC2 constraint kept separate
> (different condition, documented).

**Where:** `language/pasm2/getxacc.yaml` — no statement of it anywhere.
**What silicon does (EF-070):** a read after a burst of N clocks holds N − 1 terms; the last term
waits in an internal register no instruction reads and is added on the first active clock of the
**next** Goertzel burst. Waiting does not deliver it. A trailing zero-term burst (same mode, input
enables clear) delivers it — 16 of 16 sequences, N = 64 and 65, both signs.
**Correction:** add a `silicon_errata` entry with the effect and the proven workaround, citing EF-070;
reconcile with the existing `sinc2_constraint` note (Chip Gracey's off-by-one) — related path,
different condition, so neither replaces the other.

### F-465 — `setq.yaml` says the cancelled block delta leaves `PTRx` at "+4 for one long"; silicon applies the plain expression's own step — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** all five places (`setq.yaml`, `rdlong.yaml`, `wrlong.yaml`,
> `wmlong.yaml`, `concepts/setq_block_ops.yaml`) now say the plain expression's own step (+4 for
> `ptra++`, +12 for `ptra++[3]`), citing EF-067 (ALTD tested; `wmlong.yaml` notes WMLONG itself
> untested). `setq.yaml` also gains the no-wait-RDFAST block-read note (F-478 family).

**Where:** `language/pasm2/setq.yaml` `silicon_errata.block_transfer_ptrx_delta` — "(PTRx advances by
+4 for one long, NOT by N*4)". **Widened 2026-09-25 (P2 Errata E1 drafting, «#357»):** the same
wording is in four more places, all read on disk — `rdlong.yaml:28`, `wrlong.yaml:27`, `wmlong.yaml:19`
(`setq_block_ptrx_delta`: "PTRx advances by +4, NOT N*4") and `concepts/setq_block_ops.yaml:23`
("the normal PTRx expression amount (+4 for one long), NOT by N*4"). **This entry previously called
`setq_block_ops.yaml` "already right"; it is not** — it says "normal PTRx expression" and then pins
the amount to one long in the same sentence. Its line-27 example (`ptra++`, "+4") is correct as an
example and stays.
**What silicon does (EF-067):** `ptra++` → +4, but **`ptra++[3]` → +12**: the step is whatever the
PTRx expression does without `SETQ`, not one long. `augs.yaml` is right. Confirmed across `ptra`,
`ptrb`, `RDLONG`, `WRLONG`, `SETQ2` and an 8-long block, every long delivered to the `ALTD` destination.
**Correction:** in all five places, replace "+4 for one long" / "+4" with "the plain PTRx
expression's step (e.g. +4 for `ptra++`, +12 for `ptra++[3]`)", citing EF-067. Only `ALTD` was tested
as the intervening instruction.

### F-466 — `augs.yaml`'s intervening-`ALTx` erratum can now say where the damage lands and settle its `AUGD` scope note — `DONE` 2026-10-01
> **Applied 2026-10-01 («#372»):** `augs.yaml` description adds where the damage lands (the ALTx
> D register's auto-increment from S[17:9]; AUGS #$3C5C0A55 → +5), and the scope note's "not
> asserted" is replaced by EF-066's AUGD result, scoped to the one ALTx variant tested.

**Where:** `language/pasm2/augs.yaml` `silicon_errata.intervening_altx_immediate_s_consumes_augs` —
its `description`/`example`, and its `scope_note` ("Whether THIS specific intervening-#S errata also
applies to AUGD … is not stated in any golden source and is deliberately not asserted here").
**What silicon does (EF-066):** confirmed as described (the `ALTx` is augmented, the target still gets
the augment). **Where it lands:** an `ALTx` takes its base from `S[8:0]` and its auto-increment from
`S[17:9]`; the augment leaves the base alone, so the substituted register is the one aimed at — the
damage is the `ALTx` D register's auto-increment, taken from the `AUGS` value (`AUGS #$3C5C0A55` →
+5). **`AUGD`:** a pending `AUGD` survived an intervening immediate-`S` `ALTS` and reached its `#D`
target intact; an `ALTx` has no immediate-`D` form to consume it.
**Correction:** add the observable effect to the description, and replace the scope note's "not
asserted" with the EF-066 result, scoped as tested (one `ALTx` variant for the `AUGD` half).

### F-449 — `sumnc.yaml` and `sumnz.yaml` carry behavior prose in their flag fields — `DONE` 2026-09-22 (651e1ad0, shipped in v1.21.0; status flipped 2026-09-28)

> `pasm2/sumnc.yaml:29` and `pasm2/sumnz.yaml:30` hold *"0 then D = D - S, else D = D + S"* where a
> C (resp. Z) effect belongs. Correct values, from the manual's Part II entry
> (`instructions-s.md:1332-1335`) and from `sumc.yaml:6`/`sumz.yaml:7`: C = `true sign of (D +/- S)`,
> Z = `Result == 0`. **The manual is right; the YAML is wrong.** The manual's Appendix A had
> inherited the corruption and was corrected in this pass.

### F-450 — `incmod.yaml` C effect is a corrupted string — `DONE` 2026-09-22 (651e1ad0, shipped in v1.21.0; status flipped 2026-09-28)

> `pasm2/incmod.yaml:39` reads *"1, else D = D + 1 and C = 0"*. The manual's Part II entry
> (`instructions-i.md:81`) has it right: `D was S (wrapped)`. Manual right, YAML wrong; Appendix A
> had inherited it and was corrected in this pass.

### F-451 — four more shipped flag/oneliner strings are garbage or wrong-shaped — `DONE` 2026-09-22 (651e1ad0, shipped in v1.21.0; status flipped 2026-09-28)

> - `pasm2/rcr.yaml:28` — C effect `Last bit out1` (stray footnote digit). Every sibling uses
>   `last bit shifted out if S[4:0] > 0, else D[31]`.
> - `pasm2/getct.yaml:6` — C effect `same`, which is meaningless. Part II correctly shows `---`:
>   GETCT's WC is an **input selector** choosing which half of the 64-bit counter is returned, and
>   C is not written. (This also corrects a subagent proposal to *add* GETCT to the manual's
>   "WC only" list — it does not belong there, and the manual's own count was fixed the other way.)
> - `pasm2/getct.yaml:36` — `oneliner: T=0 on reset, CT++ on every clock` describes the **register**,
>   not the instruction. The manual's Appendix C is right: `Get CT[31:0] or CT[63:32] if WC into D`.
> - `pasm2/pollxrl.yaml:30` — Z effect `XRLEvent`, missing the space; the manual has `XRL Event`.

### F-452 — `loc.yaml` categorizes LOC as Math and Logic — `DONE` 2026-09-22 (651e1ad0, shipped in v1.21.0; status flipped 2026-09-28)

> `pasm2/loc.yaml:31` says `category: Math and Logic`, which places LOC under Arithmetic in the
> manual's categorical index and `instruction-categories.md`. LOC loads an address (the manual's own
> entry title is *Load Address*), and the identical `(per W)` PA/PB/PTRA/PTRB mechanism puts CALLD
> under Branching. **The manual is faithfully following its source here, so the manual needs no
> edit** — the YAML category is the defect, and the manual's grouping will follow once it is fixed.

