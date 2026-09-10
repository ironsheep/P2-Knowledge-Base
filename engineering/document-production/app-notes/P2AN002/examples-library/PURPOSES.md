# Example purposes — P2AN002

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `cordic-distance-heading.spin2` — Distance and bearing between two points from one XYPOL, the cartesian-to-polar navigation primitive
- `cordic-rotate-point.spin2` — Rotate a point about the origin with ROTXY, using the P2's full-circle 32-bit binary angle
- `cordic-draw-circle.spin2` — Place points around a circle or arc with POLXY, polar to cartesian one point at a time
- `cordic-sine-cosine.spin2` — Generate a sine or cosine wave with QSIN and QCOS, scaled by an amplitude you choose
- `cordic-fixed-point.spin2` — 64-bit-safe scaling, magnitude, and log/exp without overflow, via MULDIV64 and the solver
- `cordic-pipeline-throughput.spin2` — Keep the 54-stage pipeline full so a finished result arrives every eight clocks instead of every 55
