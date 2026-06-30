# P2 Capability Taxonomy — the Spine

> **Status:** v1 (2026-06-29), authored under the *Capability Coverage &
> App-Note Roster* sprint (`engineering/planning/P2-CAPABILITY-COVERAGE-AND-APP-NOTE-ROSTER-SPRINT-PLAN.md`,
> Phase 1). This is the **single classification axis** every P2 community/teaching
> artifact maps onto — OBEX objects, Quick Bytes, P1 app notes, P2 manuals, and
> (future) P2 app notes. It exists so those corpora can be *compared* for
> coverage and gap analysis.

## Why one axis

OBEX, Quick Bytes, and the P1 app notes each speak their own vocabulary
(OBEX has 9 categories; Quick Bytes ~21 tags; P1 app notes their own topics).
You cannot ask "what does the P2 ecosystem already cover, and where are the
holes" until every artifact is normalized to **one shared notion of the
task/capability it addresses.** That shared notion is this spine. Each artifact
classifies to a **primary domain + leaf**, optionally with **secondary** leaves
when it genuinely spans more than one.

**The spine is P2-complete, not a union of the source vocabularies.** Some P2
capabilities (CORDIC, the streamer, XBYTE, events) have little or no
community-artifact coverage *yet* — they still get first-class domains, because
the whole point is to surface where coverage is *missing*.

---

## The 11 domains

### A. Core compute model
*How to think in the chip's compute model — the architecture-technique layer.*
Leaves: cogs / multicore structure · task scheduling & native multitasking
(P1 coroutines transform to here) · execution timing & determinism · stack &
local storage · inline PASM · abstract data structures · events · interrupts ·
locks & inter-cog coordination · system emulation / VM (full-chip orchestration,
e.g. NeoYume / MegaYume).
> Architecturally grounded in `deliverables/ai/P2/architecture/cog.yaml`,
> `event_system.yaml`, `interrupts.yaml`, `locks.yaml`,
> `multi_resource_management.yaml`. **The richest predicted app-note vein** —
> P1 leaned a third of its app notes here, and it's the P2's steepest learning
> curve.

### B. Smart Pins & I/O
*Using the 64 smart pins and basic pin I/O.*
Leaves: pin modes & configuration · ADC (incl. sigma-delta, SAR) · DAC ·
PWM / NCO · frequency / edge / pulse measurement · Schmitt / comparator inputs ·
quadrature decode (smart-pin mode) · USB / repository pin modes.
> Grounded in `architecture/smart_pins.yaml`, `smart_pin_patterns.yaml`,
> `io_pin_timing.yaml`. P1 counters transform to here.

### C. Math & DSP
*On-chip math acceleration and signal processing.*
Leaves: CORDIC (rotate / vector / scale / log/exp) · fixed-point & floating-point ·
Goertzel / tone detection · digital filtering · FFT · PRNG (pseudo-random) ·
image codecs (e.g. JPEG decode).
> Grounded in `architecture/cordic.yaml`. Largely **P2-unique** — no P1
> precedent for CORDIC.

### D. Streaming & video generation
*The streamer / FIFO data-movement engine and pixel generation.*
Leaves: streamer modes · FIFO · XBYTE bytecode-execution engine · pixel / scanline
generation · HDMI / DVI / VGA signal generation · DMA-like block movement.
> Grounded in `architecture/streamer/`, `fifo.yaml`, `xbyte_engine.yaml`.
> Largely **P2-unique**. *Distinguish from G:* D is signal/pixel **generation**;
> G is the **driver/UI** built on top.

### E. Comms & protocols
*Talking to other devices and hosts.*
Leaves: UART / serial · I2C · SPI · 1-Wire · wireless (XBee, ESP, BLE) ·
IoT gateway · PC-host / desktop-application comms · networking · IR remote ·
RFID · CAN bus · DMX · MAVLink.

### F. Sensors & environment
*Acquiring real-world measurements.*
Leaves: temperature / humidity · GPS / NMEA · distance / ultrasonic · light /
optical · touch / capacitive · RTC / timekeeping · human input (buttons,
encoders as *input*) · IMU / 9-DOF · compass / magnetometer · machine vision
(camera modules).

### G. Displays & graphics
*Driving displays and building visual output.*
Leaves: VGA / DVI / HDMI text & image **drivers** · LCD / e-ink · LED matrix /
NeoPixel / addressable LED · terminal / ANSI output · GUI: menus, window
managers, widgets · HMI display modules (Nextion-style) · graphics libraries.

### H. Motors & motion
*Actuation and motion control.*
Leaves: servo (incl. multi-servo) · brushless / BLDC · stepper / DC ·
quadrature encoders (as *motion feedback*) · robotics platforms.

### I. Storage & memory
*Persisting and moving bulk data.*
Leaves: on-board / SPI flash · SD card / FAT filesystem · external RAM
(HyperRAM / PSRAM) · hub & lookup RAM patterns · EEPROM.
> Grounded in `architecture/hub.yaml`, `lookup_ram.yaml`.

### J. Audio
*Sound generation and playback.*
Leaves: sound engine / synthesis · DAC audio playback · music / tone sequencing.

### K. Dev tools & workflow
*Building, loading, debugging, and host-side workflow.*
Leaves: toolchain / editor setup (VS Code) · project templates / scaffolding ·
DEBUG windows & instrumentation · programming / loading (incl. wireless load) ·
host-platform integration (e.g. Raspberry Pi as host).

---

## Source-vocabulary mapping

How each existing corpus's categories/tags resolve onto the spine. **Cross-cutting
categories don't map to one domain — each artifact under them is classified by its
own content.**

### OBEX `functionality.category` (9) → domain

| OBEX category | Spine domain |
|---|---|
| `display` | G |
| `audio` | J |
| `motors` | H |
| `communication` | E |
| `sensors` | F |
| `tools` | K |
| `drivers` | **cross-cutting** — a *role*, not a domain; classify per object by what it drives (a SPI flash driver → I; a VGA driver → G; a servo driver → H) |
| `demos` | **cross-cutting** — classify per object by what it demonstrates |
| `misc` | **cross-cutting** — classify per object |

### Quick Bytes tags (~21) → domain

| QB tag | Spine domain |
|---|---|
| Smart Pins | B |
| ADC/DAC | B |
| Math *(implicit)* | C |
| VGA/HDMI | G (driver) — note D when it's signal-generation |
| Visual | G |
| LED | G |
| LCD | G |
| Gaming | **cross-cutting** — usually G; classify per content |
| Protocols | E |
| Wireless | E |
| IoT | E |
| Raspberry Pi | K (host integration) |
| Sensors | F |
| Environmental | F |
| RTC | F |
| GPS | F |
| Human Input | F (input) — note B when it's smart-pin sensing |
| Motor Control | H |
| Robotics | H |
| Memory | I |
| Audio | J |
| Development Tools | K |
| Utility | K — classify per content; some are F/E/I utilities |

---

## Classification schema (for the catalog YAMLs)

Each artifact carries:

```yaml
capability:
  domain: B            # one of A–K
  leaf: adc            # leaf slug within the domain
  secondary:           # optional, when the artifact genuinely spans domains
    - { domain: F, leaf: light }
```

**Rules:**
1. Exactly **one** primary `domain` + `leaf`. No orphans — if nothing fits, the
   spine is incomplete; fix the spine, don't force the artifact.
2. `secondary` is optional and only for genuine multi-domain artifacts.
3. A cross-cutting source category (`drivers`/`demos`/`misc`, `Gaming`,
   `Utility`) is **never** the classification — resolve to the real domain by
   what the artifact does.

> **Leaf lists are illustrative, not closed.** Classifiers may introduce a
> finer leaf when an artifact warrants it (the OBEX pass added `ir-remote`,
> `imu`, `can-bus`, `dmx`, `emulation`, etc.). A genuinely new, recurring leaf
> is backfilled into the domain's list above; it is **not** a missing-domain
> signal. A *new domain* is warranted only if a real capability fits **none** of
> A–K — which has not occurred (all 11 domains hold as of the 2026-06-29 OBEX
> pass, 130 objects).

## Non-capability resources (out of the spine)

Some artifacts that appear in a community catalog are **not capabilities** — they
are design *resources*, not something a developer learns to do. Concretely:
**hardware-design assets** — PCB / schematic files (KiCAD, DipTrace), 3D /
mechanical models (Fusion, STEP), board libraries (e.g. OBEX 4864/4898/4899/4905/5096).

These are **recorded but excluded from capability classification and from
app-note-gap analysis**: they generate no app-note candidate and occupy no
domain's capability space. Park them at `capability: {domain: K, leaf:
hardware-design}` as a recognized non-capability marker (so nothing is orphaned),
and exclude `leaf: hardware-design` rows from the coverage matrix's gap logic.
This is distinct from a *missing domain* — the artifact has no capability to
classify, not a capability with no home.

## See also
- `engineering/standards/documentation-standards/artifact-placement-rubric.md`
  — which *form* (OBEX / Quick Byte / app note / manual) a given capability gap
  should take.
- The format-donor + app-note-companion decision record in
  `engineering/document-production/app-notes/`.
