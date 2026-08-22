# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `ch03-blink-led.spin2`: The first program - a pin driven high and low on a timer, and nothing else to distract from it
- `ch03-inline-pasm-toggle.spin2`: The same blink with one native instruction dropped inline, showing where Spin2 ends and PASM2 begins
- `ch03-two-cog-blink.spin2`: Two LEDs at two rates, because the second cog runs the same method independently rather than taking turns
- `ch03-shared-mailbox.spin2`: A hub long as the meeting point - one cog writes it, another reads it, with no copy passed between them
