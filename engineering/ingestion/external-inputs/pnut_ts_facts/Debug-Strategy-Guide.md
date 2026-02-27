# Debug Strategy Guide: Managing the 255-Record Limit

This guide helps you choose the right debug strategy for your Spin2/PASM2 project. It contrasts the available debug mechanisms, explains when to use each, and shows how they work together to keep you within the P2's hard limit of 255 unique debug records.

For detailed syntax and configuration reference, see [DEBUG-MASK-Usage-Guide.md](DEBUG-MASK-Usage-Guide.md).

---

## The Problem: Why You Need a Strategy

Every `debug()` statement that compiles into your program consumes a **debug record slot**. The P2 debug system has three hard limits:

| Limit | Value | What It Means |
|-------|-------|---------------|
| **Unique debug records** | **255 max** | Each distinct `debug()` call uses one slot |
| **Single record size** | 255 bytes | One debug statement can't exceed 255 bytes of encoded data |
| **Total debug data** | 16 KB | All debug records combined can't exceed 16,384 bytes |

The 255-record limit is the one you'll hit first in any non-trivial project. A robotics application with sensor reads, motor control, communication, and error handling can easily have 300+ debug statements scattered across its source files.

**Key insight:** The compiler deduplicates identical debug records. Two calls to `debug("hello")` in different places share one slot. But `debug("hello A")` and `debug("hello B")` each consume their own slot.

---

## The Mechanisms at a Glance

The P2 debug system gives you tools at three levels. Only the **compile-time** tools reduce your record count:

| Mechanism | Level | Reduces Record Count? | Granularity |
|-----------|-------|-----------------------|-------------|
| `-d` compiler flag | Compile-time | Yes (all or nothing) | Global |
| `DEBUG_DISABLE` | Compile-time | Yes (all or nothing) | Global (per source file) |
| `DEBUG_MASK` + `debug[N]()` | Compile-time | **Yes (selective)** | Per channel (32 channels) |
| `DEBUG_COGS` | Runtime | No | Per cog |
| `debug IF()` / `IFNOT()` | Runtime | No | Per statement |

**Runtime mechanisms still compile the debug record and consume a slot.** They only suppress *output* at execution time. For staying within 255 records, only compile-time mechanisms matter.

---

## Mechanism 1: The `-d` Compiler Flag

### What it does

The `-d` (or `--debug`) flag is the master switch. Without it, **zero** debug records are compiled regardless of anything else in your source.

### When to use it

- **Always required** to enable any debug output
- Omit it for final production builds to guarantee zero debug overhead

### Record impact

| Flag | Records consumed |
|------|-----------------|
| No `-d` | 0 |
| `-d` | Up to 255 (depends on source) |

### Example

```bash
# Development: debug enabled
pnut-ts -d myapp.spin2

# Production: no debug code at all
pnut-ts myapp.spin2
```

---

## Mechanism 2: `DEBUG_DISABLE`

### What it does

`DEBUG_DISABLE` is a source-level kill switch. When set to any non-zero value, **all** debug statements are excluded from compilation, even when building with `-d`.

### When to use it

- **Release builds from source**: Toggle between debug and release without changing the build command
- **Library/object files**: Disable debug in a child object so its debug statements don't count against the parent's 255-record budget
- **Quick toggling**: Faster than editing a build script; change one constant and recompile

### Record impact

| Setting | Records consumed |
|---------|-----------------|
| `DEBUG_DISABLE = 0` (or not defined) | Normal compilation |
| `DEBUG_DISABLE = 1` (any non-zero) | **0 records** |

### Example

```spin2
CON
  RELEASE = 0                   ' Change to 1 for release
  DEBUG_DISABLE = RELEASE

PUB main()
  debug("Starting up")          ' Compiled only when RELEASE = 0
  debug("Sensor: ", UDEC(val))  ' Compiled only when RELEASE = 0
```

### Strength

Global, zero-effort elimination of all debug code. One constant controls everything.

### Limitation

All-or-nothing. You can't keep error messages while removing verbose tracing.

---

## Mechanism 3: `DEBUG_MASK` + `debug[N]()` (Selective Channels)

### What it does

`DEBUG_MASK` is a 32-bit constant where each bit enables a debug "channel" (0-31). Debug statements written as `debug[N](...)` are only compiled if bit N is set in the mask. **Disabled channels consume zero records.**

**Requires:** `{Spin2_v46}` or later version directive.

### When to use it

- **Large projects** approaching the 255-record limit
- **Multi-subsystem projects** where you only need to debug one area at a time
- **Verbosity control** where you want errors always visible but trace messages optional
- **Team projects** where different developers debug different subsystems

### Record impact

Only channels with their bit set in `DEBUG_MASK` generate records. Channels with cleared bits produce **zero code and zero records**.

| Scenario (assume 80 debug stmts per channel) | Mask | Records |
|-----------------------------------------------|------|---------|
| All 4 channels enabled | `%1111` | ~320 (would FAIL) |
| Only 2 channels enabled | `%0101` | ~160 |
| Only errors enabled | `%0001` | ~80 |
| All channels disabled | `%0000` | 0 (but regular `debug()` still compiles) |

### Example: Channel-per-subsystem

```spin2
{Spin2_v46}
CON
  ' Channel assignments (document these!)
  CH_ERROR  = 0                 ' Error reporting
  CH_MOTOR  = 1                 ' Motor control
  CH_SENSOR = 2                 ' Sensor readings
  CH_COMM   = 3                 ' Communication

  ' === CHANGE THIS LINE TO CONTROL WHAT COMPILES ===
  DEBUG_MASK = (1 << CH_ERROR) | (1 << CH_SENSOR)   ' Only errors + sensors

PUB main() | sensorVal, motorSpeed
  debug[CH_ERROR]("System OK")                       ' COMPILED (bit 0 set)
  debug[CH_SENSOR]("Temp: ", SDEC(sensorVal))        ' COMPILED (bit 2 set)
  debug[CH_MOTOR]("Speed: ", UDEC(motorSpeed))       ' SKIPPED (bit 1 clear)
  debug[CH_COMM]("Packet TX")                        ' SKIPPED (bit 3 clear)
```

### Example: Verbosity levels

```spin2
{Spin2_v46}
CON
  LVL_ERROR = 0
  LVL_WARN  = 1
  LVL_INFO  = 2
  LVL_TRACE = 3

  VERBOSITY = 1                 ' Show errors and warnings only
  DEBUG_MASK = (1 << (VERBOSITY + 1)) - 1   ' = %11

PUB main()
  debug[LVL_ERROR]("Fatal: null pointer")       ' COMPILED
  debug[LVL_WARN]("Buffer 90% full")            ' COMPILED
  debug[LVL_INFO]("Processing record 42")       ' SKIPPED
  debug[LVL_TRACE]("Entering subroutine X")     ' SKIPPED
```

### Strength

**Surgical control.** You pick exactly which categories of debug code compile. Disabled channels have zero overhead and consume zero records. You can bring a 400-statement project down to 80 compiled records by enabling only the channels you need right now.

### Limitation

Requires upfront planning. You must assign channels when writing debug statements and use the `debug[N]()` syntax. Regular `debug()` statements are unaffected by the mask and always compile.

---

## Important: Regular `debug()` Always Compiles

Standard `debug()` statements (without a channel number) are **not** controlled by `DEBUG_MASK`. They compile whenever `-d` is used and `DEBUG_DISABLE` is not set.

```spin2
CON
  DEBUG_MASK = 0                ' ALL channels disabled

PUB main()
  debug("I always compile")     ' YES - regular debug(), unaffected by mask
  debug[0]("I am disabled")     ' NO  - channel 0 is masked off
```

**Strategy tip:** Use regular `debug()` sparingly for critical always-on messages (boot confirmation, fatal errors). Use `debug[N]()` for everything else so you can control it with the mask.

---

## Runtime Mechanisms (Don't Reduce Record Count)

These are useful tools, but they **do not** help you stay within the 255-record limit because they still compile the debug record.

### `DEBUG_COGS` - Per-Cog Runtime Filtering

An 8-bit mask controlling which cogs can produce debug output at runtime. Useful for silencing noisy cogs without recompiling, but every debug statement on every cog is still compiled and still consumes a record slot.

```spin2
CON
  DEBUG_COGS = %00000001        ' Only cog 0 outputs debug
```

**Use for:** Reducing runtime debug noise in multi-cog applications.
**Does NOT help with:** The 255-record limit.

### `debug IF()` / `debug IFNOT()` - Conditional Output

Evaluates a condition at runtime and suppresses the debug output if the condition is false. The debug record is still compiled.

```spin2
PUB main() | errorCount
  debug IF(errorCount > 0)("Errors: ", UDEC(errorCount))   ' Always compiled, conditionally shown
```

**Use for:** Reducing runtime debug noise without recompiling.
**Does NOT help with:** The 255-record limit.

---

## Decision Flowchart: Which Mechanism to Use

```
Start: "I need debug output in my P2 project"
  │
  ├─ Project has < 100 debug statements?
  │   └─ YES → Use regular debug() everywhere. You're well within 255.
  │
  ├─ Project has 100-255 debug statements?
  │   └─ Use regular debug() but monitor your count.
  │       Consider debug[N]() for new subsystems so you can
  │       disable them later if you approach the limit.
  │
  ├─ Project has 255+ debug statements (or is growing toward it)?
  │   └─ USE DEBUG_MASK + debug[N](). Assign channels to subsystems.
  │       Enable only the channels you're actively debugging.
  │
  ├─ Shipping a release build?
  │   └─ Either omit -d flag, or set DEBUG_DISABLE = 1.
  │       Both produce zero debug overhead.
  │
  ├─ Writing a reusable object/library?
  │   └─ Use DEBUG_DISABLE in the object so its debug statements
  │       don't consume the parent project's record budget.
  │       Or use debug[N]() with documented channel assignments.
  │
  └─ Multi-cog project with too much debug output at runtime?
      └─ Use DEBUG_COGS to silence cogs you're not investigating.
          Use debug IF()/IFNOT() for conditional runtime filtering.
          (These don't reduce record count, only runtime output.)
```

---

## Deduplication: Free Savings

The compiler automatically deduplicates identical debug records. Two calls to the exact same debug statement share one record slot:

```spin2
PUB main()
  debug("tick")                 ' Slot 1
  waitms(100)
  debug("tick")                 ' Reuses slot 1 (identical content)
  waitms(100)
  debug("tock")                 ' Slot 2 (different content)
```

This means:
- Repeated identical debug statements in a loop cost only **one** slot
- But `debug("val=", UDEC(x))` and `debug("val=", UDEC(y))` are different records (different variable references) and each consume a slot

**Strategy tip:** If you have debug statements inside frequently-called methods, the deduplication handles it automatically. You don't need to worry about loops or repeated calls inflating your record count.

---

## Putting It All Together: Recommended Project Setup

### Small project (< 100 debug statements)

```spin2
CON
  _clkfreq = 200_000_000

PUB main()
  debug("System starting")
  debug("Sensor: ", SDEC(readSensor()))
  ' Just use regular debug() everywhere. Simple and effective.
```

### Medium project (100-200 debug statements)

```spin2
{Spin2_v46}
CON
  _clkfreq = 200_000_000

  ' Channel assignments
  CH_MAIN   = 0
  CH_SENSOR = 1
  CH_MOTOR  = 2
  CH_COMM   = 3

  ' Enable channels you're currently debugging
  DEBUG_MASK = (1 << CH_MAIN) | (1 << CH_SENSOR)

PUB main()
  debug[CH_MAIN]("System starting")                  ' Compiled
  debug[CH_SENSOR]("Temp: ", SDEC(readTemp()))        ' Compiled
  debug[CH_MOTOR]("PWM: ", UDEC(dutyCycle))           ' Skipped
  debug("CRITICAL: watchdog timeout!")                 ' Always compiled (no channel)
```

### Large project (200+ debug statements)

```spin2
{Spin2_v46}
CON
  _clkfreq = 200_000_000

  ' --- Debug channel plan ---
  ' Channels 0-3:  Core subsystems
  CH_ERROR  = 0                 ' Errors (always enabled in dev)
  CH_INIT   = 1                 ' Initialization
  CH_STATE  = 2                 ' State machine transitions
  CH_PERF   = 3                 ' Performance metrics

  ' Channels 4-7:  Hardware subsystems
  CH_SENSOR = 4
  CH_MOTOR  = 5
  CH_SERVO  = 6
  CH_LED    = 7

  ' Channels 8-11: Communication
  CH_UART   = 8
  CH_SPI    = 9
  CH_I2C    = 10
  CH_CAN    = 11

  ' === ACTIVE DEBUG SELECTION ===
  ' Enable only what you're investigating right now.
  ' This keeps compiled records well under 255.
  DEBUG_MASK = (1 << CH_ERROR) | (1 << CH_SENSOR) | (1 << CH_I2C)

  ' Runtime: only debug cogs 0 and 1
  DEBUG_COGS = %00000011

  ' Give terminal time to connect
  DEBUG_DELAY = 500

PUB main()
  debug[CH_INIT]("Boot complete")                     ' Skipped (CH_INIT not in mask)
  debug[CH_ERROR]("Self-test passed")                 ' Compiled
  debug[CH_SENSOR]("Accel X: ", SDEC(ax))             ' Compiled
  debug[CH_MOTOR]("RPM: ", UDEC(rpm))                 ' Skipped
  debug[CH_I2C]("ACK from $", UHEX_BYTE(addr))        ' Compiled
```

---

## Quick Reference: Mechanism Comparison

| | `-d` flag | `DEBUG_DISABLE` | `DEBUG_MASK` + `debug[N]()` | `DEBUG_COGS` | `debug IF()` |
|---|---|---|---|---|---|
| **Level** | Compile-time | Compile-time | Compile-time | Runtime | Runtime |
| **Granularity** | All debug | All debug | Per channel (32) | Per cog (8) | Per statement |
| **Eliminates records?** | Yes (all) | Yes (all) | Yes (per channel) | No | No |
| **Eliminates code?** | Yes | Yes | Yes | No | No |
| **Zero overhead?** | Yes | Yes | Yes (disabled channels) | No | No |
| **Requires code changes?** | No (build flag) | CON constant | CON constant + `debug[N]` syntax | CON constant | Wrap each statement |
| **Version requirement** | Base | Base | `{Spin2_v46}` | Base | Base |

---

## Common Mistakes

**1. Using `debug IF()` to manage record count**
`debug IF(condition)(...)` still compiles the record. It only suppresses runtime output. If you're hitting the 255 limit, `debug IF()` won't help. Use `DEBUG_MASK` instead.

**2. Forgetting that regular `debug()` ignores the mask**
`DEBUG_MASK = 0` disables all channels, but `debug("hello")` still compiles. Use `debug[N]()` syntax for statements you want to be maskable.

**3. Not defining `DEBUG_MASK` before using `debug[N]()`**
If you write `debug[0]("test")` without defining `DEBUG_MASK`, you'll get a compile error. Always define the mask constant, even if you set it to `$FFFF_FFFF` to enable everything.

**4. Using the same debug string with different variables and expecting deduplication**
`debug("x=", UDEC(x))` and `debug("x=", UDEC(y))` are different records. Deduplication only helps when the entire record is byte-for-byte identical.

---

*This guide covers debug strategy for the Parallax Propeller 2 as implemented in the PNut-TS compiler. For complete syntax reference, see [DEBUG-MASK-Usage-Guide.md](DEBUG-MASK-Usage-Guide.md).*
