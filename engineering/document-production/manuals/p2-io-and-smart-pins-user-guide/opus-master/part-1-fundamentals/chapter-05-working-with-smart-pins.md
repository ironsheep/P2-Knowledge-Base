# Chapter 5: Working with Smart Pins {#ch5}

This chapter covers practical patterns for smart pin operation, debugging techniques, and common troubleshooting scenarios. The concepts here apply across all smart pin modes documented in Parts II through IV.


## 5.1 The Read/Acknowledge Cycle

### How IN and Acknowledge Work

When a smart pin event occurs (measurement complete, data ready, etc.), the smart pin raises its IN flag. This signals to cogs that attention is needed.

**Acknowledging instructions** (WRPIN, WXPIN, WYPIN, RDPIN, AKPIN) lower the IN flag, signaling to the smart pin that the event was handled. This allows IN to be raised again for the next event.

**Non-acknowledging read** (RQPIN) reads the result without lowering IN.

### Polling Patterns

**Check-then-read (recommended):**
```spin2
repeat
  if PINREAD(pin) == 1                    ' IN high?
    result := RDPIN(pin)                  ' Read and acknowledge
    ' Process result
```

```pasm2
.loop         testp     #pin wc           ' Check IN
        if_nc jmp       #.loop            ' Wait if low
              rdpin     result, #pin      ' Read and acknowledge
              ' Process result
              jmp       #.loop
```

**Blocking wait (PASM2):**
```pasm2
              testp     #pin wc           ' Check IN
        if_nc jmp       #$-1              ' Tight loop until high
              rdpin     result, #pin      ' Read result
```

**Time-limited wait:**
```spin2
start := GETCT()
repeat until PINREAD(pin) == 1 or (GETCT() - start) > timeout
if PINREAD(pin) == 1
  result := RDPIN(pin)
else
  ' Handle timeout
```

### Waiting Strategies

Every pattern above keeps the cog **executing** — the poll-spin loops on `TESTP`/`PINREAD`, and the time-limited wait re-reads `GETCT()` on each pass. That burns instruction cycles (and power) for the whole wait. When a cog has nothing to do until the smart pin is ready, the P2's event system offers a true **stall**: the cog halts and resumes the instant the pin acts. These are PASM2 patterns; Spin2 code reaches them through inline PASM.

**Blocking wait via the event system (the true stall).** A selectable event (SE1–SE4, four per cog) can watch a pin's IN flag. `SETSE1` arms it for the rising edge of IN; `WAITSE1` then halts the cog — no instructions execute — until that edge occurs:

```pasm2
              setse1    #%001<<6 + pin    ' Arm SE1 on IN rising edge
.wait
              waitse1                     ' Cog halts until IN rises
              rdpin     result, #pin      ' Read + ack (lowers IN)
              jmp       #.wait
```

`WAITSE1` auto-clears the SE1 flag as it releases, so the next `WAITSE1` waits for the next edge. An acknowledging read (`RDPIN`) is still required to retrieve the result and lower IN. The four slots are independent, letting one cog track up to four sources — but each `WAITSE` waits on exactly one.

**Wait with a timeout (never hang).** `WAITSE1` stalls *indefinitely* — if the smart pin never completes, the cog never wakes. To bound the wait, race the pin event against the system counter. No single instruction waits on an event *and* a timer at once, so poll both and branch on whichever fires first:

```pasm2
              getct     deadline          ' Read current time
              addct1    deadline, ##timeout   ' Deadline = now + wait
              setse1    #%001<<6 + pin    ' Arm SE1 on IN rising edge
.race
              pollse1   wc                ' Pin ready?
        if_c  jmp       #.ready           ' Yes - go read it
              pollct1   wc                ' Timeout reached?
        if_nc jmp       #.race            ' Neither yet - keep polling
              jmp       #.timedout        ' Timed out
.ready
              rdpin     result, #pin      ' Pin won the race
.timedout
              ' Handle the timeout
```

`ADDCT1` sets counter-comparator 1 to a deadline; `POLLCT1 WC` reports (and clears) whether that deadline has passed, exactly as `POLLSE1 WC` does for the pin event. This costs a few instructions per pass — more than a pure stall — but it can never hang. For background servicing, that same SE1 event can instead drive an interrupt (via `SETINT1`), freeing the cog to run other code between events.

**Let the smart pin time itself out.** Several input modes carry the timeout in hardware, removing the software race entirely. `P_EVENTS_TICKS` (mode `%10010`) with Y[2] = 1 raises IN either when the event arrives *or* after X clocks with no event (Chapter 13), so a single `WAITSE1` covers both outcomes — read the result, then decide whether it was a real event or a timeout. The windowed measurement modes (`%10101`–`%10111`, Chapter 15) instead raise IN after a fixed number of clocks, giving a "wait exactly this long, then read" cadence. When one of these fits, prefer it: the blend is done in silicon at zero cog cost.

### Checking Without Clearing

To inspect the IN state without affecting it:
```spin2
state := PINREAD(pin)                  ' Just checks, doesn't acknowledge
```

```pasm2
              testp     #pin wc           ' Checks IN, no acknowledge
```

To read the Z value without acknowledging:
```spin2
value := RQPIN(pin)                       ' Read quietly
```

### The 2-Clock Delay

After acknowledging, wait 2 clocks before polling IN again:
```pasm2
              rdpin     result, #pin      ' Acknowledge
              nop                         ' Wait 2 clocks (NOP = 2 clocks)
              testp     #pin wc           ' Safe to poll
```

Processing between reads provides sufficient delay.


## 5.2 Continuous vs One-Shot Modes

### Continuous Modes

These modes run indefinitely once enabled, producing periodic output or ongoing measurements:

| Mode | Behavior |
|------|----------|
| NCO Frequency/Duty | Runs continuously, IN raised on overflow |
| PWM Triangle/Sawtooth | Runs continuously, IN raised each frame |
| Quadrature Encoder | Runs continuously (or periodically with X>0) |
| Counter modes (X=0) | Totalizer mode, counts indefinitely |
| ADC modes | Samples continuously at configured rate |

**Using continuous modes:**

- Configure once
- Read results as needed (RDPIN/RQPIN)
- Update parameters anytime (WYPIN for new values)
- Mode runs until DIR cleared or reconfigured

### Periodic Modes

These modes repeat automatically but generate periodic events:

| Mode | Period Control |
|------|----------------|
| Counter modes (X>0) | X defines measurement window |
| Period measurement | X defines number of periods |
| Serial TX/RX | Operates per data word |

**Using periodic modes:**

- Each period, IN is raised
- RDPIN retrieves period result and starts next period
- Missing reads can cause data loss (results overwritten)

### One-Shot Modes

These modes complete a defined action then stop:

| Mode | Behavior |
|------|----------|
| Pulse/Cycle Output | Outputs Y pulses, then stops |
| Transition Output | Outputs Y transitions, then stops |

**Using one-shot modes:**

- Configure and enable
- Wait for IN (operation complete)
- Write new Y value to restart
- Or reconfigure for new parameters

**Restarting one-shot:**
```spin2
' Wait for completion
repeat until PINREAD(pin) == 1
result := RDPIN(pin)                      ' Acknowledge

' Start new operation
WYPIN(pin, new_count)                     ' New Y value triggers restart
```


## 5.3 Multi-Pin Patterns

### Configuring Pin Groups

Use pin ranges for identical configuration:
```spin2
' Configure pins 0-7 for PWM
WRPIN(0..7, P_PWM_TRIANGLE | P_OE)
WXPIN(0..7, base_period | (frame << 16))
PINLOW(0..7)

' Set individual duty cycles
WYPIN(0, duty_0)
WYPIN(1, duty_1)
' ...
```

```pasm2
              setq      #7                ' 8 pins
              wrpin     ##(P_PWM_TRIANGLE | P_OE), #0
              setq      #7
              wxpin     x_value, #0
              setq      #7
              drvl      #0                ' Enable all 8
```

### Relative Pin Addressing

Smart pins can use adjacent pins for input:

**Quadrature encoder (A on pin N, B on pin N+1):**
```spin2
WRPIN(encoder_pin, P_QUADRATURE | P_PLUS1_B)
```

**Synchronous serial (data on pin N, clock on pin N+1):**
```spin2
WRPIN(data_pin, P_SYNC_RX | P_PLUS1_B)
```

**Comparator (compare pin N to pin N+1):**
```spin2
WRPIN(comp_pin, P_COMPARE_AB | P_PLUS1_B)
```

### Synchronized Multi-Pin Output

For phase-synchronized outputs (audio, motor control):

1. Configure all pins with same base period
2. Use NCO mode with appropriate phase offsets in X[31:16]
3. Enable all simultaneously

```spin2
' Three-phase motor control
WRPIN(phase_a, P_NCO_FREQ | P_OE)
WRPIN(phase_b, P_NCO_FREQ | P_OE)
WRPIN(phase_c, P_NCO_FREQ | P_OE)

' Same frequency, different phases (0°, 120°, 240°)
WXPIN(phase_a, 1 | (0 << 16))             ' Phase = 0
WXPIN(phase_b, 1 | (21845 << 16))         ' Phase ≈ 120°
WXPIN(phase_c, 1 | (43690 << 16))         ' Phase ≈ 240°

' Same frequency value
WYPIN(phase_a, freq_value)
WYPIN(phase_b, freq_value)
WYPIN(phase_c, freq_value)

' Drive all pins low simultaneously for coordinated startup
PINLOW(phase_a..phase_c)
```

### Multi-Cog Access

When multiple cogs need the same smart pin data:

**Pattern: One owner, multiple observers**
```pasm2
' Cog 0 - Owner (uses RDPIN)
              testp     #sensor wc
        if_c  rdpin     result, #sensor   ' Read and acknowledge

' Cog 1..N - Observers (use RQPIN)
              rqpin     result, #sensor   ' Read without acknowledge
```

The owner controls the timing; observers passively read.


## 5.4 PINSTART and PINCLEAR

### PINSTART - One-Call Configuration

PINSTART combines WRPIN, WXPIN, WYPIN, and enable into one call:

```spin-syntax
PINSTART(Pin, Mode, Xval, Yval)
```

**Example:**
```spin2
' Instead of:
PINFLOAT(pin)
WRPIN(pin, P_NCO_FREQ | P_OE)
WXPIN(pin, 1)
WYPIN(pin, freq)
PINLOW(pin)

' Use:
PINSTART(pin, P_NCO_FREQ | P_OE, 1, freq)
```

### When PINSTART Helps

- Quick setup of known configurations
- Reducing code size
- Prototyping

### When to Use Raw Configuration

- Mode doesn't need all three registers
- Partial reconfiguration (WYPIN alone, for example)
- Precise control over enable timing
- PASM2 code (PINSTART is Spin2 only)

### PINCLEAR - Reset to Normal

`PINCLEAR(pin)` disables smart pin mode and returns the pin to Direct I/O — equivalent to `PINFLOAT(pin)` followed by `WRPIN(pin, 0)`. See §4.14 for the complete reset-to-normal reference.


## 5.5 Debugging Smart Pins

### Verifying Configuration

**Check that mode is active:**
```spin2
' After configuration, wait for first IN
repeat 1000                               ' Timeout after many loops
  if PINREAD(pin) == 1
    result := RDPIN(pin)
    DEBUG("Smart Pin active, first result: ", UDEC_(result))
    quit
DEBUG("Smart Pin not responding")
```

**Inspect Z register:**
```spin2
value := RQPIN(pin)                       ' Read without disturbing
DEBUG("Z register: ", UHEX_(value))
```

### Common Configuration Errors

**No output (output modes):**

- Missing P_OE in WRPIN
- DIR still low (not enabled)
- WRPIN value has wrong mode bits

**No events (IN never goes high):**

- Mode not enabled (DIR=0)
- X register has invalid period (0 when period required)
- Mode waiting for input that isn't present

**Wrong timing:**

- X register calculation error
- Using wrong clock frequency assumption
- Frame period vs base period confusion

**Erratic behavior:**

- Configured while DIR=1 (should configure while DIR=0)
- Multiple cogs acknowledging same pin
- X or Y values out of valid range

### Debugging Checklist

1. **Is DIR=1?** - Smart pin must be enabled
2. **Is P_OE included?** - Required for output modes
3. **Is mode correct?** - Verify mode bits in WRPIN value
4. **Is X valid?** - Check period/parameter calculations
5. **Was configured while reset?** - DIR should be 0 during WRPIN
6. **Is input present?** - For input modes, verify signal at pin

### Using Scope/Logic Analyzer

For timing issues:

1. Capture the pin output
2. Verify frequency/period matches expectations
3. Check for glitches during configuration
4. Verify phase relationships in multi-pin setups


## 5.6 Performance Considerations

### Instruction Timing

| Instruction | Cycles |
|-------------|--------|
| WRPIN/WXPIN/WYPIN | 2 |
| RDPIN/RQPIN | 2 |
| AKPIN | 2 |
| TESTP/TESTPN | 2 |

### Configuration Overhead

Full configuration (DIRL + WRPIN + WXPIN + WYPIN + DRVL) = 10 cycles.

For frequently-reconfigured modes, consider:

- Just updating Y (WYPIN) when only output value changes
- Using reset (DIRL + DRVL = 4 cycles) instead of full reconfig

### Read Overhead

RDPIN every event: 2 cycles + polling overhead.

For high-frequency events:

- Use larger measurement windows (X register)
- Read less frequently
- Some events are lost when results are overwritten before they are read

### When Overhead Matters

- Events faster than ~10 MHz at 200 MHz sysclk
- Tight timing loops
- Multiple smart pins requiring attention

### When Overhead is Negligible

- Events slower than 1 MHz
- Occasional configuration changes
- Asynchronous operation (smart pin runs independently)


## 5.7 Troubleshooting Quick Reference

### "Pin Not Responding"

| Check | Action |
|-------|--------|
| DIR state | Ensure DRVL/DRVH/PINLOW was executed after configuration |
| WRPIN value | Verify mode bits are correct (%SSSSS field) |
| Pin number | Confirm correct pin in all instructions |
| Cog conflict | Check if another Cog is controlling the pin |

### "No Output"

| Check | Action |
|-------|--------|
| P_OE | Add P_OE to WRPIN value for output modes |
| Drive strength | Ensure not set to P_HIGH_FLOAT / P_LOW_FLOAT |
| Mode requires Y | Some modes need WYPIN before output starts |
| Reset during config | Configure with DIR=0, then enable |

### "Wrong Frequency/Timing"

| Check | Action |
|-------|--------|
| X register | Verify base period calculation |
| Y register | For NCO, verify frequency calculation |
| Clock frequency | Confirm _clkfreq matches actual clock |
| Frame vs base | X[31:16] is frame, X[15:0] is base |

### "Events Too Fast/Slow"

| Check | Action |
|-------|--------|
| Measurement window | X register sets window for counter modes |
| Sample period | Check ADC sample rate setting |
| Base period | NCO/PWM timing derived from base period |

### "IN Never Goes High"

| Check | Action |
|-------|--------|
| Mode enabled | DIR must be 1 |
| Input present | For input modes, verify signal at pin |
| X = 0 issue | Some modes need X > 0 to generate events |
| Acknowledge timing | Wait 2 clocks after acknowledge before polling |

### "Data Corrupted/Wrong"

| Check | Action |
|-------|--------|
| Read timing | Read before next event overwrites result |
| Bit width | Ensure Z interpretation matches mode |
| C flag | Some modes put extra data in C flag |
| Multi-Cog | Only one Cog should RDPIN; others use RQPIN |

### "Works Then Stops"

| Check | Action |
|-------|--------|
| One-shot mode | May need WYPIN to restart |
| Y exhausted | Pulse/Transition modes count down Y |
| Buffer overflow | Reading too slowly loses data |


## 5.8 Best Practices Summary

### Configuration

1. Always configure while DIR=0 (reset state)
2. Include P_OE for output modes
3. Verify calculations for X and Y values
4. Enable last (DRVL/DRVH after WRPIN/WXPIN/WYPIN)

### Operation

1. Poll IN before reading (avoid unnecessary reads)
2. Use RQPIN for observers, RDPIN for owner
3. Update Y for new output values (don't reconfigure)
4. Reset (DIRL + DRVL) is faster than reconfigure

### Multi-Pin

1. Use pin ranges for identical configurations
2. Enable simultaneously for synchronization
3. Use relative addressing for related pins
4. Designate one cog as owner for shared pins

### Debugging

1. Start simple - verify basic operation first
2. Check DIR and P_OE before investigating further
3. Use RQPIN to inspect without disturbing
4. Verify calculations independently


*This chapter completes Part I: Fundamentals. For specific smart pin mode documentation, proceed to Part II (Output Modes), Part III (Input Modes), or Part IV (Special Modes).*
