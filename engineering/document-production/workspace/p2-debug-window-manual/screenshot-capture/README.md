# Screenshot Capture — P2 Debug Window Manual

Generates the manual's output-window figures by **running the examples on a real P2**
and letting each example `SAVE` its own DEBUG window to an image. This is build
tooling for the manual — it lives under `workspace/`, not `manuals/`.

> **Location note.** The manual *source* is in
> `manuals/p2-debug-window-manual/opus-master/`. All *production* tooling (templates,
> `assemble-manual.sh`, outbound staging, and this folder) is in
> `workspace/p2-debug-window-manual/`. Both end in `p2-debug-window-manual` — easy to mix up.

## What's here

```
screenshot-capture/
├── capture-screenshots.sh   # the resumable driver (run this)
├── examples/                # one self-saving .spin2 per figure
│   └── fig-NN-window-name.spin2
└── captures/                # scratch: raw .bmp the window writes (created on first run)
```

Final figures land in `../assets/` as `fig-NN-window-name.png` and flow to outbound
with the rest of the manual's assets.

## Tools (set once in the script, applied to every example)

- `CC='pnut-ts -d'` — the **compiler** (`.spin2` → `.bin`).
- `RUN='pnut-term-ts -r {BIN}'` — **PNut Term-ts**: `-r` downloads the `.bin` to the
  P2's RAM and runs it, opening the DEBUG window. `{BIN}` is filled in per example.

You do **not** edit anything per-example — the script feeds every example through these.

## How to run (on a host with a P2 attached)

```
./capture-screenshots.sh
```

For each example: compile → `pnut-term-ts -r` (window opens; the example `SAVE`s its
window; the program ends / you quit PNut Term-ts) → the `.bmp` is converted to a `.png`
in `../assets/`.

- **Resumable.** It skips any example whose `.png` already exists, so re-running picks
  up the next missing capture. A failed/partial run just gets retried next time.
- **Blocking.** Each run waits for PNut Term-ts to exit before moving on — so it doesn't
  matter whether PNut Term-ts self-quits on program end or you quit it by hand.
- **`.bmp → .png`** uses ImageMagick (`magick`/`convert`). Without it, the script keeps
  the `.bmp` and the figure refs point at `.bmp` instead.

## How an instrumented example is shaped

Each `examples/fig-NN-*.spin2` draws one representative frame, then:

```spin2
debug(`Win SAVE 'fig-NN-window-name')   ' writes fig-NN-window-name.bmp on the host
waitms(2000)                            ' let the host flush the file, then the program ends
```

`SAVE 'name'` appends `.bmp` (so the arg is the base name, no extension). The filename
must match the `.spin2` stem so the resumable check and the `.png` conversion line up.

These same example sources double as the **example-`.zip`** deliverable's runnable files.
