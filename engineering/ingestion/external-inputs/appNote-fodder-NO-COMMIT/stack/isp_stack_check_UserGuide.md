# isp_stack_check - User Guide

A utility object for detecting stack overflow in Spin2 COG tasks on the Parallax Propeller 2. It fills a task stack with a known sentinel pattern before launch, then checks at runtime whether the sentinel has been overwritten -- catching overflows that would otherwise silently corrupt memory.

- **Author:** Stephen M. Moraco, Iron Sheep Productions, LLC
- **License:** MIT
- **Dependencies:** None

---

## Why You Need This

When you launch a Spin2 method in a new COG with `cogspin()`, you provide a stack buffer. If the method's call depth or local variables exceed that buffer, the stack silently overwrites whatever memory follows it. This object detects that situation by:

1. Filling the stack with a recognizable pattern (`$a5a50df0`) before launch
2. Placing a sentinel value (`$addee5e5`) immediately after the last stack long
3. Checking at runtime whether the sentinel is still intact

If the sentinel has been overwritten, the COG halts with a debug message -- giving you a clear signal instead of mysterious corruption.

---

## Quick Start

```spin2
OBJ
    stack_check : "isp_stack_check"

CON
    TASK_STACK_LONGS = 128

DAT
    taskStack       LONG    0[TASK_STACK_LONGS]
    endStackMark    LONG    stack_check.DO_NOT_WRITE_MARK       ' sentinel after stack

PUB startTask()
    ' Step 1: Prepare the stack (fill with pattern + set sentinel)
    stack_check.prepStackForCheck(@taskStack, TASK_STACK_LONGS)

    ' Step 2: Launch the COG
    cogspin(NEWCOG, myTask(), @taskStack)

PRI myTask()
    repeat
        ' Step 3: Check for overflow each iteration
        stack_check.checkStack(@taskStack, TASK_STACK_LONGS)
        ' ... do work ...
```

---

## Public API Reference

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `DO_NOT_WRITE_MARK` | `$addee5e5` | Sentinel placed after the last stack long; overflow detected if overwritten |
| `NOT_WRITTEN_MARK` | `$a5a50df0` | Fill pattern written to every stack long before launch |
| `TST_UNKNOWN` | `0` | Test result: unknown |
| `TST_PASS` | `1` | Test result: pass |
| `TST_FAIL` | `2` | Test result: fail |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `prepStackForCheck` | `(pStack, nStackLongCt)` | Fill stack with `NOT_WRITTEN_MARK` and write `DO_NOT_WRITE_MARK` sentinel at `pStack[nStackLongCt]` |
| `checkStack` | `(pStack, nStackLongCt)` | Verify sentinel is intact. If overwritten: emit debug message and **halt the COG** |
| `reportStackUse` | `(pStack, nStackLongCt)` | Count how many longs were used and print `"^^^ STACK used N of M"` to debug |
| `testReport` | `(pStack, nStackLongCt, pTestId, bPassFail)` | Print pass/fail result, report stack usage, check for overflow. **Halts on failure** |
| `dumpStack` | `(pStack, nStackLongCt)` | Hex dump the entire stack contents to debug |
| `dbgMemDump` | `(pMessage, pBytes, lenBytes)` | General-purpose hex memory dump (16 bytes per row with addresses) |

### Parameter Reference

- **pStack** -- Pointer to the first long of the stack buffer (e.g., `@taskStack`)
- **nStackLongCt** -- Number of longs in the stack buffer (not bytes -- longs)
- **pTestId** -- Pointer to a zero-terminated string identifying the test
- **bPassFail** -- `TST_PASS` (1) or `TST_FAIL` (2)

---

## The Three-Phase Usage Pattern

Every production use follows the same three phases:

### Phase 1: Declare Stack + Sentinel (DAT section)

```spin2
CON
    STACK_SIZE_LONGS = 128

DAT
    taskStack       LONG    0[STACK_SIZE_LONGS]
    endStackMark    LONG    stack_check.DO_NOT_WRITE_MARK
```

The sentinel long **must** be declared immediately after the stack buffer in DAT. This places it at the exact memory address the object will check. At compile time, it holds `$addee5e5`; at runtime, `prepStackForCheck()` also writes this value programmatically.

### Phase 2: Prepare Before `cogspin()` (startup method)

```spin2
PUB start()
    stack_check.prepStackForCheck(@taskStack, STACK_SIZE_LONGS)
    cogspin(NEWCOG, myTask(), @taskStack)
```

This fills every stack long with `$a5a50df0` and writes the sentinel at position `[STACK_SIZE_LONGS]`. Call this **before** `cogspin()` -- it must run before the task starts using the stack.

### Phase 3: Check at Runtime (inside the COG task)

```spin2
PRI myTask()
    repeat
        stack_check.checkStack(@taskStack, STACK_SIZE_LONGS)
        ' ... do work ...
```

If the sentinel has been overwritten, `checkStack()` prints `"^^^ STACK Overflow! Depth greater than N longs"` to debug and halts the COG in an infinite loop for analysis.

---

## Real-World Usage Patterns

The following patterns are drawn from 3 production projects across 7 consumer files.

### Pattern 1: Single COG with Periodic Checking

The most common pattern -- one background task with a check at the top of each loop iteration.

**Sensor driver COG** (from P2-Magnetic-Imaging-Tile, `isp_tile_sensor.spin2`):

```spin2
OBJ
    fifo        : "isp_frame_fifo_manager"
    stack_check : "isp_stack_check"

CON
    SENSOR_STACK_SIZE_LONGS = 128

DAT
    sensor_cog_stack    LONG    0[SENSOR_STACK_SIZE_LONGS]
    sensor_stack_mark   LONG    stack_check.DO_NOT_WRITE_MARK

PUB start(sensor_base_pin) : success
    stack_check.prepStackForCheck(@sensor_cog_stack, SENSOR_STACK_SIZE_LONGS)
    cog_id := cogspin(NEWCOG, sensor_loop(), @sensor_cog_stack)

PRI sensor_loop()
    configure_smart_pins()

    repeat
        stack_check.checkStack(@sensor_cog_stack, SENSOR_STACK_SIZE_LONGS)
        ' ... read sensor, push frames to FIFO ...
```

---

### Pattern 2: Granular Checking Around Deep Call Chains

When your COG task calls multiple initialization routines with deep call chains, check the stack **after each one** to pinpoint exactly which routine overflows.

**OLED display COG** (from P2-Magnetic-Imaging-Tile, `isp_oled_single_cog.spin2`):

```spin2
CON
    OLED_STACK_SIZE_LONGS = 128

DAT
    display_cog_stack   LONG    0[OLED_STACK_SIZE_LONGS]
    display_stack_mark  LONG    stack_check.DO_NOT_WRITE_MARK

PRI display_loop()
    ' Check BEFORE init (baseline)
    stack_check.checkStack(@display_cog_stack, OLED_STACK_SIZE_LONGS)

    init_hardware()
    ' Check AFTER init_hardware
    stack_check.checkStack(@display_cog_stack, OLED_STACK_SIZE_LONGS)

    init_color_lut()
    ' Check AFTER init_color_lut
    stack_check.checkStack(@display_cog_stack, OLED_STACK_SIZE_LONGS)

    init_cell_origin_lut()
    ' Check AFTER init_cell_origin_lut
    stack_check.checkStack(@display_cog_stack, OLED_STACK_SIZE_LONGS)

    ' Main loop
    repeat
        stack_check.checkStack(@display_cog_stack, OLED_STACK_SIZE_LONGS)
        ' ... render frames ...
```

**HDMI display COG** (from P2-Magnetic-Imaging-Tile, `isp_hdmi_display_engine.spin2`) follows the same granular pattern:

```spin2
PRI display_loop()
    stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)
    gfx.start()
    stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)

    gfx.cls($00_00_00)
    stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)

    gfx.DrawSensorGrid(GRID_X, GRID_Y, CELL_SIZE, CELL_GAP)
    stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)

    DrawStaticLabels()
    stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)

    repeat
        stack_check.checkStack(@display_cog_stack, HDMI_STACK_SIZE_LONGS)
        ' ... process FIFO frames, update display ...
```

This approach is invaluable during development -- if `init_color_lut()` overflows, you see the halt **immediately** after that call instead of some time later in the main loop.

---

### Pattern 3: Multiple COG Stacks in One Object

When an object launches more than one COG, each stack gets its own buffer, sentinel, and prep call.

**Serial receiver with watchdog** (from P2-Magnetic-Imaging-Tile REF, `isp_string_receiver.spin2`):

```spin2
OBJ
    RPi         : "isp_serial"
    stack_util  : "isp_stack_check"
    strQ        : "isp_string_queue"

CON
    STACK_SIZE_LONGS = 96       ' 48 and 32 crash!

DAT
    ' Watchdog COG stack
    taskWdStack     LONG    0[STACK_SIZE_LONGS]
    endWdStackMark  LONG    stack_util.DO_NOT_WRITE_MARK

    ' Serial receive COG stack
    taskRxStack     LONG    0[STACK_SIZE_LONGS]
    endRxStackMark  LONG    stack_util.DO_NOT_WRITE_MARK

PUB start()
    ' Prepare BOTH stacks
    stack_util.prepStackForCheck(@taskRxStack, STACK_SIZE_LONGS)
    stack_util.prepStackForCheck(@taskWdStack, STACK_SIZE_LONGS)

    ' Launch serial receive COG
    rxCogId := cogspin(NEWCOG, TaskSerialRx(@serialRxBffr, RX_CHR_Q_MAX_BYTES), @taskRxStack)

    ' Launch watchdog COG (elsewhere)
    wdCogId := cogspin(NEWCOG, TaskCidHealthWd(), @taskWdStack)

PRI TaskSerialRx(pRxBffr, lenRxBffr)
    repeat
        stack_util.checkStack(@taskRxStack, STACK_SIZE_LONGS)
        ' ... receive characters ...

PRI TaskCidHealthWd()
    repeat
        stack_util.checkStack(@taskWdStack, STACK_SIZE_LONGS)
        ' ... monitor health ...
```

Note the comment `' 48 and 32 crash!` -- this is exactly the kind of discovery `isp_stack_check` enables. The developer tried smaller stacks, detected the overflow, and increased to 96.

---

### Pattern 4: Checking from Both the Task and Its Callers

You can call `checkStack()` from the COG that owns the stack **and** from the main COG that calls methods which interact with the task's data. This catches overflow regardless of which COG detects it first.

**COG-offloader pattern** (from P2-OctoSerial, `isp_octoport_serial.spin2` -- currently commented out):

```spin2
CON
    STACK_SIZE_LONGS = 64

DAT
    taskStack       LONG    0[STACK_SIZE_LONGS]
    endStackMark    LONG    stack_util.DO_NOT_WRITE_MARK

PUB addPort(rxp, txp, mode, baudrate, txPullup) : portHandle
    stack_util.prepStackForCheck(@taskStack, STACK_SIZE_LONGS)
    ' ... launch background task ...

PRI taskUnloadStringToQ()
    repeat
        ' Check from WITHIN the background task
        stack_util.checkStack(@taskStack, STACK_SIZE_LONGS)
        ' ... process strings ...

PUB getRxString(pUserBuf, nBufLen) : pNextString
    ' Check from the CALLING COG (main program)
    stack_util.checkStack(@taskStack, STACK_SIZE_LONGS)
    ' ... dequeue string ...
```

---

### Pattern 5: Unit Test Reporting with `testReport()`

The `testReport()` method combines pass/fail reporting with stack usage analysis -- useful for automated testing.

**Queue overrun tests** (from P2-Magnetic-Imaging-Tile REF, `isp_string_receiver.spin2`):

```spin2
CON
    #0, TST_UNKNOWN, TST_PASS, TST_FAIL        ' from isp_stack_check

PRI runTests() | bPassFail, bQueOverrun
    ' Test 1: Should detect overrun
    bQueOverrun := fillQueuePastCapacity()
    bPassFail := (bQueOverrun == TRUE) ? TST_PASS : TST_FAIL
    stack_util.testReport(@taskRxStack, STACK_SIZE_LONGS, string("(1) Rx too many"), bPassFail)

    ' Test 2: Should NOT overrun
    bQueOverrun := fillQueueToExactCapacity()
    bPassFail := (bQueOverrun == FALSE) ? TST_PASS : TST_FAIL
    stack_util.testReport(@taskRxStack, STACK_SIZE_LONGS, string("(2) Rx Exact full"), bPassFail)

    ' Test 3: Wrap-around test
    bQueOverrun := wrapAroundTest()
    bPassFail := (bQueOverrun == FALSE) ? TST_PASS : TST_FAIL
    stack_util.testReport(@taskRxStack, STACK_SIZE_LONGS, string("(3) Rx wrap test"), bPassFail)
```

Debug output from `testReport()` looks like:

```
+++ ---------
+++ TEST [(1) Rx too many] - pass
^^^ STACK used 47 of 96
```

On failure, the output includes `FAIL` and the COG halts for analysis.

---

## Stack Sizing Guidelines

| Task Complexity | Recommended Size | Notes |
|----------------|-----------------|-------|
| Simple loop, few locals | 32-64 longs | Clock tasks, simple watchdogs |
| Moderate (serial I/O, queues) | 64-96 longs | String processing, protocol handlers |
| Complex (display drivers, deep call chains) | 128+ longs | Graphics init, multi-stage pipelines |

**How to right-size a stack:**

1. Start with a generous allocation (e.g., 128 longs)
2. Add `reportStackUse()` calls to see actual high-water mark
3. Reduce the allocation to ~1.5x the reported usage
4. Keep `checkStack()` in your main loop as ongoing protection

---

## Tips and Best Practices

1. **Always place the sentinel immediately after the stack in DAT.** The `LONG stack_check.DO_NOT_WRITE_MARK` must be the very next long after `LONG 0[SIZE]` -- no gaps, no other variables between them.

2. **Call `prepStackForCheck()` before `cogspin()`.** The fill pattern enables both overflow detection and usage reporting. Without it, `reportStackUse()` cannot distinguish used from unused longs.

3. **Use granular checking during development.** Place `checkStack()` calls after every major function call to pinpoint exactly which routine causes overflow. You can remove the extra checks once the stack is right-sized.

4. **The `reportStackUse()` method counts from the bottom up.** It stops at the first long that still contains `NOT_WRITTEN_MARK`, reporting everything below that as "used." This gives you a high-water mark for sizing.

5. **`checkStack()` halts on overflow.** When it detects the sentinel has been overwritten, it enters an infinite `repeat` loop. This is intentional -- it freezes the COG so you can examine debug output and memory state.

6. **Common object prefixes** seen across production code:
   - `stack_check` -- used in newer projects (P2-Magnetic-Imaging-Tile src/)
   - `stack_util` -- used in older projects (P2-OctoSerial, REF code)

7. **Use `dbgMemDump()` as a standalone utility.** It works on any memory region, not just stacks -- useful for inspecting buffers, register maps, or data structures during debugging.

---

## Projects Using This Object

| Project | Consumer Files | Stacks Monitored | Primary Use Case |
|---------|---------------|-----------------|-----------------|
| P2-Magnetic-Imaging-Tile (src/) | 3 files | 3 COG stacks (OLED, HDMI, Sensor) | Display and sensor driver overflow protection |
| P2-Magnetic-Imaging-Tile (REF/) | 3 files | 4 COG stacks (clock, display, watchdog, serial Rx) | Multi-COG overflow detection + unit test reporting |
| P2-OctoSerial | 1 file (commented out) | 1 COG stack (string queue offloader) | Background task overflow detection |
| P2-uSD-FAT32-FS | 0 files | -- | Present but currently unused |
