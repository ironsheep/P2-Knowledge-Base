# Chapter 12: Bidirectional Control — Keyboard and Mouse {#ch-12}

Every chapter so far has sent data one way: your P2 produces output, a DEBUG
display window shows it. This chapter reverses the direction. Using two commands —
`PC_KEY` and `PC_MOUSE` — your running program reads the host PC's keyboard and
mouse back through the same debug link, so the window you opened for output
becomes a control surface as well.

The mechanism is shared. `PC_KEY` and `PC_MOUSE` work on any display window — TERM,
PLOT, SCOPE, BITMAP, all of them — because you address the input to a window by
name and the host reports the state of that window. The window must have focus for
input to be noticed: keypresses and wheel events go to whichever window the host
user has clicked into.

Both commands follow the same shape: you pass a **pointer to a buffer in hub RAM**,
and the host writes the current input state into that buffer. They do not return a
value. You read the result afterward from the variable you pointed at:

```spin2
PUB main() | key, mouse[7]
  debug(`TERM Console SIZE 40 10)

  debug(`Console PC_KEY(@key))            ' host writes key code into key

  debug(`Console PC_MOUSE(@mouse))        ' host fills 7 longs

  repeat
```

One rule governs both: **`PC_KEY` and `PC_MOUSE` must be the last command in their
`DEBUG()` statement.** You can send output earlier in the same statement, but the
input command comes last. In Spin2 the buffer lives in hub RAM, so you pass its
address with `@` — `@key`, `@mouse`. (In PASM the buffer is a cog register and you
pass it with `#`; this chapter is Spin2.)

## PC_KEY — reading the keyboard

`PC_KEY(pointer_to_long)` takes the address of a single long. The host writes the
most recent keypress that occurred within the last 100 ms into that long, and
writes **0 when no key was pressed**. It is not a function that returns the key —
this is wrong:

```spin2
' WRONG - PC_KEY does not return a value
key := debug(`Console PC_KEY)
```

The correct form passes a pointer and then reads the long:

```spin2
debug(`Console PC_KEY(@key))   ' host fills key
case key                        ' now read it
  ...
```

The window must have focus for the keypress to be seen. Because the host reports
the keypress from the last 100 ms, poll at least that often if you do not want to
miss keys.

### Key codes

The long holds one of these values. Printable characters arrive as their ASCII
code; a small set of navigation and editing keys arrive as low codes:

| Code | Key | Code | Key |
|------|-----|------|-----|
| `0` | no keypress | `8` | Backspace |
| `1` | Left Arrow | `9` | Tab |
| `2` | Right Arrow | `10` | Insert |
| `3` | Up Arrow | `11` | Page Up |
| `4` | Down Arrow | `12` | Page Down |
| `5` | Home | `13` | Enter |
| `6` | End | `27` | Esc |
| `7` | Delete | `32`–`126` | Space through `~` (all symbols, digits, letters) |

That is the complete list the source defines. The four arrows are `1`–`4` — not
`$C2`/`$C3` or any other encoding. There are no function-key codes and no modifier
state: `PC_KEY` reports a single key per poll, with no separate Shift / Ctrl / Alt
flags. A capital `A` arrives as code 65 and a lowercase `a` as 97, but you cannot
read "Ctrl is held" independently of a key.

### Example: arrow keys adjust a value

This program opens a TERM window and lets the arrow keys nudge a number up and
down. Up/Down change it by one; Left/Right by ten. The value is redrawn only when a
key is actually pressed:

```spin2
CON _clkfreq = 200_000_000

PUB main() | key, value
  debug(`TERM Adjust SIZE 32 6 TITLE 'Arrow Keys Adjust')
  value := 50
  show(value)
  repeat
    key := 0
    debug(`Adjust PC_KEY(@key))
    case key
      3: value += 1                       ' Up arrow
      4: value -= 1                       ' Down arrow
      1: value -= 10                      ' Left arrow
      2: value += 10                      ' Right arrow
    if key
      show(value)
    waitms(20)

PRI show(v)
  debug(`Adjust 0 "Value: " `sdec_(v) 13 "Up/Down +/-1, Left/Right +/-10")
```

Click the window to give it focus, then press the arrow keys. Each `case` arm acts
on one key code; the `if key` guard skips the redraw on the polls where no key
arrived (`key` is 0). The `key := 0` at the top of each pass clears the variable so
a stale value is never re-acted on.

## PC_MOUSE — reading the mouse

`PC_MOUSE(pointer_to_7_longs)` takes the address of a **seven-long array**. The
host fills all seven with the current mouse state relative to the named window.
Declare the buffer as `long mouse[7]` and pass `@mouse`:

```spin2
debug(`Watch PC_MOUSE(@mouse))
```

The seven longs, in order, are:

| Index | Field | Meaning |
|-------|-------|---------|
| `mouse[0]` | xpos | X position within the window. **Negative if the mouse is outside the window** (both xpos and ypos go negative together). |
| `mouse[1]` | ypos | Y position within the window. |
| `mouse[2]` | wheel delta | Scroll-wheel change: `0`, or `+1` / `-1` when the wheel moved. The window must have focus. |
| `mouse[3]` | left button | `0` released, `-1` pressed. |
| `mouse[4]` | middle button | `0` released, `-1` pressed. |
| `mouse[5]` | right button | `0` released, `-1` pressed. |
| `mouse[6]` | pixel | Color at the mouse position, `$00_RR_GG_BB`, or `-1` if the mouse is outside the window. |

The position units depend on the window type — for a TERM window they are character
column and row; for pixel-based windows like BITMAP they are pixels. (See the per-
window hover-coordinate behavior in each window's chapter.)

**Buttons are a full-long state, not a bitmask.** Each button long is either `0`
(released) or `-1` (pressed). Test it directly — `if mouse[3]` is true when the left
button is down. Do not mask it:

```spin2
' WRONG - buttons are 0 / -1, not packed bits
if mouse[3] & 1
```

```spin2
' CORRECT
if mouse[3]
```

Because `-1` is all bits set, a bit test happens to work for the low bit, but it
misrepresents the data and is not how the host reports it. Treat each long as a
boolean state of one button.

Detect "outside the window" with the position: `mouse[0]` (and `mouse[1]`) go
negative when the pointer leaves the window, and `mouse[6]` is `-1` in that case
too.

### Example: read mouse position and buttons

This program continuously displays the mouse state in a TERM window, clearing and
redrawing each pass:

```spin2
CON _clkfreq = 200_000_000

PUB main() | mouse[7]
  debug(`TERM Pointer SIZE 40 8 TITLE 'Mouse State')
  repeat
    debug(`Pointer PC_MOUSE(@mouse))
    debug(`Pointer 0)                                 ' clear + home
    if mouse[0] < 0
      debug(`Pointer "Pointer outside window" 13)
    else
      debug(`Pointer "X: " `sdec_(mouse[0]) "  Y: " `sdec_(mouse[1]) 13)
      debug(`Pointer "Wheel: " `sdec_(mouse[2]) 13)
      debug(`Pointer "Buttons  L:" `sdec_(mouse[3]))
      debug(`Pointer "  M:" `sdec_(mouse[4]) "  R:" `sdec_(mouse[5]) 13)
      debug(`Pointer "Pixel: " `uhex_long_(mouse[6]))
    if mouse[3]                                        ' left button down?
      debug(`Pointer 13 "LEFT DOWN")
    waitms(30)
```

Move the mouse over the window and the position updates; move outside and the
program reports it from the negative `xpos`. Press the left button and the buttons
read `-1` (shown as `-1` by `` `sdec_ ``), and the `LEFT DOWN` line appears.

### Where you'd use this

In computer science and computer engineering, host input turns a DEBUG display
window into a **human-in-the-loop control surface** — interactive parameter adjustment and
manual test rigs you drive by hand while the program runs.

**On an embedded project**, you reach for it to tune PID gains live, to nudge a
setpoint, to jog an actuator by hand, or to trigger and label a calibration
capture — all without recompiling, using the host keyboard and mouse as a temporary
control panel.

**Bandwidth fit:** input is polled a few tens of times a second; it is negligible
against the link budget.

**Extension (real hardware):** the same `PC_KEY` / `PC_MOUSE` polling that reads the
host here can hand its values to real outputs — drive a smart-pin PWM from a tuned
gain, step a motor from an arrow key — turning the panel into live control.

## Considerations

- **The model is polling, not interrupts.** Nothing is pushed to your program; you
  ask for the current state each time you issue `PC_KEY` / `PC_MOUSE`. Build the
  command into your loop and poll at a steady rate.
- **`PC_KEY` reports keys from the last 100 ms.** Poll at least every 100 ms or you
  can miss a keypress. The examples here poll far faster than that.
- **One key per poll, no modifier state.** `PC_KEY` returns a single code; there is
  no separate Shift / Ctrl / Alt status and no way to read two keys held together.
  Design around single-key input.
- **Buttons and "outside" are sentinel values, not flags.** Buttons are `0` / `-1`;
  position goes negative and `pixel` becomes `-1` when the pointer leaves the
  window. Test these as whole-long states.
- **Must be the last command in the `DEBUG()` statement.** Put any output earlier;
  end the statement with the input command.
- **Focus matters.** The host user must click the window to give it focus before
  keypresses and wheel deltas register. The window name in the command selects
  *which* window's input you read.

## Try it

Start from the mouse example and turn the window into a click target: when
`mouse[3]` goes from `0` to `-1` (a press edge — track the previous value in a
variable so you fire once per click, not every poll), increment a counter and show
it. Then combine both commands in one loop: poll `PC_KEY` to reset the counter on
Esc (code 27) and `PC_MOUSE` to count clicks. You will have a single window that
reads both input devices, using nothing but the debug link and a bare P2 board.
