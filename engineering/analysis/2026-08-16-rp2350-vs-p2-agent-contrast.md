# RP2350 vs P2 — Agent-Produced Contrast (INPUT DOCUMENT)

## ⚠️ TRUST TIER — READ BEFORE CITING

**This is an UPSTREAM LEAD, not an authority.** It was produced by an AI agent at
Stephen's request on 2026-08-16 and supplied as input to the deSilva Appendix A
review (observation **V-3**).

- **NOT a citable source.** No claim in this document may appear in a
  reader-facing manual on this document's word alone.
- **RP2350 claims** require the Raspberry Pi RP2350 datasheet. We hold **no
  RP2350 source** in the ingestion tree (2026-08-16 sweep: the only mention
  anywhere is a passing line in `sources/spin2-v51/p2-article-brainstorm.md`).
- **P2 claims** must be checked against our own KB / ingestion tree, which
  outranks this document absolutely. At least one P2 claim here is suspect —
  see "Assessment" below.
- Its value is **framing**: which axes the comparison should be drawn on.

Same tier as forum material and Titus: useful lead, never a peer-trust citation.

---

## VERBATIM — as supplied

> Tell me more about the RP2350 versus the P2 in hardware architecture, please.

The RP2350 and Propeller 2 are both unusually capable microcontrollers, but they embody almost opposite design philosophies. RP2350 is a conventional bus-and-peripheral MCU with two CPU cores plus programmable I/O engines; the P2 is an eight-way symmetric real-time parallel processor where every cog can directly participate in I/O work.

### At a glance

| Hardware aspect | RP2350 | Propeller 2 (P2X8C4M64P) |
|---|---|---|
| Main CPU arrangement | Two cores: choose dual Arm Cortex-M33F or dual Hazard3 RISC-V at boot/OTP configuration | Eight identical 32-bit cogs, all running simultaneously |
| CPU character | Conventional load/store cores with NVIC interrupts, standard ABI/toolchains, FPU/DSP on the Arm option | Deterministic custom cores with tight cog-local execution and explicit parallelism |
| Typical clock | Up to 150 MHz | Up to 320 MHz, depending on operating conditions |
| On-chip SRAM | 520 KB, organized as 10 SRAM banks | 512 KB shared Hub RAM, plus 4 KB local Cog/Lookup RAM per cog |
| Local CPU memory | Caches and bus-visible SRAM architecture; program/data normally live in shared memory or external flash | Each cog has 512 longs Register RAM and 512 longs Lookup RAM—2 KB + 2 KB per cog |
| I/O count | 30 GPIO on RP2350A or 48 GPIO on RP2350B | 64 Smart Pins |
| Flexible I/O | 3 PIO blocks, 4 state machines each: 12 total | Smart functionality exists at every pin, controlled by any cog |
| DMA | 16 DMA channels | Cogs plus streamer/smart-pin hardware move data; not a conventional channel-DMA-centric architecture |
| Math hardware | Hardware single-precision FPU and DSP instructions on Cortex-M33 path | Central CORDIC engine for trig/vector operations |
| Flash | External QSPI flash on RP2350; RP2354 variants add stacked flash | External boot source/flash is normal; P2 executes from Hub RAM after loading |
| Analog | 12-bit ADC, temperature sensor, PWM blocks | Per-pin DAC/ADC/comparator-style smart-pin capabilities, with I/O supply partitioned in groups of four |

RP2350 gives you a familiar modern MCU environment; P2 gives you far more identical, deterministic execution agents.

### CPU and parallelism

**RP2350: two application cores plus I/O coprocessors**

An RP2350 starts in one of two ISA modes: two Arm Cortex-M33 cores or two Hazard3 RISC-V cores. The CPU pair is symmetric, but it is still essentially a conventional dual-core MCU: core code, interrupts, DMA, memory-mapped peripherals, and an AHB/APB interconnect. The Arm path has a hardware single-precision FPU and DSP instructions, which is attractive for control loops, filters, sensor fusion, and existing CMSIS-oriented code.

The PIO blocks are the key architectural twist. There are three PIO instances with four state machines apiece, so 12 small deterministic I/O engines. A PIO state machine is not a general processor: it executes a compact I/O-oriented instruction set, uses FIFOs, and is intended to synthesize interfaces or waveforms—custom serial buses, precise capture/generation, LED protocols, unusual display timing, and similar jobs.

**P2: eight peers, not "main cores plus I/O blocks"**

On the P2, every cog is a full 32-bit processor with the same instruction set and access to the same Hub RAM and pin fabric. There is no designated "core 0 for application, core 1 for I/O" division imposed by hardware. You can instead dedicate one cog to video timing, one to a network driver, one to an SD/FAT layer, one to a control loop, and leave four for the application—without those roles having fundamentally different CPU capabilities.

That makes the P2 a better fit when concurrency is intrinsic to the problem. Rather than arranging interrupt priorities and hoping latency remains bounded, you often turn the time-critical task into a permanently running cog. For example, a PASM2 cog can own an SD data path, while another cog independently owns precise pulse measurement or RF-adjacent timing.

The trade-off is software structure: P2 rewards explicit ownership, mailboxes/locks, and producer-consumer designs. RP2350 rewards a more familiar firmware model built around drivers, interrupts, RTOS tasks, and DMA.

### Memory architecture

The difference is deeper than the near-identical headline SRAM capacity.

RP2350's 520 KB is banked shared SRAM behind its bus fabric. Its two CPUs, DMA, PIO, and peripherals interact through conventional memory-mapped machinery. The banking allows useful concurrency, but contention still matters when CPUs and DMA masters target the same resources. Program storage is normally external QSPI flash, and the RP2350's XIP subsystem makes it practical to execute code directly from flash.

P2's 512 KB Hub RAM is a contiguous shared address space, but every cog also has its own 2 KB Register RAM and 2 KB Lookup RAM. Cog RAM is especially important: it acts as both very fast local working storage and a local instruction space. The P2 also supports Hub execution, so a cog can execute larger programs from shared Hub RAM while using a FIFO/prefetch mechanism; this reduces the old P1-style "2 KB code ceiling," though local cog execution remains the tightest deterministic option.

A useful framing:

- On RP2350, local CPU speed is largely about the core pipeline, memory placement, cache/XIP behavior, bus traffic, and DMA arbitration.
- On P2, you can place the critical inner loop in one cog's local memory, yielding an isolated timing domain, while bulk buffers and inter-cog exchange reside in Hub RAM.

For deterministic driver work, the P2 memory model is unusually direct: local loop state stays local, and Hub accesses are intentional rather than accidental consequences of normal code execution.

### I/O architecture

This is where the P2 is most architecturally distinct.

**P2 Smart Pins**

Every one of the P2's 64 pins is a Smart Pin. Each can be configured for autonomous digital or analog-adjacent functions: counting, timing, pulse measurement, serial shifting, DAC output, ADC-related measurement modes, comparator/logic modes, and more. A cog configures the pin, then can often let the pin hardware perform repetitive external work while it attends to other processing. Each pin is individually accessible from all cogs, with mechanisms for coordination when several cogs need shared access.

The P2's pin system also has a streamer, which works alongside cogs and smart pins for high-rate serial/parallel data movement. In practice, Smart Pins plus streamer plus cogs blur the usual distinctions among GPIO, timer/counter, DMA, PWM, serial peripheral, and programmable-I/O unit.

That is particularly valuable for applications involving:

- Accurate edge and period measurement
- High-rate waveform generation
- Bit-banged or nonstandard protocols
- Composite/video-like timing
- Parallel display/camera-style streams
- Multiplexed serial interfaces with hard timing limits

**RP2350 PIO and fixed peripherals**

RP2350 has standard peripherals—UART, SPI, I²C, PWM, ADC, USB—and supplements them with its 12 PIO state machines. This is an excellent and flexible arrangement: use hardened peripherals where the protocol is standard, use DMA to keep them supplied, and reserve PIO for specialized timing or custom interfaces.

But PIO is a pool of 12 shared engines, whereas P2 Smart Pin capability is distributed across all 64 pins. If you require many independent timed I/O channels at once, P2's architecture can scale more naturally: allocate pin functions and cogs rather than consuming a scarce set of PIO state machines and associated pin mappings.

Conversely, if you need USB, a conventional ADC subsystem, standard serial peripherals, or an ecosystem of mature vendor SDK drivers, RP2350's fixed-peripheral model is usually simpler.

### Practical choice for P2 work

For an engineer already writing Spin2/PASM2 drivers, the RP2350 will feel like a very capable mainstream MCU with unusually good programmable I/O. Its strengths are excellent toolchain compatibility, FPU/DSP availability on Arm, security features including OTP, conventional DMA, and accessible low-cost board support.

The P2 is more compelling when the architecture itself is the solution:

- You need more than two genuinely independent real-time processing paths.
- Timing must remain predictable without an interrupt-heavy design.
- You want each I/O pin to be an autonomous instrument rather than merely a GPIO connected to a limited set of peripheral blocks.
- You can benefit from putting a full processor permanently beside an I/O/dataflow problem.
- You want to build the equivalent of several peripherals in software without sacrificing the main application's responsiveness.

A concise analogy: RP2350 is a strong dual-core MCU with a programmable peripheral department; P2 is an eight-person real-time workshop where every worker can directly operate every machine.

---

## Assessment — see the V-3 discussion in
## `SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md` for the disposition.

Filled in during the 2026-08-16 review; the short form:

- **Most useful contribution:** it relocates the comparison axis from *pin
  mapping* (which would need per-pin RP2350 citations we do not have) to
  **scarcity of the flexible resource** — 12 shared PIO state machines vs. smart
  functionality at all 64 pins. That is a **countable** claim, durable and
  checkable, and the P2 half of it is entirely ours to source.
- **Suspect P2 claim:** "Up to 320 MHz, depending on operating conditions."
  Checked against our own material before any use — a P2 clock-rate claim is
  ours to get right, and this is exactly the shape of unsourced claim the
  correctness sweep exists to remove.
- **RP2350 numbers were unverified in this document** — they have since been
  checked against primary vendor sources. See the verified table below; use
  THAT, never this document's table.

---

## VERIFIED — primary vendor sources (checked 2026-08-16)

These are the only RP2350 facts cleared for reader-facing use. Cite the
documents, not revision-specific pages.

**Sources:**
- *RP2350 Product Brief*, Raspberry Pi Ltd — <https://datasheets.raspberrypi.com/rp2350/rp2350-product-brief.pdf>
- *RP2350 Datasheet*, Raspberry Pi Ltd — <https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf>

| Verified fact | Where |
|---|---|
| "Three high-performance Programmable I/O (PIO) co-processors, with a total of twelve independent state machines" | Product Brief p.1 |
| Hardened serial peripherals: **2 × UART, 2 × SPI controllers, 2 × I2C controllers**, 24 × PWM channels, 1 × USB 1.1 | Product Brief, Key features |
| Dual Arm Cortex-M33 **or** dual Hazard3 RISC-V **@ 150 MHz** | Product Brief, Key features |
| 520 KB on-chip SRAM, **in ten independent banks** | Product Brief, Key features |
| Four package variants: **30 or 48 GPIO**, with/without 2MB stacked flash | Product Brief p.1 |
| "**SIO, PIO0, PIO1 and PIO2 can connect to all GPIO pins**" — PIO is NOT pinmux-limited | Datasheet §1.2.3 |
| Hardened peripherals ARE pin-limited: Bank 0 table shows SPI0/UART0/I²C0 on fixed repeating pin subsets; "Some internal peripheral connections appear in multiple places to allow **some** system level flexibility" | Datasheet §1.2.3, Table 3 |
| "The four state machines execute from **shared instruction memory**" | Datasheet §11.2 |
| "Each PIO instance has a **32-slot instruction memory, which all 4 state machines can see**" | Datasheet §11.2 |
| "Instruction memory is implemented as a 1-write, 4-read register file, allowing all four state machines to read an instruction on the same cycle without stalling" | Datasheet §11.2.8 |

### Two corrections this research forced

1. **Pin mapping is the WRONG axis.** V-3 was originally framed on RP2350 "I/O
   comms choice mapping." PIO reaches every GPIO, so that framing would have been
   corrected by the exact expert reader it was meant to convince. The mapping
   constraint is real only for the *hardened* peripherals.
2. **The right axis is scarcity + shared program store** — 12 state machines in
   3 blocks, four sharing one 32-slot instruction memory. That is the wall PIO
   users actually hit, and it is what earns recognition.

### Claim explicitly REJECTED from this document

**"Up to 320 MHz, depending on operating conditions" (P2).** Our own KB
(`deliverables/ai/P2/hardware/edge-standard-module.yaml`) records
`recommended_max_mhz: 180` with `overclock_tested_mhz: 320`;
`P2-UNIFIED-AUTHORITATIVE-DESCRIPTION.md` says "DC to 320 MHz operation (180 MHz
typical)." This document presents the **overclock** figure as a headline spec —
exactly the unsourced-claim shape the correctness sweep exists to remove, and
about our own chip. Any side-by-side clock comparison is **150 vs 180**.
