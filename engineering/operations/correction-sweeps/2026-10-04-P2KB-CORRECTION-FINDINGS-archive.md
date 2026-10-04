# P2KB Correction Findings — ARCHIVE, swept 2026-10-04

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 4 findings carrying a `DONE` status token: F-400, F-523 (served in KB v1.23.1) and
> F-526, F-540 (both decided on the bench — EF-090, EF-091 — and served in KB v1.23.2), each
> verified served through p2kb_get on 2026-10-04.
>
> Swept by rename-then-trim: the register was `git mv`'d here (history follows this file) and
> copied back; this copy was cut to the 4 findings and the live copy had the same entries
> removed with the edit tools. Every entry below is the pre-sweep text (commit eea3efe7),
> verbatim; `audit-register-hygiene.py --sweep-check eea3efe7` proves every line is accounted for.

---

### F-526 — the KB says a PINSTART/WYPIN Yval written during reset is lost for sync serial TX `%11100`; the Silicon Doc says that is how the shifter is primed — `DONE` (bench CONFIRMED EF-090; served in v1.23.2, verified 2026-10-04 via p2kb_get)
> **Bench: `CONFIRMED` (EF-090, first run).** Prime-in-reset sent `$A5, $3C` in 5 of 5; enable-first sent `$3C, $3C` in 5 of 5 (W1 lost, W2 twice); start-stop control exact. **Applied 2026-10-04 («#379»):** `pinstart.yaml` — `%11100` removed from the lost-Yval list and stated as the opposite case (a reset-time word primes the shifter; PINSTART's Yval is the first word sent); the note line likewise. `smart-pin-11100-sync-serial-transmit.yaml` — `stream_continuous` primes while DIR is low, then enables; `timing.continuous_mode` states the rule and the measured failure. **Widened in the same file (all sourced, all in its examples):** the Spin2 example routed the clock with `P_PLUS1_B` from pin 42 while declaring `CLK_PIN = 40` (pin−1) → `CLK_PIN = 42`; negative-edge clocking used `P_INVERT_A`, but the Silicon Doc inverts the **B** input ("the B input may be inverted by setting B.[3]") → `P_INVERT_B` (`$0800_0000`, compiler-checked), and the `clock_edge` note likewise; the PASM example had no clock routing at all (its own `critical_requirements` call that mandatory) and bit-pattern comments showing `BBBB=1111` for a word with B = 0 → `P_PLUS1_B` added, comments recomputed from compiled values (`$0100_0078`, `$0900_0078`), `clk_pin` 42; the inline example gained `P_PLUS1_B`. Gates: crossref 3,870/3,870, claim-sourcing Tier 1 none, constant fidelity clean, payload locator gate clean, no duplicate keys.
`language/spin2/methods/pinstart.yaml:9` lists "serial transmit (%11110, %11100)" among modes whose Yval is
lost. **The Silicon Doc (`silicon-doc-text.txt`, %11100 section after :4640):** continuous mode "a first
word is written via WYPIN during reset (DIR=0) to prime the shifter"; "During reset, the buffer flows
straight into the shifter"; "Upon release of reset, the output will reflect the LSB of the output word
written by any WYPIN during reset." EF-011 (the bench basis) tested `%00100`, `%00101` and `%11110`
only. `%11100` was added by inference when F-509 was widened («#375», mine). Same defect in
`architecture/smart-pins/smart-pin-11100-sync-serial-transmit.yaml` `stream_continuous` (:75-81): continuous
mode, "Enable FIRST", then "Prime shifter (after enable)" — the opposite of the documented continuous-mode
procedure (the first word likely goes out wrong). The start-stop example (X.[5]=1) is unaffected (WYPIN
before the first clock is documented there). **Fix:** remove `%11100` from the lost-Yval list (keep
`%11110`, `%00100`, `%00101`); restore the documented continuous-mode prime-in-reset sequence; say that
sync TX primes in reset. Found because the I/O & Smart Pins guide (ch11:292-296) had it right.
**Bench before the fix (Stephen, 2026-10-04: "should be proven on bench so we know truth").** Rig
built and compiled (pnut-ts 1.55.8): `p2-io-and-smart-pins-user-guide/audit/verification-tests/test-f526-sync-tx-prime-in-reset.spin2`
— TX P4 / CLK P5 / RX P6, internal selectors only; arm A prime-in-reset, arm B enable-first, arm C
start-stop control; pre-registered CONFIRMED / REFUTED / BOTH-WORK. Awaiting the run («#379»).

### F-540 — the KB is silent on whether a `##` (AUGS/AUGD) prefix consumes a skip-pattern bit; the XBYTE guide teaches that it does — `DONE` (bench CONFIRMED-COUNTS EF-091; served in v1.23.2, verified 2026-10-04 via p2kb_get)
> **Bench: `CONFIRMED-COUNTS` (EF-091, first run).** Under SKIP and SKIPF, pattern `%1000` landed on `add #4` (acc 9): the AUGS takes its own bit. Both characterization patterns matched the same reading exactly (`%0010` → MOV un-augmented, x `$145`; `%0100` → pending AUGS augmented the next immediate, acc `$1220D`). **The XBYTE guide is right; no guide change.** **Applied 2026-10-04 («#379»):** `pasm2/concepts/instruction_skipping.yaml` `pattern_consumption` states both facts (AUGS only — AUGD was not run, so it is not claimed), sourced in its `sources:`; the file also gained `aliases` (it had none: "skip pattern" reached nothing).
F-485 removed "AUGS/AUGD both consume pattern bits" from the KB as unsourced. The XBYTE guide
(`xbyte-body.md:321-328`, :362-366) teaches it, reasoning from the Silicon Doc's "shifted right by one bit
for each instruction encountered" (AUGS is an instruction). Neither is a cited statement. **To do:** a
bench run (SKIPF pattern over a `##` instruction) settles it; then the KB states it (sourced) or the guide
changes. Not a guide defect until then. **Rig built and compiled** (pnut-ts 1.55.8; the listing shows
exactly one `AUGS #$91` before each `MOV x, #$145`): `p2-xbyte-programming-guide/audit/verification-tests/test-f540-augs-skip-pattern-bit.spin2`
— SKIP and SKIPF, control sequence without `##` gating the bit numbering; pattern `%1000` decides (acc
9 = AUGS counts, acc 5 = it does not). Awaiting the run («#379»).

### F-523 — repo paths and `file:line` citations in shipped YAML prose — `DONE` (served in v1.23.1, verified 2026-10-04 via p2kb_get; the MCP itself still serves stripped fields — F-439)
> **Applied 2026-10-03 («#376»).** Re-measured with the real filter and a wider pattern (bare `:NNNN` cites too): **251 payload lines in 74 files**. Every citation MOVED into a stripped field in the same top-level block (`source:`/`sources:` keys; `# Source(s):` column-0 comment blocks; provenance keys renamed `path:`/`source_line:`/`*_source:` → stripped names). Widened in the same pass, same class: `extraction_metadata.source_documents` lists (10 files) → `sources:`; the `v55:NNNN` shorthand (F-400) and `v55_line:` keys; names of internal registers in prose (`SOURCE-ERRATA.md`, `P2KB-CORRECTION-FINDINGS.md`, `APP-NOTE-DESIGN-DECISIONS.md`); `source_document:` keys outside the code-example schema. **Not changed, deliberately:** the two code-example files keep `source_metadata.source_document` (the schema requires it; the value is a document name); line cites into public Parallax files (`flash_loader.spin2 line 275`) are citations a reader can follow; the schema's own example values. **Verification:** a negative-controlled structural checker against HEAD (stripped keys aside, identical structure; removed text only citation tokens; no number vanished from any file), a duplicate-key parse of every changed file, every flagged change and every comment change read by hand. It caught one slip of mine (an Edit trimmed a trailing space → `source_reference:1711`, invalid YAML), fixed before commit. Gates: payload 0 hits; crossref 3,870/3,870; claim-sourcing Tier 1 none (Tier 2 29 → 27), negative control PASS; source-lock and constant-fidelity exit 0. **Gate:** `validate_internal_ids` fails on repo paths, document `file:line`, bare `:NNNN`, `vNN:NNNN` and internal-register file names; planted-failure test catches each form and passes a decoy line. New finding while sweeping: F-525.
Found 2026-10-03 while reviewing F-519's diff. Measured with the shipped filter: **190 payload lines in
69 files** carry repo paths (`engineering/ingestion/sources/...`, 115) or document `file:line`
citations (`silicon-doc-text.txt:3854`, 58; others) in content prose, outside the stripped fields. A
consuming agent can open none of them; doctrine (provenance is for us) says the shipped entry states
the fact only. **Why it is carved out, not swept with F-519:** these citations are what
`audit-yaml-claim-sourcing.py` reads to decide whether a claim block is grounded; stripping them from
prose without moving them into a `source:` field beside each claim would disarm that gate. The fix is a
per-claim move into stripped fields, block by block, then the F-519 gate widened to repo paths and
`file:line`. **Expires:** the KB release after the one carrying F-506…F-522 — it ships in that release
or this carve-out is re-read and its reason re-justified.

## `pnut-ts` shorthand `v55:NNNN` is used as a citation across the shipped set and resolves to no file (2026-08-30, release fix pass step 3) — F-400

### F-400 — a locator form that a reader can follow and a tool cannot — `DONE` (served in v1.23.1, verified 2026-10-04 via p2kb_get: no `v55:` shorthand in pasm2-getting-started)

> **Applied 2026-10-03.** Resolved by option (a), because F-523 removed the shorthand from shipped text anyway: every `vNN:NNNN` left the payload (13 lines, `guides/pasm2-getting-started.yaml` and `guides/spin2-getting-started.yaml`), each moved into its block's `source:` naming the file (`spin2-v55-text.txt:1718`) wherever a bare number would otherwise follow a different file. That included one live instance of exactly this finding's failure: `how_to_declare: Spin2 v55 :1709-1710, :1725` sat after the datasheet path, so `:1725` bound to the datasheet. `v55_line:` keys → `source_reference:`. Count of `v(35|51|55):NNNN` across all KB YAML afterwards: **0**. The gate now fails on the form in the payload.

**Not fixed. Registered, bounded, and a definition call.**

Several files cite the Spin2 v55 documentation in a shorthand established at the top of the same block — `(v55:1709-1710, :1725)`, `v55:812`, `v55:520`. `guides/pasm2-getting-started.yaml` uses it heavily. The block always names `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` in full somewhere above, so a human reading the block resolves it without effort, and **every instance checked in the F-399 sweep resolved to the right line** (`v55:1725` is the `clkmode_` compiler-constant row, exactly what the claim needs).

**Why it is still a finding.** The shorthand is not a path. A tool walking the file binds `:1725` to whatever full path token is nearest, which is how the F-399 extractor attributed it to `p2-datasheet-text.txt:1725` — the CALL instruction row. That is the same failure mode F-399 fixed in `basic-io.yaml` by rewriting the citation, and consistency says the same fix applies here. It was not applied in this pass because the form is used widely enough (55 spin2-v55 citations, plus `v51:` and `v35:` variants) that changing it is its own sweep with its own verification, and doing half of it is worse than doing none.

**The call for whoever takes it:** either (a) expand every shorthand to a full path, or (b) declare the shorthand a supported citation form and give the resolvers a prefix table (`v55:` → `sources/spin2-v55/spin2-v55-text.txt`, and so on) so tools and readers agree. **(b) is the recommendation** — the shorthand is genuinely more readable inside a long multi-source block, and a declared prefix table makes it machine-resolvable without touching 55 citations.
