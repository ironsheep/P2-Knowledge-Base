# Method Pointer Usage Guide for Spin2

This document provides comprehensive coverage of method pointers in Spin2, including how to obtain method addresses, store them in variables, call methods indirectly, pass parameters, handle return values, and implement common patterns like callbacks and dispatch tables.

## Overview

Method pointers are 32-bit values that hold the address of a method, enabling indirect (dynamic) method calls. They provide powerful capabilities for:

- **Callbacks** - Register handlers that get called when events occur
- **Dispatch tables** - Select methods at runtime based on state or input
- **Polymorphism** - Call different implementations through a common interface
- **Decoupling** - Separate the caller from knowledge of specific methods

Spin2 supports three forms of method pointers:

| Form | Syntax | Description |
|------|--------|-------------|
| Local method | `@MethodName` | Pointer to a method in the current object |
| Object method | `@obj.MethodName` | Pointer to a method in a child object |
| Indexed object method | `@obj[i].MethodName` | Pointer to a method in an indexed child object |

---

## Declaring Method Pointer Variables

Method pointers must be stored in LONG variables. They cannot use bitfields.

### VAR Block Declaration

```spin2
VAR
  LONG callback           ' Method pointer variable
  LONG handlers[4]        ' Array of method pointers
  LONG onComplete         ' Event handler pointer
```

### Local Variable Declaration

```spin2
PUB Process() | handler, tempPtr
  handler := @DoWork
  handler()
```

### Parameter Declaration

```spin2
PUB RegisterCallback(handler)
  callback := handler

PUB CallWithHandler(LONG processFunc, data)
  processFunc(data)
```

### Invalid Declarations

```spin2
VAR
  BYTE ptr              ' ERROR: Must be LONG
  WORD ptr              ' ERROR: Must be LONG
  LONG ptr : 16         ' ERROR: Cannot have bitfield specification
```

**Compiler Error**: "Method pointers must be long variables without bitfields"

---

## Getting Method Addresses

Use the `@` operator to obtain a method's address.

### Local Method Pointers

Get the address of a method in the current object:

```spin2
VAR
  LONG handler

PUB Setup()
  handler := @ProcessData     ' Get address of local method

PUB Run()
  handler()                   ' Call through pointer

PRI ProcessData()
  ' ... implementation ...
```

### Object Method Pointers

Get the address of a method in a child object:

```spin2
OBJ
  serial : "jm_serial"
  motor  : "servo_driver"

VAR
  LONG outputMethod

PUB Setup()
  outputMethod := @serial.tx        ' Method in child object
  outputMethod := @motor.SetPosition ' Different child object
```

### Indexed Object Method Pointers

Get method addresses from object arrays:

```spin2
OBJ
  sensors[4] : "sensor_driver"

VAR
  LONG readMethod

PUB SelectSensor(index)
  readMethod := @sensors[index].Read    ' Method from indexed object

PUB GetReading() : value
  value := readMethod()
```

### Method Pointers in Expressions

Method addresses can be used directly in expressions:

```spin2
PUB Example()
  ' Pass method pointer directly to another method
  RegisterHandler(@OnButtonPress)

  ' Store in array
  handlers[0] := @State0
  handlers[1] := @State1
  handlers[2] := @State2

  ' Conditional assignment
  callback := condition ? @HandlerA : @HandlerB
```

---

## Calling Through Method Pointers

Once you have a method pointer, call it using parentheses.

### Basic Indirect Call

```spin2
VAR
  LONG handler

PUB Example()
  handler := @DoWork
  handler()               ' Indirect call - executes DoWork
```

### With Parameters

Pass parameters in parentheses just like a normal method call:

```spin2
VAR
  LONG processor

PUB Example()
  processor := @Calculate
  result := processor(10, 20, 30)   ' Call with 3 parameters

PRI Calculate(a, b, c) : result
  result := a + b + c
```

### With Return Values

#### Single Return Value

```spin2
VAR
  LONG calculator

PUB Example() | result
  calculator := @Add
  result := calculator(5, 3)    ' Returns 8

PRI Add(a, b) : sum
  sum := a + b
```

#### Multiple Return Values

Use the `:N` syntax to specify expected return count:

```spin2
VAR
  LONG coordGetter

PUB Example() | x, y, z
  coordGetter := @GetPosition
  x, y, z := coordGetter() : 3    ' Expect 3 return values

PRI GetPosition() : px, py, pz
  px := currentX
  py := currentY
  pz := currentZ
```

The `:N` suffix tells the runtime how many values to expect from the method pointer call.

### Null Pointer Check

Always verify a method pointer is valid before calling:

```spin2
VAR
  LONG callback

PUB TriggerEvent(data)
  if callback <> 0
    callback(data)
  ' or use short-circuit evaluation:
  ' callback and callback(data)
```

---

## Special Method Pointers: RECV and SEND

Spin2 provides two special built-in method pointers for inter-cog communication.

### RECV - Receive Method Pointer

`RECV` is a special method pointer for receiving data from inter-cog mailboxes.

```spin2
VAR
  LONG receiver = RECV

PUB WaitForMessage() : data
  data := receiver()          ' Receive from mailbox
  ' or simply:
  data := RECV()
```

**Restrictions:**
- Takes no parameters
- Always returns exactly one value
- Cannot be used with `\RECV()` syntax

### SEND - Send Method Pointer

`SEND` is a special method pointer for sending data to inter-cog mailboxes.

```spin2
VAR
  LONG sender = SEND

PUB SendMessage(data)
  sender(data)                ' Send to mailbox
  ' or simply:
  SEND(data)
```

**Restrictions:**
- Returns no value (cannot be used as a term)
- Cannot be used with `\SEND()` syntax

### Using RECV/SEND for Flexible I/O

```spin2
VAR
  LONG inputMethod
  LONG outputMethod

PUB SetupStandardIO()
  inputMethod := RECV
  outputMethod := SEND

PUB SetupSerialIO()
  inputMethod := @serial.rx
  outputMethod := @serial.tx

PUB ProcessIO() | char
  char := inputMethod()
  outputMethod(char + 1)
```

---

## Method Pointer Arrays and Dispatch Tables

Arrays of method pointers enable powerful dispatch patterns.

### Basic Dispatch Table

```spin2
CON
  STATE_IDLE    = 0
  STATE_RUNNING = 1
  STATE_PAUSED  = 2
  STATE_ERROR   = 3
  NUM_STATES    = 4

VAR
  LONG stateHandlers[NUM_STATES]
  LONG currentState

PUB Init()
  stateHandlers[STATE_IDLE] := @HandleIdle
  stateHandlers[STATE_RUNNING] := @HandleRunning
  stateHandlers[STATE_PAUSED] := @HandlePaused
  stateHandlers[STATE_ERROR] := @HandleError
  currentState := STATE_IDLE

PUB Update() | nextState
  if currentState >= 0 and currentState < NUM_STATES
    nextState := stateHandlers[currentState]()
    currentState := nextState

PRI HandleIdle() : next
  ' ... idle logic ...
  next := STATE_RUNNING

PRI HandleRunning() : next
  ' ... running logic ...
  next := STATE_RUNNING

PRI HandlePaused() : next
  ' ... paused logic ...
  next := STATE_IDLE

PRI HandleError() : next
  ' ... error logic ...
  next := STATE_IDLE
```

### Command Dispatch

```spin2
CON
  CMD_READ  = 0
  CMD_WRITE = 1
  CMD_ERASE = 2
  CMD_RESET = 3
  NUM_CMDS  = 4

VAR
  LONG cmdHandlers[NUM_CMDS]

PUB Init()
  cmdHandlers[CMD_READ] := @DoRead
  cmdHandlers[CMD_WRITE] := @DoWrite
  cmdHandlers[CMD_ERASE] := @DoErase
  cmdHandlers[CMD_RESET] := @DoReset

PUB ExecuteCommand(cmd, param) : result
  if cmd >= 0 and cmd < NUM_CMDS
    result := cmdHandlers[cmd](param)
  else
    result := -1   ' Invalid command
```

### Menu System

```spin2
CON
  MENU_ITEMS = 5

VAR
  LONG menuActions[MENU_ITEMS]

PUB InitMenu()
  menuActions[0] := @ActionNew
  menuActions[1] := @ActionOpen
  menuActions[2] := @ActionSave
  menuActions[3] := @ActionSettings
  menuActions[4] := @ActionQuit

PUB HandleMenuSelection(selection)
  if selection >= 0 and selection < MENU_ITEMS
    menuActions[selection]()
```

---

## Callback Patterns

Method pointers enable callback-based programming.

### Event Handler Registration

```spin2
VAR
  LONG onButtonPress
  LONG onButtonRelease
  LONG onTimeout

PUB RegisterButtonHandler(pressHandler, releaseHandler)
  onButtonPress := pressHandler
  onButtonRelease := releaseHandler

PUB RegisterTimeoutHandler(handler)
  onTimeout := handler

PUB CheckEvents()
  if ButtonPressed()
    if onButtonPress
      onButtonPress()
  if ButtonReleased()
    if onButtonRelease
      onButtonRelease()
  if TimedOut()
    if onTimeout
      onTimeout()
```

### Completion Callback

```spin2
VAR
  LONG completionCallback

PUB StartAsyncOperation(onComplete)
  completionCallback := onComplete
  ' ... start operation ...

PRI OperationFinished(result)
  if completionCallback
    completionCallback(result)
```

### Progress Callback

```spin2
PUB ProcessWithProgress(data, size, progressCallback) | i, percent
  repeat i from 0 to size - 1
    ProcessItem(data, i)
    if progressCallback
      percent := (i * 100) / size
      progressCallback(percent)
  if progressCallback
    progressCallback(100)
```

### Filter/Transform Callback

```spin2
PUB TransformArray(pArray, count, transformFunc) | i, value
  repeat i from 0 to count - 1
    value := LONG[pArray][i]
    LONG[pArray][i] := transformFunc(value)

' Usage:
PUB Example()
  TransformArray(@values, 10, @DoubleValue)
  TransformArray(@values, 10, @SquareValue)

PRI DoubleValue(x) : result
  result := x * 2

PRI SquareValue(x) : result
  result := x * x
```

---

## Comparison Callbacks

Method pointers enable custom sorting and searching.

### Custom Sort Comparator

```spin2
PUB SortArray(pArray, count, compareFunc) | i, j, temp, cmp
  repeat i from 0 to count - 2
    repeat j from i + 1 to count - 1
      cmp := compareFunc(LONG[pArray][i], LONG[pArray][j])
      if cmp > 0
        temp := LONG[pArray][i]
        LONG[pArray][i] := LONG[pArray][j]
        LONG[pArray][j] := temp

' Comparator functions:
PRI CompareAscending(a, b) : result
  result := a - b

PRI CompareDescending(a, b) : result
  result := b - a

' Usage:
PUB Example()
  SortArray(@numbers, 20, @CompareAscending)
  SortArray(@numbers, 20, @CompareDescending)
```

### Custom Search Predicate

```spin2
PUB FindFirst(pArray, count, predicateFunc) : index | i
  index := -1
  repeat i from 0 to count - 1
    if predicateFunc(LONG[pArray][i])
      return i
  return -1

PRI IsEven(x) : result
  result := (x & 1) == 0

PRI IsPositive(x) : result
  result := x > 0

' Usage:
PUB Example() | idx
  idx := FindFirst(@values, 100, @IsEven)
  idx := FindFirst(@values, 100, @IsPositive)
```

---

## Object Method Pointer Patterns

### Pluggable Components

```spin2
OBJ
  lcd    : "lcd_driver"
  serial : "serial_driver"

VAR
  LONG printChar
  LONG printStr

PUB UseDisplay()
  printChar := @lcd.Char
  printStr := @lcd.Str

PUB UseSerial()
  printChar := @serial.tx
  printStr := @serial.str

PUB Print(pStr) | c
  repeat while (c := BYTE[pStr++]) <> 0
    printChar(c)
```

### Strategy Pattern

```spin2
OBJ
  fastAlgo : "algorithm_fast"
  safeAlgo : "algorithm_safe"

VAR
  LONG processMethod

PUB SetFastMode()
  processMethod := @fastAlgo.Process

PUB SetSafeMode()
  processMethod := @safeAlgo.Process

PUB DoProcess(data) : result
  result := processMethod(data)
```

### Multiple Output Targets

```spin2
OBJ
  term  : "terminal"
  log   : "sd_logger"
  radio : "rf_transmitter"

VAR
  LONG outputs[3]
  BYTE outputCount

PUB AddTerminalOutput()
  outputs[outputCount++] := @term.str

PUB AddLogOutput()
  outputs[outputCount++] := @log.write

PUB AddRadioOutput()
  outputs[outputCount++] := @radio.send

PUB Broadcast(pMessage) | i
  repeat i from 0 to outputCount - 1
    outputs[i](pMessage)
```

---

## Parameter Count Considerations

Method pointer calls don't have compile-time parameter validation against the target method's signature.

### Matching Parameters

Ensure the call site provides the correct number of parameters:

```spin2
VAR
  LONG processor

PUB Example()
  processor := @TwoParams
  processor(1, 2)         ' Correct: 2 parameters

  processor := @ThreeParams
  processor(1, 2, 3)      ' Correct: 3 parameters

PRI TwoParams(a, b)
  ' ...

PRI ThreeParams(a, b, c)
  ' ...
```

### Flexible Parameter Handling

For dispatch tables with varying parameters, consider wrapper methods:

```spin2
VAR
  LONG handlers[4]

PUB Init()
  handlers[0] := @WrapNoParam
  handlers[1] := @WrapOneParam
  handlers[2] := @WrapTwoParams
  handlers[3] := @WrapThreeParams

PUB Dispatch(index, p1, p2, p3) : result
  result := handlers[index](p1, p2, p3)

PRI WrapNoParam(p1, p2, p3) : result
  result := ActualNoParam()

PRI WrapOneParam(p1, p2, p3) : result
  result := ActualOneParam(p1)

PRI WrapTwoParams(p1, p2, p3) : result
  result := ActualTwoParams(p1, p2)

PRI WrapThreeParams(p1, p2, p3) : result
  result := ActualThreeParams(p1, p2, p3)
```

---

## Restrictions and Limitations

### Variable Type Restrictions

| Allowed | Not Allowed |
|---------|-------------|
| LONG variable | BYTE variable |
| LONG array element | WORD variable |
| LONG parameter | Bitfield variable (`LONG x : 16`) |
| LONG local | COG register with `@` (use `^@` instead) |

### What Cannot Be Method Pointers

```spin2
' These will cause compiler errors:

VAR
  BYTE badPtr1           ' Wrong type
  WORD badPtr2           ' Wrong type
  LONG badPtr3 : 20      ' Has bitfield

PUB Example()
  badPtr1 := @SomeMethod  ' ERROR
  badPtr2 := @SomeMethod  ' ERROR
  badPtr3 := @SomeMethod  ' ERROR
```

### RECV/SEND Restrictions

| Method | Can Take Parameters | Can Return Value | Can Use `\` Abort |
|--------|---------------------|------------------|-------------------|
| RECV | No | Yes (exactly 1) | No |
| SEND | Yes | No | No |

---

## Best Practices

### 1. Initialize Before Use

```spin2
VAR
  LONG callback

PUB Init()
  callback := 0           ' Explicit initialization

PUB SetCallback(handler)
  callback := handler

PUB TriggerCallback()
  if callback              ' Always check
    callback()
```

### 2. Use Constants for Dispatch Indices

```spin2
CON
  CMD_START = 0
  CMD_STOP  = 1
  CMD_PAUSE = 2

' Instead of magic numbers:
' handlers[0], handlers[1], handlers[2]

' Use named constants:
handlers[CMD_START] := @DoStart
handlers[CMD_STOP] := @DoStop
handlers[CMD_PAUSE] := @DoPause
```

### 3. Document Expected Signatures

```spin2
' Callback signature: PRI handler(eventType, eventData) : handled
VAR
  LONG eventHandler

' Comparator signature: PRI compare(a, b) : result (-1, 0, or 1)
VAR
  LONG comparator

' Transform signature: PRI transform(value) : newValue
VAR
  LONG transformer
```

### 4. Bounds Check Dispatch Indices

```spin2
PUB Dispatch(index, param) : result
  if index >= 0 and index < NUM_HANDLERS
    result := handlers[index](param)
  else
    result := DEFAULT_RESULT
```

### 5. Consider Type Safety with Wrapper Objects

For complex systems, wrap method pointers in objects that enforce signatures:

```spin2
OBJ
  callbacks : "callback_manager"

PUB Example()
  callbacks.Register(EVENT_CLICK, @OnClick)
  callbacks.Trigger(EVENT_CLICK, mouseX, mouseY)
```

---

## Summary Table

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Get local method address | `ptr := @Method` | Address of method in current object |
| Get object method address | `ptr := @obj.Method` | Address of method in child object |
| Get indexed object method | `ptr := @obj[i].Method` | Address of method in object array element |
| Call through pointer | `ptr()` | Execute method with no parameters |
| Call with parameters | `ptr(a, b, c)` | Execute method with parameters |
| Call with single return | `r := ptr()` | Execute and capture return value |
| Call with multiple returns | `x, y := ptr() : 2` | Execute and capture N return values |
| Null check | `if ptr <> 0` | Verify pointer is valid before call |
| Use RECV | `val := RECV()` | Receive from inter-cog mailbox |
| Use SEND | `SEND(val)` | Send to inter-cog mailbox |

---

## Related Documentation

- **Addressing-Usage-Guide.md** - The `@` operator and address-of semantics
- **Pointer-Usage-Guide.md** - Typed pointers (`^BYTE`, `^WORD`, `^LONG`)
- **STRUCT-Usage-Guide.md** - Structure definitions and member access

---

*This document describes method pointer usage in Spin2 as implemented in the PNut-TS compiler.*
