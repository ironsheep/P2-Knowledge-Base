# Changelog: Getting Started with the Propeller 2

All notable changes to *Getting Started with the Propeller 2, Meet the Chip, Read
Its Code, Put It to Work* are recorded here. The manual owns its own version (manual
head); this is the source of truth for the version string carried in `request.json`
metadata and on the title page.

Format follows the house manual-changelog convention (audience-facing, traceable to
commits). Newest entry first.

---

## v1.0.4 (2026-09-10)

**The one cog-launch value that means the opposite of what it looks like.**

### Added

- **One board check before the first program runs** (Putting It to Work): P56 is the LED on a P2 Eval Board and on the standard P2 Edge Module, but the **P2 Edge 32MB Module** carries its two LEDs on **P38 and P39**, and P56 there is a PSRAM clock line — so the program as printed lights nothing and writes to the memory bus. Change `LED` to match your board
- **The `-1` return travels in one direction only** (Running Code on Another Cog): it is what `cogspin` returns on failure, never a value you pass in. `coginit(-1, ...)` — the idiom carried over from P1 code — arrives as `$FFFF_FFFF`, whose low six bits read `%111111`, and starts an even/odd **pair** of cogs, quietly spending two where one was meant. `NEWCOG` is the symbol that means "any free cog"

---

## v1.0.3 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this guide, including commercially, with attribution and under the same terms.


## v1.0.2 (2026-07-21)

A readability refinement. No chapters added, no technical content changed.

- **Prose**: the orientation reads more naturally, with more variety in how its sections open and close.

---

## v1.0.1 (2026-07-11)

An accuracy refinement. No chapters added.

- **Instruction timing**: most register-to-register PASM2 instructions execute in two clocks, while branches and hub accesses take more.

---

## v1.0.0 (2026-06-24)

**Initial release for community review.** A warm orientation on-ramp to the Propeller 2,
the layer below the reference manuals: it builds a mental model of the chip, teaches you to
read P2 code, and puts it to work, then points you to the reference manuals for depth and to
the companion *P2 Architect's Guide* for whole-system design. P1-migration sidebars
throughout, with runnable, compile-clean Spin2 examples.
