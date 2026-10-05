# P2KB Correction Findings — ARCHIVE, swept 2026-10-05 (the register reconciliation, «#386»)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 130 findings verified CLOSED on 2026-10-05 against the tree and the latest release
> tags (KB `v1.23.3` and each manual's latest tag): every verdict came from a read-only agent
> with re-runnable `contains`/`absent` assertions, and the arbiter re-ran all of them and read
> each caveat by hand. Most carry `RESOLVED` — which the register's legend defines as closed,
> awaiting a sweep — and the rest `DONE`. The 63 section headings whose every entry closed came
> with them. The open findings (F-547 and 49 others) stay in the live register.
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut
> to the closed findings, and the live copy had the same text removed. **Method disclosed:** of the
> 78 line ranges removed across the two copies, 57 were deleted by the dispatched agents with a
> line-range `sed`/`perl` command — a breach of this project's rule that file content changes go
> through the edit tools — and 21 with the Edit tool (one, a 258-line range the live-side agent
> missed, by the arbiter). Losslessness rests on the check, not the method: every line below is
> the pre-sweep text (commit dd4cf8ed), verbatim, nothing was lost or duplicated across the two
> files, and `audit-register-hygiene.py --sweep-check dd4cf8ed` proves it.

---

## The changelog/cover version drift, and the gate that now catches it (2026-09-22) — F-461

### F-461 — nothing checked that a manual's rendered version had a changelog entry — `RESOLVED — gate built, wired and armed 2026-09-22`

**Three manuals released in one evening, and ALL THREE reached the promote step with a changelog
that did not describe the version printed on their own cover.**

| Manual | `request.json` | CHANGELOG top entry |
|---|---|---|
| Assembly | 3.1.10 | v3.1.9 — and carrying none of the twelve batch-2 corrections that caused the bump |
| deSilva | 3.0.8 | v3.0.7 — the already-tagged release. No v3.0.8 entry existed at all |
| Single-Step Debugger | 1.0.1 | none — caught only because the two before it had made the pattern obvious |

**The mechanism is the same every time, and it is structural, not careless.** A render needs a
version; `request.json` is where the version lives, so it gets bumped. The changelog is a different
file, and nothing requires touching it. The two drift silently and agree again only by accident.

**Why no existing gate saw it.** `audit-changelog` reads the top entry well — but `release-manual`
runs it at **promote**, after the Forge render is already spent. Every prepare-phase gate reads the
markdown body and has no opinion about the directive. So the defect was free to travel to the last
step before publication three times in one evening, and each repair was made under time pressure at
exactly the wrong moment.

**The instrument:** `engineering/tools/validation/audit-changelog-version-sync.py`, wired into
`validate-manual-release.py --phase prepare` as `changelog-version-sync` (blocking), where the fix
is free. `audit-gate-arming.py` confirms it is armed. `--negative-control` proves both checks
distinguish both ways, including that a decorated value still compares equal so a shape defect
cannot masquerade as a changelog mismatch.

**The first fleet sweep it ever ran found two more, of a different class.** Two of the ten manuals
carried a *decorated* `metadata.version` — `p2-debug-window-manual` at `"Version 1.1.3"` and
`p2-xbyte-programming-guide` at `"v1.1.0"`. The cover supplies the word "Version" itself, so an
adopted document renders **"Version Version 1.1.3"**. Both were invisible because neither manual has
adopted metadata single-sourcing yet: their covers come from hardcoded markdown and the value only
reached the PDF properties. **A landmine, not a defect — until the release at which that manual
adopts single-sourcing, which the standing rule requires.** Both `request.json` values corrected to
bare numbers in the same pass; the fleet is green, ten of ten.

**What this says about the gate set generally.** The value here was not the rule, which is obvious
once stated. It was that nothing *ran* it at the moment it was cheap — the same shape as F-301's
tracker that was read and never written, and as `audit-backtick-balance.py` sitting on disk, clean,
invoked by nothing. The question to ask of any rule is not "is it written down" but "what executes
it, and when".

## Shipped-artifact fallout of the Assembly v3.1.10 release (2026-09-22) — F-460

### F-460 — the Single-Step Debugger manual's shipped PDF labels PA and PB as COGINIT parameters — `RESOLVED — proven on the artifact 2026-09-22`

**Not a YAML finding; it does not gate the YAML head.** Recorded here so it is not lost.

The cog-register figure macro `\SpecialRegistersMapDiagram` lives in
`engineering/document-production/platform/templates/p2kb-platform-diagrams.sty` and labelled `PA`
and `PB` as *"Parameter A (COGINIT)"* / *"Parameter B (COGINIT)"*. They are not: PA and PB receive
an address from `CALLD`'s return form, from `CALLPA`/`CALLPB`, and from `LOC`. Assembly's own prose
two lines beneath the figure said so, which is how it was caught.

Fixed 2026-09-22 (b811fd930) in **both** copies — the platform file and Assembly's
`p2kb-pasm2-diagrams.sty` workspace fork, which is the one Assembly actually renders from — and
proven on the returned Assembly v3.1.10 PDF (`CALLD ret / CALLPA / LOC` present ×1, `Parameter A
(COGINIT)` absent).

**The second half — CLOSED the same day.** `p2-single-step-debugger-manual` was the *only* other
document that draws this macro (grep for `SpecialRegistersMapDiagram` across `workspace/` and
`manuals/` returns exactly these two), and its v1.0.0 of 2026-09-10 predated the fix. It
re-rendered as **v1.0.1 on 2026-09-22 06:48** and was **verified on the page, not on the diff**:
p39 rendered at 105 dpi and read — `$1F6 PA — CALLD ret / CALLPA / LOC`, `$1F7 PB — CALLD ret /
CALLPB / LOC` — with `Parameter A (COGINIT)` and `Parameter B (COGINIT)` absent from the whole
document. 47pp, unchanged, which is the expected result for a figure-label fix.

**Worth keeping from how the bundle was built.** The content-hash diff against
`manual_store_platform_hashes` found exactly ONE of this manual's ten platform files stale in the
Forge manual store — `diagrams.sty`, `e900593a…` → `5b3d2f2b…` — so the deploy carried the body
`.md`, that one `.sty`, and a force-staged `request.json` for the document switch. The hash map
turned "which shared files does this re-render actually need?" from a judgement call into a
measurement, and it named the right file without being told what the defect was.

### F-455 — `addon-rtc.yaml` lost the VIO3V3 trickle-charge mechanism — `RESOLVED — applied 2026-09-22`

> Deleted: `VIO3V3: "3.3V supply; powers the RTC and trickle-charges the backup battery."`
> **Source:** `P2-RTC-Add-on-text.txt:56` — "3.3V voltage required to power the RTC board and
> trickle-charge the on-board battery". A tree-wide grep for `trickle|charge` returned only
> RC-capacitor text in an app note: the mechanism by which the RTC survives power loss was absent
> from the entire KB. Restored with the 150 nA typical backup current and the consequence for a
> board left unpowered.

### F-456 — `addon-rtc.yaml` lost the cell specification and the UN 38.3 transport classification — `RESOLVED — applied 2026-09-22`

> Deleted: Seiko MS421R 1.5 mAh / 0.11 g, 3.2 mm mounting hole, 0.8 x 1 in PCB, −20…+60 °C, and the
> **UN Manual of Tests and Criteria Part III §38.3 → Class 9 Dangerous Goods** classification.
> **Source:** `complete-P2-RTC-Add-on-reference.md:54-67`. Only the cell part number survived, as a
> datasheet pointer. The transport classification is a fact a product integrator needs and cannot
> derive from the electrical specification. Restored in full.

### F-457 — `addon-hyperram-hyperflash.yaml` lost its ACC HDR jumper instruction, and the surviving text says the opposite — `RESOLVED — applied 2026-09-22`

> Deleted: "the board does NOT source power via the pass-through header's 5V socket, so the P2-ES
> Eval Board Rev B's ACC HDR jumper can remain in its default off position."
> **Source:** `hyperram-hyperflash-text.txt:57`, verbatim.
> ⚠ **What made this worse than a plain omission:** after the deletion, the only `ACC HDR` text left
> in the shipped KB was `addon-serial-host.yaml:78,89`, which states the **opposite** — that board
> *requires* the jumper fitted. A reader carrying that instruction across would fit a jumper this
> board does not want. Restored, with an explicit warning not to carry the Serial Host rule over.

### F-458 — `smart-pin-11011-usb-host-device.yaml` replaced an honest gap statement with a pointer to a document that does not contain the fact — `RESOLVED — applied 2026-09-22`

> A commit deleted an explicit "not stated in any primary source" note about the J/K/SE0/SE1
> line-state detector thresholds and replaced it with `"...are electrical characteristics — see the
> P2 datasheet."` **The datasheet contains ZERO occurrences of `SE0` or line-state** (it names USB
> twice, as a capability). Restored as a NOT-STATED entry that names where it is not stated and says
> the closer is Chip Gracey or a bench measurement, not further reading.
>
> ⭐ **Shared mechanism, worth naming alongside F-454:** this did not *soften* a claim, it replaced
> an accurate statement with a confident wrong one. That is why the study's "weakened" class was
> empty (0 of 518) while real damage existed — **the failure mode in this window is over-confident
> replacement, not hedging.** Same family as the manuals' payoff-sentence defect.

### F-459 — `spin2-builtin-symbols-complete.yaml` advertises 1,024 symbol records it does not carry — `RESOLVED — applied 2026-09-22`

> `category_summary.clock` claims `pll_multipliers: 1024 symbols (XMUL1-XMUL1024)`,
> `clock_sources: 5 symbols` and `crystal_dividers: 7 symbols`. The file carries **zero** records in
> all three, and an inline comment still said "exactly one XMUL record is carried here" after the
> last one was removed on 2026-09-14. An agent reading the summary is promised 1,024 lookups that do
> not exist. "Valid YAML, wrong content" — no gate reads a summary block against its own file.
>
> **Applied:** the summary is now explicitly labelled as the SOURCE DOCUMENT's tally rather than
> this file's inventory, the zero-record categories are named, and the reader is redirected to
> `architecture/clock_system.yaml`. **The record deletion itself was CORRECT and is not reopened:**
> `XMUL`/`XDIV`/`XSEL` appear nowhere in Spin2 v55; they survive only in the superseded v51
> extraction.

> ⚠️ **DO NOT RE-RAISE: the `-D symbol=value` entry in
> `language/spin2/preprocessor/external-symbols.yaml:278` is CORRECT.** No finding is filed for it.
> The study initially flagged it as asserting compiler behaviour the compiler contradicts — it says
> PNut-TS **rejects** `-D symbol=value` with a quoted error and a non-zero exit, and the container's
> `pnut-ts` accepted it silently. **The YAML is right and the finding was wrong.** The container
> ships **v1.55.5**; v1.55.8 lives under `~/.local/pnut/`. Tested there with a clean control:
> `-D VERS=200` → `ERROR- -D VERS=200 is not supported; -D takes a presence-only symbol name (use -D VERS)`,
> **exit 1, no output file** — matching the YAML's quoted string and both sub-claims exactly.
> `-D 9BAD` and `-D BAD-NAME` are likewise rejected; `-D VERS` compiles.
> 🔴 **The general lesson, which applies to every compiler-settled finding taken in this container:
> `/usr/local/bin/pnut-ts` is a RELEASE BEHIND (1.55.5 vs 1.55.8). Re-run on the 1.55.8 path before
> trusting any `pnut-ts` verdict.** The install cannot be overwritten without root and is awaiting
> the container rebuild.

## KB defects surfaced by the Assembly Manual deep audit (2026-09-22, «#348») — F-447 … F-453

All six surfaced by the `document-audit` deep pass on the P2 Assembly Language Reference Manual
(`engineering/document-production/manuals/p2-assembly-language-manual/audit/periodic-audit-2026-09-22.md`).
Every one was verified by the arbiter against a primary source, not taken from a subagent's report.
**F-447 and F-448 are applied in this pass**; the rest are open.

F-447 and F-448 (and F-449…F-452, swept 2026-10-01) are archived; F-453 stays open.

### F-453 — `architecture/locks.yaml`'s `state_versus_allocation` block carries no `source:` — `DONE` (verified 2026-10-05 «#386»: the block cites the Silicon Doc in v1.23.3)

> The block is **correct** — `silicon-doc-text.txt:3698` states it plainly (*"A lock will also be
> implicitly released if the cog that's holding the lock is stopped (COGSTOP) or restarted
> (COGINIT), or if LOCKRET is executed for that lock"*) and `:3686`/`:3696` give the
> allocation-versus-held split. But it ships with no provenance, and the claim-sourcing gate reads
> that field. **This cost a round-trip in this very audit:** one subagent declined to carry the fact
> into the manual *because* it could not corroborate it, while another had already cited the Silicon
> Doc for it. A correct fact with no source behaves like an unsourced one.

## COGSTOP and the lock system — F-442

### F-442 — `COGSTOP` frees a held lock and leaks its number; the KB said neither — `RESOLVED — applied 2026-09-19; validated by the v1.20.0 release, 2026-09-20`

`p2kbSpin2Cogstop` stated *"Locks owned by cog are NOT released"*, with matching notes and
best-practice lines. The opposite is true of the held state, and the half that actually costs
something was absent entirely.

**Two independent pieces of state, freed by different things:**

| | cleared by |
|---|---|
| the **held** state (taken / by which cog) | the owner's `LOCKREL`, **or the owner cog becoming inactive — for any cause, including `COGSTOP`**, or the lock being unallocated |
| the **allocation** (whether the number is issued) | **`LOCKRET`, and nothing else** |

So stopping a cog that holds a lock frees the lock **and leaks its number**: anyone can now take
it, nobody can ever be issued it again, and after sixteen leaks `LOCKNEW` returns nothing for the
rest of the run — surfacing at some later `LOCKNEW` in code that never touched the lock that leaked.

**The page's advice was right and its reason was wrong.** Release, and more importantly `LOCKRET`,
before stopping — not because the lock would otherwise stay held, but because `LOCKRET` is the only
thing that reclaims the number. Kept the advice, replaced the reason.

**Authority (Stephen, 2026-09-19): his own reading of the hub RTL**, `lock_ena[i] = cog_ena[lock_cog[i]]`
(`hub.sv:670`) with allocation cleared only by `LOCKNEW`/`LOCKRET` (`hub.sv:658-660`), ruled correct
by him in those words — *"the RTL (my reading of the RTL) is correct and we do leak locks."*
Corroborated two ways: the reporting project measured it 3/3 byte-identical with a passing control
and zero inconclusive runs (P2 Edge, 2026-08-31), and **this page already documented half the
consequence** — `LOCKREL … WC` returns *"the cog ID of the current owner (if held) or the last owner
(if released)"*, which is exactly the stale owner field their capture saw.

**None of that provenance is in the YAML**, per his ruling the same day: the entry states the fact,
the register holds how we know it.

**Applied:**
- `language/spin2/methods/cogstop.yaml` — `effects.resources` now carries both halves and the leak;
  the note, best-practice and warning lines give the true reason; `related:` added to
  `architecture/locks.yaml` and `lockret.yaml`, which a reader of this page had no way to reach.
- `architecture/locks.yaml` — new `state_versus_allocation` section, with the rule that every
  `LOCKNEW` needs a `LOCKRET` on every path out including error and shutdown paths.

**Swept the same page's example family (their AMBIGUOUS-7), because it is the same defect:** every
pattern took a hard-coded lock number that `LOCKNEW` never issued, and by this page's own `LOCKTRY`
definition an unallocated lock can never be taken — so `basic_mutex`, `timeout_lock`, `multi_lock`,
`shared_memory_protection`, `resource_arbitration`, `producer_consumer` and
`initialization_synchronization` spin forever as written, and the last never initialises. All now use
an allocated `lock_num`, under a new `pattern_prerequisite` section that states the requirement once
and warns off lock 15 specifically (a DEBUG build holds it).

**Also fixed, same entry:** the first example used `IF driver_cog => 0`. `=>` is P1 syntax and does
not compile in Spin2 — verified, `pnut-ts` exits 1 with *"Expected end of line"*, which does not point
at the operator. Now `>=`, and the example was compiled.

## The P2X8C4M64P handoff, applied — F-443, F-444

### F-443 — the handoff's remaining actionable items, applied — `RESOLVED — applied 2026-09-19; validated by the v1.20.0 release, 2026-09-20`

Each settled against a source this project already holds, not against the report.

- **GAP-8 / AMBIGUOUS-8.** `waitms`/`waitus` claimed *"Internally calculates: WAITX(...)"*. The
  interpreter reads CT, computes the span, **adds the current counter to make an absolute target**,
  and waits via `pwct` — `getct` / `cmpm w,x wc` / `if_c jmp`, the MSB rule. So the `$8000_0000`
  bound exists *because* it is a counter-target wait, and past it the call **returns immediately**
  with no error and no partial wait. The same rule settles `ADDCT1/2/3`, which said the event fires
  *"on CT = D + S"*: it fires once the counter has **passed** the target, so a target in the recent
  past fires at once. Both stated, with the long-wait pattern.
- **AMBIGUOUS-9.** All four signed comparison stubs read *"Signed/unsigned compare"* — the report
  named two; the siblings had it too. The v55 table commits plainly (`spin2-v55-text.txt:472-486`):
  `<`, `<=`, `>=`, `>` signed; `+<`, `+<=`, `+>=`, `+>` unsigned. Each stub now says signed, names
  its unsigned and floating-point siblings, and carries the CON-block rule that relational
  operators return `1.0`/`0.0` on float constants. **Not documented: the PNut-TS constant-fold
  defect** they hit — it is fixed in 1.55.8 and the KB does not carry per-version tool bug state.
- **GAP-6.** `-1` is a legal pin field, derivable from our own ADDPINS encoding: bits [5:0] = 63,
  bits [10:6] = 31, wrapping within the upper port = **P32..P63**. `PINLOW(-1)` acts on half the
  chip. Warned on seven pin methods and on `ADDPINS`, with the guard — and the guard must be a
  **signed** compare, which is where this finding and AMBIGUOUS-9 meet.
- **GAP-5.** `DEBUG_COGS` was documented as an output filter on both definition pages while our own
  `debug_interrupt.yaml` and `pin-capture.yaml` already called it the per-cog debug **interrupt**
  enable. Corrected, with the default-all-eight consequence and the `DEBUG_MASK = 0` distinction.
- **AMBIGUOUS-1 / -2 / -3 / -5.** `X_PINS_ON` and `X_WRITE_ON` are one bit (D[23]); the symbols
  example composed the pin base with `+`, the carry hazard F-361 already cost us; `X_ALT_ON`'s SPI
  advice reached past its own 1/2/4-bit scope; the `%01110` page wrote Y before DIR and used
  `pinstart()`. All corrected — and where no source settles it (whether `%01110` is positively
  immune to an early Y write), the page now says so rather than reasoning to an answer.
- **AMBIGUOUS-4.** `xinit`'s *"may have different effective limits; verify against the Silicon Doc"*
  was unactionable, and the Silicon Doc answers it: `D[15:0]` counts **NCO rollovers**, same
  16-bit field and same `$FFFE` maximum in every mode (`part2-pixel-ops.txt:228-234`). Granularity
  changes data-per-rollover, not the count limit.
- **GAP-4, qualitative half only.** The byte cap fails **silently**, counts the literal format
  strings inside `debug()` plus overhead, does **not** count DAT strings, and is measured by the
  two-compile subtraction. The two budgets have non-overlapping remedies. **Their numeric ceiling is
  not published** — they state it is unbisected and measured by a quantity that may not be what the
  limit counts, and that scope is recorded on the page.
- **GAP-7.** What a `-d` build takes — top 16 KB of hub, `LOCK[15]`, P62/P63, **P62 reconfigured by
  every `debug()`**, cog-start traffic, a debug interrupt per enabled cog, `HUBSET` enables locked
  until reset, `RCFAST`/`RCSLOW` illegal — assembled in one place for the first time. They built
  that list from research we delivered them; it did not exist here.
- **FINDABLE-3.** Aliases added for the words a developer actually arrives with: the compiler's own
  error strings (*"DEBUG data is too long"*, *"within first 16 longs"*), the symptom (*"board prints
  nothing"*, *"mute board"*), and the neighbour-routing phrasings.

**Not applied, and why:** `META-1` (the index version does not move on content change) is reframed
rather than actioned — the index already ships per-entry `mtime` and `sha256` of the git blob, which
is the per-page change signal asked for; the defect is that nothing tells a consumer so. `FIELD-1`
(the ~98 s-per-character stall) is declined: they offer it as a question and we have no mechanism
either. Both recorded in the triage.

### F-444 — a `count_field` block closed the `instructions:` map, and `GETXACC` fell inside it — `RESOLVED — found and fixed 2026-09-19; validated by the v1.20.0 release, 2026-09-20`

Mine, and it shipped in v1.19.1/v1.19.2. Adding `count_field:` at column 0 between `XSTOP` and
`GETXACC` in `architecture/streamer/overview.yaml` **closed the `instructions:` mapping**, so
`GETXACC` became a child of `count_field` and left the instruction list an agent reads:

    instructions: [SETXFRQ, XINIT, XCONT, XZERO, XSTOP]        <- GETXACC gone
    count_field:  [location, terminating, perpetual, ..., GETXACC]

**Every gate passed.** The file parses, every cross-reference resolves, the DoD suite is green — the
YAML is *valid*, it is just wrong about what the streamer's instructions are. No instrument we have
reads meaning.

**Found by sweeping my own session's edits** for the defect class after catching this one by eye,
comparing every file's top-level key set at `v1.18.2` against now. Six files lost a top-level key;
**five were deliberate** and documented (F-429's *"22 examples removed because the code was never
there"*, F-427's unsourced-content purge). This was the only accident.

**The gate this argues for:** a structural diff at release — a top-level key that disappears from a
published entry should have to be declared, the way a removed cross-reference already is.

### F-435 — the ABORT entries teach that a trapped call returns the method's result; it returns 0 — `RESOLVED — applied 2026-09-17; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

`language/spin2/constructs/abort.yaml` `trap_operator.expression_context` says `result := \method()`
returns *"the method's normal return value (if no ABORT)"*. It does not. The value trap discards the
method's results and supplies **0** on normal completion, so the only values a trap can produce are
the abort value and 0.

**Confirmed from our own ingestion tree, not from the request.** The Spin2 interpreter source we
hold (`engineering/ingestion/external-inputs/source-code/spin-interpreter/v51/Spin2_interpreter.spin2`)
states the return path as a case table over the frame's two flags, at `:1385-1389`:

```
'  case {trap_flag, push_flag}
'    %00: restore caller stack
'    %01: return (Z ? stack_args : results)
'    %10: restore caller stack
'    %11: return 0
```

and implements it at `:1399-1401` — `rczr pbase wcz` / `if_c_and_z mov v,#0`. `%11` is exactly a
*value* trap (trap_flag AND push_flag): return 0. Only `%01` — push without trap — returns results.
The request cites the v55 interpreter; we hold v51 and it already says this, which makes the two
readings independent. **Compiler corroboration:** `pnut-ts` v1.55.5 accepts `v := \no_results()` for
a method declaring **no** results — meaningless if results passed through a trap.

**Second defect, same entries.** `propagation_behavior` and `anti_patterns.uncaught_abort` say an
untrapped ABORT *"terminates the program"*. It ends the **task**, or the cog when no other task runs
in it; other cogs continue. Same source: `launch_method` sets the trap flag on every cog/task top
frame (`:1997`, `or pbase,#%10`) with the frame's return pointer documented as `@TASKSTOP()`
(`:1972`), and the abort handler pops *"while !trap_flag"* (`:1446`, `:1459-1460`) — so it lands on
that pre-set trap rather than running off the bottom.

**Blast radius — this is the agent-consumer failure mode, not a wording nit.** Five of the entry's
six `patterns` are built on the false premise and are wrong as written (`error_code_pattern`'s
`safe_operation`, `try_finally_pattern`, `retry_pattern`, `graceful_degradation`,
`resource_cleanup`), as is the `expression_context` example itself. An agent that emits
`level := \read_level()` gets 0 on every success and nothing says so. A fourth gap: bare `ABORT` and
`ABORT 0` cannot be told from success by value, and the entries never say to use non-zero codes.

**Where it came from.** `abort.yaml`'s own header names its source: *"Spin2 v51 documentation,
pnut_ts Error-Handling-Usage-Guide.md"*. The usage guide carried the same two errors and has been
corrected upstream. This is [[feedback_upstream_input_docs_not_authority]]'s exact shape — a
usage-guide claim carried into the KB without probing the interpreter.

**Applied:** `expression_context`, `propagation_behavior.description`, `return_vs_abort.ABORT`, the
`patterns` block, `anti_patterns.uncaught_abort` + a new `reading_result_through_trap`,
`error_handling_strategy.top_level`, and the whole `behavior`/`trap_operator`/`notes` of
`language/spin2/keywords/ABORT.yaml`. Every replacement example compiled with `pnut-ts -d` before
shipping — which caught one defect in the request itself: its `supervise_a_cog` example calls an
undefined `worker_body()` and does not assemble (`Expected a method, object, or variable`). Given a
body here rather than shipped broken.

### F-437 — `validation_chain` swallowed every failure it claimed to catch — `RESOLVED — found and fixed 2026-09-17 while applying F-435; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

Found while fixing F-435, and **not** part of that request — the upstream doc proposed dropping this
pattern rather than correcting it, so a straight application would have removed the evidence without
recording the defect. `abort.yaml`'s `validation_chain` read:

```
PUB validate_all(data) : valid
  \validate_range(data)
  \validate_checksum(data)
  \validate_format(data)
  valid := TRUE                ' All passed
```

described as *"Run multiple validations, fail on any."* It does the exact opposite. Each bare `\`
is an **instruction-context** trap: it catches the abort, discards the value, and execution
continues on the very next line — so a failing `validate_range` is swallowed, the remaining
validations still run, and `valid := TRUE` always executes. The pattern reports success on every
input, including the ones it exists to reject.

Distinct from F-435: that one is *results do not pass a trap*; this one is *an untested trap is a
silent catch*. A reader could absorb F-435's correction completely and still write this.

**Applied:** pattern rewritten to test each trap and return early, and the rule stated in the
pattern's own description so the shape is named where someone would copy it. The related caution is
now on `trap_operator.instruction_context` too, which previously read only "Result is discarded."
Compiled with `pnut-ts -d` before shipping.

### F-438 — the preprocessor entry states pre-1.55.8 `-D` behaviour as fact — `RESOLVED — fixed 2026-09-19; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

Found by sweeping the KB for what the 1.55.8 upgrade invalidates, which is the half of an upgrade
nobody is prompted to do. `language/spin2/preprocessor/external-symbols.yaml:278` read:

> *"There is NO -D symbol=value form in either compiler. PNut-TS accepts the text without complaint
> and defines NOTHING — pnut_ts -D VERS=200 leaves VERS undefined, with no diagnostic."*

True when written against v1.55.3 (F-235). **False from 1.55.8**, measured here on the release
binary — v1.55.5 for contrast, both run on the same source:

| | v1.55.5 | v1.55.8 |
|---|---|---|
| `-D VERS=200` | exit **0**, no diagnostic, symbol undefined, `p.bin` written | `ERROR- -D VERS=200 is not supported; -D takes a presence-only symbol name (use -D VERS)`, exit **1**, **no output file** |
| `-D 9BAD` / `-D BAD-NAME` | accepted | rejected, exit 1 |

**The durable half of the entry was right and stays**: there is still no value-carrying
command-line define in either compiler, and the symbol is still presence-only. What changed is that
the attempt is now diagnosed instead of ignored, so the sentence describing the silence had to go.
Rewritten to state the rejection and its message, with the old silence named as what an older
compiler does — not as three version eras (**cite the edition, never the build**).

**Same sweep, nothing else exposed:** no `.spin2` in the repo uses `#if`/`#elseif` (now an error), no
script passes `-D SYM=value` to the compiler, and nothing in `engineering/tools/` or the skills parses
a `.map`. The two open items on `DRAFTS/PNUT-TS-PUNCH-LIST.md` are both fixed by this release and
were moved to *Shipped* with the evidence.

## The first run of the full cross-reference gate (2026-09-13) — F-432, F-433, F-434

### F-434 — 246 references in the served KB did not resolve once every string and every depth was read — `RESOLVED — 242 repaired 2026-09-13; 2 held for the F-429 pass; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

What the F-340 gate found on its first full run, by kind: **217** paths written short (a bare
`calld.yaml`, a partial `groups/counter_event_jumps.yaml`) that an agent cannot follow as written;
**18** paths to files that do not exist; **8** root-prefixed (`/deliverables/ai/P2/…`); **3** `../`
relative. Plus, from the nested reference walk before it: prose document titles sitting in hardware
`documentation.related` lists, a `"WAITX instruction"` where a path belonged, and three
`combines_with` entries written as `name: description`.

**Repairs (Sacred Rule #7 — every reference redirected, none dropped):**
- **225 short / relative / root-prefixed paths in 97 files** rewritten to their full KB path, mapped
  only where the target was unique (the containing directory, or a basename held by exactly one
  file); every file re-parsed clean after.
- **Ambiguous by hand:** `architecture/locks.yaml` "per `lockrel.yaml` encoding" (PASM2 and Spin2
  both have one — the clock counts are the PASM2 encodings) → `language/pasm2/lock*.yaml`;
  `debug-displays/*` `statements/debug.yaml` → `language/spin2/statements/debug.yaml`.
- **Shorthand that named no file:** `reti1/2/3.yaml` and `resi1/2/3.yaml` (`architecture/cog.yaml`,
  `architecture/interrupts.yaml`) → `language/pasm2/reti1.yaml` (likewise reti2, reti3) etc.;
  `fundamentals-manifest.yaml` (a retired scheme) → the `language/fundamentals/` directory, with the
  retirement stated.
- **Wrong field, not wrong text:** seven hardware files' `documentation.related` held external
  document titles ("P2 Silicon Documentation", vendor datasheets) — moved to `references:`, and where
  the title named a KB entry ("Edge module documentation") a real `related:` path added.
  `waitms`/`waitus` `related_pasm` → `language/pasm2/waitx.yaml`; `asm_integration_analysis.yaml`
  `combines_with` → the three `*_analysis.yaml` paths, descriptions kept as comments;
  `object_archetypes.yaml` → `architecture/cog.yaml` (its `cog-ram-organization.yaml` never existed).
- **Two files that were never knowledge:** `language/pasm2/concepts/additional_concepts_needed.yaml`
  (`category: planning`) and `manual_category_alignment_check.yaml` (`category: validation`) are
  internal gap analyses naming nine planned files that do not exist, and asserting gaps since
  closed (CORDIC is documented). No file referenced either. **Moved out of the served tree** to
  `engineering/operations/archive/kb-planning-artifacts-2026-09-13/` — kept, not deleted.
- **Neighbourhood, same pass:** `language/pasm2/idioms/hub-memory.yaml` said a SETQ block read moves
  "up to 16 longs" and is "atomic from the hub's perspective"; the Silicon Doc states no 16-long cap
  and says the hub FIFO takes priority and the block move **waits** (`silicon-doc-text.txt:3257`) —
  the opposite of atomic. Replaced with the source's rule; the `flash_loader.spin2 lines 148-151`
  citation, attached to a cog-register example the loader does not contain, now sits only on the
  LUT-chained pattern those lines actually are (`sources/flash-loader/flash_loader.spin2:148-152`).

**Held:** `language/pasm2/concepts/event_interrupt_config.yaml` (`calld.yaml`) and
`language/pasm2/xinit.yaml` (`streamer_smartpin_control.yaml`) — both files are being edited by the
F-429 pass; repaired when it lands.

### F-432 — debug-ISR examples use `IJMP0`/`IRET0` as register names, which do not assemble — `RESOLVED — fixed 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

The Silicon Doc names them, but as roles: *"During a debug ISR, INA and INB … become readable/writable
RAM registers named IJMP0 and IRET0"* (`silicon-doc-text.txt:2423`). `pnut-ts` v1.55.5 has no such
symbols — `MOV IJMP0, #5` → `Undefined symbol`, while `MOV INA, #5` assembles. So
`architecture/debug_interrupt.yaml`'s `execution_tracer` and target-handler examples could not
assemble. **Fixed:** the code writes `INA`/`INB`, each commented with the IJMP0/IRET0 role it plays
inside the ISR. Prose that *names* the roles is correct and unchanged. Found by the F-430 pass.

### F-433 — `spin2-pasm2-integration.yaml` teaches Propeller 1 code as P2 — `RESOLVED — all 13 examples repaired and compiling 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13 (dispatched, arbiter-verified by re-extracting and compiling every example:
> 13/13 clean under `pnut-ts` v1.55.5).** Compiling the whole file widened the finding from two P1
> constructs to **every one of its 13 examples but one**: `WAITCNT`/`cnt` → the P2 periodic-timer idiom
> `GETCT`/`ADDCT1`/`WAITCT1`; `MOV ptra, par` removed, since COGINIT's third argument arrives in the new
> cog's PTRA (`spin2-v55-text.txt:517`), with the missing `ORG 0` added; bare `_RET_` (a condition
> prefix, not an instruction, `silicon-doc-text.txt:858-861`) → `RET`, in four examples and in the
> constructs list; `CALL(#$080)` (crashes the compiler) and `result := CALL(...)` (CALL is a statement
> and blocks until RET, `spin2-v55-text.txt:556`) rewritten around a real label call — the "start it,
> let it run, stop it" narrative was impossible for a blocking call and was replaced; `WAITUS` used as a
> PASM2 instruction → `WAITX`; `IF … THEN` (Spin2 has no `THEN`); an invented `point.FIELD[LONG][x, y]`
> syntax → a real `{Spin2_v45}` `STRUCT` (`spin2-v55-text.txt:147`); `#1000` and `#-1` immediates past
> the 9-bit range → `##`; undefined `result`/`temp`/`complexMath`; trailing-colon labels; and an
> interrupt example whose PASM handler wrote to hub address 0 because the Spin2 side never passed
> `@shared_flag` — the file's own `hub_address_resolution` gotcha, now demonstrated rather than
> violated. `COGINIT(16, …)` now reads `COGINIT(COGEXEC_NEW, …)`.

Its cog-startup example waits with `WAITCNT cnt, ##160_000_000` and writes `MOV outa, cnt`; the next
example reads its parameter with `MOV ptra, par`. `WAITCNT`, `cnt` and `PAR` are Propeller 1; P2 has
none of them (`pnut-ts` rejects `WAITCNT`), and a P2 cog receives its parameter in PTRA/PTRB via
COGINIT (`silicon-doc-text.txt:370-415`). Found by the F-430 pass's compile check. Every example in
the file is being compiled and repaired source-first.

## Five clock "built-in symbols" that Spin2 does not have — found by measuring what F-340's nested walk would report (2026-09-13) — F-431

### F-431 — `spin2-builtin-symbols-complete.yaml` ships five clock constants with invented values; the compiler rejects every one — `RESOLVED — fixed 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13, source-first.** The five clock entries deleted, substituting nothing; no
> `XDIV`/`XMUL` name remains anywhere in the KB. **Widened:** the same file's event section defined
> only three of Spin2 v55's seventeen event/interrupt symbols, and one of the three was wrong —
> `EVENT_INT` described as a "Pin edge/level interrupt event", where v55 says *"Interrupt-occurred
> event or interrupts off"*. The section was **rebuilt from the v55 table**
> (`spin2-v55-text.txt:1638-1656`): all 17 names (`EVENT_INT`/`INT_OFF`, `EVENT_CT1..3`, `EVENT_SE1..4`,
> `EVENT_PAT`, `EVENT_FBW`, `EVENT_XMT`/`XFI`/`XRO`/`XRL`, `EVENT_ATN`, `EVENT_QMT`), value = the table's
> number, description = the table's text, scoped PASM per its heading; the unsourced
> `usage_context`/`hardware_relationship` flavour text was not carried. `pnut-ts` accepts all 17 and
> rejects a planted `EVENT_NOT_REAL`.

**How it was found, which is the point.** Stephen asked what a full cross-reference check would take
(F-340). Running a scratch copy of `validate-crossref-keys.py` with the nested walk enabled reports
**40** unresolved references the shipped validator cannot see. Six of them are `related_symbols`
entries naming `XDIV1`/`XDIV2`/`XDIV4`/`XMUL2`/`XMUL3`/`XMUL4` — and chasing those showed the file does
not merely *reference* invented names, it *defines* some. **Exactly F-338's shape, in the same file,
in the same field the validator does not read.**

**Sites** — `language/spin2/symbols/spin2-builtin-symbols-complete.yaml`, block `# Clock Setup Symbols`:
`RCFAST` (`:1784`, value `$0000_0000`), `XI` (`:1796`, `$0000_0001`), `PLL` (`:1808`, `$0000_0002`),
`XDIV1` (`:1820`, `$0000_0000`), `XMUL2` (`:1832`, `$0000_0040`), plus `related_symbols` naming the
further non-entries `RCSLOW`, `XDIV2`, `XDIV4`, `XMUL3`, `XMUL4` (`:1792`, `:1804`, `:1816`, `:1828`, `:1840`).

**Evidence, three ways.**
- **Compiler:** `pnut-ts` v1.55.5 rejects all five as `CON x = NAME`. **Controls:** it accepts `P_ADC`
  and `CLKFREQ_` and rejects `NOT_A_SYMBOL`, so the harness discriminates.
- **Spin2 v55:** `XDIV1`/`XMUL2` appear **0** times. `RCFAST`, `XI` and `PLL` appear only as *words* —
  "internal RCFAST oscillator", "XI/XO-crystal-plus-PLL mode" (`spin2-v55-text.txt:1711-1719`,
  `:1740`, `:899`) — never as constants. Spin2's clock is configured by the `_clkfreq`, `_xtlfreq`,
  `_xinfreq`, `_errfreq`, `_rcfast`, `_rcslow` CON symbols and read back through `clkmode_`/`clkfreq_`
  (`:1711-1725`).
- **The values have no source.** No Parallax document assigns `XI = 1`, `PLL = 2` or `XMUL2 = $40`.

**Correction (source-first).** Delete the five entries and the `related_symbols` that name them,
**substituting nothing** — per F-338, a substitution would be an inference about what the author
meant. Clock setup is already documented from source in
`language/spin2/constants/special-configuration-symbols.yaml`; any inbound reference is redirected
there (Sacred Rule #7). Then sweep the **whole file** for the class, not these five: its 135-plus
nested records were never read by any gate until F-340's walk lands — which is the argument for
landing it.

## Two KB-wide classes surfaced by the LUT fix, carved out because each needs its own per-site pass (2026-09-13) — F-429, F-430

Both were found while applying F-422/F-427 and **fixed inside the LUT neighbourhood**; what remains is
outside it. Carved out, named here, rather than folded into a LUT change: each touches 13-14 files
nobody asked about, and each needs a per-site read (F-429) or a YAML-aware edit (F-430) — a text
regex for F-430 would also match YAML mapping keys.

### F-429 — `source:` provenance labels in 14 KB files name programs that do not contain the code, or name no file at all — `RESOLVED — 43/43 sites repaired 2026-09-13 (dispatched, arbiter-verified); validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13.** All 43 sites across the 14 named files resolved source-first (open the
> named file, search for the distinctive instruction sequence, cite or replace/remove — never
> cite-in-place). **21 grounded (cited to real `file:line`, code replaced with the file's actual
> lines where the KB's version differed in meaning) · 22 removed (label named no file, or the
> named file's real code did not match the claimed mechanism) · 0 gaps.** Evidence widened past
> the 3 originally-confirmed fabrications: `pasm2/event_interrupt_config.yaml`'s five
> `Spin2_debugger.spin2`-labeled examples (SETINT3/IJMP3/RETI3-based "debug ISR" patterns) were
> all fabricated — `SETINT3`, `IJMP3`, `RETI3`, and `BRK_EVENT` never appear anywhere in
> `Spin2_debugger.spin2`; P2's BRK-triggered debug interrupt is a separate hardware channel from
> the cog INT1-3 mechanism the examples invented. Similarly `multi_cog_synchronization.yaml`'s
> "singleton debug monitor" pattern (never-release-the-lock, elect-one-monitor-cog) does not
> match the real mechanism (a lock held briefly by whichever cog is mid-debug-interrupt, released
> on exit). Two per-instruction YAMLs (`altgb.yaml`, `smart_pin_patterns.yaml`) had a motor-
> commutation / quadrature-decoder example matching the earlier LUT-pass finding's pattern:
> plausible-sounding code the named file does not contain. Grounded citations point at
> `engineering/ingestion/sources/flash-loader/flash_loader.spin2`,
> `engineering/ingestion/external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2`, and
> `engineering/ingestion/external-inputs/source-code/external-projects/P2-BLDC-Motor-Control/src/isp_bldc_motor.spin2`
> (the OBEX-2874 copy of `isp_bldc_motor.spin2` is a 0-byte placeholder — the external-projects
> copy is the only one with content). `cog_hub_execution.yaml`'s bare-filename
> `per_instruction_yamls` reference entry was rewritten to full KB paths in the same pass.
> Verified: `verify-yaml-format.py` clean on all 14 files; `validate-crossref-keys.py` shows the
> same pre-existing 15 unresolved references present before this pass (none introduced by it).
>
> **Arbiter verification, 2026-09-13.** Status set to `PENDING-VALIDATION`, not `DONE`: the fix is
> applied, the served KB is not yet released. Every example now carrying a `.spin2` citation was
> checked mechanically — each code line, whitespace-insensitive, looked up in the cited source line
> range ±3: **26 code blocks, 25 match**; the one miss was a scope artefact (a generic
> `SETQ #31` example sharing a node with the debugger excerpt the citation belongs to) and the key
> was renamed `debug_use_source` so the citation cannot be read as covering the generic example.
> No bogus label remains anywhere in the KB (the finding's grep returns 0). The dispatched agent
> ran `git stash`/`git stash pop` mid-pass with other repairs in flight; every concurrent edit was
> checked present afterwards. **Two unlabeled blocks it flagged but did not own** —
> `cog_hub_execution.yaml` `overlay_table_structure`/`overlay_management` — describe an overlay
> table and a 32/128-long overlay layout the Spin2 debugger does not have (its overlays load with one
> `SETQ #overlay_end-overlay_begin` + `RDLONG overlay_begin,pb`,
> `spin-debugger/v51/Spin2_debugger.spin2:382-384`); removed in the same pass, source-first.

**The class.** Example blocks carry a bare `source:` naming where the code came from. Seven label
values recur: four name **no file anywhere** — `waveform_generation`, `audio_processing`,
`motor_control`, `data_processing` — and three name real files held in ingestion —
`isp_bldc_motor.spin2` (`external-inputs/source-code/obex-projects/2874-ISP_BLDC_Motor_Control/`),
`flash_loader.spin2` (`sources/flash-loader/`) and `Spin2_debugger.spin2`
(`external-inputs/source-code/spin-debugger/v51/`).

**Why the real-file labels are not evidence either.** The two checked in the LUT pass were both false:
the motor-commutation LUT example credited to `isp_bldc_motor.spin2` — a file with no LUT instruction in
it — and a "debug trace" example credited to `Spin2_debugger.spin2` that is not the debugger's code. A
label naming a real file is a claim, and 2 of 2 checked were wrong.

**Sites** (measured 2026-09-13, after the LUT fixes; `grep -rn -E '^\s*source: (waveform_generation|audio_processing|motor_control|data_processing|isp_bldc_motor\.spin2|flash_loader\.spin2|Spin2_debugger\.spin2)\s*$' deliverables/ai/P2`):
- **No such file (CONFIRMED):** `pasm2/rdfast.yaml:55` (`audio_processing`), `pasm2/altgb.yaml:90` (`waveform_generation`), `architecture/smart_pin_patterns.yaml:187` (`motor_control`).
- **Names a real file — verify:** `pasm2/xinit.yaml` 37, 54, 72 · `pasm2/rdfast.yaml` 46 · `pasm2/brk.yaml` 24, 43 · `pasm2/wypin.yaml` 47, 62, 79, 91 · `pasm2/altgb.yaml` 72 · `pasm2/locktry.yaml` 47 · `pasm2/lockrel.yaml` 51 · `pasm2/testp.yaml` 59 · `pasm2/concepts/setq_block_ops.yaml` 71, 158, 200 · `pasm2/concepts/multi_cog_synchronization.yaml` 117 · `pasm2/concepts/cog_hub_execution.yaml` 157, 278, 301 · `pasm2/concepts/event_interrupt_config.yaml` 59, 120, 138, 155, 334 · `architecture/smart_pin_patterns.yaml` 27, 45, 65, 169, 249 · `pasm2/concepts/streamer_smartpin_control.yaml` 39, 100, 112, 157, 193, 232, 284, 320, 342.

**Correction (source-first).** Per site, open the named file and find the code. Present → cite it by
path and line, as `setq_block_ops.yaml`'s debugger loop now does. Absent → remove the example; if the
concept needs one, re-derive it from the named file's real code or from a Parallax source. **Never
re-label an example in place with a plausible source** — that is the claim-first repair
`SOURCE-REPAIR-ORDER.md` exists to stop.

### F-430 — PASM2 labels written with a trailing colon do not assemble: 70 lines in 13 KB files — `RESOLVED — 76 labels fixed in 16 files 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13 (dispatched, arbiter-verified).** Every changed line diffed against `HEAD`:
> colon-only, line counts unchanged. The filing's counts were a heuristic and were wrong both ways:
> **widened** in `cog_attention.yaml` (10→12), `debug_interrupt.yaml` (7→8), `interrupts.yaml` (3→6),
> `stack_operations.yaml` (2→3); **false positives** in `dual_communication.yaml` (all 10 are Spin2
> `CASE` branch labels, legal) and `p2-source-file-organization-standard.yaml` (MIT licence text).
> A tree-wide rescan found the class **outside the filed list**: `pasm2/groups/interrupt_resume.yaml`
> and `interrupt_return.yaml` (fixed — their example also used `;` comments, which Spin2 does not
> have, now `'`, compiled clean), and `pasm2/concepts/event_interrupt_config.yaml` (4),
> `pasm2/concepts/multi_cog_synchronization.yaml` (3), `pasm2/testp.yaml` (1) — fixed once the F-429
> pass on those files landed, each edit verified by parsing the file before and after and requiring
> the two documents to be identical except for the removed colons.

`pnut-ts` v1.55.5 rejects both `label:` and `.label:` in a `DAT` block — `Expected a unique name, BYTE,
WORD, LONG, or assembly instruction` — so every code block carrying one fails at its first label. PNut
is the compiler this KB targets. Measured 2026-09-13 by parsing each YAML and scanning only multi-line
strings that contain PASM2 mnemonics, after `lookup_ram.yaml`'s four were fixed under F-427:

`spin2/integration/spin2-pasm2-integration.yaml` 21 · `architecture/cog_attention.yaml` 10 ·
`spin2/patterns/applications/dual_communication.yaml` 10 · `architecture/debug_interrupt.yaml` 7 ·
`architecture/event_system.yaml` 6 · `architecture/locks.yaml` 4 · `architecture/interrupts.yaml` 3 ·
`pasm2/concepts/execution_modes.yaml` 2 · `pasm2/concepts/stack_operations.yaml` 2 ·
`spin2/constructs/repeat.yaml` 2 · `architecture/xbyte_engine.yaml` 1 · `spin2/constructs/case.yaml` 1 ·
`spin2/conventions/p2-source-file-organization-standard.yaml` 1.

**Correction:** drop the colon from each label, then compile each touched block. Edit YAML-aware (locate
the line through the parsed string), never with a line regex over the raw file: `^\s*\w+:\s*$` is
also the shape of a YAML mapping key. **Check the scan's scope first** — a block that is Spin2 rather
than PASM2, or one written for a different assembler on purpose, is not a defect; confirm per file.

## LUT memory — code that does not assemble, content nobody sourced, and three sourced facts the LUT page never carried (2026-09-13, LUT app-note research) — F-422, F-427, F-428

Found while researching whether LUT memory deserves its own app note. Stephen chose **option A**:
no LUT app note; route every gap to the document that owns it (the stand-alone note is parked on
`document-production/PUNCH-LIST.md`, the silicon questions are **VO-J-006**). F-359 re-derived
`architecture/lookup_ram.yaml`'s header, encodings and sharing direction on 2026-08-26; **it did not
reach the file's patterns, performance or applications sections**, and this batch is what was left.
Every code verdict below was compiled with `pnut-ts` v1.55.5 — which proves **legality only**; the
semantic verdicts cite their sources.

### F-422 — LUT code in four KB files and the Assembly manual does not assemble, or states the wrong prefix, literal range or timing — `RESOLVED — KB and manual source fixed 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13.** Every site in the table below corrected to its source. The class sweep run
> while fixing **widened** it by three sites the filing did not carry, all the same defect:
> `pasm2/setq2.yaml` notes ("LUT access is single-cycle"), `pasm2/concepts/setq_block_ops.yaml`
> (`lut_advantage` "single-cycle", and a `performance` block of transfer rates no source states —
> "2 + N cycles", "10-20x faster than a loop" — replaced by the Silicon Doc's "one long per clock"
> rule, `silicon-doc-text.txt:3257`), and `pasm2/concepts/streamer_smartpin_control.yaml` ("Single-cycle
> LUT access", removed). Assembly manual §1.3.2 now teaches `SETQ2 #count-1` + `RDLONG 0, hubaddr` and
> names the `0`-not-`$200` pitfall. **Verified:** every code block remaining in
> `architecture/lookup_ram.yaml` compiled together clean under `pnut-ts` v1.55.5; the replacement
> block-load, dump, event and pair-start forms each compiled; all 10 edited YAMLs parse; cross-refs
> resolve.

| Site | Says | Verdict | Source / proof |
|---|---|---|---|
| `architecture/lookup_ram.yaml:105`, `:123` | `S may be an immediate #0..#511` | **Wrong** — a literal LUT address reaches `#0..#255` | `RDLUT r0,#256` and `#511` → `Constant must be from 0 to 255`. The Assembly manual already states it (`part-i/chapter-01-execution-model.md:101`, `part-ii/instructions-r.md:325`, `instructions-w.md:714`). |
| `lookup_ram.yaml:127`, `:341` | `WRLUT #$12345678, …` | **Does not assemble** | `Constant must be from 0 to 511 (m130)`; `WRLUT ##$12345678, r0` assembles. |
| `lookup_ram.yaml:197` | `CMP index, #512 WZ` | **Does not assemble** | `Constant must be from 0 to 511 (m130)`. |
| `lookup_ram.yaml:179`, `:335`; `pasm2/concepts/execution_modes.yaml:192`; `pasm2/idioms/hub-memory.yaml:71` | `RDLONG $200, …` / `WRLONG $200, …` after `SETQ2` | **Does not assemble** — the block form addresses the LUT as `$000..$1FF` | `Register cannot exceed $1FF`; `SETQ2 #127` + `RDLONG 0, r1` assembles. Silicon Doc: `RDLONG first_lut,S/#/PTRx` (`silicon-doc-text.txt:3264-3267`, `:3278-3281`). `pasm2/concepts/setq_block_ops.yaml:97` already has it right (`rdlong 0, ptra`). |
| `pasm2/concepts/execution_modes.yaml:187-189` | `to_cog:` → `SETQ2 #511` / `RDLONG 0, hub_addr ' Load cog RAM from hub` | **Wrong prefix** — `SETQ2` loads the **LUT**; `SETQ` loads register RAM | `silicon-doc-text.txt:3257-3267`. |
| `pasm2/concepts/setq_block_ops.yaml:99` | `rdlut value, phase ' Single-cycle lookup` | **Wrong** — `RDLUT` is 3 clocks | P2 Datasheet `p2-datasheet-text.txt:2061`. |
| `architecture/event_system.yaml:514` | interrupt source `13=LUT $1FF read` | **Drops the subject** — it is the *streamer's* read, not a cog's `RDLUT` | `silicon-doc-text.txt:2289`: `13 Streamer read location $1FF of lookup RAM`. |
| Assembly manual `part-i/chapter-01-execution-model.md:103` | load the LUT from hub "using `SETQ` for burst transfers" | **Wrong prefix** — `SETQ2` | `silicon-doc-text.txt:3264`; the same manual's `part-ii/instructions-r.md:284` states it correctly. |

**Correction:** align each site to its source. The two block-load examples take the Silicon Doc's own
`SETQ2`+`RDLONG first_lut` / `SETQ2`+`WRLONG first_lut` forms. Class sweep run 2026-09-13 across
`deliverables/ai/P2/`, every `manuals/*/opus-master/` and `app-notes/` for `#0..#511` LUT claims,
`RDLONG`/`WRLONG`/`WMLONG $200`/`$3FF`, over-range `#` immediates on LUT code, and `SETQ` used for a LUT
load; the sites above are all it returned. (`xbyte_engine.yaml:253` and Assembly manual
`appendix-b-condition-codes.md:143,146` use `_RET_ SETQ` to set the **XBYTE** LUT base — a different,
correct use, per `silicon-doc-text.txt:969`.)

### F-427 — `lookup_ram.yaml` carries content no source states, some of it contradicting the file itself; the Assembly manual carries one such claim — `RESOLVED — removed/re-derived 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13, source-first** (`SOURCE-REPAIR-ORDER.md`). Removals: `shared_read`, bandwidth,
> power, `FIFO_mode`, the `waveform_generation`, `fast_buffer` and `fast_stack` patterns, the
> `common_applications` benefit bullets, and "FIFO buffers" from the description. Re-derived from
> source: the `lookup_table` load, `lut_dump`, a `uses:` list taken from the datasheet's own
> enumeration (`p2-datasheet-text.txt:596-601`), and a source for `LUT_to_DAC_streaming`
> (`silicon-doc-text.txt:159`). The waveform pattern was **deleted, not rebuilt** (Stephen,
> 2026-09-13) — its sourced home is `architecture/streamer/dds-goertzel.yaml`, now linked. Two
> defects the filing missed, fixed in the same pass: the four `label:` lines in the file's own
> patterns do not assemble (`pnut-ts` rejects the colon — the class is **F-430**), and the bare-name
> `related_topics` block became a full-path `related:` block (Sacred Rule #7: redirected, none dropped).
> **The same fabricated-example class sat in the LUT neighbourhood and was fixed with it:**
> `pasm2/setq2.yaml` and `pasm2/concepts/setq_block_ops.yaml` each carried a motor-commutation LUT
> example that indexes the LUT as if it held bytes ("8 bytes per state") and credits
> `isp_bldc_motor.spin2`, which contains **no** `SETQ2`, `RDLUT`, `WRLUT` or `SETLUTS` at all — removed;
> and a "debug trace" example credited to `Spin2_debugger.spin2`, which is not the debugger's code —
> `setq_block_ops.yaml` now carries the debugger's actual `SETQ2` block loop
> (`spin-debugger/v51/Spin2_debugger.spin2:151-162`, compiled clean), `setq2.yaml`'s copy was removed.
> Invented `source:` labels on the two surviving LUT examples now cite the Silicon Doc mechanism. The
> rest of that provenance class, outside LUT, is **F-429**. Assembly manual §1.3.1: the CORDIC sentence
> removed; the paletted-display sentence kept (sourced). **Line budget:** `lookup_ram.yaml` is 356
> lines against the 200-line ceiling for an architecture entry — down from 379, still over; a split is
> not in this finding's scope.

| Site | Claim | Why it goes |
|---|---|---|
| `lookup_ram.yaml:298` | `shared_read: "3 clock cycles"` | **Contradicts `:58-59`** of the same file ("there is no instruction that reads another cog's LUT"). |
| `lookup_ram.yaml:300-306` | `bandwidth.streaming: "32 bits per clock"`, `power_consumption` | No source. |
| `lookup_ram.yaml:90-92`, `:348-349` | `FIFO_mode` "can be used with hub FIFO"; "LUT often used with hub FIFO" | No source. |
| `lookup_ram.yaml:187-204` (`waveform_generation`) | `WXPIN #512, #0 ' 512 samples`, `XINIT lut_stream_mode` | No source ties `WXPIN` to a streamer sample count, and the streamer's LUT window is **eight selectable sizes, not a flat 512** (F-302; `silicon-doc-text.txt:1586-1600`). Also carries F-422's `#512`. |
| `lookup_ram.yaml:226-260` (`fast_buffer`, `fast_stack`) | a LUT circular buffer and stack | No source. Mixes cog-space `$200`/`$2FF`/`$3FF` into `RDLUT`/`WRLUT` addressing, which is `$000..$1FF` (`:30`); `MOV buffer_ptr, #$200` → `Constant must be from 0 to 511 (m130)`. |
| `lookup_ram.yaml:262-292` (`common_applications`) | benefit bullets such as "Smooth, high-frequency waveforms", "No hub bandwidth needed" | No source for the bullets. |
| `lookup_ram.yaml:380` | `last_updated: "2024-12-30"` | The file was re-derived 2026-08-26 (its own `:369-370`). |
| Assembly manual `chapter-01-execution-model.md:95` | "The LUT integrates with the P2's streamer and **CORDIC** subsystems … **CORDIC operations can store results in LUT memory**" | No source links CORDIC to the LUT. A CORDIC result reaches the LUT only as any value does, through `WRLUT`. The paletted-display sentence that follows **is** sourced (8-bit values offset into the LUT at base `%bbbb00000`, `silicon-doc-text.txt:1464`, `:1472`) and stays. |

**Correction:** delete the unsourced content outright — this project does not keep a claim no source
states, and a pattern that does not assemble cannot be "illustrative". The sourced remainder
(`lookup_table` with the corrected block load, `shared_data_exchange`, `lut_dump` corrected,
`verify_sharing` with `##`) stays.

### F-428 — three sourced LUT facts are missing from the page a reader goes to for LUT memory — `RESOLVED — added 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **Applied 2026-09-13.** `architecture/lookup_ram.yaml` gains `special_features` `spin2_lut_area`,
> `LUT_events` and `pair_start`, each with its source, and `related:` full paths to
> `spin2/constructs/inline_pasm.yaml`, `pasm2/setse1.yaml` and `pasm2/coginit.yaml`. Findability, in the
> same pass: the file had **no `aliases:`** (the index harvests aliases, not keywords), so "LUT", "LUT
> RAM", "Lookup RAM", "LUT sharing" and the datasheet's "Paired-Cog communication mechanism" resolved to
> nothing — added, collision-checked against the index first; `rdlut.yaml`, `wrlut.yaml` and
> `setluts.yaml` had no `related:` back to the LUT page — added. Assembly manual: §1.3.2 gains the
> Spin2 16-long paragraph, §1.3.3 the `COGINIT` pair start and the `SETSE` handshake.

Not wrong: **absent where they are needed.** Each is carried elsewhere in the KB, but neither
`architecture/lookup_ram.yaml` nor Assembly manual §1.3 states or links it.

| Fact | Source | Where the KB already has it |
|---|---|---|
| **A Spin2 cog has 16 free LUT longs.** The interpreter occupies LUT `$010..$1FF`; `$000..$00F` is free and "ideal for streamer modes which use the LUT" | `spin2-v55-text.txt:805-806`, `:833-834` (identical in `spin2-v51/spin2-language-section.txt:3114-3118`, `:3182-3191`) | `spin2/constructs/inline_pasm.yaml:54`, `spin2/concepts/inline_pasm2.yaml:31` |
| **Sharing has a handshake:** `SETSE1..4` arm LUT read/write events on `$1FC..$1FF`, including the companion cog's writes | `silicon-doc-text.txt:504`, `:2246-2249`; P2 Datasheet `p2-datasheet-text.txt:613-614` | `pasm2/setse1.yaml:14-25` (and `setse2..4`) |
| **`COGINIT` can start a sharing pair:** `%x_1_xxx1` finds and starts an even/odd pair | `silicon-doc-text.txt:413`, `:502` | `pasm2/coginit.yaml:5`, `:65-68` |

**Correction:** state each in `lookup_ram.yaml` (with `related:` to the file that already carries it,
by full path) and in Assembly manual §1.3 / §1.3.3. **The Spin2 fact matters most** — a reader planning
LUT use from a Spin2 program otherwise learns it only by reading the inline-PASM pages.

## Auto-shrunk table columns reserve a FIXED 0.93 of \linewidth while colsep scales with column count, so every wide table overruns by a predictable amount (2026-09-11, IOSP v1.0.10 certification) — F-423

### F-423 — `p2kb-platform-tables.lua` uses a constant `usable = 0.93`; the correct value depends on the column count — `RESOLVED — fixed 2026-09-11; VALIDATED ON BOTH RELEASED ARTIFACTS, re-measured 2026-09-13`

**Validation (added 2026-09-13).** The status above had read *"FIX APPLIED — awaiting verification"*,
which is not a legend token, so the hygiene gate flagged it — and it was stale: the verification it
waited for had landed the same day. Re-measured on the released PDFs rather than taken from
`PLATFORM-FEATURE-ADOPTION.md`'s record: `audit-pdf-margin-overflow.py` reports **CLEAN** on
*P2 I/O & Smart Pins User Guide* v1.0.10 (397 pages) — the document whose Appendix D table crossed the
margin — and on *P2 Assembly Language Reference Manual* v3.1.8 (506 pages), the first full-size
render after the fix, whose tables re-flowed (505 → 506pp). Tightened to a **1pt** tolerance over
IOSP pp328-332, the only span left anywhere near the margin is **p330 +2.1pt, a justified prose line**
("see Appendix B. For application ex-") — not a table cell. The four Appendix D table spans that
measured +20.3 to +24.1pt are gone, and 2.1pt is well inside the 20pt tolerance that is the gate's
verdict.

**The mechanism, and it is exact.** The auto-shrink branch computes per-column fractions, then
distributes `leftover = usable - summ` to columns with wrappable prose, so the emitted widths
**always sum to exactly `usable`** whenever any column can wrap. `usable` is hardcoded:

```lua
local usable = 0.93      -- fraction of \linewidth available to column bodies
```

But tabularray adds `colsep` on BOTH sides of EVERY column, so the space colsep consumes is
`2 x colsep x num_cols` — it scales with the column count, and 0.93 does not. With the
~468pt measure these manuals use and the 5pt colsep the filter emits:

| columns | usable should be | filter uses | overrun |
|--:|--:|--:|--:|
| 6 | 0.872 | 0.930 | **27.2pt** |
| 7 | 0.850 | 0.930 | **37.2pt** |

**Measured against that prediction, on three sites in two independently-rendered documents:**

| document | site | columns | predicted | MEASURED |
|---|---|--:|--:|--:|
| Streamer Guide v1.1.1 | §6.2 and §8.1 mode tables | 6 | 27.2pt | **26.64pt** |
| I/O & Smart Pins v1.0.10 | p246 | 6 | 27.2pt | **27.12pt** |
| I/O & Smart Pins v1.0.10 | p328 | 7 | 37.2pt | **37.12pt** |

Within half a point on every one. This is not a heuristic that occasionally misfires; it is a
constant that is wrong by a computable amount.

**Whether it SHOWS depends on content, which is why it survived.** An overrun only crosses the
right margin if the last column's text actually fills its reserved width. Streamer's tables
overrun by 26.64pt and print clean — pages 30, 33 and 34 were rendered and inspected during that
release. I/O & Smart Pins' Appendix D "All Output Modes at a Glance" (p330) does fill it, and four
spans cross the margin by 20.3-24.1pt. The published v1.0.9 measures the same four spans at the
same magnitudes, so it has shipped this way.

**THERE IS NO DOCUMENT-LEVEL WORKAROUND, and that is the load-bearing fact.** Shortening cells or
headers does not help: the leftover-distribution step scales the columns back up to fill 0.93
regardless. Only the platform constant can fix it.

**The fix** is to derive `usable` from the column count and the chosen colsep rather than hardcode
it — `usable = 1.0 - (2 * colsep_pt * num_cols) / linewidth_pt` — or to emit widths against
`\dimexpr\linewidth - <total colsep>\relax` so the arithmetic is exact rather than nominal.

**FIX APPLIED 2026-09-11.** `usable` is now derived per table — `1.0 - (2 * colsep_pt * num_cols)
/ LINEWIDTH_PT`, computed inside the font-tier loop (each tier has its own colsep) and recomputed
for the tier actually chosen. LINEWIDTH_PT is nominal at 468pt, which is enough: it reserves space
colsep genuinely consumes rather than guessing a safety margin.

**Why it landed now rather than after the wave, reversing the recommendation below.** The deferral
argument was that a shared-file change needs its own render to verify, and should not ride inside
someone else's release. That reasoning expired: **I/O & Smart Pins had to re-render anyway** for an
unrelated defect (its PDF Title lost the `&`), so the verification render is free rather than
extra. Stephen had agreed to ship the overrun as-is — this supersedes that only in the sense that
the cost which justified accepting it no longer exists.

**It also could not have shipped as-is.** `audit-pdf-margin-overflow.py` is BLOCKING and its
tolerance IS its verdict — there is no per-site acceptance path, by design. Releasing IOSP with
the p330 overrun would have meant inventing one, which is how a gate stops meaning anything.

**Expect tables to change.** 0.93 was generous; the derived value is 0.850-0.872 at six and seven
columns, so some tables that previously fit at `\small` will now fall through to a smaller tier.
That is correct — they genuinely did not fit — but it is a visible change, and the IOSP render is
where it gets checked. The already-published documents are untouched as published; their tables
change only at their next render.

**Original reasoning, kept for the record — why it was not applied in the first pass.** `p2kb-platform-tables.lua` is loaded by every document in
the set. Narrowing columns re-flows every auto-shrunk table in all of them, so it needs its own
change with a before/after render comparison — the same reasoning that carved F-319 out of
Assembly v3.1.7, and the same reasoning that says a shared-file fix lands with a verification pass
rather than inside someone else's release. **It blocks I/O & Smart Pins v1.0.10 specifically**,
because that document is the one whose table actually crosses the margin and it cannot be fixed
locally. Stephen's call: land the platform fix and re-render, or ship the pre-existing overrun
and fix the platform after the wave.

---

## A release gate could not reach a fixpoint: satisfying it re-broke it, because its own fix is a commit it reads (2026-09-10, manual-head gate-runner wiring) — F-420

### F-420 — `sync-manual-examples.py` derives `Updated` from the file's git mtime, so committing its own fix re-breaks the gate — `RESOLVED 2026-09-11 (c42acd95) — fix applied, both controls verified on real history`

Found 2026-09-10 while wiring the manual-head gate runner. Not a content defect: a **gate that
cannot reach a fixpoint**, which trains people to ignore it.

**The mechanism.** `sync-manual-examples.py:372` sets the header's `Updated....` field from
`git log -1 --format=%ad --date=format:'%b %Y' -- */<name>` — the last commit that touched the
FILE. A header re-sync is itself a commit that touches the file. So:

1. version bumps → `--check` reads RED → sync writes `Updated.... Aug 2026`
2. commit the synced file → its last-touching commit is now **September**
3. `--check` reads RED again, wanting `Sep 2026` — immediately after doing the right thing

Reproduced 2026-09-10 across all three corpus-shipping manuals: Getting Started (4 files),
deSilva (3) and I/O & Smart Pins (15) all went GREEN, were committed, and read RED on the next
run. 22 files, one line each, `Aug 2026` → `Sep 2026`.

**The tool anticipated this and the mitigation is incomplete.** Its own comment at :368 says
month granularity was chosen so that *"the tool would not be idempotent across a commit … a month
changes rarely and only when the body actually changed in a new month."* The second half is
false. `git log -1 -- <file>` returns the last commit touching the file **including a header-only
commit**, so the field moves whenever a re-sync crosses a month boundary — which is exactly what a
release does, because a release is when the version bumps. The mitigation reduces the frequency to
once per month boundary; it does not remove the class.

**Why it matters more than one stale line.** This gate is now BLOCKING in
`validate-manual-release.py --phase prepare`. A blocking gate that goes red immediately after
being satisfied is the fastest way to teach an operator to skip it — the same failure the
non-blocking KNOWN tier exists to avoid elsewhere in that runner.

**The fix (not applied — it rewrites 22 shipped headers and wants its own verification pass).**
Derive `Updated` from the last commit that changed the file's **body**, not the file. The tool
already splits header from body to rebuild the header, and `verify-example-corpus-identity.py`
already compares bodies, so the concept exists on both sides: walk `git log --format=%H -- <file>`
newest-first, strip each revision's header, and take the first commit whose body differs from its
parent's. Prove it with a negative control — a body-only change must move the field, a header-only
commit must not.

**RESOLVED 2026-09-11, commit `c42acd95`** — the specified fix, applied as written: `Updated`
now comes from the newest revision whose **body** differs from its predecessor's, so a header-only
re-sync is invisible to it and the gate reaches a fixpoint. The October relapse the interim state
predicted cannot occur.

**The first control was worthless, and that is the part worth carrying forward.** A throwaway git
repo was built in a scratch directory and "passed" a negative control there. It proved nothing:
`git()` runs `git -C str(REPO)` with REPO derived from the script's own path, so every query went
to *this* repo and the scratch commits were never read — the same shape as
`backups-copy-breaks-path-derived-repo`. **A tool that pins its own repo root cannot be controlled
from outside that repo.** The controls that count are real commits here:

| file | history | result |
|---|---|---|
| `adc-single-pin-base.spin2` | Sep header-only commit over two body commits (Jun, Aug) | **Aug 2026** — header-only skipped, and the NEWER of the two body commits chosen, which is the positive half |
| `cordic-sine-cosine.spin2` | Sep header-only over one body commit | **Jun 2026** |
| `ch03-blink-led.spin2` | **five consecutive header-only commits** (Jun/Jul/Aug/Sep/Sep) over one body commit | **Jun 2026** — the old rule's churn made visible |

**Consequence, and the reason this was worth doing properly rather than re-syncing again:** reading
the body makes the **already-published** headers right instead of forcing a re-release. P2AN001 and
P2AN002 had shipped hours earlier carrying Jun/Jul/Aug — when their code was actually last written —
and the old rule wanted them rewritten to September purely because the header was added then.
Re-syncing all eight adopted documents rewrote 23 files and left those two at **zero rewritten**;
their public ZIPs are correct as shipped. It also cleared a standing RED nobody had filed:
`p2-debug-window-manual`'s 34 examples read out-of-sync before the change and GREEN after, without
a byte moving. `p2-xbyte-programming-guide` was the one released document whose corpus did change
(one header line), so its published ZIP was repacked to match.

### F-408 — the Assembly manual's own feature list says the P2 has "programmable pull-up/down resistors" — `RESOLVED — validated on the released PDF 2026-09-11`

`p2-assembly-language-manual/opus-master/part-i/chapter-05-hardware.md:231`. The sprint's origin
class (ledger §1.4) in ALM's capability summary. `P_HIGH_*`/`P_LOW_*` select **drive strength**.

**The repair is not a deletion.** Ledger §1.24 settled that a reader *can* pull a line high or low —
`P_HIGH_15K` with `DIR=1, OUT=1` is a 15 kΩ path to VIO, and the Silicon Doc uses that vocabulary
for these same rungs (`silicon-doc-text.txt:4599`). The difference that breaks code is that the pull
is a property of **driving**, so **DIR must stay high**. Source:
`architecture/pin-drive-configuration.yaml`, `language/{pasm2,spin2}/concepts/basic-io.yaml`.

**APPLIED 2026-09-10** — ALM v3.1.8: the bullet now reads *"Independently selectable drive strength for the high and low side of the output driver"*, and a new paragraph after the component list carries the eight-rung ladder, the independent high/low sides, `P_HIGH_15K`+`DIR=1`+`OUT=1` as a 15 kΩ path to VIO, and the DIR caveat. The word "pull-up" is KEPT, per §1.24. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-Assembly-Language-Manual.pdf p98`, not from the opus-master source and not from the compile log. reads "the P2 has **no separate** programmable pull-up or pull-down resistors. The high side and the low side of each pin's driver each select one rung of the same eight-rung ladder, running from a fast digital drive down to float, and the two sides are selected independently." The repair is the explanation the finding asked for, not a deletion. (A naive grep for `programmable pull-up` still hits -- inside the negation that IS the fix; the artifact had to be read, not counted.)
### F-409 — ADDSX's C-flag prose contradicts its own Operation line and encoding row — `RESOLVED — validated on the released PDF 2026-09-11`

`part-ii/instructions-a.md:228` reads *"the C flag is set (1) if the result is negative
(**Result[31] = 1**)"* while `:208` and `:219` in the same file both give **`C = true sign of
(D + S + C)`**. The two differ **exactly on overflow**, the condition `TJV` exists to detect.

This is **F-379** in the manual — the KB repaired the identical wording in
`language/pasm2/{addsx,subsx}.yaml` this release. The rest of the family is already correct in ALM
(`ADDS :169`, `SUBS :1223`, `SUBSX :1254`, `CMPS :387`, `CMPSX :470`, `SUMC :1321`), so **ADDSX is
the lone outlier** — F-379's own lesson repeating: *a class sweep that misses one member leaves a
defect that looks deliberate, because every neighbour is right.*

Lesser, same paragraph: `:191` (ADDS) writes *"the true sign of the signed sum, Result[31] = 1"* as
if the two were one thing. It recovers in the next sentence, so fix the parenthetical only.

**APPLIED 2026-09-10** — ALM v3.1.8: both `:191` (ADDS) and `:228` (ADDSX) now state C as the true sign at full precision and say plainly it is **not** `Result[31]`; ADDSX cites `TJV` as the case that separates them. **Independently re-verified the "lone outlier" claim** — the only surviving `Result[31]` in ALM is `appendix-a:74` for **CMPM**, where it is CORRECT (`cmpm.yaml`: *"C: Set to MSB of (D - S), i.e., Result[31]"*) — that IS the instruction. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-Assembly-Language-Manual.pdf, ADDSX entry`, not from the opus-master source and not from the compile log. `Operation: D = D + S + C; C = true sign of (D + S + C)` and the encoding row's C column both read `true sign of (D + S + C)`. Prose, Operation line and encoding row now agree.
### F-410 — ALM says GETBRK's flag effect is optional; it is required, and the sibling manual says so — `RESOLVED — validated on the released PDF 2026-09-11`

`part-ii/instructions-g.md:14` (`{WC|WZ|WCZ}` braces) and `:19` (*"optional effects"*). The shipped
KB, `language/pasm2/getbrk.yaml:13`: *"GETBRK **REQUIRES** a flag effect (WC, WZ, or WCZ); the
no-flag form does not assemble."* Each flag selects a **different** result (**F-368**).

**`p2-xbyte-programming-guide/opus-master/xbyte-body.md:1193` already has it right** — *"It requires
a flag effect, and the flag you choose selects which information you get"* — which is Chip Gracey's
own CG-3 correction. **Two shipped manuals disagree with each other**, and ALM's syntax braces are
wrong as well as its prose.

**APPLIED 2026-09-10** — ALM v3.1.8: syntax line is now `**GETBRK**  *Dest*  **WC|WZ|WCZ**` (braces dropped — 166 other syntax lines legitimately use `{}`, GETBRK being the lone required-flag instruction), and the bullet states the flag is **required** and *selects which of three different results* is returned. **Narrower than filed:** the entry's own **Explanation** body was ALREADY correct (*"A flag effect is required … does not assemble"*), so the manual was contradicting itself three paragraphs apart, not simply wrong. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-Assembly-Language-Manual.pdf, GETBRK entry`, not from the opus-master source and not from the compile log. the signature reads `GETBRK Dest WC|WZ|WCZ` -- the flag effect carries no optional brackets, and the Result line says the status retrieved depends on "the flag effect specified". Required, as the sibling manual has it.
### F-411 — ALM's clock row attributes to the P2 Datasheet two figures the datasheet does not contain, and contradicts its own Chapter 4 — `RESOLVED — validated on the released PDF 2026-09-11`

`front-matter.md:144`: *"180 MHz recommended; **250 MHz typical overclock; 350 MHz absolute max**¹"*,
footnoted at `:153` *"¹ **Per P2 Datasheet.**"*

The datasheet's AC Characteristics PLL row gives **min 3.33 / typ 180 / max 320 MHz**
(`p2-datasheet-text.txt:2200`, footnote 2 at `:2209`). It contains **neither 250 nor 350**.

- **250 MHz "typical overclock"** — no source we hold.
- **350 MHz** is real but is **not** an absolute maximum and **not** the datasheet's: it is the
  **VCO/1 overclock ceiling** from the Silicon Doc (`part3-interrupts.txt:545`).
  `architecture/clock_system.yaml:209` states the distinction outright.
- **The datasheet's actual 320 MHz maximum is absent from the row.**

**And the manual contradicts itself:** `part-i/chapter-04-timing.md:94` says *"up to 320 MHz"*, with
`:96`, `:562`, `:655` all computing from 320. `ch04:34` states the 350 MHz VCO/1 case **correctly** —
copy that discipline up. This is the whose-limit rule (**E-007**): every clock figure must name
whether it is the compiler's, the datasheet's, or an overclock ceiling.

**APPLIED 2026-09-10** — ALM v3.1.8: the row now reads *"180 MHz typical; 320 MHz datasheet maximum"* and the footnote gives min 3.33 / typ 180 / max 320 with the 105 °C condition, attributing 350 MHz to the Silicon Documentation as the VCO/1 overclock ceiling. Datasheet re-verified live: 250 and 350 appear nowhere as clock figures (the only hits are *"~350 unique instructions"* and a `250 ms` code example). **A second defect found at the same time, NOT in this finding:** `ch04:20` gave 320 MHz as the **XI external-input** ceiling; the datasheet rates direct drive into XI at **DC–200 MHz**, and 320 is the PLL *output* max. Rewritten to keep the two limits apart. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-Assembly-Language-Manual.pdf, For P1 Developers table + footnote 1`, not from the opus-master source and not from the compile log. the row reads `180 MHz typical; 320 MHz datasheet maximum`, and the footnote now attributes correctly: "The P2 Datasheet's AC Characteristics give the PLL system clock as 3.33 MHz minimum, 180 MHz typical, 320 MHz maximum, with the nominal 180 MHz rating specified up to 105 C. Beyond the datasheet, the Silicon Documentation notes..." -- datasheet figures are now the datasheet's, and the non-datasheet claim is attributed separately.
### F-412 — the IOSP states the input threshold as fixed volts; the datasheet gives it as a fraction of the I/O supply — `RESOLVED — validated on the released PDF 2026-09-11`

`p2-io-and-smart-pins-user-guide/.../chapter-12-digital-input.md:25` and `:95` — *"approximately
**1.65V** threshold"*.

**F-407**'s shape in the manual. The P2 Datasheet DC Characteristics (`:2163`) give **one** threshold
as `Vih = Vxxyy * 0.3 min / *0.5 typ / *0.7 max`. At 3.3 V that is **0.99 / 1.65 / 2.31 V** — 1.65 is
the *typ*, the band is ±0.66 V wide, and **it moves with `Vxxyy`**, so two pin groups on different
supplies do not share thresholds. Same chapter, same class: `:156` hard-codes
`threshold = (level / 256) × 3.3V` for the level comparator, which genuinely is a fraction of VIO;
`:130`, `:133`, `:583` derive the ~1.4 V TTL level from that same hard-coded supply.

**APPLIED 2026-09-10** — IOSP v1.0.10: §12.1 now states `Vih` as `Vxxyy * 0.3 / * 0.5 / * 0.7`, spells out the 0.99–2.31 V band at 3.3 V, says the threshold moves with the supply, and instructs that 1.65 V is the typical value and not the switching point. The level-comparator formula reads `(level / 256) * Vxxyy`, its voltage table names the 3.3 V supply its rows assume, the TTL level-108 derivation says to recompute for another `Vxxyy`, and the Example-4 block declares the assumption. `:95`'s restatement now points at §12.1 instead of repeating a number. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-IO-and-Smart-Pins-User-Guide.pdf p184`, not from the opus-master source and not from the compile log. "a fraction of the I/O supply Vxxyy: minimum Vxxyy * 0.3, typical Vxxyy * 0.5, maximum Vxxyy * 0.7 ... The threshold is a band, not a point. At a 3.3 V supply it spans 0.99 V to 2.31 V, with 1.65 V as the typical value ... The threshold moves with the supply ... **Quote 1.65 V as the typical value at 3.3 V, never as the switching point.**" The remaining `1.65V` hits in the manual are DAC OUTPUT arithmetic (128/256 x 3.3 V), a different quantity, and p187 states the scaling rule for those too.
### F-413 — P2AN001's clock pitfall states a 300 MHz maximum that exists in no source, and contradicts its own YAML companion — `RESOLVED — validated on the released PDF 2026-09-11`

`app-notes/P2AN001/opus-master/P2AN001.md:638` — *"The P2's **specified maximum is 300 MHz**; the
original research code ran at 320 MHz, **which is over spec**."*

**300 MHz appears in no source we hold and in no KB file.** The datasheet maximum is **320 MHz**, so
the research code was **at** the limit, not over it. `application-notes/p2an001-…yaml` was corrected
2026-09-09 and now carries the datasheet's min 3.33 / typ 180 / max 320 with its 105 °C footnote —
so **the note and its own companion now disagree**, which the four-artifact model forbids.

**APPLIED 2026-09-10** — P2AN001 v1.0.5: the pitfall now gives min 3.33 / typ 180 / max 320 MHz with the 105 °C footnote, and states that the research code's 320 MHz sat *at* the datasheet maximum rather than beyond it, though above the typical rating. Note and companion agree. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.



**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2AN001.pdf`, not from the opus-master source and not from the compile log. the string `300 MHz` does not occur anywhere in the released PDF.
### F-414 — P2AN001 carries the unreproduced 15 mV designer figure and not the measured ≤9 mV result — `RESOLVED — validated on the released PDF 2026-09-11`

`P2AN001.md:626`. The note qualifies 15 mV correctly as designer-stated, but the companion has moved
past it: *"Hardware-verified 2026-07-07 on real P2: the ratiometric single-pin absolute error was
**≤9 mV**, reproducible… the wider '~15 mV pin-to-pin spread' figure is a designer report that **the
bench has NOT yet reproduced**… **Do not quote 15 mV as a specification.**"* Empirical sources are
first-class here and outrank a designer report.

**APPLIED 2026-09-10** — P2AN001 v1.0.5: the pitfall now LEADS with the measured ≤9 mV floor (offset, not noise, so averaging does not remove it) and demotes 15 mV to a designer report the bench has not reproduced, with the instruction not to quote it as a specification. Verified LIVE against `P2-EMPIRICAL-FINDINGS.md` rather than via the companion — the ledger states the ≤9 mV result *"does NOT support a ~15 mV single-pin absolute floor"*, CONFIRMED 2026-07-07. Render owed, so this stays `PENDING-VALIDATION` until the rebuilt PDF is read.


---


**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2AN001.pdf`, not from the opus-master source and not from the compile log. "Measured on real P2 silicon (2026-07-07), the single-pin ratiometric absolute error was <=9 mV, reproducible" -- and the designer figure is demoted in the same paragraph: "The P2's designer separately reports having seen pins read as much as 15 mV apart pin-to-pin (Reference 2). Treat that as a designer report, not a specification -- the bench has not yet reproduced it ... Design to the measured <=9 mV single-pin floor, and do not quote 15 mV as a specification."
### Re-adjudicated, not newly filed — F-356's DeSilva disposition

F-356 records `p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md:2881` as *"checked and left
because it is already **correct**."* Against the framing in force on 2026-08-25, it was. **Ledger
§1.24 (2026-09-09) changed the framing.** Under it the line is weak twice: *"No pullup/pulldown **by
default**"* implies a non-default internal pull exists, and it sends the reader to **smart-pin
modes** when the mechanism is **drive strength**. Not re-filed as a correction — nothing here makes
a reader's code fail — but F-356's disposition should not be read as settling it.

### F-416 — `cordic.yaml` states a ~28-bit trig precision that no source gives, and that the P2AN002 companion already dropped — `RESOLVED — validated on the served KB 2026-09-11`

`deliverables/ai/P2/architecture/cordic.yaml:183` — `trig_functions: "~28 bits of precision"`.

**No Parallax source states a bit figure for CORDIC trigonometric precision.** Swept 2026-09-10:
neither `silicon-doc-text.txt` nor `p2-datasheet-text.txt` contains a 28-bit precision claim
anywhere. The figure survives in the KB while the **P2AN002 YAML companion already removed its own
`verify: Precision ~28 bits` flag under cite-or-omit** — so the KB and a shipped companion now
disagree about a number neither can source.

Surfaced while applying the v1.18.0 manual sweep: P2AN002 quoted "about 28 bits" in two places
(`:354`, `:369`) and was traced back to this file rather than to an authority.

**Proposed correction:** drop the bit count and state the behaviour the sources do support — the
integer operations (QMUL/QDIV/QFRAC/QSQRT) are exact 64-bit integer operations; the iterative ones
(QROTATE/QVECTOR/QSIN/QLOG/QEXP) leave the low bits approximate, with the magnitude scale factor
corrected in hardware. If a bit figure is wanted, it needs a bench measurement and an EF entry, not
a carried-forward number.

**Already applied downstream (P2AN002 v1.0.4):** the note now describes the residual instead of
counting it, and tells the reader to measure it against their own tolerance. The KB edit is what
remains owed here.

> ✅ **APPLIED 2026-09-10; `PENDING-VALIDATION` until a KB release publishes it** — p2kb-mcp serves
> the PUBLISHED tree, so a consumer still reads `~28 bits` until then. Repaired under `SOURCE-REPAIR-ORDER` — re-read the source, **removed the
> whole uncited block**, repopulated from the source rather than citing in place.
>
> **The finding was NARROWER than the defect, in two directions.** (a) The claim was alive at **two**
> KB sites, not one: `architecture/cordic.yaml:183` *and* `application-notes/p2an002-…yaml:95`, whose
> `precision:` field still carried *"trig … ~28 bits"* — this entry recorded the companion as having
> dropped it, and only its `verify:` flag had been. Both are repaired. (b) Opening the block found
> **three further wrong values in the same six lines**, which is exactly what the repair order
> predicts — see **F-419**.
>
> **Source trace:** no bit count for CORDIC trigonometric precision appears anywhere under
> `engineering/ingestion/sources/` (swept). The repopulated `accuracy:` block cites
> `silicon-doc-text.txt:175-182` and states the formats that source gives; the trigonometric entry
> now says plainly that no source states a figure and none is asserted, pointing at a bench
> measurement + EF entry as what a number would require.
>
> **Findability improved in the same touch:** the file's `see_also:` was four bare-prose strings
> (*"QMUL instruction details"*, *"Pipeline optimization techniques"*, …) which that field never
> resolves, so a consumer following them reached nothing. Redirected per Sacred Rule #7 into a
> `related:` block of resolving keys — the seven `Q*` instruction entries, plus
> `cordic_solver.yaml` and `p2kbAppNoteP2an002CordicForRealWork` for the pipeline-optimization
> concept. `validate-crossref-keys.py` CLEAN.


**VALIDATED ON THE PUBLISHED ARTIFACT 2026-09-11.** KB v1.18.1 is on the remote and `p2kb-mcp` is serving it, so the release-yamls §7b CONTENT PROBE was finally runnable — and it was run against the *served* entry (`p2kb_get p2kbArchCordic`), not against the repo tree and not against a refresh reporting OK, which is the distinction this finding was held open for. The live `accuracy:` block reads `logarithm: 32-bit unsigned -> 5.27 fixed-point`, `exponential: 5.27 fixed-point logarithm -> 32-bit unsigned`, `square_root: 64-bit -> 32-bit square root`, and a `trigonometric:` entry that states plainly that NO Parallax source gives a bit count. The `~28 bits` figure and both `5.32` values are absent from the served content. `source:` cites `silicon-doc-text.txt:175-182`.
### F-419 — `cordic.yaml`'s `accuracy:` block contradicted its own `operations:` block on three quantities — `RESOLVED — validated on the served KB 2026-09-11`

Found 2026-09-10 while repairing F-416, by removing the uncited block instead of citing it in place.

`deliverables/ai/P2/architecture/cordic.yaml`, the six-line `accuracy:` block. Four of its six
values were defective — one uncited (F-416's `~28 bits`) and **three flatly wrong**:

| field | the block said | Silicon Doc `:176-182` + the KB's own entries |
|---|---|---|
| `square_root` | "16-bit result, ±1 LSB" | **64-bit → 32-bit** (`qsqrt.yaml`; and this file's own `operations.square_root:79`) |
| `logarithm` | "5.32 fixed-point" | **5.27** (`qlog.yaml`; own `operations.logarithm:104`) |
| `exponential` | "5.32 fixed-point" | **5.27** (`qexp.yaml`; own `operations.exponential:112`) |

**The file disagreed with itself.** Its `operations:` block already stated all three correctly, so a
consumer's answer depended on which block it happened to read — the F-409 shape (ADDSX's prose
against its own operation line), in the KB rather than a manual. "5.32" looks like a plausible
transcription of a 32-bit total, which is why it survived: 5 integer + 27 fraction **is** 32 bits.

**Nothing could have caught it.** The values are well-formed, they sit beside correct neighbours,
and no gate we run compares two blocks inside one file for agreement.

**Applied:** the block is removed and repopulated from `silicon-doc-text.txt:175-182`, each entry
naming the per-instruction file that owns the detail rather than restating it. `verify-yaml-format`
clean, `validate-crossref-keys` clean. Stays `PENDING-VALIDATION` until a KB release publishes it.


**VALIDATED ON THE PUBLISHED ARTIFACT 2026-09-11.** KB v1.18.1 is on the remote and `p2kb-mcp` is serving it, so the release-yamls §7b CONTENT PROBE was finally runnable — and it was run against the *served* entry (`p2kb_get p2kbArchCordic`), not against the repo tree and not against a refresh reporting OK, which is the distinction this finding was held open for. The live `accuracy:` block reads `logarithm: 32-bit unsigned -> 5.27 fixed-point`, `exponential: 5.27 fixed-point logarithm -> 32-bit unsigned`, `square_root: 64-bit -> 32-bit square root`, and a `trigonometric:` entry that states plainly that NO Parallax source gives a bit count. The `~28 bits` figure and both `5.32` values are absent from the served content. `source:` cites `silicon-doc-text.txt:175-182`.
### F-417 — two open-drain configurations name the wrong side of the driver, in a released manual and a released appendix — `RESOLVED — validated on the released PDF 2026-09-11`

Neither was on the v1.18.0 sweep list; both surfaced while applying it, by asking of every
pull-vocabulary site the question §1.24 asks. Both are **fixed**; renders are owed.

**(a) `p2-assembly-language-manual/opus-master/part-iii/appendix-f-smartpin-constants.md:312`** —
an example commented *"Configure for open-drain with 1.5kΩ pull-up"* over
`P_HIGH_FLOAT | P_LOW_1K5`. `P_LOW_1K5` is the **low-side** rung (`spin2-builtin-symbols-complete.yaml`:
*"Drive low 1.5kΩ"*), so the 1.5 kΩ is the **sink**, not a pull-up; an I2C bus pull-up is external.
The block also set **no DIR**, so as printed it drove nothing.

**(b) `p2-io-and-smart-pins-user-guide/.../chapter-06-digital-output.md:441`** — the §6.6
*Configuration Quick Reference* row read *"Open-drain + internal pull-up | `P_HIGH_15K` \|
`P_LOW_FAST`"*. That configuration is **not open-drain**: with `P_HIGH_15K` the high side actively
drives through 15 kΩ instead of floating. The row is now *"Weak-high / strong-low (open-drain
substitute)"*, and the prose beside it says a genuine multi-master bus wants `P_HIGH_FLOAT` with an
external pull-up. A quick-reference table is exactly where a wrong label does damage, because it is
scanned and copied rather than read.

*Why this class keeps recurring:* §1.24 made "pull-up" acceptable vocabulary, which is right — but
the vocabulary being acceptable does not make a **composition** correct. The remaining question at
every site is *which side drives, and does DIR let it*.


**VALIDATED ON THE RELEASED ARTIFACT 2026-09-11** — read from `P2-Assembly-Language-Manual.pdf, open-drain example`, not from the opus-master source and not from the compile log. `P_HIGH_FLOAT | P_LOW_1K5` with the comment "Open-drain: floats when OUT=1, sinks through 1.5k when OUT=0. The bus pull-up is external -- the 1.5k here is the LOW-side drive." The sinking side is named correctly and the external pull-up is stated.
## The datasheet's DC Characteristics table was never carried, so the KB answered "what is the input threshold?" with silence after the fabricated answer was removed (2026-09-09, terminology review) — F-407

### F-407 — fabrication removed correctly, the real table never put in its place — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**Location:** `deliverables/ai/P2/architecture/io_pin_timing.yaml`.

**How it surfaced.** Stephen asked, after the F-406 pull-up review, whether anything **else** in the release change set had that same shape. This is the answer: the only other instance in the 112 changed files.

**What happened.** The uncited-quantity purge removed this file's `input_characteristics` block, and removing it was **correct** — it stated `VIL_max 0.8 V`, `VIH_min 2.0 V`, a `~1.5 V` switching threshold, Schmitt thresholds of `1.65 V`/`1.35 V` and `~300 mV` hysteresis, and **no Parallax source states any of it**. But nothing replaced it. From that day the KB answered the input-threshold question with **nothing at all**, and carried no marker saying the answer was unknown — while the real table sat in a source this same file already cites.

**What the source actually has.** P2 Datasheet 2022/11/01, **DC Characteristics**, p.47-48 (`p2-datasheet-text.txt:2151-2186`):

| Symbol | Parameter | Value | Line |
|---|---|---|---|
| `Vih` | Input Logic Threshold | min `Vxxyy*0.3` · typ `*0.5` · max `*0.7` | `:2163` |
| `Iil` | Input Leakage Current | ±0.1 µA typ · ±10 µA max | `:2165` |
| `Vol` | Output Low Voltage (vs GND) | 15 / 160 / 510 mV at 1 / 10 / 30 mA | `:2172-2174` |
| `Voh` | Output High Voltage (vs Vxxyy) | −6 / −170 / −580 mV at 1 / 10 / 30 mA | `:2176-2178` |
| `Vdd` · `Vxxyy` | Supply ranges | 1.7/1.8/1.9 V · 3.15/3.3/3.45 V | `:2159`, `:2161` |

**The threshold row is the one that matters, and its shape is what the fabrication got wrong.** The datasheet states **one** threshold as a **fraction of the I/O supply**, not a VIL/VIH pair in fixed volts. At 3.3 V that is 0.99 / 1.65 / 2.31 V — and it **moves with `Vxxyy`**, so two pin groups on different supplies do not share thresholds. The removed block's fixed 0.8 V / 2.0 V pair could not have been derived from this table; it reads as generic 5 V-logic TTL numbers.

**Named as not stated, so the next reader does not infer it:** separate VIL/VIH figures, Schmitt switching thresholds, and hysteresis in millivolts. The P2 **has** Schmitt input modes (`P_SCHMITT_A` and variants) and no source we hold says what hysteresis they produce.

**A cross-check this table settles.** `Vol`/`Voh` are characterised at 1, 10 and 30 mA and stop, agreeing with the `±30 mA` absolute maximum already in the file. **This is the table that made the shipped `150 mA` pin-current claim impossible** (F-348 class) — it was in the datasheet the whole time.

**And one claim verified rather than asserted.** The file's description says no source states propagation, rise or fall figures. Checked: the **AC Characteristics** table on the facing page (`:2188-2210`) is oscillator frequency and XI/XO capacitance **only**. The claim stands. Its PLL row — 3.33 / 180 / 320 MHz — is the same ceiling F-378 corrected the clock files to.

**Correction applied 2026-09-09.** A `dc_characteristics:` block, every figure transcribed from the table, read at its line, per-row line numbers recorded in the block, and verified programmatically after writing. The description now states what the two electrical tables are *for*: absolute maximum ratings are stress limits, DC characteristics are what you design to.

**Why no instrument caught it.** No gate can see a **missing** block. The sourcing gate scores quantities that are present; the fidelity gate scores constants that are present; the crossref gate resolves references that are present. **A question the KB does not answer at all is invisible to every one of them** — and this file passed all of them, cleanly, while carrying no answer.

**Why `PENDING-VALIDATION`.** Applied; the release is what it awaits.

---

## A coder asking for a pull-up got a denial first and the answer fourth, and 15 of 17 phrasings of the question resolved to nothing (2026-09-09, terminology review) — F-406

### F-406 — the KB was correct about the constants and hostile to the reader asking for them — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**Location:** `deliverables/ai/P2/architecture/pin-drive-configuration.yaml` (retrieval) and both `concepts/basic-io.yaml` files (framing).

**How it surfaced.** Stephen, reviewing the release change list: *"our spin2 language has pull up and pull down named constants... how are these handled in our .yaml files?"*

**First, what is NOT wrong — checked before anything was changed.** All 16 drive-strength constants are defined, described and exemplified, and coverage **grew** this release:

| | `v1.17.0` | HEAD |
|---|---|---|
| distinct `P_HIGH_*`/`P_LOW_*` names | 16 | 16 |
| occurrences across the shipped set | 73 | **153** |
| files carrying them | 11 | **13** |

Each carries `value`, `bit_pattern`, `description`, `usage_context` (`"SmartPin input/output configuration (WRPIN)"`), `hardware_relationship` and `related_symbols`; all 16 encodings were re-checked against the v55 table and are right; 16 files show them in working `WRPIN`/`PINSTART`/`DRVH`/`DRVL` examples. **Nothing was removed.** The only `P_*` deletions this release were `P_LEVEL_B` and `P_SCHMITT_B`, and `pnut-ts` rejects both as undefined symbols while accepting `P_LEVEL_A`/`P_SCHMITT_A`.

**What WAS wrong — two things, both about the reader rather than the facts.**

1. **Retrieval.** Of 17 phrasings a coder actually types, **2 resolved** — `pull-up` and `pull-down`, hyphenated singular. `pullup`, `pulldown`, `pull up`, `pull_up`, `weak pull-up`, `pull-up resistor`, `pull resistor`, `bias resistor`, `P_PULLUP`, `P_PULLDOWN` and the rest returned the undifferentiated category dump. **Now 17 of 17.**
2. **Framing.** Both `basic-io.yaml` files opened the `internal_pull_resistors` block with *"The P2 has no internal pull-up/pull-down resistor network"* and delivered the answer **fourth**, under a key named `substitute_for_a_pull_up`. The reader asking a real question was told first that the thing does not exist, then that it sort of does, under another name, as a substitute.

**The substantive point, and Stephen's:** `P_HIGH_15K` with `DIR=1, OUT=1` is a 15 kΩ resistive path to VIO. **In the reader's circuit that is a pull-up** — it holds the net and a stronger driver overpowers it. **The Silicon Doc uses that vocabulary for these same ladder rungs**: `silicon-doc-text.txt:4599`, USB mode — *"two 15k pull-downs for 'host' or a 1.5k pull-up and a float for 'device'"*. So "partially correct" is exactly right, and the KB was policing vocabulary the authority itself uses.

**The one real difference, unchanged and now stated first:** the pull is a property of **DRIVING**. Drop DIR and it is gone. That is why the old `WRPIN P_HIGH_15K` + `DIRL` idiom did nothing, and it is the fact that breaks code.

**Correction applied 2026-09-09**, shape chosen by Stephen (option C of three):
- 18 pull-vocabulary aliases added to `pin-drive-configuration.yaml`. **Aliases only — an alias is never a definition.**
- Both `basic-io.yaml` blocks now lead with `yes_you_can_pull_a_line_high_or_low`, then the DIR caveat, then `how_the_p2_does_it` — where the no-dedicated-bias-network fact explains *why* the DIR rule exists instead of standing as a refusal.
- Keys renamed: `there_is_no_bias_resistor_selector` → `how_the_p2_does_it`; `substitute_for_a_pull_up`/`_down` → `pull_a_line_high`/`_low`. **None of the three is in the published `v1.17.0` set** — they were authored this cycle — so the rename costs no consumer anything, and this was the last point at which it was free. The published parent key `internal_pull_resistors` is deliberately unchanged. Nothing in any script, filter or generator reads these names; verified by grep.

**No claim, source or example changed.**

**Why no instrument caught it.** Every gate asks whether a file is *right*. **None asks whether the reader can find it, or whether it answers the question the reader actually asked.** This file was correct, cited, gate-green, and unreachable by 15 of the 17 ways its subject is named. Third instance of the class this week, after F-401 and F-404.

**Why `PENDING-VALIDATION`.** The served index is the published one; the aliases reach no agent until the set is pushed.

---




## 24 of the 54 Spin2 DEBUG formatter names the v55 reference lists resolve to nothing, because the file documents them as a composition rule rather than as strings (2026-09-09, ledger re-derivation) — F-404

### F-404 — `UHEX_LONG_ARRAY` and 23 sibling formatter names are unreachable by the token an agent types — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**Location:** `deliverables/ai/P2/language/spin2/debug-commands/debug-formatters-arrays.yaml`.

**How it surfaced.** Verifying F-401's own claim while re-deriving the release change ledger. F-401 moved pure-symbol Spin2 names from 0 of 62 to 62 of 62; this is the same class one level further in, and F-401's pass did not reach it.

**What is wrong.** The file defines the array formatters **by composition** — `formatters: {decimal: [UDEC, SDEC], hexadecimal: [UHEX, SHEX], binary: [UBIN, SBIN], floating: [FDEC]}` crossed with `array_types: {REG_ARRAY, BYTE_ARRAY, WORD_ARRAY, LONG_ARRAY}`. **A composition rule is not a string.** No field in the shipped set holds the literal token `UHEX_LONG_ARRAY`, so the alias harvester — which reads scalar name-bearing fields — has nothing to read, and the path-derived camelCase key cannot carry it either.

**Measured against the emitted index at HEAD, not reasoned** (the *published* index is `v1.17.0`'s, so it cannot answer this): of the **54** distinct formatter names the Spin2 v55 language reference lists in its formatter tables, **30 resolved and 24 did not** — and all 24 are the sized and register forms (`<fmt>_{REG,BYTE,WORD,LONG}_ARRAY`). The bare `_ARRAY` forms resolve, because the 2026-09-05 pass enumerated those seven by hand.

**Why it matters more than a count suggests.** `UHEX_LONG_ARRAY` is the **only trusted packed-data feed shape for a scrolling LOGIC or SCOPE window** — a single `` `(packed) `` long does not fill the window, and our own DEBUG Window manual teaches the full-window array feed (F-207). The one name an agent most needs when a scrolling window renders empty resolved to nothing.

**Authority.** All 24 transcribed from `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` and each read at its line: `:943` (`FDEC_REG_ARRAY`), `:951-954` (UDEC), `:960-963` (SDEC), `:969-972` (UHEX), `:978-981` (SHEX), `:987-990` (UBIN), `:996-999` (SBIN). **`FDEC` has `_REG_ARRAY` and `_ARRAY` forms only** — no `FDEC_BYTE_ARRAY`/`_WORD_ARRAY`/`_LONG_ARRAY` appears in the reference, and none was invented to make the cross-product tidy.

**Correction applied 2026-09-09.** The 24 names are added to the file's `aliases:` block, grouped by array type, with the source lines recorded in place. **They are lookup keys for a rule the file already documents** — no new claim is made, and an alias is never a definition. Re-measured in the regenerated index: **54 of 54 resolve**, `UHEX_LONG_ARRAY` → `["p2kbSpin2DbgDebugFormattersArrays"]`, alias entries 2,896 → **2,920**, and the dark-file count is **unchanged at 173** — this repair adds names, not files.

**Why no instrument caught it.** The same reason as F-401: **no gate in this project asks whether a file can be *found*.** Every one of them asks whether it is *right*. `verify-yaml-format.py` parses it, `validate-crossref-keys.py` resolves its references, the sourcing and fidelity gates read its quantities and constants — and a name that exists in no field is invisible to all of them because there is nothing to read.

**Why `PENDING-VALIDATION`.** The served index is the published one, so this reaches no agent until the set is pushed. The validation owed is one post-publish probe: `p2kb_find("UHEX_LONG_ARRAY")` returning the array-formatter page instead of dumping the category list. Same gate as F-401 and F-402.

---

## `boot-rom-contents.yaml` ships six ROM residents; the authoritative list names three, and two of the extras appear in no source at all (2026-09-08, boot-ROM survey) — F-403

### F-403 — character font data and sin/cos/log math tables are asserted as boot-ROM contents with `verification_status: "Existence confirmed"`, sourced only to our own generated narrative — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**Location:** `deliverables/ai/P2/architecture/boot-rom/boot-rom-contents.yaml`, `residents:` — the `utility_routines`, `character_font_data` and `math_tables` entries.

**What the authority says.** The P2 Hardware Manual 2022-11-01 states the ROM's contents in one line, and it names **three** things:

> `ROM | 16 KB (Bootloader, P2 Monitor debug interface, and TAQOZ (Forth) command interface)`
> — `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:210`

The same three-item list is what our own extraction matrix recorded from that manual (`engineering/ingestion/extraction-matrices/BOOT-PROCESS-COMPLETE.md`, "Boot ROM Contents (16 KB)"). The P2 Datasheet (`:99`) and Silicon Doc (`:189`) say only *"16KB boot ROM"* and inventory nothing.

**What the shipped file says.** Six residents — the three above plus `utility_routines`, `character_font_data` ("Bitmap font data for terminal output / debug displays") and `math_tables` ("Sin/cos/log tables"). The latter two carry `verification_status: "Existence confirmed; specifics not yet documented"`.

**Existence is not confirmed.** Measured 2026-09-08 against the ROM assembly listing we hold — the strongest available evidence, since it *is* the ROM:

| term | `ROM_Booter.lst` | `rom_booter_v33_01j.lst` |
|---|---|---|
| `font` | **0** | **0** |
| `glyph` | **0** | **0** |
| `sine` / `sin_` | **0** | **0** |
| `log2` | **0** | **0** |

`TAQOZ` (48 hits) and `Monitor`/`debugger` (40) are plainly present in the same listing, so the search is not blind to real residents.

**Where the claim actually came from.** `engineering/ingestion/sources/rom-booter/rom-booter-narrative.txt:51-56` — *"Beyond the bootloader, the ROM also contains: Monitor/debugger code, TAQOZ Forth interpreter, Utility routines, Character font data, Math tables (sin/cos/log)"*. That file was created by commit `9fcf7d84` **"Complete narrative text generation for all P2 sources"** — it is **our own generated summary of the source, not a Parallax document.** A generated narrative was promoted to an authority, which is the F-341 defect shape (manufacturing provenance inside the documentary truth root).

**Why no instrument caught it.** The claims carry no quantities, so `audit-yaml-claim-sourcing.py` never scored them; they name no constants, so the fidelity gate never saw them. The file cites four real sources in its header, which is exactly what makes a Tier-2 sweep read it as a citing file. Same blind spot as F-402: **no gate reads a semantic claim.**

**Correction applied 2026-09-08.** The two unsupported residents are removed and the removal is recorded in place so the narrative cannot quietly reintroduce them. `utility_routines` is retained but reclassified: the listing does contain called subroutines, which is an observation about the code, not a documented ROM component, and it is now stated that way rather than as a fifth resident with a source line.

**Not asserted in the correction:** that font data and math tables are *absent* from the ROM. A 16 KB mask ROM can hold unlabelled data blocks that an assembly listing's symbol names would not reveal. What is established is that **no source we hold supports them and the one authoritative content list omits them** — so the KB must not state them. If their presence matters, it is a question for Chip Gracey, not a document.

**The sweep half — and the ordering lesson it carries** (`b0057ec1`, same day). `2a6df5ef`'s commit body ends *"Class sweep run: no other shipped file makes a font-data or math-table ROM claim."* **That was written before the sweep's output was read, and it was wrong.** The sweep returned four hits and two of them were the same fabricated list, in the same directory: `architecture/boot-rom/_index.yaml` stated six residents in its `description:` sentence **and again** in the `contains:` line under `boot-rom-contents`. Both corrected to the three the Hardware Manual names, plus the shared subroutines the listing actually shows. The other two hits were read and correctly left alone — `hardware/p1_rom_font_character_set.yaml` documents the **P1's** ROM font, which is real and is a different chip, and `assembly-directives/file.yaml` shows a `FILE` directive including a font file from *user* code.

*Two consequences worth carrying.* **A class-sweep claim written before its output is read is an assertion, not a measurement** — the same shape as F-396, where a repair record inside the repaired file read as a finished sweep. And **the second site was in the sibling `_index.yaml` of the very directory being corrected**: an index file restates its members' claims, so any finding that removes a claim from a file must sweep that file's index in the same pass.

**Why `PENDING-VALIDATION` and not `RESOLVED`.** Both halves are applied and no source-side work is owed; what remains is the release. The corrected file reaches an agent only when the set is published. *(Re-graded 2026-09-09 during the ledger re-derivation: the entry had stood at `CONFIRMED` while its own body said "Correction applied 2026-09-08" — the exact status-lag this register's "annotate as you fix, in the same pass" rule exists to prevent.)*

---

## Two files defined the Spin2 `+//` operator and they disagreed about what it does; corrected, and the duplicate home merged (2026-09-05, F-401 index regeneration) — F-402

### F-402 — `modulo_add.yaml` called `+//` an "Unsigned Modulo Add" that "performs addition"; corrected, and `op_addmodulo.yaml` is now the single definition home — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**How it surfaced.** Arming the `operator:` field as an index alias (F-401) made `+//` resolve to **two** targets — `language/spin2/operators/modulo_add.yaml` and `language/spin2/operators/op_addmodulo.yaml`. The collision was the symptom; reading the two files found they did not agree.

**What was wrong** (`modulo_add.yaml`, corrected in this pass):
- `name: Unsigned Modulo Add` and *"The +// operator performs addition with unsigned modulo"* — **it performs no addition**. A leading `+` on a division-family operator selects the UNSIGNED form: `/` signed divide vs `+/` unsigned divide, `//` signed remainder vs `+//` unsigned remainder.
- `related_operators` gave `"//": Unsigned divide remainder` — this **inverts the single distinction the file exists to draw**. `//` is the signed remainder.
- `related_operators` listed `"%%": Signed modulo`. `%%` appears in neither operator reference and is not a Spin2 operator; removed rather than relabelled.

**Authority:** `engineering/ingestion/sources/spin2-v51/complete-spin2-operators.md:715` (*"`+//` | Remainder (unsigned)"*), :62 (precedence group *"`*` `/` `+/` `//` `+//` `SCA` `SCAS` `FRAC` | Multiply/Divide"*), :103 (*"The `+/` and `+//` operators treat both operands as unsigned 32-bit integers"*). `op_addmodulo.yaml` — *"Unsigned remainder (modulo)"* — was correct throughout, and is now the definition home.

**Why the examples still worked, which is why this survived.** Every wrap-around idiom in the file adds *explicitly* and then takes the remainder — `(tail + 1) +// 32`, `(index + 1) +// BUFFER_SIZE`. The code was right while the prose describing it was wrong, so nothing an agent copied would fail; only what it *believed the operator was* would be wrong. No instrument can see that: the sourcing gate reads quantities, the constant gate reads names, and neither reads a semantic claim.

**The merge — decided by Stephen and applied the same day (`19385b66`).** Two files defining one operator is what the project's single-definition-home discipline exists to prevent (`architecture/pin-drive-configuration.yaml` declares its own non-home status explicitly for the same reason). The recommendation put to him was to keep `op_addmodulo.yaml` — it carried the correct terse definition and matches the naming convention of the other 74 operator files — and fold in `modulo_add.yaml`'s richer material. **He agreed, and that is what shipped.**

- `op_addmodulo.yaml` is the **definition home**: +156/−3, gaining 13 top-level keys and losing none. The worked ring-buffer patterns came across intact — `(index + 1) +// BUFFER_SIZE`, the head/tail distance idiom, and the power-of-2 `&`-mask comparison.
- `modulo_add.yaml` is a **32-line redirect**, not a deletion. Its index key `p2kbSpin2OpModuloAdd` **is in the published `v1.17.0` set**, and removing a published key breaks any consumer that cached it. The file states its `definition_home:` and one true sentence in place of a conflicting definition.
- Result: **one definition, two resolvable keys, no conflict.** Verified against the emitted index — `+//` resolves to `["p2kbSpin2OpModuloAdd", "p2kbSpin2OpOpAddmodulo"]`, the redirect and the home.
- Four keys were deliberately **not** carried over: `created`, `documentation_level`, `documentation_source: code_analysis` (the very token this entry's class sweep flagged), and `references` — which held *"P2-OctoSerial: Extensive use in circular buffers"*, *"Spin2 documentation: Arithmetic operators"* and *"Production code patterns from Iron Sheep Productions"*, three pointers and not one locatable citation. The home file carries a real one in their place.

**Why `PENDING-VALIDATION`.** Nothing is owed on the source side. The served index is the published one, so this reaches no agent until the set is pushed; the validation owed is the post-publish probe that `+//` resolves to the home. *(Re-graded 2026-09-09 during the ledger re-derivation: this entry had stood at `PARTIAL` saying "two files still define one operator … the call is Stephen's" **four days after he made the call and the merge landed**. The artifact was right and the register was stale — read the tree, not the status line.)*

**Class sweep, run:** only two files in the whole set carry `documentation_source: code_analysis` — this one and `architecture/multi_resource_management.yaml`. The latter documents an architectural *pattern*, not a language fact, so code analysis is a legitimate provenance there and it is **not** a finding. No other file calls `//` unsigned or references `%%`.

---

## Every Spin2 operator and special symbol is unreachable by the token an agent actually reads in source: 0 of 62 are in the index (2026-09-05, codegen findability audit) — F-401

### F-401 — the index harvests four name fields and `operator:`/`symbol:` are not among them, so `+//`, `:=`, `<=>`, `^@`, `??` resolve to nothing — `RESOLVED`

> **VALIDATED 2026-09-09 on the published server** — v1.18.0 pushed (tag `v1.18.0` → `0be06925`); `p2kb_refresh` returned 1133 entries / 2950 aliases, and the probes ran against the live index: `p2kb_find("+//")` → 2 keys, `p2kb_find("UHEX_LONG_ARRAY")` → the arrays page, `p2kb_find("pullup")` → `p2kbArchPinDriveConfiguration`, and `p2kb_get("p2kbArchIoPinTiming")` returns the `dc_characteristics` block. The served index file is byte-identical to `origin/main`.

**Location:** `engineering/tools/generate-p2kb-index.py`, `harvest_aliases_from_yaml()` (the harvester), against `deliverables/ai/P2/language/spin2/operators/` (77 files) and `language/spin2/special-symbols/` (13 files).

**What is wrong.** The harvester reads exactly four fields — `aliases`, `pattern_id`, `instruction`, `method`. The operator and special-symbol files name themselves in `operator:` and `symbol:`, which it does not read, and their symbolic value can never appear in the path-derived camelCase index key either (`op_addlteqgt.yaml` → `p2kbSpin2OpOpAddlteqgt`; the token is `+<=>`). Measured across the whole shipped set: **62 distinct pure-symbol names — `:=` `==` `+/` `+//` `<=>` `+<=>` `#>` `<#` `@` `@@` `^@` `~` `~~` `??` `..` `? :` and 46 more — and 0 of the 62 appear in the index in any form.**

**Evidence.** Live against the published index, not reasoned: `p2kb_find("+//")` matches nothing and falls back to dumping all 59 categories / 1,129 entries — the undifferentiated-directory response. Contrast the word-named population, which is healthy: **560 of 560** mnemonic/method names (every PASM2 instruction, every Spin2 method) resolve by name, 0 misses. The defect is confined to symbolic tokens, and they are precisely the tokens an agent meets when reading or generating Spin2 source.

**The fix is known to work.** The alias table already carries 161 punctuated keys and the matcher resolves them exactly: `p2kb_get("#32201")` returns `"resolved_from": "#32201"`. So punctuation survives both the index and the query path; adding `operator:` and `symbol:` as harvest sources is sufficient, and needs no matcher change.

**Proposed correction.** Add `operator` and `symbol` to `harvest_aliases_from_yaml()` alongside the existing four (+62 tokens). Then `keyword` (36 files), `directive` (24), `register` (17), `concept` (27), `name` (32), `component_name`, `title` (39) — which together cover **246 of the 452 files currently reachable by neither alias nor category**. Nested-name files (`object_metadata.title`/`object_id`, 131 OBEX objects; `quick_byte.*`, 42) need one level of descent and should be judged separately, since OBEX has its own `p2kb_obex_*` retrieval path.

**Scale, for prioritisation.** 452 of 1,133 files (39.9%) are reachable by neither an alias nor a category; 576 are in no category at all. The index's per-file record is `{path, mtime, sha256}` — no title, no description — so there is no content-level retrieval to fall back on. Everything rests on aliases, keys and categories.

**APPLIED 2026-09-05, in TWO passes.** Pass 1 (`ba24f0f9` harvester + `d55b6c7f` index) harvested twelve name-bearing scalar fields; `group:` was excluded on measurement (11 files, 2 distinct values — collisions, not lookups). Pass 2 (`19385b66` + `da896073`) answered *why the residue was dark*: those files were **not missing data** — they named themselves in fields the harvester did not read, because **the field a file uses follows its subtree's convention rather than one house style** (`variable:` for CLKFREQ/CLKMODE/VARBASE, `topic:` for Operator Precedence, `construct:` for Inline PASM2 and ten siblings, `statement:` for DEBUG, `register_name:` for PTRA, `fundamental:` for three language fundamentals). Nine more fields harvested, every value read first. `fundamental_concept:` was deliberately **not** harvested — it holds multi-paragraph prose, and reading it would put whole essays in the alias table. Thirteen files carried no name anywhere and got a hand-authored `aliases:` block instead.

Measured in the emitted artifact, against the index each pass replaced:

| | before (at `v1.17.0`) | after pass 1 | **after pass 2 — HEAD** |
|---|---|---|---|
| pure-symbol names in the index | **0 of 62** | 62 of 62 | **62 of 62** |
| files reachable by an alias | 591 (52.2%) | 916 (80.8%) | **955 (84.3%)** |
| files reachable by neither alias nor category | 452 (39.9%) | 206 (18.2%) | **173 (15.3%)** |
| alias entries | 2,082 | 2,660 | **2,896** |
| aliases lost | — | 0 | **0** |

**Every one of the 173 that remain is under `community/`** — 131 OBEX objects and 42 Quick Bytes, which name themselves one level down (`object_metadata.title`, `quick_byte.*`) and have their own `p2kb_obex_*` retrieval route. **Outside `community/` the count is zero.** *(Re-derived from the emitted index 2026-09-09; the two right-hand columns are that measurement. The single-column table this entry carried until then recorded pass 1 only and was never updated after pass 2 — the same status-lag as F-402, in numbers rather than in a status token.)*

**Two named seams in pass 2, both worth carrying.** The **DEBUG formatters** were the largest single gap — `UDEC`, `SDEC`, `UHEX`, `SHEX`, `UBIN`, `SBIN`, `FDEC` and their `_BYTE`/`_WORD`/`_LONG` variants resolved to **nothing**, and those are among the most-typed names in Spin2 work. (The composite `_<size>_ARRAY` forms were still missed by that pass and are **F-404**.) And `symbols/streamer-symbols.yaml` got the treatment `spin2-builtin-symbols-complete.yaml` had already had: its **78** `X_*` constants are defined one level down under `symbol:` keys, so neither they nor the file were reachable — `X_RFBYTE_1P_1DAC1`, `X_IMM_32X1_LUT` and `X_ALT_ON` all resolved to nothing, while `X_PINS_ON` and `X_WRITE_ON` resolved only because `pin-selection.yaml` happens to list those two by hand. **These constants are what a streamer command word is composed from, and composing one wrong is silent.** Its `total_symbols` also read **82 against 78 actual records**; corrected — the same class as the `1224`-vs-136 the symbols file carried.

F-376's third silent exit-0 is closed in the same function: a harvest failure now returns its reason and the generator refuses to emit rather than reporting success over a file that is present-but-unfindable. Proven with a negative control — a planted malformed YAML gives exit 1, names the file and the parser error, and leaves the existing index byte-identical.

**Why this is `PENDING-VALIDATION` and not `RESOLVED`:** the served index is the published one, so none of this reaches an agent until the set is pushed. The validation owed is a post-publish probe — `p2kb_find("+//")` returning the operator file instead of dumping 59 categories.

**Still open, deliberately out of these passes:** **173** files remain dark, and pass 2 closed the residue this line used to name. 131 OBEX objects and 42 Quick Bytes name themselves one level down (`object_metadata.title`, `quick_byte.*`) and OBEX has its own `p2kb_obex_*` route, so they are likely not dark in practice; **the ~33 files that carried no name field at all were given hand-authored `aliases:` blocks in pass 2**, which is why 206 became 173 and why the remainder is now exactly the `community/` population. Reading a *nested* name is a different change from reading a scalar field that was already there, and it needs its own decision — not to be started unasked.

**Not introduced by the unpublished delta, and not fixed by it.** Identical at `v1.17.0` and at HEAD: 62 symbols absent in both. The delta moved file-level darkness 461 → 452 (40.8% → 39.9%), which is real but is not this. Related: F-116 (hardware findability, closed — `hardware/` is now 0% dark, 29/29 reachable) and F-376's `except Exception: pass` in the same harvester, which silently drops a malformed file's aliases (task «#339» item 3) — the two touch the same function and should be fixed in one pass.

---

## The 409-citation read, run to the end: 721 locators opened at their cited lines, 22 repaired, and the instrument had to be repaired first (2026-08-30, release fix pass step 3) — F-399

### F-399 — every citation locator in the shipped set now resolves AND its cited line supports the claim it carries; F-377's class is closed by reading, because nothing else can close it — `RESOLVED`

**This is the discharge of F-377 and of the census's category-1 "409".** F-377's finding was that a locator can be **in range, non-blank, and still point at the wrong line**, and that no instrument in this project can see that. The only closure available is to open every cited line and read it. That has now been done.

**MEASURED TOTAL: 721 citation locators, in 83 shipped files, citing 40 source documents.** Every one was opened. The evidence is not truncated: the per-file counts are reproducible from the extractor described below.

The census counted **424** locators and **409** in the "resolvable" class. The number here is larger for three reasons, all benign: this extractor binds **bare continuation locators** (`", :1565"`) that the census's count did not enumerate separately; it expands a multi-locator token (`path:9-19` plus its trailing `:99-115`, `:114`) into one record each; and roughly thirty citations were added by the repairs in this same release. The classes are the same; the granularity is finer.

---

### The instrument had two defects, and both had to be fixed before any count could be trusted

The census's appendix names the §1 method but ships no script, so the extractor was written for this pass. Two defects surfaced immediately, and **either one alone would have produced a confidently wrong measurement.**

**1. `str.splitlines()` breaks on FORM FEED, and these sources are full of them.** Python's `str.splitlines()` splits on `\x0c` (and `\v`, `\x1c`, `\x1d`, `\x1e`, `\x85`, ` `, ` `) in addition to `\n`. **117 of the ingested source files disagree with `grep -n` about their own line count** — `p1-propeller-manual-v1.2-layout-text.txt` by **+398** lines, `p1-PE-Kit-Labs/122-32305-PE-Labs-Fundamentals-text.txt` by +232, `pasm2-manual-narrative.txt` by +161, `p2-documentation.txt` by +122, `spin2-v51/spin2-text.txt` by +56.

These are PDF-derived captures; the form feeds are page breaks. **The citations were written by agents reading with `grep -n` / `sed -n`, and a human verifying one uses `sed -n 'Np'` — so newline-only is the TRUTH SIDE, and any Python tool that uses `splitlines()` reads a different line than the citation means.** Under `splitlines()` the extractor reported **14** citations landing on blank lines; with newline-only splitting the true figure is **6**. Eight "defects" were the instrument's own.

This is the `feedback_scope_an_instruments_truth_side` shape exactly: the instrument and the thing it measures have to agree about what a line *is* before any verdict it issues means anything. **Any future tool that resolves a `path:line` citation against these sources must split on `\n` only.**

**2. A bare continuation locator cannot be bound to its file without a rule, and this corpus writes locators on BOTH sides of the path.** The dominant form is `path:N, :M, :K` — locators follow. But a second form trails the attribution: both `basic-io.yaml` files wrote *"features summary p.2 :107,:117; Special-Purpose Registers table p.13 :579-586 ... -- <path>p2-datasheet-text.txt"*, with every locator BEFORE the file it belongs to, and the previous scalar ending in a different filename. Nearest-token binding and preceding-token binding each mis-bind a different set, and both mis-bound this one.

**Where a locator could not be bound without guessing, the CITATION was rewritten**, not the tool — a citation whose file attribution is ambiguous to a careful reader is a citation defect, and the same ambiguity is what would mislead an agent chasing it. Fixed in `language/pasm2/concepts/basic-io.yaml`, `language/spin2/concepts/basic-io.yaml` and `architecture/streamer/pin-capture.yaml`.

---

### What the read found: 22 locators repaired across 12 files

| class | count | |
|---|---|---|
| **points at content that does not support the claim** | **18** | the F-377 shape; in range, non-blank, invisible to every gate |
| lands on a blank line | 1 | `clock_system.yaml` cited `part3-interrupts.txt:520`; the HUBSET clock-mode line is `:521` |
| names a file that resolves to nothing | 2 | `edge-standard-module.yaml` and `edge-32mb-module.yaml` each cited a bare `narrative.txt` |
| ambiguous — the basename exists under two source folders | 1 | `pin-drive-configuration.yaml` cited `complete-tables-reference.md:326-338`; that name is under **both** `p2-datasheet/` and `p2-hardware-manual/`, and F-367 established two same-named documents can differ |

**Ten of the eighteen were the F-365 carry-over shape** — `p2-documentation.txt` line numbers attributed to `silicon-doc-text.txt`, in `architecture/streamer/pin-capture.yaml` (5) and `architecture/streamer/pin-selection.yaml` (5). Some landed in range on unrelated content (line 3604 is CORDIC example code); some were past the end of the file. **The claims were right in every case; only the locators were wrong** — which is precisely why the range check reported zero and why F-377 said no tool can see this.

**The other eight, each found by reading and by nothing else:**

- `p2an002-cordic-for-real-work.yaml` — the CORDIC solver summary was sourced to `:434` (COGID and COG RAM) and the GETQX/GETQY no-result event to `:5145` and `:5401` (the RDLUT and MERGEW encoding tables). Correct: `:3304`, `:3315`, `:2054`, `:2291`, `:3413`.
- `architecture/locks.yaml` — LOCKRET's datasheet row cited as `:1794`. That line is **`into C.`**, a wrapped continuation of the LOCKREL row above it. LOCKRET is `:1795`. **A wrapped table row is its own defect class**: the PASM2 tables in `p2-datasheet-text.txt` wrap a long description onto the line *above* its mnemonic, so an off-by-one lands on a neighbouring instruction's prose and still reads like a table row.
- `architecture/lookup_ram.yaml` — `:1831` cited as if it were a LUT instruction row. It is **RDLONG**. The LUT rows are `:2061`/`:2063`/`:2065`, which the header already carried; what `:1831` actually supports is the cog/LUT block-transfer note on RDLONG's row, and it now says so.
- `architecture/streamer/modes-reference.yaml` — the D[16] alternate-bit-order flag sourced to `:3653-3654`, which is **`jmp #loop 'loop for another sample set`**. The rule is at `:1456`.
- `architecture/streamer/dds-goertzel.yaml` — S[11:0] and the %T phase-offset bits sourced to `:4062-4095`, which is the **PWM/SMPS smart-pin mode** text; and the worked program's mode/data longs to `:4289-4305`, which is **Table 34's streamer clocks/bits rows**. They are `:1586-1600` and `:1686-1687`.

**Every replacement locator was opened and read before it was written.**

---

### Two mechanical class-checks, run corpus-wide, both now clean

Reading 721 citations one at a time finds what it finds; it does not prove a class is closed. Two checks were built to do that, and both were run over the whole set after the repairs:

1. **The carry-over detector.** For all **222** `silicon-doc-text.txt` citations, compare the claim's context against the SAME line number in `silicon-doc-text.txt` and in the superseded `p2-documentation.txt`. A locator that matches p2-documentation better is a carry-over candidate. **Result after repair: zero.** (Before repair it named exactly the sites listed above.) The one surviving `p2-documentation.txt` citation in the set — `smart-pin-11011-usb-host-device.yaml:19` — is **deliberate and correct**: it documents a sentence the DOCX capture omits, and says so.
2. **The no-shared-anchor detector.** Flag any citation whose cited text shares no distinctive token (mnemonic, `$hex`, `%binary`, number-with-unit) with its claim. **175 of 721 flagged; all 175 read individually; all sound.** The flag rate is high because prose claims citing prose legitimately share no such token — the detector is a reading aid, not a verdict.

**RESULT: 721 of 721 read. Every locator resolves — 0 missing, 0 out of range, 0 on a blank line, 0 ambiguous — and every cited line carries the claim attached to it.**

**What this does NOT certify**, and it matters: this closes the question *"is the claim supported by the line it cites?"* It says nothing about a claim that cites nothing (the Tier-2 population, F-381), and nothing about a claim that is wrong in a file with no citation defect at all — which is the class F-390, F-391 and F-395 belong to, and which has no instrument. **The delta is not the defect boundary, and neither is the citation set.**

---

## The KB told readers to feed a 5.5 V-maximum board 9 V, and that the two Edge breakout carriers cannot take accessory boards at all — both are the opposite of what the guides say (2026-08-30, release fix pass step 1) — F-395

### F-395 — `hardware-compatibility-matrix.yaml` shipped an out-of-range supply voltage and an inverted accessory-header capability; two module files carried a pin range that contradicts its own count — `RESOLVED`

**Class: a documented value that is simply wrong.** Not a citation gap — the file cited nothing
anywhere, so nothing could go red. This is the class F-390/F-391 opened, found the same way: by
reading the file, not by running an instrument.

**Three defects, all in files that no gate had ever flagged.**

**1. `external_power: "5V or 6-9V depending on carrier"`** (`hardware-compatibility-matrix.yaml:233`
as shipped). **No P2 carrier accepts a wide input.** All three guides state the same requirement
verbatim — *"Voltage input requirements: 5 VDC, absolute maximum 5.5 VDC"*:
`engineering/ingestion/sources/edge-breakout-board/edge-breakout-board-narrative.txt:53`,
`engineering/ingestion/sources/edge-mini-breakout/edge-mini-breakout-narrative.txt:55`,
`engineering/ingestion/sources/edge-module-breadboard/edge-module-breadboard-narrative.txt:61`,
each followed by a boxed *"CAUTION! Always use a well-regulated power supply and do not exceed
5.5 VDC"*. A reader taking the KB at its word applies 9 V to a 5.5 V absolute maximum.
**This is the `max_current_per_pin: 150mA` shape exactly** — an out-of-range electrical figure, in
the one number that decides what you plug in, sitting where the blocking gate structurally could
not reach it. `edge-breadboard-carrier.yaml` had *the same* wide-input claim removed on 2026-08-25
(ledger item 7, and the comment at `:59-64` records it); the sweep stopped at that file.

**2. `addon_support: "none"` / `reason: "No 2x6 expansion headers"`** for the #64029 and #64019,
plus *"Edge carriers (64029, 64019) have no 2x6 addon headers → Cannot use 64006-series add-on
boards"* under `incompatibilities`. **Every carrier has 2x6 accessory headers and takes the #64006
boards.** `edge-breakout-board-narrative.txt:39` — *"All 64 Smart I/O pins brought out to 0.1"
2x6 way P2 accessory headers"*; `edge-mini-breakout-narrative.txt:45` — the same for its 40 pins,
and `:171-177` describes the accessory headers with their 5 V output;
`edge-module-breadboard-narrative.txt:56` — *"All 64 Smart I/O pins brought out to 0.1" pin sockets
and 2x6 way P2 accessory headers"*. Our own `edge-mini-breakout.yaml:56-58` already said the #64019
takes *"the #64006-ES P2-ES Eval Board Accessory Set (eight boards)"*, so **the file contradicted a
sibling page** — the F-391 shape. **Nine sites** across five blocks carried the inversion
(`edge_carrier_compatibility` ×3, `host_pin_availability` ×2, `compact_memory_system`,
`incompatibilities`, `upgrade_paths`, and the `pin_access` column below).
Consumer cost: an agent asked "which board for add-ons?" is told to buy the Eval Board and that two
of the three carriers are disqualified. The recommendation is wrong and the reason for it is
fabricated.

**3. `pin_access: "P0-P31, P58-P63 accessible (40 pins)"`** —
`edge-standard-module.yaml:261` and `edge-32mb-module.yaml:439`. **The range and the count disagree
with each other**: P0-P31 + P58-P63 is 38, not 40. The guide says P56-P63
(`edge-mini-breakout-narrative.txt:28`), which is what makes 40. The file's own arithmetic was the
tell, and nothing checks arithmetic. `edge-32mb-module.yaml:441` compounded it with
*"PSRAM pins internal to module, not on headers"* — P56/P57 are PSRAM CLK/CE and they DO reach the
#64019's headers; it is P40-P55 that do not.

**Also corrected in the same pass:** the `combinations` table's `pin_access:` was a single bare
integer that meant the carrier's header count on some rows and the module's free-pin count on
others, so P2-EC32MB on a full 64-pin carrier read `40`. A pin budget is the product of two
independently sourced facts — what the MODULE frees and what the CARRIER brings to a header — and
both are now stated per row from their own guides, with no derived total. The unsourced `rating:`
values were **deliberately left in place**: they belong to F-374, whose class boundary is still
Stephen's call, and removing six of the thirteen would have silently moved that finding's count.

**APPLIED 2026-08-30.** All three defects corrected against the guides above, with block-level
`source:` fields added. Four gates re-run: claim-sourcing PASS (Tier 1 none), crossref 0
unresolved, constant-fidelity PASS, duplicate-keys 0 across 1132 files.

---

## F-350 corrected one file of a four-file family and no sweep ever ran — the whole fabrication set was still live in `p2-hardware-selection-guide.yaml` (2026-08-30, release fix pass step 1) — F-396

### F-396 — every fabrication F-350 removed from `p2-hardware-feature-comparison.yaml` on 2026-08-25 was still shipping, unchanged, in the sibling selection guide — `RESOLVED`

**This is the finding about the other findings.** `p2-hardware-feature-comparison.yaml:159-167`
carries a `corrections_applied_2026_08_25` block naming exactly what F-350 removed. Every item on
that list was still present in `p2-hardware-selection-guide.yaml` five days later, because F-350
was applied to the file where it was noticed and the family was never swept.

| F-350 removed from feature-comparison | still live in selection-guide | authority |
|---|---|---|
| part number `64000-ES` for the Eval Board | 3 sites (`:21`, `:27`, `:36`) | Rev C guide documents **#64000**; `-ES` is the limited-edition engineering sample (`p2-hardware-feature-comparison.yaml:83`) |
| fabricated `P2-EVAL-STD-BREAKOUT` | 2 sites (`:42`, `:57`) | the part is **#64029** |
| fabricated `P2-EVAL-MINI-BREAKOUT` | 3 sites (`:51`, `:66`, `:72`) | the part is **#64019** |
| *"USB-C programming"* | 3 sites (`:37`, `:104`, `:165`) | dual **micro-USB**; `complete-p2-eval-board-reference.md:59`, `:76`. The ingestion's own cross-source analysis already wrote *"**there is no barrel jack**"* (`p2-eval-board-cross-source-analysis.md:145-147`) |
| eval board `127x89mm` | `:221` | **3.55 x 3.55 in** (90 x 90 mm), octagonal — `complete-p2-eval-board-reference.md:62`, `:253-260` |
| carriers' wrong dimensions | `76×51mm` (`:222`), `38×25mm` (`:52`, `:223`) | #64029 = **4 x 1.4 in (101.6 x 35.6 mm)** (`edge-breakout-board-narrative.txt:64`); #64019 = **3.15 x 1.4 in (80 x 35.5 mm)** (`edge-mini-breakout-narrative.txt:65`) |
| *"All 64 pins on edge castellations"* | `castellation` ×2 (`:54`, `:247`) | the string **"castell" appears nowhere** in the #64019 guide; the carrier has four plated mounting holes and an edge socket |

**Plus one not in F-350's list:** `"VGA video output up to 1024×768"` (`:84`) — the #64006H guide
lists sockets and signal formats (`p2-eval-add-on-boards-text.txt:326-334`) and states no
resolution ceiling. `1024` appears in that source only inside a phone number.

**The structural lesson, and it is the point of this entry.** F-350's disposition read as complete
because the file it was found in was fully repaired and carries a correction record saying so. What
made it incomplete is invisible from that file: **a fabrication that reaches a family of sibling
documents is one finding with N locations, and a repair record written in one of them looks
identical to a finished sweep.** This is the standing rule
(`feedback_classwide_sweep_on_every_finding`) failing in the one place it is hardest to notice —
not a missed occurrence in a grep, but a missed *file*, in a family where the repaired file
documents its own repair.
Two consequences worth carrying: (a) a correction record belongs with the FINDING, not only in the
repaired file; (b) when a finding names a fabricated value, the sweep must run over the whole
corpus and be reported with its total, before the finding can close.

**APPLIED 2026-08-30.** All 15 sites corrected against the guides above. Gates re-run, all green.

---

## Nineteen electrical quantities shipped uncited in two hardware files; one was a derived LED current with no source, and one was an amplifier's OUTPUT rating filed as a supply requirement (2026-08-30, release fix pass step 1) — F-397

### F-397 — the census's category-1 uncited-quantity block, sourced or removed — `RESOLVED`

**Origin:** `engineering/analysis/2026-08-30-yaml-defect-census.md` §3 — 14 quantities in
`hardware-compatibility-matrix.yaml` (4 blocks) and 5 in `p2-hardware-selection-guide.yaml`
(1 block), category 1 not because they were known wrong but **because of their shape**: uncited
electrical figures in wholly-uncited files, where Tier 1 structurally cannot reach them (F-381).
Reading them found that three *were* wrong.

**Sourced as stated (kept, now cited):** LED Matrix ~4 mA per lit LED and 224 mA if all 56 were on
(`p2-eval-add-on-boards-text.txt:195-197`); Serial Host 500 mA continuous per USB socket (`:100`);
the 5 V shunt-jumper requirement (`:114`); 50 Hz flicker threshold and >180 MHz I/O switching
(`:189-191`); A/V 3.3 V LDO power selection (`:357-359`); VIO 3.3 V up to 300 mA per 8 I/O pins and
the PC-USB 500 mA / AUX-USB 2000 mA limits (`complete-p2-eval-board-reference.md:55-58`).

**Wrong, and replaced with what the source states:**
- **`"64006A (Control) - ~16mA max (4 LEDs)"`** — **no source anywhere states 16 mA.** The #64006
  guide says the Control board has four blue LEDs and four push-buttons, each on a **470 Ω series
  resistor** (`:62`, `:74-80`), and gives no current. 16 mA reads as 4 × the LED Matrix's 4 mA — a
  figure borrowed from a different board with different circuitry and presented as this board's
  maximum. **A derived electrical quantity wearing a data key is the 150 mA defect in miniature.**
  Replaced with the resistor fact and an explicit note that the guide states no current figure.
- **`"64006H (A/V Breakout) - 80mW audio amplifier"`** under `high_power:
  addon_power_requirements` — 80 mW is real (`:328`, *"Amplified Audio Out (80mW)"*) but it is the
  amplifier's **output** rating. Filed as a power *requirement* it invites a supply budget built
  from the wrong number, off by whatever the amplifier's efficiency is. A correct citation attached
  to a miscategorised quantity still ships a wrong claim.
- **`"5V @ 1A minimum (USB-C or barrel jack)"`** and **`"Additional current budget (50-500mA
  each)"`** — 1 A, 50 mA and the connector both unsourced; see F-396 for the connector.
  Replaced with the guide's actual limits and an explicit statement that the #64006 guide gives a
  current for two of its eight boards and none for the rest.

**APPLIED 2026-08-30.** All five blocks now carry block-level `source:`. `audit-yaml-claim-sourcing.py`
Tier 2 advisory 32 → 27; Tier 1 still none, so adding citations to these two wholly-uncited files did
not expose an uncited sibling block in either (the F-381 trap was checked for, not assumed).

---

## Inline PASM's real stack rule is "5 of the 8 hardware levels", and our page says "PASM doesn't use Spin2 stack" — the one number a nested inline routine needs is the one we omit (2026-08-30, debug/stack research) — F-394

### F-394 — `inline_pasm.yaml` omits the 5-level hardware-stack budget, the CALL-based entry/exit contract, and the interpreter's PTRA/PB save-restore — `RESOLVED — applied 2026-09-22 («#351»), with one sub-claim REFUTED`

> **Applied 2026-09-22.** `language/spin2/constructs/inline_pasm.yaml` now carries:
> a `hardware_stack_budget:` block — **5 of the 8 levels**, sourced verbatim to
> `spin2-v55-text.txt:812` AND `:837` ("Use up to 5 levels of the hardware stack for nested CALLs,
> including CALLs to hub RAM"), noting v55 states it on both the ORG/END and the `CALL()` surface;
> a rewritten `stack_usage` consideration explaining that exceeding it corrupts the interpreter's
> own return path and fails AFTER the block returns; and a new `entry_exit_contract` consideration
> carrying the appended-RET rule from `spin2-v55-text.txt:790` ("Your PASM code will be assembled
> with a RET instruction added at the end…") and `:796`.
>
> 🔴 **ONE SUB-CLAIM OF THIS FINDING IS REFUTED AND WAS NOT WRITTEN.** The finding asserted a
> **C/Z = 0 entry condition** attributed to v55:812. It is not there: `:788-840` — the whole
> inline-PASM section — contains no C/Z statement at all. Checked independently by the dispatched
> agent and by the arbiter. Rather than assert it, the file now carries an explicit
> `not_stated_by_any_source_we_hold:` entry telling the reader NOT to assume C or Z are cleared,
> set, or carried in. **Do not restore the C/Z claim without a source.** The PTRA/PB save-restore
> half is likewise unwritten: its only evidence is the interpreter listing, and the copy in this
> repo is **v51, not the v55 the finding quotes**.

**Class: OMISSION — three facts, each stated plainly in a source, each load-bearing for anyone writing
inline PASM that nests, parks, or touches the pointer registers.**

`deliverables/ai/P2/language/spin2/constructs/inline_pasm.yaml:299-301` is the file's entire treatment
of the subject:

```yaml
  - consideration: "stack_usage"
    description: "PASM doesn't use Spin2 stack"
    solution: "Manual stack operations if needed"
```

True and useless. The rest of the file is strong — the `$000..$11F` code area, the `$1E0..$1EF`
16-variable buffer, the `$100..$11F` multitasking-taskptr overlap, the `$120..$1D7` / LUT
`$010..$1FF` avoid-list are all correct and well cited. These three are missing:

**1. Inline PASM gets 5 of the 8 hardware stack levels, not 8.** Spin2 v55 states it twice, once for
inline PASM and once for `CALL()`: *"Use up to 5 levels of the hardware stack for nested CALLs,
including CALLs to hub RAM"* (`sources/spin2-v55/spin2-v55-text.txt:812` and `:837`). The interpreter
holds the other three across the block. **This is the practical form of G-028** — the undocumented
9th-push behaviour becomes an undocumented **6th**-push behaviour the moment code is inline, and the
budget is small enough to reach by accident in a three-deep helper chain.

**2. Inline PASM is entered by CALL, and that is what makes it exitable — or parkable.** v55:790-797:
*"CALL the PASM code. The PASM code returns when an intervening `_RET_` or `RET` executes, or the
appended RET executes"*, and *"Your PASM code will be assembled with a RET instruction added at the
end."* Confirmed in the interpreter's `inline` routine — `call w` — and confirmed in the emitted
image: `org / jmp #$ / end` compiles to exactly two longs, the branch and the auto-appended RET
(`pnut_ts -l`, 2026-08-30). The consequence the KB should carry: **code that never returns leaves the
cog parked inside that CALL, with the interpreter suspended rather than damaged** — which is a
legitimate diagnostic instrument, not a hang (see the note on F-392).

**3. PTRA, PTRB, PA and PB are explicitly SAFE to use inside inline PASM — the interpreter saves and
restores them.** The `inline` routine's own comment says so: *"call pasm code (can use pa/pb/ptra/ptrb/
stack, C/Z=0)"*, and the code brackets the call with `mov y,pb` / `mov z,ptra` before and
`mov pb,y wc` / `_ret_ mov ptra,z` after. This matters **because PTRA is the live Spin2 stack
pointer** (F-392): without the save-restore an inline block that used PTRA would corrupt the method
stack, and a reader who knows F-392 will assume exactly that unless told otherwise. The save-restore
is also *why* the `$120..$1D7` avoid-list is not merely tidiness — `z` and `y` live there, so
clobbering that range destroys the saved PTRA rather than any abstract "interpreter state".
v55:812 additionally states the entry condition **C/Z = 0**, which the file's `flag_states` note does
not mention.

**Correction:** replace the `stack_usage` consideration with the 5-level budget cited to v55:812/:837
and cross-linked to `language/pasm2/concepts/stack_operations.yaml` (the 8-level hardware stack) and
G-028; add the CALL entry/exit contract with the auto-appended RET; add the PTRA/PB save-restore and
the C/Z=0 entry condition, and say plainly that the `$120..$1D7` rule exists to protect that
save-restore. Same treatment for the `CALL()` / `REGEXEC` surface, which shares all three facts.

---

## We tell agents to pass `-1` for "any available cog", and the silicon reads `-1` as "start a PAIR" — two cogs on one stack buffer (2026-08-30, debug/stack research) — F-390

### F-390 — `cogspin.yaml` and `coginit.yaml` document `-1` as a synonym for `NEWCOG`; it is not, and the value it actually selects launches an even/odd cog pair — `RESOLVED`

**Class: BEHAVIOUR — an agent following the KB emits code that silently consumes two cogs and gives
them one shared stack. This is a manufactured instability, in the exact class the question that
surfaced it was asking about.**

Two sites:

| file | line | text |
|---|---|---|
| `language/spin2/methods/cogspin.yaml` | 24 | `- NEWCOG or -1: Start any available cog` |
| `language/spin2/methods/coginit.yaml` | 22 | `- COGEXEC_NEW or NEWCOG (-1): Start any available cog` |

**What the sources say.** Spin2 v55's *Built-In Symbol for COGSPIN() Usage* table lists **exactly one**
symbol — `NEWCOG = %01_0000` (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1667-1669`).
v51 lists the same single value (`spin2-v51/spin2-text.txt:12516-12520`). Neither edition mentions
`-1` for `COGSPIN` or `COGINIT`. `-1` is `TASKSPIN`'s `NEWTASK` (v55:1670-1672) and P1's `COGNEW`
convention; it appears to have been carried across, and it is also the **return** value both methods
give when no cog is free — which is very likely where the confusion started (`cogspin.yaml:45` states
that return correctly).

**Proof the two are not interchangeable — `pnut_ts` v1.55.4, 2026-08-30.** The same program compiled
twice, `cogspin(-1, worker(), @stk)` vs `cogspin(NEWCOG, worker(), @stk)`, differs in the emitted
constant: the `-1` form emits the compact bytecode `$A0` (`bc_con_n1_14`, the −1..14 constant), the
`NEWCOG` form emits `$42 $10` (push byte 16). Different value, different binary, 6312 vs 6312 bytes
with the operand bytes differing from offset 6285.

**What `-1` actually does.** The Spin2 interpreter's `cogspin_` does `or x,#%10_0000` (set hubexec) and
then `coginit x,y wc` with **no masking** of the cog operand
(`Spin2_interpreter.spin2`, `cogspin_` and the `pop2` block). So `-1` reaches `COGINIT` as
`$FFFF_FFFF`, and the silicon decodes `D[5:0] = %111111`. Per the Silicon Doc's COGINIT D format
(`engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt:377-390`):

> `%x_1_xxx0` — *If a cog is free (stopped), then start it.*
> `%x_1_xxx1` — ***If an even/odd cog pair is free (stopped), then start them.***

`%111111` has D[4]=1 (free-cog search) **and D[0]=1 (pair)**, so it selects the pair form —
`silicon-doc-text.txt:413` gives `COGINIT #%1_1_0001,addr` as exactly that call. `NEWCOG|%10_0000` is
`%11_0000`, the single-cog form.

**Consequence:** `cogspin(-1, worker(), @stk)` starts **two** cogs running `worker()`, both handed the
**same** `@stk`. Two Spin2 interpreters push call frames into one buffer with no arbitration. Also,
the pair form returns the **even/lower** cog's ID, so `cogstop(id)` later stops one of the two.

**Correction:** in both files, state `NEWCOG` (`%01_0000`) as the only symbol for "any available cog",
delete `-1` as an input value, keep `-1` described as the failure **return**, and add the pair form
(`COGEXEC_NEW_PAIR` / `HUBEXEC_NEW_PAIR`) where the input values are enumerated. Sweep for the pattern
elsewhere: three lines match `NEWCOG.*-1|-1.*NEWCOG|cogspin(-1|coginit(-1` across the shipped set, and
the third (`cogspin.yaml:45`) is correct and stays.

**Bench confirmation available (not required to act):** `c := cogspin(-1, worker(), @stk)` then
`cogchk()` per cog — the prediction is two running cogs, not one.

**APPLIED 2026-08-30.** `cogspin.yaml:18-49` and `coginit.yaml:14-41` rewritten. `-1` is gone as an
input from both; `NEWCOG` (`%01_0000`) is stated as the only COGSPIN symbol, and COGINIT now carries
all six of its table's symbols including the two `_PAIR` forms it had never listed. Both files gained
a block `source:` (v55 `:1658-1665` / `:1667-1669`, v51 `:12516-12520`, Silicon Doc `:381-390`) and a
`not_an_input:` field stating what `-1` actually selects and why. `-1` stays as the failure **return**
(`cogspin.yaml:71`, unchanged and correct). **Class sweep run over all 1133 shipped files** for
`NEWCOG.*-1|-1.*NEWCOG|cog(spin|init)\s*\(\s*-\s*1`: the only surviving match is that correct return
line. Four gates re-run, all green.

---

## `HUBSET D[2]` protects nothing: the KB's write-protect bit is off by fourteen bits, and "all COG states saved" is the opposite of what the silicon does (2026-08-30, debug/stack research) — F-391

### F-391 — `architecture/hub.yaml` states a fabricated HUBSET bit position and a debug save scope the Silicon Doc contradicts — `RESOLVED`

**Class: BEHAVIOUR (the bit) + FABRICATION (the save scope).**

Two claims in `deliverables/ai/P2/architecture/hub.yaml`:

| line | shipped text | what the source says |
|---|---|---|
| 33 | `protection_bit: "Set via HUBSET D[2]"` | **W is D[16]**; `L` is D[17]; `D[15:0]` are the per-cog debug enables |
| 225 | `state_preservation: "All COG states saved on debug entry"` | **only registers `$000..$00F`**, and only if the ROM entry routine is used |

**Authority — Silicon Doc v35 Rev B/C, *Write-Protecting the Last 16KB of Hub RAM and Enabling Debug
Interrupts*, `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt:2743-2774`:**

> `{#}D = %0010_xxxx_xxxx_xxLW_DDDD_DDDD_DDDD_DDDD`
> `%L:` *Lock W and D bit settings until next reset*
> `%W:` *Write-protect last 16KB of hub RAM … 1 = Last 16KB of hub RAM disappears from its normal
> range and is write-protected at `$FC000..$FFFFF`, except from within debug ISR's*
> `%D:` *Debug interrupt enables for cogs 15..0*

The worked examples at `:2765-2772` confirm the field positions: `$2000_0001` = enable cog 0 only;
`$2001_FFFF` = all 16 cogs **+ write-protect**; `$2003_00FF` = cogs 7..0 + write-protect + **lock**.
`D[2]` is inside the cog-enable field — a `HUBSET` built from the KB's sentence would land in the
`%0000` clock-configuration opcode entirely, not the `%0010` protection opcode.

**On the save scope**, `silicon-doc-text.txt:2427-2431` and Table 25 (`:2442-2477`): the ROM routine at
`$1F8` saves **`$000..$00F` only**, to `$FF800 + !CogNumber << 7`. `architecture/debug_interrupt.yaml`
already carries this correctly ("*Nothing preserves PA, PB, PTRA, PTRB or any other register
automatically*"), so `hub.yaml:225` also **contradicts a sibling KB page**.

**Correction:** replace `protection_bit` with the operand format and the `L`/`W`/`D` field map, citing
`:2743-2762`; replace `state_preservation` with "registers `$000..$00F` only, via the `$1F8` ROM
routine — see `architecture/debug_interrupt.yaml`", and link the two pages.

**APPLIED 2026-08-30.** `hub.yaml` `write_protection` now carries the full operand format
`%0010_xxxx_xxxx_xxLW_DDDD_DDDD_DDDD_DDDD` with W=D[16], L=D[17], D[15:0] as the per-cog enables, plus
the three worked examples, sourced to `silicon-doc-text.txt:2743-2762` and `:2765-2772`.
`debugging.state_preservation` now states `$000..$00F` ONLY, via the `$1F8` ROM routine, saved to
`($FF800 + !CogNumber << 7)` and restored by `$1FD`, with an explicit "nothing else is preserved
automatically" — sourced to `:2427-2431` and `:2437-2439`. The two pages are linked:
`related_components` gained `architecture/debug_interrupt.yaml`. Four gates re-run, all green
(crossref 0 unresolved, so the new reference resolves).

---

## A streamer count of `$FFFF` is PERPETUAL, and our own stated bound points a reader straight at it (2026-08-30, P2KB-GAPS-RUNNING-LOG GAP-3) — F-382

### F-382 — `p2kbPasm2Xinit` gives the chunk bound as `longs * 32 < 65536`, which admits the one value that means "never terminate" — `RESOLVED — verified applied 2026-09-22 («#351» drain)`

> **Verified in the tree 2026-09-22, not from the record.** `language/pasm2/xinit.yaml:105-107` now
> states `$FFFF` = PERPETUAL streaming and "The largest TERMINATING count is `$FFFE`", and the bound
> reads `longs * 32 <= 65534`. The `CONFIRMED` status had been lagging the tree.

**Class: BEHAVIOUR — measured by the reporter, re-verified here against the tree.**

`language/pasm2/xinit.yaml:105` states:

> *"Maximum block per XINIT for bit-counted streamer modes: 2047 longs (65504 bits). The streamer's
> bit-count field is 16 bits, so transfers in bit-granularity modes must satisfy `longs * 32 < 65536`."*

`< 65536` admits **65,535 = `$FFFF`**, and `$FFFF` in the count field is the **perpetual/continuous**
encoding — the streamer runs without terminating the chunk. **A chunk chain written to our documented
rule and sized at its stated ceiling silently collapses to its remainder.** The reporter's did: a
7-chunk chain became one chunk of 32,771 samples. Their `CAP_CHUNK_MAX` is now `65_534` (`$FFFE`)
with the reason recorded at the constant.

**Verified here 2026-08-30:** the bound reads exactly as quoted, and a corpus-wide grep for any
statement associating `$FFFF` with perpetual or continuous streaming returns **nothing** — the
encoding is documented nowhere in the shipped set.

**Why this is ours and not the reporter's carelessness.** The KB's own arithmetic points *at* the trap
value, and the `large_transfer_chunking` worked example is safe as written (`bmask x, #10` caps at
2047 longs = 65,504 bits) — **so the hazard is invisible from the page, because the example never
reaches the value that breaks.** Their run sheet records the judgement at the time: *"No amount of
care against the KB alone would have caught this."*

**Correction.** State on `p2kbPasm2Xinit` and in the modes reference that **`$FFFF` in the count field
selects perpetual/continuous streaming**, and correct the bound from `longs * 32 < 65536` to a maximum
count of **`$FFFE`** for terminating transfers. Source the perpetual encoding from the Silicon Doc
before writing it — the reporter measured the behaviour; we have not yet located the documentary
statement.

---

## Two pin-reading questions the KB discusses in detail and never answers (2026-08-30, P2KB-GAPS-RUNNING-LOG GAP-1/GAP-2) — F-384

### F-384 — nothing states what the streamer INPUT samples, or what a live smart pin does to it; and AAAA's "read state" is undefined for a smart-pin neighbour — `DONE` (verified 2026-10-05 «#386»: pin-capture.yaml and smart_pins.yaml in_signal_semantics, v1.23.3)

**Class: BEHAVIOUR — empirically settled by the reporter, needs our own sourcing before it ships.**

**What they measured.** A silicon edge counter reading its own pin level through a jumper from SCK
counted **4,736 rises on every one of six sector reads**, decomposing exactly as an SPI sector read
must: 512×8 = 4,096, CRC16 adds 16 → 4,112, and the remaining 624 is CMD17 + R1 + token poll +
trailing clocks. **Two pre-registered self-tests ran first** — a DC level check, then 137 deliberately
driven edges counted as exactly 137 — so the mechanism was proven before the measurement. The counter
failed **only** when aimed *through* a pin driven by a live smart pin.

**The consequence, and it is unsignposted:** a pin whose smart pin cannot be disabled — `SCK` running
`P_TRANSITION`, because it generates the clock — **cannot be read correctly by the streamer at all**,
and no software routing repairs it, because routing only moves `IN`.

⚠ **And the page that should carry this grew without it.** `p2kbPasm2StreamerSmartpinControl` gained
`bit_edge_lockstep` and `alignment_pad`, both marked GOLDEN, and `alignment_pad` is explicitly about
**the streamer sampling an input pin** at exactly this use case. `pin_output_hierarchy` on that page
and on `p2kbArchSmartPins` remains **output-only**. So the KB now discusses the streamer reading an
input pin in detail and still never says what it reads or that a live smart pin on that pin corrupts
it. **A reader arriving via `alignment_pad` — the most likely route for anyone doing SPI capture — is
given the timing and not the hazard.**

**GAP-2, related and still open:** `p2kbArchSmartPins` → `aaaa` reads *"relative +1 pin's read state"*
with **"read state" undefined for a neighbour running a smart-pin mode** — which is the same question
one level down.

**Correction.** State, in the streamer overview and again in `alignment_pad` where the reader already
is, what the streamer input path samples and what a live smart pin does to it, with the corollary that
pins whose mode cannot be disabled are not capturable. Define "read state" on the AAAA table for the
smart-pin case. **Both need a documentary or EF-ledger source before shipping — the reporter's
measurement is the lead, not yet our citation.**

---

## `p2kbArchStreamerPinSelection` names one field three different ways, and the streamer symbols never got the composition rule the smart pins did (2026-08-30, P2KB-GAPS-RUNNING-LOG AMBIGUOUS-1) — F-385

### F-385 — `D[19:16]` vs `D[19:17]` vs `D[22:17]` on one page, and mode constants that collide with the pin-base field — `DONE` (verified 2026-10-05 «#386»: pin-selection.yaml composition rule and field split, v1.23.3)

**Class: AMBIGUITY — no instrument can see it; a reader cannot construct a mode word without guessing.**

**Verified here 2026-08-30 in `architecture/streamer/pin-selection.yaml`:** the header comment at `:2`
says *"D[22:20] pin group and **D[19:16]** sub-pin selection"*; `:15`, `:98` and `:114` also say
`D[19:16]`; but `:74` defines the field as ***"D[19:17]**, the low three bits of the six-bit pin number
in **D[22:17]**"* and `:76-78` explains that reading well. Separately `:179-180` assigns **`D[16]`** to
the `%a` alt bit — a bit the header's `D[19:16]` claims for the sub-pin field.

**The body's explanation is now good.** The residual defect is that four sites still say `D[19:16]` and
contradict it, including the header comment a reader meets first.

**What it costs:** the reporter's four signals sit on **P58–P61, straddling a 4-pin boundary**. Under
the aligned reading a 4-pin capture at base 58 silently captures 56–59, dropping CS and SCK — no error,
plausible meaningless data.

⭐ **And there is a precedent we have already accepted on the other side of the chip.**
`p2kbArchSmartPins` now carries a `composition_rule` — *"COMBINE PIN-MODE CONSTANTS WITH `|`, NEVER
`+`… The P_* constants are BIT FIELDS positioned inside the WRPIN mode word, not additive flags…
There is no error and no warning — the pin simply does something else"* — backed by measured silicon
(EF-054). **The streamer side has the identical hazard undocumented:** `X_8P_4DAC2_WFBYTE = $E006_0000`
sets bits 17 and 18, inside the pin-base field, and our own examples compose with `+` —
`pin-selection.yaml` shows `mode + 8<<17`, and `streamer-symbols.yaml:425` shows
`X_RFWORD_RGB16 | X_PINS_ON | X_DACS_3_2_1_0 + base<<17 + 640`, **mixing both operators in one line.**

**Correction.** Reconcile the four `D[19:16]` sites to the `D[19:17]` / `D[22:17]` model the body
already explains, starting with the header comment. Give the streamer symbols the same
`composition_rule` treatment the smart-pin constants received: which bits each mode constant occupies,
and what `+` does when the base collides with them. Add a **misaligned**-base example — the current one
is aligned, which is precisely why it does not disambiguate.

---

## `X_PINS_ON` and `X_WRITE_ON` are one bit listed as two controls, and the file that resolves it is a different file (2026-08-30, P2KB-GAPS-RUNNING-LOG AMBIGUOUS-2/3) — F-388

### F-388 — `streamer-symbols.yaml` lists both at `$0080_0000` under separate headings with no cross-note — `RESOLVED — verified applied 2026-09-22 («#351» drain)`

> **Verified in the tree 2026-09-22.** `language/spin2/symbols/streamer-symbols.yaml:417` and `:429`
> each carry the reciprocal cross-note ("SAME BIT as X_WRITE_ON — D[23] is one enable whose meaning
> follows the mode… They are not two independent controls"), and both symbols were retained as the
> finding required.

**Class: AMBIGUITY.**

**Verified here 2026-08-30:** `language/spin2/symbols/streamer-symbols.yaml:311-312` gives
`X_PINS_ON = $0080_0000` and `:323-324` gives `X_WRITE_ON = $0080_0000`, under separate headings, as
though they were independent controls. `architecture/streamer/pin-selection.yaml` resolves it — one
bit `D[23]`, meaning *"enable pin output"* in output modes and *"enable WRFAST"* in capture modes —
**in a different file.** A reader working from the symbol list will reasonably conclude they are
independent and can be combined.

**AMBIGUOUS-3 (`X_ALT_ON` scope) is folded here** and carries a correction the reporter made against
their own log: their original entry described a contradiction *between two pages*; the text has since
moved and the entry pointed at the wrong file. Re-derive the current state before acting on that half.

**Correction.** Cross-note the two symbols in `streamer-symbols.yaml` — same bit, mode-dependent
meaning — pointing at the page that carries the full explanation. Do not delete either symbol; both
spellings are real and both appear in Parallax material.

---

## The SETXFRQ increment rule is quoted in three files and applied in none of their pixel-rate tables — 9 wrong NCO words in the shipped KB, 8 more in a released manual (2026-08-29, «#332» release-review recomputation) — F-380

### F-380 — `SETXFRQ` values computed by truncation or by `round()`, where the source requires truncate-then-increment — `RESOLVED — validated on the served KB 2026-09-11`

**The rule, read at the line.** *Parallax Propeller 2 Documentation* v35, Streamer NCO —
`engineering/ingestion/sources/silicon-doc/part2-pixel-ops.txt:104-117`, with the footnote at
`:117` continuing at `:121` (one sentence, split by a page break):

> "For fractions with remainders, the computed D/# value should be incremented, in order to
> produce proper initial rollover behavior."

The source's own table shows it applied: `1/3` is given as `$2AAA_AAAA+1`, `1/5` as
`$1999_9999+1`, `1/6` and `1/7` likewise, while the exact divisions `1/2`, `1/4` and `1/8` carry
no increment. So the rule is **truncate, then increment when the division leaves a remainder** —
equivalently a ceiling. It is **not round-to-nearest**: a remainder below half still increments.
That distinction is the whole defect.

**What was wrong.** Every affected block *quoted or paraphrased the correct rule* and then failed
to apply it to its own numbers. Nothing detected this: the values are well-formed hex in the right
magnitude, they carry citations, and an off-by-one in bit 0 of a 31-bit phase word is invisible to
every gate we run.

*Shipped KB — `language/pasm2/setxfrq.yaml`, 2 of 4 `common_values`:*

| target @ 250 MHz | rule | shipped |
|---|---|---|
| 25.175 MHz | `$0CE3_BCD4` | `$0CE3_BCD3` |
| 44.1 kHz | `$0005_C7C1` | `$0005_C7C0` |

The other two (`$0CCC_CCCD`, `$0006_4A9D`) were right, and their `arithmetic:` notes said
"remainder rounded up per the source footnote" — the two wrong ones carried no such note. That is
the signature: the increment was applied where someone wrote it down and skipped where they did not.
The file also stated **two different rules** — `computation:` said `D = round(...)` while `source:`
quoted the round-up footnote — and its `cross_checked_against:` cited `nco-timing.yaml` as
agreement, which was self-corroboration: that file carried the same wrong value.

*Shipped KB — `architecture/streamer/nco-timing.yaml`, 7 of 12 `video_rates`:* 25.175 MHz at all
three system clocks (`$0CE3_BCD4` / `$0ABD_C806` / `$0A11_EB86`), 40.000 MHz @ 300 (`$1111_1112`),
65.000 MHz @ 250 (`$2147_AE15`), 74.250 MHz @ 250 (`$2604_1894`) and @ 320 (`$1DB3_3334`). The
same file's `common_values` ratio table is **fully correct at all 8 ratios** and its
`frequency_calculation.note` stated the rule — the file applied it in one block and not the other.

*Released manual — `p2-streamer-programming-guide` v1.1.0 (published 2026-08-22, 91pp), 8 of 18
values in Appendix C's "Common Video Pixel Rates" table,* plus the rule stated as
`round($8000_0000 * pixel_rate / clock_frequency)` in **three** places (the §-body prose, the
worked Example 2, and the table caption). The worked example prints
`word = round($8000_0000 × 25.175 / 250) = $0CE3_BCD3` — teaching the wrong rule and the wrong
result in one line. Wrong rows: 640×480 @25.175 (all three clocks), 720×480 @27.000 MHz @300,
800×600 @300, 1024×768 @250, 1280×720 @250 and @320.

**How it surfaced.** The 2026-08-27 release review flagged `setxfrq common_values` as a two-value,
two-file residue (§0.5 item 13 of the change ledger). Recomputing the whole class rather than the
two named values found 9 wrong in the KB and 8 more in a released manual — the ledger's count was
low because it checked the values the differential read had named, not the class.

**Applied 2026-08-29 («#332»).** All 9 KB values corrected; both files' rule statements rewritten
to state truncate-then-increment explicitly, with the citation and the page-break note; the
`round()` wording removed from `setxfrq.yaml`'s `computation:`, its top-level `description:` and
`frequency_formula.formula`; the self-corroborating `cross_checked_against:` rewritten to say the
source is the authority, not the agreement; a `derivation:` block added to `nco-timing.yaml`
`video_rates` naming which two entries divide exactly; and `nco-timing.yaml`'s note changed from a
list of special cases (1/3, 1/5, 1/10) to the general rule. Manual master
`manuals/p2-streamer-programming-guide/opus-master/streamer-body.md` corrected at all 8 values and
all 3 rule statements — **the workspace render was NOT edited; it regenerates from the master.**

**⚠️ OWED: a Streamer Guide re-release.** The corrected values are in the master; the published
v1.1.0 PDF still carries the 8 wrong ones. Scheduling that release is Stephen's.

**Status corrected 2026-09-10: this read `RESOLVED` while its own paragraph above said a re-release
was owed.** The legend is explicit — `RESOLVED` requires the validation to have LANDED and the
artifact to have been READ; a fix awaiting its render is `PENDING-VALIDATION`. Left as `RESOLVED`,
this entry reported a reader-facing defect as closed while the shipped PDF still taught the wrong
values. That is the both-directions failure the register warns about, in its own file.

**PREPARED 2026-09-10 — v1.1.1 is staged for the release wave.** `request.json` carries 1.1.1 /
September 2026 (this manual single-sources its cover from `\DocVersion`, so that is the only
version site), and the CHANGELOG entry states the rule as truncate-then-conditional-increment.
**All eighteen Appendix C values were re-derived independently from the rule before the bump** —
`floor($8000_0000 * pixel / sysclk)` plus one where the division leaves a remainder, in exact
rational arithmetic — and matched the master at 18 of 18, with `round(` at zero occurrences. The
caption's claim that exactly three entries divide exactly (25.000, 40.000 and 65.000 MHz, each at
320 MHz) was confirmed by the same computation. Closes when the v1.1.1 PDF is rendered and read.

---


**VALIDATED ON THE SERVED KB 2026-09-11.** `language/pasm2/setxfrq.yaml` now states the rule the source states and says which arithmetic it is NOT: *"D = (target_frequency x $8000_0000) / clkfreq, truncated, then incremented by 1 if that division left a remainder. The increment is required by the source, not an optional refinement"* (`:52`), and `:58` closes the door on the defect explicitly — *"It is NOT round-to-nearest -- a fraction whose remainder is below half still increments."* It proves the rule against the source's OWN table rather than asserting it: 1/3 is given as `$2AAA_AAAA+1` and 1/5 as `$1999_9999+1`, while the exact divisions 1/2, 1/4 and 1/8 carry no increment. `:57` cites `part2-pixel-ops.txt:104-117` verbatim and flags that the governing sentence is SPLIT BY A PAGE BREAK (:117 and :121) — which is plausibly how the increment clause was lost in the first place. `:55` carries the 2^31-not-2^32 multiplier, and `architecture/streamer/nco-timing.yaml:106` derives from the same rule rather than restating it.

**The adjacent app-note residue is clean too:** `p2an003-dac-analog-signal-generation.yaml:127` keeps its DDS phase-increment arithmetic explicitly OUT of the sourced block — *"not statements taken from a Parallax source"* — and points at `setxfrq.yaml frequency_formula` for the rule that is sourced.
## `ADDSX` and `SUBSX` ship the PASM2 Manual's wrong C-flag sentence while contradicting it in the same file (2026-08-27, «#328» E-016 sibling sweep) — F-379

### F-379 — the two instructions v1.11.1's signed-flag repair skipped, plus two malformed `SUM*` encoding fields — `RESOLVED`

**This is the outcome the E-016 sibling sweep existed to find: the manual is wrong AND our KB followed it.**

E-016 established that the PASM2 Manual's *prose* describes the signed-add/subtract C flag one way
while the manual's *own table on the same page* says something different and more precise, and that
the table is the more precise statement. `adds.yaml` and `subs.yaml` already rebut the prose. The
sweep found two siblings that do not:

| File | `description` said | its own `flags_affected.C` / `encoding[0].c` said |
|---|---|---|
| `language/pasm2/addsx.yaml` | *"the C flag is set (1) if the result is negative (Result[31] = 1)"* | `sign of (D+S+C)` |
| `language/pasm2/subsx.yaml` | the same sentence verbatim | `sign of D-(S+C)` |

**Each file contradicted itself**, and a reader who reads the `description` — the field a consuming
agent is most likely to surface — learned the wrong quantity. It is wrong in exactly the case that
matters: `Result[31]` and the true sign differ **only on overflow**, which is the condition `TJV`
exists to detect.

**Refuted three times inside the manual itself**, so this needed no external source: Table 9 at
`sources/pasm2-manual/pasm2-manual-text.txt:912` and Table 169 at `:3983` give the true-sign form;
the manual's own `TJV` description at `:4196` (restated `:5168`) says the jump *"requires that C be
updated (to the correct sign) by the previous ADDS / ADDSX / SUBS / SUBSX / CMPS / CMPSX / SUMx"* —
which could never fire if C were `Result[31]`; and the manual's summary tables at `:4482` and
`:4809` say **"correct sign"**.

**Root cause, and it is the useful part.** Commit `87511c99` (v1.11.1, *"signed flags"*) repaired
this exact class across `adds · cmps · cmpsx · subs · sumc · sumnc · sumnz · sumz` — **and skipped
`addsx` and `subsx`**. A class-wide sweep that misses two members leaves a defect that now looks
deliberate, because every neighbour is correct.

**Two further defects in the same family, found in the same pass and fixed with it** — both
column-split artifacts from the original CSV import, both in fields no gate reads:
`sumz.yaml` `encoding[0].z` read `1 then D = D - S, else D = D + S` — the *C column's condition
text* sitting in the Z field, where the manual's Table 172 (`:4039`) gives `Result = 0`. That one
was wrong, not merely malformed. `sumc.yaml` `encoding[0].c` carried the same condition prose welded
in front of a correct C semantic. `sumnc.yaml` and `sumnz.yaml` are clean — the four `SUM*` files
are asymmetric because v1.11.1 rewrote only two of them.

**Applied 2026-08-27.** All four corrected; `addsx`/`subsx` now carry the true-sign statement in the
wording `adds`/`subs` already use, each naming the manual table that overrides the prose and pointing
at E-016. `grep -rn 'Result\[31\] = 1' deliverables/ai/P2/` returns nothing outside the new
rebuttals.

**What no gate could see.** Every instrument in this project passed all four files throughout:
they parse, their keys resolve, their citations are present, and `pnut-ts` assembles the
instructions regardless — a compiler proves legality, never a flag's meaning. Only reading the
`description` against the same file's `flags_affected` catches a file disagreeing with itself.

## The KB ships the compiler's acceptance range as a frequency ceiling, 180 MHz past the silicon limit (2026-08-27, «#326» verification) — F-378

### F-378 — `_CLKFREQ range: "3,333,333 Hz to 500,000,000 Hz"` carries no silicon limit, and a remote agent will act on it — `RESOLVED`

`deliverables/ai/P2/language/spin2/constants/special-configuration-symbols.yaml:59` gives `_CLKFREQ`
a `range:` of **3,333,333 Hz to 500,000,000 Hz**, sourced to the pnut-ts clock-configuration guide.
That figure is real, and it is the **compiler's acceptance range** — «#326» confirmed empirically
that `_clkfreq = 400_000_000` assembles clean, exit 0.

**The P2 Datasheet's AC Characteristics give the PLL absolute maximum as 320 MHz** (`3.33` min /
`180` typical / `320` max, `p2-datasheet-text.txt:2200`, with footnote 2 at `:2209` stating
*"Nominal PLL frequency (system clock speed) is 180 MHz at up to 105 °C"*).

**Why this is a defect rather than a difference.** The entry does not say which of the two it is
quoting. A remote agent reading only this entry — which is exactly how the shipped set is consumed
— will emit a `_clkfreq` up to 500 MHz, get a clean compile, and ship silicon running 180 MHz past
the datasheet maximum. Nothing anywhere in the path says otherwise: the compiler accepts it and the
KB's own stated range endorses it.

**This is E-007's rule, not a new one.** `SOURCE-ERRATA.md` E-007 settled that where two documents
frame a limit differently, the KB must **label which framing it is quoting**. That ruling was
applied to the clock limits in the Hardware Manual; it was never applied here.

**Fix.** Keep the compiler range — it is true and useful — and label it, adding the datasheet
ceiling beside it, the way «#326» did for `guides/pasm2-getting-started.yaml`
`timing_considerations.clock_frequency`. Sweep the same question across every `range:` in the
shipped set that came from a compiler guide rather than a datasheet.

**Related, and it must not be silently "corrected" back.** «#326» deliberately shipped `%01_11` for
the XI-input-plus-PLL clock mode where our own `spin2-v55-text.txt:1713` and `:1738` read
`01_1 1`. That space is **our extractor's**, not the source's: the arbiter confirmed against
`word/document.xml` that the value is one cell split across two Word runs, that it is the only one
of the nine so split, and that the literal `01_1 1` appears **nowhere** in the DOCX. Recorded in
`engineering/ingestion/sources/spin2-v55/spin2-v55-complete-extraction-audit.md`. A future pass that
"reconciles" the KB to the extraction would introduce a bit pattern that does not exist.

**APPLIED 2026-08-29 («#334»). The sweep this entry called for was run, and `_CLKFREQ` was one site
of five.** Every `range:` in the shipped set traceable to the pnut-ts guide rather than a datasheet
was checked against the P2 Datasheet's AC Characteristics table:

| symbol | shipped range (= pnut-ts acceptance) | datasheet rating | gap |
|---|---|---|---|
| `_CLKFREQ` | 3,333,333 Hz – **500,000,000 Hz** | PLL max **320 MHz** (`p2-datasheet-text.txt:2200`) | +180 MHz |
| `_XINFREQ` | 250 kHz – **500 MHz** | direct drive into XI max **200 MHz** (`:2198`) | +300 MHz |
| `_XTLFREQ` | 1 MHz – **60 MHz** "typical" | crystal max **50 MHz** (`:2199`) | +10 MHz |

Two further sites stated the compiler figure as if it were silicon:
`language/spin2/system-variables/clkmode.yaml` PLL `use_case: "High-speed operation (up to
500 MHz)"`, and `language/spin2/concepts/timing_operations.yaml`'s rollover table carrying a
**500 MHz** row — a frequency no P2 clock source is rated to reach. The rollover row is now 320 MHz
(13.4 s, 3.125 ns), recomputed.

All five now state the compiler range labelled as the compiler range, with the datasheet rating
beside it and each cited to its own line. The Parallax Propeller 2 Documentation's overclock note
is carried too — the PLL can be pushed to **350 MHz** in `VCO / 1` mode, `%PPPP = 15`
(`part3-interrupts.txt:545`) — so a reader sees the rated maximum, the documented overclock
ceiling, and the compiler limit as three different things, which is what E-007 asks for.

**Two further defects surfaced in the same files while citing them, both fixed in the same pass:**
`timing_operations.yaml` described the system counter as **32-bit**; the Silicon Doc states it was
*"extended to 64 bits. GETCT WC retrieves upper 32-bits"* (`silicon-doc-text.txt:55`), so the file
now says the counter is 64-bit and that the rollover discussion concerns the 32-bit value GETCT
returns alone. And its `minimum_resolution` block carried a `min_practical` column (~1 us / ~100 ns
/ ~50 ns / ~30 ns) plus *"Spin2 interpreter overhead adds several microseconds to any operation"* —
**no source states either and no bench result here measures them**; removed under cite-or-omit, with
a note that the overhead is real and needs a silicon measurement before the KB can give a figure.

**This pass is what produced F-381** — citing these three files promoted them out of Tier 2 and
exposed 12 always-uncited blocks as Tier-1 blocking. All 12 are now cited or removed.

## Two silent-failure bugs in the KB tooling (2026-08-26, «#324» verification) — F-376

### F-376 — `fetch-kb-file.sh -v <KEY>` fetches nothing and exits 0; the index generator swallows parse errors — `DONE` (verified 2026-10-05 «#386»: both tools fixed at HEAD)

Two unrelated bugs, same shape: **the failure is silent and the exit code is 0.**

**1. `engineering/tools/p2kb/fetch-kb-file.sh` double-shifts its verbose flag.** The
`--verbose|-v)` case runs `shift` at `:439`, and the argument loop shifts again at `:466`. So the
flag consumes the key that follows it: `fetch-kb-file.sh -v language/pasm2/add.yaml` drops the
key, fetches nothing, and exits 0. Any user or script that puts `-v` before the key gets silence
rather than an error. **Fix:** delete the `shift` inside the `--verbose|-v)` case.

**2. `engineering/tools/generate-p2kb-index.py` swallows every parse failure during alias
harvest** — the harvest ends `except Exception as e: # Silently skip files that can't be parsed /
pass` (~`:116`). A syntactically invalid YAML is still indexed with its path and sha256, silently
loses all of its aliases, and the run exits 0 printing nothing. Since `aliases:` is the mechanism
the whole KB's findability rests on, a file can go unfindable without anything saying so.
**Fix:** count and report skipped files, and fail the run if any file the index claims to cover
could not be parsed.

**Neither is in this sprint's repair scope** — both are tooling, and «#324» was a measurement task.
Recorded here so they are not rediscovered.

## The shipped set scores and star-rates hardware, which the KB entry rule excludes and no source authorises (2026-08-26, «#322» verification) — F-374

### F-374 — 40 quality-score sites across 18 shipped files state a judgement, not a fact — `RESOLVED — verified applied 2026-09-22 («#351» drain)`

> **Verified in the tree 2026-09-22.** All five named score keys return zero hits corpus-wide:
> `rating: 5_stars_*`, `educational.value`, `educational_value: 10/9`, `quality_rating:`,
> `recommendation_score:`. The surviving near-misses were checked and are legitimate under this
> finding's own scope: `educational:` blocks carrying `complexity_level`/`concepts_taught` (utility,
> not a score), `educational_value:` used as a CONTAINER for `learning_objectives`, the string
> `"educational_value"` as a comparison DIMENSION NAME, and `addon-motor-driver.yaml:155`'s
> `rating: "…32 A / 400 V"`, which is an electrical rating.

**The rule this violates** (Stephen, 2026-08-26, saved as `feedback_kb_entries_state_existence_access_utility`): a KB entry states **existence, access and utility**. Never quality commentary, never version comparison. It was given while re-scoping F-370, which had wanted to call ROM TAQOZ *"cut-down"* — and the same shape turns out to be spread across the hardware tree.

**Measured 2026-08-26 by walking every parsed node of all 1132 shipped files:**

| Key | Sites | Example value |
|---|---|---|
| `rating` | 13 | `5_stars_perfect`, `2_stars_limited`, `5_stars_professional` |
| `educational.value` | 8 | `high`, `very_high` |
| `educational_value` | 7 | `10`, `9` (under `quality_metrics`), `high` |
| `quality_rating` | 6 | `production`, `professional`, `specialized_excellent` |
| `recommendation_score` | 6 | `5` |

**40 sites, 18 files — 16 under `hardware/`, 2 under `code-examples/`.**

**Why this is a defect and not a style preference.** Two independent reasons, either sufficient:

1. **Nothing sources it.** `5_stars_perfect` and `recommendation_score: 5` trace to no Parallax document and no measurement. They are our opinion, shipped into a set whose bar is cite-or-omit. `audit-yaml-claim-sourcing.py` does not catch them because they carry no digits it recognises as a quantitative claim — a scoring adjective is an unsourced claim wearing a data key.
2. **The consumer cannot act on it.** `deliverables/ai/P2/` is read by remote agents generating code. An agent asked to pick a carrier board can do something with *"has 8 LDOs, one per 8-pin group"*; it can do nothing correct with *"5 stars"* except launder our preference into its own output as fact.

**Scope boundary — do NOT widen this sweep, and this half matters as much as the other.** The same rule *permits* utility, and the tree is full of legitimate utility statements that must survive untouched: `best_for` (6 sites), `recommendation` (20 sites, e.g. *"Use OBEX driver — do not attempt to implement HUB75 timing manually"*), and `advantages` (30 sites) all answer **what is this good for**, which is exactly the third thing an entry is supposed to state. A sweep that removes them replaces one defect with a worse one. The class here is **scores and ratings**, not guidance.

**Fix.** Per site, one of two: delete the key where the judgement carries nothing (`recommendation_score: 5` on three boards that all score 5 says nothing at all), or replace it with the sourced fact the score was standing in for — `quality_rating: production` on `edge-standard-module.yaml` is presumably reaching for something real about the module's intended use, and the board guide can say it properly.

**How this surfaced.** «#322» dropped a stray `educational_value: "excellent"` from `edge-breadboard-carrier.yaml` as a duplicate-key repair (F-360), noticed the surviving scalar was also bare quality commentary, and reported the pattern as corpus-wide. Arbiter verification measured it: a first pass matching the bare key `value` returned 299 sites and was thrown out as over-broad — most are legitimate — and the count above is the narrowed, defensible class.

## `validate-crossref-keys.py` exempts three top-level fields from resolving, and 14 shipped file paths sitting in them point at nothing (2026-08-26, «#321» verification) — F-373

### F-373 — `see_also`, `references` and `related_concepts` are typed `'text'`, so a file path in any of them is never resolved and the gate stays green — `RESOLVED — gate half landed 2026-09-13 with F-340; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **GATE HALF LANDED 2026-09-13.** A file path in `see_also`, `references` or `related_concepts` — or
> in any other string — is now resolved and fails the gate if it does not exist or is not written
> KB-root-relative. Prose in those fields stays informational. The content this finding repaired
> on 2026-09-09 is now defended, and the first run found it had already regressed in two places
> (`language/spin2/conventions/spin2-*-jonnymac.yaml` root-prefixed `see_also`) — fixed under F-434.

> **CONTENT HALF CLOSED 2026-09-09 (task «#335»).** Every unresolvable file reference in those three
> fields has been repaired across the shipped set. Re-measured after the sweep: **159 file references
> + 7 directory references, 0 broken, 0 root-prefixed, 0 globs.** Before it: **18 broken · 22 carrying
> a `deliverables/ai/P2/` prefix unresolvable as written · 3 globs = 43 sites.** Per Sacred Rule 7,
> **not one reference was deleted** — every one was redirected to where the content actually is:
>
> - **8 wrong-base** — `cogspin` → `language/pasm2/concepts/multi_cog_synchronization.yaml`;
>   `pinstart` → `language/spin2/constructs/inline_pasm.yaml` (the definition home, not the
>   `concepts/inline_pasm2.yaml` redirect stub); `streamer-symbols` and `xcont` → four
>   `architecture/streamer/` files whose `../../` relative form resolved to nothing; `labels.yaml` →
>   `language/pasm2/{jmp,call,djnz,rep}.yaml`. **`call.yaml` was ambiguous** — two files answer to
>   that basename — which is the `complete-tables-reference.md` trap F-399 closed; full paths kill it.
> - **4 to a file that never existed** — `language/spin2/methods/_index.yaml`, from the four add-on
>   board files, now `language/spin2/methods/wrpin.yaml`, the entry point all four boards genuinely
>   go through (Stephen's call, option C of three). **Authoring the real catalog is punch-listed**
>   (`engineering/document-production/PUNCH-LIST.md`) as explicitly *maybe*, not owed.
> - **2 to a retired scheme** — `manifests/P2/language/*-manifest.yaml`. Git says why: manifests were
>   part of DOD v3.0 key-based access (`e271cab0`), removed by `03189a7d`. No manifest has existed
>   since. Redirected to what carries that inventory now — the Spin2 language map, and the PASM2
>   `groups/` tree — each with the retirement recorded in place so the next reader is not left
>   guessing why a link moved.
> - **2 prose-prefixed** — `pin-power-domains.yaml` buried its paths inside a sentence
>   (`"P2 Edge standard module — the board's 8 LDOs …: hardware/edge-standard-module.yaml"`), which no
>   tool can bind. Path is now the value; the prose is a comment above it, so nothing was lost.
> - **3 globs** — `architecture/smart-pins/*.yaml` in `wrpin`/`wxpin`/`wypin` → `architecture/smart_pins.yaml`.
> - **22 root-prefixed** — the `deliverables/ai/P2/` prefix stripped in 5 files. Every one resolved
>   to a real file *after* stripping, so these were never dangling; they were **unresolvable as
>   written**, because a consumer that prepends the KB root gets `deliverables/ai/P2/deliverables/ai/P2/…`.
>
> **What remains open, and why this stays `PARTIAL`:** the **gate half**. All three fields are still
> typed `'text'`, so the validator still cannot see any of this — it was green before the sweep and is
> green after it, and it would be green again tomorrow if a broken path were reintroduced. **The
> repair is content-only and nothing defends it.** That is the same shape as F-360's armed-but-unwired
> duplicate-key gate and F-405's unrun validator: *a defect closed by a one-time repair, with no gate
> wired to the release path, is a defect scheduled to come back.*

**Not F-340.** F-340 is the **nested-traversal** blind spot, and it is *disclosed on every run*:
the banner reads `✅ ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — 692 nested site(s) NOT checked
(F-340)`. The sites here are **top-level and ARE traversed** — they are simply exempted from
having to resolve, and that exemption is disclosed nowhere. F-340's own text treats this typing
as the accepted baseline (*"should `related_documentation` be `'text'` like `see_also`?"*), which
is why it has never been filed as a defect in its own right.

**The mechanism.** `engineering/tools/validate-crossref-keys.py` `CROSS_REF_FIELDS` types
`'see_also': 'text'`, `'references': 'text'` and `'related_concepts': 'text'` (*"informational
only"*), and the resolver then does `if ref_type == 'text': continue`. A value in one of those
fields is never looked up, whether it is prose or an unmistakable file path.

**Measured 2026-08-26 over all 1132 shipped files.** 760 top-level values sit in the three
text-typed fields. 160 of them are path-shaped. Resolving each against the KB root, the citing
file's own directory, and the repo root, and setting aside 3 intentional globs
(`architecture/smart-pins/*.yaml`):

> **14 shipped `see_also:` file paths resolve to nothing, with the gate green.**

| Citing file | Value | Why it fails |
|---|---|---|
| `hardware/addon-motor-driver.yaml`, `addon-microsd.yaml`, `addon-hd-audio.yaml`, `addon-rtc.yaml` | `language/spin2/methods/_index.yaml` | no such file (4 sites) |
| `language/pasm2/concepts/labels.yaml` | `jmp.yaml`, `call.yaml`, `djnz.yaml`, `rep.yaml` | **bare names**; the files are at `language/pasm2/` |
| `language/spin2/symbols/streamer-symbols.yaml` | `../../architecture/streamer/modes-reference.yaml`, `…/dac-routing.yaml` | relative depth off by one — both targets exist |
| `language/spin2/methods/cogspin.yaml` | `concepts/multi_cog_synchronization.yaml` | no such file |
| `language/spin2/methods/pinstart.yaml` | `concepts/inline_pasm2.yaml` | no such file; the concept is in `language/spin2/constructs/inline_pasm.yaml` |
| `guides/spin2-getting-started.yaml`, `pasm2-getting-started.yaml` | `manifests/P2/language/*-manifest.yaml` | outside `deliverables/ai/P2/` entirely |

**This is a live negative control, not a hypothetical.** The gate exits 0 and prints
`ALL TOP-LEVEL CROSS-REFERENCES RESOLVE` while fourteen top-level references do not. The banner
is therefore wrong in a second way that F-340's disclosure does not cover, and
`validate-dod-release.py` inherits it. *A gate must read the artifact* — here it reads the
artifact and then declines to check what it read.

**Fix (two parts, neither is "delete the reference" — Sacred Rule #7).**
1. **Instrument:** resolve any text-typed value that is unmistakably a path (ends `.yaml`, no
   glob), leaving genuine prose alone; and say so in the banner, the way F-340's scope line does.
   A negative control is owed with it.
2. **Content:** repoint all 14. Most targets exist and only need the right path — bare names to
   full paths (Sacred Rule #7's stated form), the streamer pair one level up,
   `inline_pasm2.yaml` to `language/spin2/constructs/inline_pasm.yaml`. The `_index.yaml` and
   `multi_cog_synchronization.yaml` targets do not exist, so those redirect to where the content
   **is** documented.

**How this surfaced.** Dispatched work on «#321» reported the `'text'` typing as an out-of-scope
observation, proven by injection into a scratch copy. Arbiter verification replaced the injection
with a measurement of the live tree, which is what turned a design question into fourteen shipped
defects.

## The sprint plan's "8 blocked sources" was wrong on five of them (2026-08-26, «#318») — F-371

### F-371 — a document-shaped-file test was applied to sources whose primary artifact is not a document — `RESOLVED`

**This is my own error, in the plan I wrote, and it materially misinformed the reader.** The
ingestion-backlog sprint plan told Stephen that **8 sources are blocked — "no primary document
staged"** and named them. The classification came from one test:

```
find <src> -maxdepth 1 \( -name '*.pdf' -o -name '*.docx' \)
```

That is a test for a **document-shaped file**. Five of the eight sources have a primary artifact
that is not a document, so the test returned nothing and the absence was read as *blocked*.

| Source | What it actually holds | Verdict |
|---|---|---|
| `rom-booter` | `ROM_Booter.lst` **411 KB** + `rom_booter_v33_01j.lst` **432 KB** | **not blocked** — needs audit + cross-source |
| `flash-loader` | `flash_loader.spin2` + a 38 KB Theory-of-Operations | **not blocked** — needs audit + cross-source |
| `pnut-ts-pasm-ref` | `PASM2-Instruction-Database.json` **322 KB** | **not blocked** — needs an audit rollup |
| `p2-qa-spreadsheet` | the `.xlsx` in `external-inputs/p2/`; **991 rows already extracted, audit present** | **not blocked** — needs cross-source |
| `quick-bytes-code` | 3 code archives + a `.spin2` | **not blocked, and mis-scoped** — a *community artifact* to catalogue, not a 7-pass ingestion |
| `p2docs-github-io` | narrative + validation report only | **blocked** — needs the site |
| `iron-sheep-compiler` | one condition-codes `.md` | **blocked** — needs compiler output |

**Two genuinely blocked, not eight.**

**The dashboard said so all along.** `rom-booter`'s note reads *".lst assembly; no audit /
cross-source"* and `p2-qa-spreadsheet`'s reads *"991 rows; audit present; no cross-source"*. **The
rows I was classifying already carried the answer**; the test I ran did not read them. A second
error compounded it — an inventory using `find ! -name '*.md'` hid `p2-qa-spreadsheet`'s extraction
and audit, because both are `.md`.

**Why this is filed rather than quietly corrected.** It is the same defect class this sprint kept
finding in the dashboard — **a number or a status produced by a check that was not measuring what
its label claimed**. F-250's `100% (stated)` over digit-free text, the PASM2 Manual's 64% measuring
the document rather than the capture, `quick-bytes-code`'s 15% grading a catalogue task on an
ingestion scale, and now a *blocked* label produced by a filename pattern. **Writing my own instance
of it into the same register is the only thing that makes the pattern visible as a pattern.**

**Fixed** in `engineering/ingestion/README.md` — a new *"What is actually outstanding, and what would
unblock it"* section gives each source its real primary artifact, what is genuinely missing, and
whether it needs anything from outside the repo. **Status `RESOLVED`:** the plan's claim is corrected
in the dashboard, which is what the next session reads.

## The TAQOZ author says ROM TAQOZ is an EARLY build, not just a cut-down one (2026-08-26, «#317») — F-370

### F-370 — `taqoz-forth.yaml` calls ROM TAQOZ "the finite, fixed version"; its author says it is also an **early** version — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`, and RE-SCOPED BY STEPHEN.** He ruled on this directly: *"do not put quality information like that in the [YAMLs]. All we want to know is that TAQOZ exists, how you get to it, and what it is useful for."* So the ROM-vs-RELOADED comparison this finding proposed — cut-down, early build, words may behave differently — **was NOT carried**, and the finding's original recommendation is superseded. What went in is the half that is utility: a `useful_for:` block giving the author's own guidance (use ROM TAQOZ for hardware debugging, especially when a larger environment will not load) plus what the resident interpreter is good for. The file already covered existence and access. Rule saved to auto-memory as `feedback_kb_entries_state_existence_access_utility`.

**How this surfaced.** The Bit Bashers Guide DOCX carries two reviewer comments, both anchored to
the same paragraph — the one marked *"(not in ROM)"*. A reader hit exactly that limit; **the author
of TAQOZ answered.**

| | |
|---|---|
| **[0]** Anonymous, 2023-03-30 | *"This did not work for me. I got `??? .D ???` instead of `--- 1234...`"* |
| **[1]** **Peter Jakacki**, 2023-04-06 | *"The ROM version is not only a cut-down version but also **an early version**. Use ROM version for debugging hardware etc especially when you can't seem to load the RELOADED version which can then be backed up to Flash or SD."* |

**Why the tier is high.** Peter Jakacki **is** the author of TAQOZ. For TAQOZ specifically he stands
where Chip Gracey stands for P2 silicon — this is designer testimony inside the document's own
review thread, not a forum lead.

**What our KB says** (`deliverables/ai/P2/architecture/boot-rom/taqoz-forth.yaml:47-50`):

> *"ROM TAQOZ is the finite, fixed version; TAQOZ Reloaded is the actively-developed environment.
> The two have different word sets."*

**Correct as far as it goes, and it misses the consequence.** "Finite and fixed" reads as *a subset,
frozen* — which invites the assumption that a word present in both behaves the same in both. The
author says ROM is also an **earlier build**. **A shared word may therefore differ in behaviour, not
just in presence**, and the KB's framing gives a reader no reason to suspect that.

**Fix (YAML head).** Carry the author's wording and its consequence into
`taqoz-forth.yaml`, cited to
`sources/TAQOZ-Forth-Bitbashers-Guide/reviewer-comments-harvest-2026-08-26.md`. Also worth carrying
his usage guidance, which is practical and nowhere in our tree: **use ROM TAQOZ for hardware
debugging, especially when RELOADED will not load.**

**The file's own chase plan is executable today, and nobody has run it.** Its
`knowledge_gaps.rom_vs_reloaded_word_diff` says *"Which specific words are in ROM TAQOZ vs. only in
TAQOZ Reloaded is not documented"*, with the chase *"Extract ROM dictionary from `ROM_Booter.lst`;
compare with TAQOZ Reloaded glossary"*. **We hold `ROM_Booter.lst`** —
`engineering/ingestion/sources/rom-booter/ROM_Booter.lst`, 411,535 bytes, **48 TAQOZ mentions**. The
first half of that chase needs no new source. Not run in this pass — this is an ingestion task and
the chase is YAML-head work — but recorded as **actionable now** rather than blocked.

### F-368 — `getbrk.yaml` drops the Z value for the pattern-queued case, and declares `Z: No effect` for an instruction that requires a flag effect — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`.** The dropped branch is restored: `or 0 if a pattern IS queued (D <> 0)`. `flags_affected` no longer says `Z: No effect` for an instruction that requires a flag effect — it now carries a `note:` that GETBRK has no no-effect form, a per-flag description of what WC and WZ each select, and a `source:` at `silicon-doc-text.txt:2591`.

**The source** (`sources/silicon-doc/silicon-doc-text.txt`, GETBRK D WZ):

> `Z = 1 if no SKIP/SKIPF/EXECF/XBYTE pattern queued (D = 0) or 0 if pattern queued (D <> 0)`

**The shipped YAML** (`deliverables/ai/P2/language/pasm2/getbrk.yaml:36-37`):

> `- WZ: Z = 1 if no SKIP/SKIPF/EXECF/XBYTE pattern is queued (D = 0), or pattern queued if D <> 0.`

**The `0` is gone.** *"or 0 if pattern queued"* became *"or pattern queued if"* — which is not a Z
assignment at all. A reader learns what Z is when no pattern is queued and **nothing** about the
other branch, in the one sentence that exists to tell them.

**Second defect, same file:** `flags_affected: Z: No effect` (`:45`), while `:13` of the same file
states *"GETBRK REQUIRES a flag effect (WC, WZ, or WCZ)"* and `:36` describes what WZ does to Z.
The file contradicts itself.

**Fix (YAML head).** Restore the branch — `or 0 if pattern queued (D <> 0)` — and reconcile
`flags_affected` with the instruction's own requirement.

### F-369 — the smart-pin DIR-reset behaviour is in the Silicon Doc and carried nowhere in the KB — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`, and it carried more than the finding recorded.** Added `critical_requirements.reset_without_reconfiguring` to `architecture/smart_pins.yaml`. Reading the source paragraph in full turned up the **mechanism** behind a rule the KB already asserted without explaining: each smart pin holds **126 bits of state data** separate from its WRPIN configuration, and WRPIN *multiplexes* those bits to the subcircuit chosen by `%SSSSS`. Issuing WRPIN while DIR is high remaps them underneath live state — *"unpredictable and quite certainly useless behavior"*. So the existing *"configure only while DIR is low"* rule is a consequence of the multiplexing, not a convention, and that is now recorded as `why_this_is_the_rule`.

**The source:** *"Once a smart pin is configured via WRPIN and then started by making its DIR bit
high, it can be reset at any time by making its DIR bit low. It does not lose its configuration set
by the last WRPIN…"* (`sources/silicon-doc/silicon-doc-text.txt:3856`; this entry originally recorded `:3360`, which today reads `(X,Y) ROTATION` — corrected 2026-08-27 during «#328» verification. The shipped YAML always cited `:3856`, so nothing downstream inherited it).

**Measured:** `grep -rl` across all of `deliverables/ai/P2/` for `DIR bit low`, `reset at any time`
and `does not lose its configuration` returns **zero files**.

This is an operational fact a driver author needs — that a smart pin can be reset mid-flight without
re-issuing WRPIN — and it is one of the paragraphs the `external-inputs/` copy is missing, which is
plausibly why it never reached the KB. **Fix (YAML head):** carry it into
`architecture/smart_pins.yaml` with this citation.

## The TQFP-100 package drawing was in the Silicon Doc all along — G-021 closes, and G-019 was overstated (2026-08-26, «#312») — F-366

### F-366 — the shipped KB has no package-dimension record, and the source to write one has been in the repo unextracted — `RESOLVED`

**APPLIED 2026-08-26 («#320») — `RESOLVED`.** `deliverables/ai/P2/hardware/p2-package-mechanical.yaml`
now exists (commit `491d033b`), carrying the millimetre dimension rows off the ON Semiconductor
sheet with its aliases, and stating what the drawing does **not** give — there is no thermal data
on it, so **G-020 stays open**. The status flip was missed at the time and is made here during
«#321» verification: the artifact and its commit were checked directly, not taken from a closing
report.

**How this surfaced.** «#312» re-tested every source-silent verdict against the completed
silicon-doc extraction, because all of them were reached while the Tier-1 authority was 75%
ingested and contributing **none** of its 48 tables.

**G-021 is OVERTURNED.** `assets/images-silicon-doc-2026-08-26/silicon-034.png` is the ON
Semiconductor **MECHANICAL CASE OUTLINE / PACKAGE DIMENSIONS** sheet — **TQFP100 14×14, 0.5P, CASE
932BR, ISSUE O**, 03 JUL 2018, document **98AON94348G** — carrying the complete millimetre table.
Read off the rendered drawing twice (whole page, then the table at 3.5× zoom), both reads agreeing,
and **not OCR'd**: tesseract misreads digits on these sheets and these are precision values.

Full transcription is in
`engineering/analysis/2026-08-26-silicon-doc-retest-of-source-silent-verdicts.md`. Headline values:
`D`/`E` 15.80/16.00/16.20 · `D1`/`E1` 13.80/14.00/14.20 · `e` 0.50 BSC · `b` 0.17/0.22/0.27 ·
`L` 0.45/0.60/0.75 · `A` max 1.20 · `M` 0°–7°.

**What is owed (YAML head).** `deliverables/ai/P2/` has **no package/mechanical record at all**.
The dimensions are now sourced and citable; a record should be written and cited to this drawing.
This task does not edit shipped YAML, so it is handed over rather than applied.

**Also corrected, and this half matters as much.** **G-019 was overstated.** Its clause *"no
per-drive-mode current in mA anywhere in the corpus"* is false against the completed extract: the
drive ladder is stated outright at `silicon-doc-text.txt:206`, and **Table 30** gives digital
input-filter low-pass times computed in the document (`6.25ns × 32 × 3 = 600ns`). The *core* of
G-019 survives — `propagation delay`, `rise time`, `fall time`, `slew rate` all return zero hits,
and all 9 `ns` quantities were read individually and none is a pin-driver AC spec. But a register
row carrying a claim broader than its evidence is a false negative someone will later rely on, so
the row was corrected rather than left.

**Why this is filed as a finding and not just a gap update.** Two of the three re-tested gaps moved
because **the corpus was incomplete, not because the analysis was poor** — and Table 30, the thing
that corrected G-019, lives *inside a table cell*, which is exactly the content class that no
PDF-era capture could carry and that our own first DOCX pass flattened until «#310» fixed the
walker. **The lesson is about sequencing, not diligence: a "source is silent" verdict is only as
good as the extraction it was drawn against**, and this project now has a worked example of that in
both directions.

## 23 shipped-KB citations point into the superseded lossy silicon-doc capture (2026-08-26, «#310») — F-365

### F-365 — the shipped KB cites `p2-documentation.txt`, the PDF-era extraction now known to be lossy — `RESOLVED`

**APPLIED 2026-08-26 («#320») — `RESOLVED`.** All 23 citations re-anchored to
`silicon-doc-text.txt`, each verified by reading the old target and finding the same content in
the new artifact — line numbers were never translated. **Measured during «#321» verification:**
`grep -rn p2-documentation.txt deliverables/ai/P2/` returns **1**, down from **24 across 10 files**
at `36196329`. The one that remains is deliberate —
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml:19` names the superseded capture on
purpose, because F-372 / G-027 is precisely a conflict *between* the two captures of the same v35
document. The status flip was missed at the time and is made here.

**What was measured.** References to the superseded artifact, outside its own folder:

| Referencing | Count |
|---|---|
| shipped KB `deliverables/ai/P2/` | **24** — of which **23 carry `:line` locators** |
| other `deliverables/` | 3 |
| `engineering/` working docs | 266 |
| **total** | **293** |

**Severity, stated honestly rather than inflated.** The sampled shipped locators (`:188`,
`:3602`, `:3606`, `:3961`, `:3997`, `:3999`) were each read back 2026-08-26 and **all resolve to
content that matches what cites them.** These citations are **not broken**. This is lineage
hygiene, not a correctness emergency, and it should not be reported as though 23 facts were
wrong.

**Why it still matters.** The cited capture is PDF-derived, carries **zero of the document's 48
tables**, and splits code lines. It has already produced one wrong fact that reached the shipped
KB — **F-363**, the `$1F6`/`$1F7` PA/PB row — and the mechanism is visible in the artifact:
`p2-documentation.txt:907-908` are the bare token `CALLD-imm` alone, its table row shredded. A
citation into that capture is a citation into a source we now know drops structure silently.

**Fix (YAML head).** Re-anchor the 23 locators to `silicon-doc-text.txt`, verifying each against
the new artifact rather than translating line numbers — the two files do not share numbering, and
"verify citations live, not from a ledger" applies exactly here.

**The old artifact is deliberately NOT archived.** `ingest-source` §0.6 gates the archive-move on
first re-pointing downstream references; with 293 of them a move would strand every one, which is
a Sacred Rule #7 violation. Marked in place instead —
`engineering/ingestion/sources/silicon-doc/SUPERSEDED-BY-2026-08-26-DOCX.md`. The move happens
after this finding is worked, not before.

### F-363 — `complete-system-registers-index.yaml` says PA/PB hold the "CALLD-imm parameter"; all three authorities say **return** — `RESOLVED`

**APPLIED 2026-08-26 («#319») — `RESOLVED`.** `$1F6` → `CALLD-imm return, CALLPA parameter, or LOC address`; `$1F7` → `...CALLPB...`. Both rows now carry a `source:` naming all three authorities and a `note:` stating why the rows are deliberately not identical. **Citation drift caught while applying:** this finding cited `silicon-doc-text.txt:313-314`, which was the numbering BEFORE «#310» re-emitted that artifact; the live locations are `:452-453`, verified by reading them. The Hardware Manual (`:357`) and Datasheet (`:564-565`) locators were unaffected and re-verified.

**How this surfaced.** «#310» reconciled the prior PDF-era artifact `COG-RAM-REGISTER-MAP.md`
against the new DOCX extraction of the Silicon Doc. The `$1F6`/`$1F7` rows disagreed.

**What each source says.**

| Source | `$1F6` (PA) |
|---|---|
| **silicon-doc** (DOCX, 2026-08-26) `silicon-doc-text.txt:313` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **p2-hardware-manual** `p2-hardware-manual-text.txt:357` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **p2-datasheet** `p2-datasheet-text.txt:564` | `CALLD-imm return, CALLPA parameter, or LOC address` |
| **our shipped YAML** `complete-system-registers-index.yaml:73` | `CALLD-imm parameter, or LOC address` |

`$1F7` (PB) is the same, with `CALLPB`. **Three independent ingested authorities agree
verbatim, cell-identical, and the shipped KB disagrees with all three.**

**Two distinct defects in one line.**
1. **`return` became `parameter`.** PA holds the **return address** written by a `CALLD`
   with an immediate operand. Calling it the parameter inverts what the register receives.
2. **The `CALLPA`/`CALLPB` role was dropped entirely** — and with it the PA/PB distinction.
   Our two rows are byte-identical to each other; the sources' are not.

**Where it came from — the mechanism, not just the fact.** The prior PDF-era capture shredded
that table: `p2-documentation.txt:907-908` contain the bare token `CALLD-imm` alone on a line,
its row torn away. The prior artifact then reconstructed a plausible sentence from the fragment,
and the reconstruction is what shipped. **This is the F-250 class in a new place** — a lossy
extraction that reads as fluent, correct-looking prose. The DOCX capture keeps the row intact
because it carries real table structure.

**Reached our KB?** Yes — 2 sites, both in
`deliverables/ai/P2/architecture/system-registers/complete-system-registers-index.yaml`
(`:73`, `:79`). Class sweep for `CALLD-imm` across `deliverables/ai/P2/` returns exactly those
two. No other file carries the wording.

**Fix (YAML head, not this task).** `$1F6` → `CALLD-imm return, CALLPA parameter, or LOC
address`; `$1F7` → `CALLD-imm return, CALLPB parameter, or LOC address`. Triple-sourced, so no
further research is owed.

## The hygiene gate reports CLEAN on the register that owns the `G-`/`Q-` allocators while reading none of its entries (2026-08-26, p2-click-adapter ingestion) — F-362

### F-362 — `audit-register-hygiene.py` reports CLEAN on the register that owns the `G-` and `Q-` allocators while reading zero of its entries — `RESOLVED`

**How this surfaced.** The p2-click-adapter ingestion (2026-08-26) needed a new gap ID. Allocating
it by hand-reading the maximum `G-` in the table is exactly the two-writer collision the register
discipline exists to prevent, so the gate was run on `KNOWLEDGE-GAPS.md` to confirm the allocation.
It reported one violation (`no-counter`) and, once that was fixed, **CLEAN** — while its own summary
line read `findings : 0 entries, 0 distinct IDs` against a register holding **22 `G-` rows and 8
`Q-` rows**.

**What was measured.** `_ENTRY_HEAD` models exactly two entry dialects:

```
_ENTRY_HEAD = (r"^(?:#{2,4}\s+(<P>-\d+[a-z]?)\s*[—-]"      # heading form  (## F-001 — …)
               r"|-\s+\*\*(<P>-\d+[a-z]?)\s+[—-])")        # bullet form   (- **F-357 — …)
```

`KNOWLEDGE-GAPS.md` uses a **third** dialect exclusively — the markdown table row
(`| G-019 | Domain | … |`) — for both Part A gaps and Part B expert questions. Neither pattern
matches it, so `parse()` returns zero blocks and every per-entry check (duplicate IDs, status
presence, headline-vs-body agreement, ID coverage, orphaned sections) is skipped. Only the counter
check runs.

**Negative control — the proof, not the inference.** A duplicate `G-019` row was planted directly
beneath the real one in a copy of the register and the gate re-run:

```
$ python3 engineering/tools/validation/audit-register-hygiene.py <copy-with-planted-duplicate-G-019>
  next-ID counter   : G-23 (`Next gap ID`; no live G- entries)
  findings          : 0 entries, 0 distinct IDs
  CLEAN  …: no register-hygiene violations
  exit=0
```

**A duplicate ID in a register passes CLEAN with exit 0.** This is the same class as F-359 and the
`logic analyzer` misroute: the instrument answers with the wrong thing rather than nothing, and
"CLEAN" on an unread file is more dangerous than an error, because it is indistinguishable from a
verified pass. A prototype that adds the table-row alternative to `_ENTRY_HEAD` (plus
`m.group(3)` in `parse()`) makes the planted duplicate fire at **exit 1**, confirming the dialect
gap is the whole cause.

**Why the fix is not the one-line dialect add.** With entries visible, the status checks fire on
every row, because `STATUS_WORDS` is a single module-global tuple carrying the *corrections*
register's vocabulary. `KNOWLEDGE-GAPS.md` uses its own lifecycle — `OPEN` / `ANSWERED` /
`STILL-UNKNOWN` / `RELOCATED` / `PARTIAL` — and `OPEN` is **deliberately excluded** from
`STATUS_WORDS`, for a documented reason that is still correct: in the corrections register `OPEN`
is ordinary English prose (8 whole-word uppercase occurrences), and admitting it globally would let
a finding carrying **no** status pass check 4 on a stray word. So the real fix is a **per-register
status vocabulary**, selected the way the ID families already are — read off the counter label the
file declares (`Next gap ID` vs `Next finding ID` vs `Next erratum ID`) rather than hard-coded.
The hook exists: `main()` already rebuilds `FINDING_START` / `ID_RANGE` / `ID_ONE` / `GUARD_RE`
per register from `COUNTER_RE`; `STATUS_RE` needs to join them.

**Scope note.** Deliberately **not** applied in the p2-click-adapter commit. Widening a
module-global status vocabulary that 85 live findings are graded against is a regression surface
that wants its own verification pass (baseline captured: all three registers exit 0, the tool's
`--negative-control` suite passes 13 checks), not a bolt-on at a release boundary. What WAS fixed
in that commit is the allocator defect this finding surfaced — see below.

**Fixed alongside (allocator ownership).** `KNOWLEDGE-GAPS.md` declared **no** counter at all, and
`P2KB-CORRECTION-FINDINGS.md` declared `Next gap ID: G-008` — **stale by fourteen** against the
gaps register's actual `G-022`, and a second register claiming an allocator it does not own. F-352
caught the smaller instance of this same drift (`G-007`) and corrected the number rather than the
ownership, so it recurred. Now: `KNOWLEDGE-GAPS.md` declares `Next gap ID: G-023` ·
`Next expert-question ID: Q-009` and states outright that it owns the `G-` and `Q-` allocators;
the corrections register's duplicate `Next gap ID` clause is retired with a pointer to it. All
three registers exit 0 under the gate afterwards.

**Status:** `RESOLVED` — fixed and verified 2026-08-27 («#327»). Three shapes the tool did not
model, all repaired in `engineering/tools/validation/audit-register-hygiene.py`:

1. **The table-row entry dialect.** `_ENTRY_HEAD` gained `| G-019 | … |`, and `parse()` now also
   returns each row's **status CELL**, located from the table's own `Status` / `State` column
   heading. The cell, not the row, is what the status checks read — because the ledger's own
   lifecycle word `open` is *also* ordinary English in its prose ("_Still open:_ …"), so a
   vocabulary carrying it, searched over a whole row, would have made check 4 unfailable and
   re-created this very finding in a new costume.
2. **Per-register status vocabulary**, selected off the counter label exactly as the ID families
   already were. `OPEN` **stays excluded** from the corrections vocabulary; the ledgers get their
   own (`OPEN` · `ANSWERED` · `STILL-UNKNOWN` · `RELOCATED` · `NARROWED` · `PARTIAL` · `RESOLVED` ·
   `ASKED`, case-folded, with `sweep=False` because a moving ledger keeps an answered row on
   purpose). An unknown label falls back to the corrections vocabulary, which fails loudly on a
   foreign lifecycle rather than passing it.
3. **An ID family is a prefix string, not a letter** — so the P1 quad's namespaced `F-P1-` /
   `G-P1-` / `Q-P1-` allocators parse. Those two registers also declared `**Next ID:`** with no
   `<thing>` word; they were corrected to the convention rather than the pattern loosened, because
   the label now *selects the vocabulary*, and `P1-KNOWLEDGE-GAPS.md` had written that same
   nameless counter twice in one file for two different families. The gate still refuses the
   labelless form — proven by a control case.

**Proof, both directions.** The planted-duplicate `G-019` fixture passes **CLEAN at exit 0**
through the pre-fix tool (read out of `.backups/`, which reports `0 entries, 0 distinct IDs`) and
**fails at exit 1 with `duplicate-id`** through the fixed one. Five registers now exit 0 with the
gate actually reading them: corrections **102 live / 294 archived / 0 unaccounted** (unchanged),
`SOURCE-ERRATA` **17 live** (unchanged), `KNOWLEDGE-GAPS` **36 live** (was `0 entries`),
`P1-CORRECTION-FINDINGS` **0 entries, counter governed** (was exit 1), `P1-KNOWLEDGE-GAPS`
**14 live** (was exit 1 and `0 entries`). `--negative-control` carries **11 new permanent cases**
(24 total), including the planted-duplicate shape itself, a blank status cell, a status word in a
row's prose with the cell blank, two families on one counter line, and both sides of the `OPEN`
exclusion.

**Surfaced but NOT filed** (allocator belongs to the sprint arbiter): the corrections register
carries a third ID series, `ENH-NN`, with **no declared counter** — and live `ENH-02` / `ENH-03`
name different proposals than the archived `ENH-02` / `ENH-03` in
`correction-sweeps/2026-08-15-…-archive.md`, i.e. the allocator has already collided across the
archive boundary. The gate deliberately does not model that family (doing so turns it red over a
defect whose remedy is renumbering live entries), but it now prints an `unmodelled series :
ENH-NNN` report line on every run so the question surfaces instead of staying silent.

## Duplicate YAML keys silently destroy content, and no gate can see them (2026-08-25, found by the release-review change ledger) — F-360

- **F-360 — Five duplicate-key sites in the shipped set discard a block's content at parse time,
  and `verify-yaml-format.py` passes every one of them because duplicate keys are legal YAML.** —
  `RESOLVED`

  **The mechanism.** YAML resolves a repeated key by **last-one-wins**, silently. The earlier
  block is not merged and not flagged — it simply does not exist for any consumer. `yaml.safe_load`
  succeeds, so a format gate that asks *"does this parse?"* answers yes. **This is a check that
  cannot fail**, and it was proven so rather than assumed: planting `test_dup: 1` / `test_dup: 2`
  into `architecture/locks.yaml` left `verify-yaml-format.py` at **exit 0**.

  **Found on the arbiter's own work first.** `architecture/pin-drive-configuration.yaml` — the file
  «#295» created as the single definition home for the fact this whole sprint turns on — carried a
  duplicate `note:` under `idioms:`. It was introduced **by the arbiter** hours earlier, while
  correcting the EF-063/EF-064 attribution: `gap_no_dedicated_bench_test:` was written with no
  indented body, so its intended children became siblings, and the new `note:` collided with
  `idioms.note`. **What was destroyed was the corrective sentence itself** — that `%M..M` selects
  drive strength, that the Pin Mode Legend contains no bias-resistor selector, and that the two
  idioms below are hardware-verified rather than documentary. A consumer parsing the file got the
  gap note in its place. **Fixed** (restructured as a proper nested mapping; `idioms.note` restored,
  0 duplicates in that file).

  **Four more are pre-existing and still stand.** Swept all **1130** shipped YAMLs:

  | File | Duplicate key | What is discarded |
  |---|---|---|
  | `architecture/lookup_ram.yaml:90` | `operation` | an entire block-scalar description |
  | `architecture/lookup_ram.yaml:93` | `usage_example` | an entire worked example |
  | `hardware/edge-breadboard-carrier.yaml:174` | `educational_value` | a **structured block**, replaced by the scalar `"excellent"` |
  | `language/pasm2/drvl.yaml:4` | `timing` | a `timing:` block on a PASM2 instruction, where timing is load-bearing |

  **NOT FIXED — deliberately, and this is a decision for Stephen at the release review.** Resolving
  each is a content judgement (which of the two blocks is the intended one), and **arming a
  duplicate-key check would turn the release red on four pre-existing files.** Doing that silently
  at the gate is the same move this sprint spent itself repairing. His options: fix the four and
  arm, arm and accept the red until they are fixed, or ship and schedule both.

  **The "lack".** The format gate asks whether a document *parses*, which duplicate keys do. Nobody
  asked whether it *says what it appears to say*. Sibling to F-335's family — an instrument
  answering a narrower question than its name implies — and to the standing lesson that a gate must
  read the artifact rather than a property of it.

  **Recommended repair when it is armed:** duplicate-key detection belongs in
  `verify-yaml-format.py` (it already loads every file), as a distinct violation class, with a
  negative control that plants a duplicate and requires a non-zero exit.

  **RESOLVED 2026-08-26 — gate armed, all sites fixed, and the count was wrong.** The gate shipped
  as its own instrument, `engineering/tools/validation/audit-yaml-duplicate-keys.py` (armed in
  `02ff61b7`), not folded into `verify-yaml-format.py`. Armed, it found **3 files / 4 sites**, not
  the five this finding recorded: the `pin-drive-configuration.yaml` site was already fixed, and
  the node-tree walk found nothing the manual sweep had missed. `deliverables/ai/P2` now returns
  **0 duplicate keys across 1132 files**.

  **In every one of the four, the surviving value had to be adjudicated — and in two of them the
  value consumers see today was the wrong one:**

  | Site | Kept | Why |
  |---|---|---|
  | `architecture/lookup_ram.yaml` `operation` (90 vs 98) | the **earlier**, discarded block | Lines 98-114 were the orphaned body of a **removed** pseudo-instruction for LUT-to-DAC streaming: its `- instruction:`/`encoding:`/`description:` header had been replaced by a comment, leaving `operation:`/`usage_example:` to be absorbed into the **SETLUTS** entry above and overwrite it. Consumers were reading streamer setup as SETLUTS's operation. SETLUTS's own content restored; the orphan deleted (its substance is already carried, with correct constant names, by `programming_patterns.waveform_generation` and `architecture.special_features` (feature: `LUT_to_DAC_streaming`) in the same file). |
  | `architecture/lookup_ram.yaml` `usage_example` (93 vs 102) | the **earlier**, discarded block | Same orphan, same repair. |
  | `hardware/edge-breadboard-carrier.yaml` `educational_value` (174 vs 205) | the **earlier**, structured block | The scalar `"excellent"` that was winning is also bare quality commentary, which the KB entry rule (existence / access / utility) excludes. Dropped. |
  | `language/pasm2/drvl.yaml` `timing` (4 vs 35) | the **earlier**, richer block | The later block was a strict subset (`cycles`/`type`); the earlier one additionally carried `pin_output_latency`. The discarded block is byte-identical to the one that is **live** in its twin `drvh.yaml`, so DRVL and DRVH were silently disagreeing about pin timing. The claim is sourced — P2 Documentation v35 Rev B/C (`silicon-doc-text.txt:1987`) and the P2 Hardware Manual (`p2-hardware-manual-text.txt:967`) both state the three-clock DIRx/OUTx transition delay — and that citation was added to **both** twins, which carried the claim uncited. |

  **Still open, and it is the same class of lack this finding is about:** the armed gate is **not**
  wired into `validate-dod-release.py`. That validator runs 11 checks and calls two sibling audits
  (`audit-constant-fidelity.py`, `audit-claim-sourcing.py`) as blocking gates; the duplicate-key
  audit is not among them, so a duplicate reintroduced tomorrow turns nothing red at release. The
  gate exists and passes — but nothing makes it run.

  Status: `RESOLVED` — 4/4 sites fixed, gate armed and returning 0; wiring it into
  `validate-dod-release.py` remains open.

---
## The published index and its gzip drifted apart in committed history, and the release validator has been red on it (2026-08-25, «#305», arming the content gates) — F-357

- **F-357 — `deliverables/ai/p2kb-index.json.gz` is four days behind `deliverables/ai/p2kb-index.json`
  in committed history, so `validate-dod-release.py` fails its Gzip Compression check on a clean
  tree.** — `RESOLVED`

  **How it surfaced.** «#305» armed two content gates inside `validate-dod-release.py` and ran the
  suite to prove the release path green. Every content check passed and the suite still reported
  **❌ VALIDATION FAILURES - DO NOT RELEASE**. The failure was not the new gates.

  **Measured at `HEAD`, before any edit this session:** the `.json` declares
  `generated: 2026-08-25T05:35:28`, 1130 entries; the `.gz` decompresses to
  `generated: 2026-08-21T23:15:55`, **1129** entries. One key present only in the `.json`
  (`p2kbArchPinDriveConfiguration`) and **181** entries differing between the two. Both files are
  unmodified in the working tree — the drift is committed.

  **Cause.** A task regenerated the index and committed the `.json` without regenerating the `.gz`.
  `release-yamls` Step 5.5 already warns that "both the index AND its `.gz` must be regenerated
  together — that failure is easy to miss if you only regen the `.json`". It was missed anyway,
  and nothing caught it because the DoD suite is not run outside a release.

  **Fixed** by regenerating the `.gz` from the committed `.json`
  (`gzip -c deliverables/ai/p2kb-index.json > deliverables/ai/p2kb-index.json.gz`); the pair is now
  byte-identical on decompression and the suite exits 0. Derived artifact, no content implication.

  **Why it is filed rather than just fixed.** A *published* index and its *published* gzip
  disagreed for four days, and `p2kb-mcp` serves the published state. Any consumer taking the `.gz`
  path saw a 1129-entry index missing a file this sprint added. The `release-yamls` warning
  (2026-08-25 revision) now names this incident so the next reader knows it is not hypothetical.

  **What is NOT closed by this entry:** nothing forces the two into lock-step outside a release
  run. The DoD suite catches it, but only when someone runs it.

  Status: `RESOLVED`

---

## The hygiene gate cannot see the new errata register, so its monotonic allocator is ungoverned (2026-08-25, arbiter, during «#307») — F-355

- **F-355 — `audit-register-hygiene.py` is hard-coded to one register's vocabulary, so
  `engineering/ingestion/SOURCE-ERRATA.md` has an unchecked monotonic allocator.** — `RESOLVED`

  > **Headline corrected 2026-08-25 («#302»).** It read `CONFIRMED` while this entry's own closing
  > line read `Status: RESOLVED` — the scannable layer and the authoritative layer disagreeing, in
  > the *understating* direction that check 10 exists to catch. **Check 10 could not see it:**
  > `BODY_STATUS` matches `^**Status:**` at column 0, and every bullet-form entry in this register
  > (this one included) writes an indented, unbolded `Status:` instead. Verified against the
  > shipped tool source, not inferred. The blind spot is closed in the same pass — see the
  > negative-control note added to the tool.

  **The defect.** The tool's counter check is `re.search(r"\*\*Next finding ID:\s*`?F-(\d+)`?\*\*", text)`
  (`audit-register-hygiene.py:271`) and it emits `no-counter` when absent. The errata register
  declares **`Next erratum ID: \`E-NNN\``** — different label, different prefix — so the gate
  reports nothing about it at all. Every protection it provides for `F-NNN` (counter ahead of every
  allocation, orphaned sections, duplicate IDs, unaccounted coverage) is simply absent for `E-NNN`.

  **Why it matters more than it looks.** The whole reason this project re-checks the next-ID before
  every dispatch is that two agents allocating from a stale number collide silently. The errata
  register is now a live input to «#307» and to every future ingestion, and it allocates two ID
  families (`E-NNN` and `D-NNN`). It is exactly the artifact that needs the gate.

  **This is the arbiter's gap, created the same day.** I stood the register up and gave it a
  counter in a vocabulary no instrument reads — the same class as declaring a section header for an
  ID with no live entry, which this very tool caught me doing hours earlier.

  **Interim, done rather than assumed:** the errata register's IDs were verified by hand at filing
  time — `E-001`…`E-009` present and contiguous, no duplicates, header counter at `E-010` = max+1.
  Command: a parse of `^## (E-\d{3})` against the `Next erratum ID:` header. That is a one-off
  check, not a gate, and it does not survive the next person who forgets.

  **The fix for «#305», specified so it needs no rediscovery:** parameterise the prefix and label —
  take `(label, prefix)` pairs per register file rather than hard-coding `Next finding ID` / `F-`,
  and run the same four checks over each. `SOURCE-ERRATA.md` needs **two** families registered
  (`E-` for errata, `D-` for the open questions in Part B). **Do not "fix" this by renaming the
  errata register's counter to `Next finding ID:`** — that would make two different registers claim
  the same allocator name and is a worse defect than the one it closes.

  ⚠️ Add a **negative control** with the fix: a register with a deliberately stale counter must
  FAIL, and *"the file was not examined at all"* must be a distinct non-zero exit rather than a
  pass. That is the standing lesson from the digit-density gate — a gate that measures nothing and
  exits 0 manufactures confidence.

  **RESOLVED 2026-08-25 by «#305»**, parameterised exactly as specified and NOT by renaming the
  errata counter. `(label, prefix)` are read off the register itself — `COUNTER_RE` matches
  `**Next <word> ID: X-NNN**` in any spelling — and the ID shapes are built from the series the
  file actually uses (`series_in` / `build_id_res`). **Every** declared counter is now checked,
  and a series that is allocated with **no** counter declared is itself a violation, which is
  the general form of this defect.

  **Two further hard-codings surfaced while doing it, both of which would have made the new
  coverage lie:**
  - `canon()` matched `([FG])-0*(\d+)` and returned the ID **unchanged** for anything else. So
    the errata register's canonical live set held `E-001` while the gap scan looked for `E-1`,
    and all ten entries were reported as "went silent" while sitting in plain view. A
    canonicaliser that silently declines to canonicalise is worse than one that raises.
  - The finding heading pattern required `###`. The errata register heads an entry with `##`,
    which the section-structure checks would then have read as a section header. Entry headings
    are now tested first, and `#{2,4}` is accepted.

  **`RESEARCHING` added to `STATUS_WORDS`** (the errata lifecycle's middle state). `OPEN` and
  `GAP` were deliberately **not** added: both occur as ordinary uppercase English in the
  corrections register's prose (8 whole-word occurrences today), and admitting them would let a
  finding carrying no status pass check 4 on a stray word. A vocabulary that silences a check is
  worse than one that is short.

  **`D-` was not registered, because it does not exist.** This finding says the errata register
  "allocates two ID families (`E-NNN` and `D-NNN`)". Measured on disk: `D-` appears **zero**
  times, and Part B's open-question table keys off `E-006`. A `--series` flag exists for a family
  declared before its first filing; nothing needed it.

  **Negative control added, as this finding required:** nine cases through the shipped entry
  point — a stale counter and a clean one in **both** dialects, a register with no counter, a
  series with no counter declared, a missing status, a duplicate ID, and an unreadable register,
  which exits **2** distinctly from a violation's 1. Both live registers verified CLEAN
  afterwards, with the corrections register's numbers unchanged from entry (80 live, 300
  archived, 0 unaccounted, 5 guardrails exempt).

  Status: `RESOLVED`

---
## Check 10 had never once been able to fire, on either side of the comparison it makes (2026-08-25, «#302», the whole-register reconciliation) — F-358

- **F-358 — `audit-register-hygiene.py`'s headline-vs-body check reads `**Status:**` at column 0
  only and the *first physical line* of a headline only, so in this register it could see 5 of 20
  status declarations and missed every wrapped headline — including both live disagreements it
  exists to catch.** — `RESOLVED`

  **How it surfaced.** «#302»'s job was to leave all 81 status tokens accurate. Deriving the state
  per entry by hand — rather than trusting the gate that reports the file CLEAN — turned up two
  entries whose headline and body contradicted each other:

  | Finding | Headline said | Its own body said |
  |---|---|---|
  | **F-355** | `CONFIRMED` (on line **2** of a wrapped headline) | `Status: RESOLVED` (indented) |
  | **F-347** | `PENDING-VALIDATION` (line 2) | `**Disposition.** PARTIAL` (blockquoted) |

  Check 10 exists for exactly this and reported CLEAN on both, every run, since it was written.

  **Two independent blind spots, and each alone was sufficient to hide F-355.**

  1. **Body side — `BODY_STATUS = ^\*\*Status:\*\*` matched column 0 only.** This register declares
     a verdict four other ways: indented under a bullet entry (`  Status: …`), inside a blockquote
     (`> Status: …`), and as `**Disposition.**`. **Measured on the file: 20 status-declaration
     lines, 5 visible, 15 invisible** — three quarters of the bodies.
  2. **Headline side — the checks read `block["headline"]`, which `parse()` sets to the FIRST LINE.**
     Bullet entries routinely wrap and the register puts the status at the end of the bold lead-in,
     i.e. on line 2, 3 or 4. For every wrapped entry `lead_status()` returned `None`, so check 10
     skipped it outright and 4b had nothing to test.

  **F-355 was invisible on BOTH sides simultaneously**, which is why fixing either one alone would
  have left the disagreement standing while reporting the repair complete — the failure mode this
  project already names as *a check derived from the thing it is checking*.

  **The root cause is not either regex. It is that check 10 shipped with no negative control.**
  Every other check here has one; this one was reasoned about and never asked to fail. **A check
  that cannot fail has not been verified, it has been RUN** — the standing lesson from the
  digit-density gate, arriving again in the tool that was built to stop this class.

  **Fixed** by widening `BODY_STATUS` to every spelling the register actually uses, and by adding
  `scannable_head()`, which accumulates the headline until its `**` markers balance so the whole
  bold lead-in is read. **Both proven before/after:** a fixture carrying an indented-`Status:`
  disagreement passed **CLEAN** through the pre-widening tool (read out of `.backups/`) and **FAILS**
  through the fixed one; a second fixture with the status on line 2 of a wrapped headline did the
  same. Four permanent cases were added to `--negative-control` — the two failing spellings, the
  wrapped-headline case, and an **agreeing** case so an over-eager matcher is caught on the other
  side. The control now runs **13** cases and all pass.

  **Both live registers verified CLEAN afterwards** with the widened checks — corrections (81 live,
  300 archived, 0 unaccounted) and `SOURCE-ERRATA.md` (10 live, next `E-011`) — and the errata
  register is unaffected, since it carries its status in the `##` entry heading and declares no
  `Status:` lines at all.

  **Consequence for the register itself, applied in the same pass:** with the checks able to see
  every headline, **6 entries were found carrying no status token in their scannable headline at
  all** (F-250, F-251, F-252, F-328, F-334, F-335) — a reader scanning headlines got nothing, which
  is worse than a disagreement because there is no signal to notice. All six now carry their body's
  token in the lead-in. **All 81 entries now carry a scannable status that agrees with their body.**

  Status: `RESOLVED`

---
### F-342 — a Parallax board guide states the pull-up mislabel itself, and prescribes it in the one configuration where it cannot work — `RESOLVED — the adjudication this entry owed was made and executed BOTH ways; the source-defect half now lives in the errata register`

> **RELOCATED + CLOSED 2026-08-25 («#302»). Pointer left behind rather than a move, because the
> reasoning above is the origin of the erratum and is worth reading in place.**
>
> This entry is a **source-document defect** by the three-register test — *if Parallax fixed the
> #64013 guide tomorrow, would it disappear?* **Yes.** Its home is
> **`engineering/ingestion/SOURCE-ERRATA.md` → `E-004` (`RESOLVED`)**, *"the pull-up mislabel, in a
> Parallax guide, prescribed where it cannot work"*, which carries the same two locators
> (`P2-RTC-Add-on-text.txt:74-77`, `spin2-v55-text.txt:1505`), the same Pin-Mode-Legend counter-cite,
> and the empirical corroboration with its ⚠️ scoping (EF-063/EF-064 are rig apparatus, never the
> authority). That register did not exist when this was filed — it was created 2026-08-25.
>
> **The adjudication this entry left open is settled, and NOT by picking one branch.** It asked for
> (a) keep the quote and add a DIR-high note, or (b) route it upstream as a board-guide erratum.
> **Both were done.** (b) is `E-004`. (a) is applied and **verified on the artifact, not on a status
> line**: `deliverables/ai/P2/hardware/addon-rtc.yaml` `pin_mode_tip` is no longer the guide's
> sentence — it is a map carrying `source:` (all four citations), `board_fact:` (SCL/INT/CLKOUT
> share the single +0 pin, so only one is usable at a time), `p2_side_mechanism:` (*"Hold the pin
> weakly high with P_HIGH_150K and DIR HIGH"*), and an explicit
> `do_not_copy_the_guides_wording` key quoting the wrong text so it cannot be re-adopted. The KB
> half is tracked under **F-353**.
>
> **The D3/R9 restraint held:** the source's wording was never silently improved — it is quoted,
> labelled wrong, and answered.

> **Where the KB carries it:** `deliverables/ai/P2/hardware/addon-rtc.yaml:49-51` (`pin_mode_tip`).
>
> **Where it comes from:** `engineering/ingestion/sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:74-77`
> — *"To use the I2C SCL function, set the I2C output mode to use 3.3 k-ohm pull-up. … then disable
> I2C and set the P2 Smartpin (or equivalent) **input mode** to 150 k-ohm pull-up."*
> (P2 RTC Add-on Board #64013, v1.0 11/29/2022, page 2.) The KB is quoting its source faithfully.
>
> **Why it is a finding and not a KB defect.** Two things are wrong in the source itself:
>
> 1. **The mislabel, from Parallax.** There is no 150 kΩ pull-up on the P2. `P_HIGH_150K` is
>    *"Drive high 150kΩ"* (`sources/spin2-v55/spin2-v55-text.txt:1505`) — a drive-strength
>    selector. This is F-321's exact rename, in a Parallax document.
> 2. **It is F-322-shaped.** "input mode … 150 k-ohm pull-up" is a contradiction on this silicon:
>    input mode is DIR = 0, and the Pin Mode Legend states *"DIR = direction bit; 0: input (float),
>    1: output (drive)"* (`sources/p2-datasheet/p2-datasheet-text.txt:1144`; identical at
>    `sources/p2-hardware-manual/p2-hardware-manual-text.txt:871`). With DIR = 0 the drive-high
>    selection is inactive and the pin is plain high-impedance — the INT/CLKOUT line would float.
>
> **Deliberately NOT rewritten** (D3/R9): a source's wording is not ours to silently improve, and
> the correct replacement is a behaviour claim about the #64013 board that no source states.
>
> **What is owed.** Adjudicate whether the KB should (a) keep the quote and add a note that the
> weak high drive requires DIR high, citing the legend line above, or (b) route the discrepancy
> upstream as a board-guide erratum. This is the second Parallax-source-level instance of the
> F-321 class after F-341's derived-analysis documents, and the first in a *published Parallax
> document* rather than one of ours.

### F-343 — the KB credited the 64006A Control Board with pull-up resistors its own board guide does not give it — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml:141` —
> `special_features: "Current limiting resistors, pull-up resistors"`.
>
> **What the source says.** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:16-23`
> (Product Guide v2.0, 1/12/2021) gives every one of the eight I/O pins **one** component: a
> *470 Ω series resistor*. Pull-up and pull-down appear **nowhere** in that board's source. The
> KB's own `hardware/addon-control-board.yaml` agrees — 470 Ω series resistors on all eight pins,
> no bias network.
>
> **Two KB files disagreed about a physical board**, and the wrong one is the comparison table an
> agent reads to pick a board.
>
> **APPLIED 2026-08-25 by «#296» §5**, by deleting the unsupported half:
> `special_features: "Current limiting resistors (470 ohm in series with each LED and each switch)"`.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree, not from a status line. `hardware/addon-control-board.yaml` now contains no `pull` string at all — the fabricated pull-up credit is gone rather than reworded, which is the right disposition for a claim the board's own guide never made.
### F-345 — a worked example read a button with inverted flag polarity, under a comment asserting the opposite — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `deliverables/ai/P2/language/pasm2/concepts/basic-io.yaml`, `common_patterns.button_read`
> (`:243` before the fix): `TESTP #button_pin WZ      ' Z=1 if button pressed (low)`.
>
> **Evidence.** `TESTP` sets the flag **to** the pin state, not to its complement —
> `deliverables/ai/P2/language/pasm2/testp.yaml` encoding table: `c: IN[D[5:0]]`, `z: IN[D[5:0]]`;
> Silicon Doc, `sources/silicon-doc/part2-video-output.txt:291` — *"read pin D bit in INx and
> affect C or Z"*, with `TESTPN` (`:292`) as the inverting form. So `Z = 1` means the pin is
> **high** — the button **released**. The example ran its handler on exactly the wrong half of the
> input, and the following `IF_Z CALL` compiled perfectly.
>
> **This is why a clean compile is not a verification** — the same lesson as F-322, by a different
> mechanism (flag polarity rather than DIR state), found only on the semantic read.
>
> **APPLIED 2026-08-25 by «#296» §5:** `TESTP #button_pin WC ' C = pin state` / `IF_NC CALL
> #button_action ' a press shorts the pin to ground`. Swept: `TESTP`/`TESTPN` with a
> polarity-claiming comment appears nowhere else in the shipped set.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree, not from a status line. `code-examples/smart-pins-002-button-reading.yaml` now reads `if INA[BUTTON]` -> *"Button is pressed (high)"* with `else` -> *"Button is not pressed (low)"*. The comment asserts what the code does; the inversion is gone.
### F-346 — three worked examples were structurally unrunnable, and one rule contradicted its own two examples — `RESOLVED — VALIDATED IN THE SERVED KB, 2026-09-21`

> **VALIDATED IN THE SERVED KB 2026-09-21** («#344») — all four sites read back from `p2kb-mcp`
> (`p2kbPasm2BasicIo`, `p2kbArchSmartPin00000NormalMode`), which is what an agent actually receives,
> not from the repo tree and not from this register's status line. `led_blink` carries the `blink`
> label and `JMP #blink`; both patterns carry `CON`/`DAT` headers; `button_read` has its `poll` loop
> and a defined `button_action` stub; the smart-pin listing opens on `CALL #setup_pins` / `JMP
> #main_loop` with the two `LONG`s moved below the code beside `pin RES 1`.
>
> **Recompiled from the served bytes**, not from the repo: `led_blink` 28 bytes, `button_read`
> 32 bytes, smart-pin `pasm2_complete` 96 bytes, all exit 0 on `pnut-ts` 1.55.5.
>
> ⚠️ **And the compile validates only half of this finding — the control says so.** Feeding the
> ORIGINAL pre-fix form back through `pnut-ts` fails at `m211` ("Expected a unique constant name"),
> so the compiler does catch the missing `CON`/`DAT`. It does **not** catch `JMP #$`, execution
> beginning on data, or a `rule:` string contradicting its own examples — all three are legal. Those
> were re-validated by reading. The repaired rule now reads *"Set OUT to the desired state while the
> pin is still floating, then raise DIR"*, and its two examples agree with it: the `wrong:` limb sets
> OUT to the **un**desired state before raising DIR, which is the actual failure, rather than
> differing in ordering as the old pair did.

> **All four found by reading examples I had just compiled successfully.** None was caught by any
> gate; `pnut-ts` is the legality half only.
>
> | Where | What was wrong | Fix applied |
> |---|---|---|
> | `language/pasm2/concepts/basic-io.yaml` `common_patterns.led_blink` | `JMP #$ ' Repeat` — `$` is the **current** instruction's address, so this is a jump to self. The LED blinked once and the cog hung. Proved by byte-identity: `JMP #$` at cog address 1 compiles identically to `JMP #1`, and differently from `JMP #0`. | labelled `blink`, `JMP #blink` |
> | `language/pasm2/concepts/basic-io.yaml` `common_patterns.led_blink`, `.button_read` | neither fragment compiled — a bare `name = value` line with no `CON`, then `ORG` with no `DAT`; `button_read` also called an undefined `#button_action` | `CON`/`DAT` headers added; poll loop and a `button_action` stub added |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml` `pasm2_complete` | `ORG` was followed immediately by `led_pin LONG 56`, so **execution began on data** (cog address 0 held `$38`), and nothing ever called `setup_pins` — the pins the listing exists to configure were never configured | entry point added (`CALL #setup_pins` / `JMP #main_loop`); the two `LONG`s moved below the code beside `pin RES 1` |
> | `language/pasm2/concepts/basic-io.yaml` `safe_initialization_patterns.avoid_glitches` | `rule: "Set DIR before OUT to prevent output glitches"` — while **both** of its own examples set OUT first and DIR second. An agent reading the `rule:` string alone would do the opposite of what the file demonstrates. | `rule: "Set OUT to the desired state while the pin is still floating, then raise DIR"`, and the `wrong:` comment restated to name the actual failure (raising DIR latches the wrong level onto the pin) |
>
> **All four sites recompiled from the shipped YAML bytes after the fix**, and re-read.

---

## Four defects surfaced by the whole-KB promotion filter (2026-08-25, «#298» Plan §7) — F-348…F-351

> **Origin.** «#298» applied the belonging test — *can this block change the code an agent emits?* —
> to every quantitative block in the shipped KB (114) and every block the sprint's two purges removed
> (119). Three of these four are content defects the purge could not see; the fourth is an instrument
> artifact that inflates the Tier-2 count. The dispositioned list is
> `engineering/analysis/2026-08-25-whole-kb-promotion-filter.md`. Every line number below was read off
> disk on 2026-08-25.

### F-348 — a *cited* block shipped a pin-current limit five times the datasheet's absolute maximum, plus TTL logic levels the P2 datasheet does not contain — `DONE` (verified 2026-10-05 «#386»: block deleted from both twins, ±30 mA in io_pin_timing, v1.23.3)

> **Where:** `deliverables/ai/P2/language/pasm2/concepts/basic-io.yaml` and
> `deliverables/ai/P2/language/spin2/concepts/basic-io.yaml`, both `hardware_specifications`
> (11 lines, byte-identical twins). **Removed 2026-08-25**; backups at
> `.backups/deliverables/ai/P2/language/{pasm2,spin2}/concepts/basic-io.yaml.20260825-082653`.
>
> **What was wrong — five of six values:**
>
> | Shipped | P2 Datasheet |
> |---|---|
> | `max_current_per_pin: "150mA"` | **±30 mA** max allowable current per I/O pin — `sources/p2-datasheet/p2-datasheet-text.txt:2142` |
> | `VIL_max: "0.8V"` / `VIH_min: "2.0V"` | no such pair; a single ratiometric **Vih = Vxxyy × 0.3 / 0.5 / 0.7** — `:2163` |
> | `VOL_max: "0.4V at rated current"` | **15 mV** drop at 1 mA sinking, 510 mV at 30 mA — `:2172`, `:2174` |
> | `VOH_min: "2.4V at rated current"` | **−6 mV** drop at 1 mA sourcing, −580 mV at 30 mA — `:2176`, `:2178` |
>
> The four thresholds are 5 V-TTL boilerplate. The `150mA` is the F-327 drive-ladder fabrication's
> top rung, and it is **the number an agent uses to size an LED series resistor** — a 5× error in the
> direction that damages silicon.
>
> **Why two purges and a whole-class drive-strength sweep all missed it — measured, and it is a
> citation false negative, not a coverage gap.** `audit-yaml-claim-sourcing.py` judged the block
> **cited** because `INLINE_CITE_RE` matched the word **`datasheet`** inside
> `max_current_total: "Check datasheet for package limits"`. That is a **deferral**, not an
> attribution. Verified across the whole cited population: of the 30 cited quantitative blocks in the
> KB, this pair are the **only** two whose citation token identifies **no document at all** — every
> other one resolves to a named document ("P2 Datasheet", "Silicon Doc v35", "AKM AK5704 datasheet",
> "NXP PCF8523 datasheet", "W25Q128JV datasheet"). The nearest neighbour, and the one to watch, is
> `hardware/addon-rtc.yaml` `pin_mode_tip` — it defers to *"the RTC datasheet"*, which is also a
> deferral, but it identifies the document by role and its sibling `rtc_chip` block names it outright
> (NXP PCF8523). That is the line: **naming a document, however briefly, versus naming the class of
> document**. This is the same principle F-334 established — *a citation names a DOCUMENT* — in its
> remaining uncovered form.
>
> Note also that `4cecb02c` ("Correct the drive-strength mislabel class; both fidelity tiers now read
> zero") swept the class and did not reach these, because the fidelity tool is keyed on **named
> constants** and this block names none.
>
> **Nothing was lost.** The correct facts already ship, cited, in
> `deliverables/ai/P2/architecture/io_pin_timing.yaml` `absolute_maximum_ratings` (±30 mA per pin,
> ±10 mA diode) and `input_voltage_and_protection`. No `related:`/`see_also:` anywhere referenced
> `hardware_specifications`; `validate-crossref-keys.py` re-ran clean (3156 refs, 0 unresolved).
>
> **Owed:** «#299» decides whether anything returns in their place, source-first from the datasheet
> lines above. Nothing may return that states a per-pin current above ±30 mA.

### F-349 — PLL lock time is stated as ~10 microseconds in one place and ~10 milliseconds in four others; it is a delay an agent emits — `RESOLVED — validated on the served KB 2026-09-11`

> **The outlier:** `architecture/clock_system.yaml` `stabilization_timing` — `pll_lock: "~10 microseconds"`.
> Removed by «#293» (`15c84de5`), so it is **not currently shipping** — but it is a Population-2
> repopulation candidate and would return the contradiction.
>
> **The four that ship, all agreeing on milliseconds:**
> - `language/spin2/methods/clkset.yaml` `timing` — `cycles: "~10-20ms for PLL lock"`
> - `language/spin2/system-variables/clkmode.yaml` `notes` — *"PLL must lock before switching to PLL source (~10ms)"*
> - `language/pasm2/hubset.yaml` `safe_clock_switching` — *"Wait for PLL to lock (~10ms)"*, and its
>   step_2 code computes `clkfreq/100` clocks = 10 ms
> - `language/pasm2/asmclk.yaml` `expansion_details` — emits `WAITX ##20_000_000/100`, a 10 ms wait at 20 MHz
>
> **Why it matters:** this is not a documentation nicety. It is the literal WAITX operand between
> configuring the PLL and switching to it. A three-orders-of-magnitude error in the short direction
> switches the clock source before lock.
>
> **RESOLVED 2026-08-25 by «#299» — the answer is 10 ms, and it is stated outright, not inferred.**
> Three Parallax documents state it, and each was read on **two independent extraction paths** (the
> raw docling text and the reconstructed table):
> - **P2 Datasheet 2022/11/01** p.18 — %E row: *"XI input must be enabled by %CC. Allow 10ms for
>   crystal+PLL to stabilize before switching over to PLL clock source."*
>   (`sources/p2-datasheet/p2-datasheet-text.txt:783-785`; same cell at
>   `sources/p2-datasheet/complete-tables-reference.md:133`). %SS row: *"CC != %00 and E=1, allow
>   10ms for crystal+PLL to stabilize before switching to PLL"* (`:828`, `:151`).
> - **Propeller 2 Documentation v35** — identical wording (`sources/silicon-doc/part3-interrupts.txt:528-529,:576`).
> - **P2 Hardware Manual 2022/11/01** — identical wording
>   (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:572,:592`; `complete-tables-reference.md:105,:123`).
>
> All three also *emit* the wait in their own worked example: `WAITX ##20_000_000/100` — 10 ms at the
> RCFAST rate the code is still running at (`p2-datasheet-text.txt:857-859`;
> `silicon-doc/p2-documentation.txt:6266`; Spin2 v55 states the same line twice, once for `clkmode_`
> and once for `ASMCLK`, `sources/spin2-v55/spin2-v55-text.txt:1725,:1738`). The crystal-only case is
> **5 ms** (`p2-datasheet-text.txt:830`). The `~10 microseconds` figure has no source and is not
> restored; `architecture/clock_system.yaml stabilization_timing` returned carrying the 10 ms / 5 ms
> pair with the citation and a `conflict_resolved` note.
>
> 🔴 **A FIFTH LOCATION THIS FINDING DID NOT NAME, found by working the file rather than the list.**
> `architecture/clock_system.yaml programming_examples` carried **`WAITX ##20_000_000/10000  ' Wait
> 100µs for PLL lock`** in TWO examples — `pll_160mhz_from_20mhz_crystal` and `overclock_250mhz`. The
> sourcing gate cannot see them because they sit inside a code region, which the gate strips by
> design; that is the same blind spot F-333 records for prose. Both corrected in place to
> `WAITX ##20_000_000/100  ' Wait ~10ms for crystal+PLL to stabilize`. **Class-wide sweep run:**
> `grep -rn "PLL lock\|PLL to lock\|pll_lock\|for PLL" --include=*.yaml deliverables/ai/P2/` — the
> only remaining hits are the four surviving millisecond statements this finding already named, plus
> the new cited block. No sixth location.
>
> `PENDING-VALIDATION` — the KB edit is applied and gate-verified; only the YAML release is owed.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree, not from a status line. every site now states **10 ms**: `clkmode.yaml:113` quotes the Silicon Doc verbatim at `silicon-doc-text.txt:2635` (*"Allow 10ms for crystal+PLL to stabilize"*), `hubset.yaml` :60/:73/:97 and `clock_system.yaml` :93/:172 agree, and `clkset.yaml:43`'s `~10-20ms` is a consistent range rather than the microsecond error. `clock_system.yaml:177` carries the adjudication in place: *"An earlier form of this block stated pll_lock as ~10 microseconds. Three Parallax sources state 10ms, each via two independent extraction paths (raw text and reconstructed table); the microsecond figure has no source."* The wrong figure is not merely replaced — the file records why it lost.
### F-350 — the F-328(b) eval-board fabrication class is not confined to `p2-eval-board.yaml` — `RESOLVED — VALIDATED IN THE SERVED KB, 2026-09-21`

> **VALIDATED IN THE SERVED KB 2026-09-21** («#344») — `p2kbHwP2HardwareFeatureComparisonP2Hardware
> FeatureComparison` read back from `p2kb-mcp`, not from the repo tree. All five keys carry the
> re-derived values (`3.55 x 3.55 in` · two micro-USB, *"No USB-C and no barrel jack"* · eight I/O
> Pin Breakout Edge Headers in 8 groups of 8 · 16 MB flash with the P2 *"soldered on the board --
> this is NOT an edge-module carrier"* · `eval_board_addons` rewritten with its `correction_note`),
> the three fabrications are absent, and 64006G is the Goertzel board.
>
> **THE CLASS WAS SWEPT, NOT THE FILE** (D5), and the sweep carried a control, because an absence
> found by one search is not an absence. Pattern — `USB-C`, `127x89`, `Up to 2 add-on`, `A-side`/
> `B-side`, the three invented `P2-EVAL-*` part numbers, `Combined Digital I/O`, `Stereo DAC
> output`, `27x40` — run over the whole shipped tree: **zero live occurrences.** The same pattern
> run over the pre-fix backups **hits every term**, which is what makes the live zero mean
> something rather than meaning the search was broken.
>
> Every live hit was read rather than counted, and all are benign: the `corrections_applied_2026_08_25`
> and `correction_note` blocks recording what was removed; `p2-hardware-selection-guide.yaml:218-219`,
> which is the *repair* (*"the #64000 has neither a USB-C socket nor a barrel jack"*); and
> `addon-serial-device.yaml:97` (*"microUSB connectors (not USB-C)"*, correct). One hit was an
> artifact of the search itself — `USB-C` matching inside **USB-c**apable at `:24` — the same
> count-versus-read trap this task was told to expect.

> **Where:** `deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml`,
> `development_boards.p2_eval_board` and `compatibility_matrix.eval_board_addons`. Backup at
> `.backups/deliverables/ai/P2/hardware/p2-hardware-feature-comparison.yaml.20260825-082759`.
>
> F-328(b) catalogued invented #64000 hardware in `p2-eval-board.yaml`. Sweeping the **class** rather
> than the occurrence found the same invented peripherals in a second file, which F-328 never named.
>
> **Removed 2026-08-25 (fabricated — the board has none of them; `grep -rn -i "\bVGA\b\|HDMI\|resistor
> DAC\|audio\|prototyp\|breadboard"` over `sources/p2-eval-board/complete-p2-eval-board-reference.md`
> returns zero hits):** `audio_capability: "Stereo DAC output"` · `video_capability: "VGA output"` ·
> `breadboard_area: "Large prototyping area"`.
>
> **Still shipping and WRONG — owed to «#307», needs re-derivation from the repaired capture, not deletion:**
>
> | Key | Ships | `complete-p2-eval-board-reference.md` |
> |---|---|---|
> | `development_boards.p2_eval_board.dimensions` | `127×89mm` | **3.55″ × 3.55″** (`:62`, `:260`) ≈ 90 × 90 mm |
> | `…usb_connectivity` | `USB-C programming + micro-USB serial` | **two micro-USB** (`:59`, `:76`); no USB-C anywhere |
> | `…addon_headers` | `Two 2x6 headers for add-on boards` | **eight** I/O Pin Breakout Edge Headers (`:35`, `:52`) |
> | `…flash_memory` | `16MB (with P2-EC)` | 16 MB correct; the P2 is **soldered on-board** (`:124`), not an edge module |
> | `compatibility_matrix.eval_board_addons` | `Up to 2 add-on boards`; `A-side (P32-P39) + B-side (P24-P31)` | **8 sets of 8** covering all 64 pins (`:52`) |
>
> **The generalizable half.** F-328(b)'s own lesson was that a purge keyed on missing citations cannot
> see a wrong scalar or an invented section. This adds the sibling: **a finding scoped to one file
> cannot see the same fabrication copied into another.** The class-wide sweep is what found it, and it
> is the only thing that would have.
>
> **APPLIED 2026-08-25 («#307»).** All five keys re-derived from the repaired capture and cited, in
> `development_boards` and `compatibility_matrix` — `dimensions` → 3.55 in x 3.55 in ·
> `usb_connectivity` → two micro-USB (PC-USB 500 mA / AUX-USB 2000 mA), no USB-C, no barrel jack ·
> `addon_headers` → eight I/O Pin Breakout Edge Headers · `flash_memory` → 16 MB on the board, the
> P2 soldered on (not an edge-module carrier) · `eval_board_addons` → eight headers in 8 groups of 8
> covering all 64 pins, replacing "Up to 2 add-on boards" and the invented A-side/B-side split.
> **And the class ran wider than five:** the same read found invented carrier part numbers, wrong
> carrier and edge-module dimensions, a fabricated "3.3V input only / edge castellations" mini
> breakout, an eval board with a barrel jack it does not have, and **`64006G` described as a
> "Combined Digital I/O" board** — it is the Goertzel board, i.e. the F-121 fabricated-name family
> in a file F-121 never named. Full list in the file's own `corrections_applied_2026_08_25` keys and
> in **F-353**. The file now cites per block; its six Tier-2 blocks left the advisory lane.
>
> Status: `RESOLVED` — applied, gate-verified, released, and read back from the served KB on
> 2026-09-21 («#344»). The YAML release that was owed here has landed.

### F-351 — the sourcing gate reads Parallax part numbers, Unicode code points and an ISO designator as amperes; 12 blocks are pure instrument artifacts — `RESOLVED`

> **RESOLVED 2026-08-25 by «#305»**, both repairs as suggested here plus the thousands-separator
> one. A bare `A` now requires at most three integer digits (a current in this domain is
> `1.5A`/`20A`/`100A`; a part number or standard designator is a four-or-more digit run);
> `U+XXXX` is masked alongside `%binary` and `$hex`; the number pattern accepts `,` groups so
> `3,333,333 Hz` is one token rather than `333 Hz` + `000 Hz`. Deliberately NOT applied to the
> other units — `500,000,000 Hz` and `2000Ohm` are real claims.
>
> **Measured: 9 blocks, not 10.** The tenth on this finding's list
> (`hardware/p2-hardware-feature-comparison.yaml` `selection_criteria`) had already been drained
> by an earlier task and was not in the population when «#305» ran. The other nine are exactly
> as listed. Five negative-control cases were added — the three artifacts MUST NOT fire, and a
> real `1.5A`/`4A` current and a `100A` inrush MUST STILL fire, so the fix cannot be widened
> into a disarm.

> **Instrument:** `engineering/tools/validation/audit-yaml-claim-sourcing.py`, `QTY_RE`. **Do not fix
> here — «#305» owns instrument repair** (see F-335/339/340/341). Filed so the Tier-2 count is read
> correctly in the meantime.
>
> **Mechanism.** `QTY_RE` accepts a bare `A` as amperes with only `(?<![\w%$])` guarding the number's
> left edge. That guard passes at a string's start and after `+`, so:
>
> | Text | Read as | Real meaning |
> |---|---|---|
> | `"64006A"` | 64006 amperes | a Parallax part number |
> | `unicode: "U+221A"` | 221 amperes | the SQUARE ROOT code point |
> | `ISO/IEC 14443 A/MIFARE` | 14443 amperes | the RFID standard's designator |
>
> **Measured, whole-KB:** **10 of the 84 Tier-2 blocks** state no quantity at all — every token in them
> is one of the three artifacts above: `hardware/addon-control-board.yaml` `part_number`, `aliases`,
> `availability` · `hardware/hardware-compatibility-matrix.yaml` `physical_stacking_constraints`,
> `optimal_configurations` · `hardware/p2-hardware-feature-comparison.yaml` `selection_criteria` ·
> `hardware/p2-hardware-selection-guide.yaml` `decision_tree`, `application_specific_guides` ·
> `hardware/p1_rom_font_character_set.yaml` `character_categories` ·
> `community/obex/objects/4070.yaml` `object_metadata`. Two further **cited** blocks are the same
> artifact (`community/quick-bytes/{five-buttons-on-one-pin,leds-beyond-the-basics}.yaml` `quick_byte`,
> both on `related_boards: 64006A`). **Twelve blocks KB-wide.**
>
> **So the true Tier-2 advisory population is 74, not 84** — the gate's own number over-reports by 12%,
> and every one of the ten sits in `hardware/`, the tree where part numbers are densest.
>
> **A second, milder artifact: thousands separators split.** `range: "3,333,333 Hz to 500,000,000 Hz"`
> in `language/spin2/constants/special-configuration-symbols.yaml` `clock_configuration` yields the
> tokens `333 Hz` and `000 Hz`. This does not create a false finding (the block carries real MHz) but
> it inflates the per-block quantity count the advisory prints.
>
> **Suggested repair for «#305» to adjudicate:** require the ampere unit to be preceded by a word
> boundary that is not a digit-run continuation (a part number is `\d{4,}[A-Z]`), and mask `U+XXXX`
> alongside the existing `%binary`/`$hex` masking. Both are testable with the negative-control harness
> the tool already carries.

### F-353 — the 58 in-scope blocks: 34 returned cited, 24 held in the ingestion tree, 0 whole-block gaps — and six wrong scalars in SURVIVING blocks that only a source-first read could find — `RESOLVED — VALIDATED IN THE SERVED KB, 2026-09-21`

> **VALIDATED 2026-09-21** («#344»), all three limbs, exhaustively rather than by sample.
>
> **(a) + (b) — 34 of 34 blocks present, 34 of 34 carrying their OWN citation.** Checked
> mechanically across all 15 files; every one names an `engineering/ingestion/sources/` path inside
> the block itself, so none of them leans on a file-level or sibling citation.
> ⚠️ **The checker was falsified before its result was believed.** Its first form accepted a
> file-level `source:` anywhere as citation for any block, which would have passed all 34 whatever
> the truth. Re-run with that fallback removed: same 34/34. Control, by the same method: three
> blocks the KB itself declares authored-here guidance (`summary_recommendations`, `notes`,
> `comparison_categories`) return NO CITATION REACHABLE, and two known-cited blocks return cited —
> so the instrument discriminates.
>
> **(c) — all six scalars corrected**, each read in place: `edge-32mb-module` is `P2-EC32MB`
> throughout with a note recording that **#64000-ES is a different product** · `edge-standard-module`
> `ec32mb_module.fully_free_pins: 40` (with `accessible_pins: 46`) · all three Edge carriers state
> they have **no** on-board USB-to-serial and name the Prop Plug as the only wired path, the
> breadboard carrier with the guide citation at its `connectivity.programming` · `edge-mini-breakout`
> `blocked_pins` now says P32-P55 *"may be reached by adding jumper wires"* rather than "not
> accessible". `p2-eval-board.yaml:190` still reads "USB (primary method)" and is **correct** — the
> #64000 does carry built-in FTDI — exactly as this finding predicted.
>
> **Gate effect re-measured, not quoted:** `audit-yaml-claim-sourcing.py` Tier 1 remains **0** across
> 1131 files, and Tier 2 now reads **27** advisory blocks — down from the 78 recorded here at filing.

> **THE THREE NUMBERS.** **34 restored with a trace · 24 held in ingestion · 0 gap.** 34 + 24 = 58;
> plus «#299»'s `getct.yaml description` = F-334's 59. Every ACTIONABLE block came back; no
> ACTIONABLE block failed to verify.
>
> **Restored (34), each written from the guide named in its own `source:` key:**
>
> | File (`deliverables/ai/P2/hardware/`) | Blocks returned | Written from |
> |---|---|---|
> | `edge-32mb-module.yaml` | `specifications` · `pin_mapping` · `boot_modes` · `limitations` · `development_workflow` | P2-EC32MB Edge Module Rev B Guide v2.0 — `sources/edge-32mb-module/edge-32mb-module-narrative.txt` |
> | `edge-standard-module.yaml` | `specifications` · `pin_mapping` · `boot_modes` | P2-EC Edge Module Rev D Product Guide v3.0 — `sources/edge-standard-module/edge-standard-module-narrative.txt` |
> | `p2-eval-board.yaml` | `specifications` | #64000 Eval Board Rev C Guide v2.0 — `sources/p2-eval-board/complete-p2-eval-board-reference.md` (the F-250 forced-OCR re-ingestion) |
> | `addon-motor-driver.yaml` | `signal_map` · `pwm_control` · `current_sense` · `specifications` | #64010 Universal Motor Driver Guide v2.0 — `sources/p2-universal-motor-driver/complete-p2-universal-motor-driver-content.md` |
> | `hub75_adapter.yaml` | `description` · `specifications` · `software_features` · `notes` | #64032 HUB75 Adapter Official Specifications — `sources/p2-hub75-adapter/p2-hub75-adapter-official-specs.md` |
> | `programming-prop-plug.yaml` | `description` · `reset_option` · `specifications` | #32201 Prop Plug Guide v3.0 Rev E — `sources/propplug-rev-e/complete-propplug-rev-e-reference.md` |
> | `addon-serial-host.yaml` | `signal_map` · `usb_host_capabilities` · `development_workflow` | #64006 Series Guide v2.0 — `sources/p2-eval-add-on-boards/p2-eval-add-on-boards-text.txt:99-134` |
> | `addon-serial-device.yaml` | `description` · `signal_map` | same guide, `:253-284` |
> | `addon-goertzel-touch.yaml` | `specifications` | same guide, `:24-46` + `:290-317` |
> | `addon-hd-audio.yaml` | `description` · `dac_board` | #64014 HD Audio Guide v1.0 — `sources/P2-HD-Audio-Add-on/P2-HD-Audio-Add-on-text.txt` |
> | `addon-hyperram-hyperflash.yaml` | `specifications` · `configuration` | #64004-ES Guide v1.0 — `sources/hyperRam-n-hyperFlash/complete-hyperram-hyperflash-reference.md` |
> | `addon-rtc.yaml` | `description` | #64013 RTC Guide v1.0 — `sources/P2-RTC-Add-on/P2-RTC-Add-on-text.txt:15-37` |
> | `addon-wx-wifi.yaml` | `pin_descriptions` | #32420 WX Wi-Fi Module Guide v1.0 — `sources/parallax-wx-wifi/complete-wx-wifi-reference.md:96-114` |
> | `edge-mini-breakout.yaml` | `connectivity` | #64019 Mini Breakout Guide v1.1 — `sources/edge-mini-breakout/edge-mini-breakout-narrative.txt` |
> | `edge-standard-breakout.yaml` | `connectivity` | #64029 Breakout Board Guide v1.0 — `sources/edge-breakout-board/edge-breakout-board-narrative.txt` |
>
> **Held in ingestion (24)** — CORRECT-BUT-NOT-ACTIONABLE per «#298», and each one's content is
> demonstrably still readable in the ingestion tree, so removing it from the KB lost nothing:
> `addon-hd-audio` `set_contents` (`P2-HD-Audio-Add-on-text.txt:17`) · `use_cases` (`:32-35`) ·
> `addon-motor-driver` `power_signals` (`complete-p2-universal-motor-driver-content.md:154-160`) ·
> `protection` (`:41`, `:170`) · `addon-rtc` `power_signals` (`P2-RTC-Add-on-text.txt:56`, `:68`) ·
> `specifications` (`:41-52`, `:89-93`) · `addon-wx-wifi` `part_variants`
> (`complete-wx-wifi-reference.md:5`, `:26-29`) · `specifications` (`:44-61`) ·
> `edge-breadboard-carrier` `power_specifications` / `specialized_features` / `specifications`
> (`edge-module-breadboard-narrative.txt:53-57`, `:60-69`, `:163`, `:167-171`) ·
> `edge-mini-breakout` `power_management` / `specifications`
> (`edge-mini-breakout-narrative.txt:43`, `:54-65`) · `edge-standard-breakout` `power_management` /
> `specifications` (`edge-breakout-board-narrative.txt:35-36`, `:42-64`, `:191`) ·
> `addon-hyperram-hyperflash` `host_note` (`complete-hyperram-hyperflash-reference.md:95-96`) ·
> `addon-serial-device` `rev_b_5v_note` (`p2-eval-add-on-boards-text.txt:113-115`;
> `boards/addon-serial-device-64006f.md:25`) · `specifications` (`:39-42` — see F-354 for the one
> item of it that is NOT there) · `addon-serial-host` `description` / `limitations` /
> `power_requirements` / `specifications` (`:99-115`, `:39-42`) · `edge-standard-module`
> `revision_history` (`edge-standard-module-narrative.txt:519-551`) · `hub75_adapter`
> `power_requirements` (`p2-hub75-adapter-official-specs.md:128-142`, with the caveat in F-354).
>
> 🔴 **SIX WRONG SCALARS IN BLOCKS THE PURGE NEVER TOUCHED.** Reading the guides rather than the
> removal list is what surfaced these; a citation-keyed purge is structurally blind to all of them
> (the same lesson F-328(b) records). All six are **corrected in place** and cited:
>
> | Where | Shipped | The guide says |
> |---|---|---|
> | `edge-32mb-module.yaml` `alternate_part` + one alias + `availability.part_lookup` | `64000-ES` | The guide names this module **#P2-EC32MB** throughout (`edge-32mb-module-narrative.txt:17`, `:41`, `:46`, `:557`). **#64000-ES is a different product** — the limited-edition P2-ES *Eval Board* (`p2-eval-add-on-boards-text.txt:42`; `hyperram-hyperflash-text.txt:22`). A search for the eval board was landing on the edge module. The bad identity traces to a derived analysis file, `sources/edge-32mb-module/edge-32mb-cross-source-analysis.md:16`, not to the guide. |
> | `edge-standard-module.yaml` `comparison_with_32mb.ec32mb_module.fully_free_pins` | `38` | **40** — "Smart I/O pins: 46 accessible, 40 fully free" (`edge-32mb-module-narrative.txt:120`) and "P0-P39 are fully free" (`:417`). The same file's own `compatibility.alternatives.tradeoff` already said 40, so the file contradicted itself. |
> | `edge-mini-breakout.yaml`, `edge-standard-breakout.yaml`, `edge-breadboard-carrier.yaml` — `advantages`, `development_workflow`, `programming.methods`, and the carrier's `connectivity.programming` | "USB programming integrated", "USB (primary - built-in)", "Built-in USB-to-serial", "Connect USB for programming and power" | **None of the three Edge carriers has a USB-to-serial converter.** All three guides say the same thing: "Programming: Serial up to 2 MBaud; **requires** Prop Plug (#32201) programming adapter" (`edge-mini-breakout-narrative.txt:60-61`, `edge-breakout-board-narrative.txt:59`, `edge-module-breadboard-narrative.txt:67`). An agent told the board has built-in USB emits no Prop Plug step at all. Class-wide sweep run: `grep -rn "built-in\|integrated" … hardware/` — the only remaining "USB (primary method)" is `p2-eval-board.yaml:190`, where it is **correct** (the #64000 does carry a built-in FTDI-to-USB interface, `complete-p2-eval-board-reference.md:78`). |
> | `edge-mini-breakout.yaml` `pin_access.blocked_pins` | `P32-P55 (not accessible)` | "Pins P32–P55 **may be accessed** by adding jumper wires on the bottom side of the PCB to the mini prototyping sections" (`edge-mini-breakout-narrative.txt:31-33`). Not accessible *at a header*; not unreachable. |
>
> **F-350's five, and eleven more of the same class, in `p2-hardware-feature-comparison.yaml`.**
> F-350 named five wrong keys still shipping in that file. Correcting them source-first meant
> reading every quantity in the file, and the fabrication went well past five — see the file's own
> `corrections_applied_2026_08_25` keys for the full list. Beyond F-350's five: all three Edge
> carriers carried **invented part numbers** (`P2-EVAL-STD-BREAKOUT`, `P2-EVAL-MINI-BREAKOUT`,
> `P2-EVAL-BREADBOARD-CARRIER` — the real parts are #64029, #64019, #64020) and wrong dimensions;
> the mini breakout was described as "3.3V input only" with "All 64 pins on edge castellations"
> (it is 5 VDC via a barrel jack, with 40 pins at 0.1″ headers); both edge modules carried
> `27×40mm` (the guides say 37 × 51.7 mm); the eval board's programming interface read "USB-C +
> micro-USB + PropPlug header" and its power input "5V USB or 6-15V barrel jack" (the #64000 has
> **two micro-USB sockets and no barrel jack at all**); and **`64006G` was described as a "Combined
> Digital I/O" board with 4 LEDs and 4 switches** — #64006G is the **Goertzel** board, which is the
> F-121 fabricated-board-name family reappearing in a file F-121 never named. All corrected or
> removed against the guides, with a `source:` per block.
>
> **Gate effect, measured.** `audit-yaml-claim-sourcing.py` Tier 1 stayed at **0** across all edits.
> Tier 2 moved **84 → 78**: the six `p2-hardware-feature-comparison.yaml` blocks left the advisory
> lane because that file now cites. The `hardware/` share went 39 → 33. Nothing changed tier in the
> other direction, and no block was demoted.
>
> Status: `RESOLVED` — every edit is applied, gate-verified, released, and read back from the served
> KB on 2026-09-21 («#344»). The YAML release that was owed here has landed.

## `hardware/p2-eval-board.yaml` describes a board the #64000 guide does not (2026-08-24, F-250 re-ingestion) — F-328

> **Origin.** Repairing the #64000 source (F-250 — its extraction had lost every numeral)
> made it possible, for the first time, to check the board YAML against what the guide
> actually says. Every item below was read off the repaired capture
> (`engineering/ingestion/sources/p2-eval-board/complete-p2-eval-board-reference.md`) and
> confirmed on the rendered page. **Nothing here is fixed in this filing** — the ingestion
> head produces raw source data; the YAML is the purge/repopulate tasks' work.

- **F-328 — `deliverables/ai/P2/hardware/p2-eval-board.yaml` carries claims the #64000 Rev C
  guide contradicts, plus whole blocks describing hardware the board does not have; and the
  guide itself contradicts itself on one pin pair.** — `DONE` (verified 2026-10-05 «#386»: the owed YAML release landed; p2-eval-board.yaml v1.23.3) · Two separable halves.

  **(a) The source contradicts itself — a genuine documentary conflict, not an extraction
  defect.** The #64000 guide's §18 "microSD Card Socket" (p.12) lists *"P58 - DI/CD (data in
  and card detect); P59 - DO (data out); P60 - /CS; P61 - CLK"*. Its own I/O Pin Assignments
  table (p.15) lists *"P58 microSD MISO (SDO); P59 microSD MOSI (SDI); P60 microSD CS; P61
  microSD CLK"*. P60/P61 agree; **P58 and P59 are opposite in direction between the two
  places**. Both readings are confirmed on the rendered pages and in the original text layer
  (whose table font preserved the fragments `" D MI O ( DO)"` / `" D MO I ( DI)"`). The guide
  does not resolve it, and this source alone cannot settle which is right.

  **RESOLVED 2026-08-24 by cross-source normalization — no bench, no schematic needed.** The
  answer is **P58 = MISO** (card `DO`, a P2 *input*) and **P59 = MOSI** (card `DI`, a P2
  *output*). The guide's own p.15 I/O table is **correct**; its §18 bullet list is a
  **documentary error in the source** and is recorded as errata. Five independent authorities
  agree, in descending strength:
  1. **`engineering/ingestion/sources/rom-booter/rom_booter_v33_01j.lst:135-138`** — the P2's
     own boot ROM, which is the implementation itself and therefore conclusive:
     `spi_cs = 61 'pin SPI memory select (also sd_ck)` · `spi_ck = 60 '...clock (also sd_cs)` ·
     `spi_di = 59 'pin SPI memory data in (also sd_di)` · `spi_do = 58 'pin SPI memory data
     out (also sd_do)`. It names `sd_di` = **59** and `sd_do` = **58** outright.
  2. **`sources/silicon-doc/p2-documentation.txt:9281-9302`** — the boot-pin table, flattened
     by extraction but unambiguous once re-columned: `P59 (output)` ↔ SPI flash `DI (input)` ↔
     SD card `DI (input)`; `P58 (input)` ↔ flash `DO (output)` ↔ SD `DO (output)`. Note the SD
     column swaps CLK/CSn relative to flash (P61 = SD CLK, P60 = SD CSn), which independently
     corroborates §18's *"P60 - /CS; P61 - CLK"*.
  3. **`sources/p2-eval-board/complete-p2-eval-board-reference.md`** (the repaired capture of
     this very guide) — p.15 I/O table: P58 microSD MISO (SDO), P59 microSD MOSI (SDI).
  4. **`sources/p2-microSD-addon/64009-P2-microSD-AddOn-Guide-v1.0.md:41-42`** — supplies the
     vocabulary key that makes the two statements comparable at all: *"MOSI → Connects to
     SD-DI (CMD/MOSI)"* and *"MISO → Series 240R from SD-DO (MISO)"*. So card `DI` ≡ bus
     `MOSI` and card `DO` ≡ bus `MISO`; the two guides are not using different conventions.
  5. **`sources/p2-board-pin-mapping-knowledge.md:129-130`** — P58 = Flash SPI DO/MISO,
     P59 = Flash SPI DI/MOSI.

  **Consequence: the KB is already correct and must NOT be changed.**
  `P58: "microSD MISO (SDO) / Flash SPI DO"` stands, now with an authority behind it rather
  than a coin flip. Half (a) is therefore **not** a KB defect and is **not** work for the
  repopulation tasks — it is a source errata plus a citation. When «#307» repopulates the
  microSD block, cite the ROM booter (1) or the silicon-doc boot table (2), **never §18**.
  *Lesson worth keeping: the apparent contradiction was legible only after a third source
  supplied the DI/DO ↔ MOSI/MISO vocabulary key. A two-source conflict is sometimes a missing
  translation, not a disagreement — check for the key before escalating to the bench.*

  **(b) The YAML asserts hardware the guide does not describe.** Uncited *and* wrong, which is
  why it is filed rather than left to the uncited-block purge — a purge keyed on missing
  citations will not necessarily reach a scalar or a whole fabricated section:
  - `specifications.microcontroller.revision: "Rev D"` — the guide is **Rev C silicon**
    throughout (`P2X8C4M64PES`, "Rev C Silicon", "Rev C silicon approved for production").
  - `clock_speed: "20MHz crystal, PLL to 320MHz"` — the guide states 20 MHz crystal,
    **recommended maximum 180 MHz**, "overclocking possible beyond 300 MHz", and a **390 MHz**
    experiment. `320MHz` appears nowhere.
  - `built_in_peripherals.proto_area.breadboard_section: "Basic prototyping area"` — **the
    #64000 has no prototyping area.** Fabricated whole.
  - the `video_audio:` block (`vga_support` / `hdmi_support` / `audio_output`) — the guide
    never mentions VGA, HDMI, video, or resistor DACs. Fabricated whole.
  - `connectivity.programming` lists a **Prop Plug (#32201) on a "4-pin header"** and
    `connector: "USB-B or USB-C"` — the guide describes **micro-USB** only, plus the WX WiFi
    SIP module (#32420S) on the P56–P63 header. It never mentions a Prop Plug.
  - `switches.user_switches: "TBD quantity"` — there are none; the switches are the reset
    button and a **4-position mode dip bank** (USB RES · FLASH · P59 △ · P59 ▽).
  - `headers.connector_type: "Standard 0.1 inch headers"` — the I/O breakout headers are
    **2×6 edge headers** (eight of them); the 0.1″-spaced feature is the AUX power **pads**.
  - `flash_size: "TBD - check documentation"`, `physical.dimensions: TBD`,
    `temperature_range: "Commercial grade"`, `current_consumption: "TBD"` — the guide states
    **16 MB (128 Mbit) W25Q128JVSIM**, **3.55″ × 3.55″** with four mounting holes 40 mm apart,
    and **−40 to +85 °C**. These are `TBD` only because the extraction had no digits in it.
  - `supply_voltage: "5V or USB powered"` — the guide: **two micro-USB** inputs (PC-USB
    500 mA, AUX-USB 2000 mA), absolute maximum **5.5 VDC**, plus optional 5V/GND AUX pads at
    4.5–5.5 V. There is **no barrel jack**.
  - `expansion_ecosystem.individual_addons` names #64032 HUB75 and #64008 MicroBUS — not in
    this source (they may be sourced elsewhere; that is the repopulation step's call).

  **→ the sprint's purge/repopulate tasks** (remove-all, then re-derive source-first from the
  repaired capture). Do **not** cite-in-place: half of (b) would then acquire a citation to a
  guide that says the opposite. Half (a) is **closed** — see the resolution above; it needs a
  citation swap, not a decision.

  > **PURGE PASS APPLIED 2026-08-24 («#294») — it reached FOUR of the ten (b) items; SIX stand.**
  > The uncited-block purge removed exactly one top-level block from this file,
  > `specifications` (was `:24-56`, 33 lines). **What that took out (4 of 10):** the `Rev D`
  > scalar (`specifications.microcontroller.revision`, was `:27`); `clock_speed: "20MHz crystal,
  > PLL to 320MHz"` (was `:29`); `supply_voltage: "5V or USB powered"` (was `:52`); and the four
  > TBDs whose answers are in the repaired guide — `flash_size` (was `:37`), `physical.dimensions`
  > (was `:44-48`), `current_consumption` (was `:54`), `temperature_range` (was `:55`).
  >
  > **What SURVIVES the purge, untouched, and is therefore still owed to «#307»** (post-purge
  > line numbers, file is now 172 lines):
  > - `built_in_peripherals.proto_area` (`:54-56`) — the **fabricated prototyping area**.
  > - `switches.user_switches: "TBD quantity"` (`:48`).
  > - `headers.connector_type: "Standard 0.1 inch headers"` (`:52`).
  > - the whole `video_audio:` block — `vga_support` / `hdmi_support` / `audio_output`
  >   (`:70-73`). Fabricated whole; still standing.
  > - `connectivity.programming` (`:58-65`) — `connector: "USB-B or USB-C"` and Prop Plug
  >   **#32201**.
  > - `expansion_ecosystem.individual_addons` (`:127-134`) — #64032 HUB75 / #64008 MicroBUS.
  >
  > **Why all six were missed — one reason, measured, not the one that looks likely.** Each of
  > the four surviving blocks (`built_in_peripherals`, `connectivity`, `video_audio`,
  > `expansion_ecosystem`) states **zero unit-bearing quantities**: "0.1 inch", "16 MB", "32 MB",
  > "4-pin", "#32201" carry no unit the gate counts (inch, MB and bare integers are structure by
  > design). A quantity-keyed gate therefore never looks at any of them. Note what is NOT the
  > cause: `built_in_peripherals` does carry a genuine `source:` for the LED bank (`:45`), which
  > would have silenced it too — but that is belt-and-braces, not the operative reason, and the
  > other three carry no citation at all and were still passed over.
  >
  > **The generalizable lesson:** a purge keyed on MISSING CITATIONS is orthogonal to a WRONG
  > SCALAR and to an INVENTED SECTION. It caught the four items that happened to carry volts,
  > megahertz, or a `TBD` inside a quantitative block, and passed over the six that are pure
  > prose — including both wholly fabricated sections. Removal is not a substitute for the
  > re-derivation; it guarantees only that what remains was never *uncited*, never that it is
  > *true*.

  > **(b) CLOSED OUT 2026-08-25 («#298» + «#307»).** «#298» removed five of the six surviving
  > items as UNSOURCED and kept `expansion_ecosystem.individual_addons` (a cross-reference roster,
  > not a fabrication). «#307» then wrote the TRUE replacements back as a cited `specifications`
  > block on `p2-eval-board.yaml`, source-first from the repaired capture: Rev C silicon
  > (P2X8C4M64PES), 20 MHz crystal with a recommended maximum of 180 MHz, 16 MB W25Q128JVSIM,
  > 3.55 in x 3.55 in, -40 to +85 C, two micro-USB inputs (500 mA / 2000 mA) with an absolute
  > maximum of 5.5 VDC, eight I/O Pin Breakout Edge Headers, and the four-switch mode bank
  > (USB RES · FLASH · P59 up · P59 down) in place of the "TBD quantity" user switches. The
  > fabricated prototyping area, VGA/HDMI/audio block, USB-B/USB-C connector and Prop Plug #32201
  > are gone and were not written back. See **F-353**.

  Status: `DONE` (2026-10-05: the owed YAML release landed) — **(a) RESOLVED 2026-08-24** by cross-source normalization against
  the ROM booter and the silicon-doc boot table: P58 = MISO / P59 = MOSI, the KB is already correct
  and stands unchanged, and the guide's §18 is source errata. **(b) applied 2026-08-25** as
  described above; only the YAML release is owed.

---

## The `hardware/` uncited-block purge — the removal record, and a citation token that silences the gate (2026-08-24, «#294») — F-334

> **Origin.** Plan §4 part 2 removed all 48 Tier-1 uncited quantitative blocks from
> `deliverables/ai/P2/hardware/`, taking `audit-yaml-claim-sourcing.py` to **0 Tier 1 / exit 0**
> across 1129 files for the first time. Two things are recorded here: the **removal record**,
> which is «#307»'s working list (F8 — «#307» must not have to do git archaeology), and a
> detector defect the pass proved while working inside these files.

### Removal record — 48 blocks, 16 files, 2026-08-24

Line ranges are **pre-removal** (`git show 15c84de5:<path>` reproduces them). Every removal is a
whole top-level YAML key, the unit the gate measures. Nothing was reworded, repointed, or
partially trimmed; surviving keys were verified byte-equal at the parse against the
`.backups/…20260824-233259` copies.

  | File (`deliverables/ai/P2/hardware/`) | n | Blocks removed (pre-removal line range) |
  |---|---|---|
  | `addon-goertzel-touch.yaml` | 1 | `specifications` (74-87) |
  | `addon-hd-audio.yaml` | 4 | `description` (19-25) · `set_contents` (26-30) · `dac_board` (79-120) · `use_cases` (128-135) |
  | `addon-hyperram-hyperflash.yaml` | 2 | `specifications` (73-86) · `configuration` (87-100) |
  | `addon-motor-driver.yaml` | 6 | `signal_map` (45-62) · `power_signals` (63-68) · `pwm_control` (69-81) · `current_sense` (82-86) · `specifications` (87-110) · `protection` (111-116) |
  | `addon-rtc.yaml` | 3 | `description` (18-24) · `power_signals` (52-55) · `specifications` (97-113) |
  | `addon-serial-device.yaml` | 2 | `description` (16-23) · `signal_map` (36-69) |
  | `addon-serial-host.yaml` | 2 | `signal_map` (37-70) · `usb_host_capabilities` (93-111) |
  | `addon-wx-wifi.yaml` | 3 | `part_variants` (3-5) · `pin_descriptions` (78-91) · `specifications` (97-108) |
  | `edge-32mb-module.yaml` | 5 | `specifications` (44-255) · `pin_mapping` (256-405) · `boot_modes` (406-444) · `limitations` (665-675) · `development_workflow` (676-686) |
  | `edge-breadboard-carrier.yaml` | 3 | `specifications` (25-46) · `specialized_features` (73-92) · `power_specifications` (209-225) |
  | `edge-mini-breakout.yaml` | 3 | `specifications` (24-43) · `connectivity` (52-68) · `power_management` (184-190) |
  | `edge-standard-breakout.yaml` | 3 | `specifications` (24-42) · `connectivity` (50-66) · `power_management` (165-170) |
  | `edge-standard-module.yaml` | 3 | `specifications` (43-183) · `pin_mapping` (184-315) · `boot_modes` (316-354) |
  | `hub75_adapter.yaml` | 4 | `description` (13-17) · `specifications` (49-66) · `software_features` (135-185) · `notes` (212-219) |
  | `p2-eval-board.yaml` | 1 | `specifications` (24-56) |
  | `programming-prop-plug.yaml` | 3 | `description` (21-30) · `reset_option` (45-52) · `specifications` (53-64) |

**Findings that name content in this record:** F-328(b) (`p2-eval-board.yaml specifications` —
see that entry for the four items removed and the six that survive) · F-251 and F-252 (the Edge
module LED facts — both annotated in place with their new addresses). **The two heaviest losses
for «#307» to price:** `edge-32mb-module.yaml` 744→321 lines and `edge-standard-module.yaml`
582→270, because in both the entire `pin_mapping` went. Board-level pin maps **pass** the
actionability test (they change which pin numbers appear in generated code), so these are
high-priority repopulation, source-first from the Edge module guides.

- **F-334 — `audit-yaml-claim-sourcing.py` treats a board REVISION (`Rev B` / `Rev C`) and a
  POWER `source:` as citations, which silences the gate on 11 quantitative blocks that are as
  uncited as the 48 just removed.** — `DONE` (verified 2026-10-05 «#386»: detector repaired at HEAD, the 11 blocks resolved in v1.23.3) — the gate's `INLINE_CITE_RE` includes `rev\s*[BC]\b`, which
  is a reasonable citation token in `Silicon Doc Rev C` prose and a **false positive** in a
  hardware file, where `Rev B` is the board's own identity: `board_revision: "Rev B (Guide
  v2.0)"`, or plain description text *"Goertzel experimenter board (Rev B) with pads…"*.
  Separately, `CITE_RE` matches any `source:` key — including
  `hub75_adapter.yaml` `source: P2 development board 5V supply` and
  `source: External 5V power supply (required)`, where "source" means a **power** source.

  **Both fire in the citation half only**, so the effect is a **false negative**: one such token
  anywhere in a top-level block marks the whole block cited and the gate never inspects it.
  **Measured, whole-KB, 2026-08-24 (after the purge):**

  | File | Block | qty | silenced by |
  |---|---|---|---|
  | `hardware/addon-hyperram-hyperflash.yaml` | `host_note` | 1 | `Rev B` |
  | `hardware/addon-serial-device.yaml` | `specifications` | 1 | `Rev B` |
  | `hardware/addon-serial-device.yaml` | `rev_b_5v_note` | 2 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `description` | 4 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `specifications` | 5 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `power_requirements` | 6 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `development_workflow` | 1 | `Rev B` |
  | `hardware/addon-serial-host.yaml` | `limitations` | 3 | `Rev B` |
  | `hardware/edge-standard-module.yaml` | `revision_history` | 6 | `Rev B`, `Rev C` |
  | `hardware/hub75_adapter.yaml` | `power_requirements` | 12 | the two power-`source:` keys |
  | `language/spin2/methods/getct.yaml` | `description` | 1 | `Rev B` |

  **Why «#294» did not act on it.** Three reasons, in order. (1) Its authority to touch the
  detector was bounded to a **proven false positive** — a block wrongly *flagged*; this is the
  opposite direction. (2) `hardware/addon-serial-host.yaml` alone would gain 5 blocks, and the
  purge's own success criterion is `hardware/` = 0, so acting would have made the task's gate
  unreadable mid-flight. (3) One of the 11 — `language/spin2/methods/getct.yaml` — is **outside
  `hardware/`**, in a tree «#293» already closed, which «#294» was forbidden to touch; fixing
  the detector without it would have left Tier 1 at 1 and the tool at exit 1, i.e. a green task
  reported red for a reason unrelated to its work.

  **Repaired 2026-08-24.** Both patterns were tightened around one principle: **a citation names
  a DOCUMENT, or an empirical record — not a hardware revision, and not a physical supply.**

  - `rev\s*[BC]\b` is **gone** from `INLINE_CITE_RE`. It was not replaced with an
    adjacent-to-a-document-word variant because the corpus says that is unnecessary: **every**
    real citation in all 1129 files that carries a revision also names the document it is a
    revision *of* — `"P2 Silicon Doc v35 (KNOWN BUGS, Rev C) -- verbatim"`, `"Propeller 2
    Documentation v35 - Rev B/C Silicon"`, `"#64000 … Eval Board Rev C Guide v2.0"` — so each is
    still recognised by `silicon doc`, `p2 documentation`, or the `guide` value token. Measured
    before deciding: **0 blocks and 0 files** in the KB rested on the revision token as their
    only *genuine* citation signal.
  - `CITE_RE` is replaced by `CITE_KEY_RE` + **`CITE_VALUE_RE`**: the key name is no longer the
    test, the **value** is. A key that introduces structure (`sources:` + a list, `source: |` +
    a block scalar) is tested against its nested body, which is where the document is named.
    The accept-vocabulary is drawn from the 88 corpus values that *are* citations, so every real
    short form still passes (`"P2 Datasheet"`, `"Silicon Doc v35"`, `"Hardware Manual
    2022-11-01"`, `"PNut v47 release notes"`, `flash_loader.spin2`, `parallax-quick-bytes`,
    `complete-builtin-symbols.md`, `…/P2-EMPIRICAL-FINDINGS.md EF-053`). Of the **312** cite-key
    lines in the corpus, **224 name no document at all** — power supplies, pattern-category tags
    (`source: motor_control`), event-name lists (`sources: ["CT-passed-CT1", …]`), compiler
    search paths (`source: "-I directories"`).

  **Negative control: 12 → 25 cases, 0 FAIL** (`--negative-control`, which now prints the count
  and its split: quantity 5 · region 7 · citation 13). The thirteen citation cases each state a
  real quantity, so none of them can pass by having nothing to find — what they measure is purely
  whether the block is judged *cited*. Six of them **FAIL against the shipped detector and PASS
  against the repaired one** (board revision · silicon revision in prose · `source:` naming a
  power supply · `source:` naming a host rail · `source:` naming a pattern category · `sources:`
  listing event names); the other seven prove a real citation is still recognised in each of its
  corpus spellings — short form, versioned, a genuine citation that *also* carries `Rev C`,
  `derived_from:` with a file+line, `verified_against:` with an EF number, a `sources:` list, and
  bare inline attribution with no cite key at all. No MUST-NOT-FIRE case regressed.

  **The instrument, before and after.** The repaired detector reported **4 Tier 1 / exit 1**, and
  the union of Tier 1 + Tier 2 went **84 → 95**: exactly the 11 blocks below became visible and
  **nothing disappeared**. After the removals it reads **0 Tier 1 / exit 0** with Tier 2 back at
  exactly **84** — which is the cross-check this entry asked for, satisfied: no file silently
  changed tier, the eleven were removed rather than demoted. The zero is now a *true* zero: the
  same tool failed, on this tree, an hour earlier.

### Removal record — 11 blocks, 6 files, 2026-08-24 (the same purge, finishing)

Line ranges are **pre-removal**. Every removal is a whole top-level YAML key; surviving keys were
verified parse-identical to the `.backups/…20260824-235306` copies (`yaml.safe_load` diff: only
the named keys gone, no key added, no surviving value changed). No `related:`/`see_also:` line
falls inside any removal range, and no file anywhere deep-links one of these keys — both checked
programmatically before deleting.

  | File | Block (pre-removal range) | What went | Repopulates under |
  |---|---|---|---|
  | `hardware/addon-hyperram-hyperflash.yaml` | `host_note` (26-30) | 5V-socket / ACC-HDR jumper guidance | «#307» |
  | `hardware/addon-serial-device.yaml` | `specifications` (41-59) | 3.3V, 3.2mm, 5mm, 9.5mm | «#307» |
  | `hardware/addon-serial-device.yaml` | `rev_b_5v_note` (60-65) | Rev-B 5V shunt note | «#307» |
  | `hardware/addon-serial-host.yaml` | `description` (16-23) | 500 mA load-switch limit | «#307» |
  | `hardware/addon-serial-host.yaml` | `specifications` (37-58) | 500mA/1A/~2mA + physical dims | «#307» |
  | `hardware/addon-serial-host.yaml` | `power_requirements` (59-71) | the same current budget again | «#307» |
  | `hardware/addon-serial-host.yaml` | `development_workflow` (102-110) | 5V-availability checklist | «#307» |
  | `hardware/addon-serial-host.yaml` | `limitations` (120-126) | 500mA per-port limit | «#307» |
  | `hardware/edge-standard-module.yaml` | `revision_history` (204-235) | VIN 5.5V→16V, 2A→3A, 2.5MHz→750kHz | «#307» |
  | `hardware/hub75_adapter.yaml` | `power_requirements` (127-139) | 35mA @ 35MHz + the four panel budgets | «#307» |
  | `language/spin2/methods/getct.yaml` | `description` (8-15) | "~21 seconds at 200MHz" wrap figure | «#299» |

**Sources to repopulate from:** the `#64006 Series` and `#64004-ES` product guides (already cited
in each file's own `documentation.primary`), the P2-EC Edge Module guide's revision table, the
HUB75 driver study, and — for `getct` — the Spin2 language reference. **`getct.yaml` is the one
outside `hardware/`**: it is «#299»'s, and its wrap figure is *derived* (2³² ÷ 200 MHz), so it
needs a source that states it or a rewrite that does not compute.

  **Three of the dispatched candidates were NOT violations** and were left alone — measured, not
  assumed: `architecture/smart_pin_patterns.yaml` `timing_patterns` and `language/pasm2/waitx.yaml`
  `examples` state **zero** quantities once code regions are stripped (their numbers are all
  inside example bodies), and `architecture/boot-rom/spi-flash-boot.yaml`
  `phase_2_post_load_state` is **correctly** silenced: its `cog_clock.source:` attributes the
  20-30 MHz figure to `architecture/clock_system.yaml`, which does carry it
  (`frequency: "20-30 MHz across process/voltage/temperature"`, line 35). So no `architecture/`
  block was in scope after all — the finding is 11, in two trees, not three.

  **REPOPULATION EXECUTED 2026-08-25 («#307» and «#299»).** All 48 + 11 blocks are dispositioned
  and disposed of: in `hardware/`, 34 returned cited and 24 are held in the ingestion tree
  (**F-353**, with the per-block table and the seven content-level holes in **F-354**); outside it,
  `language/spin2/methods/getct.yaml description` was «#299»'s and is recorded with F-347/F-352.
  Nothing on either record is still owed.

  Status: `DONE` (2026-10-05: released and verified in v1.23.3) — the detector repair, all 59 removals and the whole repopulation
  are applied and gate-verified; only the YAML release is owed. See **F-335**, which this repair
  exposed.

---

## `audit-yaml-claim-sourcing.py` does not know the `documentation: primary:` citation spelling, so a whole class of board file is mis-tiered into the advisory lane (2026-08-24, F-334 repair) — F-335

> 🔴 **(e) A DEFERRAL READS AS A CITATION — ADDED BY THE ARBITER 2026-08-25 (during «#298»), AND IT
> IS THE ONE THAT ACTUALLY HURT SOMEBODY.** `CITE_KEY_RE`/`INLINE_CITE_RE` match the bare word
> *datasheet* anywhere in a block. `language/pasm2/concepts/basic-io.yaml` and its Spin2 twin each
> carried:
>
> ```yaml
>   max_current_per_pin: "150mA"
>   max_current_total: "Check datasheet for package limits"
> ```
>
> The second line is a **deferral — an instruction to go look elsewhere** — and it scored the whole
> block as cited. So the block sailed through «#293» *and* «#294» while asserting
> **`max_current_per_pin: "150mA"` against the datasheet's stated `Max. allowable current per I/O
> pin ±30 mA`** (`sources/p2-datasheet/p2-datasheet-text.txt:2163`). **Five times the absolute
> maximum, in the exact number a reader uses to size an LED series resistor.** The same block
> shipped `VOL_max: "0.4V"` / `VOH_min: "2.4V"` — 5 V-TTL thresholds the P2 datasheet does not
> contain (its real figures are millivolt drops: Vol 15 mV sinking 1 mA, `:2172-2178`).
>
> **This is the third member of the same family**, after (F-334) a board revision `Rev B`/`Rev C`
> and a power `source:`. The pattern is now explicit and should drive the repair rather than three
> more one-off patches: **the citation side matches on the PRESENCE OF A TOKEN, never on whether
> the sentence actually attributes the block to a document.** *"Check datasheet for…"*, *"see the
> datasheet"*, *"per the manual"* are pointers away from the block; a citation points *at* a source
> for the claim being made. Fixing (a)-(e) individually will keep finding a sixth.
>
> Removed under «#298» (both copies, pure deletion) and filed as **F-348**. The correct facts
> already ship, cited, in `architecture/io_pin_timing.yaml absolute_maximum_ratings`.

> 🔴 **TWO FURTHER DEFECT CLASSES, ADDED BY THE ARBITER'S RE-RUN 2026-08-25. «#305» MUST DISPOSE OF
> ALL OF THEM BEFORE ARMING — THEY ARE NOT INDEPENDENT, AND ONE PAIR CANCELS.**
>
> **(c) An escaped single-line string hides example code from `strip_code_regions`.** The stripper
> recognises **block scalars** (`|`). `language/pasm2/waitx.yaml`'s `examples:` stores its PASM2 as a
> double-quoted single-line string with literal `\n` escapes, so the stripper never sees a code
> region and the gate reads **4 quantities** out of PASM2 *comments* — `' For 1kHz PWM at 200MHz
> clock:` and `' 100us @ 200MHz`. Those are chosen demo parameters, which the tool's own header says
> it exists to skip. Measured: 4 quantities raw, **4 surviving the strip** (compare
> `architecture/smart_pin_patterns.yaml timing_patterns`, where 1 raw → **0** stripped, correctly).
>
> **(d) A slug still passes as a citation, so (c) is currently masked.** `waitx.yaml examples` carries
> `source: hub75_driver` · `source: inline_pasm2_pattern` · `source: bit_bang_spi` ·
> `source: software_pwm` · `source: input_debounce` — **pattern-category tags, not documents**. These
> are the same shape as `source: motor_control`, which F-334's repair added as a control and rejects;
> the filename/slug accept-branch lets these through. So the block is not flagged.
>
> 🔴 **THE POINT IS NOT EITHER BUG — IT IS THAT THEY CANCEL.** A quantity-side false positive is
> being hidden by a citation-side false negative, and the block reads clean for two wrong reasons.
> Fix either one alone and the gate starts failing on a block that was never a real violation. That
> is why (a)-(d) must be dispositioned **together**, in the order this finding sets out, and why the
> current `PASS  no Tier 1 violations` — while true for the two paths F-334 repaired — is **not yet a
> safe thing to arm a release gate on.**
>
> **What IS settled and should not be re-litigated:** F-334's two repairs are proven. The arbiter ran
> the five false-negative cases against the pre-repair detector loaded side-by-side: all five scored
> *cited* before and *uncited* after, while three real citation forms — short form, an EF record, and
> one that itself carries `Rev C` — still score cited. 25 controls, 0 FAIL.

> **Origin.** Surfaced while repairing F-334. Removing the `Rev B` token from `INLINE_CITE_RE`
> dropped `addon-serial-host.yaml` and `addon-serial-device.yaml` out of "citing" entirely — and
> that is **wrong**, because both files cite perfectly well, three lines from the bottom. The
> detector simply does not recognise the spelling. Filed rather than fixed: the fix is measured
> below and it is **not safe to arm as-is**, for a reason that is itself a finding.

- **F-335 — the eval add-on board files cite as `documentation:` → `primary: "<doc>"`, a spelling
  no citation key in the tool matches, so files that DO know the citing convention are scored as
  wholly-uncited and their F-327-shaped blocks land in Tier 2 (advisory) instead of Tier 1
  (blocking).** — `RESOLVED` — `addon-serial-host.yaml:171-172` is the type case:

  ```yaml
  documentation:
    primary: "P2 Eval Add-on Boards (#64006 Series) v2.0"
  ```

  That is a citation by any reading, and it is the ONLY one in the file. `CITE_KEY_RE` knows
  `source`/`sources`/`reference`/`references`/`authority`/`derived_from`/`verified_against` and
  not `documentation`, so `file_cites` is false, so **the file's own other sections cannot act as
  the control** and Tier 1 — the tier the release gate «#305» will arm on — never applies to it.
  Until F-334 was repaired the effect was invisible: the `Rev B` token was propping these files
  up in Tier 1 by accident, for entirely the wrong reason.

  **Measured, whole-KB, 2026-08-24.** Adding `documentation` to the key vocabulary (value-tested
  exactly like the others) moves **Tier 1 from 4 to 34 and Tier 2 from 91 to 61** — thirty
  blocks across eight board files that have sat in the advisory lane throughout this sprint:
  `addon-av-breakout` (3), `addon-control-board` (6), `addon-digital-video-out` (4),
  `addon-led-matrix` (3), `addon-microsd` (1), `addon-mini-prototyping` (5), `addon-wx-adapter`
  (1), plus the two serial boards already purged under F-334.

  **Why it was NOT applied in the same pass, and this is the real content of the finding.**
  Reading those thirty blocks shows most of them are not claims at all — they are the **quantity**
  half over-firing, which is a different defect in the other half of the same tool:

  | Kind | Example | Why it is not a measurement |
  |---|---|---|
  | part number | `addon-control-board.yaml:2` `part_number: "64006A"` | `QTY_RE` reads `64006A` as **64006 amperes**. Same string flagged again in `aliases` and in `availability.part_lookup`. |
  | rail NAME | `supply_voltage: "3.3V from host"`, `label: "5V"`, `voltage: "3.3V (VIO)"` | `3.3V`/`5V` here name the rail, the way `GND` names a net. Present in nearly every board file. |
  | connector NAME | `addon-digital-video-out.yaml:83` `name: "5V (5V-arrow)"` | a silkscreen label. |

  Arming the key widening without repairing `QTY_RE` first would therefore force the deletion of
  a board's `part_number` and `aliases` blocks to reach zero — **content destruction to satisfy
  an instrument defect**, which is the exact inversion of what this sprint is for.

  **The scope this finding must own, because it is wider than it looks.** The rail-name over-fire
  is not confined to the thirty: it is also why three of F-334's eleven removals went
  (`addon-hyperram-hyperflash.host_note` on a "5V socket", `addon-serial-host.development_workflow`
  and `addon-serial-device.rev_b_5v_note`, all on rail names with no measurement in them), and it
  reaches back into the 48 (`addon-rtc.power_signals` was removed for
  `VIO3V3: "3.3V supply; powers the RTC…"`). Those removals were made **deliberately, for
  consistency** with the 48 already accepted — but they are the same shape, and the decision
  about rail names should be made **once, globally**, not differently at each task boundary.

  **What is owed, in this order.** (1) Decide the rail-name question: is `3.3V` naming a supply
  rail a claim that must be sourced, or is it structure like a pin number? Whichever way it goes,
  it applies to the 48, to F-334's eleven, and to the Tier 2 population alike. (2) Fix `QTY_RE`
  so a part number (`64006A`) is not a current — that one has no second side, it is simply wrong.
  (3) Only then add `documentation` to `CITE_KEY_RE`, with negative-control cases for the
  spelling, and re-run. **«#305» should not arm the release gate on Tier 1 until (3) lands** —
  not because the gate is wrong today, but because eight board files are currently exempt from it
  for a reason nobody chose.

  **RESOLVED 2026-08-25 by «#305», (a)–(e) together, in the order this finding set out.**

  1. **The rail-name question, decided: a voltage designator in a hardware file IS a claim.**
     It asserts a fact about a physical board — what is printed on it, what it connects to —
     and a reader wires hardware from it. The alternative disarms the gate on `vdd_max` /
     `VOH_min`, which is the exact F-348 shape that shipped a figure five times the
     datasheet's absolute maximum. It is also the reading already applied to the 48 and to
     F-334's eleven, so nothing already accepted has to be re-litigated. Recorded as two
     standing negative-control cases (`label: "5V"` and `vdd_max: "3.6V"` MUST STILL FIRE)
     so the decision cannot flip in silence.
  2. **(b) / F-351 — `QTY_RE` repaired.** A bare `A` preceded by four or more integer digits
     is a part number or a standard designator, not a current; `U+XXXX` is masked alongside
     `%binary` and `$hex`; the number accepts thousands separators. Measured: **9 blocks**
     that stated no quantity at all left the advisory lane (`addon-control-board` ×3,
     `hardware-compatibility-matrix` ×2, `p2-hardware-selection-guide` ×2,
     `p1_rom_font_character_set`, `obex/objects/4070`). F-351 listed ten; the tenth
     (`p2-hardware-feature-comparison` `selection_criteria`) had already been drained by an
     earlier task, so it was not in today's population.
  3. **(c) and (d) landed in the same edit, because they cancel.** (c): a code example stored
     as a **double-quoted scalar with literal `\n` escapes** was invisible to the region
     stripper, which now judges a quoted scalar by the same `CODE_MARKER_RE` test it applies
     to a `|` block — plus a guard requiring a real `\n` escape, without which the rule
     blanked `p2an003-dac-analog-signal-generation.yaml:118`, a `source_statement:` holding a
     quoted SENTENCE that opens with an apostrophe. Blanking prose is the "turn the gate off
     by stealth" failure, reproduced in the other value shape. (d): a lowercase snake_case
     slug is a pattern-category tag, not a document — vetoed by shape rather than by token.
  4. **(e) — a deferral is not a citation.** Vetoed as a PHRASE (`check|see|refer to|consult
     |look up|read|review` + a document noun) rather than anchored at the start of the value,
     because *"Sinks 150mA per pin; see the datasheet for package limits"* reads the same way
     and an anchor would miss it. A deferral that NAMES the document (`"See P2 Silicon Doc
     v35"`) is an attribution and still counts. Applied to the inline path per LINE, which is
     the half that actually fired.
  5. **(a) — `documentation` added to `CITE_KEY_RE` last, as this finding required.**

  ⚠️ **TWO CORRECTIONS TO THIS FINDING'S OWN TEXT, measured against the tree 2026-08-25.**
  - (d) attributes the leak to "the filename/slug accept-branch". It is not that: of the five
    slugs on `waitx.yaml`, **only `inline_pasm2_pattern` passed**, and it passed because the
    bare `pasm2` token in `CITE_VALUE_RE` matches INSIDE the identifier. The corpus carried
    exactly two such values (the other is `lock_validation` at `lockrel.yaml:70`, via
    `validat`). `hub75_driver`, `bit_bang_spi`, `software_pwm` and `input_debounce` never
    passed at all.
  - (c) states `waitx.yaml` reads "4 quantities raw, 4 surviving the strip". **That does not
    reproduce**: with the pre-repair detector loaded side by side, the file yields **0**
    quantities raw and 0 after the strip. The PASM2 comments carrying `1kHz` / `200MHz` /
    `100us` sit after `#pwm_loop` on the same physical line, and `strip_yaml_comment` reads
    that `#` as a YAML comment and drops the rest. So the block read clean for a THIRD wrong
    reason, not two. The underlying defect in (c) is real and is fixed; its stated symptom
    was masked by an unrelated accident.

  **Measured effect of (a)–(e) together, instrument only, against the committed tree:**
  Tier 1 **0 → 20**, Tier 2 **78 → 49**. The 29 that left Tier 2 are the 20 re-tiered by (a)
  plus the 9 artifacts removed by (b). The 20 were then drained source-first (see F-335's
  disposition in the sprint plan §10): 17 blocks gained a per-block `source:`, three unsourced
  inferences were removed. Final state: **0 Tier 1, 49 Tier 2**, and both gates armed.

  Status: `RESOLVED`

---

## The P2 Hardware Manual states a VCO range the datasheet and the Silicon Doc both contradict (2026-08-24, `p2-datasheet` re-ingestion) — F-330

> **Origin.** The `p2-datasheet` table recovery (plan §8) cross-checked every recovered table
> against the DOCX-derived `p2-hardware-manual` tables. Nine of ten comparisons agreed cell for
> cell. This is the one that did not. **Nothing is fixed in this filing** — the ingestion head
> produces source data; any YAML consequence belongs to the purge/repopulate tasks.

- **F-330 — Two Parallax documents of the SAME edition date (2022/11/01) give different
  recommended VCO ranges in the same `%MMMMMMMMMM` table note, and the P2 Hardware Manual is
  the outlier.** — `RESOLVED — relocated to the errata register as E-003; the guard this entry existed to be is now served there`

  > **RELOCATED + CLOSED 2026-08-25 («#302»), pointer left behind, never a silent move.**
  >
  > By the three-register test — *if Parallax fixed the Hardware Manual's Table 10 note tomorrow,
  > would this disappear?* — **yes**, so this is an **erratum**, not a KB correction. This entry
  > says so itself: *"Treat the Hardware Manual's Table 10 note as source errata."* It now lives at
  > **`engineering/ingestion/SOURCE-ERRATA.md` → `E-003` (`RESOLVED`)**, *"the VCO note contradicts
  > the manual's own PLL Example"*, which carries all six rows of evidence (including the decisive
  > self-contradiction at `:574` vs `:603`), the same 100–200 MHz verdict, the same 350 MHz =
  > VCO/1-overclock-ceiling disambiguation, and the Spin2 v51 solver bound as the third legitimate
  > context for the number. That register was created 2026-08-25, after this was filed.
  >
  > **The guard function is preserved, which is the only thing this entry was for.** It carried
  > **no owed KB work** — *"KB impact: NONE"*, `clock_system.yaml` already draws the line correctly
  > — and existed solely *"to prevent a future agent from 'fixing' that 200 to 350 on the Hardware
  > Manual's authority."* `E-003` performs exactly that guard, in the register an ingestion agent
  > actually consults before trusting a source.
  >
  > ⚠️ **THIS ENTRY'S OWN DESCRIPTION OF THE KB IS STALE, AND WAS CORRECTED ONLY BECAUSE THE FILE WAS
  > RE-READ.** It states the KB carries `vco_range: "99 MHz to 201 MHz"`, `max_overclock: "350 MHz"`
  > and `absolute_max: "350 MHz (may be unstable)"`. **None of those three keys exists on disk today**
  > — `clock_system.yaml` was rewritten during this sprint's uncited-block purge (F-347's removal
  > record lists `configuration_constants`, `pll_system`, `clock_specifications` and `anti_patterns`
  > among the blocks removed from this very file). Repeating the entry's own text as verification
  > would have published a false confirmation of a file nobody had opened.
  >
  > **What is actually there, measured 2026-08-25 — and it is STRONGER than what this entry
  > described:**
  > - `:104` `vco_range:` now quotes the source verbatim — *"The PLL's VCO is designed to run between
  >   100 MHz and 200 MHz and should be kept within that range."*
  > - `:129` `overclocking:` and `:270` `overclock_ceiling:` carry the 350 MHz VCO/1 figure **with its
  >   Silicon Doc locator**, kept separate from the recommendation.
  > - `:209` states the third context explicitly — *"350 MHz is the absolute VCO/1 overclock ceiling,
  >   NOT the XI-input limit."*
  > - `:130` `cross_source_conflict:` **names F-330 by ID inside the shipped YAML** and states the
  >   resolution. **The guard is now in the artifact itself**, which is a better place for it than any
  >   register — it reaches the agent at the moment of use.
  >
  > **Consequence for whoever maintains that file:** `:130` points at `F-330`. That pointer still
  > resolves — this entry stays in place — but the evidence now lives at `E-003`, so a future
  > citation refresh should carry the reader on to the errata register.

  **The identical sentence, two numbers:**

  | Source | Sentence, verbatim |
  |---|---|
  | **P2 Datasheet**, p.18 (`sources/p2-datasheet/p2-datasheet-text.txt:793`) | "The VCO frequency should be kept within 100 MHz to **200 MHz**." |
  | **P2 Datasheet**, p.19 PLL Example (`:850`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |
  | **Propeller 2 Documentation v35 Rev B/C** (`sources/silicon-doc/part3-interrupts.txt:545` area) | "The VCO frequency should be kept within 100 MHz to **200 MHz**." |
  | **Propeller 2 Documentation v35 Rev B/C** (`sources/silicon-doc/p2-documentation.txt:6233`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |
  | **P2 Hardware Manual**, Table 10 (`sources/p2-hardware-manual/complete-tables-reference.md:107`) | "The VCO frequency should be kept within 100 MHz to **350 MHz**." |

  **Verified at the source, not only in the extract.** The manual's `350` was read directly out
  of `word/document.xml` of
  `sources/p2-hardware-manual/Propeller 2 Hardware Manual - 20221101.docx`, so it is the
  document's own text and not a DOCX-walk artifact.

  🔴 **DECISIVE, AND ADDED BY THE ARBITER'S RE-RUN: THE HARDWARE MANUAL CONTRADICTS ITSELF.**
  The filing above frames this as three documents against one, which would leave it a question
  of relative document authority. It is not — the manual states **both** numbers, twelve
  paragraphs apart, in the same voice:

  | Same document, two numbers | Sentence, verbatim |
  |---|---|
  | **Table 10 note** (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:574`) | "The VCO frequency should be kept within 100 MHz to **350 MHz**." |
  | **Its own PLL prose** (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:603`) | "The PLL's VCO is designed to run between 100 MHz and **200 MHz** and should be kept within that range." |

  Line 603 is verbatim identical to the datasheet's `:850` and the Silicon Doc's `:6233`. So the
  manual's own body text agrees with the other two sources and disagrees with its own table note.
  That settles it without weighing authority at all: **the Table 10 note is a localized
  substitution error inside an otherwise-correct document**, which is exactly what "source
  errata" means and is why G-016/G-017-class upstream reporting is the right disposition rather
  than any re-ranking of the manual as a source.

  **Where 350 legitimately belongs — the vocabulary key.** 350 MHz is a real P2 number, but it
  is the **overclock ceiling**, not the recommended range. The Silicon Doc says so in the very
  next row of the very same table, against `%PPPP`: *"For fastest overclocking, the PLL can be
  pushed to 350 MHz using the 'VCO / 1' mode (%PPPP = 15)."* Spin2 v51's clock-setup symbols
  carry the same bound as a compiler constraint
  (`sources/spin2-v51/complete-clock-setup-symbols.md:276`, "MUST be between 100 MHz and
  350 MHz"). The Hardware Manual appears to have substituted the overclock ceiling into the
  *recommendation* sentence, which is why this is a defect rather than two documents describing
  two different things: both sentences make the same claim ("should be kept within") with
  different numbers, and they cannot both be the recommended range.

  **Resolution for downstream use.** Recommended/design VCO range = **100–200 MHz** (datasheet
  and Silicon Doc, two independent sources, each stating it twice). **350 MHz** = the VCO/1
  overclock ceiling and the Spin2 solver's upper bound. Treat the Hardware Manual's Table 10
  note as **source errata**; do not cite it to raise a recommended-range figure.

  **KB impact: NONE — recorded so it is not "corrected" later.**
  `deliverables/ai/P2/architecture/clock_system.yaml` already draws the line correctly
  (`vco_range: "99 MHz to 201 MHz"`, `max_overclock: "350 MHz"`,
  `absolute_max: "350 MHz (may be unstable)"`, and an explicit note distinguishing the two).
  **This finding exists to prevent a future agent from "fixing" that 200 to 350 on the Hardware
  Manual's authority.** No YAML edit is owed.

---


### F-331 — `pasm2/wrpin.yaml` mislabels three of the six WRPIN D-operand fields; two agreeing Parallax sources and the YAML's own sibling file all say otherwise — `RESOLVED — validated on the served KB 2026-09-11`

> **APPLIED 2026-08-25 by «#295» phase 2 — REPOINTED, not re-worded.** The `d_operand_format.fields:`
> map no longer restates the six fields at all. It now carries three pointers:
> `reference:` → `architecture/smart_pins.yaml (configuration_format.fields)`, which already has all
> six right; `m_sub_fields:` → the new `architecture/pin-drive-configuration.yaml`; and
> `input_selectors:` → the block below it, which was correct and is untouched.
>
> **Why repoint rather than re-word.** The three sources word `M` two ways ("pin mode" /
> "low-level pin control"), so re-wording means picking one; pointing at the single home means
> picking none, and it removes the third copy that made the drift possible. Deletion is the
> correction.
>
> **Evidence is triple-sourced, one better than this finding records** — the Silicon Doc agrees
> with the datasheet and the Hardware Manual: `part4-smart-pins.txt:55` reads *"%M..M: low-level pin
> control"* and `:63` reads *"%TT: pin DIR/OUT control (default = %00)"*, with `%SSSSS` at `:107`.
> None of the three says "DAC/output mode", "DAC/output value", or "+ smart-pin mode".
> (This finding's own body cites `:59` for the `%TT` line; measured, it is `:63`.)
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit.

**Location:** `deliverables/ai/P2/language/pasm2/wrpin.yaml:34-36` (the `d_operand_format.fields:` map).

**What the two sources say, verbatim and identically** — P2 Datasheet @ 2022/11/01 p.23
(`engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1054-1059`) and P2 Hardware
Manual @ 2022/11/01 (`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:786-791`):
`A` = PIN input selector · `B` = ADJ input selector · `F` = PIN and ADJ input logic/filtering ·
**`M` = pin mode** · **`T` = pin DIR/OUT control (default = %00)** · **`S` = smart mode**.

| Field | YAML says | Both sources say |
|---|---|---|
| `M` | "13-bit low-level pin control **+ smart-pin mode**" | **pin mode** — the smart mode is `S`, a different field |
| `TT` | "**DAC/output mode**" | **pin DIR/OUT control** (default `%00`) |
| `SSSSS` | "**DAC/output value or pin-output bit selection**" | **smart mode** (the 32 `%SSSSS` modes) |

**The file's own sibling already has all six right** —
`deliverables/ai/P2/language/spin2/methods/wrpin.yaml:28-35` reads "Bits 20:8 (M): Low-level pin
control", "Bits 7:6 (TT): Pin DIR/OUT control", "Bits 5:1 (SSSSS): Smart pin mode selector
(5 bits, 32 modes)". So the two WRPIN entries in the shipped KB describe the same 32-bit word
differently, and an agent that reads the PASM2 one is told `SSSSS` selects a DAC value.

**Not the whole file** — the same file's `input_selectors:` block (`:37-56`) is **correct** and
matches both sources including the two rows Titus rev5 had swapped (`x101` = relative −3,
`x111` = relative −1). Only the three `fields:` descriptions are wrong; do not purge the block.

**Proposed correction:** replace the three descriptions with the sources' own words (`M` = pin
mode; `TT` = pin DIR/OUT control, default `%00`; `SSSSS` = smart mode), keeping the existing
bit-range annotations from the Spin2 sibling. **Closes the last open half of `KNOWLEDGE-GAPS`
G-008.**


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. same structural repair as F-326 — the three mislabelled fields were not corrected in place, the restatement that allowed them to drift was removed and replaced by a pointer to the single home. The file says so itself at the redirect.
### F-338 — `P_LEVEL_B` and `P_SCHMITT_B` do not exist: two fabricated constant names stood in four `related_symbols:` lists, and nothing in the toolchain could see them — `DONE` (verified 2026-10-05 «#386»: names gone in v1.23.3; F-340's nested check at HEAD)

> **Evidence, three ways.** Neither name is in the Spin2 v55 symbol table (114 rows, 116 distinct
> names, `spin2-v55-text.txt:1419-1562`). Neither is on `audit-constant-fidelity.py`'s 120-name
> truth side. `pnut-ts` v1.55.3 **rejects both** as `PUB main()` / `wrpin(0, NAME)`, while
> accepting all seven of the legal siblings they are near-misses on — `P_LEVEL_A`,
> `P_LEVEL_A_FBN`, `P_LEVEL_B_FBP`, `P_LEVEL_B_FBN`, `P_SCHMITT_A`, `P_SCHMITT_A_FB`,
> `P_SCHMITT_B_FB`. That seven-accept control is what proves the harness discriminates rather than
> rejecting everything.
>
> ⚠️ **A naive grep says both names EXIST.** They are substrings of the `_FB` / `_FBP` / `_FBN`
> forms, so `grep P_LEVEL_B` returns hits for `P_LEVEL_B_FBP` and `P_LEVEL_B_FBN`. Match on word
> boundaries — `grep -P '\bP_LEVEL_B\b(?!_)'` — or this reads as a false clear.
>
> **APPLIED 2026-08-25:** all four entries deleted from
> `language/spin2/symbols/spin2-builtin-symbols-complete.yaml`, **substituting nothing** (a
> substitution would be an inference about what the author meant). Whole-tree re-grep with word
> boundaries: **0 hits**.
>
> **Why this is `PARTIAL` and not closed: the class is still undetectable.** Nothing found these
> for years, and nothing would find the next one — see **F-340**. This entry stays open until that

> 🔴 **MEASURED BY THE ARBITER 2026-08-25 (during «#304») — THE EXPOSURE IS 24% OF ALL REFERENCE
> SITES, AND THE GATE'S GREEN IS NOT A STATEMENT ABOUT THEM.**
>
> `validate-crossref-keys.py` iterates a **fixed 15-name `CROSS_REF_FIELDS` dict** and tests
> `if field_name not in content` — `content` being the **top level** of each document (`:447-492`).
> So a reference field is checked only when it is a top-level key, and any reference nested below
> that is invisible. Counted across `deliverables/ai/P2/`:
>
> | | sites |
> |---|---|
> | reference-field occurrences the validator **sees** (top level) | **742** |
> | occurrences it **structurally cannot see** (nested) | **230** |
> | **coverage** | **76%** |
>
> Nested, by field: `related_symbols` **136** · `related` 57 · `see_also` 25 ·
> `related_instructions` 6 · `cross_references` 3 · `related_pasm` 2 · `combines_with` 1.
>
> **`related_symbols` alone is 136 unchecked sites, and that is exactly where the two fabricated
> names (`P_LEVEL_B`, `P_SCHMITT_B`) lived undetected.** They were not missed by bad luck; they
> were in a field the instrument does not read.
>
> ⚠️ **AND «#304» FOUND THE SECOND HALF OF THE SAME HOLE:** a field that is not in the dict at all
> is invisible even at top level. `knowledge_progression:` and `next_steps:` in
> `guides/*-getting-started.yaml` carried the citations that route every new agent into
> `concepts/basic-io.yaml` — **the validator could not have reported them wherever they pointed.**
> Its exit 0 was silence, not a verdict.
>
> **For «#305»: `3161 refs, 0 unresolved` must not be read, or reported at release, as
> "cross-references are clean."** It means *the 76% the instrument looks at resolve.* Either widen
> the traversal to nested occurrences and unknown reference-shaped fields, or state the scope
> wherever the number is quoted. **A gate whose green is narrower than its name is the defect this
> sprint exists to repair, one level up.**
> detection gap is dispositioned.

### F-339 — `audit-constant-fidelity.py`'s own docstring misstates the size and the shape of the blind spot it declares — `RESOLVED`

> **RESOLVED 2026-08-25 by «#305».** Both numbers re-measured against disk before the
> docstring was rewritten: the v55 table carries **116** distinct `P_` constants over **114**
> rows (two rows name a constant *and* its brevity alias), **ADDED = 0**, **RE-DESCRIBED =
> 20**. This finding's figures are confirmed exactly; the task body dispatched with «#305»
> repeated the wrong 100 and was corrected. 19 of the 20 move visibly once v55 is on the truth
> side; `P_OR_AB` is the twentieth and moves invisibly for the self-cancelling `strip_desc`
> reason this finding already documents — left alone, as instructed. `KNOWN LIMITATIONS`
> item 4 now records the closure and the measured cost instead of the estimate.

> **Location:** `engineering/tools/validation/audit-constant-fidelity.py`, `KNOWN LIMITATIONS`
> item 4 (around `:114`). For **«#305»**, which arms this gate; **do not fix it inside a task that
> is being measured by it.**
>
> | The docstring says | Measured 2026-08-25 |
> |---|---|
> | the v55 table "carries 100 distinct `P_` constants" | **116** (114 table rows; two rows carry a name *and* a brevity alias — `P_TRUE_OUTPUT`/`P_TRUE_OUT`, `P_INVERT_OUTPUT`/`P_INVERT_OUT`) |
> | the blind spot is "wherever v55 ADDED or RE-DESCRIBED a constant" | **ADDED is 0** — every one of the 116 is already on the truth side. **RE-DESCRIBED is 20**, and that is the entire exposure |
>
> **So the gap is not missing names, it is 20 superseded descriptions**, and framing it as
> add-or-redescribe hides which half matters. The 20, measured by loading the tool's own
> `harvest_source()` and diffing it against a hand parse of `spin2-v55-text.txt:1419-1562`:
> `P_ADC`, `P_ADC_EXT`, `P_ASYNC_RX`, `P_ASYNC_TX`, `P_COUNT_HIGHS`, `P_COUNT_RISES`,
> `P_INVERT_OUT`, `P_NCO_DUTY`, `P_NCO_FREQ`, `P_OR_AB`, `P_PULSE`, `P_PWM_SAWTOOTH`,
> `P_PWM_SMPS`, `P_PWM_TRIANGLE`, `P_QUADRATURE`, `P_REG_UP`, `P_REG_UP_DOWN`, `P_SYNC_RX`,
> `P_SYNC_TX`, `P_TRUE_OUT`. Four v51-only names are absent from v55 — `P_COMPARATOR`,
> `P_COMPARATOR_FB`, `P_FLOAT`, `P_PASS` — and the KB references and defines none of them.
>
> **The KB side is already at v55**, as of «#295» phase 2: all 116 records carry the v55 wording.
> Verified before adopting it that this moves nothing — 0 `QUANTITY` clashes and 0 `CONTRADICT`
> clashes across all 116 when the v55 text is compared against the v51 truth side. So closing this
> is a docstring-and-harvest repair, not a content change.
>
> **One artifact that is NOT a defect and must not be "fixed".** `strip_desc()` keeps the *last*
> pipe-delimited cell, so a description containing a `|` is truncated. Only `P_OR_AB`
> ("Select A | B, B") does, the tool truncates both sides identically, and it self-cancels. The
> shipped record is correct as written; do not align it to the tool's displayed `"B, B"`.

### F-340 — `validate-crossref-keys.py` validates TOP-LEVEL keys only, so 67 nested `related_symbols:` lists in one file are never checked at all — `RESOLVED — traversal landed 2026-09-13; validated by the v1.19.0/.1/.2 releases, 2026-09-19`

> **TRAVERSAL LANDED 2026-09-13 (Stephen: "our gate has to be that all references resolve").**
> `validate-crossref-keys.py` no longer reads the top level. It checks **every KB path token in any
> string at any depth** (must be a KB-root-relative path to a file that exists; `engineering/…`
> tokens must exist in the repo; only an `_index.yaml` may list siblings by bare name) and walks
> **every reference field at every depth** — the fifteen typed fields plus any `related_*`,
> `prerequisites`, `next_steps`, `knowledge_progression`, `canonical_entries` — resolving named
> entries against index keys, aliases, and every `symbol_name:` defined in the KB. JSON-schema
> field descriptors are skipped and counted. The F-340 scope banner is gone because there is no
> unread share left to disclose. **Negative control** (`--negative-control`) plants eight defects —
> nested missing path, bogus nested symbol, missing `see_also` path, root-prefixed `next_steps`,
> missing path in an undeclared field, prose in `related`, a bare filename in prose, a `../` path —
> plus a positive control; all eight caught, positive clean. `validate-dod-release.py` now runs the
> negative control as part of the gate, and `release-yamls` states the gate as **0**, not a rate.
> **First run of the full gate: 246 references did not resolve** (F-434) and it surfaced **F-431**;
> the nested walk alone would have caught F-338 in August.

> **Location:** `engineering/tools/validate-crossref-keys.py:491-492` —
> `if field_name not in content or not content[field_name]: continue`, where `content` is the
> parsed file's **top-level** mapping. Every `CROSS_REF_FIELDS` entry is looked up there and
> nowhere else. For **«#305»**.
>
> **Measured consequence.** `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` carries
> **135 `related_symbols:` lists**, every one nested inside a record, and the validator reports
> `related_symbols: 7 resolved` for the whole KB. Those 7 are the seven entries of the **one**
> top-level `related_symbols:` in the entire corpus — `language/pasm2/asmclk.yaml:76-83` — and this
> file contributes **zero** references to the count. **This is exactly how F-338
> survived**: two names that do not exist, sitting in a field the validator names in its own
> vocabulary, in the file that holds 99% of that field's instances.
>
> **What is owed.** Walk nested structures for the cross-reference fields, not just the top-level
> mapping — and add a negative control that plants a known-bad name in a nested list and proves
> the walk fails on it. A field that reports "resolved" while reading none of the corpus is worse
> than no check: it reads as coverage.
>
> **«#305» DISPOSITION, 2026-08-25 — the SCOPE half is done; the TRAVERSAL half is still owed.**
>
> This finding was assigned to «#305» because that task arms two release gates and must not
> arm anything on a number that reads wider than it is. What «#305» did:
>
> - **The blind spot is now MEASURED AND PRINTED on every run.** The validator counts the
>   reference sites its traversal cannot reach and reports them beside the rate:
>   *"⚠️ SCOPE: this traversal reads TOP-LEVEL fields only. 688 nested reference site(s) were
>   NOT checked (82% of 3849 coverage)."* A gate must read the artifact; a blind spot that is
>   counted is no longer silent.
> - **The inflated banner is gone.** `✅ ALL CROSS-REFERENCES VALIDATED SUCCESSFULLY` now reads
>   `✅ ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — 688 nested site(s) NOT checked (F-340)`, and
>   `validate-dod-release.py` reports *"All TOP-LEVEL cross-references resolve"* rather than
>   *"All cross-references resolve"*. The same wording is carried into `release-yamls` Step 1
>   and into the sprint plan's *what a green exit does not certify* section.
> - **A missing measurement now FAILS the release.** The DoD check previously passed silently
>   when the validator printed no resolution rate at all; a validator that printed no
>   measurement audited nothing, and that now fails.
>
> **Why the traversal itself was NOT landed here, measured rather than assumed.** With the
> nested walk enabled, **54 references do not resolve** — 26 `related_symbols` (including four
> JSON-Schema keywords, `type`/`items`/`description`/`required`, which the walk reaches inside
> `spin2-language-schema.yaml` and which are not references at all), 15 `related_documentation`
> (descriptive text such as *"P2 Silicon Documentation"*, *"Pin mapping references"*), 2
> `related_pasm`, and the rest spread thin. Roughly half are content triage and half are a
> field-typing question (should `related_documentation` be `'text'` like `see_also`?). That is
> a task, not a side effect of arming a different gate, and landing it inside «#305» would have
> turned a green release path red on 54 items with no owner.
>
> ⚠️ **Counting units differ between this entry and «#305»'s measurement, and both are right.**
> This finding counts **sites** (742 seen / 230 unseen, 76%). «#305» counts **individual
> references** (3161 seen / 688 unseen, 82%). Same defect, same dominant field
> (`related_symbols`), different denominators — do not treat one as correcting the other.
>
> Status: `RESOLVED` — scope half 2026-08-25; the nested traversal and its negative
> control landed 2026-09-13 (see the TRAVERSAL LANDED note under the headline). The owed
> validation — a YAML release running clean against the full gate — ran on 2026-09-19:
> v1.19.0, and again at v1.19.1 and v1.19.2, each with the gate green at 3,7xx references.

## Pin drive-strength documented as bias resistors, and one block fabricated outright (2026-08-24, agent-report sweep) — F-321…F-327, F-329, F-333

> 🔴 **F-322's SOURCE ATTRIBUTION IS WRONG — CORRECTED BY THE ARBITER 2026-08-25 (during «#295»
> phase 1). The finding's VERDICT stands; its cited evidence does not, and «#296» must not inherit
> the string.**
>
> F-322 reads: *"What the source actually prescribes — same file, §'Weak Pull-Up':
> `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)`"*, citing `sources/silicon-doc/part4-smart-pins.txt`.
> **There is no such section in that file.** Case-insensitive search for *pull-up* / *pull up* /
> *pullup* / *pull-down* across `part4-smart-pins.txt` returns **zero hits**.
>
> **Where the string actually comes from, measured:** `engineering/ingestion/smart-pins-catalog/
> ingestionSources/basic-io/spin2-v51-extract.md:284-287` — a **derived catalog extract**, not a
> Parallax document, carrying a `### Weak Pull-Up` heading over
> `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)` with the hand-written comment *"15kΩ pull-up, float when
> driving low"*. Its neighbours (*"Hysteresis for noisy signals"*, *"Maximum drive strength
> (default)"*) are the same authored-commentary shape. **This is our own writing, not the source's.**
>
> ⚠️ **AND THE OPPOSITE OVERSTATEMENT IS ALSO WRONG.** «#295»'s design concluded *"no Parallax
> documentary source states a `P_HIGH_15K | P_LOW_FLOAT` idiom."* Too strong as worded — the string
> does exist in the ingestion tree, at the line above. The accurate statement is narrower and is
> what phase 2 must carry: **Spin2 v55 — the current edition, which supersedes v51 — defines both
> constants individually and composes them into no idiom at all.** `spin2-v55-text.txt:1504`
> = *"P_HIGH_15K | Drive high 15kΩ"*; `:1519` = *"P_LOW_FLOAT | Float low"*. The composition, and
> the word "pull-up" attached to it, are ours.
>
> **Disposition, unchanged in outcome:** under D4 the idiom does not ship as documentary. What ships
> instead is stronger — **EF-063/EF-064**, hardware-verified on real silicon
> (`external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`), which state
> `P_HIGH_15K` with **DIR high** and do **not** use `P_LOW_FLOAT`. Empirical outranks documentary
> here, so the substitution is an upgrade rather than a workaround.
>
> 🔴 **THIS IS THE SECOND CONFIRMED FINDING TODAY WHOSE EVIDENCE CITATION WAS WRONG** — F-327's
> `:296` attribution was the first, corrected in this same section. Both were caught by
> re-verification during execution, not by review at filing time. A finding's VERDICT and its
> CITED EVIDENCE are separately fallible, and this register's own citations need the same
> hand-verification we apply to the KB's. Route to «#300»/«#302» as a register-wide evidence audit.

> 🔴 **SCOPE OF F-321/F-323 CHANGED BY «#293» — MEASURED BY THE ARBITER 2026-08-24, READ THIS
> BEFORE WORKING «#296».** «#293» removed the uncited `pull_up_modes:` / `pull_down_modes:` blocks
> from `language/spin2/concepts/basic-io.yaml` and `language/pasm2/concepts/basic-io.yaml` as part
> of the §4 purge. Those blocks were carrying most of the mislabel, so the deletion resolved much
> of F-321/F-323 as a side effect:
>
> | `audit-constant-fidelity.py` | at «#293» entry | after «#293» |
> |---|---|---|
> | `[CONTRADICT]` (Tier 2) | **23** | **5** |
> | `[UNDEFINED]` (Tier 1) | **50** | **55** |
>
> **«#296»'s verify criterion is therefore `5 → 0`, not `23 → 0`.** Do not read the remaining 5 as
> a partial failure of anything.
>
> **And «#295» must now define 55, not 50.** The five that newly became `[UNDEFINED]` are
> `P_HIGH_150K` · `P_HIGH_15K` · `P_HIGH_1K5` · `P_LOW_15K` · `P_LOW_1K5` — drive-strength
> selectors whose ONLY definition in the shipped set lived inside the deleted mislabel blocks, so
> removing the wrong description removed the only definition with it. That is remove-all working as
> designed, not a regression: «#295» defines them from the source, in the source's own words.
>
> The «#293» executor did not surface this — it never ran `audit-constant-fidelity.py`, which is
> not in its task's verify list. The arbiter measured it at the boundary by diffing HEAD against
> the working tree. A dispatched agent sees one task, not the dependency graph.

> **Origin.** An agent consuming the published KB could not work out how to use pull-ups and
> pull-downs, and reported conflicts around the smart-pin area (relayed by Stephen, 2026-08-24).
> Agent report is a lead, not a source; every item below was re-derived from
> `{{DOMAIN_AUTHORITY}}` before filing.
>
> **F-329 was added to this section 2026-08-24**, after the `p2-hardware-manual` DOCX re-ingestion
> found the *same* fabricated ladder in three further blocks of `io_pin_timing.yaml` that F-327's
> location line does not cover. It belongs to this root cause, not a new one.
>
> **Root cause, one sentence:** *the P2 has no pull-up or pull-down resistors, and the KB
> documents a whole family of them.* `P_HIGH_*` / `P_LOW_*` select **drive strength** — how hard
> the pin drives **while it is driving** — and the KB reframes them as always-on bias resistors.
> Every downstream error in this sweep follows from that one reframing.
>
> **NOT a regression of the 2026-07-01 `P_*` audit (F-177…F-183).** That audit's question was
> *"is this constant NAME legal in v55?"* — arbiter `pnut-ts`, enumeration the v55 manual — and
> its answer still holds: every name here is legal. It never asked whether the KB's **description**
> of a constant matches the source's. `P_HIGH_15K` is a legal name carrying a wrong definition,
> which the name audit cannot see by construction. **Name coverage is not semantic coverage.**
> This sweep is the first evidence of that gap having live consequences, and it is the case that
> motivates the source-fidelity gate.
>
> **Primary source for the whole sweep:**
> `engineering/ingestion/smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md`,
> the predefined-label tables at lines ~150–195, plus
> `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt` for the DIR/output rule.

### F-321 — the 16 `P_HIGH_*` / `P_LOW_*` drive-strength selectors are documented as pull-up/pull-down resistors — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `language/spin2/concepts/basic-io.yaml:203-213` (`pull_up_modes:` / `pull_down_modes:`)
> and `language/pasm2/concepts/basic-io.yaml:271-281` (same two blocks, same values).
>
> **What is wrong.** The source names these by what they do; the KB renames them by what a reader
> coming from another MCU expects:
>
> | Constant | Source wording | KB wording |
> |---|---|---|
> | `P_HIGH_1K5` | Drive high 1.5kΩ | "1.5kΩ **pull-up** (strong)" |
> | `P_HIGH_15K` | Drive high 15kΩ | "15kΩ **pull-up** (medium)" |
> | `P_HIGH_150K` | Drive high 150kΩ | "150kΩ **pull-up** (weak)" |
> | `P_HIGH_1MA` | Drive high 1mA | "1mA constant current **pull-up**" |
> | `P_LOW_1K5` | Drive low 1.5kΩ | "1.5kΩ **pull-down** (strong)" |
> | `P_LOW_15K` | Drive low 15kΩ | "15kΩ **pull-down** (medium)" |
> | `P_LOW_150K` | Drive low 150kΩ | "150kΩ **pull-down** (weak)" |
> | `P_LOW_1MA` | Drive low 1mA | "1mA constant current **pull-down**" |
>
> The KB also drops the two ends of each ladder entirely — `P_*_FAST` (drive fast, 30mA; the
> default) and `P_*_FLOAT` (float) — and omits `P_*_100UA` / `P_*_10UA` from these blocks.
>
> **Why it matters, not just a wording preference.** A pull-up is active whenever the pin is not
> driven. A drive-strength selector applies **only while the pin drives that direction**. The two
> behave differently in exactly the case a reader reaches for a pull-up — a released bus, a button
> to ground — so the rename does not simplify the model, it inverts it. F-322 is the direct
> consequence.
>
> **Correction.** Restate all sixteen in the source's own terms — drive strength for the high side
> and the low side, selected independently — and delete the `pull_up_modes:` / `pull_down_modes:`
> framing. Where the reader's *intent* is a pull-up, document the idiom, not a fictional component
> (see F-325). Match the source's wording, not an interpretive paraphrase.
>
> **APPLIED 2026-08-25 by «#296» §5, across three tasks.** «#293» deleted the two `pull_up_modes:` /
> `pull_down_modes:` blocks; «#295» re-defined all sixteen from the source in the single home
> (`language/spin2/symbols/spin2-builtin-symbols-complete.yaml`); «#296» removed the surviving
> mislabel from every remaining site. `audit-constant-fidelity.py` `[CONTRADICT]` **5 → 0**
> (`PASS  no Tier 1 violations across 120 source-defined constant(s); 0 Tier 2`).
>
> **Sites corrected in this pass, with the source line each was matched against** — all four
> quantities re-read on disk 2026-08-25, and v55 (current edition) preferred over the v51 extract
> the tool cites:
>
> | Site | Was | Now | Source |
> |---|---|---|---|
> | `language/spin2/conventions/johnny-mac-documentation-style.yaml:303` | "150K pullup resistor" | `P_HIGH_15K` · "drive high 15 kOhm" | `sources/spin2-v55/spin2-v55-text.txt:1504` |
> | `language/spin2/conventions/spin2-docs-jonnymac.yaml:196` | "150K pullup resistor" | `P_HIGH_15K` · "drive high 15 kOhm" | `spin2-v55-text.txt:1504` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53` | "Add pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:84` | "With pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
> | `language/pasm2/concepts/basic-io.yaml:241` | "Enable pull-up" | "Drive high 15kOhm" | `spin2-v55-text.txt:1504` |
>
> **Why the two `conventions/*.yaml` rows also change CONSTANT.** Their example is a bit-banged
> sensor read on a timing loop, and both were rewritten to the verified `weak_high` composition
> that `architecture/pin-drive-configuration.yaml` ships — which is stated with `P_HIGH_15K`
> (EF-063). `P_HIGH_150K` is the weakest resistive rung but one; holding a bit-banged line through
> it is not a composition any source or bench result states, so keeping the name would have meant
> shipping an unverified idiom to preserve a constant that was only ever incidental to a
> *documentation-style* example. The rung actually verified on silicon is what ships.
>
> **Plus eleven sites the instrument cannot see** (its limitation 3 — prose that names no constant,
> and a comment on the line *above* the constant rather than at end-of-line): the
> "internal pull resistors" framing in both `concepts/basic-io.yaml` summary/description/
> critical_distinction blocks and their `configuration_layer.methods` lists, the two
> `guides/*-getting-started.yaml` "pull resistors" blurbs, `hardware/addon-control-board.yaml`'s
> "internal pull-down (P_LOW_15K)" notes (×4 + 2 code comments),
> `hardware/p2-hardware-feature-comparison.yaml:141` (see **F-343**),
> `language/spin2/methods/pinfloat.yaml:67`, `language/spin2/methods/cogstop.yaml:110` and
> `code-examples/smart-pins-002-button-reading.yaml:62` (the last three said "pull-up/pull-down
> resistors" without saying *external*, which in a P2 file reads as a chip feature — each now says
> **external**, matching `pinfloat.yaml:78`'s own already-correct wording).
>
> **Not rewritten, because the source itself carries the mislabel:** `hardware/addon-rtc.yaml:49-51`
> — filed as **F-342**.
>
> **Verified, not asserted.** The zero was proved non-vacuous by a negative control: the mislabel was
> re-inserted into all five flagged files, `audit-constant-fidelity.py` reported exactly those five
> `[CONTRADICT]` rows, and the files were restored (`git status --short deliverables/ai/P2` back to
> the 12 intended files). A gate that cannot fail has not been verified.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. `architecture/pin-drive-configuration.yaml` is now the single home and states the ladder as DRIVE STRENGTH by encoding (%000 Fast, %001 1.5k, %010 15k, %011 150k, %100 1mA, %101 100uA, %110 10uA, %111 Float) with both P_HIGH_*/P_LOW_* constant names per rung. The words `pull-up resistor` / `pull-down resistor` / `bias resistor` survive ONLY as `aliases:` — deliberately, so an agent searching the wrong-but-common term lands on the correct page. That is the findability mechanism working, not a residual defect.
### F-322 — every worked pull-up example disables the drive it just configured, so none of them work — `RESOLVED — validated on the served KB 2026-09-11`

> **Where — 8 sites, 3 files:**
> `language/spin2/concepts/basic-io.yaml:218-219, 229-230, 296-297, 377-378` ·
> `language/pasm2/concepts/basic-io.yaml:286-287, 348-349` ·
> `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53-54, 84-85`
>
> **The shape, in every one of them:**
> ```spin2
> PINSTART(16, P_HIGH_15K, 0, 0)   ' "15kΩ pull-up"
> PINFLOAT(16)                     ' "Input with pull-up"
> ```
> and its PASM2 twin, `WRPIN ##P_HIGH_15K` followed by `DIRL`.
>
> **Evidence it cannot work.** `part4-smart-pins.txt:74` — *"for smart pin mode off
> (%SSSSS = %00000): **DIR enables output**."* `PINFLOAT` / `DIRL` set DIR=0. With the output
> disabled the drive-high selector is inactive, so the pin is plain high-impedance: **no pull-up
> of any strength.** An agent following any of these ships a floating input whose reads depend on
> whatever is on the board.
>
> **What ships instead** ⚠️ *(this paragraph REWRITTEN IN PLACE by the arbiter 2026-08-25 during
> «#296». What stood here — a `WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)` attributed to a Silicon Doc
> §"Weak Pull-Up" — was **wrong about its source and is not shipped**. The section-preamble block
> above carries the full measurement. It is rewritten rather than annotated because a reader
> arriving top-down would otherwise act on a false claim before reaching the note that retracts
> it — which is the same two-places-drift defect this whole section is about.)*
>
> There is **no** Silicon Doc §"Weak Pull-Up"; `sources/silicon-doc/part4-smart-pins.txt` returns
> zero hits for pull-up/pull-down. Spin2 **v55** — the current edition — defines the two constants
> individually (`spin2-v55-text.txt:1504` *"Drive high 15kΩ"*, `:1519` *"Float low"*) and composes
> them into **no idiom at all**. The composition, and the word "pull-up" attached to it, are ours.
>
> The correct composition is **hardware-verified, which outranks documentary here** — EF-063/EF-064
> (`external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`): `WRPIN` with
> `P_HIGH_15K`, then **DIR high** (`PINHIGH` / `DRVH`), and **no `P_LOW_FLOAT`**.
>
> 🔴 **The part of the original paragraph that was RIGHT, and is the finding's actual substance:
> DIR must be HIGH, not low.** A drive-strength selection does nothing while the pin is floated —
> that is precisely what F-322's `PINFLOAT`/`DIRL` examples destroyed, and why a clean compile
> proved nothing about them. Shipped in `architecture/pin-drive-configuration.yaml` as the
> `weak_high` / `weak_low` idioms, DIR stated in both.
>
> **Correction.** Rewrite all eight against the source idiom, with DIR high and the low side
> floated, and say plainly why DIR=0 defeats it — that sentence is the one a reader needs and no
> file currently contains it.
>
> 🔴 **The "What the source actually prescribes" paragraph above is SUPERSEDED** by the arbiter's
> attribution correction at the head of this section (2026-08-25). `P_HIGH_15K | P_LOW_FLOAT` under
> a §"Weak Pull-Up" heading is **our own** derived catalog extract, not a Parallax statement, and it
> was **not** shipped. Read that block before this one.
>
> **APPLIED 2026-08-25 by «#296» §5.** Four sites survived «#293»'s purge; all four were rewritten to
> the **hardware-verified** composition (EF-063 / EF-064,
> `external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md:827,840`) that
> `architecture/pin-drive-configuration.yaml` already ships — `P_HIGH_15K` with **DIR high**, and no
> `P_LOW_FLOAT`. Every one now carries the DIR sentence explicitly:
> *"DIR=1, OUT=1 - a drive is live only while DIR is high."*
>
> | Site | Was | Now |
> |---|---|---|
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53-54` | `WRPIN(...P_HIGH_15K)` + `PINFLOAT` | `WRPIN` + `PINHIGH` |
> | `architecture/smart-pins/smart-pin-00000-normal-mode.yaml:84-85` | `WRPIN ##...P_HIGH_15K` + `DIRL` | `WRPIN` + `DRVH` |
> | `language/pasm2/concepts/basic-io.yaml` `button_read` | `WRPIN ##P_HIGH_15K` + `DIRL` | `DIRL` (pre-config) → `WRPIN` → `DRVH` |
> | `language/spin2/concepts/basic-io.yaml` `button_read` | `PINSTART(...)` + `PINFLOAT` | `PINCLEAR` → `WRPIN` → `PINHIGH` |
>
> **Plus one the finding's location line did not cover:** `language/spin2/concepts/basic-io.yaml`
> `application_examples.matrix_keypad` had the identical `PINSTART(... P_HIGH_15K ...)` +
> `PINFLOAT(...)` pair on the column pins, so the whole scan read undriven pins. Rewritten to the
> same idiom.
>
> **And the two `conventions/*.yaml` style files** carried the same shape a third way: they
> configured `P_HIGH_150K` and never raised DIR at all, then read the pin with `RDPIN` — which
> returns the *smart pin's* Z register and is meaningless with the smart pin off
> (`%SSSSS = %00000`). Both rewritten: `P_HIGH_15K` → `WRPIN` → `DRVH` → `TESTP … WC` → `RCL`.
>
> **Compiled AND read for semantics, separately — a clean compile is not a verification, and this
> finding is why.** All nine touched examples compile under `pnut-ts v1.55.3` from the *shipped YAML
> bytes* (extracted with `yaml.safe_load`, not retyped). `P_HIGH_15K` was confirmed to be `$1000`
> and `##P_NORMAL | P_HIGH_15K` confirmed to bind the `##` to the whole expression, by byte-identity
> of the compiled binaries against `##$1000` — and against `##($C0 | $1000)` for `P_TT_11`, so the
> control has a non-zero left operand.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. the worked examples now pair the configuration with `DRVH` and say why: *"DIR = 1, OUT = 1 -- REQUIRED; DIRL here floats the pin"* and *"a drive is live only while DIR is high"*. The Spin2 file additionally documents the original error in place: *"PINFLOAT(16) as 'input with pull-up' ... Both are wrong: PINFLOAT drops DIR, which deactivates [the drive]"*.
### F-323 — the two `basic-io.yaml` files give contradictory mechanisms for the same feature — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `language/spin2/concepts/basic-io.yaml:197-201` says internal bias is enabled
> *"via **PINSTART()** with special modes"*; `language/pasm2/concepts/basic-io.yaml:265-269` says
> *"via **WRPIN** smart pin modes."* Same concept, two files, two mechanisms.
>
> **Both are wrong, in different directions**, which is why this is filed separately from F-321.
> `WRPIN` alone sets the configuration but leaves DIR untouched. `PINSTART` is the *smart-pin*
> start sequence (WRPIN + WXPIN + WYPIN + DIRH) — using it to set a **non**-smart-pin drive
> strength starts a smart pin that was never wanted, and its DIRH is then immediately undone by
> the `PINFLOAT` on the next line (F-322).
>
> **This is the conflict the reporting agent hit.** It is the only true *conflict* in this sweep;
> everything else here is unanimous error, which is why a conflict-detection gate alone would not
> have caught the rest.
>
> **Correction.** One mechanism, stated once, in the file that owns the concept; the other file
> points at it rather than restating it.
>
> **APPLIED 2026-08-25 by «#296» §5 — by deletion and repointing, not by rewording both copies.**
> «#293» deleted both `internal_pull_resistors:` sections, which carried the two contradictory
> mechanism sentences. «#296» removed what survived them: the residual
> `- "PINSTART() - Enable internal pull resistors"` (spin2, `:29`) and
> `- "WRPIN - Enable internal pull resistors"` (pasm2, `:29`), plus the "pull resistors" phrase in
> both files' `summary:`, `description:` and `critical_distinction:`.
>
> **Neither file restates the mechanism now.** Both point at the single home built by «#295»:
> `deliverables/ai/P2/architecture/pin-drive-configuration.yaml` (index key
> `p2kbArchPinDriveConfiguration`), added as a **full path** in each file's `see_also:` alongside
> `.../spin2-builtin-symbols-complete.yaml`; the surviving `WRPIN` line names the target inline.
> Same repointing added to `architecture/smart-pins/smart-pin-00000-normal-mode.yaml` (`related:`)
> and `language/spin2/methods/pinfloat.yaml` (`see_also:`).
>
> 🔴 **No constant name was written as a YAML key anywhere in this pass.** That shape is what
> `audit-constant-fidelity.py`'s `DEF_RE` reads as a *definition*, and using it would have
> re-manufactured this very finding inside the task chartered to end it. Verified mechanically:
> the tool still attributes **120 source-defined constants** and reports **0** `DIVERGENT`.
>
> `validate-crossref-keys.py`: **3149 → 3156** references, **0 unresolved**, 100.0%.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. both `basic-io.yaml` files now give the SAME mechanism — drive-strength configuration, each redirecting to `architecture/pin-drive-configuration.yaml`. They remain non-identical by design (one states Spin2 method syntax, the other PASM2 instruction syntax); the MECHANISM no longer differs.
### F-324 — `bits_M_6_0: "Control drive strength"` is wrong at both ends — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `language/pasm2/concepts/basic-io.yaml:262`.
>
> **Evidence, decoded from the source's own bit patterns** (13-bit `%M..M` field, M12…M0):
>
> | Constant | Source pattern (M field) | Bits set |
> |---|---|---|
> | `P_HIGH_1K5` | `0000000001000` | M[3] |
> | `P_HIGH_150K` | `0000000011000` | M[4:3] |
> | `P_HIGH_FLOAT` | `0000000111000` | M[5:3] |
> | `P_LOW_1K5` | `0000000000001` | M[0] |
> | `P_LOW_FLOAT` | `0000000000111` | M[2:0] |
> | `P_INVERT_OUTPUT` | `0000001000000` | M[6] |
>
> So **drive-high = M[5:3]**, **drive-low = M[2:0]**, and the source's own encoding notes agree
> (`%…xxxxxxxHHHxxx…` and `%…xxxxxxxxxxLLL…`). **M[6] is output polarity, not drive strength.**
> The KB's `M[6:0]` wrongly annexes the polarity bit and erases the high/low split that makes the
> field usable.
>
> **Correction.** State the two 3-bit sub-fields with their positions. Also fix the companion
> dangling pointer at `language/spin2/concepts/basic-io.yaml:195` —
> *"Consult smart pin mode documentation for drive strength bit encoding"* — which points at
> nothing that exists (F-325 is what it should point at).
>
> **APPLIED 2026-08-25, in two tasks — verified on disk, not carried from the plan.**
>
> - **The wrong field itself is gone.** `bits_M_6_0: "Control drive strength"` was inside the
>   `wrpin_encoding:` block that «#293» deleted from `language/pasm2/concepts/basic-io.yaml`; the
>   companion dangling pointer at `language/spin2/concepts/basic-io.yaml:195` went with the same
>   purge. Confirmed by `grep -n 'wrpin_encoding\|bits_M_6_0'` over both files — **zero hits** —
>   and against `git show 15c84de5~1:` for what was removed.
> - **The correct layout ships**, stated by position, in the home «#295» built:
>   `architecture/pin-drive-configuration.yaml` `sub_fields:` — `output_polarity` **M[6]**,
>   `drive_high` **M[5:3]** (legend `HHH`), `drive_low` **M[2:0]** (legend `LLL`), plus `C` M[8],
>   `I` M[7] and the mode-select bits. The two sources that independently confirm the split are both
>   cited there: the Spin2 v55 symbol-table masks
>   (`sources/spin2-v55/spin2-v55-text.txt:1501` `%…xxxxxxxHHHxxx…`, `:1511` `%…xxxxxxxxxxLLL…`,
>   `:1497` the `O` polarity bit) and the P2 Datasheet 2022/11/01 p.24 Pin Mode Legend
>   (`sources/p2-datasheet/p2-datasheet-text.txt:1131-1147`), cell-identical in the P2 Hardware
>   Manual (`sources/p2-hardware-manual/p2-hardware-manual-text.txt:847-873`).
> - **Nothing in «#296» re-states it.** Per R4 the touched files point at that home rather than
>   carrying a second copy of the bit ranges.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. resolved by relocation rather than rewording — the mislabelled field no longer exists in `wrpin.yaml`. The %M sub-fields, their bit ranges and the drive ladder live once in `architecture/pin-drive-configuration.yaml`.
### F-325 — the drive-strength ladder is fully documented in the ingestion tree and entirely absent from the shipped KB — `RESOLVED — validated on the served KB 2026-09-11`

> **APPLIED 2026-08-25 by «#295» phase 2, in two homes with a boundary between them.**
>
> - **`language/spin2/symbols/spin2-builtin-symbols-complete.yaml`** — 68 records added, so the
>   file now defines **all 116** `P_*` constants the Spin2 v55 symbol table carries
>   (`spin2-v55-text.txt:1419-1562`), each with the source's own wording, its 32-bit value and its
>   bit pattern. `audit-constant-fidelity.py` `[UNDEFINED]` **55 → 0**, exit 1 → 0. Fourteen
>   pre-existing glossed descriptions were re-worded to v55 in the same pass, and a top-level
>   `aliases:` block was added so those 116 names are reachable through the published index at all —
>   `generate-p2kb-index.py` harvests top-level `aliases:` only, and this file had none, so not one
>   of its constants was findable by name.
> - **`architecture/pin-drive-configuration.yaml`** *(new)* — the `%M..M` field: every sub-field
>   with its bit range (this is also F-324's "state the two 3-bit sub-fields"), the eight-rung drive
>   ladder, and the DIR/OUT rule.
>
> 🔴 **The ladder is stated BY ENCODING, never as `NAME: "description"`.** That shape is what
> `audit-constant-fidelity.py` reads as a *definition*, so writing the ladder the natural way would
> have made the new file a **second definition home** for 16 constants and re-manufactured
> F-321/F-323 inside the task chartered to end them. Verified mechanically, not by eye: the tool's
> own `DEF_RE`/`RECORD_RE` match **0** lines in the new file, and the tool attributes **0**
> definitions to it. Measured after: **116 constants defined in the KB, 0 with more than one
> definition, 0 defined outside the single home** (down from 58 defined across two homes with 7
> duplicated).
>
> **The pull-up idiom this finding asks for is NOT shipped as documentary** — see the arbiter's
> F-322 attribution correction above. What ships is the hardware-verified composition
> (EF-063/EF-064): `P_HIGH_15K` / `P_LOW_15K` with **DIR high**, and no `P_LOW_FLOAT`. Both idioms
> carry DIR explicitly, because omitting it is exactly F-322. Both compile under `pnut-ts` v1.55.3
> and were read for semantics; the unverified `P_HIGH_15K | P_LOW_FLOAT` variant is filed as a gap
> (**F-336**), not shipped as content.
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit — the new
> file's index key `p2kbArchPinDriveConfiguration` does not exist until then.

> **What is missing.** Eight high-side values and eight low-side values, each with its bit pattern
> and its meaning — `FAST (30mA)` · `1K5` · `15K` · `150K` · `1MA` · `100UA` · `10UA` · `FLOAT` —
> plus the sub-mode selectors that share the field (`P_SYNC_IO`, `P_INVERT_IN`,
> `P_INVERT_OUTPUT`, the `P_TT_*` / `P_OE` / `P_BITDAC` DIR-OUT controls).
>
> **Where it already exists:** `basic-io/spin2-v51-extract.md:150-195`, as clean tables. It was
> extracted and never promoted into a YAML. Sixteen shipped files *use* these constants; **no
> shipped file defines them.**
>
> **Correction.** Promote the ladder into the KB. Placement is a design decision to settle before
> editing (new `architecture/pin-drive-configuration.yaml` vs. extending the `basic-io` pair) —
> flag it per the `sprint-plan` overlay's design-decision rule rather than deciding it in passing.
> The pull-up/pull-down *idiom* belongs here too, stated as a composition of drive settings
> (`P_HIGH_15K | P_LOW_FLOAT`, DIR high) rather than as a component the chip does not have.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. the ladder is present in the shipped KB in full — eight rows, each with its %HHH/%LLL encoding, its drive, and both constant names — plus a `no_other_rungs:` guard reading *"The legend enumerates these eight and no others."*
### F-326 — `wrpin.yaml` expands three of its six D-operand fields and stubs the one that carries the pin configuration — `RESOLVED — validated on the served KB 2026-09-11`

> **APPLIED 2026-08-25 by «#295» phase 2. The deferral now has somewhere to go.** The stub
> `M: "13-bit low-level pin control + smart-pin mode"` is gone; `pasm2/wrpin.yaml`'s
> `d_operand_format.fields:` now points at `architecture/pin-drive-configuration.yaml` for the
> field's internals and at `architecture/smart_pins.yaml` for all six field ranges. The finding's
> own instruction — *"point it at the file F-325 creates, but not at prose that does not exist"* —
> is what was done. `architecture/smart_pins.yaml` gained the reciprocal pointer inside
> `configuration_format.fields.m:`.
>
> **The companion check this finding asks for was done too.** `language/spin2/methods/wrpin.yaml`
> had the same shape *and worse*: `common_smart_modes:` (13 keys) and `tt_field.constants:`
> (4 keys) were **17 second definitions** of constants the symbols file also defines. Both blocks
> are replaced with pointers; the four `P_TT_*` keep their values, binaries and `P_OE`/`P_CHANNEL`/
> `P_BITDAC` aliases in `smart_pins.yaml`, so nothing is lost. Everything else in `tt_field:` —
> `context_dependent:`, `p_oe_required_for:`, `one_bit_three_names:`, `when_smart_pin_on:`,
> `source_selection:` — is field *behaviour*, is cited and correct, and is untouched.
>
> **Owed:** index regeneration + `validate-crossref-keys.py` after the boundary commit.

> **Where:** `language/pasm2/wrpin.yaml`, `d_operand_format.fields`. `AAAA`, `BBBB` and `FFF` get
> full treatment — `input_selectors` enumerates all eight source-select encodings and the invert
> bit. The 13-bit field is one line: **`M: "13-bit low-level pin control + smart-pin mode"`**.
> `language/spin2/methods/wrpin.yaml` should be checked for the same shape.
>
> **Why it happened, and why it is still ours to fix.** The Silicon Doc defers at exactly this
> field — *"In the Spin2 documentation, there are many predefined labels documented, which cover
> these pin configurations"* (`part4-smart-pins.txt`, after the `%FFF` table). The ingestion
> followed the source faithfully to the deferral and then **stopped at the pointer instead of
> following it**, even though the target was itself ingested (F-325). `wrpin.yaml` is where an
> agent asking "how do I configure a pin" lands, so the stub sits directly on the path that
> generated this whole sweep.
>
> **Correction.** Expand the field, or point it at the file F-325 creates — but not at prose that
> does not exist. **A deferral in a source is a work item, not an answer**, and this sweep is the
> cost of treating one as an answer.


**VALIDATED ON THE SERVED KB 2026-09-11** — read from the published tree (v1.18.1, on the remote), not from a status line. `wrpin.yaml`'s `d_operand_format.fields` no longer expands ANY of the six — it redirects all six to `architecture/smart_pins.yaml` and the 13-bit %M internals to `pin-drive-configuration.yaml`, under the comment *"One home per fact ... Restating them here is what let three of the six drift wrong (F-331)."* The stub-vs-expansion asymmetry the finding named is gone because nothing is expanded here now.
### F-327 — `io_pin_timing.yaml` documents a pin drive-strength system, and a slew-rate control, that no source describes — `RESOLVED — validated on the served KB 2026-09-11`

> **Where:** `architecture/io_pin_timing.yaml:200-233` (`drive_strength_configurations:`)
> and `:234-246` (`slew_rate_control:`).
>
> **This is a different and more severe class than F-321.** F-321 is a *mislabel* — the KB
> renamed a real mechanism. This is **fabrication**: the KB describes a mechanism that does
> not exist. Four claims, none of which any authoritative source states:
>
> | KB claim | Source check |
> |---|---|
> | Drive ladder `1.5mA · 3.0mA · 15mA · 30mA · 75mA · 150mA` | **Not in any source.** The real ladder is `FAST (30mA) · 1.5kΩ · 15kΩ · 150kΩ · 1mA · 100µA · 10µA · FLOAT`, eight values per side. |
> | Impedance table `~2000Ω · ~1000Ω · ~200Ω · ~100Ω · ~40Ω · ~20Ω` | **Zero hits** for this framing in `sources/silicon-doc/`. |
> | `WRPIN_bits: "M[6:5,4:3,2:1,0]"` | Wrong. Drive-high is `M[5:3]`, drive-low `M[2:0]`, and `M[6]` is output polarity (see F-324). |
> | `slew_rate_control:` — fast/slow slew, `<2ns` / `5-10ns`, EMI trade-off | **The string "slew" appears ZERO times** across `sources/silicon-doc/`, `sources/spin2-v51/`, and `smart-pins-catalog/`. The P2 has no documented programmable slew rate. |
>
> **Independent confirmation of the real encoding**, from a second source not used for F-324 —
> `sources/silicon-doc/assets/images-20260706/P2-Silicon-Doc-v35_image_catalog.md:139,161`
> describes the WRPIN figure's own legend: *"HHH/LLL Drive-strength"* and *"the H/L → DRIVE
> strength table (000 Digital, 001 1.5k, 010 15k, 011 150k, …)"*. Three bits per side, and the
> ladder is resistive, exactly as the Spin2 label table has it.
>
> **Likely provenance, offered as a lead and not as a finding:** `150mA` *does* appear in the
> sources — as the **VIO group current budget** (`p2-complete-signal-flow-matrix.md:193-200`),
> a board-power fact about eight-pin groups. A per-pin drive ladder built from a per-group
> power limit would explain the shape. Do not act on this without checking; it is a hypothesis
> about how the text arose, not a source.
>
> **The tell that makes this mechanically detectable.** The same file cites sources where it
> has them — `absolute_maximum_ratings:` names the Parallax Datasheet (`:267`), and
> `input_voltage_and_protection:` names Silicon Doc v35 in its `latchup_context.source` (`:296`).
> The two fabricated blocks carry **no `source:` field at all**. A file that demonstrates it knows
> how to cite, and then states six quantities and a whole feature without citing anything, is
> flagging itself.
>
> ⚠️ **ATTRIBUTION CORRECTED 2026-08-24 (arbiter, during «#293»).** This paragraph originally
> credited `:296` to **`special_timing_modes:`**. That was wrong, and it mattered: at the HEAD this
> finding was written against, `:296` is a `source:` nested under `latchup_context:` inside the
> **preceding** block `input_voltage_and_protection:` (`:276-297`); `special_timing_modes:` began at
> `:298` and was itself **genuinely uncited** — which is why the sourcing tool flagged it and «#293»
> removed it. The finding's conclusion is unaffected (`:267` does cite, and both fabricated blocks
> do not). Only the second example was misattributed, by exactly the off-by-one-block error that
> **citing a register finding by line number instead of by ID** produces. Resolve findings by ID.
>
> **Correction.** `slew_rate_control:` has no correct form — **delete it outright**; there is
> nothing to align it to. `drive_strength_configurations:` is replaced by the real ladder,
> which after F-325 lands should be a pointer to the single definition home rather than a
> fourth copy. Neither block is "corrected in place": an unsourced claim is removed, not
> rewritten, per this register's no-inference rule.
>
> **Why the fidelity instrument did not catch this, and what it means for the gate.**
> `audit-constant-fidelity.py` compares the KB's description of a *named constant* against the
> source's. These blocks **name no constants** — they describe the mechanism in prose and
> numbers. That is limitation 3 in the tool's own docstring, and it proved itself within the
> hour of being written: *name coverage is not semantic coverage, and that cuts both ways.*
> Detecting this class needs a second detector — **an uncited quantitative claim in a file that
> cites elsewhere** — which is the "information that should no longer be in the files" half of
> the release gate, and is now sprint scope rather than a nice-to-have.
>
> **Class-wide sweep result (2026-08-24): the manuals are CLEAN.** No manual or app-note
> opus-master carries the fabricated ladder, the impedance table, or a pin slew-rate claim.
> (`architect-guide-body.md`'s "slew" hits are rate-adapters in a dataflow sense — unrelated.)
> This class is confined to the YAML, so no manual corrections wave follows from it.

> **APPLIED «#293» 2026-08-24 — REMOVED, repopulation owed.** Both named blocks are gone from
> `architecture/io_pin_timing.yaml`, removed as whole top-level blocks at their entry-state ranges:
> `drive_strength_configurations:` **`:200-233`** (34 lines, 21 quantities) and `slew_rate_control:`
> **`:234-246`** (13 lines, 2 quantities). Removed under the sprint's remove-all rule (D7), **not**
> corrected in place — this entry's proposed "replaced by the real ladder" is withdrawn as
> claim-first; the `SOURCE-REPAIR-ORDER` rule (agent-side) §2 governs, and «#299» re-derives from the
> repaired source or not at all. `slew_rate_control:` is **never** repopulated.
>
> **The zero-hit `slew` claim re-verified at HEAD**, now across five source trees rather than three
> — `sources/silicon-doc`, `sources/spin2-v51`, `smart-pins-catalog`, and both of this sprint's
> re-ingestions, `sources/p2-datasheet` and `sources/p2-hardware-manual`: **0 hits each**.
>
> **«#299» 2026-08-25 — the repopulation decision is made and it is NOTHING.** Working the sources
> rather than the blocks, no Parallax document states a per-pin milliamp drive ladder, an impedance
> table, or a slew rate; the datasheet states drive as eight named MODES
> (*"Separate drive modes for high and low output: logic / 1.5 k / 15 k / 150 k / 1 mA / 100 µA /
> 10 µA / float"*, `sources/p2-datasheet/p2-datasheet-text.txt:117`), which already ship cited in
> `architecture/pin-drive-configuration.yaml drive_ladder`. **None of F-327's or F-329's nine
> `io_pin_timing.yaml` blocks returned**, nor the four `basic-io.yaml` copies. Instead, the two
> `pin_architecture` blocks came back carrying a `no_milliamp_ladder:` key that states the absence
> and points at the definition home, so the next agent to look finds a denial rather than a silence.
>
> `PENDING-VALIDATION` — the removal is applied, the repopulation question is answered, and only
> the YAML release is owed.


**VALIDATED ON THE SERVED KB 2026-09-11** — `p2kb_get p2kbArchIoPinTiming` against the published index (v1.18.1, now on the remote), not the repo tree. The served file's top-level `description:` — the exact field F-333 named as the place no instrument could see — now carries an explicit *"What it deliberately does NOT carry"* section reading: *"Slew rate. There is none to document. 'slew' returns zero hits across every ingested Parallax source ... A prior form of this description asserted configurable slew rates; it was fabrication (F-327, F-333) and is not restored."* Drive strength is likewise redirected to `architecture/pin-drive-configuration.yaml` rather than restated.

**Class sweep run at the same time** (`feedback_classwide_sweep_on_every_finding`): every `slew` occurrence remaining in `deliverables/ai/P2/` is either a NEGATION of the fabricated claim (`basic-io.yaml` x2: *"no programmable slew rate exists"*) or the unrelated Spin2 **slew/easing engine** decomposition pattern, which is a software shaping construct and not a pin electrical claim. No residual assertion survives.
### F-329 — the SAME fabricated drive ladder stands twice more in `io_pin_timing.yaml`, in blocks F-327 does not name, alongside ~20 nanosecond quantities that NEITHER of the sprint's two extraction paths carries — `DONE` (verified 2026-10-05 «#386»: io_pin_timing.yaml blocks cite Silicon Doc lines, v1.23.3)

> **Found:** 2026-08-24, by the DOCX-primary re-ingestion of `p2-hardware-manual` (the source
> plan §8 names as the datasheet's cross-check partner). This is **additive to F-327, not a
> re-file**: F-327's location line is `:200-233` + `:234-246`, and every claim below sits
> **outside** those ranges. Applied literally to the lines it names, F-327's fix would leave the
> fabricated ladder standing in two other blocks of the same file.
>
> **Where — three blocks, none of them named by F-327:**
>
> | Lines | Block | What it carries |
> |---|---|---|
> | `:96-105` | `timing_specifications.output_timing.propagation_delay.fast_mode` / `.normal_mode` | `2.5/3.5/5.0 ns` and `3.5/5.0/7.0 ns` |
> | `:108-113` | `…propagation_delay.drive_strength_impact` | **2nd copy of the fabricated ladder** — `1.5mA · 3.0mA · 15mA · 30mA · 75mA · 150mA`, each with a ns delta |
> | `:118-137` | `…output_timing.rise_time.configurations` | **3rd copy** — five `drive:` entries `150mA/75mA/30mA/15mA/1.5mA`, each with a `15pF` load and a ns rise time |
> | `:145-158` | `timing_specifications.input_timing.propagation_delay` | `2.0/3.0/4.5 ns`, `3.5/5.0/7.0 ns` |
>
> **None of these blocks carries a `source:` field** — the same self-flagging tell F-327 identified.
>
> **1. The cited datasheet pages do not exist.** Line 3 reads
> `# Datasheet Reference: pages 42-45, 76-78, Electrical Specifications`.
> `Propeller2-P2X8C4M64P-Datasheet-20221101.pdf` is **50 pages** (`pdfinfo`). Pages 76-78 cannot
> exist. Its electrical tables are **DC Characteristics on p.47 and AC Characteristics on p.48**;
> pages 42-45 are not them. This is not an off-by-a-few citation — it points outside the document.
>
> **2. Neither of the two independent extraction paths carries I/O-pin timing in nanoseconds.**
>
> - **Path A — P2 Hardware Manual (2022/11/01), re-ingested DOCX-primary 2026-08-24.** Its
>   *I/O Pin Timing* section states delay **only in clock cycles** ("three additional clocks",
>   "three clocks before", "two clocks before"). Its three timing diagrams
>   (`assets/images-p2-hardware-manual-20260824/fig-34..36`, newly extracted — this source had
>   **no image catalog at all** before) are clock-numbered `0..6` with **no nanosecond axis**;
>   `fig-34` was rendered and read to confirm. Across the whole extract
>   (`p2-hardware-manual-text.txt`, 159,098 chars) the unit tokens present are
>   `MHz · V · ms · kΩ · kHz · Ω · µA · pF · mA` — **`ns` appears zero times, and so does the word
>   "nanosecond"**. The document has no nanosecond quantity anywhere in it.
> - **Path B — P2 Datasheet.** Its AC Characteristics table contains exactly **two** symbols:
>   `Freq` (oscillator frequency) and `Cin` (XI/XO pin capacitance). There is no propagation-delay,
>   rise-time or input-timing row anywhere in it.
>
> **Stated as a measurement, not a verdict:** the datasheet's extraction is the known-broken
> `p2-datasheet-narrative.txt`, so "the datasheet does not say X" is weaker evidence than
> "the hardware manual says Y". The AC table's *content* is present in that extract (all symbols,
> parameters, conditions, values and units, merely column-linearized) and it is the only AC table
> in a 50-page document — but **the `camelot lattice` pass owed by plan §8 is what settles it**.
> The drive-ladder half below does not depend on that and is decisive on its own.
>
> **3. The relabeling is decisive on documentary grounds.** The P2 Hardware Manual gives the pin
> drive ladder in two independent places within itself, and both are **resistive**:
>
> - **Table 18's nested legend** (`complete-tables-reference.md`, Table 21 — a table nested inside
>   a cell, which is why a naive DOCX walk drops it): `HHH/LLL` = `000 Fast · 001 1.5 kΩ ·
>   010 15 kΩ · 011 150 kΩ · 100 1 mA · 101 100 µA · 110 10 µA · 111 Float`.
> - **The equivalent-schematic figures** (`fig-10`..`fig-33`), whose on-diagram legend reads
>   `000 Digital · 001 1.5k · 010 15k · 011 150k · 100 1mA · 101 100uA · 110 10uA · 111 Float`.
>
> The KB's `1.5mA / 15mA / 150mA` reuse the numerals of the **kΩ** rungs with the unit changed.
> This is the third source to say so, after F-324's bit-pattern decode and F-327's silicon-doc
> image catalog.
>
> **4. Two of the fabricated rungs exceed the device's rated maximum.** Both sources agree the
> **maximum current per I/O pin is ±30 mA** (Hardware Manual *Specifications* table, verbatim
> `Max current per I/O | +/- 30mA`; the datasheet's DC Characteristics characterises `Vol`/`Voh`
> at sinking/sourcing 1 mA, 10 mA and 30 mA — 30 mA is the top of its own characterisation).
> A `75mA` or `150mA` per-pin drive mode is not a P2 capability, so `rise_time` rows keyed to
> them describe nothing.
>
> **What is NOT wrong in this file, and must survive the purge.** `instruction_to_pin_timing:`
> (`:16-89`) is **exactly corroborated** by the Hardware Manual, clause for clause: output latency
> 3 clocks after the instruction; `INx` reads 3 clocks stale; `TESTP`/`TESTPN` 2 clocks stale
> ("fresher than INx"); smart-pin IN drop 2 clocks after `WRPIN/WXPIN/WYPIN/RDPIN/AKPIN`. That is
> the corroborated core of the file and it is *un*cited today — it needs a citation added, not
> removal. **Recording this is the point of running the ingestion before the purge**: without it,
> a remove-all sweep over uncited quantitative blocks takes the good half with the bad.
>
> **Correction.** Remove `:96-105`, `:108-113`, `:118-137` and `:145-158` under the sprint's
> source-first rule (an uncited claim is removed, not rewritten). Fix or delete the impossible
> page citation on line 3. Re-derive `instruction_to_pin_timing:` in place with a citation to
> the Hardware Manual's *I/O Pin Timing* section. Fold the drive-ladder occurrences into whatever
> single definition home F-325 creates rather than leaving a fourth, fifth and sixth copy.
>
> **Lesson for the sweep that follows.** F-327 found this class and named two blocks; the same
> fabrication was sitting in three more blocks of the same file, and the deciding evidence for
> two of them was **inside a table nested in another table's cell** and **inside a figure**.
> A finding's location line is where it was *seen*, never the extent of the defect —
> sweep the file, not the line range.

> **APPLIED «#293» 2026-08-24 — REMOVED, one item owed.** All four locations this entry names sit
> inside the single top-level block `timing_specifications:` (`:90-172` at entry state), which was
> removed whole — 83 lines, 45 quantities — taking `:96-105`, `:108-113`, `:118-137` and `:145-158`
> with it. Six further uncited quantitative blocks in the same file went in the same pass, per this
> entry's own "sweep the file, not the line range": `clock_relationships:` `:173-199`,
> `input_characteristics:` `:247-262`, `special_timing_modes:` `:298-320`,
> `protocol_timing_examples:` `:321-337`, `compensation_techniques:` `:359-374`,
> `best_practices:` `:375-391`. The file went 433 → 175 lines (`wc -l`).
>
> **The impossible page citation is gone in both of its two locations** — the header comment
> (`# Datasheet Reference: pages 42-45, 76-78, Electrical Specifications`) *and* its restatement
> inside `extraction_metadata.source_documents` as a `- document: "P2 Datasheet"` entry listing the
> same two ranges plus "Timing characteristics tables". This entry named only the header; sweeping
> the file found the second copy, which is this entry's own lesson applied to itself.
>
> **`instruction_to_pin_timing:` survived, as this entry requires** — it is intact at `:15` and was
> never flagged (it states delay in clocks, which carry no unit token). Its citation is owed to
> «#299», and its corroboration is already found and recorded here.
>
> `PARTIAL` because the removals are applied and the `instruction_to_pin_timing:` citation is owed.

### F-333 — the fabricated slew-rate claim ALSO stood in `io_pin_timing.yaml`'s top-level `description:`, where no instrument could see it, because it carries no unit — `RESOLVED — validated on the served KB 2026-09-11`

> **Found:** 2026-08-24, by «#293», *after* removing every block F-327 and F-329 name. A residual
> `grep -i slew` over the file — run because F-329's lesson says to sweep the file, not the line
> range — returned one surviving hit that both prior findings had walked past.
>
> **Where:** `architecture/io_pin_timing.yaml:9-14`, the top-level `description:` block, reading
> *"Each pin can be configured for different drive strengths, slew rates, and input
> characteristics."* Removed whole (6 lines). The file now returns **0** hits for `slew`.
>
> **Why no instrument caught it, and this is the point of the finding.**
> `audit-yaml-claim-sourcing.py` fires on an uncited block that states a **physical quantity**, and
> a quantity requires a **unit token** — that is what makes the gate mechanical rather than a matter
> of taste. This sentence names the fabricated *mechanism* and attaches **no number to it at all**,
> so it scores zero quantities and is structurally invisible to the gate, exactly as
> `audit-constant-fidelity.py` was structurally blind to F-327 for naming no constants.
>
> **Both of this sprint's instruments therefore share one shape of blind spot:** each keys off a
> *token* — a constant name, a unit — and a fabrication written in plain prose carries neither. The
> gate is still worth having; it found 59 blocks in these four trees. But **passing it is not
> evidence that a file is free of fabrication**, and no release note should imply otherwise.
>
> **No new evidence is owed.** The claim is F-327's, already `CONFIRMED`, and «#293» re-verified its
> zero-hit basis across five source trees at HEAD. This entry records a third *location*, not a new
> claim.
>
> **Consequence for «#299»:** `io_pin_timing.yaml` now has no top-level `description:`. Whatever is
> written back must not restore "slew rates", and must come from the repaired Hardware Manual /
> Datasheet rather than from the removed text.
>
> **REPLACEMENT WRITTEN 2026-08-25 by «#299».** `architecture/io_pin_timing.yaml` now carries a
> top-level `description:` derived from the repaired P2 Datasheet, cited to
> `sources/p2-datasheet/p2-datasheet-text.txt:117` and `:2126-2149`. It says what the file carries
> (instruction-to-pin latency, absolute maximum ratings, 5 V handling) and then says outright what
> it does NOT carry and where those live — drive strength at
> `architecture/pin-drive-configuration.yaml`, and slew rate nowhere, because there is none.
>
> ⚠️ **THE ZERO-HIT CRITERION IN THIS ENTRY IS NOW WRONG AND MUST NOT BE RE-RUN AS WRITTEN.**
> `grep -ci slew` on `io_pin_timing.yaml` returns **2**, and both hits are the new description
> **naming slew rate in order to forbid it** — the same deliberate-mention shape
> `audit-guide-conformance.py` already classifies as `[D6] named in order to forbid it`, and the
> same shape `pin-drive-configuration.yaml not_documented_here` uses. The correct check is that no
> hit ASSERTS a slew rate. Stated here explicitly so a later sweep does not "fix" the denial back
> into a silence, which is what let this claim survive two purges in the first place.
>
> `PENDING-VALIDATION` — the removal and the replacement are both applied; only the YAML release
> is owed.


---


**VALIDATED ON THE SERVED KB 2026-09-11** — `p2kb_get p2kbArchIoPinTiming` against the published index (v1.18.1, now on the remote), not the repo tree. The served file's top-level `description:` — the exact field F-333 named as the place no instrument could see — now carries an explicit *"What it deliberately does NOT carry"* section reading: *"Slew rate. There is none to document. 'slew' returns zero hits across every ingested Parallax source ... A prior form of this description asserted configurable slew rates; it was fabrication (F-327, F-333) and is not restored."* Drive strength is likewise redirected to `architecture/pin-drive-configuration.yaml` rather than restated.

**Class sweep run at the same time** (`feedback_classwide_sweep_on_every_finding`): every `slew` occurrence remaining in `deliverables/ai/P2/` is either a NEGATION of the fabricated claim (`basic-io.yaml` x2: *"no programmable slew rate exists"*) or the unrelated Spin2 **slew/easing engine** decomposition pattern, which is a software shaping construct and not a pin electrical claim. No residual assertion survives.
## Open — CONFIRMED corrections (2026-08-11, DeSilva reader-report sweep)

> **Sweep origin:** a reader reported that the DeSilva tutorial's Ch.1 "Experiment 3:
> Fading" does not fade on a P2 EVAL (#64000 Rev B) — copied, pasted, triple-checked.
> Root cause: the smart-pin mode was written **without `P_OE`**, so the smart pin
> generated the PWM but the pin's output driver stayed disabled. Confirmed against
> `language/spin2/methods/wrpin.yaml` `tt_field` — `when_smart_pin_on: "x0=output
> disabled, x1=output enabled (regardless of DIR)"` and `p_oe_required_for: "All output
> modes (NCO, PWM, Pulse, Transition, Serial TX, DAC, USB)"`. The manual was fixed the
> same pass; **the same class is still present in the KB's own examples**, below.
> Note this class had already been fixed once in DeSilva (v3.0.3 corrected the
> async-serial TX recipe to `P_ASYNC_TX | P_OE`) but was **not swept class-wide** —
> which is how the PWM example survived to a reader.

- **F-250 — the #64000 Eval Board Rev C guide was ingested with EVERY DIGIT MISSING; any
  numeric fact traced to it is unsafe.** — `DONE` (verified 2026-10-05 «#386»: re-ingested with the digit-density gate; KB half closed under F-328) · `engineering/ingestion/sources/p2-eval-board/`
  was extracted with a text-layer tool, but that PDF's font encoding does not map numerals —
  `pdftotext` silently drops them. Evidence: the shipped `p2-eval-board-narrative.txt` has
  digits on **91 of 1315 lines**; `pdf-ocr --force-ocr` + re-extract yields **368**. Lines
  read *"The Propeller has cores, KB of hub RAM, and Smart I/O pins"* (8 / 512 / 64 gone)
  and *"Buffered LEDs on top eight I/O pins"* survives only because "eight" is spelled out.
  **Consequences:** (1) the LED pin map sat as `TBD` in `hardware/p2-eval-board.yaml` for
  months while the answer was in the repo (F-248) — no grep for `P56` could hit a document
  with no digits; (2) **every** voltage, current, capacity, pin number, part number and page
  reference sourced from this extraction is suspect; (3) the extraction audit and
  cross-source analysis both list "LED pins" as a *gap*, so the loss was mistaken for the
  source being silent. **→ TRACKED → ingestion:** re-ingest this source with forced OCR,
  re-verify every numeric claim already derived from it, and — the general lesson —
  **add a digit-density sanity check to the ingestion pass**: a hardware document whose
  extraction is nearly digit-free has failed, not been read. Worth spot-checking the other
  board/hardware sources for the same font family.
  >
  > **INGESTION HALF APPLIED 2026-08-24** (sprint task #306, ahead of the #294 purge — under
  > remove-all, whatever this failed to recover would have been *permanently* gone).
  >
  > - **Re-ingested, forced OCR.** `pdf-ocr --force-ocr --deskew` → `pdftotext -layout` →
  >   `engineering/ingestion/sources/p2-eval-board/p2-eval-board-text.txt`. Density
  >   **1.5% → 56.5%** on the gate tool's metric (lines of ≥12 chars), **10.0% → 52.6%** on
  >   non-blank lines — the frame this filing used above, where its 91/1315 counted every
  >   line including blanks. Quote the metric with the number; they are not interchangeable.
  >   In the 29–58% peer band. Prior capture archived, not deleted:
  >   `sources/p2-eval-board/archive/` (+ `archive/README.md` pointer, + a fresh `pdftotext`
  >   run kept as the evidence exhibit).
  > - **Recovered, triple-validated** (OCR ∩ original text layer ∩ rendered page — the two
  >   text layers are complementary here: the body font keeps letters and drops digits, the
  >   *table* font keeps digits and drops letters). Both ruled tables re-cut with
  >   `camelot lattice`; `pdf2md`/docling added as a fourth leg across all 17 pages (whole-doc
  >   runs OOM'd; `pdfseparate` + one page at a time got through) and agrees throughout.
  >   **All 17 pages read against their rendered image; nothing
  >   unrecoverable.** Curated capture: `sources/p2-eval-board/complete-p2-eval-board-reference.md`.
  >   Two things only the rendered page could give: the edge-header **pin order** (in no text
  >   layer at all), and that the boot-mode switch columns are the silkscreen triangles
  >   **P59 △ / P59 ▽** — OCR reads them as the letters "A"/"V".
  > - **Downstream re-verified.** `sources/p2-eval-board/p2-eval-board-rev-c-complete-extraction-audit.md`
  >   (its false "100% across the board" replaced by measured coverage) and
  >   `sources/p2-eval-board/p2-eval-board-cross-source-analysis.md` (which had described a
  >   board with a barrel jack, a proto area and VGA/HDMI — none of it in the source).
  >   `engineering/ingestion/README.md:51` no longer reads `100% (stated)`.
  > - **The general lesson is now an instrument, not a note.**
  >   `engineering/tools/validation/audit-extraction-digit-density.py`, wired into
  >   the `ingest-source` skill (agent-side) **§2a as a mandatory pass-1 gate** (plus the
  >   pass-1 convention list, the §7 hand-back, and *What NOT to do*). Corpus sweep
  >   `--all`: **clean, 53 artifacts**, 4 hand-written folder descriptions exempted by name
  >   with reasons. Negative control: the archived lossy artifact scores 1.5% and exits 1.
  > - **Spot-check of the other board/hardware sources: `p2-eval-board` was the only
  >   outlier** (10% against 29–58% across eleven peers). **This is not a clean bill of
  >   health for the other eleven** — digit density catches *total* numeral loss, never
  >   partial. It is a smoke alarm.
  >
  > **What is still owed, and by whom:** the #64000 board YAML itself. Re-verification found
  > claims the repaired source contradicts or does not contain — filed separately as
  > **F-328**, and repaired by the sprint's purge/repopulate tasks, not here. The ingestion
  > head is done with this one.
  >
  Status: `DONE` (2026-10-05: KB half closed under F-328) — ingestion half complete 2026-08-24; the KB-side re-derivation it
  exposed is carried by F-328.

- **F-251 — the "why do the LEDs glow when I touch a pin" explanation must account for the
  LED BUFFER, and the freshly-shipped DeSilva v3.0.5 aside does not.** — `DONE` (verified 2026-10-05 «#386»: shipped in deSilva v3.0.9) · The #64000 guide
  (feature 12) and both Edge module YAMLs describe the onboard LEDs as **buffered** — the P2
  pin drives a buffer *input*, and the buffer drives the LED. DeSilva v3.0.5's new Chapter 1
  aside "Why Your LEDs Glow When You Touch Them" instead explains the effect as microamps
  coupling *through the LED itself*, which would produce a faint glow. On a buffered board
  the floating **buffer input** picks up the coupling and the buffer drives the LED at full
  strength — which matches the reader's actual report ("the leds will light up", not "glow
  faintly"). The aside's conclusion (floating pins have no opinion; drive them or use
  pull-ups) is right; the mechanism is wrong. **→ manual head:** correct the aside in the
  next DeSilva patch. Also worth stating there that on the #64000 **P58-P63 are shared with
  the USB-data and memory signals**, so those LEDs are active at power-up and after reset by
  design — a second, entirely non-mysterious reason a reader sees lit LEDs.

  > **EVIDENCE BASE MOVED 2026-08-24 by the «#294» uncited-block purge — read before citing.**
  > This finding's premise says *"the #64000 guide (feature 12) and **both Edge module YAMLs**
  > describe the onboard LEDs as buffered."* **The Edge half of that is no longer true of the
  > KB.** The purge removed `pin_mapping` from both Edge module YAMLs, and with them every
  > `led_buffered` entry; `buffer` now matches nothing LED-related in either file (only
  > unrelated "framebuffer" prose).
  > **What still stands, and is the stronger citation anyway:**
  > `hardware/p2-eval-board.yaml:27` `type: "Buffered LED bank"` and `:29` `buffer: "Driven
  > through an LED buffer that isolates them from the I/O signals"` — inside the
  > `built_in_peripherals` block, which survived the purge *and* carries a real `source:` line
  > (`:45`) naming the #64000 Rev C Guide feature 12. The P58-P63 shared-signal point this
  > finding also wants stated is at `:31-34` (`power_at_startup`), same block, same citation.
  > So the manual fix is **not blocked** — cite the eval-board file, not the Edge files. If the
  > buffered-LED fact is wanted for the Edge modules specifically, it is «#307» repopulation
  > work, source-first from the Edge module guides.

  > **RE-MEASURED 2026-08-25 («#301»). The mechanism half was ALREADY FIXED — and the sentence this
  > finding called "right" is the one that was wrong.**
  >
  > **What was already done, on 2026-08-17.** Commit `a0fb4884` (*"DeSilva v3.0.5: the LEDs are
  > buffered — correcting the aside I shipped hours ago"*) rewrote the Ch.1 aside. It now teaches
  > exactly the buffered mechanism this finding asked for — *"Your P2 pin doesn't feed the LED
  > directly; it feeds the *input* of a buffer… It takes very little to push that floating input past
  > the buffer's threshold, and when it crosses, the buffer switches: the LED doesn't glimmer, it
  > comes **on**"* — and it carries the P58–P63 shared-signal point this finding also wanted, as a
  > second, non-mysterious cause. Nothing was owed on the mechanism.
  >
  > 🔴 **What was NOT done, and was a live defect until today.** This entry ends by saying *"the
  > aside's conclusion (floating pins have no opinion; drive them or use pull-ups) is right."*
  > **The pull-up half is not right, and the aside shipped it**: `COMPLETE-OPUS-MASTER.md:294` read
  > *"If you want a pin held at a known level **without driving it**, the P2 gives you pull-ups and
  > pull-downs for exactly that."* The P2 has **no bias resistors at all** — `P_HIGH_*`/`P_LOW_*`
  > select **drive strength**, and per the Pin Mode Legend a drive selection is live **only while DIR
  > is high** (`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:41-43`, `:166-171`,
  > sourced to P2 Datasheet 2022/11/01 p.24). So the sentence was wrong twice over: it invents a
  > component, and its "without driving it" framing is the exact inversion F-322 exists to kill.
  > This entry predates that determination, which is why it blessed the sentence.
  >
  > **Fixed, and used as the teaching moment rather than deleted** — the reader is standing in front
  > of a floating pin, which is the best possible moment to learn this: *"…if you are reaching for the
  > pull-up resistor you would have switched on somewhere else — there isn't one. The P2 has no bias
  > resistors at all. What it has instead is a choice of *how hard to drive*: the same `drvh`, but
  > through 15 kΩ rather than through a fast transistor, if you ask for it (Chapter 14)… a weak drive
  > is still a drive, so `dir` stays high either way."* Chapter 14 verified as the manual's smart-pin
  > /`WRPIN` chapter (`:4614`). The wording is aligned to the KB's `weak_high` idiom
  > (`pin-drive-configuration.yaml:203-222`) rather than inventing a third form.
  >
  > **Cross-checked and deliberately left alone:** `COMPLETE-OPUS-MASTER.md:2881` ("Common I/O
  > Gotchas" #2) already says *"**No pullup/pulldown by default** — Use external resistors or
  > configure smart pin modes"*, which is **correct**. The two sites disagreed with each other; now
  > they do not.
  >
  > **Owed to «#302»/release:** page-level confirmation of the reflowed `::: sidetrack` in Ch.1, then
  > release. The eval-board citation this entry recommends is re-verified live at
  > `hardware/p2-eval-board.yaml:109-111` (`type: "Buffered LED bank"`, `pins: "P56-P63 (one LED per
  > pin)"`) and `:124` (P58–P63 shared with USB data and P2 memory signals) — note both moved from
  > the `:27`/`:29`/`:31-34` this entry recorded.

  Status: `DONE — mechanism fixed 2026-08-17; the pull-up sentence this entry called "right" was wrong and is fixed 2026-08-25 («#301»); shipped in deSilva v3.0.9 (verified 2026-10-05)`.

- **F-252 — the Getting Started guide hardcodes `LED = 56` with no board caveat (same class
  as the DeSilva fix).** — `DONE` (verified 2026-10-05 «#386»: shipped in Getting Started v1.0.4) · `p2-getting-started-guide/opus-master/getting-started-body.md:558`
  declares `LED = 56  ' the pin our LED is on`, used by the blink examples at `:493` and
  `:408`. On a **P2 Edge 32MB PSRAM Module** P56 is the PSRAM **clock** — the example lights
  nothing and drives the memory bus; the LEDs there are **P38/P39**. This is exactly the
  failure a reader hit this session, and it lands in the guide most likely to be a
  newcomer's *first* P2 program. **Fix:** one line naming the per-board LED pins (the
  DeSilva Ch.1 aside is the model, but Getting Started wants a single sentence, not a
  sidetrack). Sources now in the KB: `hardware/edge-standard-module.yaml` (P56/P57),
  `hardware/edge-32mb-module.yaml` (P38/P39), `hardware/p2-eval-board.yaml` (P56-P63,
  P56/P57 free). **→ manual head.** Surfaced by the v1.16.2 YAML→Manual impact survey.

  > **TWO OF THE THREE NAMED SOURCES MOVED 2026-08-24 («#294» uncited-block purge). The fact
  > survives; the addresses changed.** Verified line by line against the post-purge files:
  > - `hardware/edge-32mb-module.yaml` (P38/P39) — **gone from this file entirely.** The purge
  >   removed its `pin_mapping` block (which held `led_buffered: 2  # P38-P39` and the P38/P39
  >   pin entries) and its `boot_modes` block (which held the `LED:` DIP-switch line naming
  >   P38/P39). `P38`/`P39` now match **nothing** in that file.
  > - `hardware/edge-standard-module.yaml` (P56/P57) — **survives, at a new address.** Its own
  >   `pin_mapping` went too, but the `comparison_with_32mb` block was not flagged and stands:
  >   `:158` `led_pins: "P56, P57"` and `:164` `led_pins: "P38, P39"`. That single surviving
  >   block now carries **both** boards' LED pins, so it alone can source the whole caveat.
  > - `hardware/p2-eval-board.yaml` (P56-P63, P56/P57 free) — **survives untouched** at `:28`
  >   (`pins: "P56-P63 (one LED per pin)"`) and `:31-34`, inside the cited
  >   `built_in_peripherals` block.
  >
  > **The manual fix is not blocked** — every pin number the caveat needs is still in the KB.
  > Cite `edge-standard-module.yaml:158,164` for the Edge pair and `p2-eval-board.yaml:28` for
  > the eval board. When «#307» repopulates `edge-32mb-module.yaml`, P38/P39 must come back
  > there source-first; until it does, do not cite that file for this fact.

  > **APPLIED 2026-08-25 («#301») — and the "do not cite that file" warning above is now STALE, which
  > is why every locator was re-verified on disk before use rather than copied from this entry.**
  >
  > **`edge-32mb-module.yaml` has been repopulated.** The 2026-08-24 annotation says P38/P39 *"match
  > **nothing** in that file"*. Today they match plenty, source-first as required: `:140-141`
  > (`P38: "Buffered LED"`, `P39: "Buffered LED"`), `:165` (`pins: "P38, P39"`), `:201` (the `LED`
  > DIP switch), all under a real `source:` at `:175` naming *P2-EC32MB Edge Module Rev B Guide v2.0,
  > §7 LED Buffer and §8 LEDs P38 and P39*. So the per-board file **is** citable again and was cited.
  > The other two locators also moved: `edge-standard-module.yaml:145` (`pins: "P56, P57"`, now with
  > its own `warning:` at `:146-148` — *"DIFFERENT PINS from the P2-EC32MB module… Confusing the two
  > puts an LED write on a PSRAM data line"*) and `p2-eval-board.yaml:110`
  > (`pins: "P56-P63 (one LED per pin)"`).
  >
  > **The PSRAM claim was verified, not assumed:** `edge-32mb-module.yaml:137` reads
  > `"P56": "PSRAM CLK (Common)"`. So `LED = 56` on that board really does drive a memory clock line.
  >
  > **Fix, in the shape this finding specified** — one bullet, not a sidetrack — added to the bullet
  > list under the first runnable program in `getting-started-body.md`: *"**One board check before you
  > run it.** `56` is the LED pin on a P2 Eval Board and on the standard P2 Edge Module, but the **P2
  > Edge 32MB Module** puts its two LEDs on **P38 and P39** — and P56 there is a PSRAM clock line, so
  > as written this program would light nothing and write to the memory bus instead. Change `LED` to
  > match your board."*
  >
  > **The code block was deliberately NOT touched.** It is captioned `ch03-blink-led.spin2`, so it is
  > byte-identity-paired to an example file; changing `LED = 56` there would have broken that pairing
  > and made the guide's first program board-specific in a different direction. The caveat is prose
  > beside the listing, which is what this finding asked for. `sync-manual-examples.py --check`
  > reports **no** "BODY differs" for the guide, so the pairing is intact. The other `LED = 56` sites
  > (`:339` skeleton, `:644`, `:704`, and `LED_A = 56` at `:603`) are left alone on purpose: the
  > caveat belongs once, at the first program a newcomer actually runs.
  >
  > **Owed to «#302»/release:** confirm the added bullet sets on the page, then release.

  Status: `DONE — caveat added to opus-master 2026-08-25 («#301»); shipped in Getting Started v1.0.4 (verified 2026-10-05)`.

---

## Forum docs-feedback (2026-08-16) — the DDS LUT is not fixed at 512 entries — F-302

**Origin:** Christof Eb., Parallax forum 2026-08-16, reviewing the *P2 Streamer Programming
Guide* §17.2. Raw post + full analysis at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-260819/` (gitignored — find it
by path). Same reviewer as F-256. His parenthetical *"(No, it does not need to be 512
entries.)"* is **correct**, and it lands on the KB as well as the manual.

### F-302 — `p2kbArchDdsGoertzel` states the DDS/Goertzel LUT window as a flat `entries: 512`, hiding a selectable 8-way loop size, a bounded-region offset, and a phase-offset field. `RESOLVED 2026-08-22 — KB applied 2026-08-21; the manual half shipped in Streamer Guide v1.1.0`

> **MANUAL HALF SHIPPED 2026-08-22, Streamer Guide v1.1.0 (91pp).** §10.3 "LUT Window" is
> a new section carrying all eight loop sizes with the `%A` region bits and the `%T` phase
> offset, and §17.2 was rebuilt on top of it — the flat "must contain 512 entries" claim is
> gone from the manual as it is from the KB.

> **KB APPLIED 2026-08-21.** All six sites. `entries: 512` is now `entries_default` plus an
> `entries_note` saying it is the %000 case, beside a `lut_window:` block carrying all eight
> loop sizes with their NCO index bits and LUT ranges, and named `capabilities` for the two
> things the %A and %T bits actually buy — bounded sub-regions and phase offset/modulation.
> `s_operand.field_11_0` is split into `field_11_9` (loop-size selector) and `field_8_0` (%A/%T),
> quoting Silicon Doc :4093-4095 verbatim. `operation.steps.1` no longer states NCO[30:22] as a
> general rule. The two `repeat i from 0 to 511` loops are correct FOR the %000 case and now say
> so rather than reading as the only option. **The table and the quote were re-read out of
> `p2-documentation.txt:4058-4095` before being written, not copied from this register.**

**Location:** the DDS/Goertzel architecture YAML behind P2KB key `p2kbArchDdsGoertzel` —
`lut_setup.entries: 512` and `s_operand.field_11_0: "loop size + LUT window"`.

**What is wrong.** `entries: 512` reads as a hardware requirement; it is only the `%000` case.
`field_11_0` names the field but carries none of its content, so nothing downstream can use it.
The KB is *not false* here in the way the manual is (the manual says "**must** contain 512
entries"), but it is thin in exactly the place the manual went wrong, and it is what a
downstream author would consult.

**Evidence — Silicon Doc `sources/silicon-doc/p2-documentation.txt:4062-4092`, verbatim table:**

| `S[11:0]` | Loop Size | NCO Bits | LUT Range |
|---|---|---|---|
| `%000_TTTTTTTTT` | 512 | 30..22 | `%000000000..%111111111` |
| `%001_ATTTTTTTT` | 256 | 30..23 | `%A00000000..%A11111111` |
| `%010_AATTTTTTT` | 128 | 30..24 | `%AA0000000..%AA1111111` |
| `%011_AAATTTTTT` | 64 | 30..25 | `%AAA000000..%AAA111111` |
| `%100_AAAATTTTT` | 32 | 30..26 | `%AAAA00000..%AAAA11111` |
| `%101_AAAAATTTT` | 16 | 30..27 | `%AAAAA0000..%AAAAA1111` |
| `%110_AAAAAATTT` | 8 | 30..28 | `%AAAAAA000..%AAAAAA111` |
| `%111_AAAAAAATT` | 4 | 30..29 | `%AAAAAAA00..%AAAAAAA11` |

and (`:4093-4095`, verbatim): *"On each clock, the lookup RAM is read at the 9-bit location
bound by the %A bits, with the lower bits being the sum of the %T bits and the topmost NCO
bits. This allows you to set bounded areas within the LUT and to shift or modulate the phase of
playback."*

**Proposed correction.** Replace `lut_setup.entries: 512` with a `lut_window:` block carrying
the eight loop sizes and their NCO index bits; expand `s_operand.field_11_0` into the three
sub-fields — loop-size selector `S[11:9]`, `%A` region-bound bits, `%T` phase-offset bits — and
state the two capabilities the Silicon Doc names explicitly: **bounded LUT sub-regions** (more
than one waveform resident at once) and **phase offset / modulation**. Keep `entries: 512` only
as the `%000` default, labelled as such.

**Why it matters beyond the correction.** The guide's §17.2 headline applications are
"Function generator, audio synthesis, **RF modulation**" — and the field that does modulation is
the one neither the KB nor the manual documents.

**Additional YAML sites found by the 2026-08-20 class-wide sweep — these are part of F-302, not
separate findings.** The correction above named `lut_setup.entries` and `s_operand.field_11_0`
only; the sweep found the same assumption stated four more times in the same file:

| `architecture/streamer/dds-goertzel.yaml` | What is wrong |
|---|---|
| `:57` | `operation.steps` step 1 — `"Read LUT entry at NCO[30:22]"` as an **unconditioned general rule**. This is the KB twin of the manual's §10.2 defect and was **missing from this finding's original correction text.** |
| `:89` | `' Build 512-entry sine/cosine table` (code example) |
| `:100` | `repeat i from 0 to 511` in the `sinc2_amplitude` example |
| `:227` | `usage_pattern.data` comment restating `512-entry LUT window` as fact |

Sibling files verified **correct** and usable as the fix template: `dds-goertzel.yaml:11,:18`
(`%1111_0ppp_p111` / `%1111_1ppp_p111`, with the correct `D[22:19]` multiple-of-four caveat).

**Downstream (manual head, not a YAML edit):** *Streamer Guide* §10.2 `:648`
(`LUT[NCO[30:22]]` stated as the general rule), §10.3 `:674` ("must contain 512 entries" —
**false**), §17.2 tip `:1458` ("the 512 entries"), the `:1424` code comment ("512-entry LUT
window"), and the `\DiagDdsGoertzel` diagram in
`workspace/p2-streamer-programming-guide/templates/p2kb-streamer-diagrams.sty` (which renders
`entry = LUT[NCO[30:22]]`) — plus its **cloned copies** at
`workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:207` and the staged
`pdf-forge/interactive-testing/templates/p2kb-torture-diagrams.sty:207`. Tracked in
`engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md`; fix ships with that release.

---

## Class-wide sweep of the Streamer findings — the same errors live in OTHER artifacts (2026-08-20) — F-303…F-309

**Origin.** The Streamer Guide's 2026-08-19 class audit produced four confirmed factual errors.
Sweeping them across every manual, app note, `deliverables/ai/P2/`, and workspace diagram template
found them **outside** that manual as well. Recorded here — **not** scoped into the Streamer
sprint, which is deliberately confined to its own document. **Stephen decides at that sprint's
release gate whether the affected artifacts co-release.** Full sweep detail + the verified-correct
list: `engineering/planning/STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §13.

> **Before fixing any of these, read the "verified correct" list in that plan section.** The sweep
> deliberately separated look-alikes: the Assembly Manual's Appendix G **ADC Sampling Modes** and
> **DDS/Goertzel** *constant-value* tables were decoded row by row and are **correct** — they are
> named-symbol value tables, not field-encoding templates. Do not "fix" them.

### F-303 — the RGBI8 `2:2:2:2` fabrication is in a second released manual and in two live KB files. `RESOLVED 2026-08-22 — every released and live-KB site corrected; KB 2026-08-21, Assembly v3.1.7`

> **CLOSED 2026-08-23.** Both live-KB sites applied 2026-08-21 (`2:2:2:2` re-swept 2026-08-23:
> **zero** occurrences in `deliverables/ai/P2/`), and the Assembly Language Reference's site
> shipped in v3.1.7 and was read on p475 of the returned PDF. **The fourth row of the table below
> is NOT a correctness finding and never gated this one**: the P2 Layout Torture Test is an
> internal test instrument, never released and not consistency-bound (roster: *"serves the manual
> layout-standards effort, not the community"*). Its stale `\DiagRgbFormats` clone is recorded as
> instrument-local housekeeping in `PUNCH-LIST.md`, not as pending correction work — an instrument
> must never hold a published-artifact finding open.

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** p475 prints *"Read byte as color + intensity: P[7:5] selects the color, P[4:0] is the intensity"*, and `2:2:2:2` appears **zero** times in 505 pages. The LUMA8 row beside it now reads *"the color is selected by S[2:0]"*.


> **Assembly fixed 2026-08-22 (v3.1.7).** `appendix-g-streamer-constants.md:115` now reads *"Read byte as color + intensity: P[7:5] selects the color, P[4:0] is the intensity"*, with a paragraph above the table contrasting RGBI8 against LUMA8. Sourced live from Silicon Doc `p2-documentation.txt:3800`, which also shows the colour table has **eight** entries — so the old row was wrong on the colour count as well as the field split.

> **KB APPLIED 2026-08-21.** `streamer-symbols.yaml:186` and `modes-reference.yaml:221` both now
> read *"upper 3 bits select a colour, lower 5 bits are intensity"*, the framing the released
> Debug Window Manual v1.1.3 already uses. Swept: `2:2:2:2` no longer appears anywhere in
> `deliverables/ai/P2/`. *(Still-owed list as written on 2026-08-21, both since discharged:
> `appendix-g-streamer-constants.md:115` shipped in Assembly v3.1.7, and the torture-test clone
> is instrument-local — see the CLOSED note above.)*

The truth (Silicon Doc `p2-documentation.txt:3800`): RGBI8 is a **3-bit colour select + 5-bit
luminance** format, structurally the same as LUMA8. It has no per-channel R/G/B fields.

| Location | Status |
|---|---|
| `manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:115` — *"Read byte as RGBI 2:2:2:2 (16 colors + intensity)"* | **RELEASED** — Assembly Language Reference v3.1.6, 2026-08-18, 502pp |
| `deliverables/ai/P2/language/spin2/symbols/streamer-symbols.yaml:186` — `"RFBYTE → RGBI 2:2:2:2"` | **LIVE KB** (served by `p2kb-mcp`); the one wrong row in an otherwise-correct table |
| `deliverables/ai/P2/architecture/streamer/modes-reference.yaml:221` — same description, second copy | **LIVE KB** |
| `workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty:176` — `\DiagRgbFormats` cloned, draws `R 2 \| G 2 \| B 2 \| I 2` | **NOT A FINDING SITE** — internal test instrument, never released. Housekeeping only; tracked in `PUNCH-LIST.md` |

**Fix template already exists, in a released manual:** *P2 Debug Window Manual* v1.1.3
`ch04-bitmap.md:100` — *"Upper 3 bits select a color, lower 5 bits are intensity"* — and it
contrasts RGBI8 against LUMA8 immediately above. Copy that framing.

### F-305 — the Assembly Manual teaches a streamer DAC example without the pin-setup step. `RESOLVED 2026-08-22 (v3.1.7)`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** The Audio DAC example on p480 carries `COGID` / `SETNIB` / `WRPIN` / `DIRH`, and its routing reads `X_DACS_X_X_X_0` — one channel for a one-channel mode.


> **Fixed 2026-08-22 (v3.1.7).** The "Audio DAC Output" example now carries the full `cogid` / `setnib` / `wrpin` / `dirh` sequence per F-272, and the example compiles under `pnut-ts` v1.55.3.
>
> **A second defect in the same example, not in the original enumeration:** the mode was `X_RFBYTE_1P_1DAC1` — one DAC channel — routed with `X_DACS_3_2_1_0`, which the appendix's own table defines as four channels. Now `X_DACS_X_X_X_0`. Fixing the pin setup alone would have shipped a half-corrected example.

`manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-g-streamer-constants.md:237`
shows `mov mode, ##X_RFBYTE_1P_1DAC1 | X_DACS_3_2_1_0` with no `WRPIN` DAC-mode configuration and
no `DIRH` — the same omission the Streamer sprint fixes book-wide. **RELEASED** in Assembly
Language Reference v3.1.6.

Per **F-272** (resolved 2026-08-20) the correct setup is now fully citable: `%TT = %01`
(`P_CHANNEL`) with the COGID in `M[3:0]`, `DIRH` the pin, channel selected by the pin's two low
bits. `deliverables/ai/P2/architecture/streamer/dds-goertzel.yaml:203` carries a worked example,
and `wrpin.yaml:54` documents the field.

**Note the asymmetry that makes this easy to get wrong** — and note the half of it that was itself
wrong until 2026-08-20. The **`WRPIN`** part applies to **DAC** output only: ordinary digital pin
output via `X_PINS_ON` (`D[23]=1`) needs no DAC mode, no COGID and no channel, so do not add *mode*
setup to digital-output examples. But it **does** need `DIRH` like any driven pin — `X_PINS_ON`
enables the streamer's contribution to the pin's output *state*, never its output *enable*. See
**F-308** / **EF-062** (bench-proven: DIR low 4-of-8, `DIRH` 8-of-8). The citation this note used to
carry, `Silicon Doc :3602-3603`, resolves to nothing in `engineering/ingestion/` and has been dropped.

### F-308 — "digital pin output through `X_PINS_ON` requires no `DIRH`" is wrong: the streamer feeds the pin's output STATE, and DIR is still the output ENABLE. `RESOLVED 2026-08-22 — Streamer bench-sealed (EF-062), Assembly shipped in v3.1.7`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** `DIRH` appears **8 times** across Appendix G (pp.471-482): all four usage examples, the `HARDWARE` callout carrying the EF-062 numbers, and the control-flag prose. The no-`WRPIN` half survives intact.


> **Assembly fixed 2026-08-22 (v3.1.7).** All three example sites now `DIRH` their pins, and a `::: hardware` callout under the control-flag table states the state-vs-enable distinction with the EF-062 numbers. The **no-`WRPIN`** half is preserved.
>
> **Two sites the enumeration missed**, both glossing `X_PINS_ON` as *"Enable pin outputs"* — `appendix-g-streamer-constants.md:203` and `part-i/chapter-05-hardware.md:347`. Source-faithful to the Silicon Doc's encoding wording, and the exact phrasing that installs the wrong model in a reader; both now say the streamer drives the pin's output *state*.

**How it surfaced.** Two bench runs of the VO-J-003 rig (2026-08-20, logs in that rig's `logs/`).
Its digital self-test drove `DAC_PIN` through `X_PINS_ON` with DIR left low — on the strength of the
claim below — and scored **4 of 8** then **3 of 8** toggles, i.e. the pin was never driven and the
readback was float noise. Going to the primary source to explain it produced this finding.

**Locations (both live):**
- `engineering/document-production/manuals/p2-streamer-programming-guide/opus-master/streamer-body.md:834`
  — a `::: hardware` callout in §11.0: *"Ordinary pin output through `X_PINS_ON` drives the pin bus
  directly and requires no `WRPIN` and no `DIRH`."* **RELEASED in Streamer Guide v1.0.9**; v1.1.0 is
  in its correctness sprint now.
- `engineering/operations/P2KB-CORRECTION-FINDINGS.md:251` — F-305's closing note repeats the claim
  as guidance ("Do not add pin setup to digital-output examples") and cites `Silicon Doc :3602-3603`.
  **That citation does not resolve** to any extraction in `engineering/ingestion/`.

**What the primary source actually says.** *Parallax Propeller 2 Documentation v35 (Rev B/C
Silicon)*, text extracted from the shipped `.docx`:
- STREAMER section: *"Modes which can output to pins OR the streamer pin-output bus **with {OUTB,
  OUTA}** to produce the final 64 pin **output states** on each clock for the cog. For these modes,
  %e in D[23] must be '1' to enable pin output."*
- SMART PINS section: *"Normally, an I/O pin's **output enable is controlled by its DIR bit** and its
  **output state is controlled by its OUT bit**, while the IN bit returns the pin's read state."*

The streamer's pin data is OR'd into the **output state** — the OUT side. Nothing in the document
gives the streamer any authority over the output **enable**. The one documented way to drive a pin
with DIR low is the smart-pin `%TT` field (*"the %TT bits … will govern the pin's output enable,
regardless of the DIR state"*), and `X_PINS_ON` digital output uses no smart pin. So `DIRH` **is**
required, and D[23] enables the streamer's contribution to OUT, not the pin's driver.

**The "no `WRPIN`" half is correct** and should survive the fix — no smart-pin mode is needed. Only
the "no `DIRH`" half is wrong. Note the internal tension the claim already had:
`streamer-body.md:796`, twenty-eight lines earlier in the same section, states the general rule
correctly — *"**`DIRH`** on the pin. Until DIR is high, the pin does not drive."*

**Proposed correction.** Rewrite the §11.0 callout so it separates the two: digital output needs no
`WRPIN` (no DAC mode, no COGID, no channel), but it does need `DIRH` like any driven pin. Fix
F-305's note in the same pass and drop or replace its unresolvable citation.

**SEALED ON SILICON 2026-08-20 → EF-062.** VO-J-003's run 3 ran the A/B: the same streamer command
with DIR low and then `DIRH`, the `DIRH` leg starting from `OUT`=0 so a pass proves the streamer
overrode `OUT`. *Result:* `D1` plain drive (no streamer) **8 of 8** · `D2` DIR low **4 of 8** · `D3`
`DIRH` **8 of 8**. The prediction and its falsifying outcome ("if `D2` passes, reverse F-308") were
written into the program before the run; the bench was free to reverse this and did not.

**The class — the book is inconsistent with itself, and the majority of it is already right.**

*Correct, do not touch:* `streamer-body.md:796` ("Until DIR is high, the pin does not drive") ·
`:1490` the §15.2 HDMI program, which does `drvl #7<<6 + HDMI_BASE` · `:2038` the troubleshooting
checklist, "Pins configured as outputs (DRVH/DRVL as needed)" · `:623`, `:816`, `:1767` (ADC, DAC,
DDS pin enables).

*Wrong prose — **FIXED 2026-08-20**:* `:834` the §11.0 callout (rewritten: keeps "no `WRPIN`",
adds what `DIRH` is for and what a DIR-low streamer command looks like on a bench) · `:410` §5.2's
"the pin columns need none".

*Code blocks that omitted the pin enable — **ALL FIXED 2026-08-20** («#289»):*
- `:405` `X_IMM_32X1_LUT` (32-pin) -> `drvl ##31<<6` · `:435` `X_IMM_4X8_1DAC8` (8-pin) ->
  `drvl #7<<6 + pin` · `:470` `X_RFLONG_4X8_LUT` (32-pin) -> `drvl ##31<<6 + base` ·
  `:497` `X_RFBYTE_8P_1DAC8` (8-pin) -> `drvl #7<<6 + base`. Span forms compiled before use.
- §16.1 SPI — the configuration block set up `spi_clk` and never touched `spi_do`, the pin the
  streamer drives. Fixed earlier the same day.
- **§15.1 VGA — rebuilt.** It carried **four** defects, not the one this finding named, and they
  were fixed in a single edit rather than four passes: (1) no §11.0 DAC-pin setup at all for the RGB
  channels; (2) `VGA_BASE` undefined; (3) `framebuffer` undefined; (4) **a 640×480 framebuffer at
  16 bpp is 600 KB and hub RAM holds 512 KB** — the program could not have existed as written. It
  now declares `VGA_BASE = 16` (a multiple of 4, so each pin's low two bits pick its own DAC
  channel), does the §11.0 setup (`COGID` into `M[3:0]`, `P_CHANNEL`, `DIRH`) across a 4-pin span,
  and paints 350 lines into a declared `orgh` framebuffer while blanking the rest of an unchanged
  525-line field — the same trade §15.2's HDMI program already makes for the same reason (§7.1).
  **Extracted from the manuscript and compiled: 452,096 bytes**, matching §15.2's block exactly.
  The compiler caught a collision the new `CON` introduced — P2 symbols are case-insensitive, so a
  `VSYNC_PIN` constant clashed with the `vsync_pin` register; the constant was dropped.

*Not touched, and correctly so:* the §7.3 RGB pattern block already carries a `**Pattern**` label
and points at §11.0 for its DAC pins.

**Why the sweep was routed rather than done at filing time.** It was folded into «#289» and run
alongside «#280», the pass that reads every code block, so that one hand added the missing line to
every block under one contract. Routing inside a sprint, not deferral across a release — none of it
ships until v1.1.0. The failure mode being avoided is the one «#282» records: "the finding named a
row, the fix corrected a row, nobody swept the table." Worth noting that the sweep *earned its keep* —
it found §15.1 carrying four defects where this finding had named one, and a fifth `pin<<17` site
(`:435`) that the original enumeration missed.

**Sprint impact.** This is sprint decision #4 ("Digital ≠ DAC. `X_PINS_ON` needs NO wrpin/dirh"),
which later tasks were told to respect. **That decision is now half wrong and must not be applied as
written.** Surfaces at the Streamer v1.1.0 co-release gate («#288») with F-302…F-307.

**Status:** `RESOLVED 2026-08-22 — BOTH halves complete and validated on their returned PDFs.` The
Assembly Language Reference's sites shipped in **v3.1.7** and were read on the page: `DIRH` appears
8 times across Appendix G (pp.471-482) — all four usage examples, the `HARDWARE` callout carrying
the EF-062 numbers, and the control-flag prose — while the no-`WRPIN` half survives intact. The
enumeration named three sites; two more carried the same wrong model as a gloss
(`appendix-g:203`, `part-i/chapter-05-hardware.md:347`) and were corrected in the same pass.
The v1.1.0 PDF was read at «#287»
2026-08-21 and the §11.0 callout renders as the corrected split — *"X_PINS_ON requires no WRPIN: no
DAC mode, no COGID, no channel… What digital output still needs is DIRH. X_PINS_ON enables the
streamer's contribution… Until DIR is high, the pin does not drive."* The no-`WRPIN` half survived,
the no-`DIRH` half is gone, exactly as EF-062 sealed it. Still owed:
`part-iii/appendix-g-streamer-constants.md:228/:255/:289`, RELEASED in v3.1.6.

---

## F-413's 300 MHz maximum also stood in the P2AN004 companion, which F-413 never looked at (2026-09-11) — F-426

### F-426 — `p2an004`'s `measurement_ceiling` gave 300 MHz as the P2's maximum — `RESOLVED — fixed 2026-09-11`

Found while VALIDATING block G's edit to an adjacent line of the same file — the reviewer's eye
landed one line below the change. `p2an004-frequency-rotation-rc-timing-measurement.yaml:90` read:

> `runs at a legal 200 MHz (300 MHz max)`

F-413 already adjudicated this exact claim in P2AN001 and ruled it plainly: *"300 MHz appears in
no source we hold and in no KB file. The datasheet maximum is 320 MHz."* F-413 was scoped to
P2AN001's markdown and its own companion; **it never looked at P2AN004's companion**, so the same
number survived one file over.

**The trap worth recording: `300 MHz` IS genuinely sourced — three times — just never as a maximum.**
A sweep that had matched the string and deleted it would have destroyed correct content:

| site | what it says | verdict |
|---|---|---|
| `edge-standard-module` / `edge-32mb-module` / `p2-eval-board` / `p2-hardware-feature-comparison` | quotes Parallax's feature list, *"Overclocking possible beyond 300 MHz"* | **correct — keep** |
| `special-configuration-symbols.yaml:97` | *"The P2 Datasheet rates direct drive into XI at DC to 200 MHz MAXIMUM ... The compiler accepts 300 MHz beyond that"* | **correct — keep** |
| `timing_operations.yaml:44,:200` · `spin2-getting-started.yaml:63` | 300 MHz as an example `clock_freq` | **correct — a usable value, not a claimed ceiling** |
| `p2an004:90` | 300 MHz as **the maximum** | **the defect** |

So the defective thing is not the number, it is the *role* the number is given. This is the
confidence-source mismatch shape (`feedback_titus_trust_tier_representation`) in numeric form:
an overclocking threshold and a compiler ceiling promoted to a silicon specification.

**Fixed in the same pass**, per no-deferring: the line now states 200 MHz against the datasheet's
actual PLL range (180 MHz typical, 320 MHz maximum, AC Characteristics) and names what 300 MHz
really is, so the figure cannot be promoted back.

**Class check run, not assumed:** the four sites above were each read and left alone, and no other
shipped file gives 300 MHz as a maximum.

---

## F-374's class survives under three key names the sweep was scoped not to touch (2026-09-11) — F-425

### F-425 — `cost_efficiency`, `production_readiness: "excellent"` and two prose lines carry the same unsourced quality judgement F-374 removed — `RESOLVED — fixed 2026-09-11, same day as filing`

Found 2026-09-11 by the F-374 sweep itself. F-374 was deliberately scoped to five key
shapes, because an earlier pass matching the bare key `value` returned 299 sites and was
thrown out as over-broad. That boundary was correct and it is also why these survived: they
are the same defect wearing key names the narrowed class did not name.

**(a) `cost_efficiency` — 6 sites, all `hardware/hardware-compatibility-matrix.yaml`**

```
cost_efficiency: "optimal"                    :55
cost_efficiency: "underutilized"              :62
cost_efficiency: "professional_premium"       :69
cost_efficiency: "acceptable_but_oversized"   :76
cost_efficiency: "optimal_memory_solution"    :83
cost_efficiency: "expensive_overkill"         :90
```

Both of F-374's tests fail here. **Nothing sources it** — no Parallax document grades a
board's cost efficiency, and we hold no price data at all. **The consumer cannot act on
it** — an agent choosing a board cannot do anything with `expensive_overkill`; it needs the
pin count, the memory and the price, and the first two are already in the same row.
`expensive_overkill` is not a borderline call: it is an opinion about someone else's
product, shipped as knowledge-base fact.

**(b) `production_readiness` — 2 of 6 sites, and the split is the point**

`"prototype_platform"` (:167 breakout, :254 carrier, :200 mini) and `"not_applicable"`
(:243 eval board) are **categorical facts** — they say what the board is FOR, which is
utility and stays. `"excellent"` (`edge-standard-module.yaml:397`,
`edge-32mb-module.yaml:527`) is a grade and carries nothing a consumer can use. Fix only
the two; do not touch the four.

**(c) two prose lines, `hardware/p2-eval-board.yaml:224-225`** — these are the
REPLACE-WITH-THE-FACT case rather than the delete case:

```
beginners: "Ideal - no hardware selection needed"
educators: "Perfect - built-in teaching aids"
```

The adjective is the defect; the clause after the dash is a genuine fact. Strip `Ideal - `
and `Perfect - ` and keep the rest.

**Why this is filed rather than swept.** The F-374 task carried an explicit scope boundary —
*do NOT widen this sweep* — because the over-broad version of it had already been thrown out
once. Widening on my own authority would have re-made that mistake; the register is where a
newly-recognised member of a class goes (`feedback_corrections_routed_only_via_register`).

**Scope when this is worked:** the three shapes above ONLY, re-derived at the time. Do not
re-open the bare-`value` class — 299 sites, overwhelmingly legitimate utility.

---


**FIXED 2026-09-11, hours after filing — and the filing itself was the error.**

Stephen: *"If we find problems, we're supposed to get them out to the agents as soon as possible.
If you file it, we're not doing that."* Correct. `p2kb-mcp` serves the PUBLISHED tree, so a filed-
but-unfixed defect reaches nobody; filing is how a defect waits, not how it ships.

**Why it was wrong, precisely.** F-374's task carried a *do not widen this sweep* bar, and that bar
existed to stop a blind sweep of a class that was mostly LEGITIMATE — an earlier pass matching bare
`value` returned 299 sites and was discarded. It never forbade fixing sites already verified one by
one, and all three shapes here HAD been verified before this entry was written. "Do not widen
blindly" was read as "do not fix what you have proven."

**What was done:**

| site | disposition |
|---|---|
| `hardware-compatibility-matrix.yaml` — `cost_efficiency` ×6 | **deleted.** Every row already states `module_free_pins`, `carrier_header_pins` and `use_case`; the grade sat directly beneath the facts that would have justified it. |
| `edge-standard-module.yaml` · `edge-32mb-module.yaml` — `production_readiness: "excellent"` ×2 | **deleted**, together with the literal `# QUALITY RATINGS` banner heading them. `memory_class: "high_capacity"` kept (a fact) and its banner relabelled `CLASSIFICATION`. |
| `p2-eval-board.yaml` — `target_audience` | **adjective stripped, fact kept** — e.g. *"Ideal - no hardware selection needed"* → *"No hardware selection needed -- board, USB and power are one part"*. |

**The filing undercounted, which is its own lesson.** This entry named TWO prose lines; there are
**FOUR** (`professionals` and `production` carry the same shape), and it did not notice that the
`production_readiness` sites sat under a `# QUALITY RATINGS` banner that was itself the defect's
home. Both were found by opening the files to fix them. A finding written from a grep is a map, not
an inventory.

**The four surviving `production_readiness` values are NOT this defect and were deliberately kept:**
`"prototype_platform"` (×3) and `"not_applicable"` state what the board is FOR. That is utility,
which the rule permits. Only `"excellent"` was a grade.

**Verified:** class sweep returns only the known-legitimate survivors (the 32 A / 400 V terminal
spec, the four categorical `production_readiness` values, and the `educational_value` facts block);
no `QUALITY RATINGS` banner remains anywhere; `verify-yaml-format` 1133/1133 clean; crossref 100%;
`validate-dod-release` 12/12 PASS.
## The rights guard fails open, so an unadopted document emits a malformed rights string (2026-08-22) — F-319

### F-319 — `p2kb-platform-foundation.sty`'s pdfkeywords guard does not fire for a document whose `\Doc*` macros are at their defaults, so it emits `"; licensed under "` instead of nothing. `DONE — closed 2026-09-11 (token normalised 2026-10-05 «#386»); the negative control FAILED the 2026-09-10 fix and exposed the real cause (`@` at catcode 12); completed fix proven on the artifact in all four branches`

**How it surfaced.** The Assembly Language Reference v3.1.7 render (2026-08-22) came back with
`Keywords: "; licensed under "` — the both-values-present branch, with both values empty.

**Proven from the artifact, not inferred.** That exact string is what
`\hypersetup{pdfkeywords={\DocCopyright; licensed under \DocLicense}}` produces when both macros
expand to nothing. For it to be emitted at all, **both** `\ifx` tests must have taken their
not-empty path — so the guard did not fire.

**The guard (`:332-350`) and the defaults (`:288-299`):**

```latex
\providecommand{\DocCopyright}{}       % and \DocLicense, \DocTitle, ...
...
\ifx\DocCopyright\@empty ... \else ... \fi
```

The comment above it claims *"a document that has not adopted these keys writes no pdfkeywords at
all, exactly as before, so an unconverted document is unchanged rather than given a malformed
rights string."* **The artifact falsifies that claim.**

**Hypothesis for the mechanism — NOT proven, no TeX engine in this container.** `\providecommand`
routes through `\newcommand`, which defines a `\long` macro; `\@empty` is `\def\@empty{}` and is
not `\long`. `\ifx` compares the prefix as well as the body, so `\long macro:->` never tests equal
to `macro:->`. Plausible and consistent with the evidence, but **verify before relying on it**
(`EXEC_ENV_CANONICAL` has the engine).

**Proposed fix — correct under EITHER explanation**, because it normalises by full expansion rather
than depending on how the default was declared:

```latex
\AtBeginDocument{%
  \edef\P@rc{\DocCopyright}\edef\P@rl{\DocLicense}%
  \ifx\P@rc\@empty ... \fi
}
```

**Blast radius.** Every document that loads the platform foundation and has **not** wired the seven
`\renewcommand{\Doc*}` lines into its own `*-reference.latex`. Per
`PLATFORM-FEATURE-ADOPTION.md` that is every row except Streamer, Single-Step Debugger and now
Assembly — so **~14 documents**, each at its next render. Assembly is simply the first unadopted
document to render since the foundation gained this code, which is why it had not shown before.

**Why not fixed in v3.1.7 (explicit carve-out).** Assembly's own template is now wired, so its
rights emit correctly and this release ships clean — the defect is genuinely separable and is not
holding the quality bar for this document. Fixing it means editing a **shared** file that all 18
documents load, using an idiom that **cannot be tested in this container** (no TeX engine), while a
manual is mid-render. Landing it blind risks breaking rights emission for Streamer and the
Single-Step Debugger, which are proven working today.

**A LIVE VICTIM, found 2026-08-22 — and FIXED the same day, before it rendered.**
`pnut-term-ts-user-guide` was about to render for its v1.0.0 release with five of the seven `\Doc*`
macros bound and neither rights macro, and no `copyright`/`license` in its `request.json` either —
so it would have emitted the malformed `"; licensed under "` exactly as Assembly's first v3.1.7
render did. Both halves are now wired (template 7/7; `request.json` carrying
`"Copyright 2026 Iron Sheep Productions, LLC"` + `"CC BY-SA 4.0"`, the one ISP-alone document in
the set). Detail in `PLATFORM-FEATURE-ADOPTION.md` footnote ¹².

**The mechanism hypothesis above is now believed CONFIRMED by reading, though still not executed.**
`\providecommand` routes through `\newcommand`, which defines a **`\long`** macro; `\@empty` is
`\def\@empty{}` and is not `\long`. `\ifx` compares that prefix as part of the meaning, so
`\ifx\DocCopyright\@empty` can never be true for a macro declared this way — the guard takes the
both-present branch **every** time, for **every** unadopted document. That is consistent with the
only artifact evidence in hand (Assembly's `"; licensed under "`). Still unexecuted: no TeX engine
in this container. `EXEC_ENV_CANONICAL` has one.

**Consequence of fixing the victim:** the pool of available negative controls shrank again. Neither
Assembly nor PNut-Term-TS can serve — an adopted document never takes the guarded branch, so it
proves nothing. The **Layout Torture Test** is now the only candidate named for this purpose. A fix
to the shared guard must be validated by rendering an *unadopted* document and confirming the
returned PDF carries **no** Keywords at all.

**What it needs instead — and this is the point:** its own change, with a **negative control** that
Assembly can no longer provide. Render an *unadopted* document (the layout torture test is the
natural candidate) and confirm the returned PDF carries **no** Keywords at all. A fix validated only
against an adopted document proves nothing, because an adopted document never takes the guarded
branch. (`a gate must read the artifact`; `prove with a negative control`.)

---

**FIX LANDED 2026-09-10 — commit `44c29ba8`, riding the P2AN001 v1.0.5 bundle.** The `\edef`
normalisation proposed above, verbatim: the guard now tests `\edef`'d copies (`\DocRightsHolder`,
`\DocRightsGrant`), which are not `\long`, so the comparison means what it says regardless of how
the default was declared. The stale comment claiming an unconverted document is "unchanged" was
replaced with the mechanism and this finding's evidence.

**Why it landed here rather than waiting for its own change.** The carve-out reasoning above was
sound in August and expired: the fixed `.sty` had to travel to the Forge's manual store with SOME
bundle, and P2AN001 was the next one out. Holding a corrected shared file in the repo while the
store keeps the broken one is the drift that produced this evening's other failure (the app-note
template staged with P2AN002 while P2AN001 built first). The repo does not run ahead of the store.

**POSITIVE control — PROVEN on the returned artifact, 2026-09-10 23:37.** P2AN001 v1.0.5 rendered
with the changed foundation and came back with
`Keywords: "Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed under CC BY-SA 4.0"`,
`audit-pdf-metadata.py` CLEAN, all seven declared fields round-tripped. So the risk named in the
carve-out — *"landing it blind risks breaking rights emission for Streamer and the Single-Step
Debugger, which are proven working today"* — is **retired**: the adopted branch is unchanged, and
that is now measured on a real PDF rather than argued. The remaining seven documents in this
release wave are all adopted and will each re-confirm it.

**NEGATIVE control — STILL OWED. This finding is not closed.** An adopted document never enters
the guarded branch, so P2AN001 proves nothing about the half that was broken. The requirement
above stands unchanged: render an **unadopted** document and confirm the returned PDF carries
**no** Keywords at all. Candidates, verified 2026-09-10 as declaring no `copyright`/`license` in
their `request.json`: `p2-layout-torture-test` (the named candidate, and the cheapest — an
instrument, no release attached), `p2-architect-guide`, `p2-debug-window-manual`,
`p2-xbyte-programming-guide`, and app notes P2AN003 / P2AN005 / P2AN006 / P2AN007. Whichever
renders first settles it; until one does, the fix is proven safe but not proven effective.

---

**NEGATIVE CONTROL RUN 2026-09-11 — IT FAILED, and that is why it existed.** The Layout Torture
Test (unadopted, no `\Doc*` bound — confirmed by reading the generated `.tex`: zero `\Doc*`
mentions, zero `\hypersetup`) was rendered on the interactive Forge daemon against the **fixed**
`p2kb-platform-foundation.sty`. It came back with `Keywords: "; licensed under "` — **the same
malformed string the fix was supposed to eliminate.** The `\edef` normalisation alone does not
close F-319.

**Root cause, read off the machine rather than argued.** A `\typeout` probe placed in the guard
reported:

```
F319-PROBE: catcode-of-at-HERE = 12          <- @ is OTHER at this line
F319-PROBE: DocCopyright = [\long macro:->]   <- the \long diagnosis WAS correct
F319-PROBE: holder       = [macro:->]         <- the \edef DID strip \long
F319-PROBE: atempty      = [macro:->\spacefactor \@m {}empty]
F319-PROBE: holder-NOT-empty
```

That last reading is the whole finding. `\@empty` was never denoting the kernel's empty macro.
The guard sits **below** the file's line-166 `\makeatother` and **above** its line-425
`\makeatletter`, so `@` is catcode 12 there and `\@empty` tokenises as the control sequence `\@`
followed by the four letters `e m p t y`. Every test was therefore `\ifx<macro>\@` — comparing a
rights value against LaTeX's end-of-sentence macro — which is false for anything, forever. The
stray `empty` characters caused no visible damage only because they fall inside the branch `\ifx`
then skips; page-1 text is byte-identical before and after.

**Both halves are required, and that is measured, not reasoned.** A control run with
`\makeatletter` but *without* the `\edef` still emitted `"; licensed under "` (`holder-NOT-empty`),
because `\ifx` does compare the `\long` prefix. So the 2026-09-10 fix was necessary and
insufficient; the completed fix wraps the block in `\makeatletter` … `\makeatother` **and** keeps
the `\edef`.

**COMPLETED FIX — all four branches proven on returned PDFs, 2026-09-11.** One template stack, four
renders, 54pp each, compile log 0 serious signatures:

| binding | Keywords in the returned PDF | verdict |
|---|---|---|
| neither (unadopted) | *(none at all)* | **NEGATIVE control PASS** |
| both | `Iron Sheep Productions, LLC; licensed under CC BY-SA 4.0` | PASS |
| copyright only | `Iron Sheep Productions, LLC` | PASS |
| license only | `CC BY-SA 4.0` | PASS |

The two single-value branches had been **unreachable for the entire life of this code** — the
broken guard always fell to the both-present branch — so this is their first execution ever. They
were exercised deliberately for that reason, not for completeness.

**No released document was harmed.** All 17 PDFs in `deliverables/documents/DOCs/` were read:
**0** carry the malformed string, 10 carry correct rights, 7 carry none because they were rendered
before the rights block existed. Those 7 are precisely the unadopted set — each was one render away
from shipping `"; licensed under "`, which is what the negative control was protecting.

**Class-wide sweep — the same `@`-catcode defect, 4 more live sites.** A checker over every
template in the tree found `\providecommand{\subtitle}[1]{\gdef\@subtitle{#1}}` (and the
`\institute` / `\titlegraphic` siblings) sitting outside any `\makeatletter` region. With `@` at
catcode 12 that parses as `\gdef\@` with delimiter text `subtitle`, which would **globally clobber
LaTeX's `\@`** rather than define `\@subtitle`. Latent, not live — nothing reads `\@subtitle`, and
no current template emits `\subtitle{...}` — but one pandoc template variable away from firing.
Wrapped at all live sites: `p2kb-platform-foundation.sty`, `donna-book-foundation.sty`,
`p2kb-ssdbg.latex`, `p2kb-pnut-term-ts.latex`, plus the orphan `p2kb-foundation.sty` copies under
`ai-privacy-guide` and `spin2-reference-manual`. **Deliberately NOT touched** (recorded as a chosen
gap, not an accidental one): the archived `templates-archived/*MONOLITHIC.latex` pair and the three
superseded shared `p2kb-foundation.sty` copies under `templates/shared/` and `shared-assets/` —
nothing loads them; no live template does `\usepackage{p2kb-foundation}`.

**The lesson this finding paid for twice.** The August entry above reasoned its way to a mechanism
(`\long`), was upgraded to *"believed CONFIRMED by reading, though still not executed"*, and shipped
on that reading. The reading was correct **and the fix still did not work**, because a second
defect sat in the same three lines and no amount of reading the macro semantics could see it — only
the catcode could, and only a real engine reports the catcode. *A mechanism confirmed by reading is
a hypothesis; only the artifact closes it.*

## Appendix G's mode tables misdecode the naming convention the same appendix documents (2026-08-22) — F-318

### F-318 — 31 of 36 streamer mode-table rows state a wrong pin count, a wrong DAC-channel count, or both, and every usage example in the appendix cannot run as printed. `RESOLVED 2026-08-22 (v3.1.7)`

> **VALIDATED on the returned v3.1.7 PDF, 2026-08-22 (505pp, read on the page).** Appendix G grew 9pp -> 12pp (pp.471-482) and **that +3 is the manual's ENTIRE page delta** — no other section moved. The decode rule now opens the appendix; all 36 rows read correctly; the four rebuilt examples print with `SETXFRQ`, an OR-ed `D[15:0]` count and `DIRH`. `SETLUTS`-for-streamer-LUT and *"Appendix F (Streamer Mode Constants)"* both appear **zero** times. Column separation measured: tightest constant->value gap **+14.1pt**, so the v3.1.5 overlap class is absent.


**How it surfaced.** Fixing F-303's single row in `appendix-g-streamer-constants.md` and then re-deriving the
rest of the table from the artifact instead of trusting the enumeration. **The register named one wrong row in
that file; thirty-one more were wrong.** Fourteenth instance of the class — see the F-304 note.

**The rule (Silicon Doc `part2-pixel-ops.txt:139-227`).** Every streamer mode is listed as `<n>-pin + <k>-DAC<b>`
— *n pins, k DAC channels, b bits per channel* — under column headers reading literally `Pins | DAC Channels`.
Appendix G's own "Mode Naming Convention" stated the same rule: *"`_nP` Number of pins used · `_nDACn` Number of
DAC channels, bits per channel."*

**The defect.** Every description read `kDACb` as *"k pins, b DAC channels"* — the channel count taken for a pin
count, the bit width taken for a channel count. Where the name carried an explicit `nP`, the description
**ignored it**. `X_RFBYTE_8P_2DAC4` — 8 pins, 2 channels at 4 bits — printed as *"2 pins, 4 DAC channels"*.

| Table | Rows | Wrong |
|---|:--:|:--:|
| Immediate to Pins/DACs | 12 | 11 |
| RDFAST Byte Operations | 9 | 8 |
| RDFAST Word/Long | 3 | 2 |
| WRFAST Operations (capture) | 12 | 10 |
| **Total** | **36** | **31** |

**The `Value` column was correct throughout** — every encoding checks out against the Silicon Doc. The bits were
right and the prose describing them was wrong, which is why nothing downstream caught it.

**Root cause is layout, and the fix addresses it.** The naming convention sat **180 lines below** the tables that
needed it, so whoever wrote the descriptions did not have the decode rule in view. It now **opens** the appendix,
names `_kDACb` as the field that gets misread, and works three same-pin-count examples (`8P_1DAC8` / `8P_2DAC4` /
`8P_4DAC2`) that can only be told apart by decoding it correctly.

**Found in the same pass, same file:**

- **`X_RFBYTE_LUMA8` was described as grayscale.** Silicon Doc `part2-more-content.txt:48`: *"LUMA8 mode uses
  three bits in S[2:0] as colors and the 8-bit pixels as luminance values."* The colour comes from the `XINIT`
  **S operand**. FABRICATED, and the exact mirror of F-303: LUMA8 takes its colour from S, RGBI8 from the pixel.
- **All four Usage Examples could not run as printed.** Each put a frequency in `XINIT`'s `S` operand — which is
  mode-specific data, not the rate (`SETXFRQ` owns that) — and none set `D[15:0]`, so the transfer count was
  zero and the streamer stops immediately. All four rebuilt and compiled under `pnut-ts` v1.55.3.
- **`SETLUTS #0` was captioned *"Use LUT for color palette"*.** `SETLUTS` enables LUT **sharing between adjacent
  cog pairs** and has nothing to do with streamer LUT lookup; `#0` is its *disable* value (Silicon Doc `:995-1000`).
  A fabricated claim attached to a real instruction. Removed — the streamer LUT modes need no enabling
  instruction, only the palette present in lookup RAM.
- **The ADC sampling modes never named their prerequisites** — `SETSCP` to point the SCOPE pipe at a four-pin
  block, and an ADC smart pin mode on each sampled pin (Silicon Doc `:3968-3977`). Same missing-setup class as F-305.
- **`D[22:20]` (pin group, 8-pin increments, "in every mode" — `:3606`) and `D[15:0]` (transfer count) were
  documented nowhere**, though every constant leaves both at zero.
- **`X_PINS_ON` and `X_WRITE_ON` print the same value** and were presented as two unrelated flags. They are one
  bit, `D[23]`, read by the mode's direction (`%e` / `%w`, `:3602-3604`).
- **Chapter 5 §5.3.4 pointed at "Appendix F (Streamer Mode Constants)"** — Appendix F is *Smart Pin* Mode
  Constants; the streamer appendix is G. A broken cross-reference in a released manual. It also claimed "78 mode
  constants" (there are 79); the count is now gone rather than maintained, per the perishable-catalog rule.
- **§5.3.4 also described mode families that do not exist** — *"NCO mode uses data as frequency control words, RF
  mode uses data as modulation patterns."* `RF` is Read-from-FIFO; there is no NCO mode. FABRICATED.
- **The front matter named four appendices differently from their own titles** (A, D, I, J) — the reader's first
  navigation page disagreeing with the pages it indexes.

**A correction to the sweep plan's own caveat.** `STREAMER-GUIDE-CORRECTNESS-SPRINT-PLAN.md` §13 carried a
completeness note that *"neither table discloses that setting `D[19]` selects the other four-pin block."*
Checked live against the Silicon Doc, that is wrong on both halves: `D[22:19]` is a **four-bit block number**
(base pin = number x 4) and it belongs to **DDS/Goertzel only** (`:3997`) — the ADC sampling modes take their
block from `SETSCP` instead. The caveat was carried into a draft of this fix and removed before it shipped.
**Verify a ledger claim against the live source before writing it into a manual.**

**Verified correct and deliberately untouched:** the ADC Sampling Modes table (decodes `kDAC8` correctly), the
DDS/Goertzel constant values, and the RDFAST-to-LUT encodings — all re-checked row by row this pass.

## The whole app-note companion set is version-frozen (2026-08-16) — F-271

### F-271 — every `application-notes/*.yaml` companion still carries its maiden `version:` while the note it ships with has moved on, so an agent cannot tell which edition it holds. `RESOLVED — DECIDED 2026-08-16 (Stephen); the KB has one edition, so the field is deleted rather than maintained. Carried to PUNCH-LIST.md PL-004; its "Sprint 2 first" gate discharged when Sprint 2 closed 2026-08-19, and PL-004 parts 1 + 3 are being worked now.`

**Surfaced by:** the F-270 content probe against the published MCP. The corrected SINC2 line came
back live and correct — sitting four lines under `version: "1.0.0"`, in a companion to a note that
is at **1.0.3** and going to 1.0.4.

**The defect, across all seven:**

| Companion | `version:` | Note's released version (roster) |
|---|---|---|
| p2an001-single-pin-instrumentation-adc | `1.0.0` | **1.0.3** (→1.0.4 in the wave) |
| p2an002-cordic-for-real-work | `1.0.0` | **1.0.2** |
| p2an003-dac-analog-signal-generation | `1.0.0` | **1.0.2** |
| p2an004-frequency-rotation-rc-timing-measurement | `1.0.0` | **1.0.2** |
| p2an005-cooperative-multitasking-tasks | `0.1.0` | **1.0.2** |
| p2an006-sizing-cog-task-stacks | `0.1.0` | **1.0.1** |
| p2an007-data-structures-new-facilities | `1.0.0` | **1.0.1** |

**Seven for seven — so this is the convention failing, not a missed file.** The stamp has never been
advanced by any release.

**Why it matters — and the severity claim this entry first carried was WRONG, corrected 2026-08-16
on Stephen's challenge ("why are there version numbers in the yaml?").**

The original text said a frozen stamp is *"worse than absent, because an agent that caches by version
sees no change and keeps serving the stale body."* **Nothing caches by version.** Checked, not
assumed: the published index carries exactly `path`, `mtime`, `sha256` per entry — change detection
is the git commit timestamp plus a content hash, both of which updated correctly when F-270 shipped.
A consumer mechanism was asserted without being verified, which is this sprint's own named failure
mode. **The field is inert.**

**What is left is real but smaller:** the stamp misleads anyone who *reads* it — a human opening the
file, or an agent quoting `version` when citing the companion. P2AN001's was edited twice this sprint
(F-269, F-270) and still reads `1.0.0`. It is a truthfulness defect in shipped metadata, not a
cache-correctness defect. **Priority drops accordingly** — this is not urgent, and it is certainly
not worth a bulk edit of seven published files.

**The deeper finding, which is the actual reason to keep this entry.** `version:` appears in only
**24 of 1129** published YAMLs, carrying **two unrelated meanings** under one key name, with no
schema doc defining either (`APP-NOTE-DESIGN-DECISIONS.md`, which the companion header cites as its
schema authority, does not mention `version` at all):

| Population | What `version:` means there | Tell |
|---|---|---|
| **17 files** — `architecture/smart_pins.yaml` (1.2), `architecture/streamer/_index.yaml` (2.0), `spin2/conventions/*` (1.0.0–2.0.0), `guides/*` | **the file's own content revision** | almost always paired with `last_updated:`; refers to nothing outside the file |
| **7 app-note companions** | positioned as **the note's** version — sits under `doc_id:` and above `kind: application-note`, beside the note's `title`/`subtitle` | no `last_updated:` |

**So "which meaning is right" has no documented answer, and the tree's majority reading is the
opposite of the one this entry first recommended.** That recommendation was made from the app-note
files alone, before the other seventeen were looked at.

**This is F-270's rule showing up structurally.** F-270 established that *an app-note correction is
not complete until its YAML companion carries it.* The companion here **did** carry the content — and
still shipped a false edition stamp. So the rule needs its second half: **the companion ships under
the note's version, and that stamp is advanced at release, not at edit.**

**Deliberately NOT swept.** Two things need Stephen's decision before any edit:
1. **Semantics.** Does `version:` mean *the note's version* (then all seven get stamped and it becomes
   a `release-manual` step) or *the companion's own schema/content revision* (then it needs renaming
   to say so, and a separate `note_version:` added)? The files carry no comment either way. Guessing
   here and sweeping seven published files is exactly the F-211 failure mode — a class-wide sweep
   amplifying an ungrounded reading.
2. **Whether it is a KB bump at all.** These are published `deliverables/ai/P2/` files, so any stamp
   change ships in a KB release; but the *natural* moment to advance them is each app note's own
   release. Those two cadences are not the same and the answer decides which skill owns the step.

**Ask the prior question first: what is this field FOR?** (Stephen, 2026-08-16: *"how is that version
useful to agents?"*) Worked through honestly, **a bare `version:` is of no use to an agent**:

- It is **not** how change is detected — that is `mtime` + `sha256` in the index, and they work.
- It is **not** how content is selected — an agent fetches by key and gets exactly one body. There is
  no version negotiation, no second edition to choose between, no `1.0.3` still on the shelf.
- It **cannot** be compared against anything the agent holds, because the agent has no prior copy.
- A stamp only earns its place if something can be **checked against** it. `1.0.4` next to nothing is
  a number an agent can only quote — and quoting it is precisely how a stale one does harm.

**What would actually serve an agent** is the *note's* version — not as a bare number, but as the
answer to a question an agent really has: *"the PDF in front of the user — does this digest match
it?"* That makes the useful field an explicit, self-describing link to the human artifact
(e.g. `describes_document: {doc_id: P2AN001, version: 1.0.4, released: 2026-08-16}`), which a
reader can compare against the cover of the PDF they are holding. The bare `version:` key answers no
question and, worse, reads as the *file's* version to anyone applying the tree's majority convention.

**Revised recommendation — cheaper and more honest than the original.** Do **not** stamp the seven
files with note versions and add a fourth version location to maintain. Instead:
1. **Delete the bare `version:` from the seven companions** — it is inert, ambiguous, and currently
   false. Removing a field that answers nothing beats maintaining it in seven places forever.
2. **If** the match-the-PDF question is worth answering, add the explicit `describes_document:`
   block in its place, stamped by `release-manual` alongside the roster row and cover/`request.json`
   — one self-describing field, not a number whose meaning must be inferred.
3. Leave the **17 non-app-note** files alone; there `version:` + `last_updated:` is a coherent
   file-revision convention. Worth documenting, not changing.

**Note the reversal:** this entry originally recommended stamping all seven to track the note. That
was written from the app-note files alone, before the other seventeen or the index schema were
looked at, and it would have institutionalised the ambiguity rather than removing it.
[[feedback_drop_techniques_that_lower_quality]] — when a shape keeps producing defects, remove the
shape rather than add a rule to maintain it.

**Status:** `RESOLVED — DECIDED AND PUNCH-LISTED (2026-08-16)`. **Do not re-file, do not work it now.**

**Stephen's decision supersedes both recommendations above, including the revised one.** The
principle is broader than this field: **the published KB has exactly one edition — the current one —
so nothing in the tree should cite currency or a version at all.** Every reference means *latest*.
That rules out the `describes_document:` block too; it is still a currency citation, just a
better-labelled one. **Delete the shape rather than maintain it.**

**Deferred deliberately, not forgotten** — *"we are trying to get to released documents, and we are
not there yet given our task list. We should stay away from any diversions at this point in time."*
Sprint 2's release wave comes first.

> **PL-004 PARTS 1 AND 3 EXECUTED 2026-08-21.** The "Sprint 2's release wave comes first" gate
> discharged when Sprint 2 closed 2026-08-19. **Part 1:** the bare `version:` is deleted from all
> seven companions. **Part 3:** 25 build stamps rewritten plus the stale `version_info` block in
> `tools/pnut-ts-compiler.yaml` (which read v1.51.5, four minor versions behind) removed. The
> dividing line applied throughout — **cite the EDITION, never the BUILD**: `Spin2 v55`,
> `Added in PNut v47`, `{Spin2_v54}`, `minimum_version:` are facts about the LANGUAGE that a
> reader can hit, and all 278 survive untouched; `compile-verified with pnut_ts v1.55.0` is a
> record of what someone happened to run, and is gone. The seven app-note `toolchain:` lines were
> EDITED, not deleted — their `-d` requirement, `_clkfreq` and `{Spin2_v45}` gating are durable
> and load-bearing; only the `1.55` clause went. **Part 2 (the other 17 `version:`/`last_updated:`
> bearers) remains open** and still needs the per-population decision PL-004 requires; it was
> deliberately not swept on the app-note reading.

**Carried to → `engineering/tools/p2kb-mcp/PUNCH-LIST.md` PL-004**, which holds the full scope
(7 companions to strip; the other 17 `version:`/`last_updated:` bearers to review per-population,
NOT to sweep on the app-note reading; prose "as of" sweep; PDF versioning explicitly out of scope).

---

## IOSP suppressed-qualifier probe (2026-08-16, «#230») — F-274…F-275

> **Method and full result:** `engineering/analysis/2026-08-16-iosp-suppressed-qualifier-probe.md`.
> The probe asked whether a qualifier was ever **never written** — the half no diff can see, after
> «#214» returned NIL on qualifier *removal*. Result is **not nil**: two findings, both in Ch.19,
> the one chapter our own `KNOWLEDGE-GAPS.md` already flags as OPEN (G-005).
>
> **The pattern is the useful part, and it inverts hedge-counting.** Ch.16 (ADC) — the chapter that
> qualifies most — is right, and says so explicitly (*"nominal resolution … not ENOB"*, *"a
> mechanism, not a guaranteed specification"*, *"never a datasheet value"*). Ch.19 — the chapter
> that qualifies least — is the one with the gap. The guide is well calibrated where its evidence
> is rich, and goes quiet about its own uncertainty exactly where the evidence is thinnest. The
> signature to look for is a missing **dependency**, not a missing **word**.
>
> **Neither finding ships in the current wave.** IOSP left it when F-261 reversed into F-269, so
> both wait for IOSP's next release rather than being force-fitted into this one.

### F-274 — IOSP Ch.19 §19.4 teaches an FS-USB configuration at exactly the clock its own source flags, and states no sysclk dependency anywhere. `DONE — corrected in opus-master 2026-08-25 («#301»); shipped in IOSP v1.0.11 (verified 2026-10-05 «#386»)`

**Location:** `manuals/p2-io-and-smart-pins-user-guide/opus-master/part-4-special-modes/chapter-19-usb.md:122-128`.
**RELEASED (v1.0.8).**

The chapter's only worked baud example computes full-speed (12 Mbps) USB at **80 MHz**.
`engineering/ingestion/KNOWLEDGE-GAPS.md` **G-005 is OPEN**: *"Scope of smart-pin USB support;
documented sysclk floor (**FS-USB > 80 MHz**, LS-USB less)."* The chapter states **no sysclk
dependency for USB anywhere** — not in §19.4, not in §19.9 Limitations, not in the Quick Reference.
A reader following the worked example lands on the boundary the open gap is about with nothing to
tell them a boundary exists.

**Do NOT "fix" this by asserting the floor.** G-005's only source is a reviewer comment (Granville)
on the Titus document — an **upstream lead, not a citation**, and not something to carry into
reader-facing prose as fact. Doing so would trade a silence for an unsourced claim.

🟢 **NEW EVIDENCE 2026-08-24 (`KNOWLEDGE-GAPS` pass-6 catch-up) — the correction is no longer
stuck between a silence and an unsourced number.** The DOCX-primary **P2 Hardware Manual @
2022/11/01** *does* state a sysclk dependency for USB, authoritatively and quantitatively:
the baud field is a 16-bit fraction of the system clock "whose two MSBs must be 0, **necessitating
that the baud rate be less than 1/4th of the system clock frequency**", with a worked 12 MHz-at-80
MHz full-speed example (`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1489`).
That is a citable hardware constraint the chapter can state on its own authority. It is **not** the
Granville floor and must not be presented as one — the > 80 MHz claim stays unsourced (`Q-003`),
and G-005 stays `PARTIAL` for exactly that reason.

**Proposed correction:** rework the worked example at a clock unambiguously clear of the question
(the chapter's own Spin2 example at `:264` already runs at 200 MHz), and state the **documented**
dependency — baud < sysclk/4, cited to the Hardware Manual — while saying the practical floor for
reliable FS signaling is unsettled. §19.4's existing transmit-pacing `::: caution` is the shape to
copy — it already names its own limit correctly.

**Not in scope of this finding:** the register-layer content (WXPIN config word, WYPIN line states,
the 16-bit RX status word, per-pin IN semantics) is properly sourced to Silicon
`p2-documentation.txt:8886-9006` and was verified sound during the probe. It is not implicated.

> **APPLIED IN OPUS-MASTER 2026-08-25 («#301») — RENDER OWED, so this is NOT closed.**
> All three legs of the proposed correction are in
> `…/opus-master/part-4-special-modes/chapter-19-usb.md`:
> - **The worked example moved off the boundary.** §19.4's baud example now computes 12 Mbps at
>   **200 MHz** — the clock the chapter's own Spin2 example (`:264`) and Quick Reference already
>   use — giving `$0F5C` and a host WXPIN word of `$CF5C`. Arithmetic re-derived on disk, not
>   copied: `12_000_000 / 200_000_000 × $10000 = 3932 = $0F5C`; `$C000 | $0F5C = $CF5C`.
>   The old 80 MHz / `$2666` / `$E666` figures were correct *as arithmetic* (they are the Hardware
>   Manual's own worked example) — they were removed because the clock, not the maths, was the
>   defect.
> - **The documented dependency is now stated WITH its citation**, which it was not: the ¼-`clkfreq`
>   ceiling is attributed in-text to the *P2 Hardware Manual* 2022/11/01 §*USB Host/Device
>   (%11011)*. Verified live at `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1489`
>   — *"a 16-bit fraction of the system clock, whose two MSBs must be 0, necessitating that the baud
>   rate be less than 1/4th of the system clock frequency."*
> - **The unsettled floor is named as unsettled, and carries no number.** A new `::: caution`
>   ("Clearing the ÷4 rule is not the same as having enough clock") says the ÷4 ceiling is the only
>   sysclk dependency any Parallax source states, that full speed clears it above 48 MHz — which is
>   that stated rule applied to the stated 12 Mbps, not a new claim — and that **no published source
>   settles what full-speed work needs in practice**. The Granville *> 80 MHz* figure is **not**
>   carried, in line with this finding's own instruction and `Q-003`.
> - **Discoverability fixed too**, which was half the complaint: the dependency was absent from
>   §19.9 and the Quick Reference, so a reader scanning limitations never met it. §19.9 gains a
>   **Clock Requirements** subsection and §19.10 a Key Points bullet, both pointing back at §19.4.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` both exit 0 on
> the chapter (each proved able to fail on a negative control the same session). **No code block was
> touched** — the one edited line inside a fence is the ` ```formula ` block, which pairs to no
> example file — so byte-identity is untouched and `pnut-ts` does not apply.
> **Owed to «#302»:** confirm on the rendered page that the new `::: caution` and the §19.9
> subsection set, and that the reflowed §19.4 does not push the following table. `G-005` stays
> `PARTIAL` and `Q-003` stays open; neither is this finding's to close.

### F-275 — IOSP Ch.19 §19.5 states the P2 provides USB bus power; §19.8 correctly says it does not. `RESOLVED — verified IN THE RELEASE TAG 2026-08-25 («#301»), not inferred from this entry`

**Location:** `…/chapter-19-usb.md:210` against `:329`. **RELEASED (v1.0.8).**

`:210` — *"As a USB host, the P2: **Provides bus power (5V)**"*. The P2's I/O is 3.3 V and it
sources no 5 V rail. `:329` correctly lists *"5V power supply for VBUS"* among the external
components a host design must provide.

A plain factual error, self-contradicted two sections later. Not a calibration defect — surfaced by
the same read-the-claims pass, and recorded here rather than split off because it was found by the
probe and belongs with its record.

**Proposed correction:** §19.5 says the P2 *initiates* communication and *requires* a board-supplied
5 V VBUS rail, pointing at §19.8 for the external components.

**RESOLVED 2026-08-17 («#246»).** The bullet is out of the P2-verb list — it never described anything
the P2 does — and the fact it was carrying now stands on its own after the list: a host port supplies
5 V on VBUS, the P2 cannot source it (3.3 V I/O), and §19.8 has the external supply and its current
limiting. Fixed in opus-master; **IOSP is not in the release wave**, so it ships at IOSP's next
release alongside F-278's site conversions.

**ROOT CAUSE, and the fix extended (Stephen, 2026-08-17).** The claim was not invented — **the P2 Edge
breakout boards really do carry 5 V to the I/O headers**, which is almost certainly where "the P2
provides bus power" came from. Removing the wrong sentence without explaining the true one would have
left the next reader to make the same inference from the same board. §19.8 now carries what the board
guides actually say, and it is more specific than "the headers have 5 V":

- Each 8-pin accessory header provides two grounds, a **Vxx** pin (3.3 V from that group's LDO), and
  **optionally** 5 V — **passed straight through from the power jack**, not generated by the board.
- **Two headers have no 5 V routed at all: P24–P31 and P56–P63.** The second bank contains **pins
  56/57, which is the pair this chapter's own examples use** — so the chapter was teaching a host
  design on the one header that cannot supply its VBUS.
- Because the header 5 V is the input supply passed through, it carries no current limit, so §19.8's
  current-limiting requirement still lands on the design.

**Sources (three board guides, consistent):** *P2 Edge Mini Breakout Board* (#64019) §6–§7, *P2 Edge
Breakout Board* (#64029) §6–§7, *P2 Edge Module Breadboard* (#64020) §12–§13 — the last gating header
5 V behind an ACC ON/OFF shunt. The guides anticipate the confusion themselves: *"5V OUTPUT VOLTAGE IS
PROVIDED TO POWER EXTERNAL ACCESSORIES & SENSORS. DO NOT CONNECT 5V DIRECTLY TO ANY OF THE P2 SMART
I/O PINS! ALL I/O PINS OPERATE AT 3.3V LOGIC LEVEL AND ARE NOT 5V TOLERANT!"*

**Class-wide sweep done, and it is clean.** Every other `5 V` mention across all manual and app-note
masters was read: the Architect's Guide (level shifters), deSilva ("P2 is 3.3V, not 5V tolerant"),
IOSP Ch.12 (legacy 5 V logic as an input case), and P2AN004 (the TSL235R's 2.7–5.5 V supply range) are
all correct. **F-275 was the only site** — verified rather than assumed.

**Related — looked at and FIXED 2026-08-17, at the next pass as scheduled.** Pins 56/57 are also the
Edge Module's onboard LED pins and sit in the programming/WX-adapter bank — and the manual itself uses
56 as `LED_PIN` in five places and 57 as `BUTTON_PIN`. Worse, this very release adds the statement
that P56–P63 carries no 5V, so the chapter would have demonstrated a **bus-powered** peripheral on the
one bank with no bus power. §19.8 had absorbed that by adding a caveat — *"the pin pair this chapter's
examples use... must take VBUS from elsewhere"* — which is a workaround for a pin choice, not a
reason for it.

**Chapter 19's examples now use P8/P9**: a free even/odd pair in a 5V-bearing bank, clear of every
other pin constant in the manual. The §19.8 caveat is gone with the need for it, and the bank fact
stands on its own. Verified: byte-identity GREEN 15/15, `ch19-usb-device-config.spin2` compiles clean
under `pnut-ts -d`, all IOSP gates clean. The "Valid pairs" enumeration still lists 56/57 — it is an
enumeration of what the silicon allows, which is unchanged.

**The lesson is the caveat itself.** Prose was written to explain around a defect instead of removing
it, and that prose then read as settled. A sentence that exists only to excuse a choice is a marker
for the choice, not a resolution of it.

> **CLOSED 2026-08-25 («#301») — and the closure was measured against the TAG, because this entry's
> own text is what went stale.** The body above said *"IOSP is not in the release wave, so it ships
> at IOSP's next release"* and then nothing came back when that release happened. It did:
> `git show p2-io-and-smart-pins-user-guide-v1.0.9:…/chapter-19-usb.md` carries **all three** halves
> of the fix — the wrong bullet is gone, the replacement sentence stands at `:214` (*"Bus power is a
> board responsibility, not a P2 one… the P2 cannot source it — its I/O operates at 3.3V"*), and the
> examples are on the 5V-bearing pair at `:54` / `:266` (`USB_DM = 8`). Nothing is owed: master
> fixed **and** shipped. Same drift direction as F-278 — the record understated what had been done,
> which sends the next reader to redo finished work.

**Next finding ID after this block: F-276.**

---

### F-277 — deSilva tells the reader that peripheral conflicts are impossible on the P2. They are not, and our own published manual documents why. `RESOLVED — fixed 2026-08-17, shipped in v3.0.6; the owed class-wide check RUN and CLEAN 2026-08-25 («#301»)`

**Location:** `…/COMPLETE-OPUS-MASTER.md:6045` — *"**64 smart pins** means peripheral conflicts become
impossible"* — and `:5940` — *"I/O flexibility that eliminates peripheral conflicts."*
**RELEASED (v3.0.5)** — both sites are pre-existing body text; neither was touched by any Sprint 2 task.

Smart pins eliminate the **pinmux** conflict: any pin can be any function, so a design never runs out of
"the SPI pins." They do **not** eliminate **resource** conflict. *The P2 Architect's Guide* (v1.0.3,
Ch.7 Force 1) states the opposite from the silicon: P2 pin outputs are OR'd with no hardware arbiter, so
two cogs driving one bus corrupt it — and the symptom "presents as flaky hardware — intermittent,
timing-dependent, and miserable to debug, because the symptom is three layers away from the cause."

This is the most expensive kind of wrong claim: it tells a beginner that a real, nasty bug class cannot
happen, in the manual most likely to be their first contact with the chip. It is also a declared **R1**
violation, whose stated reason is precisely this case — *"a tutorial's worked examples are exactly where
an overstated claim reaches a beginner who cannot yet check it."*

**Proposed correction:** state what smart pins actually remove (the pinmux conflict, and running out of
peripheral blocks) and keep single-ownership of a shared bus as a live concern. **Class-wide check
owed:** the same "conflicts impossible / eliminates conflicts" phrasing may appear in other manuals.

**Related, same pass, same manual — not separately numbered:** `:6042` "eliminates entire categories of
problems"; `:3897` "No surprises, ever / Timing is guaranteed", self-contradicted by the *correct* hedge
at `:5911` (5911 is right); `:3729` "impossible to achieve this precision with interrupts" (F-276's
strawman); `:5804`'s impossibility aside. ⚠️ **The reader-celebration at `:5804` STAYS** — deSilva's
voice guide explicitly protects celebration of reader progress as pedagogy, and an early draft of this
finding wrongly proposed cutting it.

> **CLOSED 2026-08-25 («#301»). Both named sites and all four related sites were fixed on
> 2026-08-17 by `9f4ddb4f` — the commit is literally named *"deSilva voice pass, part 1: F-277 and
> the claims that overreached"* — and shipped in **v3.0.6** the same day. This entry was left saying
> `CONFIRMED` for eight days.** Verified by reading the commit's diff, not by trusting its message:
> `-**64 smart pins** means peripheral conflicts become impossible` → `+ … means no function is ever
> stuck waiting for the one pin that supports it`; `-I/O flexibility that eliminates peripheral
> conflicts` → `+ … and no more shuffling functions around to find pins that support them`;
> `-one that eliminates entire categories of problems` → `+ … one that changes which problems you
> spend your time on`; and the `:3897` / `:3729` absolutes are gone.
>
> **The `:5804` ⚠️ was honoured, and that is worth recording because it is the part a sweep gets
> wrong.** The celebration was **reshaped, not cut**: *"You're not just another embedded programmer
> anymore. You think in parallel. You see solutions that others miss."* survives verbatim; only the
> false-impossibility tail (*"When someone says 'that's impossible in real-time,' you know better"*)
> was replaced, with a move rather than a boast — *"When someone starts sketching an interrupt scheme
> to keep one job on time, you reach for a different move first — give that job a cog of its own."*
>
> **THE CLASS-WIDE CHECK THIS FINDING DECLARED OWED IS NOW RUN, and it is clean.** Swept **every**
> `opus-master/` body and CHANGELOG across all manuals and all seven app notes for
> `conflicts (become) impossible` / `eliminates … conflicts` and, more broadly, for the bare word
> *impossible*: **zero** conflict-impossibility claims anywhere in the P2 set. The only surviving
> `impossible` uses are legitimate — `architect-guide-body.md:101`/`:116`/`:358`/`:959` (a datasheet
> that is hard to find, a hand-wiring limit, a cohesion argument, and a torn read under a
> sequence/**acknowledge** handshake, which P2AN007 R3 `:214` confirms is the load-bearing part) and
> `xbyte-body.md:169`/`:638`, which *argue against* impossibility framing rather than assert it.
> (`Donna-Manuscript` hits are a private non-P2 book and out of scope.) Verified rather than assumed,
> which is the standard this finding set for itself.

### F-278 — wrong-code examples ship in ordinary syntax-highlighted blocks, distinguished only by a comment, in three manuals. `DONE` (verified 2026-10-05 «#386»: all 8 sites are antipattern blocks at the latest tags)

**Locations (8 sites — the 7 first enumerated, plus the 8th the narrow pattern missed).** Sites are
named by section rather than by line, because master line numbers move with every content task and a
stale number sends the next reader to the wrong block. **All 8 are CONVERTED, and 7 of them have
SHIPPED — verified against the release tags on 2026-08-20 («#282»), not inferred from this register:**

| Manual | Site | State |
|---|---|---|
| Streamer | §13.4's `\|`-vs-`+` pair | converted · **RELEASED v1.0.9** (2026-08-19) |
| Debug Window | `ch12-bidirectional.md`, both sites | converted · **RELEASED v1.1.3** (2026-08-18) |
| IOSP | `appendix-e-troubleshooting.md` ×3, `chapter-17-serial-receive.md`, `chapter-11-serial-transmit.md` | converted · **RELEASED v1.0.9** (2026-08-18) |
| Debug Window | `ch08-scope-xy.md` blockquote pair | **deliberately deferred** — see below |

**This annotation used to read `(NOT RELEASED, v1.0.9)` / `(NOT RELEASED, v1.1.3)` / `(RELEASED,
v1.0.8)`, and all three were stale.** The releases happened on 2026-08-18 and 2026-08-19 and nothing
came back to say so. Note the direction: the record understated what had been done, so a reader is
sent to redo finished work. `audit-register-hygiene.py` cannot see this class — it detects only the
opposite drift, a headline claiming a fix over a status token that does not agree. Same gap as F-272.

The platform provides `AntipatternBlock` (`p2kb-platform-content.sty:277` — red fill, red border, 4 pt
left rule), reachable as a ```` ```antipattern ```` fence or `::: antipattern` div via
`p2kb-platform-code-coloring.lua`. deSilva (6 sites) and Assembly (`appendix-h-reserved-words.md:569`)
use it correctly. The seven sites above do not — wrong code sits in ```` ```spin2 ````, marked only by a
`' WRONG` comment, so it carries identical highlighting and identical visual authority to correct code.

**Streamer's is the worst**, because the correct and the wrong form share **one block**. A reader
skimming code blocks — how people actually use a reference guide — can lift the wrong line without
reading the comment. It is the EF-053 `P_OE` material, where the failure is silent and total: measured
on silicon at 6,737 ADC counts for `|` against 1,407 for `+`, indistinguishable from no drive.

**Proposed correction:** split Streamer's into two **adjacent** blocks — correct stays ```` ```spin2 ````,
wrong becomes ```` ```antipattern ````. Green beside red is a stronger contrast than two comments in one
block, so the pedagogy improves rather than suffers. Convert the Debug Window and IOSP sites in place.

**Zero platform cost — verified:** `p2kb-streamer-reference.latex:21`, `p2kb-debugwin.latex:23` and
`p2kb-iosp-reference.latex:22` all already load `p2kb-platform-content.sty`. Markdown-only in all three.

**A fourth Debug Window site is deliberately NOT converted.** `ch08-scope-xy.md:71` pairs a wrong
line and its corrected form inside a **blockquote** callout (`> ```spin2`). Converting it would make
`> ```antipattern` the **first instance of that fence-inside-blockquote combination anywhere in the
set** — `> ```spin2` appears only in this one file (2 uses, shipped in v1.1.2, so that form is
render-proven; the antipattern form is not). Introducing an unverified fence combination into a
manual shipping in the current wave risks a silent render defect for a two-line paired contrast that
already reads correctly. **Action: verify `> ```antipattern` at the next Forge round-trip
(`forge-test`), then convert if it renders.** Same reasoning as the `\|`-in-a-table-code-span trap:
no precedent in the set is a render risk, not a green light.

**IOSP is not in the release wave.** Its sites are fixed in opus-master and ship at its next release —
editing a master is not releasing a document. *(That next release came: **v1.0.9, 2026-08-18**. All
five conversions are in the tag.)*

**IOSP RESOLVED 2026-08-17 («#246») — five sites, not four.** The four declared sites are converted.
A **fifth** turned up because this pass used the broader wrong-code pattern
(`WRONG|Wrong|INCORRECT|Do not do this`) rather than the `^' *WRONG` form that missed the Debug Window
blockquote: `part-2-output-modes/chapter-11-serial-transmit.md:174`, a `**Wrong:**`-labelled
```` ```spin2 ```` block already paired with its `**Correct:**` twin. **The narrow pattern under-counted
this finding in two manuals; the enumeration above is the floor, not the census.** Three of the IOSP
sites carried the wrong and correct forms in **one** block and were split the way Streamer's was —
```` ```antipattern ```` then ```` ```spin2 ```` — so the reader gets red-beside-green rather than two
comments in one box.

> **RE-MEASURED 2026-08-25 («#301») — the 8th site is ALREADY CONVERTED IN THE MASTER, so what is
> owed has changed shape.** `ch08-scope-xy.md:70` now reads `> ```antipattern` (with its `> ```spin2`
> twin at `:74`), converted by `f769b46a` on 2026-08-17 — i.e. it went in **ahead of the render gate
> this finding set for it**, not after. The status text below still describes a decision
> ("convert if it renders"); the decision is made and the code is in the file. Grep confirms this is
> still the **only** fence-inside-blockquote construction in the whole set: `> ``` ` matches
> `ch08-scope-xy.md` and nothing else, at exactly those four lines.
>
> **So the risk this finding identified is now live rather than avoided**, and that is the honest
> reading: an unproven fence combination is sitting in a master that will render. Nothing here can
> settle it — a PDF is produced on the Forge, not in this container.
>
> **Owed to «#302» / the next Debug Window `forge-test`, and this is the whole of it:** open the
> rendered page for §SCOPE_XY's create-line callout and confirm the `> ```antipattern` block renders
> as an AntipatternBlock **inside** the blockquote — red fill, red border, left rule — rather than
> collapsing to a plain quote, swallowing the fence markers, or breaking out of the callout. If it
> renders, this finding closes with no further edit. If it does not, revert `:70`/`:74` to
> `> ```spin2` and record the platform limitation. `p2kb-debugwin.latex:23` already loads
> `p2kb-platform-content.sty`, so a failure would be a filter/blockquote interaction, not a missing
> package.
>
> **The other 7 sites are re-confirmed shipped** and are not part of what is owed.

**Status:** `DONE — all 8 sites shipped as antipattern blocks at the latest tags (verified 2026-10-05 «#386»); history: 8 of 8 sites converted IN SOURCE; 7 shipped (Streamer v1.0.9, Debug Window
v1.1.3, IOSP v1.0.9). The 8th (ch08-scope-xy.md's blockquote pair) is converted but its render is
UNPROVEN — it is the only `> ```antipattern` in the set. Verify it on the page at the next Debug
Window Forge round-trip; that render is the only thing between this finding and closure.`

### F-279 — the XBYTE guide grounds a load-bearing hardware claim on a sibling manual in the same family, without disclosing it. `RESOLVED — fixed in the v1.1.0 restructure, shipped 2026-08-19; closed on re-verification 2026-08-23`

> **CLOSED 2026-08-23, verified against the master, not inferred.** The circular citation is **gone**:
> *"P2 Assembly Language Reference"* now appears **zero** times in `xbyte-body.md`. The `_RET_ CALL`
> hazard moved to §16.3 in the v1.1.0 restructure and is grounded on a **primary** source —
> *"Parallax's instruction table (P2 Instructions v35 – Rev B/C Silicon, row 410) defines `_RET_` as
> 'execute `<inst>` always and return if no branch.'"* That is exactly the fix this finding asked for.
>
> **This finding read `CONFIRMED` / `NOT RELEASED … ships in v1.0.2` for four days after it was done.**
> Two independent staleness paths crossed here: the fix rode a restructure that renumbered the target
> version (v1.0.2 was never published — **v1.1.0** shipped 2026-08-19 instead), and the cited line
> `:1427` now points at unrelated content because the restructure moved everything. A finding pinned to
> a line number and an unshipped version number is a finding nobody can re-check cheaply.

**Location (as filed):** `manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1427` — line
reference is **historical**; the restructure invalidated it.

The `_RET_ CALL` hazard block cites *"the condition table in the **P2 Assembly Language Reference
Manual**"* for `_RET_`'s branch-conditional semantics. That title is **not fabricated** — it is the cover
title of our own manual (`p2-assembly-language-manual/opus-master/front-matter.md:20`). The defect is
**circularity**: a peer derivation cannot ground a hardware claim, and unlike `P2AN002.md:378` — which
cites the same manual while labelling it *"a companion P2 Knowledge Base publication"* — this site
discloses nothing, so it reads to a reader as an external authority.

**Proposed correction:** repoint to the Parallax primary sources F-273 was actually grounded on —
*Propeller 2 Assembly Language (PASM2) Manual* draft (2022-11-01, p.68) and *P2 Instructions v35*
(row 410). **Verify the citation against the live source, not against this register** — a ledger is not
citation authority, and this guide has shipped fabricated names before (Appendix C).

**No set-wide normalisation owed.** The other four sites naming this document were checked and are
sound: deSilva `:5845` uses the Parallax name correctly, and the remainder are our own cover title and a
CHANGELOG font note.

### F-282 — every `MANUAL-DESCRIPTOR.md` records a stale `last_published_tag`, so every diff-since-published audit reads the wrong baseline. `DONE` (regressed and re-closed 2026-10-05 «#386»: 12 of 17 descriptors were stale again; all advanced from git, and the step is now the blocking runner gate `descriptor-baseline`) — **the whole fleet corrected and the guard's own blind spot closed 2026-08-25 («#302»)**

> **CLOSED 2026-08-25 («#302») — both halves, measured against `git tag` rather than against any
> file's own claim.**
>
> **(a) Eight descriptors were still stale at HEAD, and seven of them were invisible to the check
> built to catch this.** Measured before any edit:
>
> | Element | Descriptor said | Actually tagged | |
> |---|---|---|---|
> | Assembly | `…-v3.1.6` | **`…-v3.1.7`** | 1 release behind |
> | P2AN001 | `unreleased` | **`p2an001-v1.0.4`** | whole doc read as unreviewed |
> | P2AN002 | `unreleased` | **`p2an002-v1.0.3`** | ” |
> | P2AN003 | `unreleased` | **`p2an003-v1.0.2`** | ” |
> | P2AN004 | `unreleased` | **`p2an004-v1.0.2`** | ” |
> | P2AN005 | `unreleased` | **`p2an005-v1.0.2`** | ” |
> | P2AN006 | `unreleased` | **`p2an006-v1.0.1`** | ” |
> | P2AN007 | `unreleased` | **`p2an007-v1.0.1`** | ” |
>
> All eight advanced, each with its trailing comment rebuilt from git — `git log -1 --format=%ad`
> for the date and `git show <tag>:…pdf | pdfinfo -` for the page count, never from memory or the
> roster, because *a stale comment beside a corrected value is the same defect wearing a disguise*.
> The two genuinely-unreleased seeds (Single-Step Debugger, PNut-Term-TS) correctly carry an empty
> value and were left alone. **All 17 descriptors now match.**
>
> **(b) THE DURABLE GUARD HAD THE SAME HOLE THE FINDING DESCRIBES.** `release-manual`'s
> project-overlay added the Phase-3 advance and a fleet-verification loop — but that loop globs
> `manuals/*/MANUAL-DESCRIPTOR.md` **only**, so all seven app-note descriptors sat outside every run
> of it, and it keys a **case-sensitive** `grep "^$slug-v"` off an uppercase directory (`P2AN001`)
> against a tag namespace that went lowercase at the 2026-07-12 fleet release — the exact
> case-split this finding already identified as what produced its own original wrong filing. Run as
> written it reported **one** stale element; run corrected it reports **eight**. A fleet check that
> cannot see part of the fleet exits 0 and proves nothing.
>
> Both defects fixed in the `release-manual` skill overlay (agent-side): the glob now covers
> `app-notes/*/` and the lookup is `grep -i`, with the reasoning recorded inline so neither is
> re-simplified away.
>
> **Proven able to fail (F3).** After the fix the corrected sweep reports **no** stale elements; a
> negative control that reverted P2AN006 to `p2an006-v1.0.0` made it fire —
> `STALE P2AN006: 'p2an006-v1.0.0' vs 'p2an006-v1.0.1'` — and the file was restored. A check that
> cannot fail has not been verified, it has been run.

> **Wave descriptors fixed 2026-08-17**, each checked against `git tag` rather than against the file's
> own claim: Debug Window `v1.0.0`→**`v1.1.2`**, IOSP `unreleased`→**`v1.0.8`**, Assembly
> `v3.1.2`→**`v3.1.5`**. Their trailing baseline comments described the OLD tags (wrong dates, wrong
> page counts, one still calling IOSP a maiden release) and were rewritten to the real released dates
> and page counts. **A stale comment beside a corrected value is the same defect wearing a disguise.**
> Descriptors outside the wave are untouched and still stale.

> **Rewritten in place 2026-08-17, hours after it was filed.** The original text claimed the app-note
> *tags* were two to three releases behind and that the app-note release path "never lays the tag."
> **That was wrong, and the error was in the probe, not the repo.** The scan grepped for the
> uppercase prefix `P2AN001-`, but the app-note tag namespace switched to **lowercase** at the
> 2026-07-12 fleet release. `p2an001-v1.0.3`, `p2an002-v1.0.2`, `p2an003-v1.0.2`, `p2an004-v1.0.2`
> all exist, and `git for-each-ref --format='%(creatordate:short)'` shows each was created **on its
> release date** — not retroactively. Every app note and every manual is tagged current. The
> conclusion "specific to the app-note release path" was false in both halves.
>
> The *symptom* the finding described is real. The cause is below.

**Found:** 2026-08-17, enumerating what was pending for release alongside Debug Window and IOSP.
**Corrected the same day**, when preparing the six-element wave put the actual tag list on screen.

**The tags are complete.** Every released version of every manual and app note has a tag at the
commit that shipped it. Nothing is owed here.

**The descriptors are stale.** `document-audit`'s changeset-integrity dimension (Dimension #15) does
not read `git tag` — it reads the `last_published_tag:` field in each `MANUAL-DESCRIPTOR.md`. Those
fields were written at seed time and never advanced by a release:

| Element | Descriptor says | Actually released + tagged | Baseline error |
|---|---|---|---|
| P2AN001 | `unreleased` | **1.0.3** | whole doc reads as unreviewed |
| P2AN002 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN003 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| P2AN004 | `unreleased` | **1.0.2** | whole doc reads as unreviewed |
| Assembly | `v3.1.2` | **3.1.5** | 3 releases of published work |
| Streamer | `v1.0.6` | **1.0.8** | 2 releases |
| deSilva | `v3.0.1` | **3.0.5** | 4 releases |
| Debug Window | `v1.0.0` | **1.1.2** | 5 releases |
| XBYTE | `none` — "NOT yet released" | **1.0.1** | whole doc reads as unreviewed |

So this is **not** an app-note problem. It is fleet-wide, and it is worse on the manuals than on the
app notes — the opposite of what the original finding said.

**Why it bites.** With the recorded baseline several releases behind, the audit diffs against content
that shipped months ago and reports **already-published work as unreviewed change** — noise that
trains the reader to skip the signal. It fails in a direction that looks like diligence.

**A second, smaller defect, and the one that caused the misdiagnosis:** the app-note tag namespace is
**case-inconsistent** — `P2AN001-v1.0.0`/`-v1.0.1` uppercase, `p2an001-v1.0.2` onward lowercase. Any
case-sensitive lookup of a "latest tag" silently resolves to the pre-July tag. That is what made the
original probe read three missing releases that were never missing.

**Fix:** (a) advance every `last_published_tag:` to the element's actually-released tag, and make
advancing it a step in `release-manual` so it cannot drift again; (b) settle the app-note tag case
one way and treat lookups as case-insensitive until it is. No tags need to be created.

**Lesson, recorded because it cost a wrong finding:** the probe's *absence of a result* was read as
a fact about the repository. A grep locates; it never concludes. This is the same failure mode as
"a status line is not evidence," and it was caught only because a later task put the full `git tag`
output on screen for an unrelated reason.

---

## P2KB YAML corrections

> **Sweep origin (2026-06-13):** surfaced while auditing the Debug Window Manual's
> examples against the DEBUG display windows KB. Ground truth used is the **v55 Spin2
> documentation primary source** (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`,
> the per-window directive tables at lines ~1118–1417), which revealed the v1.8.0/v1.9.0
> reconciled `debug-displays/*.yaml` carry several errors/omissions vs that source. All
> findings below are CONFIRMED against the v55 primary source. The manual was, in several
> cases, MORE correct than the YAML.

> **✅ AUTHORITY CORRECTION — RESOLVED (2026-06-14).** The findings below were originally
> derived using the v55 **published documentation text** as authority. That was the wrong
> order: the **Pascal source** (`DebugDisplayUnit.pas`) is ground truth, and the
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md` (+ per-window theory-of-operations docs) are
> Pascal-derived — the published text is the derivative that carries the off-by-ones. The
> matrix + theory-of-operations were **re-audited against the Pascal source and re-imported**
> (2026-06-14, `REF/` under `p2-debug-window-manual`). The full analysis was **rerun against
> the matrix as authority** and the findings applied/closed below. Net outcome: in the
> majority case the matrix was right and the YAML already matched it (→ `RESOLVED-INVALID`);
> a smaller set were genuine defects (→ `DONE`); and three NEW writing-debug-statement defects
> surfaced during the rerun (F-132/F-133/F-134, all `DONE`). Every changed example was
> compile-verified with `pnut-ts -d`.

### F-207 — packed-data feed for **scrolling** LOGIC/SCOPE windows requires a **full-window array feed** (`` `uhex_long_array_ ``); a single `` `(packed) `` long does NOT fill the window — `DONE — manual DONE + HW-verified · KB DONE (v1.15.0) · the design decision adopted in Debug Window v1.1.4 ch13 (verified 2026-10-05 «#386»)`

> **Heading corrected in place 2026-08-15.** It read *"KB enrichment pending"* while this entry's own
> body recorded **"KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0. Both facets landed."** Verified
> against the YAML rather than the note: `language/spin2/debug-displays/logic.yaml` carries the
> array-feed example **and** the sub-sample-width = channel-count rule; `scope.yaml` carries the
> array feed; `language/spin2/statements/debug.yaml` carries the cross-referencing example. **No KB
> work is owed — do not re-file this as a YAML item.**
>
> **What is actually still open, and it is manual-head:** whether `ch13-packed-logic-stream` becomes
> the richer **2-channel + `LONGS_2BIT`** demo. Today's single-channel `'D0'` + `LONGS_1BIT` version
> is internally consistent and hardware-confirmed, so nothing is broken; adopting the richer form
> costs one more render. **Stephen's design call.**
>
> **Ordering caveat worth carrying:** this entry's own "verify first" note says Facet B (the
> mode↔channel-count rule) was a **peer report, not our own hardware run**, and directs us to confirm
> on silicon *before* enriching the KB — but the KB enrichment shipped in v1.15.0 regardless, so that
> order was inverted. The 2-channel render above **is** the confirming run. Until it happens, Facet B
> in the KB rests on a peer report plus how LOGIC is documented to unpack, not on our own bench.

**Surfaced:** 2026-07-11, fleet-release sweep — two published Debug Window Manual ch13 examples rendered only a fragment. **Root cause hardware-verified** the same day (Stephen ran the reshaped figure-generators; Claire read the BMPs back via image-tools).

**What's wrong (empirical ground truth):** for the **scrolling time-series** windows (LOGIC, SCOPE), feeding packed sample data as a **single** `` `(packed) `` long per message renders only a fragment — it does **not** accumulate/unpack across the window. The **only** feed that fills the window is the **full-window array feed** `` `uhex_long_array_(@buff, N) ``, which is also the **only packed example the v55/v51 docs ever show** (v55 text line ~1144 / v51 line ~1858, identical). The BITMAP (frame-buffer) window **tolerates** a per-long packed feed — which is why `ch13-packed-bitmap-frame` was always correct and was left untouched; that isolates the defect to the **feed shape for scrolling windows**, not the packing mechanism itself.
- **Pre-fix measurements:** LOGIC — data only in the last long's band (right-edge fragment). SCOPE — data only in the first few bands (left-edge fragment).
- **Post-fix hardware renders (2026-07-11 19:00, `fig-13-*_WDW.bmp`):** LOGIC = **full-width** random D0 trace (left edge, blank pre-fix, now packed with transitions); SCOPE = **two 0–255 sawtooths** (A + B), full vertical sweep. Both fixes empirically confirmed.
- SCOPE also had a 2nd defect: channel-defs lacked the **required** range → fixed to `'A' 0 255 'B' 0 255` (per the `'label' AUTO|lo hi` rule, F-137/EF-003 lineage).

**Manual — DONE (this sweep, HW-confirmed).** Fixed lockstep in opus-master `ch13-packed-data.md` + examples-library + figure-generators (byte-identical example↔code-block; corpus identity GREEN 32/32; compile clean `pnut-ts -d`): logic → `VAR buff[8]` (8 longs = 256 samples) fed via `` `uhex_long_array_(@buff, 8) ``; scope → `VAR buff[128]` array feed + the `'A' 0 255 'B' 0 255` ranges; prose gained an array-feed paragraph.

**Facet B — packing mode must match the LOGIC channel count (user-reported + HW-CONFIRMED 2026-07-11).** Stephen, exercising the *shipped* ZIP, found the (old) `packed-logic-stream` example declared **two** channels but used **LONGS_1BIT** → **all samples drew on the first channel only**; changing it to **LONGS_2BIT** made both channels display. The rule (grounded in how LOGIC unpacks): for LOGIC the packing mode's **bits-per-sub-sample must equal the channel count** — `LONGS_1BIT` = 1 channel, `LONGS_2BIT` = 2, `LONGS_4BIT` = 4, `LONGS_8BIT` = 8; each sub-sample carries one bit **per channel** per time-step. (SCOPE differs: an 8-bit-packed SCOPE sub-sample is a full per-channel *value*, and channels interleave across consecutive sub-samples — cf. `ch13-packed-scope` = 2 channels A/B via `LONGS_8BIT`.) Our reshaped `ch13-packed-logic-stream` currently sidesteps this by using a **single** channel `'D0'` + `LONGS_1BIT` (consistent, HW-confirmed) — the shipped bug cannot recur in it — but the richer, on-intent demo is 2 channels + `LONGS_2BIT` (design decision open with Stephen; would need one more render).

**KB — enrichment pending (the class-wide/systemic angle → yaml head).** The shipped KB documents the packing **modes** (`debug-displays/logic.yaml:37`, `scope.yaml:39`) and the concept ("packed-data modes let you pack multiple sub-samples", `logic.yaml:88`), and `statements/debug.yaml` shows the normal per-sample feed — but **no KB file shows the packed full-window feed**, states the single-`` `(packed) ``-long-won't-fill-a-scrolling-window fact, **or ties the packing mode to the channel count** (`logic.yaml:38` only covers the multi-bit-*bus* `count` field, not mode↔channel-count). A remote agent generating packed LOGIC/SCOPE code from the KB would reproduce both the fragment defect and the all-on-channel-0 defect.

**Proposed KB action:** (1) add a **packed full-window array-feed example** to `debug-displays/logic.yaml` and `debug-displays/scope.yaml` (and the packed-mode note in `statements/debug.yaml`) — `` `uhex_long_array_(@buff, N) `` matching v55's only packed example — plus the caveat: *a single packed-long feed advances the scrolling window by one column only; the full window requires the array feed* (BITMAP is exempt). (2) Document the **mode↔channel-count** rule in `logic.yaml` (LONGS_NBIT ⇒ N one-bit channels) and the SCOPE value-interleave form in `scope.yaml`.

> **KB APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** Both facets landed. `logic.yaml` — `packed:` gains the
> sub-sample-width = channel-count rule (Facet B) + a new LONGS_2BIT full-window array-feed example
> and an array-feed/unpack note (Facet A, unpack semantics quoted from v55 L1143/L1406). `scope.yaml`
> — `packed:` gains the per-channel-value interleave form (Facet B) + a LONGS_8BIT array-feed example
> and left-edge-fragment caveat (Facet A). `statements/debug.yaml` — a packed scrolling-window
> array-feed example cross-referencing both. D2 (Stephen): essential feed-shape snippet, NOT the
> verbatim v55 streamer example (incidental + misleading re streamer-required); unpack semantics
> quoted verbatim.

**Verify first (at fix time, §4.5):** open v55 text line ~1144 (and the REF Pascal-derived matrix / `DebugDisplayUnit.pas SetPack`) and match wording exactly — do not paraphrase. Facet A's feed-shape claim is grounded in the 2026-07-11 hardware renders + v55 showing only the array form. **Facet B is a peer report (Stephen), not yet our own hardware run — confirm on silicon before enriching the KB** (empirical > documentary); the LONGS_2BIT 2-channel render, if we adopt that example, IS that confirmation.

### F-208 — PLOT POLAR orientation (θ=0 baseline direction) is undocumented; the rotation-sense wording is murky/likely-wrong — `DONE` (verified 2026-10-05 «#386»: plot.yaml v1.23.3 and Debug Window v1.1.4 ch05 both state θ=0 East) (Test J)

**Surfaced:** 2026-07-11 — Test J had to be run to *learn* the POLAR orientation because it is documented nowhere. Per the **test-to-learn = doc/KB gap** rule (Stephen's call this date), the learned fact must be written back into both the KB and the manual, not consumed once.

**What's wrong / missing:**
- **θ=0 baseline direction is documented NOWHERE** — neither `debug-displays/plot.yaml` nor ch05-plot.md states where angle 0 points. Test J resolved it: **θ=0 → East (+x); increasing θ is counter-clockwise** (math convention); no flip.
- **Rotation-sense wording is murky/likely-wrong:** `plot.yaml:62` — *"twopi -1/0 select clockwise/counter-clockwise sense."* The default `twopi` is `$1_0000_0000` (positive → CCW), **not** 0; and the "-1/0" shorthand fails to convey the actual rule — a **negative** `twopi` reverses to clockwise.

**Evidence:** Test J (`conflict-testJ-polar-theta0`, both platforms 2026-07-11): sampling ρ≈150 from origin — **East=RED (0°)**, North/up=GREEN (90°), West=BLUE (180°), South=YELLOW (270°) → θ=0 East, CCW. Recorded in `audit/v55-vs-REF-reconciliation-2026-07-10.md`; EF entry pending (§7.6 / #196).

**Proposed correction (KB → yaml head):** in `plot.yaml` POLAR directive, state that **θ=0 points East (+x)**; the default (positive `twopi`) sense is **counter-clockwise**; a **negative `twopi` reverses to clockwise**. Replace the `"twopi -1/0"` shorthand with that sign-based rule.

> **YAML APPLIED 2026-07-11 — PUBLISHED in KB v1.15.0.** `plot.yaml:62` POLAR now reads "*Orientation:
> theta=0 points East (+x); with the default (positive) twopi the angle increases counter-clockwise;
> a NEGATIVE twopi reverses the sweep to clockwise*" — the murky `"twopi -1/0"` shorthand is gone.
> Manual side already applied (#195). Grounded EF-032/Test J.

**Manual side (→ ch05-post #195-C):** add the same orientation fact to the ch05-plot.md POLAR section — re-scoped from "optional enhancement" to **required gap-fill**.

**Grounding:** Test J (empirical > documentary). Cite the EF once promoted.

> **KB HALF RE-VERIFIED ON DISK 2026-08-25 («#300») — DONE, and richer than the entry proposed. No KB work
> is owed.** Read at the file, not from the status note above:
> `deliverables/ai/P2/language/spin2/debug-displays/plot.yaml:62` now carries **both** repairs this finding
> asked for, plus a distinction the proposal did not make:
> *"twopi = full-circle units (default $100000000): **0 => +$100000000** (default, counter-clockwise
> winding), **-1 => -$100000000** (reversed, clockwise winding) — **0 and -1 are NOT equivalent**; any other
> value is taken literally (e.g. 360 = degrees). **Orientation: theta=0 points East (+x)**; positive twopi
> increases theta counter-clockwise, negative twopi clockwise."*
> The murky `"twopi -1/0"` shorthand this finding named is gone, θ=0 is stated, and the sign-based rule
> replaced it. **Status stays `CONFIRMED` only because the manual half is still owed** — routed to «#301»,
> which owns the ch05-plot.md POLAR section. **This entry is not a KB item; do not re-file it as one.**

## Systematic `P_*` constant-name audit (2026-07-01) — F-177…F-183

> **Origin & method (Stephen's call).** After F-174/175/176 kept surfacing fictitious `P_*`
> constants ad-hoc, we ran a **corpus-wide audit** to make it the last time. Method: the
> **legality arbiter is `pnut-ts` v1.55** (our authority order: compiler → v55 doc → Silicon);
> the **v55 Spin2 manual is the enumeration**. Extracted every unique `P_[A-Z0-9_]+` token in
> `deliverables/ai/P2/` (115) and compile-tested each. **Result: after the fixes below, the
> YAMLs contain ONLY legal v55 constant names** — `Y-legal \ L` is empty (no legal-but-nonstandard
> names), and all 8 fictitious names are gone corpus-wide. Also ran the **Opus-Master propagation**:
> the manuals are clean in body (they'd already removed these — see F-176 vindication). Two
> non-blocking findings remain: **F-182** (coverage gap) and **F-183** (donor staleness).

### F-183 — count-mode *concise donors* (10100/10101/10110/10111) are broadly stale/divergent from published — `RESOLVED 2026-08-25 («#300») — re-verified on disk; the defect this tracked no longer exists`
> **CLOSED ON RE-VERIFICATION, not on assumption.** Four checks were run against the four donor
> directories under `engineering/ingestion/smart-pins-catalog/ingestionSources/` (16 files), and all four
> legs of this finding came back clean:
>
> 1. **The undefined mode-name constants are GONE from the donors.** A Unicode-tolerant sweep
>    (`grep -rniE "PERIODS.{0,3}STATES|PERIODS.{0,3}CLOCKS|B.{0,3}A.{0,3}INPUT"` over all four donor dirs
>    — deliberately loose, because `smartpin-symbols.txt` has a history of zero-width characters defeating
>    an exact grep) returns **only folder-name echoes in `source-metadata.md`**, never a constant. The
>    donors now carry exactly the legal names published uses: `P_PERIODS_HIGHS`, `P_COUNTER_TICKS`,
>    `P_COUNTER_HIGHS`, `P_COUNTER_PERIODS`.
> 2. **Nothing leaked into the shipped KB.** `P_PERIODS_STATES` / `P_PERIODS_CLOCKS_*` appear nowhere in
>    `deliverables/ai/P2/`. `P_B_A_INPUT` appears once, at
>    `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml:101`, and it is a **guard**
>    — *"P_B_A_INPUT does not exist … Never add P_B_A_INPUT"* — i.e. the anti-pattern, correctly stated.
> 3. **The reseed vector is gone.** This entry's worry was that the concise-YAML pipeline would re-emit the
>    donors over published. There are **0 `.yaml` files anywhere under `smart-pins-catalog/`**; the donors
>    are now `.md` extracts only. There is nothing left to reseed *from*.
> 4. **The "different taxonomy" is a phrasing difference, not a correctness defect** — and this is the leg
>    that had to be checked source-first rather than taken from the entry. The **donor folder names track
>    the Silicon Doc's wording literally** (`part4-smart-pins.txt:130-133`: *"%10100 = for X periods, count
>    states"* · *"%10101 = for periods in X+ clocks, count time"* · `%10110` *count states* · `%10111`
>    *count periods*), while the **published titles paraphrase the same semantics** (`%10100` *"Sum Pulse
>    Duration Over X Periods"* … `%10110` *"Count Highs Over Periods Within X Clocks"* — "highs" being the
>    A-input's high **state**). Both sides agree with the primary source. The entry's framing — published
>    hand-corrected *away* from stale donors — reads as though one side were wrong; on the evidence
>    **neither is**.
>
> **Nothing is owed at the ingestion head.** Retired rather than left `TRACKED` indefinitely: a tracked
> item whose subject no longer exists is a false open, and it costs every future reader the same check.
>
> Original text, kept for the record: Carved from F-176. The 4 donors carry undefined **mode-name** constants (`P_PERIODS_STATES`, `P_PERIODS_CLOCKS_TIME/STATES/PERIODS`) **and** a different mode taxonomy than the (hand-corrected) published files, on top of the now-removed `P_B_A_INPUT`. Published diverged from them long ago (proving the concise-YAML pipeline isn't re-run for these), so reseed-risk is currently latent. A **full donor↔published resync** (mode names + taxonomy) belongs to the ingestion/smart-pins-catalog head, not a published-YAML edit. Tracked, not release-blocking.

## Quantitative hardware-table audit batch (2026-07-07) — F-203

### F-203 — 4-manual fan-out audit of quantitative hardware tables vs trusted ingested sources — `DONE — 14 CONFIRMED_WRONG (hand-verified) + 8 AT_RISK; every manual cell settled at the latest tags (Streamer v1.1.3, Debug Window v1.1.4, IOSP v1.0.11, deSilva v3.0.9; verified 2026-10-05 «#386»)`
> **Method:** 9-unit fan-out (IOSP ×5 parts, Streamer, Debug ×2, deSilva) enumerating every quantitative/encoding
> table cell, each classified GROUNDED/DERIVED/AT_RISK/WRONG against **ingested sources only** (Silicon Doc,
> Spin2 v55, P2 datasheet), then adversarially verified. Full verdicts: workflow `wx8vrj00a` output. 1 false
> alarm rejected on hand-verify (ch06 "30mA" — actually GROUNDED, spin2-v55:1502).
>
> **CONFIRMED_WRONG — IOSP (fold into v1.0.4):**
> - `ch02` `P_HIGH_FAST`/`P_LOW_FAST` drive impedance **`~100Ω` → `~17Ω`** (datasheet Vol 510mV@30mA ⇒ ~17Ω; 30mA is correct). **FIXED.**
> - `ch18` §18.6 Hub RAM **`8-15 clocks` → `9-16 clocks`** (datasheet RDLONG `9...16`). **FIXED.**
> - `appendix-b` + `appendix-c` (table **and** the `input_max = 3300mV/gain` formula) — **F-202 ADC-range recurrence** (2 more sites; ground-referenced `0-Xmv`). PENDING (rides the F-202 nominal-table fix across §16.2 + both appendices).
>
> **CONFIRMED_WRONG — deSilva (fold into v3.0.2):**
> - SETSE Event-Modes `%000` **"Never (disabled)" → "LUT read/write & hub-lock events"** (silicon-doc part3-interrupts:48-53). **FIXED.**
> - `EVENT_INT %0000` **"Pin matches interrupt configuration" → "An interrupt occurred"** (part2-video-output:360; pin-match is `EVENT_PAT %1000`). **FIXED.**
> - `EVENT_QMT %1111` **"CORDIC/PIX math complete" → "read with no CORDIC result available"** (part2-video-output:375 — the inverse meaning). **FIXED.**
>
> **CONFIRMED_WRONG — Streamer (needs own patch, NOT in current wave):**
> - §12.2 Sub-Pin Selection table treats `D[19:17]` as a uniform 3-bit selector for 1/2/4-pin; silicon encodes `pppa/pp?a/p??a` (pin-bits shrink 3/2/1; freed low bits = DAC sub-mode). 1-pin col correct; 2/4-pin cols wrong. (p2-documentation:3004-3009).
>
> **CONFIRMED_WRONG — Debug (needs own patch, NOT in current wave):**
> - `ch05` PLOT TEXTSTYLE **horizontal align 2/3 swapped** (source %10=right, %11=left) and **vertical align 2/3 swapped** (%10=bottom, %11=top) — spin2-v55:1282; plus downstream prose **"`$20` left-aligns" → right-aligns**.
> - `ch03` TERM **`TEXTSIZE` default `10` → "editor text size"** (spin2-v55:1305; the 10 is the PLOT default).
>
> **AT_RISK (unsourced specifics — disposition per finding):** IOSP `ch16` §16.8 ADC "input impedance ~500kΩ" + "absolute-error floor ~15mV" (from P2AN001, not in EF ledger — **jumper-only verifiable, VO-J candidate**); `ch10` DAC "Max Load >10kΩ…" (10× rule-of-thumb heuristic); `ch12` "input buffer ~2ns" (sub-component; 3-clk total IS grounded); `ch07` "180MHz rated / 250 overclock" (only 350 grounded; 180 cites external datasheet); Debug `ch05` weight "100/400/700/900" (OpenType nums unsourced; "thin"→"light"); Debug `ch14` "LOCK[15]" + "~10,000 msg/s" (tool/throughput, ungrounded). Disposition: remove the unsourced number or soften to qualitative; the ~15mV/~500kΩ ADC pair → VO-J jumper test.

> ### 🔴 KB-SIDE DISPOSITION 2026-08-25 («#300») — TWO OF THIS ENTRY'S OWN SUB-CLAIMS DO NOT SURVIVE THE SOURCE
>
> Only the **KB-side** halves are dispositioned here; the IOSP / deSilva / Streamer manual cells stay with
> «#301». Every item below was checked **source-first**, and two of them inverted. **Anyone working the
> manual half must read this block before "fixing" the manual to match this entry — two of these
> corrections would introduce a defect, not remove one.**
>
> **(a) Debug `ch05` PLOT `TEXTSTYLE` vertical align — `RESOLVED-INVALID`. The KB is CORRECT; the "swap" is a
> vocabulary collision.** This entry grades the vertical pair against the v55 published text
> (`spin2-v55-text.txt:1282`: *"%YY is vertical justification: %00 = middle, %10 = bottom, %11 = top"*) and
> calls our `%10=top / %11=bottom` a swap. It is not. **The Pascal-derived matrix is the authority for the
> DEBUG windows** — this register's own *AUTHORITY CORRECTION (2026-06-14)* established that, and said the
> published v55 text is the derivative that carries the off-by-ones — and the matrix
> (`p2-debug-window-manual/REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:797-828`, from `AngleTextOut`, 3483-3516)
> states **both halves for every value** precisely so this cannot be misread:
>
> > vertical `%10` → `ty := h` (3509) → *"the text sits **ABOVE** the anchor point"*, i.e. *"the anchor is the
> > text's **BOTTOM** edge"*; vertical `%11` → `ty := 0` (3510) → *"the text sits **BELOW** the anchor"*, i.e.
> > *"the anchor is the text's **TOP** edge"*.
>
> The matrix carries an explicit red warning that **"`%10` = left" (anchor-edge vocabulary) and "`%10` = right"
> (ink-side vocabulary) describe the same pixels**, and that this ambiguity *"is what caused this row to be
> documented backwards."* v55 uses **anchor-edge** words for the vertical axis and **ink-side** words for the
> horizontal one, in the same sentence. `plot.yaml:67` uses **ink-side consistently on both axes** — and it
> says so, prefixing the pair with *"Align value->direction"*. Under that vocabulary `%10 = top` (ink above
> the anchor) is **right**. Same for the horizontal pair, which this entry and the KB already agree on.
> **No KB edit made. Making the "fix" would have broken a correct file** — the E-005 lesson (*look for the
> vocabulary key before escalating a two-source conflict*) one register over.
>
> **(b) Debug `ch05` weight `"thin"→"light"` — `RESOLVED-INVALID`, and the numbers are NOT unsourced.** The
> matrix quotes the Pascal array directly: `weight: array [0..3] of integer = (100, 400, 700, 900);` (3485),
> applied as `NewLogFont.lfWeight := weight[style and 3];` (3494). So **100/400/700/900 are sourced**, and
> **100 is OpenType `Thin`** (300 is `Light`) — our `plot.yaml:67` gloss *"0=thin, 1=normal, 2=bold, 3=heavy"*
> is correct against the Pascal. v55's *"%00 = light"* is the outlier. **No KB edit made.**
>
> **(c) Debug `ch03` TERM `TEXTSIZE` default `10` → "editor text size" — `RESOLVED-INVALID` as written; both
> statements are true and the KB's is not wrong.** The matrix settles it at
> `DEBUG-WINDOW-DIRECTIVE-MATRIX.md:502-512`: *"The global `FontSize` preference (set in `EditorUnit`, default
> **10**, user-adjustable 1–72) and the `DefaultTextSize = 10` constant both default to **10**, so every
> display window starts at **10 pt** except MIDI"* — and its per-window table lists **TERM `FontSize` = 10**
> (2186) alongside LOGIC/SCOPE/SCOPE_XY/FFT/PLOT, all 10. v55's *"editor text size"* names the **preference**;
> `10` is that preference's **default**. `term.yaml:32` (*"6..200 (default 10)"*) is therefore accurate.
> Swapping it for *"editor text size"* would have **deleted a true number and replaced it with a vaguer
> phrase**. **No KB edit made.** *(Available enhancement, not a defect and not done here: the six
> debug-display YAMLs could add that the default tracks a user-adjustable editor preference. It applies
> identically to all six, so it is an all-or-none consistency change outside this finding's scope.)*
>
> **(d) IOSP `ch16` §16.8 ADC `~15mV` absolute-error floor — ALREADY SATISFIED in the KB, and refuted on
> silicon.** The VO-J test this entry proposed **was run**: `VERIFICATION-OPPORTUNITIES.md:39` records
> **VO-J-002 → DONE → EF-024** — *"Single-pin abs error **≤9 mV** (reproducible) → does NOT support a ~15 mV
> single-pin floor"*, with the pin-to-pin-spread half reclassified to external-hardware **VO-X-002**. The KB
> already carries exactly this, correctly hedged, at
> `application-notes/p2an001-single-pin-instrumentation-adc.yaml:100`: *"…the ratiometric single-pin absolute
> error was <=9 mV … the wider '~15 mV pin-to-pin spread' figure is a designer report that the bench has NOT
> yet reproduced … **Do not quote 15 mV as a specification.**"* **No KB work owed.**
>
> **(e) IOSP `ch16` §16.8 ADC `~500kΩ` input impedance — never reached the KB.** Swept
> `deliverables/ai/P2/`: no `500k` input-impedance claim exists. It is a manual-only item → «#301».
>
> **KB-side verdict: nothing is owed.** Status stays `PARTIAL` **for the manual cells only** (Streamer §12.2
> sub-pin selection, Debug ch05/ch14, and the remaining IOSP AT_RISK numbers), all of which are «#301»'s.

> ### 🟢 MANUAL-SIDE DISPOSITION 2026-08-25 («#301») — every remaining cell settled; ONE edit, and it went the OPPOSITE way to what this entry says
>
> Each cell was opened **on disk first** and graded against its authority, not applied from this
> entry's verdict. That order mattered: **six of the ten manual cells were already fixed and nobody
> had said so**, and of the four that looked outstanding, **three were RESOLVED-INVALID and applying
> them would have damaged correct pages.** The «#300» warning generalised exactly as it said it would.
>
> **Already fixed — verified in the master, not inferred (6):**
> - **Streamer §12.2 sub-pin selection** — `streamer-body.md:958` now states the correction verbatim:
>   *"It is **not** a uniform 3-bit selector across all pin counts: as the pin count rises, fewer of
>   these bits are pin-select bits and the freed low bits become **DAC-configuration** bits."* The
>   three tables under it (`:960-989`) give 1-pin = 3 pin bits, 2-pin = `D[19:18]` + `D[17]` config,
>   4-pin = `D[19]` + `D[18:17]` config. Checked against the silicon column at
>   `sources/silicon-doc/p2-documentation.txt:3004-3009` — `pppa / pp0a / pp1a / p00a / p01a / p10a` —
>   which is the 3/2/1 shrink exactly. Recorded in Streamer `CHANGELOG.md:102-105`.
> - **IOSP `ch02` drive impedance** — `chapter-02-enhanced-direct-io.md:51`/`:66` read `~30mA / ~17Ω`.
> - **IOSP `ch18` hub access** — `chapter-18-repository.md:346` reads `9-16 clocks/access`.
> - **deSilva `SETSE %000`** — `:5026` reads *"LUT read/write & hub-lock events (not a pin event)"*.
> - **deSilva `EVENT_INT %0000`** — `:5041` reads *"…as a POLL/WAIT event it means an interrupt
>   occurred"*; **`EVENT_QMT %1111`** — `:5056` reads *"GETQX/GETQY read with no CORDIC result
>   available"* (the inverse meaning, correctly stated).
> - **Debug `ch14` `LOCK[15]` and `~10,000 msg/s`** — **gone**. `grep` for either across the whole
>   Debug Window `opus-master/` returns nothing. The ungrounded throughput number is not in the book.
>
> **AT_RISK numbers — all already dispositioned exactly as this entry directed (4):** and the IOSP
> `CHANGELOG.md:53` records the pass, naming Chapters 7, 10, 12, 16.
> - `ch16` **`~500kΩ` input impedance — removed.** `grep "500k"` over the IOSP master returns
>   nothing; `chapter-16-adc.md:598` now says *"The 1× range presents a **high input impedance**"*
>   qualitatively, with the divider consequence. (This entry's KB-side item (e) called it
>   "manual-only → «#301»"; the manual had already dropped it.)
> - `ch16` **`~15mV` error floor — removed and REPLACED WITH THE BENCH RESULT.** `:599` now reads
>   *"a few millivolts (**≤ ~9 mV measured on real P2 silicon**; representative, not a guaranteed
>   spec)"*, with pin-to-pin spread named as the larger effect. That is EF-024 / VO-J-002, i.e. the
>   manual and the KB now agree, and neither quotes 15 mV as a specification.
> - `ch10` **DAC "Max Load"** — the column is renamed **"Min Load (guideline)"** and
>   `chapter-10-dac-output.md` states outright that it *"is a **rule-of-thumb guideline** (roughly
>   10× the output impedance), not a hard specification."*
> - `ch12` **"input buffer ~2ns" — gone.** No `2ns` anywhere in the IOSP master.
> - `ch07` **"180 MHz rated / 250 overclock" — now CITED, both ends.**
>   `chapter-07-pulse-transition.md:271` attributes 180 MHz to the P2 Datasheet and the ~350 MHz
>   ceiling to the Silicon Doc, and frames 250 MHz as *"commonly used"* rather than as a rating.
>   Both citations verified live: `sources/p2-datasheet/p2-datasheet-text.txt:2209` (*"Nominal PLL
>   frequency (system clock speed) is 180 MHz at up to 105 °C"*) and
>   `sources/silicon-doc/part3-interrupts.txt:545` (*"the PLL can be pushed to 350 MHz"*).
>
> **🔴 RESOLVED-INVALID for the MANUAL too — do not apply these; two of them would break correct pages (3):**
> - **Debug `ch05` PLOT `TEXTSTYLE` alignment, BOTH axes — `RESOLVED-INVALID`.** This entry says
>   horizontal 2/3 and vertical 2/3 are each swapped in `ch05`. They are not. `ch05-plot.md:356-357`
>   reads horizontal `2`=right / `3`=left and vertical `2`=top / `3`=bottom — **ink-side vocabulary,
>   used consistently on both axes**, which is the same convention `plot.yaml:67` uses and which the
>   Pascal-derived authority confirms: `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:797-828` gives
>   horizontal `%10` → `tx := 0` → *"the text sits to the **RIGHT** of the anchor"* and vertical
>   `%10` → `ty := h` → *"the text sits **ABOVE** the anchor"*. `ch05-plot.md:360`'s downstream prose
>   *"`$20` right-aligns"* is therefore also **correct** ( `$20` → bits 4-5 = `%10` → ink to the
>   right), not the error this entry records. Applying the swap would have inverted a correct table
>   and a correct sentence. Same vocabulary collision «#300» found on the KB side; the matrix's own
>   red warning says this ambiguity *"is what caused this row to be documented backwards."*
> - **Debug `ch05` weight `"thin"→"light"` — `RESOLVED-INVALID`.** `ch05-plot.md:353` reads
>   `0`=thin, `1`=normal, `2`=bold, `3`=heavy. Against the Pascal
>   (`weight: array [0..3] = (100, 400, 700, 900)`, matrix `:797`), **100 is OpenType *Thin*** —
>   *Light* is 300 — so the manual is right and the proposed change would have introduced the error.
>   ("heavy" for 900 is an accepted synonym of Black; not a defect.)
> - **Debug `ch03` TERM `TEXTSIZE`** — this one is `RESOLVED-INVALID` **and the manual had already
>   taken the invalid change**, so it needed reverting rather than leaving. See below.
>
> **The single edit made, and it runs OPPOSITE to this entry (1):**
> `ch03-term.md:45` had a Default column reading **"editor text size"** — i.e. exactly the swap this
> entry proposed, already applied at some earlier pass. «#300»(c) ruled that
> `RESOLVED-INVALID` because it *"deleted a true number and replaced it with a vaguer phrase"*, and
> the authority agrees: `REF/DEBUG-WINDOW-DIRECTIVE-MATRIX.md:502-512` states the global `FontSize`
> preference (default **10**, user-adjustable) and `DefaultTextSize = 10` both default to **10**, and
> its per-window table lists **TERM `FontSize` = 10** (Pascal 2186). Restored to `10`, with the
> preference stated too so both halves are on the page: *"the default tracks the editor's text-size
> preference, which is itself 10."* Per C4, the REF matrix outranks the v55 prose the old wording came
> from.
>
> **Raised, not just corrected (F2):** `ch05-plot.md` gains a short paragraph after the style table
> making the alignment vocabulary explicit — *"Read those alignment names as where the ink lands
> relative to the anchor point, not as which edge of the text the anchor sits on… If a label lands on
> the wrong side of its point, you have almost certainly read the row in the other vocabulary rather
> than found a bug."* The rows were already right; what was missing was the disambiguation that
> caused this cell to be filed as a defect twice. Stating both halves is what the authority itself
> does, and why.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on
> `ch03-term.md` and `ch05-plot.md`; `sync-manual-examples.py --check` reports **no** "BODY differs"
> for the Debug Window manual, so no printed listing drifted from its example file.
>
> **STILL OWED (1 cell, and it is not this finding's to close):** IOSP `appendix-b` + `appendix-c`
> ADC-range cells (table **and** the `input_max = 3300mV/gain` formula). They are the **F-202**
> recurrence and ride that finding's nominal-table fix across §16.2 + both appendices. F-202 is
> `PARTIALLY CONFIRMED` with the exact centered endpoints **UNVERIFIED — no trusted numeric source**,
> so what would settle it is the hardware campaign F-202 names, not an edit here. Touching the
> appendices ahead of F-202 would put a third unsourced framing in the book.
>
> **Manual-side verdict: 6 already fixed · 4 AT_RISK already dispositioned · 3 RESOLVED-INVALID
> (2 of which would have introduced defects) · 1 corrected back toward the authority · 1 owed to
> F-202.** Render owed for the Debug Window edits → «#302».

## CORDIC interrupt hazard — documented on one page, missing from the pages that need it (2026-07-14) — F-224

> **This header replaced a stale one on 2026-08-21.** F-224 had been sitting under
> *"`architecture/xbyte_engine.yaml` — all three programming examples are broken"*, whose four
> findings (F-220…F-223) all closed 2026-07-14/16 and were archived 2026-08-15 — leaving a live
> register asserting that three KB examples were broken when the file had been fixed for a month.
> Verified fixed in `xbyte_engine.yaml` at commits `31bffdce` (F-220/221/222) and `bb02525a`
> (F-223). Detected by `audit-register-hygiene.py` checks 8 and 9.

### F-224 — Assembly Manual: the CORDIC interrupt hazard is documented on the `REP` page, but **not on the CORDIC pages** — `RESOLVED 2026-08-17, shipped in v3.1.6`

> **Status heading corrected 2026-08-22.** It read `CONFIRMED` while this entry's own body recorded the resolution — the entry contradicted itself, and a status line is not evidence. The body below is unchanged.

**Raised by F-217's class-wide sweep.** Having found that the XBYTE Guide sold interruptibility as a
pure benefit, the same question was asked of every other manual: *does anything show a CORDIC
issue/collect pair without telling the reader it must be fenced?*

**The Assembly Manual is NOT wrong.** `part-ii/instructions-r.md` teaches the fence properly, and even
uses a CORDIC example:

> `' Protect CORDIC operation from interrupts` … `qmul  y, x`

and states the mechanism outright: *"Interrupts are blocked during REP execution — including debug
interrupts that ordinary masking cannot hold off — to maintain timing precision and keep the repeated
block atomic."* It also carries the useful nuance that the idiom *"is only needed in PASM2 code with
interrupts enabled; Spin2 operators are already protected by the interpreter."*

**But the warning is not where the affected reader is standing:**

| Page | Content | Interrupt mentions |
|---|---|---|
| `instructions-q.md` | **QMUL · QROTATE · QDIV** — the CORDIC **issue** ops | **0** |
| `instructions-g.md` | **GETQX · GETQY** — the CORDIC **collect** ops | 3 — **all from GETBRK**, none about CORDIC |
| `instructions-r.md` | REP | ✅ the fence, with a CORDIC example |

A reader who looks up `QMUL` — which is exactly what someone about to *write* a CORDIC sequence does —
learns nothing about the hazard. They find it only by happening to read the `REP` page.

- **Severity: low.** This is an omission at the point of need, not a false claim. Same *class* as F-217,
  milder in kind: the information exists in the manual.
- **Fix (small):** a cross-reference note on the CORDIC issue/collect pages — "a CORDIC command and its
  result must not be split by an interrupt; see REP" — costing a few lines, no content change elsewhere.
- **Release consideration for Stephen:** the Assembly Manual shipped **v3.1.4 on 2026-07-14** (a
  render-only patch). This is a *content* change and would need its own bump. It is a documentation
  improvement, not a correctness bug in the shipped text, so it can ride the manual's next natural
  release rather than forcing one.

**RESOLVED 2026-08-17 («#235» wave prep).** Confirmed still open first — `instructions-q.md` had
**zero** interrupt mentions, and `instructions-g.md`'s three were all GETBRK. The rule now opens the
**Q instruction section** (where a reader looking up QMUL or QROTATE lands) and the **CORDIC
Coprocessor category** (which reaches GETQX/GETQY too), both pointing at REP for the pattern and both
noting Spin2 needs no fence. Plain reference prose, not `{.warningbox}` — that convention is reserved
for silicon bugs, and this is a programming hazard. **Rides v3.1.6**, which was otherwise the one wave
element with no prose change, so it costs nothing to carry.

**Also observed (not a defect):** 22 stray `*.backup-encoding-conversion` files sit in
`p2-assembly-language-manual/opus-master/part-ii/`. They are **untracked** — `git ls-files` returns
zero — so nothing ships and no glob in the assemble scripts reaches them (those use explicit
`REQUIRED_FILES[]`). Working-tree clutter only; worth sweeping, not a release concern.

## Forum docs-feedback sweep (2026-08-14) — F-254…F-258

**Origin:** Parallax forum posts #104–#117 (2026-08-12/13), reviewing the deSilva tutorial, the
XBYTE Programming Guide, and the P2 Architect's Guide. Full analysis (with the tone/positioning
items that are *not* defects) lives at
`engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored — find it by path). Forum posts are the **lead**; every finding below was verified
against the live opus-master, `pnut-ts` 1.55.3, or P2KB before filing.

### F-256 — `_RET_ CALL` never returns, because `_RET_` returns only if the instruction did not branch. A DOCUMENTATION defect, not a hardware one. `RESOLVED — root cause is F-273; KB applied, manual restructure applied 2026-08-16 («#227»)`

**Location:** `xbyte-body.md:879` (*"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely on
this"*), used at `:1391`, `:1400`, `:416`, `:793`.

Christof (#110) doubted *"you can combine a CALL with ret."* **Tested: `_ret_ call #set_nz`
assembles clean under `pnut-ts` 1.55.3**, and `language/pasm2/call.yaml:11` describes CALL paired
"with a `_RET_` condition" — so as stated the objection is wrong.

**But the compiler proves legality, not semantics.** The open question is what the hardware does
when one instruction both pushes a return address and returns: does control reach the helper and
then return to `$1FF` (XBYTE re-entry intact), or does the push/pop ordering break dispatch?
`architecture/xbyte_engine.yaml:71` is suggestive but addresses a *different* case (why a CALL
cannot substitute for `PUSH #$1FF` at arm time). **Not resolvable from the KB or the Silicon Doc;
no answer is asserted here.**

> **ANSWERED — AND THE ANSWER WAS IN THE INGESTED SOURCES ALL ALONG. See F-273.**
> This was never a hardware question. **`_RET_` executes the instruction and returns *only if that
> instruction did not branch*** — stated by *two* independent Parallax primary sources (Assembly
> Language Manual 2022-11-01, condition table p.68; P2 Instructions v35 Rev B/C Silicon, row 410:
> *"if `<inst>` is not branching then return by popping stack[19:0] into PC"*). `CALL` branches, so
> `_RET_ CALL` cannot return. **The behaviour is specified, not anomalous.**
>
> **The real defect is ours:** our KB documented the prefix as an unconditional *"Always + Return"*
> and the qualifier *"if no branch"* appeared **nowhere** in `deliverables/ai/P2/`. An author
> reading that writes `_RET_ CALL #set_nz` and is right to. **Root cause, KB fix and the
> alignment-check lesson are all in F-273.**
>
> **What the bench actually showed (EF-058, corrected there too):** the handler falls through into
> whatever follows it in cog RAM. In the rig that was another handler, which ran in full and whose
> own `ret` returned to `$1FF` — so **all four bytecodes dispatched and the VM finished normally.**
> The original claim *"dispatch does not resume"* is **false**. The failure mode is **silent extra
> execution**, and it is **layout-dependent**.
>
> **NO FURTHER RIG RUN IS REQUIRED.** Not for generality outside XBYTE — the prefix is architectural
> and the sources say nothing about XBYTE — and not to confirm EF-058, which can only re-observe the
> specification. The `[M-pre]` grade and the staged `DEBUG_COGS` re-run are **moot for the
> conclusion**; the conclusion now rests on documentation, with the bench as corroboration.
>
> **Applied in `xbyte-body.md` («#227», uncommitted under the «#234» gate):** every `_RET_ CALL`
> replaced by `CALL` + `RET` — §15.3's handlers and the shared `ld_imm` family, §4.4's `alu_body`,
> §5's `push_const`, §17's `voice_on` — plus the two explanations that endorsed the idiom (`:882`
> and §15.3). **That structural change stands; its EXPLANATION is being rewritten** to teach the
> documented rule rather than the mechanism previously inferred here. Slices recompile clean.

**Action:** jumper-free, single-board hardware test — arm XBYTE, run a handler ending in
`_RET_ CALL`, report whether dispatch continues. Ideal **VO-J** candidate; result goes to the EF
ledger either way. **A load-bearing idiom in a guide under community review must not stay
unverified.** If it fails, §15.3 and the Chapter 9 explanation both need rework.

### F-284 — the 9-column encoding-table filter never escaped `&`, so two shipped instruction definitions print with the AND operator eaten by LaTeX. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). pp.326/329 print `Parity of (D & S)` and `Parity of ((D & !S) == 0)` with the operator intact and the columns in register.


**Found:** 2026-08-17, verifying the six generated wave PDFs page by page. The compile log
reported **zero errors**; the defect was visible only on the page.

**Location:** `platform/filters/p2kb-platform-tables.lua` — the `cell_to_latex` helper in the
9-column instruction-encoding table handler. Visible at **P2-Assembly-Language-Manual pp.326
(TEST) and 329 (TESTN)**, sourced from `part-ii/instructions-t.md:38` and `:169`.

**Mechanism.** That handler flattens each cell with `pandoc.utils.stringify()` and emitted the
result verbatim. The near-identical 6-column handler beside it, at the same file, has always run
`text:gsub("&", "\\&")` plus `%`, `#`, `_`. So one of two adjacent code paths escaped and the
other did not. An unescaped `&` inside a `tblr` cell **is an alignment tab**: it ends the cell,
shifts every later column one to the right, and pushes the row past the table's right border —
which is what the 50.2pt overfull hbox in the log actually was.

The reader sees the TEST row's C column as `Parity of (D` and the next cell as `S)`. **The AND
operator is gone from a bit-level definition of what the instruction computes**, and the row's
remaining columns are all off by one. It has been shipping this way since at least v3.1.5.

**`%` is the worse latent case.** Through the same unescaped path it would comment out the rest
of the row — silent, complete, and with a clean log. Same class as F-281.

**Blast radius measured, not assumed:** 281 nine-column encoding tables across the manual,
scanned for `&`, `%`, `#`, `_` outside code spans. **Exactly 2 hits, both `&`, both in
`instructions-t.md`; zero `%`/`#`/`_` anywhere in that path.** The other five wave elements
contain no nine-column encoding tables and were verified unaffected. The five `&` sites elsewhere
in Assembly and deSilva all go through escaping paths and render correctly — checked in the `.tex`,
not inferred.

**Fix applied:** the 9-column helper now escapes the same four characters as its sibling. Since
`stringify()` has already flattened the cell to plain text, no intentional LaTeX can be harmed.

**Owed:** re-render `p2-assembly-language-manual` v3.1.6 and confirm pp.326/329 read
`Parity of (D & S)` and `Parity of (D & !S)` inside a 9-column row. The platform file is staged.
No version bump — v3.1.6 has not shipped.

**Lesson.** The gate that would have caught this does not exist: we check source characters and we
check compile logs, and this defect is invisible to both. It was found by rendering a page and
looking at it, prompted by triaging an overfull-hbox count. **An overfull hbox in a table is worth
opening**; it is the only signal this failure emits.

### F-286 — the escaping that stops F-284's class was per-call-site discretion, so it drifted to five more raw-emission sites. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). Assembly exercises the class: headings `2.2.2 The _RET_ Condition`, `3.3.1 The IF_x Prefix`, `B.3 The _RET_ Condition (EEEE=0000)` and `Mode %00000 - %00011: ...` all print correctly in the body **and** in the TOC, and a whole-document sweep finds **zero** literal `\_`, `\%`, `\&` or `\#` escape leakage.


**Found:** 2026-08-17, asking the process question after F-284/F-285: *what would routinely catch
these?* The answer turned out to be a structural fix rather than a checklist.

**The class.** A pandoc Lua filter that calls `stringify()` and emits the result inside a
`RawBlock` bypasses pandoc's escaping entirely. `stringify()` flattens an element to plain text,
so nothing in the result is intentional LaTeX — but `&` in a raw position IS an alignment tab, and
`%` silently comments out the rest of the line **with a clean compile log**. F-284 was one instance.

**The rule already existed, written down, with rationale — and was applied at one site in four.**
`p2kb-platform-code-coloring.lua` carried a comment stating the principle exactly ("Special LaTeX
characters in the title are re-escaped because the title text, once parsed by Pandoc, is emitted
into a raw-LaTeX block"), and its `esc()` helper was declared **inside a single `elseif` branch** —
so the sidetrack handler 100 lines below, which that very comment cites as using "the same
addcontentsline technique", emitted its title unescaped. `p2kb-platform-pagination.lua` was the same
shape: a `latex_escape()` helper at line 26, used for chapter subtitles, **not** used for the Part
title 28 lines below.

**Five unescaped raw-emission sites, all fixed:**

| Filter | Site | Raw position |
|---|---|---|
| `p2kb-platform-pagination.lua` | Part title | `\manualpart{}` |
| `p2kb-platform-figures.lua` | figure caption | `\caption{}` |
| `p2kb-platform-code-coloring.lua` | sidetrack title | `\addcontentsline{}{}{}` |
| `p2kb-platform-tables.lua` | table caption `stringify` fallback | `caption={}` outer key |
| `p2kb-platform-tables.lua` | cell renderer `pandoc.write` fallbacks (×3) | `tblr` cell |

Escaping is now a module-level helper in each filter with the invariant stated at its definition,
rather than a decision re-made at each call site. That is the actual fix: **per-call-site escaping
drifts; one shared helper is why it stops drifting.**

**Blast radius measured, not assumed — zero live exposure.** All 38 `# Part` headings and all
`figurecaption` divs across the live masters were scanned for `&` and `%`: the only hit is in a
`creation-guide.md` (not a rendered master). So the change is **inert on today's content** and the
five already-verified wave renders remain valid. The `tables.lua` cell-renderer holes are fallback
paths that fire only when `pandoc.write` fails.

**Deliberate scope limit.** `tables.lua`'s helper escapes `& % # _` — the same four its cell
renderers already escaped inline — and deliberately **not** `{ } \`, because instruction tables
legitimately carry P2 syntax like `{#}` and escaping those braces would change pages that render
correctly today. Closing a hole must not move correct output.

**Retires an authoring workaround.** Authors were told to spell "and" in Part titles because an `&`
there broke the build. That restriction was a workaround for this bug and is no longer needed.

**Owed:** the Assembly render already owed for F-285 validates all of it. Confirm p.329, and confirm
Part titles and table captions still render as before.

**The process changes that came out of this — the durable half:**
1. **`latex_escape_processor.py` now hard-fails on HTML entities in prose.** Not a warning: this
   processor escapes `&`→`\&` before pandoc runs, so `&nbsp;` becomes `\&nbsp;` and pandoc emits
   the literal text. **There is no configuration in which writing an entity here works**, which is
   why it is a gate and not advice. Verified against the real pre-fix source from git: all 32
   occurrences caught at exact line/column, and silent across all 128 live master files.
2. **`engineering/tools/validation/audit-tex-artifacts.py`** — new. Sweeps the returned `.tex` (the
   only artifact showing what LaTeX actually received) for entities, raw HTML, literal markdown,
   double-escapes, `{=latex}` leaks, `??`, TODO markers. Tuned to **zero false positives** across
   all eight outbound `.tex`; its exclusions are load-bearing and documented in the script header.
   Wired into `release-manual` as step 1e0.
3. **`release-manual` no longer says to ignore overfull hboxes.** That instruction is what let F-284
   ship: a 50.2pt overfull hbox was the defect's only signal, and the skill said to disregard it.
   Now triaged by magnitude and location (≥20pt, or any inside a table ⇒ open the page). Assembly's
   log carries 7,056 overfulls of which 36 are ≥20pt, so ranking is tractable where listing is not.
4. **`release-manual` 1d′ — read the whole page you opened.** F-285 cost nothing because it sat on
   F-284's page; a narrowly-scoped check would have passed it through again.

### F-288 — an effect group in slash form is shaped exactly like a dual mnemonic, so 16 syntax forms print split across two lines. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). All 16 forms print on one line each — `TESTP {#}Dest WC/WZ`, `TESTP {#}Dest ANDC/ANDZ`, and the TESTB/TESTBN/TESTPN sets beside them.


**Found:** 2026-08-17, during release verification of Assembly v3.1.6. Found by **reading the whole
of p.329** while confirming the F-285 repair — the repair itself is correct; this was the rest of the
page. (Third time in two days that the free evidence on an opened page carried the next defect.)

**Reader impact.** In the TESTB, TESTBN, TESTP and TESTPN entries — four syntax forms each, **16
lines** — the flag-effect group is orphaned onto its own line, with vertical gaps between the pairs:

```
TESTP {#}Dest          instead of      TESTP {#}Dest WC/WZ
WC/WZ                                  TESTP {#}Dest ANDC/ANDZ

TESTP {#}Dest
ANDC/ANDZ
```

In a reference manual's syntax block a form split across two lines reads as **two different forms**,
and these four instructions are exactly where a reader goes to learn which effects each accepts.

**Mechanism (code-verified, not inferred).** `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-entry-format.lua`
inserts `\\` before every bold run that matches an instruction-mnemonic *shape*, one shape being
`^[A-Z][A-Z0-9_]*/[A-Z0-9_]+$` — intended for dual mnemonics like `CALL/RET`. **`WC/WZ`,
`ANDC/ANDZ`, `ORC/ORZ` and `XORC/XORZ` are character-for-character that same shape**, so each was
taken for a new mnemonic and given a break *before the effects*. The filter did try to exclude
effect flags — `not text:match("^{")` — but that only catches the **brace** form `{WC|WZ|WCZ}`,
which is precisely why TEST and TESTN, written that way, always rendered correctly while their
neighbours did not.

**Wider than the 16 visible lines.** The bare forms — `WC`, `WZ`, `WCZ`, `ANDZ`, `ORZ`, `XORZ`, nine
further sites — match the plain-CAPS shape and carried the same latent bug.

**The F-285 repair did not cause these defects — it ACTIVATED them.** (Corrects a first reading that
called it unrelated.) `is_syntax_paragraph()` rejects any paragraph containing a top-level word, and
the literal `&nbsp;` was exactly such a word — so in v3.1.5 the filter **never fired on these
paragraphs at all**, and the four tight lines came from pandoc's hard breaks alone. Removing the
entities made the paragraph parse as a syntax block for the first time, and the filter's latent bugs
took effect. The bugs predate v3.1.5; their visibility does not. Verified against the released v3.1.5
PDF recovered from git.

**A SECOND defect, found by reasoning about what the re-render would show before spending it.** Once
the effect-group breaks were fixed, the four forms would still have been separated by BLANK LINES:
the filter inserts `\\` before each mnemonic **unconditionally**, while the source already ends each
form with a trailing `\` — a markdown hard break pandoc renders as `\\`. The two compose to
`\\\\`, a blank line between every syntax form. The filter now honors an existing `LineBreak` and
supplies one only when the source lacks it — which preserves the reason the filter exists (forms
written on separate source lines with no hard break still get their break).

**Fix applied.** Shape-matching cannot separate these cases; **membership** can. A single
`is_mnemonic()` predicate now decides by membership in an explicit `EFFECT_FLAGS` set (handling the
brace, slash and bare forms), and **both** loops — the mnemonic count and the break insertion — call
it, so the two can never disagree about what a mnemonic is. Verified against the real token
inventory: `WC/WZ`/`ANDC/ANDZ`/`ORC/ORZ`/`XORC/XORZ`/`WC`/`WZ`/`WCZ` are not mnemonics, while
`CALL/RET`, `ABS`, `ADDCT1`, `MUL / MULS` still are. No PASM2 instruction is named `WC`, `ANDC`,
`ORC` or `XORC`, so there is no collision — and `WRC`/`WRZ`, which ARE instructions, are absent from
the flag set and stay mnemonics. Both copies of the filter (workspace + interactive-testing) fixed
and confirmed identical.

**Same class as F-286**, one day apart: a guard written for one shape, left to cover a family. The
countermeasure is the same — one predicate, one place, used by every caller.

**PROVEN ON THE FORGE DAEMON, not merely reviewed** (run `f288-syntax-v1`, 2026-08-17). A five-case
fixture was rendered and READ: the four slash-form `TESTP` forms print one per line with no gaps; the
`{WC|WZ|WCZ}` control is unchanged; bare `WC`/`WZ`/`WCZ` print inline; **and both no-regression cases
hold** — forms written without a hard break still receive an inserted break (the filter's actual
purpose), and `CALL/RET`, `WRC`, `WRZ` are still treated as mnemonics. Compile log clean on all five
serious signatures. This is what a Lua change with no local interpreter requires: the daemon, not a
code read.

**Owed:** one Assembly render (staged). **Assembly v3.1.6 is HELD from the release wave** until p.329
shows the four TESTP forms each on one line in the production build; deSilva, P2AN001 and P2AN002 are
unaffected (this filter is Assembly-local) and release without it.

### F-289 — the code-line gate skipped every CAPTIONED code block, so it reported clean on the manual whose pages were losing channels. `RESOLVED — gate repaired and all 11 IOSP sites brought under K 2026-08-17; VALIDATED ON THE RENDERED PAGES p163 + p178 of released v1.0.9, 2026-08-25 («#302»)`

**Found:** 2026-08-17, asking a plain status question about Debug Window and IOSP while waiting on the
Assembly render. Debug Window's code-line audit reported **clean** at K=76; measuring the same files
by hand found **29 code lines over 76 columns, the worst at 137 and 130** — both longer than any line
F-281 named. A gate that silently passes is worse than no gate: nobody goes looking.

**Mechanism.** `audit-code-line-length.py`'s `is_code_fence()` returned False for **any** fence info
string starting with `{`:

```python
# ```{=latex} / ```{=html} / ```{.foo} attribute syntax -> not a plain code box
if info.startswith('{'):
    return False
```

Only `{=format}` is a raw passthrough. Pandoc **attribute** syntax —
```` ```{.spin2 caption="ch07-scope-three-channel.spin2"} ```` — IS a code box, and it is the
**captioned** form: exactly the form paired with an `examples-library/` file under the byte-identity
rule. So the gate excluded the blocks that carry the shipped examples.

**Fleet exposure: 56 captioned blocks were never gated** — Debug Window 34, IOSP 15, Getting Started
4, deSilva 3.

**This is how F-281 shipped.** Both Debug Window lines that lose a whole channel on the page
(`ch07-scope.md:272`, 121 cols → the third SCOPE channel; `ch06-logic.md:310`, 113 cols → the third
LOGIC channel and the closing paren) sit in captioned fences. The gate declared the manual clean
while two of its pages were dropping code.

**Fixed:** skip only `{=`. The `{=latex}` exemption still holds — verified: `ch03-term.md:73` (137
cols) and `ch05-plot.md:784` (130 cols) are raw passthrough and are correctly still ignored.

**The true picture, now that the gate measures what it claimed to:**

| Manual | over K=76 | past the ~101-col render cliff |
|---|---|---|
| Debug Window (v1.1.2 released) | 24 | **3** — the F-281 trio |
| IOSP (v1.0.8 released) | 11 | **2 — NEW, and shipped** |
| deSilva · Assembly · Streamer · XBYTE · Architect · Getting Started | 0 | 0 |

**TWO SHIPPED IOSP TRUNCATIONS, verified on the released PDF by rendering the pages and looking:**

1. **p178** (`chapter-11-serial-transmit.md:433`, 103 cols) — `reversed := value REV 7` keeps its code,
   but the trailing comment runs past the code box's right border and is cut at the page edge:
   *"...for MSB-first (REV n covers bits 0.."* — the closing `n)` is gone.
2. **p163** (`chapter-10-dac-output.md:462`, 102 cols) — `WXPIN(AUDIO_PIN, …)` keeps its code; the
   comment is cut mid-word at *"a 256-clock multipl"*.

**Severity: below the F-281 SCOPE/LOGIC cases.** In both IOSP sites the CODE is intact and only a
comment tail is lost, so no reader can build a wrong program from them — but the line visibly
breaches the box border, and a truncated explanatory comment is still a reader-facing defect in a
published manual. Neither is a regression: both predate v1.0.8 (`git diff` against the tag shows the
lines unchanged).

**A first-match verification nearly missed this**, twice in one investigation: `reversed := value REV
7` appears on **p175 and p178**, and p175 (a different method, comment moved above the code) renders
perfectly. Checking only the first hit would have cleared a defect two pages later — the same trap
as F-284's `Parity of (D & S)` resolving to p414 instead of the instruction pages.

**Action:** both IOSP sites are repaired by the sanctioned comment fix (move it above the instruction,
as `spi_tx_msb_first` on p175 already does — the manual's own neighbouring example shows the form).
Rides IOSP **v1.0.9**, which is already owed a CHANGELOG entry. Debug Window's trio and its 21 other
over-budget lines ride **v1.1.3**. *(This sentence originally added "and the `breaklines` platform fix
may change what re-authoring is still needed there." It does not — `breaklines` was **REJECTED** later
the same day, see [[F-281]]. Nothing at render time rescues an over-wide line; authorship plus this
repaired gate is the whole mechanism. Corrected 2026-08-19.)*

**Done 2026-08-17 — and the scope was 11, not 2.** Repairing only the two cut sites would have left
nine lines over budget, one of them (`chapter-07-pulse-transition.md:306`, **88 cols**) past the
86-column box border and therefore already spilling into the margin — a visible defect, not a lucky
one. All 11 were brought under K=76 by the sanctioned form: standalone comment blocks rewrapped,
trailing comments moved to their own line above the instruction. Five captioned examples changed in
lockstep with their masters.

**Verified, not assumed:** code-line gate clean across all 30 IOSP masters (was 11 failures);
`verify-example-corpus-identity.py` GREEN 15/15; all five changed examples compile clean under
`pnut-ts -d`. **`pdftotext` reported the p163 comment complete while the rendered page cut it
mid-word at "multipl"** — the text object exists off-page, so extraction is not evidence of what
prints. The page image is.

> **CLOSED 2026-08-25 («#302») — CONFIRMED ON THE PAGE, not on the changelog line.** IOSP
> **v1.0.9** rendered and released 2026-08-18 (`deliverables/documents/DOCs/P2-IO-and-Smart-Pins-User-Guide.pdf`,
> 396pp). Both sites this finding left owed were **rasterised at 150dpi and looked at**, because
> this entry's own lesson is that `pdftotext` reported the p163 comment complete while the page cut
> it mid-word:
>
> - **p163** (`Chapter 10: DAC Output`, Example 2) — the three-line comment *"Initialize audio DAC.
>   The PWM-dither sample period must be a multiple / of 256 clocks, so 44.1 kHz is not exactly
>   achievable: truncating the / period to 4352 clocks yields ~46 kHz (200 MHz / 4352)."* sits
>   **above** the instruction and every line ends inside the code box. The `' Period, rounded down
>   to a 256-clock multiple` line — the one that used to be cut at *"multipl"* — is complete.
> - **p178** (`Chapter 11: Serial Transmission`, Example 2) — `' MSB first: reverse the 8 data bits
>   (REV n covers bits 0..n)` prints in full, closing paren included, with `reversed := value REV 7`
>   on its own line below it.
>
> **The first-match trap this entry warned about was honoured:** `reversed := value REV 7` occurs on
> **both** p175 and p178 in v1.0.9, and p178 — the later, formerly-broken one — is the page verified.
>
> **The repaired gate is still clean at source:** `audit-code-line-length.py` over all 30 IOSP
> masters exits 0, "no code line over K=76" (was 11 failures). Debug Window's masters likewise exit 0.

**Owed: nothing.**

### F-290 — nothing continues a `debug()` directive line: the Spin2 `...` and CON symbols both compile clean and ship a different program. `RESOLVED` — **mechanism established 2026-08-17; guidance corrected at ALL THREE touch points 2026-08-25 («#302»); the repaired line verified on the released page**

**Found:** 2026-08-17, looking for a way to bring `ch06-logic.md:310` (113 cols) under K without
losing what the example teaches. Both candidate fixes were compiled and the emitted binary inspected
rather than trusted.

**A `debug()` backtick directive is a LITERAL STRING assembled at compile time. It is not Spin2
source, so no Spin2 syntax applies inside it.** Two consequences, each verified by compiling with
`pnut-ts -d` and reading the directive text back out of the `.bin`:

| Attempt | Compiles | Bytes | What actually shipped |
|---|---|---|---|
| baseline | ✅ | 9,482 | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00` |
| Spin2 `...` continuation | ✅ | **9,438** | `LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 ...` — **`...` embedded literally and ALL THREE CHANNELS DROPPED.** The window would be created with zero declared channels. |
| colors as `CON` symbols | ✅ | 9,476 | `'CS' 1 C_CS …` — **symbol names embedded verbatim, never resolved.** The PC-side `KeyColor` cannot read `C_CS`, so every channel silently falls back to `DefaultScopeColors`. |

Only the `` `(expr) `` form substitutes a value into a directive; a bare token is text.

**PROCESS DEFECT THIS EXPOSES — `prepare-manual`'s sanctioned fix is wrong for this line class.**
The code-line gate's guidance reads: *"for a **code** overflow, break at a logical boundary with the
legal Spin2 `...` line-continuation."* That is correct for ordinary Spin2 statements and **silently
destroys a `debug()` directive** — which is the majority of the over-long lines in the Debug Window
manual, i.e. exactly the population the guidance is aimed at. Corrected in the prepare-manual
project overlay.

**Same family as the trailing-`-` trap** already recorded under F-281 (compiles clean, 9,338 vs 9,408
bytes). The generalization is now explicit rather than one anecdote: **a `debug()` directive line
cannot be continued at all — it can only be shortened.** Byte-comparing the binary against the
one-line form is what catches it; the compiler never will.

**Applied to the LOGIC line (F-281, agreed with Stephen):** the create line drops `TITLE`, `SAMPLES`
and `SPACING`, reaching **70 cols** and keeping all three named channels with their exact hex colors:

```
  debug(`LOGIC SPIbus 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00)
```

Costs nothing pedagogically — **checked, not assumed**: Chapter 6 already teaches all three dropped
keywords 250 lines earlier (a table row each at 69–72, prose deriving `SAMPLES × SPACING` = window
width at 87–89, and a prior worked example using `SAMPLES 64` at line 46). The over-long line sits in
*"A complete software-only example"*, whose job is the SPI flow, not re-teaching configuration. No
published figure is tied to that example, so nothing needs regenerating. Verified: compiles clean
under `pnut-ts -d`, the emitted directive carries all three channels, and the printed block is
byte-identical to `examples-library/ch06-logic-spi-bus.spin2`.

**Also ruled out, and left as a bench question:** dropping the explicit `1` counts. `LOGIC_Configure`
reads the next token as `count` via `KeyValWithin(v, 1, 32)` **before** reading the color, and whether
a failed count consumes the token is not determinable from the manual's REF. If it consumes, the color
is lost silently. Not usable without a PNut/bench check — which is also why the explicit `1` is
probably load-bearing in every channel declaration in the manual.

**Debug Window's remaining line work:** 23 lines over K=76, **2 still past the ~101-col cliff** —
`ch07-scope.md:272` (121, the SCOPE channel case, source-determined split available) and
`ch14-multiwindow-pasm.md:299` (110, trailing comment only, comment-above fix).

> **CLOSED 2026-08-25 («#302»). The mechanism half was done on 2026-08-17; the GUIDANCE half was
> only half done, and that is what this closure completes.**
>
> **The guidance defect was still live in the place a reader actually reaches.** This entry recorded
> the fix as *"Corrected in the prepare-manual project overlay"* — and it was. But
> the `prepare-manual` skill (agent-side) still stated the destroying rule **twice, unqualified**:
> `:194` (Step 4, code-line gate) — *"for a code overflow, break at a logical boundary with the
> legal Spin2 `...` line-continuation (or aggregate into a named CON)"* — and `:201` (Step 5,
> compile certification) — *"A long line is shortened with the legal Spin2 line continuation `...`
> … (verified: compiles to the identical value)"*, whose verification is exactly the clean-compile
> this finding proves is worthless here. A rule stated correctly in the overlay and incorrectly in
> the body is the drift shape this project already named: **three touch points, and only one was
> fixed.** Both now carry the `debug()` carve-out inline and point at the overlay for the evidence.
>
> **The manual-side line is verified on the artifact, not the changelog.** The repaired form is
> byte-identical across all three places it must agree:
> - master `ch06-logic.md:311`
> - `examples-library/ch06-logic-spi-bus.spin2:25`
> - **released v1.1.3 PDF** (`P2-Debug-Window-Manual.pdf`), which prints
>   `` DEBUG(`LOGIC SPIbus 'CS' 1 $00FFFF 'CLK' 1 $00FF00 'MOSI' 1 $FFFF00) `` — all three named
>   channels with their exact hex colors, the outcome the `...` form destroyed.
>
> **Both cliff lines are gone at source:** `audit-code-line-length.py` over the Debug Window masters
> exits 0, "no code line over K=76" — so the 23-over-budget population and both >101-col cases are
> closed, not merely reduced.
>
> **The bench question is NOT closed by this entry and is deliberately carried:** whether a failed
> `KeyValWithin(v, 1, 32)` count consumes its token is still undetermined, so the explicit `1` in
> every channel declaration stays load-bearing and must not be dropped to save columns.

### F-291 — the escaper missed two code contexts, so five lines of a released manual print a literal backslash. `RESOLVED` — **escaper fixed + sweep extended 2026-08-17; BOTH RELEASED PAGES CONFIRMED CLEAN in v1.1.3, 2026-08-25 («#302»)**

**Found:** 2026-08-17, testing F-278's deferred question (does `> ```antipattern` render inside a
blockquote?) on the daemon before risking a production render. The answer is **yes** — but the test
page showed the code inside the blockquote as `DEBUG(\`SCOPE\_XY W 128 'A')`, with a literal
backslash, while the identical pair *outside* the blockquote rendered `SCOPE_XY` correctly.

**Five lines are affected in the RELEASED Debug Window v1.1.2**, verified by extracting the shipped PDF:

| Page | Prints | Context |
|---|---|---|
| p88 | `DEBUG(\`SCOPE\_XY W 128 'A')` and the `W SIZE` line beside it | fenced block **inside a blockquote** |
| p159 | `PC\_KEY`, `PC\_MOUSE`, `DEBUG\_END\_SESSION` | **double-backtick** inline spans |

**Mechanism — two blind spots in `latex_escape_processor.py`, both proved by probe:**

| Context | Before | Correct? |
|---|---|---|
| prose | escapes `_`→`\_` | ✅ right |
| `` `single span` `` | protected | ✅ right |
| ``` ``double span`` ``` | **escaped** | ❌ → p159 |
| fenced block | protected | ✅ right |
| `> ` fenced block | **escaped** | ❌ → p88 |
| quoted prose | escapes | ✅ right |

1. **Fence detection was not blockquote-aware.** It tested `line.strip()`, which leaves the `> ` in
   place, so `> ```spin2` never registered as a fence; the body was treated as prose and escaped.
   Fixed by stripping leading blockquote markers before the fence test only — quoted *prose* must
   still escape exactly like unquoted prose, and it does.
2. **Double-backtick spans were unmatched.** The inline pattern is `(?<!`)(`[^`\n]+`)`: its body
   excludes backticks and it refuses a preceding backtick, so ``` ``DEBUG(`Name `PC_KEY(@v))`` ```
   — the form used precisely *because* the content contains a backtick — fell through to prose.
   Fixed by protecting double-backtick spans before single ones.

**Why the escaped character PRINTS rather than escaping:** both contexts still render verbatim
downstream, and inside verbatim `\_` is two literal characters. The escape was never wrong in
LaTeX terms; it was applied where LaTeX rules do not apply.

**`audit-tex-artifacts.py` (F-286) MISSED this, and now does not.** The sweep excluded verbatim
regions wholesale — correct for every other check, since code legitimately contains almost every
signature. But *inside* verbatim a backslash-escaped special is the one thing that IS a defect, so
the sweep now scans verbatim for exactly `\_ \& \# \% \$`. Verified it flags the leak and does
**not** flag legitimate PASM2 `#\label` (that is `\l`, not in the set) or correct prose escaping.
**A skip-list is an assumption, and this one had a hole in it.**

**Fixed and verified:** the staged Debug Window markdown now carries `SCOPE_XY`, `PC_KEY`,
`PC_MOUSE` and `DEBUG_END_SESSION` clean in their code contexts, while prose occurrences still
escape correctly (38 legitimate `\_` remain, all prose).

**F-278's deferred site is now converted.** With the fence-in-blockquote combination proven to
render — red antipattern box, correctly indented inside the quote, trailing quoted prose intact —
`ch08-scope-xy.md`'s wrong/right pair is split: the wrong form is an `antipattern` block, the
correct form a `spin2` block beside it, matching the Chapter 12 treatment. Rides v1.1.3.

> **CLOSED 2026-08-25 («#302») — measured on the RELEASED v1.1.3 PDF with the same instrument that
> found the defect.** This finding was detected by extracting the shipped v1.1.2 PDF and counting
> literal `\_`; the count was **5**. Re-run over `P2-Debug-Window-Manual.pdf` at v1.1.3: **0**, in
> all 168 pages. Both named pages were then rasterised and looked at (the page numbers moved by one
> between releases, so they were re-located by content rather than reused):
>
> - **p87** (was p88) — `` DEBUG(`SCOPE_XY W 128 'A') `` prints a clean underscore, inside the red
>   antipattern box, with `' WRONG -- 128 follows no keyword` beside it. The fence-in-blockquote
>   combination and F-278's conversion both render as designed.
> - **p159** — `PC_KEY`, `PC_MOUSE` and `DEBUG_END_SESSION` all print clean underscores in the
>   Appendix A command list, including inside the double-backtick spans that were the second blind
>   spot.
>
> **The extended `audit-tex-artifacts.py` sweep is the durable half** and is unaffected by this
> closure: it now scans verbatim regions for exactly `\_ \& \# \% \$`, which is what makes this
> class visible at source instead of only on a returned PDF.

### F-292 — six printed snippets teach a `...` continuation inside `debug()`, so each one silently ships a different program. `RESOLVED — all six repaired 2026-08-17 and shipped in Debug Window v1.1.3; ALL SIX PRINTED SNIPPETS CONFIRMED ON THE PAGE 2026-08-25 («#302»)`

**Found:** 2026-08-17, answering "any more outstanding issues with this manual?" after F-290
established that a `debug()` directive cannot be continued at all. Searching the masters for the
pattern found six.

**Proved, not inferred.** The ch07 snippet compiled exactly as printed emits
`Waves 'Sine'  -1000 1000 100   0 0 $00FF00 ...` — **the `'Tri'` and `'Noise'` channels are gone**
and the literal `...` is embedded (9,328 vs 9,393 bytes). A reader who copies it gets a one-channel
scope where the page shows three.

| Site | Reader silently got | Route taken | Authority |
|---|---|---|---|
| `ch07-scope.md:109` | 1 of 3 SCOPE channels | three separate feeds | `SCOPE_Update` accepts a channel def and `vIndex` only resets in `SetDefaults` |
| `ch09-fft.md:163` | `'Left'` only, no `'Right'` | two separate feeds | `FFT_Update` accepts "CLEAR/SAVE/PC_KEY/PC_MOUSE **+ channel-defs** + samples" |
| `ch04-bitmap.md:144` | palette truncated at entry 7 | LUTCOLORS as its own feed | REF: "Replace LUT palette entries at runtime"; the house form is proven by generator `fig-13-packed-bitmap-frame.spin2` |
| `ch03-term.md:166` | colour pairs 2 and 3 lost | one line (`SIZE` dropped to fit) | `COLOR` is **config-only** for TERM — no `key_color` arm in `TERM_Update` |
| `ch10-spectro.md:145` | everything after `TRACE 12` lost | one line + waiver | `SPECTRO_Update` accepts only CLEAR/SAVE/PC_KEY/PC_MOUSE |
| `ch10-spectro.md:166` | everything after `TRACE 8` lost | one line + waiver | same |

**Verified by compiling all six fixed forms together and reading the emitted directives:** every
channel, colour pair and config keyword is present, and **zero** literal `...` remain in the binary.

**Why every gate missed them, and this is the transferable part.** These are *uncaptioned*
illustrative snippets — not paired with an `examples-library` file, so never compiled — and each
PHYSICAL line was short, because the `...` is what made them fit. So the width gate saw nothing and
the compile gate never ran. **The defect lived exactly in the gap between "too wide to print" and
"too broken to run", and neither gate covers it.** Extending compile certification to uncaptioned
fragments is a real question (fragments must be wrapped to compile) and is deliberately NOT decided
here.

**One pedagogical change, flagged rather than buried:** `ch04-bitmap.md`'s palette demo moves from
LUT4 with sixteen entries to **LUT2 with four** (pixels `& $03`), because sixteen `$RRGGBB` values
cannot fit a printable line by any means — `LUTCOLORS` overwrites from index 0, so it cannot be split
across messages either. The teaching survives intact (LUT mode, inline palette in one statement,
pixels as indices) at a smaller scale. The chapter's LUT-mode reference table still documents LUT4 as
4 bits / 16 entries.

**It also closes a punch-list question open since June.** The "Other" section asked whether the
original `fig-07` failure — a creation-line channel def drawing an empty "Channel 0" plot — "came
from a `...` line-continuation artifact." It did. The creation-line-versus-separate-feed debate was
chasing the wrong variable; the `...` was dropping the channels, so the REF source was right all
along and the TO-RECONCILE item closes on evidence rather than another capture.

> **CLOSED 2026-08-25 («#302») — every one of the six read off the RENDERED PAGE of the released
> Debug Window **v1.1.3** (`P2-Debug-Window-Manual.pdf`, 168pp, cover states "Version 1.1.3"). Pages
> rasterised at 130dpi and looked at, not extracted:
>
> | Site | Page | What the page now prints |
> |---|---|---|
> | `ch07-scope.md:109` | **p76** | all **three** SCOPE channels — `'Sine'`, `'Tri'`, `'Noise'` — as three separate feed lines under the create line |
> | `ch09-fft.md:163` | **p97** | both `'Left'` **and** `'Right'` declared, then the interleaved sample loop |
> | `ch04-bitmap.md:144` | **p35** | `LUTCOLORS $000000 $FF0000 $00FF00 $0000FF` — the whole 4-entry LUT2 palette in one statement, pixels `& $03` |
> | `ch03-term.md:166` | **p27** | all eight `COLOR` values on one line, closing paren inside the box; the two comment lines above name all four pairs |
> | `ch10-spectro.md:145` | **p106** | `SPECTRO Vert … TRACE 12 RANGE $20000 HSV16X LOGSCALE` — everything after `TRACE 12` present |
> | `ch10-spectro.md:166` | **p106** | `SPECTRO Slow … RATE 512 TRACE 8 RANGE $80000 LUMA8X` — everything after `TRACE 8` present |
>
> **Zero literal `...` continuations remain in any `debug()` directive across the masters.** Swept
> all 26 Debug Window master `.md` files: five lines end in `...` and **none is a directive** — a Spin2
> *expression* continuation in an ordinary assignment (`ch13-packed-data.md:189`, legal), a syntax
> notation (`ch05-plot.md:499` `SPRITEDEF … pixels... colors...`), two elision markers
> (`ch15-panels.md:305`, `ch12-bidirectional.md:75`) and a comment (`ch01-foundation.md:261`).

**Next finding ID after this block: F-295.**

---


### F-294 — a backtick inside a single-backtick span inverts every code span after it, printing seven lines of prose as code. `RESOLVED — span repaired at source 2026-08-17; p84 CONFIRMED ON THE RENDERED PAGE of released v1.1.3, 2026-08-25 («#302»)`

**Found:** 2026-08-17, in the same Debug Window v1.1.3 audit as F-293 — by opening p84 because the
compile log's largest overfull (57.66pt) pointed there.

**What p84 prints.** The whole "Try it" paragraph of Chapter 7 is wrecked: a sentence-initial stray
`.`, a font that flips to monospace mid-sentence and stays there for two lines of ordinary prose
(*"and observe the waveform stand still instead of scrolling. Finally, vary the trigger"*), then
words fused without spaces — `triggeroffsetbetween0,SAMPLES/2,` and `ANDSAMPLES-1'` — and a stray
closing quote. It is the most visibly broken paragraph in the manual.

**Mechanism.** `ch07-scope.md:474` wrote a **single**-backtick span whose body contains a backtick:

    (`debug(`Waves TRIGGER 0 -500 500 256)`)

Pandoc closes a single-backtick span at the *first* backtick it meets, so the span is `debug(`; the
next backtick **opens** a new one that runs until the backtick before `offset`, swallowing two lines
of prose. Every span in the rest of the paragraph is then inverted — code reads as prose, prose reads
as code — which is exactly what the page shows.

**Fixed** by the double-backtick form this manual already uses precisely for backtick-bearing content
(the same form F-291 protected in the escaper): ``` (``debug(`Waves TRIGGER 0 -500 500 256)``) ```.
Verified balanced.

**Swept fleet-wide.** All 155 master files, paragraph-wise (a code span may legally wrap across
lines, so a line-wise check false-positives on four innocent sites). **This is the only real
occurrence.** Two other flagged paragraphs are `CONVENTIONS` authoring headers inside `<!-- -->` in
the Architect and Getting Started masters — confirmed absent from both shipped PDFs.

**⚠️ This overfull was on record as adjudicated and benign.** It was carried as *"the 57.66pt overfull
is an unbreakable `\lstinline` prose run, not a code line"* — which is mechanically true and entirely
misleading: the run is unbreakable **because a span inverted**, and the paragraph around it is
broken. The note explained the symptom accurately enough to stop anyone opening the page. **An
explanation is not a verification**, and "already adjudicated" is exactly the label that keeps a
defect alive — the second time in one audit that a status line was wrong (see F-293 on Assembly).

**Gate gap.** No gate we own sees this: the escaper hands the span through, `audit-tex-artifacts.py`
sees legal `.tex`, the code-line gate measures code blocks, and the compile is clean. The only signal
was an overfull box that had been explained away. A paragraph-wise backtick-balance check on the
masters is the missing instrument.

> **CLOSED 2026-08-25 («#302») — p84 rasterised and READ, because this defect is a font change and
> text extraction cannot see one.** In released **v1.1.3** the whole "Try it" paragraph reads as
> prose in the body face, with only the genuine code spans set in monospace: `Sine`, `-1000 1000`,
> `AUTO`, `qsin`, `` DEBUG(`Waves TRIGGER 0 -500 500 256) ``, `offset`, `0`, `SAMPLES/2`,
> `SAMPLES-1`. **Every symptom this entry listed is gone** — no sentence-initial stray `.`, no
> monospace run through *"and observe the waveform stand still instead of scrolling. Finally, vary
> the trigger"*, no fused `triggeroffsetbetween0,SAMPLES/2,` or `ANDSAMPLES-1'`, no stray closing
> quote. The span inversion is fully unwound.
>
> **The double-backtick form held through the render**, which is what the fix depended on and had
> never been observed end-to-end.
>
> **THE GATE GAP THIS ENTRY NAMES IS ALSO CLOSED — and the first draft of this note said the
> opposite, which is worth recording.** This closure was initially written as *"a paragraph-wise
> backtick-balance check on the masters remains unbuilt"*. **Checked against the disk instead of
> against this entry's prose: `engineering/tools/validation/audit-backtick-balance.py` exists**,
> its docstring opens *"WHY THIS EXISTS — F-294"*, and it implements exactly the specified
> instrument, paragraph-wise for exactly the stated reason (a code span may legally wrap across a
> newline). Run over **every** manual `opus-master` tree: **CLEAN, exit 0.**
>
> ⚠️ **But it was BUILT AND NEVER WIRED.** No skill invoked it — `grep` over the skill set
> returned nothing but the file itself. It had to be run by hand, and nobody had. **A gate nobody
> invokes is a gate that does not exist**, which is F-301's defect in a different costume: a
> correct artifact that is not where the decision gets made. **Now armed** as
> `prepare-manual` **Step 6b**, beside the width/compile/ASCII source gates, so it runs before a
> render is spent rather than after a page ships wrecked.

**Owed: nothing.** Page validated; the declared instrument exists, is clean, and is now armed.


### F-293 — the escaper pre-escapes `^`, so eight exponent expressions across three manuals print a literal `^{}`. `RESOLVED — all three manuals VALIDATED on their released PDFs; the last site closed 2026-08-25 («#302»)`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). `^{}` appears **zero** times across all 502 pages, closing the Assembly rows (p93, p209, p284 x2, p350).
>
> **THE IOSP SITE WAS ALREADY CLOSED WHEN THIS ENTRY SAID IT WAS OWED — 2026-08-25 («#302»).** This
> entry predicted the site "absorbs the escaper fix at its next render"; **that render happened on
> 2026-08-18** (IOSP v1.0.9), eight days before anyone checked, and the entry was never advanced.
> A status line lying in the *hides-work-that-is-done* direction, which is the harder direction to
> notice.
>
> **Measured, then looked at.** `^{}` across **all 15 published PDFs in `deliverables/documents/DOCs/`:
> zero, in every one** — not just the three manuals this finding named. **IOSP p320** was then
> rasterised: *"period = 2^X[3:0]^ clocks"* prints as a **true raised superscript**, no braces, no
> circumflex — the notation the entry's 2026-08-17 decision standardised on. (`chapter-16-adc.md:601`
> writes the same expression inside a **code span**, where the literal caret is correct and
> deliberate; it is not a residual site.)
>
> **The deliberate exclusion still stands:** `p2-pasm-desilva-style/opus-master/CHANGELOG.md:98`
> (`2^x`) renders into no PDF and is released history — untouched.


**Found:** 2026-08-17, auditing the Debug Window v1.1.3 render. p107's bullet reads
`multiplies the FFT output by 2^{}shift` — braces on the page.

**Eight sites, verified by extracting the shipped/staged PDFs — not inferred from source:**

| Manual | Pages | Prints |
|---|---|---|
| Debug Window (v1.1.3, staged) | p104, p107 | `2^{}shift` |
| **Assembly (v3.1.6, rendered + marked releasable)** | p93, p209, p284 ×2, p350 | `2^{}x`, `2^{}128`, `2^{}32-1`, `2^{}32` |
| IOSP (v1.0.8, RELEASED) | p320 | `2^{}X[3:0]` |

**Mechanism — a double escape, and the sources are innocent.** Every master writes plain `2^shift`
/ `2^32`. `latex_escape_processor.py` replaced a bare `^` with `\^{}` in the *markdown*; Pandoc then
read `\^` as an escaped literal caret (emitting `\^{}` itself) and escaped the two braces it found
next, producing `\^{}\{\}` — which xelatex prints as `^{}`. The escape was correct LaTeX applied one
stage too early.

**The file already carried the right precedent and did not follow it.** Line 435: *"Don't escape
tildes - Pandoc handles them fine in markdown."* A bare caret is the identical case. The caret path
even had a comment naming the failure — *"If we escape ^ to `\^{}`, Pandoc outputs literal `^{}`
which breaks LaTeX"* — but the guard built from it only protects **matched** `^text^` superscript
pairs. Unmatched carets, which is how every one of these eight is written, fell straight through.

**Fixed in three places, not one.** The prose path plus two latent copies of the same bug — the
markdown-header path (whose `XPROTECT_CARET_X` dance defends the escaper against *itself* while
leaving Pandoc's second pass untouched) and the `\section{...}` content path. No master file changed;
fixing the tool fixes all eight sites at next render.

**Matched superscript pairs are unaffected** — `2^32^` in IOSP still resolves to true superscript.
That is why IOSP shows one broken site and not four.

**Owed: nothing.** ~~re-render Debug Window, Assembly and IOSP, then confirm the listed pages print a
caret and no braces~~ — **all three rendered and all three confirmed** (Debug Window v1.1.3
2026-08-17, Assembly v3.1.6 2026-08-18, IOSP v1.0.9 2026-08-18; verified 2026-08-22 and 2026-08-25).
**Pandoc's handling of a bare caret is no longer "reasoned, not yet observed"** — the round-trip
happened and the observation is the zero-count across all 15 published PDFs plus the rasterised
p320. Local Pandoc remains off-limits and was not used.

**⚠️ This unblocks nothing and blocks one thing: Assembly v3.1.6 was recorded "verified, releasable,
nothing blocking." It carries five of the eight sites.** The verification that cleared it was
thorough about what it looked for — outline, page count, F-288's pages, log signatures — and this was
not on the list. **A verification pass is only as wide as its checklist**, which is the F-285 lesson
arriving a second time.

**RESOLVED 2026-08-17 — the set standardizes on true superscript.** IOSP's appendix-c wrote `2^32^`
(superscript) at lines 35 and 501 but `2^X[3:0]` (literal) at 171 — one document, one concept, two
renderings. All 8 literal sites are now pandoc superscript pairs, joining the 5 that already were:
**13 consistent exponents across three manuals**, verified by re-sweep (0 unmatched carets remain in
renderable prose). The tool fix alone would have printed a correct-but-inconsistent circumflex; the
notation decision is separate from it and is now made, not deferred.

**Left alone deliberately:** `p2-pasm-desilva-style/opus-master/CHANGELOG.md:98` (`2^x`). CHANGELOGs
render into no PDF (verified across all four), and it is a released entry — rewriting shipped history
to fix text nobody renders is churn, not quality.

### F-285 — `&nbsp;` prints literally in 16 instruction-syntax lines of a RELEASED manual. `RESOLVED`

> **VALIDATED against the released v3.1.6 PDF, 2026-08-22** (502pp, text-extracted; the render happened 2026-08-18, after the 2026-08-17 fix). `nbsp` appears **zero** times across all 502 pages.


**Found:** 2026-08-17, verifying the Assembly re-render for F-284. The F-284 fix was confirmed
good on p.326 and p.329 — and p.329 put this defect on screen at the same time. It is unrelated to
F-284 and was not caused by it.

**Location:** `part-ii/instructions-t.md` — 16 sites across the TESTB, TESTBN, TESTP and TESTPN
syntax blocks. Visible at **P2-Assembly-Language-Manual p.329** and neighbours as, literally:

    TESTP {#}Dest&nbsp;&nbsp;WC/WZ

**Mechanism.** The source writes `*Dest*&nbsp;&nbsp;**WC/WZ**`. Pandoc did not resolve `&nbsp;` as
an HTML entity; it treated the ampersand as literal text and emitted `\&nbsp;` into the `.tex`, so
xelatex prints the entity as characters. The escape script is not at fault — the workspace copy
still carries a bare `&nbsp;` — and it produces no warning or error at any stage.

**Not new, and not from the platform fix.** Introduced 2025-12-21 by `096230a4` ("Fix multi-page
tables and TESTP/TESTPN formatting"), present in the v3.1.5 tag's source, and therefore shipped in
at least v3.1.5. The F-284 filter change touches only 9-column table cells; these are body prose.

**It is a one-file anomaly, not a convention.** `&nbsp;` appears **nowhere else** in the manual —
not in the other 21 instruction-letter files, not in Part I, not in Part III. The TEST page's own
neighbouring syntax lines, four lines above the corrupted ones, use a plain space:
`**TEST** *Dest, {#}Src* **{WC|WZ|WCZ}**`. So the fix is to match the file's own surroundings.

**Fix applied:** all 16 `&nbsp;&nbsp;` replaced with a single space. No other file touched. No
version bump — v3.1.6 has not shipped.

**Owed:** one more Assembly render, then confirm p.329 reads `TESTP {#}Dest WC/WZ`.

**Lesson, and it is the same one twice in a day.** Both F-284 and F-285 are invisible to every gate
we own — clean log, no warning, correct source characters — and both were found by rendering a page
and looking at it. F-285 also shows the cheaper half: **the page you open to verify one fix is free
evidence about everything else on it.** Verifying narrowly would have missed this.
