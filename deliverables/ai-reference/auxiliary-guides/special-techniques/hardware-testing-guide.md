# Propeller 2 Testing Guide

## Hardware Testing Workflow

This guide explains how to compile, download, and test Spin2 programs on Propeller 2 hardware.

## Prerequisites

- **pnut_ts** - Spin2/PASM2 compiler
- **pnut-term-ts** - Propeller debug terminal (with signal support)
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

#### Option B: Background Execution with Log Monitoring (Cleaner)
```bash
# Run download in background and capture PID
pnut-term-ts -r myprogram.bin -p P9cektn7 &
PID=$!

# Monitor the log output
tail -f logs/$(ls -t1 logs | head -1)

# When done, clean shutdown
kill -TERM $PID
```


##### FLASH Testing Workflow (Persistent Storage)
```bash
# FLASH deployment cycle
# Compile for FLASH
pnut_ts -F myprogram.spin2

# Download to FLASH and run
pnut-term-ts -f myprogram.flash -p P9cektn7 &
PID=$!

# Monitor logs
tail -f logs/$(ls -t1 logs | head -1)

# If you need to reset the processor (reboot from FLASH)
kill -USR1 $PID

# When done testing
kill -TERM $PID
```

**Signal Reference:**

- `kill -TERM $PID` - Clean shutdown of terminal session
- `kill -USR1 $PID` - Reset processor (causes reboot from FLASH)

**Alternative (only as last resort):**

- `pkill pnut-term-ts` - Kill by process name (less precise)

### 4. Understanding Debug Logs

Debug logs are created in the `logs/` directory with timestamps. Each download session creates a new log file.

Log format example:
```
[2025-09-26T02:59:35.301Z] Cog0 Queue Test Starting
[2025-09-26T02:59:35.302Z] Cog0 PASS: Empty dequeue returns -1
```

### 5. Finding the Latest Log

```bash
# Find newest log file
ls -t1 logs/*.log | head -1
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

# 3. Run in background with PID capture
pnut-term-ts -r queue_test.bin -p P9cektn7 &
PID=$!

# 4. Monitor output
tail -f logs/$(ls -t1 logs | head -1)

# 5. Clean shutdown when done
kill -TERM $PID
```

### Rapid Development Session
```bash
# Development loop for quick iterations
while true; do
  # Edit code
  vim myprogram.spin2

  # Compile
  pnut_ts -d myprogram.spin2
  
  if [ $? -ne 0 ]; then
    echo "Compilation failed, fix errors and press Enter"
    read
    continue
  fi

  # Download and run
  pnut-term-ts -r myprogram.bin -p P9cektn7 &
  PID=$!
  
  # Show log
  echo "Monitoring output (Ctrl-C to stop test)..."
  tail -f logs/$(ls -t1 logs | head -1)
  
  # When user hits Ctrl-C on tail, clean up
  echo "Stopping program..."
  kill -TERM $PID 2>/dev/null
  
  echo "Press Enter to test again, or Ctrl-C to exit"
  read
done
```

### FLASH Deployment
```bash
# For production deployment to FLASH
# 1. Compile for FLASH
pnut_ts -F production.spin2

# 2. Download to FLASH
pnut-term-ts -f production.flash -p P9cektn7 &
PID=$!

# 3. Monitor initial boot
tail -f logs/$(ls -t1 logs | head -1)

# 4. Test reset capability
echo "Testing processor reset..."
kill -USR1 $PID
sleep 2
# New log will be created after reset

# 5. Final cleanup
kill -TERM $PID
```

## Tips

- **Always compile with `-d` flag** during testing for debug output
- **Capture PID** when starting pnut-term-ts for clean shutdown
- **Use `kill -TERM $PID`** instead crude `pkill` when possible
- **Monitor logs** instead of console (console doesn't have log data)
- **Keep test programs modular** with clear pass/fail reporting
- **Use smaller data structures** for testing (e.g., QUEUE_SIZE = 5)
- **Add periodic output** to confirm program is running

## Common Issues

**Can't find PropPlug:**
- Ensure USB device is connected
- Check device permissions
- Try unplugging and reconnecting

**Download succeeds but no output:**
- Ensure program was compiled with `-d` debug flag
- Check the correct log file (newest in logs/)
- Verify debug() statements are in your code

**Process won't die:**
- Use `ps aux | grep pnut-term` to find stubborn processes
- Use `kill -9 [PID]` as last resort (forceful termination)

## Signal Control Summary

The `pnut-term-ts` tool now supports clean signal-based control:

| Signal | Command | Purpose |
|--------|---------|---------|
| TERM | `kill -TERM $PID` | Clean shutdown of terminal session |
| USR1 | `kill -USR1 $PID` | Reset processor (reboot from FLASH) |
| KILL | `kill -9 $PID` | Force kill (last resort) |

Using signals provides cleaner control than using `pkill` or Ctrl-C, and allows for precise process management when running multiple terminal sessions.
