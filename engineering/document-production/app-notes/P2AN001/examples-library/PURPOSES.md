# Example purposes — P2AN001

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `adc-single-pin-base.spin2` — Read an absolute voltage in microvolts on one pin by rotating the ADC across GIO, VIO and the pin, and taking the ratio
- `adc-three-pin.spin2` — Three pins tied to one node, sampled together for lower noise in the same time at constant source impedance
- `adc-filter-cascade.spin2` — A time-halving cascade that hands you every rate-vs-resolution trade at once from a single sample stream
