# Appendix G: FPGA Board Differences

The target for this guide is the **Propeller 2 ASIC** — the production silicon. Before the ASIC existed, the P2 design was emulated on FPGA development boards, and those boards remain in limited use. An FPGA emulation reproduces the P2's digital logic faithfully, but it cannot reproduce the analog and mixed-signal hardware built into the ASIC's pins, and it runs from a fixed development clock rather than the ASIC's configurable clock generator.

Everywhere else in this guide, behavior is described for the ASIC. Where a smart pin or I/O behavior depends on hardware the FPGA does not have, this appendix records the difference. If you are running on an FPGA board, read this appendix first.

## USB — No Built-In Resistors

The ASIC's USB smart pins (mode `%11011`, Chapter 19) include the 1.5 kΩ and 15 kΩ resistors that USB signaling requires, built directly into the pin hardware. An FPGA emulation has no such resistors — you must fit them yourself on the DP and DM lines.

## Clock — Fixed 20 MHz or 80 MHz

The ASIC derives its system clock from an on-chip oscillator and PLL, configurable across a wide frequency range. On an FPGA, the clock generator is not emulated: the only supported system-clock settings are **20 MHz** and **80 MHz**.

The timing relationships throughout this guide still hold — baud rates, NCO frequencies, and measurement windows are all expressed relative to the system clock. Simply substitute the FPGA's actual clock frequency (20 MHz or 80 MHz) wherever a calculation uses the system clock.

## Other Board-Level Differences

FPGA boards also differ from the ASIC in ways that are not specific to the pins — most notably the amount of hub RAM (an FPGA image provides only a portion of the ASIC's 512 KB, as little as 32 KB on small boards) and, on the smallest boards, the number of emulated cogs. These vary from board to board and from image to image; consult your board's documentation for its exact configuration before sizing buffers or assuming eight cogs are available.
