# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `ch01-first-blink.spin2`: Your first cog of your own - Spin2 launches a DAT block of PASM2 and then gets out of its way
- `ch02-hub-counters.spin2`: Eight cogs running one routine, told apart only by the hub address each was handed in PTRA
- `ch02-multicog-blink.spin2`: PTRA carrying a pin number, then reused as scratch to build the delay - one image, four different behaviours
