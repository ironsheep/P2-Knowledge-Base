# Spin2 Method Pointers and SEND/RECV - Deep Dive

## Method Pointers - The Complete Picture

### What Are Method Pointers?

Method pointers are **32-bit LONG values** that encode everything needed to call a method indirectly. Think of them as "smart function pointers" that know both WHERE the method is and WHAT object context it belongs to.

### Anatomy of a Method Pointer (32 bits)

```
[31..20] = Method index (12 bits) - Which method in the object
[19..0]  = VAR base address (20 bits) - Where the object's instance data lives
```

**Critical insight**: The VAR base contains (in its first LONG) the object's base address. This double-indirection allows a single 32-bit value to fully specify any method in any object instance.

### Creating Method Pointers

```spin2
VAR
  LONG methodPtr
  LONG handlerTable[4]

OBJ
  serial : "serial_driver"
  
PUB main()
  ' Basic method pointer to local method
  methodPtr := @localMethod
  
  ' Method pointer to child object's method
  methodPtr := @serial.tx
  
  ' Method pointer to indexed child object
  methodPtr := @motors[2].setSpeed
  
  ' Pass method pointers as parameters
  setupCallbacks(@onSuccess, @onError)
  
  ' Store in array for dispatch table
  handlerTable[0] := @handleTypeA
  handlerTable[1] := @handleTypeB
```

### Using Method Pointers

```spin2
' Call with no parameters, no returns
methodPtr()

' Call with parameters
methodPtr(100, 200)

' Call expecting return values (MUST specify count with :n)
result := methodPtr():1              ' One return value
x, y := methodPtr(param):2           ' Two return values

' Use return values as parameters to another method
x, y := POLXY(methodPtr():2)         ' Method returns r,theta for POLXY
```

### ⚠️ Critical Rule: No Compile-Time Checking!

**You MUST ensure parameter/return count matches the actual method!**

```spin2
PRI actualMethod(a, b) : result
  result := a + b

PUB main() | ptr
  ptr := @actualMethod
  
  ' WRONG - No parameters supplied
  ptr()                    ' Runtime error!
  
  ' WRONG - Wrong return count
  x, y := ptr(1, 2):2     ' Expects 2 returns, method has 1!
  
  ' CORRECT
  x := ptr(1, 2):1        ' Matches signature
```

### How Method Pointers Work Internally

1. **Each object reserves first LONG of VAR space** for object base address
2. **@method expression writes object base** into that first VAR long
3. **Method pointer combines** method index + VAR base address
4. **When called**, system uses VAR base to find object base, then method index to find code

## SEND - The Output Stream Mechanism

### Concept: Inherited Output Channel

SEND is a **special method pointer** that gets automatically inherited by all called methods. It's like having a global output stream that any method can write to without explicitly passing it around.

### Rules for SEND

1. **SEND target must accept ONE parameter and return NOTHING**
2. **SEND pointer propagates DOWN the call chain** (inherited by called methods)
3. **SEND pointer does NOT propagate UP** (returns restore previous SEND)
4. **Each method can override SEND** for its own use

### Basic SEND Usage

```spin2
PUB main()
  ' Set up SEND to point to serial output
  SEND := @serial.tx
  
  ' Now ANY method can output via SEND
  SEND("Hello ")
  SEND("World")
  SEND(13)  ' Carriage return
  
  ' Call method that also uses SEND
  printStatus()

PRI printStatus()
  ' This method inherits SEND from caller
  SEND("Status: ")
  SEND(getTemperature() + "0")  ' Convert to ASCII
  SEND(13)
```

### Advanced SEND Pattern - Multiple Values

```spin2
PUB demo()
  SEND := @SetLED
  
  REPEAT
    ' Flash() outputs via SEND, then returns $AA
    ' That $AA plus the other values all go to SetLED
    SEND(Flash(), $01, $02, $04, $08, $10, $20, $40, $80)

PRI Flash() : pattern
  REPEAT 2
    SEND($00, $FF, $00)  ' Uses inherited SEND
  RETURN $AA             ' Returns to caller

PRI SetLED(value)
  PINWRITE(56 ADDPINS 7, !value)
  WAITMS(125)
```

**Output sequence**: $00, $FF, $00, $00, $FF, $00, $AA, $01, $02, $04, $08, $10, $20, $40, $80

### SEND Inheritance Chain

```spin2
PUB level1()
  SEND := @uart.tx     ' Set SEND to UART
  level2()
  ' SEND is still @uart.tx after return

PRI level2()
  SEND("Level 2: ")    ' Uses inherited @uart.tx
  SEND := @lcd.write   ' Override for this level
  level3()
  ' SEND automatically restored to @uart.tx on return

PRI level3()
  SEND("Level 3")      ' Uses inherited @lcd.write
  ' No override here
```

## RECV - The Input Stream Mechanism

### Concept: Inherited Input Source

RECV is the input counterpart to SEND. It's a **special method pointer** for methods that return ONE value and take NO parameters.

### Rules for RECV

1. **RECV target must accept NO parameters and return ONE value**
2. **RECV pointer propagates DOWN the call chain** (inherited)
3. **RECV pointer does NOT propagate UP** (restored on return)
4. **Use RECV() to get next value** from input stream

### Basic RECV Usage

```spin2
VAR
  BYTE buffer[100]
  LONG index

PUB main()
  ' Set up RECV to read from serial
  RECV := @serial.rx
  
  ' Read characters until CR
  REPEAT
    c := RECV()
    IF c == 13
      QUIT
    buffer[index++] := c

PRI getPattern() : pattern
  ' Could read from different source
  RETURN lookupTable[index++ & 7]

PUB demo2()
  ' Switch RECV to pattern generator
  RECV := @getPattern
  
  REPEAT
    PINWRITE(56 ADDPINS 7, !RECV())  ' Get next pattern
    WAITMS(125)
```

## Practical Use Cases

### 1. Output Abstraction (SEND)

```spin2
' Terminal, LCD, or LED output - same code!
PUB outputMessage(device)
  CASE device
    0: SEND := @terminal.tx
    1: SEND := @lcd.writeChar  
    2: SEND := @led.showByte
    
  ' Same output code regardless of device
  SEND("Hello")
  SEND(" ")
  SEND("World")
```

### 2. Input Abstraction (RECV)

```spin2
' Read from keyboard, serial, or test pattern
PUB processInput(source)
  CASE source
    0: RECV := @keyboard.getKey
    1: RECV := @serial.rx
    2: RECV := @testPattern.next
    
  ' Process input the same way
  REPEAT 100
    data[i++] := RECV()
```

### 3. Dispatch Tables (Method Pointers)

```spin2
VAR
  LONG commandTable[10]
  
PUB setupCommands()
  commandTable[0] := @cmdHelp
  commandTable[1] := @cmdStatus
  commandTable[2] := @cmdReset
  commandTable[3] := @cmdConfig
  
PUB executeCommand(cmdNum, param)
  IF cmdNum < 10
    commandTable[cmdNum](param):0  ' Call via pointer
```

### 4. Event Handlers

```spin2
VAR
  LONG onButtonPress
  LONG onTimeout
  LONG onDataReady
  
PUB registerHandlers(button, timeout, data)
  onButtonPress := button
  onTimeout := timeout
  onDataReady := data
  
PUB mainLoop()
  IF buttonPressed
    onButtonPress():0
  IF timedOut
    onTimeout():0
  IF dataAvailable
    result := onDataReady():1
```

### 5. Plugin Architecture

```spin2
OBJ
  plugins[4] : "plugin_base"
  
VAR
  LONG processFunc[4]
  
PUB loadPlugin(slot, filename)
  ' Hypothetical dynamic loading
  plugins[slot].load(filename)
  processFunc[slot] := @plugins[slot].process
  
PUB runPlugins(data) | i
  REPEAT i FROM 0 TO 3
    IF processFunc[i]
      data := processFunc[i](data):1
```

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting Return Count

```spin2
' WRONG - No return count specified
result := methodPtr()        ' Assumes no return!

' RIGHT - Specify return count
result := methodPtr():1      ' Explicitly expect 1 return
```

### Pitfall 2: SEND/RECV Signature Mismatch

```spin2
' WRONG - tx might take parameters and return values
SEND := @serial.tx(9600)     ' Don't call it!

' RIGHT - Just the address
SEND := @serial.tx           ' No parentheses
```

### Pitfall 3: Method Pointer Scope

```spin2
VAR
  LONG globalPtr
  
PUB main()
  setupPointer()
  globalPtr():0               ' This works
  
PRI setupPointer() | localMethod
  ' WRONG - localMethod only exists in this method
  globalPtr := @localMethod   ' Won't work!
  
  ' RIGHT - Point to persistent method
  globalPtr := @persistentMethod
```

### Pitfall 4: Cross-Object Pointers

```spin2
' Method pointers include object context
' You can safely pass them between objects

OBJ
  handler : "event_handler"
  
PUB main()
  ' This works - pointer includes object context
  handler.setCallback(@myCallback)
  
PRI myCallback(value)
  ' Handler can call this via pointer
```

## Why SEND/RECV Matter

### Traditional Approach (Without SEND/RECV)

```spin2
' Must pass output method everywhere
PUB printData(outputMethod, data)
  outputMethod("Data: ")
  outputMethod(data)
  printDetails(outputMethod)  ' Must pass along
  
PRI printDetails(outputMethod)
  outputMethod("Details...")
  ' Every method needs the parameter
```

### With SEND/RECV

```spin2
' Clean, no parameter passing needed
PUB printData(data)
  SEND("Data: ")
  SEND(data)  
  printDetails()  ' No parameters needed
  
PRI printDetails()
  SEND("Details...")  ' Automatically uses inherited SEND
```

## Advanced Technique: Bidirectional Streams

```spin2
PUB interactive()
  ' Set up bidirectional communication
  SEND := @terminal.tx
  RECV := @terminal.rx
  
  ' Now any called method can do I/O
  SEND("Enter command: ")
  cmd := RECV()
  
  CASE cmd
    "h": showHelp()      ' These inherit SEND/RECV
    "s": showStatus()    ' No parameters needed!
    "c": configure()     ' Clean and simple

PRI showHelp()
  SEND("Commands: h=help, s=status, c=config")
  SEND(13)

PRI configure()
  SEND("Enter new value: ")
  value := RECV()  ' Inherited from caller
  SEND("Set to: ")
  SEND(value)
```

## Summary: Key Concepts

1. **Method pointers are complete** - They encode both method location AND object context
2. **SEND/RECV are inherited** - Automatically passed down call chain
3. **No compile-time checking** - You must ensure signatures match
4. **Restoration is automatic** - SEND/RECV restored when methods return
5. **Powerful abstraction** - Decouple I/O from business logic
6. **Dispatch tables work** - Build jump tables, event handlers, plugins
7. **Cross-object safe** - Method pointers work between objects

These features enable sophisticated patterns like plugin architectures, event-driven systems, and clean I/O abstraction that would be much more verbose in other embedded languages.