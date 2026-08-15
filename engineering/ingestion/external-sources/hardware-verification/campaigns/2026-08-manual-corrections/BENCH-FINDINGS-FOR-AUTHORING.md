# Bench Findings — Authoring Source

**Campaign:** 2026-08 manual corrections · **Bench leg completed:** 2026-08-14
**Board:** P2 Edge, 200 MHz · **Rig:** single jumper, pin 0 → pin 1 (except where noted)
**Purpose:** the material from which the documentation changes get written.

This is not the findings register (that tracks *what is wrong*, in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`). This document answers a different
question: **what did we learn that a reader needs to know, and where does it belong?**

Each test below gives the question, the rig, the measured results, and — only where it teaches
something — the discovery path. Every test then ends with an explicit split:

| label | meaning |
|-------|---------|
| **CORRECTION** | the doc says something wrong; fix the text |
| **TEACH** | the doc omits something the reader needs; write new content |
| **TRAP** | something that will bite a reader, that we discovered by being bitten |

Internal campaign lore — our probe bugs, our wrong hypotheses — is deliberately excluded unless
it maps to a reader-facing trap. The test of inclusion is: *would this have saved a reader time?*

---

## Evidence grading — read this before authoring anything

We spent this campaign discovering that our own assumptions were the problem. The failure mode we
must not now hand to readers is **writing an inference as if it were a measurement.** Every claim
below carries a grade:

| grade | meaning |
|-------|---------|
| **[M]** | **Measured** on our bench, after the `DEBUG_COGS` fix. Safe to author. |
| **[M-pre]** | Measured, but **before** the `DEBUG_COGS` fix (Test 6), i.e. with the debug interrupt live in the cog. **Trustworthy only if the test used no streamer.** A streamer measurement at this grade needs a confirming run. |
| **[D]** | **Documentary** — from the Silicon Doc, the Spin2 v55 symbol table, or Chip's shipped demo. Not measured by us. Cite it as documentation, not as our result. |
| **[I]** | **Inference** — our reading of a measurement or a source. State the observation, not the mechanism, unless we can support the mechanism. |

**Timeline that decides the grades.** `DEBUG_COGS = %0000_0001` entered `test-f260-goertzel-input`
at BUILD 2. Everything from `test-f260-goertzel` (the 23-round probe) predates it. So:

- **Safe [M]:** the input probe's C5, DC-by-sum-select, INSTRUMENT, SEQ, BISECT and TONE-delta rows.
- **Safe despite [M-pre]:** F-259 and F-263 — neither uses the streamer at all (cog DAC + smart-pin
  ADC; CORDIC + hub). F-263 additionally has seven consistent runs.
- **Needs a confirming run:** anything [M-pre] that *does* use the streamer — `:607`'s byte counts,
  C10's streamer DAC override, and F-256 (XBYTE is a different sequencer, but we have no basis for
  assuming it is immune).

### Known open — do NOT author these yet

1. **`:607` byte counts** — reproduced four times, but all four with the debugger in the streaming
   cog. Re-run staged.
2. **`_RET_ CALL` falls through** — one run, pre-fix. The sprint plan's §3 error clause already
   demands independent confirmation before restructuring XBYTE §15.3. Re-run staged.
3. **Streamer DAC override from a launched cog / `M[3:0]` = cog id** — the mechanism is [D] from
   Chip's `setnib dacmode,cogid,#2`; our supporting measurement (C10) is [M-pre] and used the
   streamer. Note also that our own `SETDACS`-path test of the same idea (C6b) came back negative,
   which we explained as testing the wrong path. That explanation is [I].
4. **`pppp × 4` = base pin** — [D] only. Our block-select sweep was [M-pre] and came back flat, so
   we have *not* independently confirmed it.

---

## Test 1 — Cog-DAC drive gating (F-259)

**Question.** A community reader reported that the Streamer Guide's cog-DAC recipe drives nothing
without `P_OE`. If true, it is the same class as the DeSilva PWM defect that started this sweep:
a shipped example that produces no output.

**Rig.** Jumper pin 0 → pin 1, verified digitally first. Pin 0 configured as a cog DAC with the
`%TT` field swept; pin 1 read with a smart-pin ADC (`P_ADC_1X | P_ADC`, `WXPIN` 12, `RDPIN`).

**Results.**

| `%TT` | reading | |
|-------|---------|---|
| `%00` (`P_TT_00`) | 1,408 | baseline, no drive |
| `%01` (`P_CHANNEL` == `P_OE`) | **6,737** | **drives — this is the guide's recipe** |
| `%10` (`P_BITDAC`) | 1,409 | no drive |
| `%11` | 1,408 | no drive |
| `%01` with `OUT=1` | 6,737 | OUT is irrelevant |
| `P_CHANNEL + P_OE` via `+` | 1,407 | **dead** |

Reproduced three times; a later independent replication returned 6,737 / 1,410 against the
original 6,737 / 1,408.

**What it means.** The guide is **right** and the reader's report is not reproduced. The reader
compared `%01` against `%10`, not "without OE" against "with OE". But the sweep exposed a real
defect he stumbled into: `P_CHANNEL` and `P_OE` are **the same bit** (`P_TT_01`), so composing
them with `+` carries `%01 + %01` into `%10` — `P_BITDAC`, a different mode that does not drive.

**Class sweep.** 281 config lines across the docs use `|`; exactly **2** use `+`, both in the
Streamer Guide (`streamer-body.md:1238`, `:1306`). Both compute correctly *today* because their
fields happen to be disjoint. It is a latent trap, not a live bug.

### Authoring

- **CORRECTION** — change those two `+` to `|`.
- **TEACH** — state the house rule once, where readers compose pin modes: *pin-mode constants are
  bit fields; combine them with `|`, never `+`. Names from the same "pick one" group share bits,
  so `+` silently carries into a neighbouring mode.*
- **TEACH** — say plainly that `P_OE`, `P_CHANNEL` and `P_TT_01` are **the same bit** with three
  names chosen for three contexts. A reader who sees all three in the symbol list assumes three
  features.
- **TRAP** — F-245's remedy ("add `P_OE`") must **not** be applied to cog-DAC configuration. Same
  bit, different meaning, and adding it to a level-driven DAC breaks it (see Test 6).

---

## Test 2 — CORDIC pipeline depth (F-263)

**Question.** A community report said only ~2 CORDIC results are usable in flight, contradicting
Chip's stated model of a 6–7 deep pipeline.

**Rig.** No pins. Four arms issuing `QMUL` and retrieving with `GETQX` at varying fill depths,
each arm differing only in where hub access sits. **Control first:** a queue-one-then-retrieve
sequence stalled 58 clocks, which is exactly the documented `GETQX` maximum (`2...58`) — proving
the rig can see the failure mode before any arm was trusted.

**Results.** Seven runs, fully consistent:

| arm | shape | first failure |
|-----|-------|---------------|
| B | P2AN002 shape — `RDLONG` inside the fill loop | FILL=2 |
| C | register fill, `WRLONG` inside the drain loop | FILL=3 |
| **D** | register-only fill **and** drain, hub I/O outside | **clean through FILL=7** |
| A | Assembly ch.5 shape | 15 of 16 results wrong |

**What it means. [M-pre, streamer-free]** Deep pipelining works — ARM D returned correct results
through FILL=7, which is inconsistent with a 2-deep result buffer. So the community report's
*conclusion* about buffer depth is not supported. **[I]** Our explanation — that the fill/drain
loop cannot keep up — is a reading of where results are lost, not something we measured directly;
state it as "results are lost from whichever phase contains the hub access", which is what the
data shows.

### Authoring

- **TEACH [M-pre, streamer-free, 7 runs]** — what we actually tested: a `RDLONG` inside the fill
  loop and a `WRLONG` inside the drain loop each cost results from that phase onward, while a
  register-only fill *and* drain stayed clean through FILL=7. The safe way to state it is as the
  tested shape: **keep hub access out of both CORDIC loops and batch it outside.** We did not test
  every hub operation or every cadence, so avoid writing an absolute law about "any hub access" or
  prescribing an exact 8-clock discipline we did not measure. **[I]** on the cause: "the loop
  cannot keep up" is our reading; the measurement shows *where* results are lost, not *why*.
- **CORRECTION** — two of our own shipped documents violate it:
  `P2AN002/examples-library/cordic-pipeline-throughput.spin2` (`rdlong` in fill, `wrlong` in
  steady state) and Assembly ch.5 `chapter-05-hardware.md:~100-126` (two `rdlong`s plus
  `CALL`/`RET` per issue).
- **TEACH** — worth showing *why* the naive version fails, because the failure is silent: results
  are simply wrong, not missing. A reader gets numbers either way.
- **EF-ledger candidate** — our board, our probe, live control.

---

## Test 3 — ADC-capture mode corruption (`:607`, F-260 sibling)

**Question.** `streamer-body.md:607` applies the `adc_pin<<17` idiom to
`X_1ADC8_0P_1DAC8_WFBYTE`. Does that field even exist in that mode?

**Rig.** A hub buffer pre-filled with a sentinel; the guide's line run verbatim at three pin
values; the highest modified byte read back. **The measurement needs nothing analog to work** —
the three candidate modes write 1, 2 and 4 bytes per NCO rollover, so the byte count reads out
which mode the silicon actually ran.

**Results.** Reproduced four times, exactly as predicted:

| `adc_pin` | command | bytes written | mode actually run |
|-----------|---------|---------------|-------------------|
| 0 | `$F082_0400` | 1,024 | correct — 1-ADC8 → WFBYTE |
| 1 | `$F084_0400` | **2,048** | **2-ADC8 → WFWORD** |
| 2 | `$F086_0400` | **4,096** | **4-ADC8 → WFLONG** |
| corrected form | | 1,024 | correct |

**What it means.** The mode's template is `%1111_DDDD_W000_0010` — `D[22:20]` are fixed zeros,
**there is no pin field**, and the ADC channel is selected by `S[1:0]`. So `adc_pin<<17` lands
inside `D[19:16]` and the `add` carries, silently selecting a different streamer mode. The line is
correct **only** for `adc_pin = 0`, and it never selects the channel at all.

### Authoring

- **CORRECTION** — the pin does not belong in `D` for this mode. The channel goes in `S[1:0]`.
- **CORRECTION** — the example omits `SETSCP`, which the Silicon Doc requires to route pins into
  the four SCOPE channels, and it uses `P_ADC_100X` whose smart-pin mode field is `%00000` where
  this mode needs an **enabled** `P_ADC` smart pin.
- **TEACH** — the general lesson, which is worth more than the fix: **streamer mode fields are
  positional and vary by mode.** A field that exists in one mode is fixed or absent in another,
  and composing with `+` against a constant that already occupies those bits will change the mode
  rather than raise an error. Show readers how to check a mode's template before composing.
- **TRAP** — this defect is invisible in testing. The capture "works", the buffer fills, and the
  data is simply the wrong shape.

---

## Test 4 — `_RET_ CALL` inside XBYTE (F-256) · **confirming run pending**

**Question.** `xbyte-body.md:879` says *"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely
on this,"* and the idiom is used at `:416`, `:793`, `:1391`, `:1400`. It assembles clean — so the
objection "you cannot combine a CALL with ret" is wrong as stated — but does it *work*?

**Rig.** A differential test, not an absolute one. Two bytecode handlers doing identical work,
differing only in where the return lives:

- `$01` — `_ret_ call #helper` (return **on** the call line)
- `$04` — `call #helper` / `ret` (return **after** it) ← the reference

Handlers and helper append tokens to a **trail**, so execution *order* is readable, not just a
count. The reference arm runs **first**; if it cannot dispatch, the probe reports the idiom as
untested rather than disproven. A third handler deliberately leaves XBYTE as the control that must
fail.

**Results.**

```
reference ($04):  h_plain → h_callret → helper → h_plain → h_halt        (5 steps, correct)
under test ($01): h_plain → h_retcall → helper → h_callret → helper →
                  h_plain → h_halt                                        (7 steps)
```

`$04` is **not in that bytecode stream.** `h_callret` ran because control fell into it. The helper
reported the pushed return address as `$8000_001A`, and the map shows `H_CALLRET` at cog `$01A` —
the instruction immediately following the `_ret_ call`. The reference arm pushed `$8000_001F`, its
own `ret`. **Both forms pushed "next instruction."**

The compiler is not at fault: `_ret_ call #tgt` emits `$0DB00008` with `EEEE=%0000` (the `_RET_`
condition genuinely present), versus `$FDB00004` / `EEEE=%1111` for a plain call.

**What it means.** `_RET_ CALL` does **not** return to XBYTE. It behaves as a plain `CALL`, and
when the callee returns, execution falls through into whatever follows — in our case an entire
adjacent handler ran, and dispatch only resumed by accident when *that* handler's `ret` popped the
`$1FF`. The community objection was wrong in form and **right in substance**.

> **Status:** one clean run, and it was taken **before** we found the `DEBUG_COGS` confound (Test
> 6). The sprint plan's §3 error clause requires confirming a "the idiom is broken" result by an
> independent path before restructuring a chapter. A re-run with `DEBUG_COGS = %0000_0001` is
> staged. **Do not author §15.3 until it returns.**

### Authoring (pending confirmation)

- **CORRECTION** — the `:879` claim, and every use of the idiom.
- **TEACH** — an instruction cannot both push-and-jump and return; the `_RET_` is silently
  ineffective on `CALL`. This is worth stating as a rule, because it *assembles*.
- **TRAP** — the failure is silent and looks like corruption elsewhere: the next handler in cog
  memory executes spuriously. A reader would hunt this in their VM logic for days.

### Separate finding from the same probe

Getting the rig working surfaced something unrelated and broadly useful: **inside a Spin2 object,
`##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address.** Measured:
`@disp` = `$1AF9` from Spin2 versus `##disp` = `$0651` from PASM, differing by 5,288 bytes; the
`##` form read interpreter memory and returned garbage. In a **standalone PASM** file the
precondition holds and `##hubsym` is correct.

- **TEACH / TRAP** — this bites anyone who copies a PASM fragment out of a guide into a Spin2
  object, which is how most P2 code is written. Pass hub addresses in from Spin2 with `@`, or use
  PTRA. Our guides present standalone-PASM fragments without saying so.

---

## Test 5 — DDS/Goertzel: does the mode work? (F-260)

**Question.** The reporter built §17.1's command exactly as printed; `WAITXFI` completed on
schedule but nothing accumulated. Is the mode broken, or the documentation?

**Rig (final).** Independent tone: a smart-pin NCO (`P_NCO_FREQ | P_OE`) on pin 0 producing a real
1 MHz square wave from cog 0 — **sharing no NCO with the detector**, which the earlier
shared-NCO design made impossible. Detector: DDS/Goertzel in a launched cog reading pin 1 through
the jumper. **Every row measures its own ADC bitstream density before its Goertzel run**, so no row
can misreport its own input.

**Results.**

| arm | ADC density | Δcos | Δsin | magnitude |
|-----|-------------|------|------|-----------|
| **on-target, 1 MHz detector** | 1020/2000 | 1,051,655 | −124,573 | **1,059,000** |
| detuned, 2 MHz detector | 1021/2000 | −1,865 | 1,775 | 2,575 |
| detuned, 500 kHz detector | 1020/2000 | 207 | −198 | 286 |
| no tone, pin driven | 349/2000 | −409 | 134 | 430 |

Densities identical across the three tone rows — the only variable is the detector frequency.
**Selectivity 411:1 against the 2× detune, 3,700:1 against the 0.5× detune, 2,460:1 null.**

**The mode works.** It always worked.

### Why 20+ probe rounds read flat — stated as what we measured, not as a mechanism

**[M] What we observed, with our discrete `XINIT` → `WAITXFI` → `GETXACC` pattern:**

- A **fresh cog's first read equalled the previous cog's last read** — five times running, across
  `COGINIT`.
- **Two identical commands returned exactly twice one command's total.**
- **Absolute reads did not track the input at all**; the difference across one command did, with
  the selectivity in the table above.

**[M] The practical rule that follows for that pattern:** read before the command, read after, and
take the difference. An absolute `GETXACC` value in this pattern is not a per-command measurement.

**[I] — and a caution we must not skip.** It is tempting to conclude "the Goertzel accumulators are
never zeroed." **That over-reaches, and Chip's shipped demo is evidence against it.** His loop is
`xcont` / `getxacc` — one read per command — and he plots the result as a live position. If the
accumulators never reset, his readings would ramp without bound; they do not. So the honest
position is:

> With a discrete `XINIT` + `WAITXFI` + `GETXACC` sequence we measured running-total behaviour.
> With Chip's continuous `XCONT` loop, per-command reads evidently work. **We have not established
> which part of the difference — `XINIT` vs `XCONT`, the wait, or the cog lifecycle — is
> responsible.**

**Author the protocol, not the mechanism.** Tell the reader to take the difference across a
command (or to follow the `XCONT`-loop pattern with an initial calibration, as the shipped demo
does). Do **not** tell them the accumulators are never cleared — we have not shown that, and it
would mislead anyone using the `XCONT` pattern.

**[I] on Chip's calibration:** we previously described his `xcal`/`ycal` as removing an analog
offset, then as removing an inherited baseline. Both were guesses. What is safe to say is that his
demo **establishes a baseline on the first pass and subtracts it from every later reading**, and
that a reader measuring absolute accumulator values without such a baseline will be misled.

### Field semantics — mostly [D], with the grades marked

| field | meaning |
|-------|---------|
| `D[27:24]` `DDDD` | DAC channel routing (`X_DACS_*`) |
| `D[23]` | SINC1 / SINC2 select — **not** `X_PINS_ON` |
| `D[22:19]` `pppp` | ADC input **block**: `pppp × 4` is the **base pin** of four |
| `D[18:16]` | `%111`, required |
| `D[15:0]` | cycles (NCO rollovers) |
| `S[19:16]` | which of the four pins are **inverted** |
| `S[15:12]` | which of the four pins are **summed** — mandatory; `0` sums nothing |
| `S[11:0]` | loop size + LUT window |

The table above is **[D]** — the Spin2 v55 symbol table, the Silicon Doc, and the comments in
Chip's shipped demo. Of it we have independently confirmed only **`S[15:12]` sum-select** **[M]**:
in the DC-by-sum-select test, `base+1` (our ADC pin) was the only selector position that responded,
and the empty selector returned exactly zero. **`pppp × 4` = base pin remains [D]** — our own block
sweep was [M-pre] and flat.

Plus: the NCO scale is **2³¹**, not 2³² **[D]**; DAC output **inverts each LUT byte's MSB** so
signed table values drive unsigned DACs **[D]**, which we met the hard way when `$FF` and `$00`
both landed one LSB apart at mid-scale **[M-pre]**; and in `DAC_MODE` with `TT=%01`, `M[3:0]`
selects which **cog's** DAC channels drive the pin **[D]**, from Chip's `setnib dacmode,cogid,#2`,
while the pin's low two bits pick the channel **[D]**. Our supporting measurement that the
streamer's DAC override works from a launched cog is **[M-pre]** and used the streamer — it needs
the confirming run before it is authored.

### Authoring

- **CORRECTION** — `:1324`'s `dds_s` is undeclared, and S is **mandatory**: `S[15:12]` selects
  which ADC pins are summed, and `S = 0` sums nothing. This alone explains the reporter's symptom.
- **CORRECTION** — `:990`'s `adc_pin<<17` is correct **only** when `adc_pin` is a multiple of 4,
  because `(adc_pin>>2)<<19 == adc_pin<<17` exactly then. The field names a **block**.
- **TEACH — the highest-value item in this document.** The read-before/read-after protocol. Without
  it the mode appears completely dead, and a reader has no way to discover why: the accumulator
  returns a large, stable, plausible-looking number.
- **TEACH** — the four-pin block model: you select a block of four with `pppp`, then choose which
  of those four to sum and which to invert in S. It is not "pick a pin."
- **TEACH** — the ADC pin is **raw**: `P_ADC_x` with smart-pin mode `%00000` and **no DIR**
  (resolves F-265; the Silicon Doc's STREAMER intro says "smart pins configured as ADC's", which
  is loose — the DDS/Goertzel section is authoritative).
- **TEACH** — the MSB inversion on DAC output. Choosing `$FF` and `$00` as "extremes" gives two
  values one LSB apart at mid-scale. The rail values are `$7F` and `$80`.
- **TRAP** — `P_ADC_100X` saturates on a directly-coupled signal. Chip's demo uses it because his
  board couples capacitively through a touch pad; ported to a wire it pins and reads a constant.
  Gain choice is a property of the *coupling*, not of the mode.

---

## Test 6 — The debugger is inside your streamer's cog (F-266)

**Question.** Not one we set out to ask. Our probe crashed into a debugger memory dump, and its
Goertzel accumulators read 1,000,000–7,000,000 of nonsense.

**What we found.** `p2kbArchDebugInterrupt` already records it, under `limitations`:

> **`streamer_interaction`:** *"Debug can disrupt streamer operations."*
> **workaround:** *"Disable debug when using streamer."*

And `DEBUG_COGS` **defaults to `%11111111`** — every cog has debug capability at runtime. The
`CogN INIT …` lines in every log were the debugger announcing cog starts, i.e. direct evidence it
was live inside the launched cogs.

**Measured cost.** Setting `DEBUG_COGS = %0000_0001` (report from cog 0 only) stopped the crash,
made the launched cogs' `INIT` lines disappear, and **collapsed the accumulators from ~1,000,000–
7,000,000 to their true values in the hundreds.** Every streamer measurement taken before that fix
was confounded.

### Authoring

- **TEACH / TRAP — high value, affects every streamer reader.** Debugging streamer code with `-d`
  is the normal way to debug, and it puts the P2's **highest-priority interrupt inside the cog
  running your streamer**, by default. Nothing in the guide warns anyone. The fix is one CON line:
  `DEBUG_COGS = %0000_0001` — restrict debug capability to the cog that actually reports.
- **CORRECTION (KB)** — surface the existing `p2kbArchDebugInterrupt` limitation where a streamer
  author will meet it, rather than only in the debug-interrupt page.
- **TEACH** — the general form: any hardware sequencer measured under the debugger may be
  perturbed by it. Restrict `DEBUG_COGS` to the reporting cog when measuring.

---

## Test 7 — `%TT` is four different fields (F-264)

**Question.** Arose from Test 1 and Test 5. What does `P_OE` / `P_CHANNEL` / `P_TT_01` actually do?

**What the Silicon Doc says** (`part4-locks.txt:118-139`, `p2-documentation.txt:7646-7660`) —
`%TT` has **four context-dependent meaning-sets**, keyed on whether the smart pin is on and
whether `DAC_MODE` (`M[12:10] = %101`) is active. For **smart pin off**:

| `%TT` | non-`DAC_MODE` | **`DAC_MODE`** |
|-------|----------------|----------------|
| `%00` | OUT drives output | **OUT enables ADC, `M[7:0]` sets DAC level** |
| `%01` | OUT drives output | **OUT enables ADC, `M[3:0]` selects cog DAC channel** |
| `%10` | OTHER drives output | OUT drives BIT_DAC |
| `%11` | OTHER drives output | OTHER drives BIT_DAC |

**Bench confirmation.** A `P_DAC_124R_3V` pin driven from its level field read a spread of
**1,305** of 2,000 samples; **adding `P_CHANNEL` dropped it to 25** — because `TT=%01` switches
the DAC's source away from the level field to a cog channel.

**Where our KB stands.** `architecture/smart_pins.yaml:249-253` carries the full table correctly.
`language/spin2/methods/wrpin.yaml`'s `tt_field` gives **one** context-free effect per value — the
smart-pin-on, non-DAC meaning — presented as *the* meaning, with only a `see_also` pointing at the
truth.

### Authoring

- **CORRECTION (KB)** — `wrpin.yaml`'s `tt_field` must state that `%TT` is context-dependent and
  name the four contexts. Keep the full table in `architecture/smart_pins.yaml`; `wrpin.yaml` needs
  enough that a reader cannot conclude the wrong thing without following the pointer.
- **CORRECTION (KB)** — `p_oe_required_for: "All output modes (… DAC …)"` is wrong for the
  non-smart-pin DAC. Qualify it to smart-pin output modes.
- **TRAP** — this is the highest-severity class we carry: **guidance that, applied in a legitimate
  context, breaks working code.** Adding `P_OE` to a level-driven DAC kills it, and F-245's remedy
  says to add it.

---

## Cross-cutting material

Worth writing once and referencing, rather than repeating per manual:

1. **Pin-mode constants are bit fields.** Combine with `|`. Names from the same "pick one" group
   share bits; `+` carries silently into a neighbouring mode. (Tests 1, 3)
2. **Streamer mode fields are positional and vary by mode.** Check the mode's template before
   composing; a field present in one mode is fixed or absent in another. (Tests 3, 5)
3. **Restrict `DEBUG_COGS` when measuring hardware sequencers.** (Test 6)
4. **`##hubsymbol` in a Spin2 object's DAT resolves against `$400`, not the object.** Pass
   addresses in from Spin2 with `@`. (Test 4)
5. **Establish a control that can fail before trusting a measurement.** Every conclusive test here
   has one — the 58-clock CORDIC stall, the ADC density beside each Goertzel row, the `WAITXFI`
   duration proving the detector frequency changed. This is worth teaching in its own right in any
   chapter that asks a reader to measure something.

---

## Evidence

| test | probe | logs |
|------|-------|------|
| 1, 3, 5 | `tests/test-f260-goertzel.spin2`, `tests/test-f260-goertzel-input.spin2` | `tests/logs/` |
| 2 | `tests/test-f263-cordic-pipeline-depth.spin2` | 7 runs |
| 4 | `tests/test-f256-retcall-xbyte.spin2` | confirming run staged |
| reference | `example/Goertzel_DEBUG_Demo.spin2` (Chip's shipped demo) | — |

Findings register: `engineering/operations/P2KB-CORRECTION-FINDINGS.md` F-253…F-266.
Sprint plan: `engineering/planning/MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP-SPRINT-PLAN.md`.
