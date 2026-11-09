# Silicon Doc walk, range 4: SD:2035-2865

Events, interrupts, debug interrupt, BRK/COGBRK/GETBRK, HUBSET (clock, write-protect/debug, filters, PRNG, reboot).
All 831 lines read. KB = `deliverables/ai/P2/` (paths below are relative to it). `pasm2/` = `language/pasm2/`.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 2035 | EVENTS (16-event list) | Carried, `architecture/event_system.yaml:27-51`. MATCH. |
| 2061 | POLLxxx list | Carried on each poll page and `event_system.yaml`. MATCH. |
| 2082 | WAITxxx list + SETQ timeout | Carried on every WAITxxx page (all 15 mention SETQ). MATCH. No WAITQMT: MATCH. |
| 2104 | Jxxx/JNxxx | Branch carried. "Flag cleared whether or not the branch occurs" is missing from 25 of the 32 J pages. NOT-CARRIED there. |
| 2124-2211 | Per-flag set/clear rules | Carried on the POLL/WAIT pages. The consolidated table is IN-PLAN §6 (`event_clearing`). |
| 2215 | Example ADDCT1/WAITCT1 | Carried, `pasm2/addct1.yaml:12`, `pollct1.yaml`, `waitct1.yaml:14` (MSB rule). MATCH. |
| 2230 | Selectable Events / SETSEn encoding | Carried, `event_system.yaml:101-114`, `pasm2/setse1.yaml`. MATCH. |
| 2262 | INTERRUPTS (priority, STALLI/ALLOWI, 16 sources) | Carried, `architecture/interrupts.yaml`. MATCH. |
| 2294 | IJMP/IRET map | Carried, `interrupts.yaml:100-129`. MATCH. |
| 2304 | RETIx / RESIx as CALLD | Concept pages MATCH. The eight per-instruction pages say C/Z "No effect". MISMATCH. |
| 2320-2345 | SETINTx / TRGINTx / NIXINTx / ALLOWI / STALLI | Carried. TRGINT is IN-PLAN §1. NIXINT pages are PARTIAL. |
| 2347-2357 | Branch-deferral conditions | Carried, `interrupts.yaml:431-438`. MATCH. |
| 2359 | Dispatch = inserted CALLD | Carried, `interrupts.yaml:411-415`. MATCH. |
| 2361-2367 | Three-state loop; same-level events ignored | NOT-CARRIED (only "same level cannot interrupt itself"). |
| 2370 | Example INT1/CT1 | Equivalent pattern at `interrupts.yaml:327-339`. MATCH. |
| 2393 | DEBUG INTERRUPT | Carried, `architecture/debug_interrupt.yaml`. MATCH, with PARTIAL on details. |
| 2405 | Table 24 ROM $1F8..$1FF | Summarised at `debug_interrupt.yaml:72-73`. PARTIAL (the instruction words are not listed). |
| 2446 | Table 25 per-cog buffers | Carried as a formula, `debug_interrupt.yaml:75-76`. The formula reproduces the table (cog 0 gives $FFF80). MATCH. |
| 2480-2484 | IJMP0 redirect; any-D CALLD ends the debug ISR; stealth | PARTIAL. The "any D register" rule is NOT-CARRIED. |
| 2489 | BRK D/# | Bit order IN-PLAN §1. Condition rule MATCH (`pasm2/brk.yaml:43`). |
| 2520 | COGBRK D/# | MATCH on the preconditions. PARTIAL on width (%CCCC vs Dest[2:0]). |
| 2527-2593 | GETBRK WCZ / WC / WZ | Carried, `pasm2/getbrk.yaml`. State codes and trap bit list are IN-PLAN §6. |
| 2596-2606 | HUB Configuration (HUBSET modes) | Framing is IN-PLAN §1 and §6 (`operand_modes`). |
| 2609-2741 | Configuring the Clock Generator, tables 26-29, PLL example | Carried, `architecture/clock_system.yaml`. Two contract defects: examples and a recipe settle the PLL while running on XI, and conflicting switch-away recipes sit on one page. |
| 2743-2774 | Write-protect + debug enables | Carried, `architecture/hub.yaml:32-52`. MATCH. The debug-area address defect is IN-PLAN §1. |
| 2776-2847 | Digital filters, table 30 | Carried, `architecture/smart_pins.yaml:215-229`. MATCH, except the unanimity rule (PARTIAL). |
| 2850-2859 | PRNG seeding / distribution | Seeding IN-PLAN §6. Distribution is PARTIAL (`spin2/concepts/random_generation.yaml`). |
| 2860-2865 | Rebooting the Chip | `pasm2/hubset.yaml:103-106`. MATCH. |

## Ledger

| SD lines | Fact (one line) | Contract/Mechanism | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 2037-2054 | 16 events numbered 0..15 with names | Contract | architecture/event_system.yaml:31-47 | MATCH | Row-by-row match, e.g. `{event: 13, name: "streamer read lookup RAM location $1FF"}` |
| 2040 | CT is the low 32 bits of the 64-bit counter | Contract | pasm2/getct.yaml (GETCT), clock_system.yaml:309 | MATCH | |
| 2061 | POLLxxx returns the flag in C/Z and clears it unless it is being set again | Contract | pasm2/pollint.yaml:5-7 (and siblings) | MATCH | "then clears the flag (unless it's being set again by the event sensor)" |
| 2063-2079 | POLLxxx-to-interrupt-source number column | Contract | interrupts.yaml:254-324; event_system.yaml:499-503 | MATCH | |
| 2082 | WAITxxx waits, then clears its flag | Contract | pasm2/waitint.yaml, waitct1.yaml:14 | MATCH | |
| 2084 | SETQ before WAITxxx gives a CT timeout; with WC, C=1 means timeout first | Contract | waitct1.yaml:14; waitint.yaml; event_system.yaml:163-165 | MATCH | All 15 WAIT pages mention SETQ (grep -c SETQ, none 0) |
| 2086 | WAITINT stalls the cog to save power | Contract (power, low) | NOT-CARRIED | NOT-CARRIED | grep "save power\|low.power\|stalls the cog" in waitint/interrupts/event pages: none. waitint.yaml says "the pipeline is stalled". Low consequence. |
| 2102 | No WAITQMT | Contract | event_system.yaml:49-50; pollqmt.yaml:15 | MATCH | |
| 2104 | Jxxx/JNxxx clear the flag whether or not they branch | Contract | 7 pages carry a clearing line (jqmt, jnqmt, jxmt, jnxmt, jxrl, jnxrl, jnfbw). **25 do not**: jint, jnint, jct1-3, jnct1-3, jse1-4, jnse1-4, jpat, jnpat, jfbw, jxfi, jnxfi, jxro, jnxro, jatn, jnatn | NOT-CARRIED (25 pages) | Grep per page for "flag is cleared\|cleared after\|then clear\|clears the". The §6 `event_clearing` table is planned, but its links go to "the 21 pages holding the sentence". These 25 pages do not hold it. |
| 2106-2121 | Jxxx list (16 pairs) | Contract | pasm2/j*.yaml | MATCH | |
| 2124 | Every set-event except INT can be an interrupt source | Contract | interrupts.yaml:49-92 | MATCH | |
| 2129-2131 | INT flag: cleared on cog start; set on INT1/2/3; debug interrupts ignored | Contract | pollint.yaml:9-12; waitint.yaml | MATCH | pasm2/jint.yaml:16-17 has "set when a hardware interrupt condition is pending". "Pending" is not "occurs", and the page omits the debug exclusion. PARTIAL on jint. |
| 2136-2152 | CTn flag: cleared on ADDCTn; set when MSB(CT-CTn)=0 | Contract | pollct1.yaml:17-19; addct1.yaml:12 | MATCH | "MSB of (CT - CT1) is 0" |
| 2157-2162 | PAT flag: four C/Z cases; cleared on SETPAT | Contract | event_system.yaml:189-197; setpat.yaml:12-21 | MATCH | C/Z are inputs. Matches the four rows. |
| 2167-2169 | FBW flag cleared on RDFAST/WRFAST/FBLOCK | Contract | pollfbw.yaml | MATCH | |
| 2174-2190 | XMT/XFI/XRO cleared on XINIT/XZERO/XCONT | Contract | pollxmt/pollxfi/pollxro.yaml | MATCH | The KB's XCONT is right where SD:2286-2287 misspell it "ZCONT". |
| 2195-2211 | XRL/ATN/QMT cleared on cog start | Contract | pollxrl/pollatn/pollqmt.yaml | MATCH | Consolidated cog-start list is IN-PLAN §6 Verify and §11. SD:2211 names "WAITQMT", which contradicts SD:2102. The KB follows :2102. |
| 2200-2203 | ATN set when any cog(s) request attention, without identifying the sender | Contract | pollatn.yaml; jatn.yaml:13-15 | MATCH | concepts/event_interrupt_config.yaml:240 has the code comment "' Check which cog sent ATN" before `POLLATN WC`. The flag carries no sender, so the comment misleads. PARTIAL there. |
| 2217-2228 | ADDCT1 adds S into D and copies the result into a hidden target register; clears the flag | Contract | addct1.yaml:12 | MATCH | "ADDCT1 sets the hidden CT1 event trigger register to the value of Dest + Src. The result is also written to Dest." |
| 2231-2242 | SEn set/clear rules | Contract | setse1.yaml:13-14; pollse1.yaml | MATCH | |
| 2246-2260 | SETSEn D encoding (LUT / lock / pin edge / level) | Contract | event_system.yaml:102-114 | MATCH | Row by row |
| 2264-2270 | INT1>INT2>INT3 priority and preemption | Contract | interrupts.yaml:27-32, :392; event_interrupt_config.yaml:256-258 | MATCH | |
| 2272, 2341-2344 | STALLI holds off branches; ALLOWI is the default on cog start | Contract | stalli.yaml; allowi.yaml; interrupts.yaml:132-158 | MATCH | |
| 2276-2291 | 16 interrupt source codes; 0 is the default on cog start | Contract | interrupts.yaml:49-92, :254-324 | MATCH | |
| 2294-2301 | IJMPx/IRETx addresses; the interrupt stores C/Z and the return address in IRETx | Contract | interrupts.yaml:34-44, :100-129 | MATCH | |
| 2304-2311 | RETIx = CALLD INB,IRETx WCZ: restores C/Z and clears the interrupt-busy flag | Contract | event_interrupt_config.yaml:80 MATCH; interrupts.yaml:225 MATCH for RETI0. **pasm2/reti0..3.yaml:15-16 and resi0..3.yaml:15-16 say `C: No effect`, `Z: No effect`** | MISMATCH | Each page's own description reads "(CALLD $1FF,$1F5 WCZ)". |
| 2311 | Any CALLD with S=IRETx and WCZ ends the interrupt (D can be any register) | Contract | NOT-CARRIED | NOT-CARRIED | grep "any register\|D = <any\|signals the cog": only groups/interrupt_resume.yaml:13, which covers the RESIx aliases alone. pasm2/calld.yaml does not mention ending an interrupt. |
| 2313-2317 | RESIx = CALLD IJMPx,IRETx WCZ; resumes the ISR next time | Contract | event_interrupt_config.yaml:83-87; groups/interrupt_resume.yaml:10-14 | MATCH | |
| 2320-2324 | SETINTx D sets the source 0..15; set IJMPx first | Contract | setint1.yaml:12; interrupts.yaml:160-171; event_interrupt_config.yaml:295 | MATCH | |
| 2327-2331 | TRGINTx forces an interrupt | Contract | trgint1.yaml:12 | IN-PLAN §1 | STALLI conflict, bench arm H |
| 2334-2338 | NIXINTx nixes a triggered interrupt that is waiting to branch; useful only after STALLI or inside a higher ISR | Contract | event_interrupt_config.yaml:74 (first half); nixint1.yaml:12 "Cancel INT1." | PARTIAL | The use-window clause is NOT-CARRIED. grep "only useful\|after STALLI" in nixint*: none. |
| 2349-2354 | Branch-deferral conditions list | Contract | interrupts.yaml:431-438 | MATCH | "AUGS or AUGD pending" matches "executing or waiting" |
| 2357 | Once the conditions clear, a pending interrupt branches; INT1 first | Contract | interrupts.yaml:155-156 | MATCH | |
| 2359 | Branch = inserted 'CALLD IRETx,IJMPx WCZ' with the PC held | Contract | interrupts.yaml:411-415 | MATCH | Quoted verbatim |
| 2361-2367 | Three states. During "waiting for branch" and "executing ISR", events at the same level are ignored (lost, not latched) | Contract | NOT-CARRIED | NOT-CARRIED | Searched "same priority\|intervening\|ignored\|are lost\|not queued\|three states\|busy flag". Closest: event_interrupt_config.yaml:259 "Same level cannot interrupt itself"; event_system.yaml:474 "Events are flags, not queued". Neither says a same-level event during the ISR is dropped. Home: architecture/interrupts.yaml `priority_preemption`. |
| 2372-2390 | INT1/CT1 example | Contract (example) | interrupts.yaml:327-339 | MATCH | |
| 2395 | Debug interrupt: hidden, above all, inaccessible to normal programs | Contract | debug_interrupt.yaml:24; event_interrupt_config.yaml:19-29 | MATCH | |
| 2397 | Enabled per cog via HUBSET; interrupt on each COGINIT; needs BRK conditions or no more interrupts | Contract | debug_interrupt.yaml:26-30 | MATCH | |
| 2399 | Last 16 KB is the buffer area, also mapped at $FC000; write-protectable, then mapped only at $FC000 | Contract | debug_interrupt.yaml:76-78; hub.yaml:39-43 | MATCH | The hub.yaml:236 address defect is IN-PLAN §1. |
| 2401, 2405-2420 | Execute-only ROM $1F8..$1FF and its 8 instructions | Contract (debugger authors) | debug_interrupt.yaml:72-73 | PARTIAL | Summarised ("saves $000..$00F to hub, loads the debugger, JMP #0"). The instruction words and the `%1111_1111_1ccc_c000_0000` pattern are not listed. The address formula is carried. |
| 2423 | During a debug ISR INA/INB become IJMP0/IRET0; IJMP0=$1F8 on COGINIT | Contract | debug_interrupt.yaml:66-69 | MATCH | |
| 2427-2439 | Entry and exit sequence; JMP #$1FD exits | Contract | debug_interrupt.yaml:72-77 | PARTIAL | `JMP #$1FD` is not named as the exit entry. Only "$1FD..$1FF -- restores... then RETI0". grep "1FD": only that line. |
| 2433 | Host link over P63/P62 with a LOCK (hypothetical) | Mechanism/design intent | event_interrupt_config.yaml:297 (LOCK[15]) | PARTIAL | Design intent only. |
| 2454-2477 | Table 25 per-cog save and image addresses | Contract | debug_interrupt.yaml:75-76 | MATCH | ($FF800 + !cog<<7) gives $FFF80 for cog 0 and $FFC00 for cog 7, as the table does. |
| 2480 | IJMP0 can be redirected in a debug ISR, losing the ROM save | Contract | debug_interrupt.yaml:258-260 | MATCH | |
| 2482 | Any CALLD anyreg,INB WCZ ends a debug ISR; RESI0 = CALLD INA,INB WCZ | Contract | groups/interrupt_resume.yaml:13 (RESI0 only) | PARTIAL | The general any-D rule is not carried (same searches as the SD:2311 row). |
| 2484 | Debug ISR runs in cog register space, so the hub FIFO is undisturbed | Contract | debug_interrupt.yaml:368 | MATCH | |
| 2491-2493 | BRK in normal code: 8-bit code; fires regardless of condition; condition gates only the code write | Contract | brk.yaml:12, :43; debug_interrupt.yaml:136-141 | MATCH | |
| 2496-2512 | BRK in ISR: condition word layout | Contract | debug_interrupt.yaml:91-121 MATCH; brk.yaml:12 `_BCDEFGHIJKLM` | IN-PLAN §1 | |
| 2514-2517 | %L must be 0 before exit; L..A cleared on entry | Contract | debug_interrupt.yaml:99-101, :122-124 | MATCH | |
| 2522-2524 | COGBRK: caller must be in its own debug ISR; target must have %I set; D=%CCCC | Contract | cogbrk.yaml:5; debug_interrupt.yaml:157-162 | PARTIAL | Preconditions MATCH. Width: SD gives 4-bit %CCCC, cogbrk.yaml:5 gives "Dest[2:0], per Parallax's PASM2 Manual". Harmless on 8 cogs, but the two sources differ unrecorded. debug_interrupt.yaml:342 "Debug any COG from any other COG" omits the precondition. |
| 2529-2545 | GETBRK WCZ, normal: C/Z and D fields | Contract | getbrk.yaml:12-20 | MATCH / IN-PLAN §6 | Fields MATCH. The %0x/%10/%11 state codes are IN-PLAN §6. D[31:23]=0 is not stated (fold into §6). |
| 2548-2553 | GETBRK WCZ in a debug ISR: C/D[23] COGINIT, D[31:24] BRK code | Contract | getbrk.yaml:22-24 | MATCH | |
| 2559-2584 | GETBRK WC: C = pattern LSB, CALL depth, modes, 16 trap bits (D[3]=CT1 ... D[1]=CT3, reversed) | Contract | getbrk.yaml:26-29 | IN-PLAN §6 | Trap bit list not enumerated. D[25] paraphrased "XBYTE pending on next _RET_/RET" (SD: top of stack = $1FF). |
| 2589-2593 | GETBRK WZ: Z and D pattern | Contract | getbrk.yaml:31-32, :48-52 | MATCH | |
| 2598-2606 | HUBSET: top bits select the circuit (five modes) | Contract | hubset.yaml:20, :24-26 | IN-PLAN §1/§6 | |
| 2613 | RCFAST 20 MHz+ worst-case (for 2 Mbaud boot); RCSLOW ~20 kHz | Contract | clock_system.yaml:77, :168, :180-186 | MATCH | hubset.yaml:52 says `"RCFAST (~20 MHz)"`. PARTIAL there: understates the "at least 20 MHz" guarantee. Fold into the §6 hubset table. |
| 2615 | XI input / XO feedback for 10-20 MHz crystals; internal loading caps | Contract | clock_system.yaml:195-200 | MATCH | |
| 2617 | PLL: /1..64, x1..1024, post /1,2,4..30 | Contract | clock_system.yaml:88-128; hubset.yaml:30-40 | MATCH | |
| 2621 | Clock-mode word layout %0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS | Contract | clock_system.yaml:134 | MATCH | |
| 2632-2643 | %E (needs %CC), %D, %M; VCO 100-200 MHz | Contract | clock_system.yaml:90-104 | MATCH | |
| 2644-2682 | %PPPP table; 350 MHz with VCO/1 | Contract | clock_system.yaml:105-129 | MATCH | |
| 2686-2715 | %CC table (XI/XO status, impedance, caps) | Contract | clock_system.yaml:155-161 | MATCH | hubset.yaml:45-48 is coarser (no XO 600-ohm drive). PARTIAL there. |
| 2719-2724 | %SS table with 10 ms / 5 ms settle | Contract | clock_system.yaml:162-168; hubset.yaml:49-55 | MATCH | |
| 2726 | Switching away from the PLL with PPPP=%1111: go to RC first, **keeping PPPP=%1111 and CC** | Contract | clock_system.yaml:210 MATCH. **clock_system.yaml:142 and :341 recommend `HUBSET #$F0` / `#$F1`** (datasheet), which sets CC=%00 and E=0 | MISMATCH (unrecorded source conflict on one page) | :142 "always start by switching to an internal oscillator using either HUBSET #$F0 (for RCFAST) or HUBSET #$F1". SD: "while maintaining the %PPPP = %1111 and %CC settings". |
| 2730-2739 | PLL example: 148.5 MHz in 4 steps | Contract | clock_system.yaml:144-151; hubset.yaml:89-101 (200 MHz analogue) | MATCH | |
| 2741 | Deglitcher; must select %00 or %01 while the crystal and/or PLL settle | Contract | clock_system.yaml:143 states it. **clock_system.yaml:229-249 (160 MHz and 250 MHz examples) switch to XI (`##%10_10`), then enable the PLL and wait while on XI (`..._1010`).** **hubset.yaml:60-68**: "Configure PLL but stay on current source ... source bits = current" | MISMATCH | Examples and recipe contradict the rule stated on the same page. |
| 2747-2761 | %0010 L/W/D fields | Contract | hub.yaml:39-49 | MATCH | |
| 2763-2772 | Three write-protect/debug examples | Contract | hub.yaml:50-52 | MATCH | |
| 2778-2792 | Four filters; length 2/3/5/8; tap = CT bit 0..31; HUBSET $4000_0000+$80*n | Contract | smart_pins.yaml:215-223 | MATCH | |
| 2780 | Flipflops must be unanimously high or low to change the output | Contract | smart_pins.yaml:216 | PARTIAL | The unanimity rule is omitted. grep "unanim" in deliverables: only community/obex/objects/4883.yaml. |
| 2794-2847 | Table 30 reset defaults | Contract | smart_pins.yaml:224-229 | MATCH | Row by row |
| 2852 | Seed writes {1'b1, D[30:0]} into 1/4 of the 128-bit state | Contract | hubset.yaml:26 | IN-PLAN §6 | `prng_seeding` |
| 2854 | Boot ROM seeds 50 times from P63 ADC noise | Contract (low) | spin2/concepts/random_generation.yaml:6-7 ("seeds that generator with thermal noise from the ADC") | PARTIAL | IN-PLAN §6 seeding. 50x/P63 not stated. |
| 2859 | PRNG iterates every clock; each cog gets a unique scrambled 32 bits; each smart pin 8 bits for dither/noise | Contract (cog), Mechanism (pin) | random_generation.yaml:6-8 | PARTIAL | pasm2/getrnd.yaml:17 says only "Get RND into C/Z... unique per cog". It does not name xoroshiro128** or the per-clock iteration. Folds into §6. |
| 2862-2864 | HUBSET ##$1000_0000 reboots | Contract | hubset.yaml:103-106; spin2/methods/hubset.yaml:37 | MATCH | |

## Findings

Only the MISMATCH and NOT-CARRIED contract rows, most consequential first.

1. **RETI0..3 and RESI0..3 pages say the flags are untouched (MISMATCH).**
   - The source: SD:2294 "store the C/Z flags and return address into the adjacent IRET register", and SD:2306 "RETI1 = CALLD INB,IRET1 WCZ". The return restores C and Z.
   - The KB: `pasm2/reti1.yaml:15-16` says `C: No effect` / `Z: No effect`. The same holds in reti0, reti2, reti3 and resi0..3 (8 pages), and each page's own description reads "(CALLD $1FF,$1F5 WCZ)".
   - The KB's own concept pages contradict them: `architecture/interrupts.yaml:225` "C, Z (restored from IRET0)" and `concepts/event_interrupt_config.yaml:80` "restores C and Z from it".
   - The risk: an agent reading only the instruction page will think its ISR must not touch the flags, or that the main code's flags survive differently.

2. **Clock examples and the switching recipe settle the PLL while running on XI (MISMATCH).**
   - The source: SD:2741 "It is necessary to select mode %00 or %01 while waiting for the crystal and/or PLL to settle into operation, before switching over to either."
   - The examples: `architecture/clock_system.yaml:235-238` (`HUBSET ##%10_10` then `...0111_1111_1010` "PLL on ... source still XI", wait, then `..._1011`), and `:246-249` (same pattern, 250 MHz).
   - The recipe: `pasm2/hubset.yaml:60-68`, "1. Configure PLL but stay on current source", with code `' PLL settings, source bits = current`.
   - The same page states the rule correctly at `clock_system.yaml:143`.

3. **Two contradictory switch-away-from-PLL recipes on one page, with no conflict recorded (MISMATCH).**
   - The source: SD:2726 says to switch to RC first "while maintaining the %PPPP = %1111 and %CC settings".
   - The KB carries this at `clock_system.yaml:210`: "first switch to an RC oscillator (SS=%00 or %01) keeping PPPP=%1111 and CC".
   - The conflict: `clock_system.yaml:142` and `:341` (from the datasheet) recommend "HUBSET #$F0 (for RCFAST) or HUBSET #$F1 (for RCSLOW)". Those immediates set CC=%00 and E=0, so they drop CC.
   - The KB serves both recipes and no `cross_source_conflict` note records the difference, while the page does record one for VCO (:130).

4. **Same-level interrupt events during a pending branch or a running ISR are ignored (NOT-CARRIED).**
   - The source: SD:2361-2367 "Waiting for interrupt event / Waiting for interrupt branch / Executing interrupt service routine. During states 2 and 3, any intervening interrupt events at the same priority level are ignored."
   - Searches: "same priority", "intervening", "ignored", "are lost", "not queued", "three states", "busy flag".
   - Closest KB text: `event_interrupt_config.yaml:259` "Same level cannot interrupt itself", and `event_system.yaml:474` "Events are flags, not queued". Neither says the event is dropped.
   - The risk: a long ISR silently misses events.
   - Home: `architecture/interrupts.yaml` `priority_preemption` (:450-452).

5. **Jxxx/JNxxx clear the event flag whether or not they branch (NOT-CARRIED on 25 of 32 pages).**
   - The source: SD:2104 "Whether or not a branch occurs, the event-occurred flag will be cleared".
   - Missing from: `jint`, `jnint`, `jct1-3`, `jnct1-3`, `jse1-4`, `jnse1-4`, `jpat`, `jnpat`, `jfbw`, `jxfi`, `jnxfi`, `jxro`, `jnxro`, `jatn`, `jnatn`.
   - Searched per page: "flag is cleared", "cleared after", "then clear", "clears the".
   - The planned §6 `event_clearing` table links only "the 21 pages holding the sentence", so these pages stay silent unless the link set is widened.
   - Related: `pasm2/jint.yaml:16-17` says the INT flag "is set when a hardware interrupt condition is pending". The source says "Set whenever interrupt 1, 2, or 3 occurs (debug interrupts are ignored)" (SD:2130).

6. **Any CALLD with S=IRETx and WCZ ends the interrupt, D can be any register (NOT-CARRIED).**
   - The source: SD:2311 "The CALLD with D = <any register>, S = IRETx, and WCZ, signals the cog that the interrupt is complete", and SD:2482 "any D-register variant (CALLD anyreg,INB WCZ)" for the debug ISR.
   - Searches: "any register", "D = <any", "signals the cog", "anyreg", "CALLD INA,INB".
   - Found only `groups/interrupt_resume.yaml:13`, which covers the RESIx aliases alone.
   - Home: `pasm2/calld.yaml`, which never mentions ending an interrupt.

7. **NIXINTx is useful only after STALLI or inside a higher ISR (NOT-CARRIED clause).**
   - The source: SD:2334 "only useful in main code after STALLI executes or in an ISR which needs to stop a lower-level interrupt".
   - The KB: `nixint1.yaml:12` says only "Cancel INT1.", and `event_interrupt_config.yaml:74` gives just the first half.
   - Searches: "only useful", "after STALLI" in nixint*.

8. **Debug-ISR exit entry `JMP #$1FD` is not named (PARTIAL, contract for debugger authors).**
   - The source: SD:2435 "you can do a 'JMP #$1FD' to execute the debug-ISR-exit routine".
   - The KB: `debug_interrupt.yaml:73` gives the range only: "$1FD..$1FF -- restores $000..$00F from hub, then RETI0". grep "1FD" finds only that line.

9. **Filter unanimity rule (PARTIAL).**
   - The source: SD:2780 "must be unanimously high or low to change the filter output".
   - The KB: `smart_pins.yaml:216` omits the rule. grep "unanim" finds it only in an OBEX record.

10. **WAITINT power stall (NOT-CARRIED, low).**
    - The source: SD:2086 "stalls the cog to save power".
    - Not stated on `waitint.yaml`.

Ledger counts (row dispositions):
- MATCH: 54, plus 1 MATCH/IN-PLAN.
- PARTIAL: 9.
- MISMATCH: 3 rows, covering 11 pages.
- NOT-CARRIED: 4 rows, one of them covering 25 pages.
- IN-PLAN: 5.

Several MATCH rows also carry a PARTIAL note on a sibling page (jint, hubset RCFAST and CC, event_interrupt_config ATN comment).

## Closure (task «#453»)

Each row was re-found by content, confirmed at its SD line, and checked against the YAML text as it stands now. Fix lines are in the files as edited by this task. KB paths are relative to `deliverables/ai/P2/`.

### MISMATCH rows

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 2304-2311 RETIx/RESIx flags | 2294, 2304-2311, 2313-2317; RETI0/RESI0 at 2420, 2423, 2482 | CLOSED, fixed | `pasm2/reti0.yaml:6-7,13-24`; `reti1.yaml`, `reti2.yaml`, `reti3.yaml` and `resi0.yaml`..`resi3.yaml` the same lines (encoding c/z, description, flags_affected). C = IRETx[31], Z = IRETx[30] (IRET0 for the two INT0 forms); the interrupt-busy flag cleared by the CALLD with S = IRETx and WCZ. The encoding clocks corrected from '4' to '4 / 13...20' (instruction listing rows 158-165). Nothing added on RESIx flags beyond the CALLD WCZ restore. |
| 2726 switching away from the PLL | 2726; datasheet p.18 and Hardware Manual (System Clock Configuration) give HUBSET #$F0 / #$F1 | CLOSED, conflict recorded, no winner | `architecture/clock_system.yaml:150` (hubset_configuration.cross_source_conflict: both recipes, unnamed; $F0/$F1 write %PPPP = %1111 with %CC = %00 and E = 0; "Not documented: which recipe holds where the two differ"); `:229` (clock_switching.switch_away_from_pll_warning), `:344-348` (anti_patterns.unsafe_switch_away_from_pll.correct) point to it. `pasm2/hubset.yaml:136` (pll_200mhz description) re-read against it: its HUBSET #$F0 starts from RCFAST, and the description now says what $F0 writes and points to the conflict. |
| 2741 PLL settling on RC | 2741, 2730-2739, 2721-2722 (10 ms / 5 ms) | CLOSED, fixed | `architecture/clock_system.yaml:244-269` (basic_crystal_20mhz now waits ~5 ms; pll_160mhz and overclock_250mhz rewritten to the four steps: HUBSET #$F0, enable crystal+PLL with %SS = %00, ~10 ms wait, %SS = %11), `:194` (stabilization_timing.pll_and_crystal_settle_on_rc), `:235-240` (clock_switching.sequence), `:340-343` (new anti_patterns.enable_pll_while_on_xi); `pasm2/hubset.yaml:96-131` (safe_clock_switching: the rule and the SD four-step example, replacing "stay on current source" and the clkfreq-based wait). No example now enables the PLL while %SS names XI or the PLL. |

### NOT CARRIED rows

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 2104 Jxxx clear the flag whether or not they branch | 2104 | CLOSED against existing text | `grep -L -i "whether or"` over the 32 event jump files lists none: all carry it. Nothing added. jint/jnint set condition matches SD:2129-2131. |
| 2311 any CALLD with S = IRETx and WCZ ends the interrupt | 2311, 2482 | CLOSED, fixed | `pasm2/calld.yaml:38-45` (one paragraph: any D with S = IRETx and WCZ clears the interrupt-busy flag; RETIx D = INB, RESIx D = IJMPx; in a debug ISR any CALLD anyreg,INB WCZ ends it, RETI0 = CALLD INB,INB WCZ, RESI0 = CALLD INA,INB WCZ); also `architecture/debug_interrupt.yaml:87` (ending_a_debug_isr). Equivalence checked with pnut-ts: CALLD INB,IRET1 WCZ and RETI1 both assemble to $FB3BFFF5, CALLD INA,INB WCZ and RESI0 to $FB3BFDFF. |
| 2361-2367 three states; same-level events ignored | 2361-2367 | CLOSED, fixed | `architecture/interrupts.yaml:472` (priority_preemption.interrupt_states); also `interrupts.yaml` best_practices keep_isr_short, `pasm2/concepts/event_interrupt_config.yaml:255`. |
| 2086 WAITINT stalls the cog to save power | 2086 | CLOSED, fixed | `pasm2/waitint.yaml:19-20`; `event_interrupt_config.yaml:156`; `clock_system.yaml` power_management.waitint. |

### PARTIAL rows on touched files

| Ledger row | SD lines confirmed | Disposition | Fix (file:line) |
|---|---|---|---|
| 2334-2338 NIXINTx use window | 2334-2338 | CLOSED, fixed | `pasm2/nixint1.yaml:12-17`, `nixint2.yaml:12-16`, `nixint3.yaml:12-17` (each its own level); `event_interrupt_config.yaml:73`; `architecture/interrupts.yaml:202-212`. |
| 2401, 2405-2420 ROM words | 2405-2420 | CLOSED, fixed | `architecture/debug_interrupt.yaml:76-86` (rom_words: the eight words with the address patterns; their 32-bit encodings stated as not documented). |
| 2427-2439 JMP #$1FD exit | 2435 | CLOSED, fixed | `architecture/debug_interrupt.yaml:75`. |
| 2433 host link over P63/P62 | 2433 | CLOSED, not carried: design intent ("somewhat hypothetical") | nothing served. |
| 2480-2484 any-D CALLD ends a debug ISR | 2482 | CLOSED, fixed | `architecture/debug_interrupt.yaml:87`; `pasm2/calld.yaml:38-45`; `pasm2/resi0.yaml` description. |
| 2522-2524 COGBRK width | 2524 | CLOSED, fixed: `pasm2/cogbrk.yaml:5,12-13` now gives the three forms Parallax's documents use, unnamed (%CCCC, D[3:0], D[2:0]; it had only Dest[2:0]); `architecture/debug_interrupt.yaml:186` gives the same three. Preconditions: `debug_interrupt.yaml:357` (cross_cog_debugging) and related_topics now state both. |
| 2780 filter unanimity | 2780, also 203 | CLOSED, fixed | `architecture/smart_pins.yaml:221` (global_digital_filters.unanimity), with where_the_output_goes. The file was re-read whole. |
| 2200-2203 ATN carries no sender | 2200-2203 | CLOSED, fixed | `event_interrupt_config.yaml:236,240` (comment rewritten) and the pattern description. |
| 2613, 2686-2715 hubset RCFAST and CC | 2613, 2686-2715 | CLOSED against «#452» | `pasm2/hubset.yaml:91` and `:83-86` carry them. |
| 2854, 2859 PRNG | 2854, 2859 | CLOSED against «#452» | `pasm2/hubset.yaml:58-59` (prng_seeding). |

### IN-PLAN rows

| Ledger row | Closed against |
|---|---|
| 2327-2331 TRGINTx under STALLI | arm H, task «#465». trgint1..3.yaml unchanged. stalli.yaml carries an uncommitted change made before this task (file time 2026-11-08 07:31); this task did not touch it. |
| 2489, 2496-2512 BRK bit order; 2399 debug-area address | task «#445» |
| 2527-2584 GETBRK codes; 2598-2606 HUBSET modes; 2852 PRNG seeding; 2124-2211 event_clearing table | task «#452» |
| 2359 inserted CALLD | `architecture/event_system.yaml` carries it (the interrupt branch is an inserted CALLD; entry clocks not documented). `interrupts.yaml` and `event_interrupt_config.yaml` entry-overhead fields now say not documented, as event_system.yaml does. |

### Sample MATCH rows re-read

| Ledger row | Result |
|---|---|
| 2794-2847 Table 30 filter defaults | MATCH. `architecture/smart_pins.yaml` reset_defaults: filt0 tap 0, 2 flipflops, 12.5 ns; filt1 tap 5, 3, 600 ns; filt2 tap 19, 5, 16.4 ms; filt3 tap 22, 8, 210 ms. Same as SD:2808-2847. |
| 2276-2291 interrupt source codes | MATCH. `architecture/interrupts.yaml` interrupt_sources and interrupt_sources_detail list 0..15 in SD order; the KB's XCONT is right where SD:2286-2287 write ZCONT. %0000 now reads "<off>, the default on cog start" and %1000 "established by SETPAT", as SD:2276 and 2284 say. |
