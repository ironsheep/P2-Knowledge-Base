# What the unpublished YAML delta does to an agent's ability to generate code

**Question asked:** of the content an agent actually receives, do the changes since
the last published set strengthen, weaken, or merely re-accurate the knowledge base
for code generation?

**Answer: strengthened, decisively, and the strengthening is mostly correctness
rather than volume.** The set removed a body of content that would have produced
code that assembles and runs and is wrong. Two new navigational defects were
introduced; both are locators, neither touches a fact.

---

## Scope, and a correction to the framing

There are no uncommitted YAML files — `git status --porcelain` is empty at
`a7fd84e3`. What is outstanding is **committed but unpublished**: 130 commits
since the released tag `v1.17.0`, 97 of them unpushed, and push is publish.

**96 content YAMLs, +6,703 / −3,480 lines.** `v1.17.0..HEAD` and
`origin/main..HEAD` select the identical 96 files (the 33 pushed-after-tag commits
touched no YAML), so the baseline choice is not a judgement call.

Everything below was measured first-hand against both trees. The baseline
measurements were taken in a real `git worktree` checkout of `v1.17.0` with today's
instruments copied in — a flat copy would have broken the tools' path-derived repo
root and produced a false green.

---

## The measured net effect

| Instrument (today's, run over both trees) | v1.17.0 | HEAD | direction |
|---|---|---|---|
| Uncited quantitative blocks, Tier 1 (blocking) | **128** | **0** | ▲ |
| Tier 2 advisory (wholly-uncited files) | 66 | 27 | ▲ |
| Constant-fidelity Tier 1 (mechanical) | **50** | **0** | ▲ |
| Constant-fidelity Tier 2 `CONTRADICT` | 23 | 0 | ▲ |
| Files with duplicate YAML keys | 3 | 0 | ▲ |
| PASM2 encodings present but **fabricated** | 41 | 0 | ▲ |
| Cross-reference sites | 1,319 | 1,423 | ▲ |
| …of which unresolved | 21 | 19 | ▲ (rate 1.59% → 1.34%) |
| Files with top-level `aliases:` (findability) | 71 (6.3%) | 84 (7.4%) | ▲ |
| Alias keys | 508 | 755 | ▲ |
| PASM2 mnemonic lines in examples | 62 | 227 | ▲ |
| Spin2 method-call lines in examples | 27 | 48 | ▲ |

Volume of executable example code went **up** by roughly 3.5×. This is not a set
that traded content for provenance.

---

## The four findings that decide the answer

Each of these is content an agent *received* from the published set and would have
acted on.

### 1. The interrupt vector map was inverted — INT1 and INT3 swapped

Published `architecture/interrupts.yaml` at `v1.17.0`:

    IJMP1 = $1F0    IJMP2 = $1F2    IJMP3 = $1F4
    IRET1 = $1F1    IRET2 = $1F3    IRET3 = $1F5

The Silicon Doc, stating it twice (`silicon-doc-text.txt:446-451` and `:2296-2301`):

    $1F0  IJMP3   interrupt call   address for INT3
    $1F1  IRET3   interrupt return address for INT3
    $1F4  IJMP1   interrupt call   address for INT1
    $1F5  IRET1   interrupt return address for INT1

An agent writing an INT1 handler from the published set installs the vector into
**INT3's register**. It compiles. It runs. The wrong interrupt fires, or none does.
Fixed in `9a1f14a3`.

### 2. Forty-one fabricated instruction encodings

44 distinct `EEEE …` bit patterns were removed from six *architecture concept*
files (`interrupts`, `event_system`, `locks`, `debug_interrupt`, `cog_attention`,
`lookup_ram`). Checked verbatim against the Silicon Doc PASM2 encoding table:

- **3 were real** — and all 3 are still carried in the KB.
- **41 appear nowhere in the Silicon Doc.** They were invented.

They were not harmless duplicates; they *contradicted* the correct per-instruction
files:

| Instruction | Published concept file | Silicon Doc + `language/pasm2/` |
|---|---|---|
| LOCKNEW | `EEEE 1101011 00L DDDDDDDDD 0000LLLLL` | `EEEE 1101011 C00 DDDDDDDDD 000000100` |
| LOCKRET | `EEEE 1101011 00L DDDDDDDDD 0001LLLLL` | `EEEE 1101011 00L DDDDDDDDD 000000101` |
| SETINT1 | `EEEE 1101011 00L DDDDDDDDD 001000SSS` | `EEEE 1101011 00L DDDDDDDDD 000100101` |
| RDLUT   | `EEEE 1010100 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` |

RDLUT is the sharpest: a **single-bit** difference, which hand-encodes to a
different instruction.

Which of the two an agent got depended entirely on whether it reached the concept
file or the instruction file first. That fork is now closed.

Counterpart check on the 42 encodings **added**: 38 appear verbatim in the Silicon
Doc; the remaining 4 are the RETI0–RETI3 aliases, correctly expanded from the
documented alias definitions at `silicon-doc-text.txt:5483-5486`
(`RETI1 = CALLD INB,$1F5 WCZ` → `EEEE 1011001 110 111111111 111110101`) and
byte-identical to the per-instruction files. No new fabrication entered.

### 3. A duplicate key was silently deleting content the file appeared to carry

This is the clearest illustration of *"the content the agent actually gets."*
`language/pasm2/drvl.yaml` at `v1.17.0` had two `timing:` keys. Parsed:

```yaml
# what an agent received from drvl.yaml at v1.17.0
timing:
  cycles: 2
  type: fixed
```

The `pin_output_latency` block was in the file's bytes and **discarded by the YAML
parser** — the later key won. Its sibling `drvh.yaml` had no duplicate and did
deliver it, so the two halves of one instruction pair disagreed about whether pin
latency exists. At HEAD:

```yaml
timing:
  cycles: 2
  pin_output_latency: "…3 system-clock cycles later… 2 + 3 = 5 clocks to pin change"
  pin_output_latency_source: "…silicon-doc-text.txt:1987"
```

Nothing lost, latency gained. Two more files (`lookup_ram.yaml`,
`edge-breadboard-carrier.yaml`) had the same defect; the duplicate-key gate now
reads 0 across 1,132 files.

### 4. Code the published set taught that does not work

Three examples, all removed or corrected:

- **The pull-up idiom.** Published `basic-io.yaml` (both PASM2 and Spin2) taught
  `PINSTART(16, P_HIGH_15K, 0, 0)` followed by `PINFLOAT(16)` as "input with
  pull-up," and named `P_HIGH_*`/`P_LOW_*` as pull-up/pull-down modes. `PINFLOAT`
  drops DIR, which **deactivates the drive** — the P2 has no bias-resistor network
  at all, only per-side drive strength. The replacement is the hardware-verified
  form (`wrpin` + `pinhigh`, DIR high, EF-063/EF-064).
- **The streamer composition trap.** Published `pin-selection.yaml` printed
  `X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + count` as *the example a reader
  copies* — an 8-pin mode at a base that is not a multiple of 8, composed with `+`.
  Assembled with pnut-ts, that yields `$A0B6_FFFF`, not `$A0AE_FFFF`: the carry
  changes D[19:16] to a **different streamer mode** at a **different pin group**,
  with no diagnostic. The file now carries the alignment rule, the `|` composition
  rule, and both failure modes. It also replaced a dense sub-pin slot table that no
  source states and the bench contradicts.
- **WAITMS / WAITUS bounds.** Published range was "1–4,294,967 ms" (~71 minutes).
  The source bounds the wait in **clocks**, at `$8000_0000` — under 11 seconds at
  200 MHz. Wrong by ~400×, and the kind of wrong that surfaces at runtime. Now
  carries the ceiling formula.

Removed `WRPIN` drive encoding (`%00 = 1.5mA … %11 = 30/75/150mA`) was wrong in
both width and units — the real field is two independent 3-bit selectors over a
resistance/current ladder. It is replaced by a new single definition home,
`architecture/pin-drive-configuration.yaml` (+277 lines), carrying the eight rungs,
their `%HHH`/`%LLL` encodings, the `P_*` constant names, the DIR/OUT rule, working
idioms, and an explicit `not_documented_here` block.

---

## What an agent gained

- **116 smart-pin `P_*` constants** are now defined with value, bit pattern and
  hardware relationship, and — because the index harvests only top-level
  `aliases:` — are now **reachable by name** for the first time. Previously not one
  was findable through the published index.
- **Register addresses** for `DIRA/DIRB/OUTA/OUTB/INA/INB` (`$1FA`–`$1FF`), the
  bit-to-pin mapping, and the trap that `$1FE`/`$1FF` double as the debug interrupt
  call/return addresses. None of this was in the published set.
- **Honest self-description.** `spin2-builtin-symbols-complete.yaml` claimed
  `total_symbols: 1224` while holding 136 records — an agent had no way to know the
  file was 11% of what it advertised. It now states 136, explains the 1224, and
  names what is missing.
- **Boot-pin directions** (P58 = MISO/input, P59 = MOSI/output, and the P60/P61
  role swap between flash and SD), which decide whether generated boot code works.
- Pin-map content in the hardware tree **grew** (e.g. `edge-32mb-module`: 45 pin
  lines removed, 64 added) even though those files are net-negative in line count —
  the deletions were prose and uncited electricals, not pin assignments.

---

## What was lost, and whether it matters

Deliberate non-restorations, all recorded rather than silent:

- **13 blocks disproven, not merely unverified** — not restored, correctly.
- **`io_pin_timing` best-practices block** — authored here with no upstream home.
  Held as **F-352** rather than given manufactured provenance. This is a genuine,
  small loss and the register says so.
- **Click-adapter block** — ruled actionable but no ingested source states it;
  filed as a gap naming what would settle it.
- **Electrical-interfacing figures** — `VIL`/`VIH`/`VOL`/`VOH`, Schmitt thresholds,
  propagation/rise/fall per drive setting, trace-delay and temperature
  compensation. Uncited; several provably wrong (a per-pin current figure five
  times the absolute maximum). Losing them costs *hardware-design* reasoning, not
  code generation.
- **Protocol timing examples** (SPI 50 MHz, I²C 400 kHz, SD 25/50 MHz) — generic
  protocol facts, not P2 facts, and stated as "reliable/possible."
- **Slew-rate control** — never existed. `slew` returns zero hits across every
  ingested Parallax source. Its removal is a fabrication deleted, not content lost.

Where a file stopped carrying something, it now says so and says where the content
lives instead. That navigational honesty is itself a codegen asset: it stops an
agent concluding that absence means the feature does not exist.

---

## Two defects this delta introduced — both fixed in this pass

Both are locators. Neither changes a stated fact. Both were repaired on 2026-09-05
rather than deferred; the counts in the table above are pre-fix.

1. **`architecture/interrupts.yaml:13`** — header comment cites
   `language/pasm2/reti0..3.yaml`, which is a shorthand, not a path. The four real
   files (`reti0.yaml` … `reti3.yaml`) exist. Not present at `v1.17.0`; introduced
   here. An agent resolving the locator literally gets nothing.
   **Fixed** — the four filenames are written out, with a note saying why the
   abbreviation was wrong.
2. **`hardware/edge-breadboard-carrier.yaml:63`** — cites
   `engineering/analysis/2026-08-25-yaml-release-change-ledger.md`, which does not
   exist. The ledger was superseded by `2026-08-27-yaml-release-change-ledger.md`
   and the 08-25 copy moved to `engineering/analysis/archived/`. A stale locator
   left by a rename — the exact F-365/F-377 class this sprint was closing. It also
   points *outside* the shipped deliverable, which a shipped YAML should not do.
   **Fixed** — re-pointed at `engineering/analysis/archived/…`, where item 7 still
   reads as cited, with the rename recorded in place.

Neither was caught by `validate-crossref-keys.py`, which reports
`ALL TOP-LEVEL CROSS-REFERENCES RESOLVE` — both sit in comment/prose text, the same
blind spot as F-373 and the 698 unchecked nested sites.

**Pre-existing and unchanged:** 17 further unresolved KB references, already
carried as block-D task «#335» and out of scope here. This delta fixed 2 of them
(`concepts/basic-io.yaml` ×2, one `concepts/labels.yaml` site) and introduced 1,
for a net 21 → 19 broken sites while total reference sites grew by 104. After this
pass's two repairs: **18 broken sites, and 0 unresolved ingestion-source citations
out of 368.**

---

## Verdict

**Strengthened.** Not by adding more, but by removing content that produced
plausible, compilable, wrong code — an inverted interrupt vector map, 41 invented
instruction encodings, a pull-up idiom that floats the pin, a streamer example that
silently selects a different mode, a delay bound wrong by 400×, and a duplicate key
that deleted a timing block from the parse.

The residual risk moved from *"the agent is confidently told something false"* to
*"the agent is told less, and told where the rest lives."* That is the right
direction for a code-generation source, and it is the harder direction to travel.

The two locators this pass introduced are repaired. The 17 block-D references
remain, tracked as «#335»; they are pre-existing, not a product of this delta, and
they do not change the verdict.
