# XBYTE Guide — worked examples

Every file here is **byte-identical to the code block it appears as in the manual**, and
each one **compiles clean** with `pnut-ts`. That identity is the point: what you read is
what builds.

| File | Manual | What it shows |
|------|--------|---------------|
| `xbyte-minimal-vm.spin2` | Ch. 10 | The smallest complete XBYTE program: load a table, prime the FIFO, arm the engine, four bytecode handlers, halt. Exercises the whole engine once. |
| `xbyte-display-list.spin2` | Ch. 16 | The complete **non-interpreter** build — the same engine walking a graphics display list. Auto-fetch, inline operands, and a seeking read cursor. |

## Building

```
pnut-ts xbyte-minimal-vm.spin2
```

`.bin` output is **not** committed — it is recreatable from the source, and the `.spin2`
is the artifact of record.

## Verification status

Both examples are **compile-verified** (`pnut-ts` v1.55.0). Running them on real P2 silicon
is a separate step; nothing here has been hardware-confirmed, and the manual does not claim
otherwise.
