# Propeller 2 Testing Guide

## Hardware Testing Workflow

This guide explains how to compile, download, and test Spin2 programs on Propeller 2 hardware.

## Prerequisites

- **pnut_ts** - Spin2/PASM2 compiler
- **pnut-term-ts** - Propeller debug terminal
- **P2 Hardware** - Connected via PropPlug USB device

## Basic Testing Workflow

### 1. Compile Your Program

```bash
# Compile without debug output
pnut_ts myprogram.spin2

# Compile WITH debug output (recommended for testing)
pnut_ts -d myprogram.spin2
```

This creates a `.bin` file ready for download to the P2.

### 2. Check Available Hardware

```bash
# List connected PropPlug devices
pnut-term-ts -n
```

Note your device ID (e.g., `P9cektn7`).

### 3. Download and Run

#### Option A: Direct Console Output (Verbose)
```bash
# Download to RAM and show output in console
pnut-term-ts -r myprogram.bin -p P9cektn7
```

#### Option B: Background Execution with Log Monitoring (Cleaner)
```bash
# Run download in background
pnut-term-ts -r myprogram.bin -p P9cektn7 &

# Wait for log creation
sleep 2

# Find the newest log file
ls -t logs/*.log | head -1

# Monitor the log output
tail -f logs/debug_YYMMDD-HHMM.log
```

#### Option C: Persistent Terminal Session (Coming Soon - Best for Development)

**Note: This feature uses signals for hardware control and is coming in the next build of pnut-term-ts**

##### RAM Development Workflow (Fast Iteration)
```bash
# 1. Start terminal session in background
pnut-term-ts -p P9cektn7 &
PID=$!

# 2. Monitor logs in another terminal
tail -f logs/debug_*.log

# 3. Development cycle
while developing; do
  # Edit and compile
  vim myprogram.spin2
  pnut_ts -d myprogram.spin2

  # Kill current program, download to RAM, run
  kill -TERM $PID
  pnut-term-ts -r myprogram.bin -p P9cektn7

  # Test runs, observe debug output in log
  # Program executes until you're ready for next iteration

  # Kill before next download
  kill -TERM $PID
done

# 4. End session
kill -TERM $PID
```

##### FLASH Testing Workflow (Persistent Storage)
```bash
# 1. Start terminal session
pnut-term-ts -p P9cektn7 &
PID=$!

# 2. Monitor logs
tail -f logs/debug_*.log

# 3. FLASH deployment cycle
# Compile for FLASH
pnut_ts -F myprogram.spin2

# Kill current execution
kill -TERM $PID

# Download to FLASH (creates .flash file first)
pnut-term-ts -f myprogram.flash -p P9cektn7

# Observe download confirmation in log
# Wait for download to complete

# Reset processor to boot from FLASH
kill -USR1 $PID

# New log created from fresh boot
# Observe program running from FLASH

# 4. End session when done
kill -TERM $PID
```

**Signal Reference:**
- `kill -TERM $PID` - Stop current program execution
- `kill -USR1 $PID` - Reset processor (reboot from FLASH)
- `kill -TERM $PID` - Graceful terminal shutdown

### 4. Understanding Debug Logs

Debug logs are created in the `logs/` directory with timestamps. Each download session creates a new log file.

Log format example:
```
[2025-09-26T02:59:35.301Z] Cog0 Queue Test Starting
[2025-09-26T02:59:35.302Z] Cog0 PASS: Empty dequeue returns -1
```

### 5. Cleanup

When testing is complete, kill background processes:
```bash
# Find process IDs
ps aux | grep pnut-term

# Kill specific process
kill [PID]

# Or kill by name
pkill pnut-term-ts
```

## Writing Testable Code

### Use Debug Statements
```spin2
PUB testFunction() | result
  debug("Starting test")
  result := doSomething()
  debug("Result: ", udec(result))
```

### Create Test Suites
```spin2
PUB main()
  debug("=== Test Suite Starting ===")

  testsPassed := 0
  testsFailed := 0

  ' Run individual tests
  runTest1()
  runTest2()

  ' Report results
  debug("Tests Passed: ", udec(testsPassed))
  debug("Tests Failed: ", udec(testsFailed))
```

### Test Patterns

1. **Unit Tests** - Test individual functions in isolation
2. **Integration Tests** - Test component interactions
3. **Edge Cases** - Test boundary conditions (empty, full, overflow)
4. **Stress Tests** - Test with many operations

## Example Test Session

### Quick Test
```bash
# 1. Write your test program
vim queue_test.spin2

# 2. Compile with debug
pnut_ts -d queue_test.spin2

# 3. Run in background
pnut-term-ts -r queue_test.bin -p P9cektn7 &

# 4. Monitor output
tail -f logs/debug_$(date +%y%m%d)-*.log

# 5. When done, cleanup
pkill pnut-term-ts
```

### Development Session (With Signal Control - Coming Soon)
```bash
# 1. Start persistent terminal
pnut-term-ts -p P9cektn7 &
PID=$!

# 2. Start log monitor in another terminal
tail -f logs/debug_*.log

# 3. Development loop for RAM testing
while developing; do
  # Edit code
  vim myprogram.spin2

  # Compile
  pnut_ts -d myprogram.spin2

  # Kill current program
  kill -TERM $PID

  # Download to RAM and run
  pnut-term-ts -r myprogram.bin -p P9cektn7

  # Test and observe log output
  # Program runs until you need to test again
done

# 4. End session
kill -TERM $PID

# For FLASH testing, use -F flag and USR1 signal for reset
```

## Tips

- Always compile with `-d` flag during testing for debug output
- Use background execution to keep console clean
- Monitor logs instead of console for cleaner output
- Keep test programs modular with clear pass/fail reporting
- Use smaller data structures for testing (e.g., QUEUE_SIZE = 5)
- Add heartbeat or periodic output to confirm program is running

## Common Issues

**Empty string error during compilation:**
- Check for encoding issues
- Use block comments `{ }` instead of line comments with apostrophes

**Can't find PropPlug:**
- Ensure USB device is connected
- Check device permissions
- Try unplugging and reconnecting

**Download succeeds but no output:**
- Ensure program was compiled with `-d` debug flag
- Check the correct log file (newest in logs/)
- Verify debug() statements are in your code