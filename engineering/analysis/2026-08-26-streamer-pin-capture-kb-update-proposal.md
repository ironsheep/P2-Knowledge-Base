# KB update proposal — streamer pin capture, and the IN-repurposing fact

**Raised by:** Stephen's research question, 2026-08-26 — *"smart pins running an SPI interface
(4 pins), can I use nearest-neighbour pins to capture their pin state via the streamer, at Nyquist
rates? Do we have supporting or contraindicating test?"*

**This is a proposal. Nothing here is applied.** Per the project rule, large YAML changes get a
file table and a sign-off first.

---

## 1. Consistency verdict — mostly consistent, one load-bearing miss

The answer to Stephen's question rested on four facts. The KB carries two of them well, one
partially, and **one not at all**.

| # | Fact the answer needed | In the KB? |
|---|---|---|
| 1 | The `%AAAA`/`%BBBB` input selector routes a pin's A/B input from a relative neighbour (±1..±3) | ✅ **Yes, and well** — `pasm2/wrpin.yaml` `input_selectors:`, `spin2-builtin-symbols-complete.yaml`, and `smart_pin_patterns.yaml` already *uses* it for SPI (`P_MINUS1_B` routes the clock in) |
| 2 | An unaligned streamer pin base silently selects a **different mode at a different pin group** (EF-065) | ✅ **Yes, in three places** — `streamer/modes-reference.yaml:21`, `streamer/overview.yaml:101`, `streamer/dds-goertzel.yaml:40` |
| 3 | The streamer's capture path reads pins **from `{INB, INA}`**, 1/2/4/8/16/32 wide, with `%w` (D[23]) driving the automatic `WFBYTE/WFWORD/WFLONG` | ⚠️ **Partial** — `streamer/pin-selection.yaml:102` documents `%w` as *"WRFAST enabled"* and names `X_WRITE_ON`, but **never says what is written or where it is read from** |
| 4 | **On a pin in a smart-pin mode, `IN` is the smart pin's event/ready flag — not the pin's logic level.** Only *"in non-smart-pin modes"* does the resultant `A` drive `IN` | ❌ **Absent** |

**Fact 4 is the one that decides the question**, and its absence is not cosmetic: an agent reading
the KB as it stands would conclude the streamer can capture the SPI pins directly, build it, and
capture ready-pulses instead of traffic. The KB contains the *raw material* — `smart_pins.yaml:176`
and `:253` both carry *"The resultant 'A' will drive the IN signal in non-smart-pin modes"* — but
only as an aside inside the input-selector discussion. **Nothing states the contrapositive**, which
is the operative half.

## 2. What is missed

1. **The IN-repurposing fact, stated as a rule with its consequence.** (Fact 4.)
2. **What the streamer capture path actually reads.** (Fact 3's missing half.)
3. **The composed pattern** — "monitor a running smart-pin bus" exists nowhere.
   `smart_pin_patterns.yaml` knows how to *build* SPI with neighbour routing, and has a
   `streamer_smartpin_sync:` block, but nothing about **observing** a bus already running.
4. **Two bench-verified streamer findings are cited nowhere in the KB:** **EF-062** (streamer
   digital pin output through `X_PINS_ON` requires `DIRH`) and **EF-059** (`adc_pin<<17` silently
   changed the streamer *mode* — the same encoding-hazard family as EF-065, proven by a byte-count
   signature). `grep -rl 'EF-062' deliverables/ai/P2/` → 0 files; same for EF-059.
5. **A gap that should be recorded rather than left implicit:** every streamer finding we hold is
   **output or ADC**. *No test has ever exercised digital pin capture into hub RAM.* The encoding
   hazards transfer; the capture path itself is unverified.

## 3. Findability verdict — this is the weakest part, and one entry is actively wrong

`generate-p2kb-index.py` harvests **top-level `aliases:` only.**

- **All seven `architecture/streamer/*.yaml` files carry zero aliases.** None is reachable by name.
- Probed against the published index, every phrasing of Stephen's question fails:

| query | resolves to |
|---|---|
| `capture pin state` · `pin capture` · `streamer capture` · `sample pins` · `trace pins` | **— not found** |
| `input selector` · `nearest neighbor` · `spi capture` | **— not found** |
| **`logic analyzer`** | **`p2kbSpin2Logic`** — the Spin2 **`LOGIC` operator** |

That last row is worse than a miss. **An agent asking "logic analyzer" is routed to a boolean
operator**, gets a confident irrelevant answer, and has no signal that it went wrong. This is the
same class as F-359's fabricated headers: the index answers with the wrong thing rather than
nothing, and confidence is unwarranted either way.

*(For contrast, the constant names work: `P_PLUS1_B` → three files including `smart_pin_patterns`.
The mechanism is findable **if you already know the constant's name** — which is exactly what
someone asking this question does not.)*

---

## 4. The proposal

### A. New block — the IN-repurposing rule  🔴 *highest value*

| | |
|---|---|
| **File** | `deliverables/ai/P2/architecture/smart_pins.yaml` (the `IN` semantics home) |
| **Change** | ADD a top-level `in_signal_semantics:` block |
| **Why** | Fact 4. The KB states only the non-smart-pin half, as an aside |
| **Source** | Silicon Doc `p2-documentation.txt:7833` (*"raises its IN signal to alert the cog(s)"*), `:7615` (*"resultant 'A' will drive the IN signal in non-smart-pin modes"*), `:7835` (RDPIN/AKPIN lowers it) |

Content, in substance: on a pin with `%SSSSS > %00000`, `IN` is a **handshake** raised on a
mode-related event and lowered by `RDPIN`/`RQPIN`/`AKPIN`; it is **not** the pin's logic level.
Only at `%SSSSS = %00000` does the post-selector, post-filter resultant `A` drive `IN`. **Consequence
to state explicitly:** anything that samples `INA`/`INB` — including the streamer's capture path —
sees the flag, not the waveform, on a pin running a smart-pin mode.

### B. Complete the capture-path description

| | |
|---|---|
| **File** | `deliverables/ai/P2/architecture/streamer/pin-selection.yaml` |
| **Change** | EXTEND the `input_modes:` block (`:102`) |
| **Why** | It names `%w` / `X_WRITE_ON` as *"WRFAST enabled"* and stops. A reader cannot tell what is captured or from where |
| **Source** | Silicon Doc `p2-documentation.txt:3955-3962` — *"1/2/4/8/16/32 pins are read from {INB, INA} … WFBYTE/WFWORD/WFLONG operations will be done automatically to record the pin data. In the case of 1/2/4-pin modes, a WFBYTE will be done each time 8 bits of pin data accrue."* |

Add: the **source** (`{INB, INA}`), the **widths** (1/2/4/8/16/32), the **accrual rule**, and a
`see_also` to the new `in_signal_semantics:` block, because the two facts are only dangerous apart.

### C. New pattern — observing a bus that is already running

| | |
|---|---|
| **File** | `deliverables/ai/P2/architecture/streamer/pin-capture.yaml` **(new)** |
| **Change** | CREATE |
| **Why** | The composed answer exists nowhere. `smart_pin_patterns.yaml` builds SPI; nothing monitors it |
| **Sources** | the two above, plus `wrpin.yaml input_selectors`, plus EF-065 / EF-057 |

Must carry, at minimum:
- **why direct capture of the bus pins fails** (A), so the reader is not left to rediscover it;
- **the neighbour-capture composition** — capture pins at `%SSSSS = %00000` with `%AAAA` routing
  from a bus pin at ±1..±3, whose `IN` therefore *does* carry pin state;
- 🔴 **the alignment constraint, restated at the point of use** — for 8-pin-and-wider modes
  `D[19:17]` holds no pin bits, so the base **must be a multiple of 8**; and both composition
  failures from EF-065 (`+` **carries** into the mode field; `|` **silently vanishes**, producing a
  byte-identical word). Neither errors, and the compiler sees neither;
- 🔴 **EF-057** — `-d` puts the highest-priority interrupt inside the streamer's cog by default;
  set `DEBUG_COGS = %0000_0001` or the measurement is confounded;
- **the honest status line:** the encoding hazards are bench-proven; **the digital capture path
  itself is untested here.**

⚠️ **Constraint on the new file:** it must not restate any constant as `NAME: description` — the
fidelity tool reads that shape as a *definition* and the file would become a second definition
home. Express by encoding and point at the symbol file, exactly as
`architecture/pin-drive-configuration.yaml` does.

### D. Cite the two orphaned empirical findings

| File | Change |
|---|---|
| `architecture/streamer/pin-selection.yaml` or `modes-reference.yaml` | ADD a citation to **EF-062** (`X_PINS_ON` output requires `DIRH`) |
| `architecture/streamer/modes-reference.yaml` | ADD **EF-059** beside EF-065 — same encoding-hazard family, independent proof |

### E. Findability — the change with the widest blast radius

| File | Change |
|---|---|
| all 7 × `architecture/streamer/*.yaml` | ADD a top-level `aliases:` block |
| new `pin-capture.yaml` | aliases incl. `logic analyzer`, `capture pin state`, `pin capture`, `streamer capture`, `bus monitor`, `trace pins`, `sample pins`, `sniff spi` |
| `pasm2/wrpin.yaml` | ADD `input selector`, `neighbor pin`, `adjacent pin routing` |
| `architecture/pin-drive-configuration.yaml` | ADD `pin-drive-configuration` (its own key is currently unreachable) |

🔴 **And resolve the `logic analyzer` misroute deliberately.** It currently resolves to the Spin2
`LOGIC` operator. Either that alias moves to the new capture page, or both are listed and the
operator's entry says what it is not. **Do not add the alias and leave the collision unexamined** —
the array form supports multi-target, but a query that returns a boolean operator *and* a capture
page with no disambiguation is not obviously better than the wrong answer alone.

### F. Record the untested-path gap

| File | Change |
|---|---|
| `engineering/ingestion/KNOWLEDGE-GAPS.md` | ADD a `G-NNN` row: no bench test exists for digital pin capture into hub RAM; every streamer EF is output or ADC |
| the hardware-verification opportunity list | ADD the test that would close it |

**The test that would close it**, sketched so it is not re-derived: run a known pattern out of one
smart pin, capture it through a neighbour-routed non-smart pin with `X_..._WFBYTE` + `X_WRITE_ON`,
and compare the hub buffer against the pattern. It is **jumper-only** — no external instrument —
so it is runnable on Stephen's bench rather than catalogue-only. It would also settle the two things
I could not establish from documents: **the sustained sample-rate ceiling** (hub write bandwidth per
NCO rollover against a Nyquist target) and **whether `%FFF` filtering on the capture pin adds
latency or inter-channel skew across the four lines.**

---

## 5. What I am deliberately **not** proposing

- **No change to the `%AAAA`/`%BBBB` selector table.** It is correct, double-sourced (datasheet +
  Hardware Manual, cell-identical), and closed gap G-001 this sprint.
- **No new constant definitions.** Everything needed already exists in
  `spin2-builtin-symbols-complete.yaml`; this proposal adds *mechanism and routing*, not symbols.
- **No claim about achievable sample rate.** I could not establish it from the sources, and a
  plausible number here would be exactly the defect this sprint spent itself removing. It is
  recorded as a gap (F) rather than answered.
- **Nothing applied.** File table above; awaiting sign-off.
