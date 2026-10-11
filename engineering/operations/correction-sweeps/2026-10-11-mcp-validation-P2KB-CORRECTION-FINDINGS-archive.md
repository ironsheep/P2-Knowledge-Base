# P2KB Correction Findings — Archive of findings closed 2026-10-11 by the close-out release MCP validation «#398»

Closed findings swept out of the live register, `engineering/operations/P2KB-CORRECTION-FINDINGS.md`
(the register carries open work only; this archive is a rename-then-trim copy of the pre-sweep
register at commit `ed0e523c`). 34 findings: F-381, F-383, F-386, F-387, F-389, F-392, F-393, F-398,
F-421, F-436, F-439, F-454, F-525, F-542, F-543, F-544, F-546, F-547, F-548, F-549, F-550, F-551,
F-552, F-553, F-554, F-555, F-556, F-557, F-558, F-559, F-560, F-563, F-568, F-570. Each sits under
the `##` section heading it was filed under.

## Found during the 2026-10 manual releases, the register reconciliation and the pre-release audit (2026-10-04/07) — F-546 … F-562 (+ F-563, found 2026-10-09 by the VO-J-035 rework; + F-564, found 2026-10-09 by «#414»; + F-565, found 2026-10-09 by «#415»; + F-566, found 2026-10-10 by «#422»; + F-567, found 2026-10-10 by «#422»/«#423»; + F-568, F-569, found 2026-10-10 by «#422»; + F-570, reported 2026-10-10 by Stephen; + F-571, found 2026-10-11 by «#398»)

### F-570 — the seven P2 errata E1-E7 could not all be found: no page listed them, and E1, E2 and E6 were reachable by no name — `RESOLVED` (reported 2026-10-10 by Stephen, applied 2026-10-10, «#422»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get "errata"` and `p2kb_get "erratum E6"` → `p2kbArchSiliconErrata` (`resolved_from` the alias), which serves all seven entries E1-E7 (title, affects, effect, rule, `related:`) and the aliases `errata`, `erratum`, `P2 errata`, `E1-E7`, `erratum E1`..`E7`, bare `E1`..`E7`; E6 reads "In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC". `p2kb_get "erratum E3"` returns only the hub, but `p2kb_find term:"erratum E3"` → `p2kbArchSiliconErrata`, `p2kbPasm2Getct`, `p2kbSpin2Getms`, `p2kbSpin2Getsec`, and the published `deliverables/ai/p2kb-index.json` carries `erratum E3` (and `ERRATUM E3`) → those same four keys (E1 → hub + `p2kbPasm2SetqBlockOps`, E7 → hub + `p2kbPasm2Rdfast`). The KB is right: the index holds both targets and the server's single-key `p2kb_get` picks the first (the hub); that is server behaviour, not a KB defect, and it is not counted against this entry.
Reported by Stephen 2026-10-10: an agent looking up all the errata could not find all of them. Measured on
the committed index (HEAD `ce07fd8f`): `errata`, `erratum`, `P2 errata` and every `erratum EN` resolved to
nothing; only `GETCT erratum E3`, `RDFAST erratum E7` and `Goertzel errata E4 E5` existed as aliases. **The
index generator is not at fault** — it stores aliases as written (and upper-cased) and lists every file that
shares one; the aliases were missing. **Applied 2026-10-10:** new hub `architecture/silicon_errata.yaml`
(`p2kbArchSiliconErrata`, category `architecture_errata`): E1-E7, each with title, what it affects, what
happens, the rule, `related:` full paths and `sources:` — E1/E2 the Parallax Propeller 2 Documentation v35
KNOWN SILICON BUGS section plus EF-067/EF-066; E3 EF-068, 075, 078-083; E4 EF-069, 076; E5 EF-070, 076; E6
EF-071 and the v35 %TT table; E7 EF-074, 077, 084, 086-088. Aliases on the hub: `P2 errata`, `errata`,
`erratum`, `silicon errata`, `E1-E7`, `erratum E1`..`E7`, bare `E1`..`E7`. Each home page
(`setq_block_ops`, `augs`, `augd`, `getct`, `getxacc`, `dds-goertzel`, `smart_pins`, `rdfast`) gains
`erratum EN` aliases, an `erratum:` label on its block and a `related:` link to the hub. **Wrong, fixed
in the same pass:** `setq_block_ops.yaml` `applies_to` said "SETQ/SETQ2 immediately followed by" a block
transfer — the opposite of the bug, which needs an ALTx/AUGS/AUGD *between* them (v35 KNOWN SILICON BUGS,
`silicon-doc-text.txt:123`); `getxacc.yaml`'s workaround claimed the zero burst does not flush under SINC2,
which no record tested (EF-076 covers SINC1; EF-072 calls the SINC2 note untested) — now "proven for SINC1
only"; the E6 block in `smart_pins.yaml` cited nothing — now EF-071 and the %TT table; `augs`/`augd` bare
`related:` names replaced by full paths. **Lookups after (throwaway regen):** `errata`, `erratum`,
`P2 errata`, `E1`..`E7` → the hub; `erratum EN` → the hub plus that erratum's home page. **Gates:** format,
claim sourcing (1006 files, 0 Tier 1), source lock PASS, duplicate keys, plain scalar, provenance key
names, index findability, crossref (4210 resolve), compile gate (72 blocks PASS), internal ids, register
ids, history prose — all clean. **Not done (left out, ungrounded):** the E1 case where a `##` operand on the
transfer inserts an AUGS needs a compile-proof record. Pages that mention an erratum without its number
(`rdlong`, `wrlong`, `wmlong`, `rdbyte`, `rdword`, `wrbyte`, `wrword`, `setq`, Spin2 `getct`/`getms`/`getsec`,
the DAC smart-pin pages, `wrpin`) point to the home pages, which carry it.

### F-568 — `addon-hd-audio.yaml` and `addon-rtc.yaml` cited the chip datasheets only in prose, leaned on un-ingested drivers and a schematic, and stated two AK5704 facts wrongly — `RESOLVED` (found 2026-10-10, applied 2026-10-10, «#422»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbHwAddonHdAudioAddonHdAudio` serves `adc_codec_chip` with the slave address "%001000C ... $10 with CAD low, $11 with CAD high" and "CAD low: write = $20, read = $21. CAD high: write = $22, read = $23", `sdto2_default` "Chip pin 6 is TDMIN (an INPUT) by default ... SDTO2E resets to 0", and `unknown_on_this_board` ("which level the #64014 ADC board ties the codec's CAD pin to ... The board guide states neither"); no `AK5704_DEVICE_ID`, no `source_trace`, no driver or schematic resource entry. `p2kb_get p2kbHwAddonRtcAddonRtc` serves `rtc_chip` ($68, $D0/$D1, reset $58, 00h-13h map) and `board_unknown` (pull-ups unknown), with the datasheet named by title and revision under `resources`; the "3.3K pull-up" appears only as a quote of the board guide's Code Tip inside `scl_pull_up_caveat`. The still-open CAD strap level stays marked unknown in both the served text and `KNOWLEDGE-GAPS.md` G-014.

> **DECIDED by Stephen 2026-10-10 ("yes A"):** a chip maker's datasheet is citable for its own chip's
> facts only (admission route 3, `AUTHORITATIVE-SOURCES.md`; doctrine *Provenance is for us*).
> **Applied 2026-10-10 («#422»):** both datasheets ingested (`sources/P2-HD-Audio-Add-on/ak5704-datasheet-*`,
> `sources/P2-RTC-Add-on/pcf8523-datasheet-*`): AKM *AK5704 Low-Power 4-ch 32-bit ADC with MIC-Amp*,
> 019000890-E-01, Rev.1, 2022/01; NXP *PCF8523 Real-Time Clock (RTC) and calendar*, Rev. 7, 28 April 2015.
> `audit-yaml-claim-sourcing.py` gains a row for each and a `DATASHEET_REVISION` rule (no revision →
> NO_EDITION, another → STALE_EDITION), with refuse and accept controls (negative control 147 cases PASS).
> **Wrong, now corrected from the AK5704 datasheet:** the address was a fixed `$10` / `$20` / `$21`; the
> slave address is `%001000C`, the low bit set by the CAD pin (Fig 48, pp.75-76; text `ak5704-datasheet-text.txt:4441`,
> `:4485-4486`), so `$11` / `$22` / `$23` with CAD high — and which level the #64014 board straps is stated
> by no ingested document. SDTO2 was "the codec's Line data OUT by default"; register `$00` SDTO2E
> defaults to 0, *"Disable (TDMIN pin: Default)"* (pp.6, 80; `:4751-4753`). **Removed as un-ingested
> provenance:** `AK5704_DEVICE_ID`, "the ADC board carries its own pull-ups", the RTC driver's "3.3K
> pull-up", both `source_trace` blocks and the driver / schematic resource entries. Chip facts now sit in
> `adc_codec_chip` / `rtc_chip`, cited to the datasheet by title, revision and page; board facts in
> `adc_board` / `board_interface`, cited to the Parallax guides; what neither states is marked unknown.
> PCF8523 `$68` / `$D0` / `$D1`, reset `$58`, BCD, the 00h-13h map and CLKOUT checked against the datasheet
> and kept (pp.6-9, 12, 33, 46, 52; `pcf8523-datasheet-text.txt:445`, `:2583`). Verified by the arbiter
> against the extracts. **Gates:** claim sourcing PASS (0 Tier 1 / 0 BAD_CITATION / 0 Tier 2); source
> lock PASS, both pages CANONICAL; format, plain-scalar, duplicate keys, crossref clean.
> **Still open (a held document, needs an ingestion pass):** the #64014 board's CAD strap level and its
> I2C pull-ups are on the Parallax *64014 Rev A* schematic, staged in
> `sources/P2-HD-Audio-Add-on/NO-COMMIT/` but image-only (a printed PDF with no text layer), so not yet
> ingested — routed to `KNOWLEDGE-GAPS.md` G-014. The #64013 pull-up question stays with the #64013
> schematic, which is not held (G-013).

### F-563 — `smart-pin-11011-usb-host-device.yaml` gives the USB receiver status bits [6] and [3..0] from the superseded PDF-era capture — `RESOLVED` (found 2026-10-09, applied 2026-10-10, «#419»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbArchSmartPin11011UsbHostDevice` serves `registers.z_register.bits` as "[6] error — ... EOP SE0 > 2 bit periods or SE1", "[3] steady state — cleared on DP/DM state change, set on 7 bit periods of no change", "[2] SE0 in — high when DP/DM state is SE0", "[1] K in", "[0] J in"; the PDF-era "SE1 in" / "EOP SE0 > 3" / "set on 7+ bits of J" wording is absent (also `git grep` at `v1.24.0` over `deliverables/ai/P2`: no hit).
Found 2026-10-09 by the VO-J-035 rework writer («#409»). `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml:61-67`
ships `[6] … EOP SE0 > 3 bits, or SE1`, `[3] SE1 in (illegal) — cleared on !SE1, set on 1+ bits of SE1`,
`[2] SE0 in (RESET) — … set on 1+ bits of SE0`, `[1] K in (RESUME) — … set on 7+ bits of K`,
`[0] J in (IDLE) — … set on 7+ bits of J`. That wording is the superseded `p2-documentation.txt:8962-8982`
(PDF-era, see `sources/silicon-doc/SUPERSEDED-BY-2026-08-26-DOCX.md`; the Hardware Manual
`p2-hardware-manual-text.txt:1507-1510` and Titus `:1411-1414` carry the same older text). The canonical
DOCX capture of the P2 Documentation v35 (`silicon-doc-text.txt:4621-4629`) gives `[6] … EOP SE0 > 2 bit
periods or SE1`, `[3] steady state — cleared on DP/DM state change, set on 7 bit periods of no change`,
and `[2]`/`[1]`/`[0]` SE0/K/J in as "high when DP/DM state is" SE0/K/J. **Silicon agrees with the DOCX:**
VO-J-035 run 1 (`campaigns/2026-10-p2kb-close-out/tests/logs/debug_261009-140053.log`) read status `$0C`
on an idle bare pair — bits 3 and 2 set together, which the "SE1 in" reading makes impossible (SE1 and
SE0 cannot both hold); as "steady + SE0" it is the documented host idle. Not an EF: run 1 was NO VERDICT for
its own question, and the rerun that decided it (EF-102) answers the WXPIN baud question only — its
status-bit readings are printed there "not judged". **Class sweep** (`grep -rn "SE1 in\|EOP SE0 > 3\|set on 7+ bits of J\|steady state" deliverables/ai/P2`):
this file only. **Fix:** replace lines 61-67's [6] and [3..0] with the DOCX wording, cited to the P2
Documentation v35, *USB smart pin* section; close-out sprint (KB v1.24.0).

> **Applied 2026-10-10 («#419»); the entry stays PENDING-VALIDATION until a release serves it.**
> `smart-pin-11011-usb-host-device.yaml` `registers.z_register.bits` [6] and [3..0] (and [5]/[4], which
> carried the same older "7+ bits" wording) now read as `silicon-doc-text.txt:4621-4629`: `[6] … EOP SE0 > 2
> bit periods or SE1`, `[3] steady state — cleared on DP/DM state change, set on 7 bit periods of no
> change`, `[2]`/`[1]`/`[0]` "high when DP/DM state is" SE0/K/J. Class sweep re-run:
> `grep -rn "SE1 in\|EOP SE0 > 3\|7+ bits of J" deliverables/ai/P2` returns nothing.

### F-560 — 78 `source:` fields in 58 files name a label, not a document — `RESOLVED` (found 2026-10-07, applied 2026-10-10, «#422»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** Provenance-only fix, so validated by absence live and presence in git. `p2kb_get p2kbCommunitySimpleAnalogInput` (a Quick Byte) serves no `source:` line (its citation is its `url:`); `p2kb_get p2kbSpin2Pinstart`, `p2kbPasm2Muxq` and `p2kbSpin2Cogspin` serve no `hub_driver` / `P2-FLASH-FS` / category-label attribution. `git grep -E "^\s+source: *['\"]?[A-Za-z0-9_-]+['\"]?\s*$"` at `v1.24.0` over `deliverables/ai/P2` returns eight lines, all EF-/CP- ids (`EF-098`..`EF-101`, `EF-057`, `EF-062`, `EF-099`, `CP-007`); `muxq.yaml:51` / `testp.yaml:57` carry "(example code, not a Parallax document)" in `source:`.
Found 2026-10-07 by the F-553 class sweep: `grep -rn -E "^\s+source: *['\"]?[A-Za-z0-9_-]+['\"]?\s*$" deliverables/ai/P2/`
returns 78 lines in 58 files whose `source:` is a bare label: `parallax-quick-bytes` ×42 (a corpus
not yet ingested — `quickbytes-integration` is NOT processed), `P2-OctoSerial` ×10, `P2-Click-eInk`
×2, and 24 one-off category names that are no document at all (`bit_bang_spi`,
`resource_protection`, `memory_operations`, `debug_logging`, …). Each such block is an example or
pattern whose stated origin cannot be checked. Not introduced by the unreleased commits — already
published. **Fix:** per `SOURCE-REPAIR-ORDER.md`, file by file: re-source from the real artifact
(ingest Quick Bytes first for the 42; OBEX/project source for OctoSerial/eInk) or remove the block;
never relabel in place. F-553 removed the `hub75_driver` and `P2-FLASH-FS` instances: the flash
driver contradicted its attributions; the HUB75 examples were invented code under a driver's name
(the real driver does use SETQ + MUXQ, and `muxq.yaml` now quotes it with a real source).

> **Applied 2026-10-10 («#422», dispatch A).** All 42 `source: parallax-quick-bytes` lines are deleted
> (Stephen's Q5: the entry's parallax.com `url:` is its citation; `scraped:` stays). Both gates read the
> rule: the sourcing gate since «#412», and `audit-yaml-source-lock.py` now tiers a quick-bytes entry with
> a parallax.com `url:` CANONICAL by importing the sourcing gate's `is_catalog()` / `catalog_cited()`,
> with four new negative controls. The other 35 label lines (24 category names, 9 `P2-OctoSerial`,
> 2 `P2-Click-eInk`; the tenth OctoSerial line was already gone) are deleted from their blocks, not
> relabelled: none of them is a Parallax document, and a repo path is not a citation. The example code
> stays; the compile gate still covers it. `waitx.yaml` lost its only provenance with the labels and now
> cites the PASM2 Manual (p.159) and the P2 Instructions sheet.

> **Applied 2026-10-10 («#422», dispatch B) — community-code attributions.** The example attributions that
> name a community artifact rather than a Parallax document (`muxq.yaml` and `testp.yaml` examples,
> `streamer_smartpin_control.yaml` `isp_bldc_motor.spin2` examples, `pinstart.yaml` `jm_ez_spi.spin2`,
> `cogspin.yaml` OBEX 4261) no longer carry a repo path in a citation key: each is now an `origin:` /
> `obex_object:` note that says what the code is and that it is "not a Parallax document". The example
> code is unchanged and still passes the compile gate. `testp.yaml` lost its only citation with the move
> and now cites the PASM2 Manual (p.136) and the Silicon Doc's I/O Pin Timing. The facts whose ONLY
> source is the flash-loader source, the Spin2 debugger v51 source, the ROM booter listing or the v55
> interpreter (44 citation lines) were held for Stephen's ruling; he ruled 2026-10-10 that Parallax's
> published source listings are citable, pinned to their edition («#422», dispatch C: listing titles
> and the `STALE_EDITION` check in the sourcing gate; BAD_CITATION 44 → 0). After the sweep the only
> `source:` values that are not a document title are EF/CP ids
> (`grep -rn -E "^\s+source: *['\"]?[A-Za-z0-9_-]+['\"]?\s*$" deliverables/ai/P2/` returns only
> EF-/CP- ids, 2026-10-10).

### F-559 — the DEBUG guide states tool limits as facts (15,872 bytes); it should teach the techniques instead — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2DbgDebugStrategyGuide` (also reached by the alias `debug data too long`) serves `the_compilers_limits` with no byte or record figure: "Those figures belong to the compiler and can change from one release to the next, so this guide states none of them ... read them from your compiler, never from a document", the `-d -l` listing method, the `m150`/`m151`/`m153` messages, and the techniques (DAT + `zstr_()`, value-only forms, merging statements, `DEBUG_MASK`, `debug(IF(...))` already in the corrected `debug(IF(errorCount > 0), ...)` form). No `15,872`, `16,384` or `255 records` figure appears.
> **Applied 2026-10-07.** `debug-strategy-guide.yaml` rewritten to the ruling: no compiler or
> debugger figure stated as fact (title, aliases, `hard_limits` → `the_compilers_limits`, decision
> guide and setups keyed to the listing, not counts); the debugger layout reduced to what is
> silicon (top 16 KB, per-cog blocks). Kept and verified by re-measurement on pnut-ts 1.55.8
> (independent check): merge cuts records (2→1), value-only forms dedup (2→1), DAT+`zstr_` removes
> text and shares a record, IF adds bytes, masked child adds nothing, error texts m150/m151/m153.
> Contradictions fixed ("every debug() consumes a slot", "non-overlapping", dedup advice). Also
> found and fixed: `debug IF(c)(...)` does not compile (m281) — now `debug(IF(c), ...)`, v55 :920.
> Class sweep: no other KB file states a DEBUG limit.
> **Ruling, Stephen 2026-10-07:** "debug limits are not hardware and are not hard and fast... we
> can teach techniques for how to mitigate bumping up against them but not the limits themselves...
> soft values change with each compiler release." So the fix is **not** to state 10,752 in place
> of 15,872: `debug-strategy-guide.yaml` drops every DEBUG byte/record limit stated as a fact
> (the 15,872 "budget" F-383 added included) and keeps the techniques — DAT + `zstr_()`, the
> value-only forms, merging statements to cut records, `DEBUG_MASK`/`DEBUG_DISABLE` — plus how to
> read the compiler's own listing for the current figures. VO-J-027 stays struck. The layout
> analysis below is kept as the reason the KB must not imply a compiled build is safe up to the
> compiler's cap; it is not KB content.
Found 2026-10-07 by the pre-release audit of F-383 / the VO-J-027 strike. The debugger pnut-ts
embeds (byte-identical to `external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2`
apart from patched config bytes) copies DEBUG data to `dat_addr = $FC000` (`:7`); its register
buffer starts at `sav_addr = $FEA00` (`:8`, 10,752 bytes later) and the debugger itself at
`dbg_addr = $FF1A0` (`:9`, 12,704 later). pnut-ts 1.55.8 accepts 15,872 bytes of DEBUG data
(listing "15_872 of 15872"; copy length word 16,002 = data + 2 + 2×records). So a build between
~10.7 KB and the compile cap compiles clean and overruns the debugger's memory at load — a fixed
layout, not a soft threshold; VO-J-027's field figures (5,783 / ~10,400 fine; 13,023 / ~14,900
mute) straddle it. `debug-strategy-guide.yaml` presents 15,872 as the budget and d8a70660 removed
the runtime-mute claim. Also left contradictory in that file by the F-383 rewrite: `:38` area
still calls a cap "silent"; `:26` "every debug() consumes a record slot"; "non-overlapping
remedies" vs the DAT+`zstr_` fix that cuts both; `:128`/`:415-419` "don't rely on dedup" vs
`over_on_records`; the records-side "merge statements" fix dropped although merging cuts records
(2→1, measured). Corroborating, not authority: SingleStep-Debugger ToO `:1191` (PNut checks
`$2A00` = 10,752). **Decision owed:** whether the KB states the layout limit (and VO-J-027 is
reinstated as a bench confirmation), given the 2026-10-07 strike ruling.

### F-558 — F-387's P1→Spin2 table: `||` in the wrong tier, `>|`→`ENCOD` off by one, two rows lose P1 behaviour — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Operators`, `changed_from_p1.fails_to_compile` serves `||a -- unary absolute value` → "ABS a; || is now binary logical OR"; `>| x` → "(x <> 0) ? ENCOD x + 1 : 0 -- ENCOD returns the bit number itself, one less than P1's >|"; `?x / x?` → "a reversible LFSR ... P1's reverse form x? has no Spin2 equivalent"; `~x / ~~x` → "x SIGNX= 7 / x SIGNX= 15 (x SIGNX 7 alone does not write x)"; and `compiles_with_a_different_meaning` carries the `<=`/`>=` assignment-form row.
> **Applied 2026-10-07.** `operators.yaml`: `||a` moved to `fails_to_compile` (m172); `>|` →
> `(x <> 0) ? ENCOD x + 1 : 0`, compile-checked against all four P1 examples (0/8/32/21);
> `?x/x?` states the reversible LFSR and that `x?` has no equivalent; `~x/~~x` → `SIGNX=` (writes
> back); `>=` assignment spelling added. Row map extended (P1 5463/5498, 5522-5535, 5577-5588).
> `generate-p2kb-index.py` comments: current count 74, dated record annotated. Independent check:
> every row re-compiled, all CORRECT. **Left, with reasons:** the derived
> `spin2-v51/complete-spin2-operators.md` blockquote formatting and `:471` cite (ingestion tree —
> Stephen's call on editing it, raised 2026-10-07); `yaml-source-lock.json:861` stale key (a ratchet
> baseline — re-recorded at its next tightening, not hand-edited).
Found 2026-10-07 by the pre-release audit of F-387 (`concepts/operators.yaml` `changed_from_p1`).
(1) `||` (P1 unary abs) is listed under `compiles_with_a_different_meaning`, but `r := ||a`
fails to compile (m172) — it belongs in `fails_to_compile`. (2) P1 `>|` returns highest set bit
**plus 1** (P1 Manual `:5576-5587`: `%1000_0000` → 8); `ENCOD $80` = 7 (compiled) — the
spelling is `ENCOD x + 1` for x≠0, 0 for x=0. (3) `?x / x?` → `??x` loses that P1 random is
reversible (P1 `:5522-5535`) and `x?` has no Spin2 equivalent. (4) `~x / ~~x` are P1 assignment
operators (`:4950`, `:5463`) — the Spin2 equivalent writes back (`SIGNX=`, v55 `:450`). (5) The
`>=` assignment form has no spelling given. Related leftovers: the derived
`spin2-v51/complete-spin2-operators.md` correction blockquote (F-547) breaks the table under GFM
and cites `:471` (ADDPINS) instead of `:472`; `generate-p2kb-index.py:113-117,128` comments and
`validation/baselines/yaml-source-lock.json:861` still name `+<=>` / `op_addlteqgt.yaml`.

### F-557 — `pasm2-getting-started.yaml` (F-542): four facts incomplete against a primary source; 36 "(order N)" row locators ship — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbGuidePasm2GettingStarted` serves GETCT "Cogs 0-3 and 4-7 each keep their own upper long, which advances only while a cog of that group is running when the lower long wraps"; ORGH "In a Spin2+PASM program, bare ORGH sets hub origin $00400 ... In a PASM-only program, bare ORGH sets hub-exec mode at the current hub address"; "## instead of # makes the assembler insert an AUGS or AUGD"; RDLONG/WRLONG "+1 if the long crosses a hub long boundary; figures for an 8-cog P2". No "(order N)" token appears anywhere in the served guide (`git grep "(order [0-9]+)"` at `v1.24.0` over `deliverables/ai/P2`: no hit).
> **Applied 2026-10-07.** GETCT gains the group-copy caveat (EF-068, EF-079 in `source:`); ORGH
> states the Spin2+PASM and PASM-only behaviours (v55 :326-327, compile-checked); `##` → AUGS or
> AUGD (Silicon Doc :5571-5572, listing-checked); hub timing gains "+1 if crossing a hub long;
> 8-cog figures" (CSV header); all 34 "(order N)" tokens moved into `source:` row maps. Gate gap
> closed: `validate-dod-release.py` REPO_LOCATOR_PATTERN now matches "(order N)" — negative control:
> 34 hits on the old guide, none on prose like "the order of operations". Independent check: all
> CORRECT. **Left:** `critical_gotchas` stays `{source, items}` (its source needs a stripped field).
Found 2026-10-07 by the pre-release audit of F-542. (1) GETCT "GETCT WC then GETCT gets the full
64-bit CT" omits EF-068 (a group of four cogs with no running cog at a low-long wrap returns a
stale upper long). (2) Bare ORGH "hub origin $00400" is the Spin2+PASM case only; v55 `:327`:
PASM-only, bare ORGH sets hub-exec at the current hub address. (3) "`##` prefixes an AUGS" —
Silicon Doc `:5571-5572`: AUGS/AUGD (the guide's own `WAITX ##` uses AUGD). (4) RDLONG/WRLONG
timing drops the CSV's "+1 if crosses hub long" and 8-cog qualifiers. (5) 34 "(order N)" (38 row numbers; "36" corrected 2026-10-07)
spreadsheet row numbers sit in shipped descriptions — an internal locator the Internal-IDs
payload scan does not pattern-match (a gate gap). Also: `critical_gotchas` changed from a list to
`{source, items}`, so readers now get `{items: [...]}` unlike the sibling Spin2 guide.

### F-556 — "2x 74HCT244" ships with no primary source (HUB75 adapter) — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11 — closed by supersession, not by the removal described below.** The 2026-10-07 removal of the part number was overtaken by F-567 (2026-10-10), which ingested the HUB75E Adapter schematic H/W Rev 1.4 as a primary source; `v1.24.0:deliverables/ai/P2/hardware/hub75_adapter.yaml` now states "two 74HCT244 octal buffers at 5 V ... output enables tied low" with `source:` naming the schematic ("U1/U2 74HCT244 buffers on +5VA between the P2 headers J1/J2 and the HUB75 connector J7"), so the defect (a part number with no primary source) no longer exists. Live: `p2kb_get p2kbHwHub75AdapterHub75Adapter` serves `level_shifting: "two 74HCT244 octal buffers at 5 V, 3.3 V in to 5 V out ... output enables tied low"` and an `authorship` line saying every fact comes from the designer's schematic or dated statement; `resources.obex` is "ISP Hub75 Matrix Driver" with no `driver_file` key (none in `v1.24.0` either). Note for a later pass: `hardware/hardware-compatibility-matrix.yaml` (`addon_board_host_compatibility`, the 64032 `note`) repeats "the adapter's 74HCT244 level shifters" inside a block whose `source:` cites only the #64006-series guide; the hub75 page it points to carries the schematic citation.
> **Applied 2026-10-07.** Part number removed from `hub75_adapter.yaml` (×2) and
> `hardware-compatibility-matrix.yaml`; "level shifter ICs" kept (`official-specs.md:22`). The
> non-existent `driver_file: isp_hub75_matrix.spin2` removed. Independent check: CORRECT. The
> OBEX name/URL mismatch it noticed is F-562.
Found 2026-10-07 by the pre-release audit of F-354. The part number appears only in this
project's own `p2-addon-board-circuit-knowledge.md:363,391`; `p2-hub75-adapter-official-specs.md:22`
(cited) says only "limited by level shifter ICs". Ships in `hardware/hub75_adapter.yaml` (twice)
and `hardware/hardware-compatibility-matrix.yaml`. The schematic PDF is not ingested. Also
`hub75_adapter.yaml:159` names `driver_file: isp_hub75_matrix.spin2`, which is in neither OBEX
2850 nor the project copy.

### F-555 — `boot-rom-contents.yaml` calls `ROM_Booter.lst` "an FPGA build of the same source"; it is an earlier revision — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbArchBootRomContents` serves no mention of `ROM_Booter.lst` or "of the same source"; its citations (stripped at delivery, present in `git show v1.24.0:deliverables/ai/P2/architecture/boot-rom/boot-rom-contents.yaml`) name only "Parallax Propeller 2 ROM Booter v33_01j (assembly listing of the Prop2 silicon ROM)". `git grep "ROM_Booter\.lst|of the same source"` at `v1.24.0` over `deliverables/ai/P2` finds no ROM_Booter.lst reference anywhere (the only "same source" hit is unrelated pnut-ts text in `object-image-dedup.yaml`). The 2026-10-07 label ("earlier revision v141, an FPGA build") is therefore not in the tag either: the FPGA listing is no longer cited in any served file, so the wrong claim cannot be read.
> **Applied 2026-10-07.** Label now: the silicon build is revision v33_01j (2019); `ROM_Booter.lst`
> is an earlier revision, v141 (2018), built for the Prop123-A9 / BeMicro-A9 FPGA boards — cited in
> `source:` (both listings' history lines, `ROM_Booter.lst:118`, Silicon Doc `:2876`,
> `:2950-2951`). My first edit dropped "FPGA" as unproven; the independent check showed it proven
> and it was restored. F-421's note corrected the same way.
Found 2026-10-07 by the pre-release audit of F-421. `rom_booter_v33_01j.lst:87-93` carries
2019 revisions (v33_01a…j) that `ROM_Booter.lst` lacks (its history ends at v141, 2018-05-27,
`:84-85`); TAQOZ builds differ. It is ALSO an FPGA build — `:118` `ver = "A" 'Prop123-A9 /
BeMicro-A9`, FPGA boards per `silicon-doc-text.txt:2876`, `:2950-2951` — so "FPGA" stays and only
"of the same source" is wrong. The F-421 register text ("neither is a newer revision") is wrong
the same way. The re-citation to the silicon listing itself is right.

### F-554 — F-386 left the false "WYPIN after enable is safe for all modes" rule in three files; one wrong locator — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbArchSmartPins` serves the corrected `correct_sequence.note` ("Write Y with WYPIN AFTER raising DIR for the trigger modes ... and asynchronous serial transmit (%11110) ... EXCEPTION -- synchronous serial transmit (%11100) in continuous mode needs its FIRST word written with WYPIN DURING reset"); `p2kb_get p2kbPasm2Wrpin` serves the matching `critical_requirement.note` ("Required for the trigger modes %00100/%00101 and asynchronous serial transmit %11110 ... Exception: ... %11100") with no "safe for all other modes"; `p2kb_get p2kbArchSmartPin01110CountAEdgesOptionalBDec` serves "That is the general order" and "the order is not critical" for this mode, no "every mode" / "safe either way"; its PASM example uses `dirh` then `wypin`. `git grep` at `v1.24.0` for "universal ... order" / "safe for all" / "EVERY mode" finds only unrelated streamer/XINIT/p2an001 text. The `:3852` locator no longer exists (the `smart_pins.yaml:105` source cites the SMART PINS section by title).
> **Applied 2026-10-07.** The rule corrected in `smart_pins.yaml` (procedure + note: documented
> reason for pulse/transition, measured effect for async TX, %11100 exception), `wrpin.yaml`
> (note; ids moved to `source:`), `smart-pin-01110` (no "every mode", no "safe either way"); locator
> `:3852` → `:3854`; "universal" → "general" in six mode pages (27 code comments). Found by the
> independent check and fixed in the same pass: Spin2 `DIRH(pin)` does not compile → `PINHIGH`;
> the `:3854` quote restored "depending on the mode"; `%11011` USB example did WYPIN before DIR
> although `silicon-doc-text.txt:4593` documents the order → reordered, and dropped from VO-J-028
> (now eight pages). Ledger: EF-019 scope note (cadence, not content; EF-090 governs %11100).
> **Left:** P2AN003's "universal … first output cycle undefined" is an app-note change → F-561.
Found 2026-10-07 by the pre-release audit of F-386. Still shipped: `architecture/smart_pins.yaml:589`
("safe for all"), `smart-pins/smart-pin-01110-count-a-edges-optional-b-dec.yaml:74` ("correct for
EVERY mode"), `language/pasm2/wrpin.yaml:73` ("safe for all other modes") — EF-090 contradicts it
for %11100. `smart_pins.yaml:107` cites `silicon-doc-text.txt:3852` (blank) for "configure while
DIR is low" — the sentence is `:3854`. The async-TX cause "they hold Y at 0 during reset" is EF-011's
interpretation, not a documented or measured fact (Silicon Doc `:4714` says output held high).
Ledger: EF-019's heading still reads CONFIRMED for prime-after-enable on %11100 with no pointer to
EF-090. Register/VO-J-028 say "ten mode pages" for a list of nine.

### F-553 — `pinstart.yaml` `production_patterns` keeps the invented labels F-543/F-549 removed from the examples — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Pinstart` serves no `production_patterns` key and no `hub75_panel` / `flash_filesystem` pattern; `p2kb_get p2kbSpin2Cogspin` serves its `production_patterns` with only `indexed_stack_allocation` (no flash-FS stress example, no `multi_cog_with_locks`) and `synchronization.file_system_access` reading "The P2 FLASH Filesystem driver supports multi-cog access without consuming a cog"; `p2kb_get p2kbPasm2Muxq` serves the "Parallax HUB75 driver" example as the 2-line `SETQ maskRgb12` / `MUXQ OUTA, reg_value` extract and no invented "Essential for HUB75" claim.
> **Applied 2026-10-07, widened by the class sweep.** `pinstart.yaml` `production_patterns`
> removed. Same labels elsewhere: `cogspin.yaml` — the flash-FS stress example and
> `multi_cog_with_locks` removed, and the claims that callers must lock the flash filesystem
> replaced by what the driver shows (`flash_fs.spin2:19` multi-cog, `:146`/`:221`/`:248` its own
> lock); `waitx.yaml`, `muxq.yaml` — invented HUB75 examples and "Essential for HUB75" removed;
> `muxq.yaml` gains a verbatim example from the real driver (`isp_hub75_rgb3bit.spin2:932-934`).
> Independent check: CORRECT. The wider label-as-source class (78 lines) is F-560.
Found 2026-10-07 by the pre-release fact audit of F-543/F-549. `production_patterns`
(`language/spin2/methods/pinstart.yaml`, after the P_OE note) was untouched by both fixes and
still carries `hub75_panel` → `source: hub75_driver` (names no document — the same invented
label F-549 removed from the examples) and `flash_filesystem` → `source: P2-FLASH-FS` with
"Configure pins as group first / Then specialize each pin's mode" — the attribution F-543
showed false: `flash_fs.spin2` (OBEX 4261) never calls PINSTART (grep: 0 hits). F-549's
applied-note says it was widened to every example in the file; this block was missed.
**Fix:** per `SOURCE-REPAIR-ORDER.md` — remove both patterns (they cite nothing real); re-add
only what a primary source states. Sacred Rule #7: the block holds no `related:` paths.

### F-552 — F-387's P1→Spin2 operator tables ship line citations in content; the release gate fails — `RESOLVED` (found 2026-10-07, applied 2026-10-07; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Operators`, `changed_from_p1` rows read e.g. "a ~> 2 -- shift arithmetic right" / "a SAR 2" with no `(P1 :NNNN)` / `(:NNN)` / `v55 :NNN` cite in any `p1:`, `spin2_spelling:` or `spin2_reads_it_as:` value; `p2kb_get p2kbSpin2OpPrecedence` level 11 carries no `spin2-v55-text.txt:472-488` cite.
> **Applied 2026-10-07.** `concepts/operators.yaml` `changed_from_p1`: all 32 row cites
> (`(P1 :NNNN)`, `(:NNN)`, `v55 :419`) moved into the block's existing `source:` as a
> row→line map (P1 Manual v1.2 layout-text 4943-4973, 5681-5683; v55 text 409-491); every
> stated fact unchanged — checked structurally against HEAD (values equal once the citations
> are removed; the post-clear note kept as "(post-clear ~)"). `operators/precedence.yaml`
> level 11: the `spin2-v55-text.txt:472-488` cite moved to a new `source:` on that entry.
> No fact needed re-proving — nothing but citation text changed. Gates: verify-yaml-format
> clean, crossref 3893/3893, `validate-dod-release.py` ALL PASSED (Internal IDs now 0).
Found 2026-10-07 measuring the delivered-output scan baseline for the delivery-filter-rule sprint
(`engineering/planning/P2KB-DELIVERY-FILTER-RULE-SPRINT-PLAN.md`). `validate_internal_ids` in
`validate-dod-release.py` reads the shipped payload and reports **33 repo-locator hits**: 32 in
`language/spin2/concepts/operators.yaml` (payload lines 324–339+, e.g. `"a ~> 2 -- shift arithmetic
right (P1 :4952)"`, `"a SAR 2 (:445)"`) and 1 in `language/spin2/operators/precedence.yaml`. All come
from commit `ad10b085` (F-387, 2026-10-07): the `p1:` / `spin2_spelling:` / `spin2_reads_it_as:`
values carry `(:NNN)` / `(P1 :NNNN)` line cites. A consumer cannot open them, and the gate blocks the
next KB release. **Fix:** move each cite to the entry's `sources:` (where the claim-sourcing gate still
reads it), keep the stated fact; re-run `validate-dod-release.py`. Not touched by the filter sprint —
its certification bundle is frozen at HEAD and this stays a register item (Stephen, 2026-10-07).

### F-551 — `guides/pasm2-getting-started.yaml` is uncited outside the blocks F-542 re-derived — `RESOLVED` (found 2026-10-07, applied 2026-10-10, «#418»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbGuidePasm2GettingStarted` serves `operand_types.register` "Cog register $000-$1FF (LUT RAM is reached with RDLUT/WRLUT, not as an operand)", the `WC`/`WCZ` examples as "carry out of the 32-bit add" / "borrow of (x - y)", `pointer_with_auto_increment.step_size` ("1 for RDBYTE/WRBYTE, 2 for RDWORD/WRWORD, 4 for RDLONG/WRLONG ... INDEX 1..16"), `reference_operators` (`#label` relative by default, `$` steps by 1 in ORG and 4 in ORGH), `timing_considerations` (4 clocks taken cog branch, 13...20 hub-exec, "+1 clock when the target is not long-aligned", QMUL "2...9 clocks to issue, the result about 55 clocks later"), `next_steps` naming real files, and `local_labels.syntax: ".labelname"` with no `:labelname` form. No `extraction_note` / `correction_2026*` key anywhere in the tag (`git grep` at `v1.24.0`: no hit). The citations that make the blocks "cited" are provenance and are stripped at delivery; the guide's `source:` blocks are present in `git show v1.24.0:deliverables/ai/P2/guides/pasm2-getting-started.yaml`.
Found 2026-10-07 scoping F-542. Of 729 lines only `file_structure` and `timing_considerations`
carried a source; F-542 re-derived `register_model`, `core_instructions`, `assembler_directives`
and `critical_gotchas`. Still uncited: `instruction_format`, `addressing_modes`, `common_patterns`,
`inline_pasm2_in_spin2`, `labels_and_symbols`, `string_handling`, `debugging_support`,
`flag_behavior`, `knowledge_progression`, `next_steps`. Also `file_structure.size_checking`
ships a dated `correction_2026_08_25` history note in reader-facing text. This is the
most-copied beginner page in the set. **Fix:** `SOURCE-REPAIR-ORDER.md` — remove and re-derive
each block from the spreadsheet / P2 Documentation / v55, compile every example, report
grounded · gaps · removals.

> **Applied 2026-10-10 («#418»); closes when a release serves it.**
> The remaining guide blocks, against the spreadsheet / P2 Documentation / v55: `operand_types`
> "or LUT register" (LUT is reached with RDLUT/WRLUT, not as an operand); the `WC`/`WCZ` examples read C
> as carry and borrow; `pointer_with_auto_increment` gained the step size (1/2/4, `INDEX` 1..16) and a
> canonical citation; `inline_pasm2_in_spin2` gained a canonical citation; `reference_operators`
> (`#label` relative by default, `$` = the current origin, stepping 1 in ORG and 4 in ORGH); the C-flag
> use ("overflow" → carry/borrow); `timing_considerations` (taken branch 4 / 13...20 clocks, +1 when
> a hub target is not long-aligned — which IS stated, P2 Documentation Hub Execution; QMUL 2...9 to
> issue, ~55 to result); `next_steps` and `immediate_next_steps` now name real files; the dated
> `extraction_note`/`correction_*` notes are gone (also from `basic-io`, `waitms`, `waitus`,
> `clock_system`, `spin2-getting-started`); the three clock-block citations are canonical. **Finding
> carried:** `:labelname` as a local-label form is accepted by pnut-ts (`:loop` assembles) but no
> Parallax document states it — the guide and `concepts/labels.yaml` now say `.labelname` and
> flag the colon form as compiler-accepted only; `language/fundamentals/pasm-labels.yaml` and
> `identifier-rules.yaml` do not list it (0 hits for `:labelname` / `:label` in both, 2026-10-10).

### F-550 — `serial_loader.yaml` `protocol_commands` gives the FPGA build's `Prop_Chk` answer and an invented `Prop_Clk` syntax — `RESOLVED` (found 2026-10-07, applied 2026-10-10, «#419»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbArchSerialLoader` serves `prop_chk.syntax` "Prop_Chk <INAmask> <INAdata> <INBmask> <INBdata>" with response "Prop_Ver ... The Rev B/C silicon responds with "G" (A-F were FPGA builds)"; `prop_clk.syntax` with the five fields ending `<HUBSETclocksetting>` and example `> Prop_Clk 0 0 0 0 19D28F8`; `prop_txt.syntax` with the four-field prefix and "2.25x denser than hex"; `response_codes` ('.' / '!'; "'?' and '~' are the sender's data terminators, and '> ' is the sender's auto-baud sequence"); `validation_format` ("Checksum complement = $706F7250 ... minus the sum of all longs"; "long-aligned"); `multi_chip_support.ina_limit` "INA[1:0] (P0 and P1) cannot be matched". No `Prop_Ver Au`, no `Prop_Clk 2 8 1` / `2 16 1`, no `performance` / `disable_option` block (`git grep` at `v1.24.0`: no `Prop_Ver Au` hit).
Found 2026-10-07 fixing F-421 in the same file. Against the P2 Hardware Manual (`p2-hardware-manual-text.txt:1629-1725`)
and the Silicon Doc (`silicon-doc-text.txt:4860-4868`):
- `prop_chk.response` "'Prop_Ver Au' (version A silicon)". Both documents: the Rev B/C silicon
  responds `CR+LF+"Prop_Ver G"+CR+LF` (HW Manual :1631-1634); the silicon ROM builds `ver = "G"`
  (`rom_booter_v33_01j.lst:131`). "A" is the FPGA build's letter (F-421).
- `prop_chk.syntax` "Prop_Chk" — the documented form carries the four INA/INB mask/data fields:
  `> Prop_Chk 0 0 0 0` (:1634).
- `prop_clk` — syntax "Prop_Clk P1 P2 P3" with P1 = source, P2 = multiply, P3 = divide, and example
  "Prop_Clk 2 8 1". No source states this. Documented: `Prop_Clk <INAmask> <INAdata> <INBmask>
  <INBdata> <clockmode>` (hex HUBSET value, e.g. `> Prop_Clk 0 0 0 0 19D28F8`, :1652, :1660;
  `boot-pattern-selection.yaml` already quotes the correct form).
- `prop_txt.syntax` "Prop_Txt ~" — documented `> Prop_Txt 0 0 0 0 <base64> ~ | ?` (:1716, :1722);
  its `efficiency` figures need checking against :1702-1725.

**Widened on reading the whole file (same day):** only `boot_sequence` (:11-34) carries a source.
Everything from `auto_baud_detection` to `performance` is uncited, and much of it contradicts the
manual: `response_codes`/`error_handling` give `?` as the error reply (the loader answers `!` for
a bad checksum; `?` and `~` are terminators the *sender* sends, :1666-1667); `'> '` is called the
loader's ready prompt (it is the sender's auto-baud sequence, :1645); auto-baud "measures bit
timing from CR"; `validation_format` describes a `'Prop'` header at offset 0 with a length field
(the documented scheme is a checksum-complement long placed anywhere long-aligned, :1688-1699);
`programming_examples` repeats the `Prop_Ver Au` and invented `Prop_Clk 2 16 1` forms;
`multi_chip_support` omits that P0/P1 cannot be matched (:1623); `security_considerations`
"disable_option: Don't pull up P61" and the `performance` figures have no source.
**Fix (M-L):** per `.claude/skills/SOURCE-REPAIR-ORDER.md` — remove the uncited blocks and
re-derive from HW Manual :1580-1725 (+ Silicon Doc :4860 ff.), every field quoted or cited.

> **Applied 2026-10-10 («#419»); closes when a release serves it.**
> `architecture/serial_loader.yaml` was re-derived from HW Manual `:1588-1725` and Silicon Doc `:4850-4868`:
> `prop_chk` (four-field syntax, `Prop_Ver G`, A-F are FPGA builds, `rom_booter_v33_01j.lst:125-131`);
> `prop_clk` (five fields, the HUBSET value, `.` reply, ~5 ms + 10 ms re-sync, the 148.5 MHz and boot-clock
> examples); `prop_txt` (four-field syntax, 2.25x denser than hex, the manual's Base64 examples);
> `response_codes` (`.`/`!`; `?`, `~` and `> ` are sender characters); `auto_baud_detection` (adapts at every
> `>`, initial `> `); `validation_format` (checksum-complement long, long-aligned anywhere);
> `multi_chip_support` (INA[1:0] cannot be matched); `programming_examples`/`error_handling` rewritten from the
> manual; the unsourced `disable_option`, `performance` and `recovery` lines removed. Class sweep
> (`Prop_Ver`, `Prop_Clk [0-9]`, `prop_chk`): this file only.

### F-549 — `pinstart.yaml`'s HUB75 and sensor-array examples carry invented `source:` labels, and the HUB75 one contradicts the board's pinout — `RESOLVED` (found 2026-10-07, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Pinstart` serves five examples and none is the HUB75 or the sensor-array one: ADC `PINSTART(16, P_ADC | P_ADC_1X, %00_1010, 0)` ("X = 0 would select a 1-clock period, which the P2 Documentation marks impractical"), PWM triangle `1000 << 16 | 1` with Y 500, async TX, quadrature on ONE pin `P_QUADRATURE | P_PLUS1_B` ("Starting both pins with ADDPINS does not pair them"), and the P58-P61 smart-pin SPI example; no `hub75_driver` / `sensor_array` label anywhere in the tag.
> **Applied 2026-10-07, and widened to every example in the file.** The two named examples were
> **removed** (uncited; HUB75 contradicts the adapter pinout; the sensor one reconfigures its ADC
> pins as outputs under a "same mode" comment). The other four were uncited too, so each was
> checked against the P2 Documentation: **three were wrong** — PWM triangle `X = 1000` sets a
> 1000-clock base and a zero frame period, so `Y = 500` exceeds its range (`:4034-4044`; now
> `1000 << 16 | 1`); quadrature `32 ADDPINS 1` starts two pins whose B input defaults to their own
> pin (`:3746-3756`), so neither sees the other phase (now one pin, `P_QUADRATURE | P_PLUS1_B`,
> `:4093-4097`); ADC `X = 0` selects a 1-clock SINC2 period, marked "impractical" in table 34
> (`:4257-4268`; now `%00_1010`, 1,024 clocks, 11-bit). Async TX was correct and gained its
> source (`:4684-4694`). Every example now carries a `source:` and compiles (pnut-ts 1.55.8).
> **Grounded fixes 3 · removals 2 · gaps 0.**
Found 2026-10-07 fixing F-543 in the same file. `examples[4]` (`source: hub75_driver`) and `examples[5]`
(`source: sensor_array`) name no document; the third invented label in the file was F-543's. The HUB75
example puts six RGB pins at 16-21 and CLK/LAT/OE at 22/23/24; the adapter's pinout
(`hardware/hub75_adapter.yaml` `signal_map`, from `p2-hub75-adapter-complete-pinout.md:8-27`) is CLK
offset 0, OE# 1, LAT 2, A-E 3-7, RGB 8-13 — so an agent wiring from this example drives the wrong
pins. The sensor example configures eight pins as ADCs, then reconfigures the same eight as
`P_HIGH_1K5` outputs "using ADDPINS for group config (same mode)" — the comment and the code disagree.
**Fix:** delete both (an example is not owed for every pattern), or replace each with a pattern
from an ingested driver, compiled, with a real `source:`. Per F-548, the HUB75 one should point to
the driver rather than restate its setup.

### F-548 — `hardware/` entries restate their drivers (API, timing, cog use, chipset tables), which every driver release can falsify — `RESOLVED` (found 2026-10-07, class sweep applied 2026-10-10, «#420»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbHwEdge32mbModuleEdge32mbModule` serves `protocol_constraints.psram` as the chip's own limits only (`chip_max_clock_mhz: 133`, `chip_alternate_clock_mhz: 84`, `max_cs_low_us: 8`, "as stated by the MegaYume PSRAM driver (OBEX 4162)"), `resources.obex.note` "The driver's API, settings and error codes are documented by the OBEX object itself", and no `code_patterns` block; `p2kb_get p2kbHwAddonLedMatrixAddonLedMatrix` serves `at_50hz_pixel_us: 357` (derived) with no `refresh_recommended_hz`, `cog_required`, `jm_p2-es_matrix` block or `power_sharing`; `p2kb_get p2kbHwEdgeStandardModuleEdgeStandardModule` serves flash as "SPI" / "24-bit (16MB)" with no 133 MHz line.
Found 2026-10-07 re-scoping F-354. Stephen's ruling: a hardware entry carries the board — pinout, pin
budget, voltages, level shifting, the board's published ceiling — and names its driver; the driver's
API, configuration, timing and resource use are the driver's (`.claude/doctrine-overlay.md`, *A
hardware entry carries the board, not the driver that runs it*). `hub75_adapter.yaml` was brought to
that shape under F-354. Known remaining instance: `edge-32mb-module.yaml` `code_patterns` (a
`psram.spin2` API restatement) and `protocol_constraints.psram` "Recommended driver settings"
(sysclk/N rates, burst formula), plus `resources` driver-feature lists and `advantages` driver
claims. 18 of 29 `hardware/` YAMLs mention "driver"; that is a mention count, not a defect count —
each needs reading. **Fix:** per file, keep board facts (the PSRAM chip's own 133 MHz and 8 µs CE#
limits are chip facts and stay), replace driver restatement with a pointer to the driver's OBEX
entry; before removing anything, run the search in *"Unsourced" is a finding about our search* so
board facts are told apart from driver facts.

> **Class sweep applied 2026-10-10 («#420»); closes when a release serves it.**
> `edge-32mb-module.yaml`: `code_patterns` (the whole `psram.spin2` API block), `protocol_constraints.psram`
> driver settings (sysclk/N rates, burst formula — which also removes S-259's wrong formula —, input-delay
> table), the flash 133 MHz line (no source), `resources.obex.features`, the OBEX-documentation reference
> and the two driver `advantages` are gone; kept: the chip's 133/84 MHz (guide §13) and the 8 µs CS-low
> figure (named as the driver's own statement, `psram16drv.spin2:171`). `addon-control-board.yaml`:
> `protocol_constraints` (PWM frequency, brightness levels, debounce, response time — absent from the
> guide, S-258) → one sourced line; the `jm_p2-es_control` driver block and the driver's LED/button
> remap; `power_sharing`. `addon-led-matrix.yaml`: `refresh_recommended_hz`/`at_120hz_pixel_us` →
> `at_50hz_pixel_us` (derived), `cog_required`, the `jm_p2-es_matrix` driver block, the unsourced
> `plot_pixel` snippet, the driver feature list, `power_sharing`. `addon-goertzel-touch.yaml`: the
> "dedicated cog for the Goertzel driver" limitation and `power_sharing`. `addon-digital-video-out.yaml`:
> `power_sharing`, `current_consumption`, the unsourced `monitor_compatibility` block.
> `addon-serial-host.yaml`: `power_sharing` plus the S-258 capability lists (storage, sensors, camera,
> gaming controllers, "USB specification compliant"). `addon-serial-device.yaml`: the S-374 class
> (HID/CDC/data-acquisition use cases, host-OS compatibility). `edge-standard-module.yaml`: the
> "133 MHz per W25Q128JV datasheet" flash clock (the datasheet is not held; the guide gives only "SPI"
> and the 16 MB capacity). Siblings read and left: `addon-rtc`,
> `addon-microsd`, `addon-hd-audio`, `addon-wx-*`, `addon-av-breakout` (their lists track their guides).

### F-547 — six comparison-operator entries describe themselves only as "Signed/unsigned compare", and one documents an operator that does not exist (`+<=>`) — `RESOLVED` (found 2026-10-05, applied 2026-10-07, cascade 2026-10-10 «#416»/«#421»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2OpOpAddlt` → "UNSIGNED less than. Returns -1 (true) or 0 (false)", priority 11; `p2kbSpin2OpOpLteqgt` → "SIGNED three-way comparison. Returns -1 ... 0 ... 1. There is no unsigned form: `+<=>` is not a Spin2 operator"; `p2kb_find term:"addlteqgt"` → 0 keys (`op_addlteqgt.yaml` is gone from the index); `p2kbSpin2OpOpEqeqeq` is an `operator_redirect` ("`===` is not a Spin2 operator ... Equality is `==`") and `op_notandand`, `op_ltshr`, `op_colon`, `op_question` are `operator_redirect` stubs in the tag; `p2kbSpin2OpPrecedence` level 11 lists the 17 operators including the six float compares and `<=>`, level 12 is `!!`/`NOT`, level 17 carries `=` and the missing compound forms; `p2kbSpin2OpOpPOW` is level 8 left-associative and states the compile-probe results (`2.0 POW 3.0 +. 1.0` is 9.0 ...).

> **DECIDED by Stephen 2026-10-08 about this entry's ingestion-tree edit: REVERT it, and AUDIT
> the operator ingestion.** This entry's commit (`53855f4f`) also edited
> `engineering/ingestion/sources/spin2-v51/complete-spin2-operators.md`. That edit is reverted
> byte-identical. ⛔ *"NEVER NEVER NEVER edit ingested docs!!!!!"* (doctrine: *The chain runs one
> way*). Stephen: `<.`, `<=`, `+<=`, `<=.`, `<=>` and more are legitimate operators, and the
> extraction appears to have lost spaces and glued them together, the likely origin of the
> invented `+<=>`. Its comparison row also lacks the float forms.
>
> **Audit scope:** every operator table in the v51 and v55 ingestions against the Parallax text,
> looking for glued, missing or invented operators. The findings are fixed through `ingest-source`
> only, then carried through to `op_*.yaml`, `operators.yaml`, `precedence.yaml` and
> `spin2-language-schema.yaml`. Also: `spin2-v55-text.txt` stores `<` and `>` as `&lt;` and
> `&gt;`, so a literal grep misses them. Re-check every citation made against it, including this
> entry's `:471-488`.

> **Applied 2026-10-07.** `op_addlt`/`op_addlteq`/`op_addgteq`/`op_addgt` now state UNSIGNED and
> name their signed and `.` siblings (v55 `:473`, `:476`, `:483`, `:486`); `op_lteqgt` states
> SIGNED three-way, -1/0/1, no unsigned form, float return in CON (`:488`, `:505`). Each gained a
> resolvable `source:`, `aliases:` (the index harvests aliases, not `keywords:`) and `related:`
> to its siblings. `op_addlteqgt.yaml` **deleted**; nothing in the KB linked to it. **One
> correction to this entry's own fix text:** v55's "CON only" column is not a restriction — it
> carries footnotes `**`/`***` (`:504-505`): in CON, applied to floats, these return float values.
> `<=>` compiles in PUB as well as CON, so "CON only" was not carried. **Proven on pnut-ts 1.55.8**
> (CON-folded values read from the `.lst`): `3<=>5`=-1, `5<=>5`=0, `7<=>5`=1;
> `$8000_0000 < 1`=-1 but `$8000_0000 +< 1`=0; `1 +> $8000_0000`=0; `$8000_0000 +>= $8000_0000`=-1;
> `$FFFF_FFFF +<= 0`=0; `a := 3 +<=> 5` → `error: Expected an expression term (m172)`.
> **Widened in the sweep:** `precedence.yaml` level 11 also listed `+<=>` and omitted the six
> floating-point compares v55 puts at the same priority — now the 17 operators of `:472-488`, in
> v55's order. The derived `sources/spin2-v51/complete-spin2-operators.md` (`:25`, `:164`) carries
> a dated correction note instead of the `+<=>` row.

> **Cascade applied 2026-10-10 («#416»); closes when a release serves it.** Authority: `sources/spin2-v55/spin2-v55-operator-reference.md` (84 rows, 17 levels) and
> `spin2-v55-text.txt:409-505`. (1) The three invented-token pages `op_notandand` (`!&&`), `op_eqeqeq`
> (`===`) and `op_ltshr` (`<>>`) are now `operator_redirect` stubs in the `modulo_add.yaml` style
> (published keys kept; no `operator:` key; each says the token is not Spin2 and points to
> `&&`/`AND`/`!!`, `==`, `<>`/`>>`/`SAR`); `op_colon` and `op_question`, the two halves of the ternary,
> are stubs pointing at `op_ternary`. (2) `precedence.yaml`: `NOT` leaves level 2 (unary `-.` added),
> level 12 is `!!`/NOT, the invented `!&&`/`!||` are gone, the ternary is a term in all blocks, level 17
> gains `=` (CON equate) and the missing `&&= ^^= ||= SCA= SCAS= FRAC=`. (3) Every `op_*.yaml` stub now
> carries the v55 row's description, priority, term/assign forms and block scope; `op_ABS`, `op_ADDBITS`,
> `op_ADDPINS`, the logical pages, `op_not`, `op_eqeq`/`op_ltgt`, `op_SCA`/`op_SCAS`, the shift family,
> `op_min`/`op_max`, `op_add`/`op_sub`/`op_mul`, the float pages, `op_inc`/`op_dec`, `op_assign`,
> `op_QLOG`/`op_QEXP`, `op_SQRT`/`op_FSQRT`/`op_FABS` and the compare pages were rewritten; `op_POW`
> is level 8 (left), the NaN/efficiency claims removed; `op_addmodulo` states `+//` is the unsigned
> remainder and that `(head - tail) +// size` fails for a negative difference (`-3 +// 30` = 13); `op_rand`
> lost the invented algorithm, period and speed claims. (4) `concepts/operators.yaml`: FRAC, REV/ZEROX/SIGNX
> (binary, priority 3), float list and CON float rule, `@`/`@@`/`^@`/`#`/`\`/`!`/`!!` entries,
> `wrap_modulo`, `safe_division`. (5) Coverage: new pages `op_bitnot` (`!`), `op_bitand`, `op_bitxor`,
> `op_bitor`, `op_postassign` (`\`), `op_equate` (`=`); unary `-` (negate) is documented on `op_sub`
> (one page per token, as `-.` is on `op_subdot`); the compound and unary assign forms sit on the page
> of the operator that owns them. (6) `spin2-language-schema.yaml`
> (17 priorities, 84 rows, no associativity field), `spin2-language-complete-map.yaml` (unsourced counts
> removed), `floating_point.yaml` (compares return 0 or -1), `guides/spin2-getting-started.yaml`
> (`<= >=`, `AND OR XOR NOT`, postfix forms), `special-symbols/hash.yaml` (PUB/PRI only), `FIELD.yaml`
> (v55: ten bits or larger need a LONG array, so the 12-bit example moved to LONG storage).
> **Compile-proof records («#421»):** the precedence of POW is not in the v55 table; the page states it
> from compile probes (`2.0 POW 3.0 +. 1.0` = 9.0, `1.0 +. 3.0 POW 2.0` = 16.0, `2.0 POW 3.0 POW 2.0` = 64.0)
> and cites **CP-006** (`op_POW.yaml:34`). The compiler's `Pointers cannot be arrays` is **CP-007**
> (`typed-pointers.yaml:238`). Both in `COMPILE-PROOFS.md`.
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

### F-546 — `instruction_skipping.yaml`'s absolute-CALL rule cites only the Silicon Doc; EF-092 proves it on silicon — `RESOLVED` (found 2026-10-04, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** Citation-only fix, so validated by absence live and presence in git. `p2kb_get p2kbPasm2InstructionSkipping` serves the rule unchanged ("If the instruction after a CALL/CALLPA/CALLPB might be skipped, its immediate branch address must be absolute (CALL #\\address ...)") and no `sources:` text; `git show v1.24.0:deliverables/ai/P2/language/pasm2/concepts/instruction_skipping.yaml:121` cites "... INSTRUCTION SKIPPING; bench-verified under XBYTE (a relative call # before a skipped instruction corrupted the VM, the absolute call #\\ ran it right), EF-092".
> **Applied 2026-10-07.** `skip_behavior.special_cases.sources` (now `:121`) cites EF-092 beside
> `silicon-doc-text.txt:889`; no content change. Proven: `:889` states the rule; EF-092
> (`P2-EMPIRICAL-FINDINGS.md:1652`, Rev C, two identical runs) — relative `call #` 4 of 5 wrong,
> absolute `call #\` all 5 right. Parsed value checked (`#\` survives YAML unescaping).

`language/pasm2/concepts/instruction_skipping.yaml:112` (rule) and `:121` (its source line). EF-092
(2026-10-04): under XBYTE, a relative `call #` before a line the pattern skips corrupted the VM (4 of 5
results wrong); the absolute `call #\` ran it right. **Fix:** add EF-092 to the `:121` source line
(hardware-verified, Rev C, cog execution under XBYTE); no content change. Held for the next KB release
so no committed-unreleased YAML blocks the manual releases under way (`kb-content-released`).

## Full impact audit: every fact KB v1.23.0 and v1.23.1 changed, against every live document (2026-10-04, «#378») — F-526 … F-541, plus F-542 … F-545 (seen verifying v1.23.1 and writing the MCP filter handoff)

### F-542 — `guides/pasm2-getting-started.yaml` teaches a wrong register map and P1 instructions — `RESOLVED` (found 2026-10-04, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbGuidePasm2GettingStarted` serves `register_model.special_registers` PA `$1F6` ... PTRA `$1F8`, PTRB `$1F9`, DIRA `$1FA`, DIRB `$1FB`, OUTA `$1FC`, OUTB `$1FD`, INA `$1FE`, INB `$1FF` with PA/PB as "CALLD-imm return, CALLPA parameter, or LOC address"; `SETS`/`SETD` in place of `MOVS`/`MOVD`; CALL "pushing {C, Z, 10'b0, PC[19:0]} onto the hardware stack -- not into PA" and RET "popping the stack"; `TJZ`/`TJNZ` "D is not changed" with `DJNZ` decrementing; `FIT $1F8`; CMP "C = borrow of (D - S)"; MUL "16 x 16 multiply"; WAITX "waits 1002 clocks" for `##1000`.
> **Applied 2026-10-07 per `SOURCE-REPAIR-ORDER.md`** — the four named blocks were uncited, so they
> were removed and re-derived source-first, not patched. Sources: the Parallax *P2 Instructions v35
> Rev B/C* spreadsheet (`sources/p2-instructions-csv/…Sheet1.csv`, each entry citing its `order`
> row), the P2 Documentation register map (`silicon-doc-text.txt:437-472`), and v55 `:302-323`
> for directives. Every example compiles (pnut-ts 1.55.8, one cog image, inside `FIT $1F8`).
> **Grounded fixes:** register map PA `$1F6` … INB `$1FF` with the Silicon Doc's roles (PA/PB are
> CALLD-imm/CALLPA/CALLPB/LOC registers; INA/INB also the debug-interrupt addresses); `MOVS`/`MOVD`
> → `SETS`/`SETD`; CALL pushes to the hardware stack, RET pops it; `TJZ`/`TJNZ` test only, `DJNZ`
> added; `FIT $1F8`. **Widened — wrong and not in the filing:** `CMP` "C=1 if D > S" (C is the
> borrow: D < S); `MUL` "lower 32 bits" (16 x 16); `WAITX ##1000` "wait 1000 clocks" (2 + D);
> LUT "same speed as cog registers" (RDLUT 3 clocks vs 2); "PTRA auto-increment is AFTER the
> access" (pre- and post-forms exist, `silicon-doc-text.txt:3189-3193`); every instruction's
> syntax now carries its `{#}`/flag-effect form. **Removals (uncited, no source found):**
> `cog_registers` "fast access (2 clock cycles)"/usage/naming lines; gotchas "flags persist",
> "labels must start in column 1", "comments use '", "pin numbers 0-63 … some contexts".
> **Gaps:** none. Two prose pointers to `rdlong.yaml`/`wrlong.yaml` went with the old timing
> strings; the guide gained a `related:` block to 13 per-instruction entries (findability).
> **The rest of the guide is F-551.**
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

### F-544 — the delivery filter deleted a line of the Edge modules' boot-pin note: a wrapped prose line began `sources:` — `RESOLVED` (found 2026-10-04, served in v1.23.3, verified 2026-10-04 via p2kb_get; MCP filter acceptance probe validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** This is the MCP filter roll's acceptance probe. With p2kb-mcp 1.5.0 applying the index `delivery_filter`, `p2kb_get p2kbHwEdgeStandardModuleEdgeStandardModule` and `p2kb_get p2kbHwEdge32mbModuleEdge32mbModule` both serve `pin_mapping.boot_pin_direction_note` whole: "P60 and P61 SWAP roles between the two boot sources: flash SPI CLK on P60 and flash SPI CS on P61, but microSD CS on P60 and microSD CLK on P61". `p2kb_get p2kbArchIoPinTiming` serves a `description` that ends at "...SYSTEM CHARACTERISTICS, pp.47-48." with no provenance line swallowed into or deleted from it (its `source:` is a top-level key, stripped).
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

### F-543 — `spin2/methods/pinstart.yaml` flash-FS example puts a clock-pin selector in X for sync TX/RX — `RESOLVED` (found 2026-10-04, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Pinstart` serves the smart-pin SPI example on the real flash pins: `PINSTART(SF_SDO, P_OE | P_SYNC_TX | P_PLUS1_B, %1_00111, 0)` (SF_SDO 59, B input = SCK at pin+1), `PINSTART(SF_SDI, P_SYNC_RX | P_PLUS2_B, %0_00111, 0)` (SF_SDI 58, SCK at pin+2), `PINSTART(SF_SCK, P_OE | P_PULSE, x, 0)` with `x.word[0]` = ticks per period and `x.word[1]` = ticks low, and the description "the data pins clock from SCK through the mode word's B-input selector (a relative pin offset), not through X; X carries only the sync-serial mode bit and the word size minus 1". The `SPI_CLK<<24` form and the flash-FS attribution are gone (`git grep` at `v1.24.0`: no hit).
> **Applied 2026-10-07 — and the defect was wider than filed.** The example's `source: P2-FLASH-FS`
> was false: the real driver (OBEX 4261, `flash_fs.spin2:44-50`) puts the flash on **P58–P61** —
> the example's 56/57 are the Eval/Edge **LEDs** — and never calls `PINSTART` or uses sync serial
> (it drives SCLK in transition mode from PASM, `:2801`). So the fix below re-sources the example
> rather than correcting it in place. Replaced with the smart-pin SPI pattern of `jm_ez_spi.spin2`
> `start()` (OBEX 2841, Jon McPhalen, `:62-79`) on the real flash pins: SDO 59 `P_SYNC_TX | P_PLUS1_B`,
> X `%1_00111`; SDI 58 `P_SYNC_RX | P_PLUS2_B`, X `%0_00111`; SCK 60 `P_PULSE`, X.word[0] period,
> X.word[1] low time. **Proven:** X.[5]/X.[4..0] per `silicon-doc-text.txt:4640-4677`; B-selector
> constants per `spin2-v55-text.txt:1438-1439`; pulse X fields per the Silicon Doc `%00100` section
> (high while the countdown > X.[31..16], so word[1] = ticks low). The code block extracted from the
> YAML compiles (pnut-ts, 6,368 bytes). `p2-reference.json` still carries the old text; it is
> regenerated by `release-yamls`.
`examples` (P2-FLASH-FS): `PINSTART(SPI_MOSI, P_SYNC_TX | P_OE, SPI_CLK<<24 | 8, 0)` and the same for
`P_SYNC_RX`. For `%11100`/`%11101` X.[5..0] is the mode and word size (`smart-pin-11100` x_register;
Silicon Doc); bits 24+ of X do nothing, and the clock is routed by the mode word's B field (a
relative-pin selector, e.g. `P_PLUS1_B`). `8` in X.[4..0] selects 9-bit words. The example cannot clock.
**Fix:** route the clock in the mode word (pins 56-59: MOSI 57 takes CLK 56 as `P_MINUS1_B`; MISO 58 as
`P_MINUS2_B`), X = `%1_00111` (or the intended word size), compile-check.

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

### F-525 — `flash-loader-case-study.yaml` tells the reader to read a narrative the KB does not ship — `RESOLVED` (found 2026-10-03, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbExampleFlashLoaderCaseStudy` serves `how_to_use_this_entry` as three lines — "Skim techniques_demonstrated for orientation", "Follow canonical links for depth on each technique", "Read the flash loader listing itself (Parallax SPI Flash Programmer and Boot Loader) for the full code" — with no `Flash-Loader-Theory-of-Operations.md` pointer (`git grep Theory-of-Operations` at `v1.24.0` over `deliverables/ai/P2`: no hit).
> **Decided and applied 2026-10-07: drop the instruction.** `Flash-Loader-Theory-of-Operations.md`
> is our own derived analysis of Chip Gracey's source — the ingestion dashboard classes it
> "derived analysis docs … not raw extraction" (`engineering/ingestion/README.md:136`); its own
> header frames it as "what we can learn about the P2 from studying it". It is published nowhere a
> reader can reach and is not a source, so neither "name the location" nor "carry its substance
> into the KB" applies. The `how_to_use_this_entry` line naming it is removed; "Read
> flash_loader.spin2 itself for source-of-truth" stays.
Found 2026-10-03 while sweeping F-523. `code-examples/flash-loader-case-study.yaml` `how_to_use_this_entry`:
"Read Flash-Loader-Theory-of-Operations.md (companion narrative) for the full walkthrough". The file lives in
this repo at `engineering/ingestion/sources/flash-loader/` and is not in the KB tree, so a consuming agent
cannot fetch it by that name. Not a citation (it is a reading instruction), so F-523's move does not
apply, and rewording it changes what the entry tells the reader. **To decide:** whether the narrative
is published anywhere a reader can reach (e.g. the PNut-TS repository, where its subject
`src/ext/flash_loader.spin2` lives). If it is, name that location; if not, either carry its substance
into the KB (a code-example companion) or drop the instruction and keep "read flash_loader.spin2 itself".

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

### F-454 — `edge-standard-module.yaml` lost its revision history, leaving a VIN maximum that destroys Rev A/B boards — `RESOLVED` (found 2026-09-22, fix applied 2026-09-22; the gate this entry named built 2026-10-09, «#410», and driven to 0 on 2026-10-10, «#420»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbHwEdgeStandardModuleEdgeStandardModule` serves `power.input_voltage` "5-16 VDC on Rev C and later ... On Rev A and Rev B the VIN maximum is 5.5 VDC", `ratings.vin` "Maximum 16 V on Rev C and later; maximum 5.5 V on Rev A and Rev B. Applying 16 V to a Rev A or Rev B module exceeds its absolute maximum by roughly three times", and the `board_revisions` block (rev_b `vin_maximum: "5.5 V"`, rev_c "VIN voltage maximum increased from 5.5 V to 16 V", rev_d). The scope decisions for the other files are served too: `p2kb_get p2kbHwEdge32mbModuleEdge32mbModule` serves `board_revisions.rev_b` / `earlier_hardware` ("the Rev B VIN figures are not asserted for it") and "(Rev B)" on `vin` and `input_voltage`.

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
> it. The gate that flags a shipped absolute-maximum stated without its board revision was owed;
> it is built (`audit-hardware-revision-scope.py`, below).

> **Gate built («#410») and driven to 0 («#420», 2026-10-10); final run 2026-10-10: 29 files scanned,
> 8 declare a revision, R-A 0, R-B 0.** `audit-hardware-revision-scope.py`
> went 12 findings in 7 files → 0. Each file now records its scope decision against its guide's
> Revision History: `board_revisions:` (Rev B/earlier deltas, source + page) in `edge-32mb-module`
> (also "(Rev B)" on `vin` and `input_voltage`), `edge-breadboard-carrier` (Rev B power-switch discharge;
> "(Rev B; no change from Rev A)" on the 5 / 5.5 VDC ratings), `p2-eval-board` (the Rev C "What's New"
> list; "(Rev C)" on the USB supply rating), `addon-motor-driver` (Rev B vs Rev A) and
> `addon-goertzel-touch` (touch pads vs probe posts); `revision_scope_reviewed:` in `edge-mini-breakout`
> (v1.1: guide edits only) and `edge-standard-breakout` (v1.0: single version). No file states a
> rating for a revision whose guide gives none: the Rev A figures are marked "not asserted".

## The provenance strip reaches two of its three consumers — F-439

### F-439 — the MCP serves provenance the fetch scripts no longer send — `RESOLVED` (found 2026-09-19 at the v1.19.0 publish verification; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** p2kb-mcp 1.5.0 applies the index's `delivery_filter`: `p2kb_version` reports
`filter_rule_source: index`, `filter_rule_id` `7dc618e4…` (the agreed rule). Live probes: PINSTART serves
no `sources:` and keeps the %11100 sentence; Instruction Skipping has no column-0 comment and keeps the
AUGS rule; the motor driver has no `source:` and no `engineering/ingestion` path; `REG_ARRAY: {source:
"cog registers", …}` survives (a content key inside a flow map is untouched); the Edge module keeps
"boot sources: flash SPI CLK on P60"; OBEX object 2842 served by `p2kb_get` has no `scrape_tracking` and
no `compatibility.source`. Record: `correction-sweeps/2026-10-11-close-out-release-mcp-test.md` step 5.
The curated `p2kb_obex_get` view has a separate field-mapping defect, F-571.

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

### F-436 — the `map_caveat` retraction is confirmed on the released compiler; applied — `RESOLVED` (found 2026-09-17, applied 2026-09-19, last residue applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2ObjectImageDedup` serves `map_caveat` ("The .map format changed at pnut-ts 1.55.8: there is no `Objects:` line ... Its labels are reliable ...") and, for the two lines that still carried byte pairs, relations only: `the_other_silent_trap` "Result: 3 images with none shared, against 2 images with the driver's shared when both declarations carry the override -- and more Code/DAT bytes", `completeness_rule` "Forwarding one of two gives 4 images, two of them the driver's. Adding the missing forwarding constant: 3 images, one driver image shared -- and fewer Code/DAT bytes." The old pairs ("348 vs 216", "372 ... 240") are absent.
> **Applied 2026-10-07.** The two byte pairs (`singleton_rule` "Objects 3 vs 2, 348 vs 216", and
> `completeness_rule` "Objects 4, 372 … Objects 3, 240") were still in the file. Re-measured on
> pnut-ts 1.55.8 with fresh fixtures, reading the `.map` SUMMARY: the mirror trap (one declaration
> overridden, its sibling not) → **3 images, none shared, 136 Code/DAT bytes** vs both overridden →
> **2 images, one shared, 92**; forwarding one of two DAT-sizing CONs → **4 images, none shared,
> 176** vs adding the missing constant → **3 images, one shared, 124**. Both lines now state the
> image counts (structure-determined) and the byte *relation*; the absolute bytes are
> fixture-dependent and are not carried. Both relations already stood in `verification.measured`.

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

### F-421 — `ROM_Booter.lst` is an FPGA build; only `rom_booter_v33_01j.lst` is the Prop2 silicon ROM — `RESOLVED` (found 2026-09-10, the KB half applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** The citations are provenance, so validated by absence live and presence in git. `p2kb_get p2kbArchSerialLoader` and `p2kb_get p2kbArchBootRomContents` serve no listing name and no FPGA-build clock constants; `git grep "ROM_Booter\.lst"` at `v1.24.0` over `deliverables/ai/P2` returns nothing, while `serial_loader.yaml:14,194`, `boot-pattern-selection.yaml:67-70` and `boot-rom-contents.yaml` cite "Parallax Propeller 2 ROM Booter v33_01j" (the silicon listing) by section (CON block `rc_max`, `timeout_per`, Command - clock setup, Serial done).
> **Correction 2026-10-07 (F-555):** "neither is a newer revision" is wrong — `ROM_Booter.lst` is
> an **earlier revision** (history ends v141, 2018-05-27, `:84-85`; the silicon listing adds the
> 2019 v33_01a..j revisions, `rom_booter_v33_01j.lst:87-93`). It IS an FPGA build, but the proof
> is `ROM_Booter.lst:118` (`ver = "A" 'Prop123-A9 / BeMicro-A9`), boards the P2 Documentation lists
> as FPGA boards (`silicon-doc-text.txt:2876`, `:2950-2951`) — not `_clockfpga`, which is defined
> and never used. The re-citation to the silicon listing stands; the shipped label is fixed under
> F-555.
>
> **Applied 2026-10-07.** Every shipped citation of `ROM_Booter.lst` now names the silicon listing.
> **Line-anchored ones were re-derived, not renamed:** each cited FPGA line was read and its
> counterpart found in `rom_booter_v33_01j.lst` with identical code — `serial_loader.yaml`
> `serial_done` :750-752 → **:758-760**; `boot-pattern-selection.yaml` `rc_max`/`timeout_per`
> :146,426 → **:154,434**, the Prop_Clk RCFAST-then-full HUBSET switch :578-587 → **:586-595**, the
> shutdown `hubset #1` :754-756 → **:762-764**. Unanchored mentions (`boot-rom-contents`,
> `spi-flash-boot`, `taqoz-forth`, `p2-monitor`, `sd-card-boot`, `_index`) now name
> `rom_booter_v33_01j.lst, the Prop2 silicon build`, after confirming that listing carries what
> each points at (SD/FAT32, Monitor, TAQOZ, flash). `boot-rom-contents` `source_listing` labels
> `ROM_Booter.lst` as the FPGA build. The two Edge-module notes titled "Parallax ROM_Booter
> listing" already cite the silicon file (`:135-138`) and were left. **Surfaced: F-550.**

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

## The hardware selection guide ships 2025 US retail prices as data, in a set with no mechanism to age them (2026-08-30, release fix pass step 1) — F-398

### F-398 — ~15 USD price sites across `p2-hardware-selection-guide.yaml`; needs a policy call, not a citation — `RESOLVED` (found 2026-08-30, decided 2026-10-08 and applied 2026-10-10, «#420»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbHwP2HardwareSelectionGuideP2HardwareSelectionGuide` serves `pricing: "For current pricing, see the Parallax store (parallax.com)."` and no dollar figure, `cost_estimate`, `total_investment`, `additional_cost` or `total_cost` key; the relative tiering stays (`ultra_budget_entry`, `value_balanced`, `capability_maximized`, "Lower cost, all pins accessible").

> **DECIDED by Stephen 2026-10-08 (option a) and APPLIED 2026-10-10 («#420»).** Every dollar figure
> (22 sites) is deleted from `hardware/p2-hardware-selection-guide.yaml`; the relative tiering (cheapest
> to dearest, and what each tier adds) stays; the file carries the one line
> `pricing: "For current pricing, see the Parallax store (parallax.com)."` (`:13`). Verified 2026-10-10:
> `grep -n '\$[0-9]'` over the file returns nothing and no `cost_estimate` / `total_investment` key
> remains anywhere under `deliverables/ai/P2/hardware/`.

**Registered as a definition call, and it is the sibling of F-374.**

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

**Why it waited for a decision before it was swept.** The disposition is a judgement with a real cost either
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

### F-392 — the KB documents `cogspin`/`TASKSPIN` stacks and is silent on the stack every Spin2 program already has; the sizing numbers it does ship are unsourced and are cited back as authority — `RESOLVED` (found 2026-08-30, applied in stages, 2026-10-09 «#414» and 2026-10-10 «#423»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Cogspin` serves `stack_requirements` as "No Parallax document states a stack size for COGSPIN. Size the buffer by measuring the high-water mark" with `p1_symbols_do_not_apply` ("P1's _STACK and _FREE declarations do not exist in Spin2 and have no effect if written"), `StackAddress` as "Size it for the method's worst case" (no "Minimum 32 longs"), the new `top_level_stack` block (`placement` after VAR space, `first_frame` 6-long header, `growth` "grows upward ... a return pops 7 longs", `size_and_limit` "Not documented ... no overflow check is documented") and `stack_observability` (any cog can read a COGSPIN/TASKSPIN buffer; PTRA is private; COGBRK from a debug ISR). `git grep -i -E "minimum (of )?[0-9]+ longs"` at `v1.24.0` over `deliverables/ai/P2`: no hit.

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
> ⏳ **CARVED OUT, and the named expiry has ARRIVED: the v55 interpreter was ingested 2026-10-09
> («#401», `external-inputs/source-code/spin-interpreter/v55/`).** Documenting the stack that every
> Spin2 program already has (the top-level cog's, its `DBASE` frame and the 6-long *Drop anchor*
> entry) needed a v55 interpreter source rather than v51 internals presented as v55 behaviour; that
> source now exists. **Not landed:** no sprint task wrote it (study row S-319, "home file decided in
> the sprint"; a search of `deliverables/ai/P2` for `DBASE`, *Drop anchor*, a top-level-stack entry
> returns nothing, 2026-10-10). Owed: items (1)-(5) below, read off the v55 listing, in a home file
> the next KB pass picks.
>
> **Applied 2026-10-09 («#414», `PENDING-VALIDATION` for this part only).** Two more sites carried the
> same unsourced floor and contradicted the fix above: `cogspin.yaml` `parameters` → `StackAddress`
> ("Minimum 32 longs recommended") now reads "Size it for the method's worst case; see
> stack_requirements below", and `guides/quick-queries.yaml` ("Check stack size (minimum 32 longs)")
> now tells the reader to check the COGSPIN stack against the method's worst case and measure the
> high-water mark. Class sweep `grep -rn -i -E "minimum (of )?[0-9]+ longs"` over `deliverables/ai/P2`: no hit remains.
>
> **Applied 2026-10-10 («#423»): the top-level stack, read off the v55 interpreter listing.** New
> `top_level_stack:` block in `language/spin2/methods/cogspin.yaml` (placement after VAR space via
> `dbase_init`/`var_longs`; 6-long first frame from `launch_spin`/`launch_method`; upward growth;
> 6-long drop anchor + return-address long = 7 popped per return; size and overflow check stated
> as **not documented**, since neither Spin2 v55 nor the listing states a size and the listing
> compares `PTRA` against no limit). `related:` links added both ways with `taskspin.yaml` and
> `p2an006`. **Corrections to the items below:** item 3's "exactly 6 longs" is the drop anchor
> alone — a return pops 7 (`returnh`), the top-level first frame is 6; item 4's `$7FFFF`/`$7BFFF`
> ceiling is **not** in the listing or Spin2 v55 (the listing's `$80000` is a zero-fill source in
> `launch_spin`, not a stack bound) and was not carried; item 5 (observability, `COGBRK`) landed as
> `cogspin.yaml` `stack_observability`, cited to the P2 Documentation v35 OVERVIEW / COGS / DEBUG
> INTERRUPT, with a `related:` link to `debug_interrupt.yaml` (its "only route" wording not carried —
> no source says *only*).

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

### F-393 — the KB documents DEBUG's syntax and display commands and not one of the resources DEBUG takes away from the application — `RESOLVED` (found 2026-08-30, the last residue applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2DbgDebugStrategyGuide` serves `what_a_debug_build_takes_from_your_program` with `hub_memory` ("top 16 KB, $7C000..$7FFFF, remapped to $FC000..$FFFFF and write-protected ... writes are SILENTLY DROPPED"), `protected_region_use` (DEBUG data, debugger, and "$FFC00..$FFFFF, one 128-byte block per cog (cog 7 at $FFC00 through cog 0 at $FFF80)"), `a_lock` ("LOCK[15] is held"), `pins_62_63`, `hubset_enables_locked`, `clock_source` ("at least 10 MHz") and `interrupt_retrigger_can_stop_for_good` ("the interrupt cycling stops permanently, not just late ... CT-based interrupts are not prone to it"). `p2kb_get p2kbSpin2Locknew` serves the cross-link in `related:` (`language/spin2/debug-commands/debug-strategy-guide.yaml`, with the comment "A DEBUG build takes one of the sixteen locks before your program runs"). The entry's "not done, low value, expiry: the next DEBUG touch" item (the `$FEA00` / `$FF1A0` debugger-internal layout in `debug_interrupt.yaml` / `hub.yaml`) is still not in those two files (`git grep` at `v1.24.0`); the served guide deliberately states only the silicon-fixed per-cog blocks at `$FFC00..$FFFFF` and says "how the debugger arranges the rest is its own and can change with the tool". Closed on that reading; if the layout is wanted after all, it is a new item, not an unserved part of this one.
> **Applied 2026-10-07.** `debug-strategy-guide.yaml` `what_a_debug_build_takes_from_your_program`
> gained `protected_region_layout` beside `hub_memory`: `$FC000` DEBUG data, `$FEA00` the debugged
> cog's `$010..$1F7` buffer, `$FF1A0` debugger + overlays + data to `$FFC00`, then the per-cog
> 128-byte blocks `$FFC00` (cog 7) … `$FFF80` (cog 0). **Proven** from the Parallax debugger source
> (`Spin2_debugger.spin2` v51 2025.04.02, `:7-10` CON, `:20-49` map) and, for the per-cog blocks it
> marks "fixed in silicon", against the P2 Documentation table 25 (`silicon-doc-text.txt:2446-2477`
> — identical addresses). The block's `source:` now also cites `hub_memory` (v55 `:900`), which was
> uncited. Placed in the debug-build cost list rather than `debug_interrupt.yaml`, which already
> carries the silicon half (`:79-87`); only v51's debugger source is held, so a later debugger's
> layout is not verified.

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

### F-383 — `p2kbSpin2DbgDebugStrategyGuide` lists three peer numbers, and the one that mutes a board is not marked — `RESOLVED` (found 2026-08-30, applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2DbgDebugStrategyGuide` serves the guide in its final F-559 shape, which supersedes the numeric `hard_limits` wording this entry first applied: no peer numbers at all; `the_compilers_limits.how_it_fails` ("the build fails at compile time with 'DEBUG data is too long' ... m153 / m150 / m151"), the `-d -l` listing method (`DEBUG records:` / `DEBUG data:`), `which_you_reach_first` (shape of the output decides, "Watch both lines of the listing"), `reducing_bytes_and_records` with `reduces_debug_bytes` in the mechanism table, `debug_mask.per_object` (a parent can set a child's `DEBUG_MASK` at instantiation), and `binary_size_is_not_the_measure`. The refuted "fails silently / mutes the board" claim is not carried.
> **Applied 2026-10-07 — by measurement on pnut-ts 1.55.8, and two of this entry's claims did not
> survive it.** Instrument: `pnut-ts -d -l` — the listing states both budgets directly (`DEBUG
> records: N of 255`, `DEBUG data: N of 15872 bytes`). Fixtures (scratch, regenerable):
> 100 × 154-byte records = **15,800 of 15,872 compiles; +1 char each fails** `total exceeds 16384
> bytes (m151)`; a 260-char literal fails `record exceeds 255 bytes (m150)`. Three labelled
> statements 62 B/3 rec · `DEBUG_DISABLE = 1` 0/0 · `DEBUG_MASK = 0` with `debug[0]` 0/0 ·
> `DEBUG_COGS = 1` 62/3 · `debug(if(v),…)` 65/3 · two `zstr_()` in one statement 4 B vs one 3 B
> (1 rec each) · `zstr_(@a/@b/@c), udec(v)` ×3 → **1 record, 6 B** · `udec(x)`/`udec(y)` 2 rec ·
> `udec_(x)`/`udec_(y)` 1 rec · no statements: `-d` adds 2,934 B to the binary, DEBUG data 0.
> **Refuted:** (a)/(c) "fails SILENTLY, no compiler error" — the compile-time cap is loud (m151);
> the reported *runtime* mute under the cap is **not carried** — Stephen 2026-10-07, striking
> VO-J-027: *"(1) it's soft not specific, (2) it's likely compiler version specific"*; a per-version,
> per-program threshold is tool behaviour, not a P2 fact, so the guide states only the loud
> compile-time limit and the listing method.
> (e) "~2,945 bytes, 18% of the budget, gone before the first debug()" — that is the debugger
> image in the binary (2,934 B with zero statements), not DEBUG data (reads 0); the
> subtraction method (g) measures that larger quantity, so the listing replaces it.
> (f) "DEBUG_MASK cannot be overridden at instantiation" — `OBJ c : "child" | DEBUG_MASK = 1`
> takes a mask-0 child from 0 records to 1 (control: no override, 0); the KB now states the
> override. **Mapping (d), now measured:** DAT + `zstr_()` cuts bytes, and records too when
> statements become byte-identical (value-only forms store no label, v55 `:918`); coalescing
> `zstr_()` calls cuts bytes only; buffer-formatted lines are one record for any number of call
> sites. **Applied:** `hard_limits` (limit 15,872, both failure modes, what is counted, the
> listing method), `the_two_budgets_…` rewritten from the fixtures, `reduces_debug_bytes`
> column, `debug_mask.per_object`, the stale "hit first" note replaced. (7) is F-389.

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

### F-386 — `p2kbArchSmartPins` now warns by name against the call `p2kbArchSmartPin01110CountAEdgesOptionalBDec` demonstrates twice — `RESOLVED` (found 2026-08-30, class sweep run 2026-10-07, «#387»; the nine mode pages settled by EF-097 on 2026-10-10, «#419»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbArchSmartPins` serves `correct_sequence.note` with the nine order-safe modes named ("the counter and timing modes %01110, %01111, %10010-%10111 and the external-clock ADC mode %11001: a Y written while DIR is low is in force after DIRH"), the `%11100` exception, and "PINSTART()/pinstart() writes Y before raising DIR, so it is NOT safe for the trigger modes or asynchronous serial transmit"; `p2kb_get p2kbArchSmartPin01110CountAEdgesOptionalBDec` serves the PASM example `dirh #counter_pin` then `wypin #0, #counter_pin  ' Count A only - Y AFTER DIRH` and `configuration_order.about_pinstart` ("%01110 is a counting mode, not a trigger mode ... pinstart() is safe here") — no longer a page that contradicts the general one.
> **Sweep run 2026-10-07 over all 33 files in `architecture/smart-pins/`.** Two shapes searched:
> `pinstart` with a non-zero Y in a mode that loses it, and `wypin` before `dirh`.
> **Trigger and async-TX pages are clean** — the only `pinstart` calls in those modes
> (`smart-pin-11110…:51, :120, :137, :149`) pass Y = 0. **The general rule itself was wrong, and is
> fixed:** `smart_pins.yaml` `correct_sequence` said "the serial modes hold Y at 0 during reset" and
> that Y-after-enable is "correct for EVERY mode". EF-011 measured only async TX among the serial
> modes; EF-090 proved sync TX `%11100` continuous **primes** its first word during reset and loses
> it if enabled first (P2 Documentation `:4650` says the same). The note now names the measured
> modes on each side and carries the `%11100` exception; its `source:` cites EF-011, EF-090 and
> `:4650`. **Eight pages write a configuration Y before `DIRH`** (`%01111`, `%10010`–`%10111`,
> `%11001`; `%11100` does too, correctly — that is the priming write). *(Corrected 2026-10-07,
> F-554: the original list named nine and was counted as "ten"; `%11011` USB has a documented
> order — `silicon-doc-text.txt:4593`, WYPIN after DIR is set — so its page was fixed, not left to
> VO-J-028.)* The P2
> Documentation states Y's reset behaviour per mode — "set to zero" for pulse/transition
> (`:3984`, `:3997`), "captured" for PWM (`:4050-4086`), and **nothing about Y** for
> %01100–%10111 (`:4116-4254`, Z only). Neither order is proven safe or harmful for those eight, so
> they are **not reordered** on inference: VO-J-028 (jumper-only) decides it.

> **Settled 2026-10-10 («#419»): EF-097 — order-safe, all nine; no reorder.** VO-J-028 ran (nine
> modes: `%01110`, `%01111`, `%10010`–`%10111`, `%11001`; `%01110` added to the eight). In every mode a Y
> written with WYPIN while DIR is low is in force after DIRH. Each of the nine mode pages now states it
> (a `notes` line and a `configuration_order.source` citing EF-097), `smart_pins.yaml`
> `critical_requirements.reset_before_configure` names the nine beside NCO and DAC-noise, and the
> `%01110` page's "NOT STATED … immunity" paragraph became the measured statement (so `pinstart()` is
> safe there). Limits carried: one board, one Y value pair per mode, internal routing only.

> **The named page is done, verified in the tree 2026-09-22.**
> `architecture/smart-pins/smart-pin-01110-count-a-edges-optional-b-dec.yaml:64-65` now runs `dirh`
> before `wypin` with the comment `' Count A only - Y AFTER DIRH`; `:70-83` adds a
> `configuration_order:` block stating the universal order and recording "(This page previously
> showed WYPIN before DIRH.)"; `:77-83` explains that `%01110` is a counting rather than a trigger
> mode, so the general page's exclusion does not apply, and marks the immunity question as NOT
> STATED by any source we hold.
>
> **The sweep this entry required (the other ~30 mode pages under `architecture/smart-pins/`, for
> `wypin` before `dirh` and for `pinstart(...)` in a trigger mode) was RUN 2026-10-07 — the first
> block of this entry — and its one open question, the nine counter-mode pages, was decided on
> silicon by EF-097 (the second block).**

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

### F-387 — `language/spin2/concepts/operators.yaml` annotates `~` and `~~` as P1 differences and leaves `||` unmarked — `RESOLVED` (found 2026-08-30, `||` note applied 2026-09-22, the class sweep applied 2026-10-07, «#387»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** `p2kb_get p2kbSpin2Operators` serves the `["||", "OR"]` note "P2 Spin2 semantics; not P1 absolute value. In P1 '||' was the Absolute Value operator. For absolute value on P2 use ABS." and the new `changed_from_p1` block in two tiers: `compiles_with_a_different_meaning` (`a ~> 2` read as `(a~) > 2` that CLEARS a; `a <- 2` read as `a < -2`; `<=`/`>=` as the P1 assignment forms) and `fails_to_compile` (`||a`, `?x / x?`, `^^x`, `~x / ~~x`, `**`, `|< x`, `>| x`, `->`, `>< n`, `=<`/`=>`), each with its Spin2 spelling.
> **Class sweep applied 2026-10-07.** Every row of P1 Manual Table 2-9 (`p1-…-layout-text.txt:4934-4975`)
> was compared with the v55 operator table (`spin2-v55-text.txt:409-491`) and each P1 form compiled on
> pnut-ts 1.55.8. New top-level `changed_from_p1` in `operators.yaml`, two tiers:
> **compiles with a different meaning (silent)** — `a ~> 2` is `(a~) > 2` and *clears a*; `a <- 2` is
> `a < -2`; `c := a <= b` is a compare where P1's `<=`/`>=` were the assignment forms of `<`/`>`;
> binary `||` is logical OR — the first three **proven by byte-identical binaries** against the
> explicit spelling. **Fails to compile (loud)** — `?x`/`x?`, `^^x`, prefix `~x`/`~~x`, `**`, `|<`,
> `>|`, `->`, `><`, `=<`, `=>` — each with its v55 spelling. `REV` takes the top bit index, so P1
> `>< n` is `REV (n-1)`: P1's own `Y >< 6` example folds to the same value under `REV 5`. Every P2
> spelling compiles; `SIGNX 7/15` folds to the sign-extended values. **Two of the three silent
> cases (`~>`, `<-`) were not in the filing** — they were found only by compiling the P1 forms.

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

### F-389 — key generation abbreviates and drops path components, so whole subtrees vanish from the term that names them — `RESOLVED` (found 2026-08-30, gate built 2026-10-09, «#410»; partial-reach directories dispositioned 2026-10-10, «#420»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** The aliases added for the four partial-reach directories resolve live: `p2kb_find "debug command"` → `p2kbSpin2DbgCZ`, `p2kbSpin2DbgDly`, `p2kbSpin2DbgPcKey`, `p2kbSpin2DbgPcMouse`; `p2kb_find "boot ROM TAQOZ"` → `p2kbArchTaqozForth` and `p2kb_get "boot ROM monitor"` → `p2kbArchP2Monitor` (`resolved_from` the alias); `p2kb_find "system registers"` → `p2kbArchCompleteSystemRegistersIndex`, `p2kbArchPtraRegister`; `p2kb_find "Spin2 conventions JonnyMac"` → `p2kbSpin2JohnnyMacDocumentationStyle` and `"Spin2 formatting conventions"` → `p2kbSpin2Spin2FormattingStandards`. The symptom/compiler-string route the entry asked for also resolves: `p2kb_get "debug data too long"` → `p2kbSpin2DbgDebugStrategyGuide`. The four baselined wide directories (`operators`, `registers`, `patterns/implementation`, `preprocessor`) remain the arbiter's judgement, as the entry states.

> **Component-survival check built and driven to 0.**
> `engineering/tools/validation/audit-index-findability.py` (in the DoD as *Index Findability by
> Directory Term (F-389)*; term = a directory's own name, reach = key + alias + category) found 8
> partial-reach directories (141 files) on 2026-10-10. Four gained aliases so the directory's name reaches
> every file (`architecture/boot-rom`, `architecture/system-registers`, `language/spin2/conventions`,
> `language/spin2/debug-commands`); four wide directories are in the reviewed baseline
> `engineering/tools/validation/baselines/index-findability.json`, each with its reason
> (`language/spin2/operators` 1/83, `registers` 1/18, `patterns/implementation` 1/19, `preprocessor` 2/14
> — one page per operator / register / pattern / directive, found by that page's own name). Final run
> 2026-10-10: 31 qualifying directories, 0 partial not baselined, 4 baselined, 14 reached by none
> (advisory). **The generator's key abbreviation is unchanged** — key names are what consumers address
> pages by; the remedy chosen (study S-387) is the gate plus alias vocabulary, and the four baselined
> directories are a judgement the arbiter may overrule (the alternative is a literal "operators" /
> "registers" alias on 129 pages). What the gate cannot see: a vocabulary gap — a query no alias answers.

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

> **Gate built («#410»); its 8 partial-reach directories dispositioned («#420», 2026-10-10).**
> `audit-index-findability.py` (term = the directory's own name; reach = key + alias + category) found 8
> partial directories (141 files). Four gained aliases so the directory's name reaches every file:
> `architecture/boot-rom` (`p2-monitor`, `taqoz-forth`: "boot ROM monitor", "boot ROM TAQOZ" …),
> `architecture/system-registers` (`ptra-register`), `language/spin2/conventions` (five pages: "Spin2
> conventions JonnyMac", "Spin2 formatting conventions" …), `language/spin2/debug-commands` (`c-z`,
> `dly`, `pc_key`, `pc_mouse`: "debug command …"). Four are in the new reviewed baseline
> `engineering/tools/validation/baselines/index-findability.json`, each with its reason:
> `language/spin2/operators` (1/83), `registers` (1/18), `patterns/implementation` (1/19),
> `preprocessor` (2/14) — one page per operator / register / pattern / directive, found by that page's own
> name, the directory word being a grouping word. **The 12 alias additions are not yet visible to the
> gate:** it reads `deliverables/ai/p2kb-index.json`, which is regenerated after commit (index
> generator needs history); until then it still reports those four directories. The baselining of the
> four wide directories is a judgement the arbiter may overrule — the alternative is a literal
> "operators"/"registers"/… alias on 129 pages.

---

## Citing ONE block in a wholly-uncited file turns its other blocks Tier-1 RED — 32 uncited quantity blocks across 24 files are structurally invisible to the blocking gate (2026-08-29, «#334», proved by accident) — F-381

### F-381 — the Tier-2 advisory class is not "reviewed and accepted", it is "no control available" — `RESOLVED` (found 2026-08-29, Tier 2 blocking and at 0 since 2026-10-10, «#422»; validated 2026-10-11 on p2kb-mcp 1.5.0 against KB v1.24.0, «#398»)

**Validated 2026-10-11.** A gate finding, so the served evidence is sampled, not the 32-block census (re-measuring that needs `audit-yaml-claim-sourcing.py`, not run here). In the tag: `git show v1.24.0:engineering/tools/validation/audit-yaml-claim-sourcing.py` has `TIER2_BLOCKING = True` (`:871`). The sourced files are in the tag and served: `git diff v1.23.3 v1.24.0` shows `language/pasm2/hubset.yaml` and `asmclk.yaml` re-cited to canonical titles with edition and page, `architecture/decomposition/rate-adaptation.yaml` and three more decomposition pages losing unsourced Hz figures ("servos want a smooth stream at their frame rate"), and `hardware/hardware-compatibility-matrix.yaml` carrying a `source:` per block (read in the tag); live, `p2kb_get p2kbPasm2Hubset` serves the same content with no `source:` text, and `p2kb_get p2kbHwP2HardwareSelectionGuideP2HardwareSelectionGuide` serves no dollar figures.

> **APPLIED 2026-10-10 («#412», «#422»).** `audit-yaml-claim-sourcing.py` now blocks on wholly-uncited
> files (`TIER2_BLOCKING` switched on, commit 89eb8c02) and accepts only a canonical Parallax title with
> its edition (and page), a source listing pinned to its edition, an EF/CP/XF id or an OBEX id as a
> citation. Final run 2026-10-10: **3 Tier 1 + 0 BAD_CITATION + 0 Tier 2** across 1,005 files, all 3 in
> `hardware/hub75_adapter.yaml` (an Iron Sheep board no Parallax document can cite — F-567, Stephen's
> call). The Tier-2 population this entry measured (32 blocks in 24 files) is now 0, and Tier 2 blocks.

> **DECIDED by Stephen 2026-10-08: ready to fix.** The gate blocks on wholly-uncited files.
> - **Source every number that drives code generation:** P2 limits, timings, register and field
>   values, ranges, constants.
> - **Numbers inside examples pass when the example is correct.** That means it compiles (ENH-03)
>   and every P2 fact it states or relies on agrees with the sourced facts. This includes comments
>   and formulas such as X = sysclk / baud. The example's own choices (baud, pins, "suppose 1 kHz")
>   pass. A wrong P2 fact makes the example wrong, and it is fixed.
> - **A P2 fact stated only inside an example** is sourced in its proper home, and the example
>   stays.
> - **How the gate tells them apart:** by location. Numbers in example blocks are exempt.
> - **OBEX is self-referencing.** OBEX numbers are never sourced. Only check that OBEX
>   references agree with the OBEX index.
> - **"Be extremely careful":** removal is the last resort. Search the sources exhaustively
>   first. A number we can test on the jumper bench becomes a bench item and stays served until the
>   bench decides. Remove it only if it can be neither sourced nor tested.

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

**The scope call was made** (Stephen, 2026-10-08, the decision block above): OBEX numbers are never
sourced (the gate accepts an OBEX id), numbers inside correct example blocks pass by location, and every
other quantity is sourced or comes out; the decomposition layer's worked examples are tagged
`authority_tier: EXAMPLE`, which the gate reads.

---

