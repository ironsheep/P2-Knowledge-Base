# Chapter 11: The MIDI Window — Piano-Keyboard Display {#ch-11}

The MIDI window draws an on-screen piano keyboard and lights its keys in
response to MIDI note messages. You feed it raw MIDI bytes — the same Note-On
and Note-Off bytes a synthesizer or controller would send — and it illuminates
the matching key, filling it from the bottom up in proportion to the note's
velocity. It is the window you reach for when you are debugging a MIDI
implementation, watching a sequencer or synthesizer engine you wrote, or
visualizing a performance: instead of reading a stream of hex bytes, you see the
notes appear on a keyboard.

The window is purely a *display*. It does not produce sound and it does not read
a MIDI port for you. You generate the MIDI bytes in software and send them with
`DEBUG()`; the window parses them and updates the keyboard. Every example in this
chapter runs on a bare P2 with no external MIDI hardware.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the MIDI window as in
> every other window. They share one mechanism across all window types, so they
> are covered together in [Chapter 12](#ch-12). This chapter is about the keyboard display.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=\linewidth]{inbox/assets/fig-11-midi.png}
\caption{The MIDI window showing notes lit on a piano keyboard.}
\end{figure}
```

## Creating a MIDI window

You create and configure the window in a single `DEBUG` statement. The first
token after the backtick is the window type (`MIDI`); the second is a name you
choose. You feed the window afterward by that name:

```spin2
debug(`MIDI Piano SIZE 6 RANGE 48 84 CHANNEL 0)   ' create, named "Piano"
debug(`Piano $90 60 96)  ' feed it by name: note-on
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | none (window name) | The window's title-bar text |
| `POS` | `left top` | `0 0` | Screen position of the window, in pixels |
| `SIZE` | `multiplier` | `4` | Key-size multiplier, **1–50** |
| `RANGE` | `first last` | `21 108` | First and last MIDI note to display, each **0–127** |
| `CHANNEL` | `channel` | `0` | The single MIDI channel to display, **0–15** |
| `COLOR` | `white_active black_active` | cyan, magenta | Lit-key colors (white key, then black key), each a named color (optional 0–15 brightness) or an `$RRGGBB` value |

A few things to know about these:

- **`SIZE`** is a multiplier, not a pixel count. The white-key width is
  `8 + SIZE x 4` pixels, so `SIZE 4` gives 24-pixel keys and `SIZE 50` gives
  208-pixel keys. The whole window sizes itself from this and from the note
  range; you do not set a width and height directly.
- **`RANGE`** selects which slice of the 128 MIDI notes is drawn. The default
  `21 108` is the standard 88-key piano (A0 to C8). You can show any subset —
  `RANGE 60 72` is one octave from middle C — or the full `RANGE 0 127`.
- **`CHANNEL`** is a single channel, 0–15. The window displays notes only on
  that channel and ignores all others; it does not have an "all channels" mode.
  MIDI channels are numbered 1–16 on instruments, so channel 1 is `0` here and
  channel 16 is `15`.
- **`COLOR`** takes exactly two color values: the first is the lit color for
  white keys, the second for black keys. Each value may be a named color
  (optionally with a `0`–`15` brightness) or a full `$RRGGBB` value. Unlit white
  keys are always white and unlit black keys are always black; only the *active*
  fill color is configurable.

```spin2
' One octave, large keys, green/orange lit colors, channel 0
debug(`MIDI Keys SIZE 8 RANGE 60 72 CHANNEL 0 COLOR GREEN ORANGE)
```

Each key is labelled with its MIDI **note number** (0–127), drawn rotated along
the key. The labels are note numbers, not musical note names — note 60 reads
`60`, not "C4".

## The MIDI bytes the window understands

Everything you send after the creation line is a stream of bytes — plain numeric
values, sent the same way you send command codes to other windows. The window
runs a MIDI parser over that byte stream. It recognizes exactly two messages:

| Message | Status byte | Then | Then |
|---------|-------------|------|------|
| **Note-On** | `$9n` (n = channel) | note number, 0–127 | velocity, 0–127 |
| **Note-Off** | `$8n` (n = channel) | note number, 0–127 | velocity, 0–127 |

`n` is the channel nibble. A Note-On on channel 0 is `$90`; on channel 5 it is
`$95`. The window acts on a message only when its channel nibble matches the
configured `CHANNEL`.

How the parser reads the stream:

- A byte with its top bit set (`$80`–`$FF`) is a **status byte**. It resets the
  parser and selects what comes next. `$9n` starts a Note-On; `$8n` starts a
  Note-Off (both only if `n` matches `CHANNEL`).
- A byte with its top bit clear (`$00`–`$7F`) is a **data byte** — a note number,
  then a velocity.
- A Note-On sets the note's velocity to the value you send. A Note-Off sets it to
  the negative of the value, which the renderer treats as "off." Either way the
  keyboard redraws after the velocity byte arrives.

**Running status.** After a status byte, the parser stays in that message type
and keeps reading note/velocity pairs until a new status byte arrives. So one
`$90` followed by several note/velocity pairs plays several notes on — you do not
repeat the `$90`:

```spin2
debug(`Piano $90 60 80 64 80 67 80)   ' three note-ons: C, E, G
```

That is three Note-On messages expressed as one status byte plus three pairs.

### Velocity and the lit fill

Velocity (0–127) controls how far up the key the lit color fills. A key lit at
velocity 127 fills completely; at velocity 64 it fills about halfway; at low
velocity only a sliver at the bottom lights. The fill always grows from the
bottom of the key upward, so a row of held notes reads like a bar chart of how
hard each was struck. White keys fill with the first `COLOR` value (default
cyan); black keys with the second (default magenta).

## Sending notes

To light a key, send a Note-On for it; to clear it, send a Note-Off for the same
note:

```spin2
debug(`Piano $90 60 96)   ' middle C (note 60) on, velocity 96
waitms(500)
debug(`Piano $80 60 0)    ' middle C off
```

When a note number comes from a variable, send its value with `` `() `` so it
goes out as a data byte rather than visible digits:

```spin2
debug(`Piano $90 `(note) `(vel))   ' note-on with variable note and velocity
```

This is the same distinction as in the other windows: `` `(note) `` sends the
*value* of `note` as a byte the parser consumes, whereas a formatter such as
`` `udec_(note) `` would render the digits as text — which the MIDI window does
not accept and would ignore as a string.

## Clearing and saving

Three runtime keyword commands round out the set:

- `` `CLEAR `` — resets every key to off (clears all stored velocities) and
  redraws an empty keyboard. Use it between takes, or to recover if a Note-Off
  was missed and a key is stuck lit.
- `` `SAVE {WINDOW} 'filename' `` — writes a `.bmp` of the display area (or of the
  whole window if you add the `WINDOW` keyword) to `'filename'` on the host; a
  filename is required.
- `` `CLOSE `` — closes this window and frees its resources.

```spin2
debug(`Piano CLEAR)   ' all keys dark again
```

## A complete software-only example

This program needs nothing but a P2 and the host running `pnut_term_ts`. It
generates its own MIDI bytes: it plays a C-major scale one note at a time, then a
C-major chord using running status, then clears the keyboard.

```{.spin2 caption="ch11-midi-scale-chord.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | i, note
  debug(`MIDI Piano SIZE 6 RANGE 48 84 CHANNEL 0)

  ' --- C major scale, one note at a time, on channel 0 ---
  ' note-on  = $90, note, velocity ;  note-off = $80, note, velocity
  repeat i from 0 to 6
    note := word[@scale][i]
    debug(`Piano $90 `(note) 96)       ' note-on, velocity 96 -> key fills
    waitms(300)
    debug(`Piano $80 `(note) 0)        ' note-off -> key clears
    waitms(60)

  ' --- C major chord via running status: one $90, then note/vel pairs ---
  ' C E G, all velocity 80, held together
  debug(`Piano $90 60 80 64 80 67 80)
  waitms(1000)
  debug(`Piano $80 60 0 64 0 67 0)     ' release all three (running status)
  waitms(300)

  debug(`Piano CLEAR)                 ' reset every key

  repeat                             ' keep the window open

DAT
scale word 60, 62, 64, 65, 67, 69, 71  ' C D E F G A B (MIDI note numbers)
```

Watch the keyboard: each scale note lights one key for 300 ms, then the three
chord keys light together for a second, then the keyboard goes dark.

To see velocity at work, hold one note and raise the velocity each pass — the lit
fill climbs higher each time:

```{.spin2 caption="ch11-midi-velocity.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | vel
  debug(`MIDI Keys SIZE 4 RANGE 21 108 CHANNEL 0 COLOR GREEN ORANGE)

  vel := 24
  repeat 5
    debug(`Keys $90 60 `(vel))         ' middle C on at the current velocity
    waitms(400)
    debug(`Keys $80 60 0)              ' off
    waitms(150)
    vel += 25
    if vel > 127
      vel := 127

  repeat                              ' keep the window open
```

### Where you'd use this

The honest answer is narrow: the MIDI window is for **music technology and MIDI
protocol work**. Its job is to show Note-On / Note-Off activity on a keyboard, and
that is the whole of it.

**On an embedded project**, that means debugging a synth or sequencer engine you
are writing, verifying the note output of a MIDI controller, or visualizing a
generative-music algorithm as it plays.

**Bandwidth fit:** MIDI is a slow, event-driven stream — comfortably inside the
link with room to spare.

**Extension (real hardware):** feed real MIDI bytes from a UART smart pin into the
window in place of the hardcoded notes, and it shows a live instrument's playing.

**If you are not building MIDI software, this is not your window.** Status values
belong in TERM ([Chapter 3](#ch-3)), a changing value in PLOT ([Chapter 5](#ch-5)),
and digital event timing in LOGIC ([Chapter 6](#ch-6)).

## Considerations

- **Only Note-On and Note-Off are recognized.** The parser acts on `$9n` and
  `$8n` and nothing else. Program Change, Control Change, Pitch Bend, Channel and
  Polyphonic Aftertouch, System Exclusive, and System Real-Time messages are not
  supported. If your software emits them, they will not move any key — and
  because their status bytes have the top bit set, each one simply resets the
  parser to wait for the next Note-On or Note-Off.
- **A velocity-0 Note-On clears the key.** Many MIDI sources end a note with a
  Note-On at velocity 0 instead of a real Note-Off. The window stores that
  velocity 0, and because a key lights only while its stored velocity is greater
  than zero, the key reads as off — the same visual result as a Note-Off. Sending
  an explicit Note-Off (`$8n`) is good MIDI practice, but it is not required to
  extinguish the key here. When you generate the bytes yourself, pairing each
  `$90` note-on with an `$80` note-off keeps your stream conventional.
- **One channel at a time.** The window shows exactly the channel set by
  `CHANNEL`; notes on other channels are ignored. To watch several channels at
  once, open one MIDI window per channel, each with its own `CHANNEL` value.
- **Choose the range to the job.** A narrow `RANGE` makes each key larger and the
  window narrower for the notes you care about; the full `RANGE 21 108` (88 keys)
  or `RANGE 0 127` is wide. Combine `RANGE` with `SIZE` to fit your display.
- **Note numbers, not note names.** Keys are labelled with MIDI note numbers
  (0–127). Middle C is 60; concert-pitch A is 69. There is no note-name labelling
  and no key-naming option.

## Try it

Start from the scale-and-chord example. Then build a short melody as a `DAT`
table of note/duration pairs and step through it, sending a Note-On, waiting the
duration, and sending the Note-Off. Add a second voice by sending a sustained
bass note on the same channel while the melody plays over it — you will see the
held key stay lit (filled to its velocity) while the melody keys come and go
above it. Finally, set `COLOR` to a pair of your own colors and lower the
velocity on the bass note to confirm the lit fill tracks velocity from the bottom
up.

> **See also.** Keyboard and mouse input in any window, including this one, is
> covered in [Chapter 12](#ch-12).
