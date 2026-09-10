# Example purposes — P2AN004

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `rc-decay-reader.spin2` — Read any resistive or capacitive sensor by timing an RC decay in hardware with P_HIGH_TICKS
- `light-to-freq-reader.spin2` — Read a light-to-frequency sensor with a reciprocal counter, accurate at low frequencies because the window ends on a whole period
- `quadrature-knob.spin2` — A drop-in encoder knob with detent normalization, preset, range clamp and a debounced button, self-verifying with two jumper wires
