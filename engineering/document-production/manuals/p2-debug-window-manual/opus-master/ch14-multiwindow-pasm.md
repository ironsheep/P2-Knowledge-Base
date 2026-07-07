# Chapter 14: Multiple Windows and PASM Debugging {#ch-14}

Up to this point each chapter has driven a single window. Real debugging rarely
stays that simple: you want a SCOPE showing a waveform *and* a TERM panel printing
the numbers behind it, both live at once. And not all of your code is Spin2 — when
the part you are chasing runs as PASM2 in its own cog, you need the same `DEBUG`
windows from inside that assembly.

This chapter covers both. Neither needs a new mechanism. You already know how to
create a window by name and feed it; running several at once is just doing that
several times, and debugging from PASM is the same `DEBUG` syntax in a different
language. The one thing to unlearn is the idea that windows talk to each other —
they do not.

## Several windows at once

You can have up to **32 graphical DEBUG displays** open simultaneously. You create
each one exactly as you would on its own: a `DEBUG` statement whose backtick names
the window type, then a **unique name** you choose. From then on you address each
window by its name, independently of every other window.

```spin2
debug(`SCOPE Wave POS 0 0 SIZE 400 200 'Sine' -1000 1000)
debug(`TERM Status POS 420 0 SIZE 40 10)
```

Two windows now exist — a SCOPE named `Wave` and a TERM named `Status`. They are
separate windows on the host. The only rule is that each name must be unique, since
the name is how every later feed is routed to the right window.

### Placing windows with POS

Every display type takes a `POS left top` keyword on its creation line, giving the
window's position on the host screen in pixels (default `0, 0`). With more than one
window open, set `POS` on each so they do not stack on top of each other. In the
example above, `Wave` sits at the top-left corner and `Status` sits 420 pixels to
its right — clear of a 400-pixel-wide SCOPE.

> Two host-wide offsets shift *all* displays together: the `DEBUG_DISPLAY_LEFT` and
> `DEBUG_DISPLAY_TOP` symbols add to every window's `POS` coordinates. Set them in a
> `CON` block when you want to nudge the whole arrangement without editing each
> `POS`. They default to `0`.

If you declare several windows **without** `POS`, `pnut_term_ts` places them for
you — it offsets each new window from the base display position rather than opening
them all on top of each other. That is enough to get started, but the arrangement is
automatic, not one you chose. To capture a layout you *do* like, **drag a window**:
while you move it, its title bar shows the window's current `left,top` in pixels.
Read those numbers off and encode them into `POS` on that window's creation line,
and your chosen arrangement reappears on every run.

### Feeding each window in your loop

Once the windows exist, you feed them by name, one statement at a time. A loop that
drives both is just both feeds in sequence:

```{.spin2 caption="ch14-multiwindow.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | ang, sine, count
  ' Two independent windows, each created by name and placed with POS.
  debug(`SCOPE Wave POS 0 0 SIZE 400 200 'Sine' -1000 1000)
  debug(`TERM Status POS 420 0 SIZE 40 10)

  ang := 0
  count := 0
  repeat
    sine := qsin(1000, ang, 256)         ' CORDIC sine, software-generated

    debug(`Wave `(sine))                 ' feed the SCOPE by its name
    debug(`Status 0 'Sample `(count)' 13 'Value:  `(sine)' 13)

    ang += 4
    count += 1
    waitms(10)
```

This opens a scrolling oscilloscope trace alongside a text panel that reprints the
sample count and the current value on every pass. Each `DEBUG` statement names its
target; nothing about the SCOPE feed affects the TERM feed or vice versa.

## Coordinating windows is just your code

There is **no cross-window *interaction***. Nothing you send to one window changes
what another shows, and there is no wildcard "all windows" target, no
synchronization group, no shared timestamp, no overlay or picture-in-picture
between windows. What you *can* do is address several windows by name in a single
feed (below); beyond that, the parser routes each backtick statement to the window
names it carries, and that is the whole model.

What looks like coordination is simply your program feeding related data to several
windows in the same loop. If you want the SCOPE and the TERM to show the same
moment, you send to both in the same iteration — as the example above does. The
"synchronization" is the structure of your loop, not a feature of the windows.

Sending one piece of data to several windows *does* have a built-in shortcut: list
more than one instance name after the backtick, and the same elements go to all of
them in a single statement. This works when the windows interpret the data the same
way — typically windows of the same type, or a shared directive such as `CLEAR` or
`SAVE`:

```spin2
debug(`ScopeA ScopeB `(sample))    ' same sample to both SCOPEs
debug(`ScopeA ScopeB CLEAR)        ' one CLEAR clears both
```

When the windows need *different* data — a raw sample to a SCOPE and a formatted
line to a TERM — there is no fan-out; you write each feed yourself, in the same loop
iteration so they show the same moment:

```spin2
debug(`Wave `(sine))                    ' the SCOPE gets the sample
' the TERM gets the same value, formatted
debug(`Status 'now: `(sine)' 13)
```

> **What does not exist.** There is no `TIMESTAMP`, `OVERLAY`, `ALL_WINDOWS`,
> `SYNC_GROUP`, `TRIGGER EXTERNAL`, or broadcast command, and no command that makes
> one window transparent over another. If you need timestamps in a log, format
> `GETCT()` yourself into a TERM feed; if you need two signals compared, put them on
> two channels of one SCOPE ([Chapter 7](#ch-7)) or use SCOPE_XY ([Chapter 8](#ch-8)). Coordination
> lives in your code.

> A separate, application-wide timestamp facility does exist: defining the
> `DEBUG_TIMESTAMP` symbol stamps every `DEBUG` *message* with the 64-bit CT
> value. That is a property of the message stream, set once in a `CON` block — not a
> command you send to a display window.

## Debugging from PASM

The `DEBUG` statement is available in PASM2 as well as Spin2. Inside cog assembly —
whether a standalone `DAT` program started with `COGINIT`, or an inline `ORG`/`END`
block inside a method — you write `debug(...)` with the same backtick display syntax
and the same output formatters you use in Spin2. The display windows do not know or
care which language fed them.

The difference is what the formatters read. In PASM, the values you display are
**cog registers** and immediates, named with PASM syntax. A register name feeds that
register's contents; the value forms (`` `() ``, `` `$() ``, `` `udec_() ``, and so
on) work exactly as in Spin2.

Here a PASM program running in its own cog drives a SCOPE window, feeding it the
value of a cog register:

```{.spin2 caption="ch14-pasm-scope.spin2"}
CON
  _clkfreq = 200_000_000

PUB main()
  coginit(COGEXEC_NEW, @blink, 0)  ' launch the PASM program in its own cog
  repeat                                  ' keep the Spin2 cog alive

DAT
              org
blink
              debug(`SCOPE Wave SIZE 400 200 'Ramp' 0 255)
.loop
              add       value, #4        ' advance a software ramp
              and       value, #$FF
              ' feed the window with the register's value
              debug(`Wave `(value))
              waitx     ##2_000_000
              jmp       #.loop

value         long      0
```

The cog creates the `Wave` window with its first `debug`, then feeds it one value
per loop. The window opens and animates identically to a Spin2-driven one.

Feeding a TERM from PASM works the same way. This cog reprints a register's value as
hex on a text panel:

```{.spin2 caption="ch14-pasm-terminal.spin2"}
CON
  _clkfreq = 200_000_000

PUB main()
  coginit(COGEXEC_NEW, @counter, 0)
  repeat

DAT
              org
counter
              debug(`TERM Mon SIZE 30 8)
.loop
              add       n, #1
              debug(`Mon 0 'count = `$(n)' 13)
              waitx     ##50_000_000
              jmp       #.loop

n             long      0
```

The same `DEBUG` also works in an **inline** `ORG`/`END` block inside a Spin2
method, where the assembly shares the method's local variables:

```{.spin2 caption="ch14-pasm-inline.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | x
  debug(`TERM Inline SIZE 30 6)
  x := 0
  repeat
    org
                add       x, #1
                debug(`Inline 0 'x = `(x)' 13)
    end
    waitms(500)
```

> **Pointers differ between Spin2 and PASM.** The interactive commands `PC_KEY` and
> `PC_MOUSE` ([Chapter 12](#ch-12)) take a pointer to a result buffer. In Spin2 that buffer is
> in hub, passed as `@key`; in PASM it must be a **cog register**, passed as `#key`.
> This is the one place the language changes the call, and it applies only to those
> input commands, not to the value formatters.

## Considerations

- **The debug link is shared by every window and every cog.** All `DEBUG` output —
  from all eight cogs, to all your windows — travels over one serial link, and the
  cogs time-share it through a hardware lock during their debug
  interrupts. There is no separate channel per window or per cog; everything is
  serialized onto the same wire and demultiplexed on the host by window name.

- **One shared link means you must pace your output.** Because every feed competes
  for that one link, the total rate across all windows and cogs is what matters, not
  the rate of any single window. Past some combined rate the link saturates and
  messages back up. With several windows updating in one loop, keep the loop's
  `waitms`/`waitx` generous enough that the combined traffic fits — tune it against
  your own serial baud rate and message sizes.

- **Slow a busy cog with `DLY`.** Adding `` `DLY `` (in Spin2) or `DLY(#ms)` (in
  PASM, where the millisecond count is an immediate) as the *last* item in a `DEBUG`
  statement delays that cog and releases the lock, letting other cogs get their
  messages onto the link. Use it when one cog would otherwise monopolize the output.

- **For high-rate data, pack it rather than sending faster.** When a single window
  needs more samples than the link comfortably carries one-at-a-time, the packed-data
  formats ([Chapter 13](#ch-13)) move many samples per `DEBUG` packet, which is the right tool
  before you reach for a faster loop.

- **There is no chip-side screenshot or export.** No `DEBUG` command captures the
  screen or exports a window from the chip. To save a single window's image, send
  that window's `` `SAVE `` command, which writes a `.bmp` on the host; capturing the
  whole screen is an action you take on the PC, outside the DEBUG system.

- **Use `` `SAVE `` to capture a window for documentation or a bug report.** Send
  `` `SAVE 'name' `` at the moment the display shows what you want to keep — for
  example after a trigger fires or an anomaly appears — and the host writes that frame
  to a file you can attach to notes or a report. It is the supported way to turn a live
  window into a static artifact.

- **Keep PASM `DEBUG` out of tight interrupt service routines.** A `DEBUG` taken
  inside an ISR can skew the cog's timing enough to disturb retriggering. Prefer
  doing `DEBUG` from cogs that are not running background ISRs (see the Spin2
  documentation on DEBUG and interrupts).

## Try it

Start from the two-window Spin2 example. Add a running peak: track the largest
magnitude the signal reaches and print it on the TERM alongside the current value,
so the SCOPE shows the waveform while the panel reports its numbers. The complete
program below compiles with `pnut_ts` and runs on a bare P2 board with `pnut_term_ts`
open — no wiring.

```{.spin2 caption="ch14-scope-trace.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | ang, signal, peak, count
  ' A SCOPE on the left, a TERM status panel on the right.
  ' Both are created up front, each by its own name, each placed with POS.
  debug(`SCOPE Trace POS 0 0 SIZE 400 220 SAMPLES 256 'Signal' -1000 1000)
  debug(`TERM Panel POS 420 0 SIZE 32 8)

  ang   := 0
  peak  := 0
  count := 0

  repeat
    signal := qsin(1000, ang, 256)         ' software-generated waveform
    if abs signal > peak
      peak := abs signal                   ' track the running peak

    ' Coordination is nothing more than feeding both windows
    ' in the same loop:
    debug(`Trace `(signal))                ' one sample to the SCOPE
    debug(`Panel 0 'Samples: `(count)' 13 ...
          'Current: `(signal)' 13 ...
          'Peak:    `(peak)' 13)  ' a fresh status block to the TERM

    ang   += 4
    count += 1
    waitms(10)
```

Then move the work into a cog: start a PASM program with `COGINIT` that generates the
ramp and feeds the SCOPE itself, and leave the Spin2 cog to print status to the TERM.
You will be driving two windows from two cogs over the one shared link — and the only
"coordination" anywhere is that both cogs are feeding windows you named.
