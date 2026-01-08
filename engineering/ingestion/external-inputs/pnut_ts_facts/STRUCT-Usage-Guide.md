# STRUCT Usage Guide for Spin2/PASM2

This document describes the `STRUCT` feature in Spin2/PASM2, which allows you to define composite data types containing multiple named members. Structures provide a way to organize related data into logical units with convenient member access syntax.

## Language Version Requirement

**STRUCT is a language extension that requires Spin2 version 45 or later.**

To use structures in your code, you must include the language version directive at the very beginning of your source file:

```spin2
{Spin2_v45}
CON
  STRUCT point(x, y)
  ' ... rest of your code
```

The directive `{Spin2_v45}` (or a later version like `{Spin2_v51}`) must appear before any other code. Without this directive, the compiler will not recognize the `STRUCT` keyword.

## Overview

Structures in Spin2 allow you to:
- Define custom data types with named members
- Use typed members (BYTE, WORD, LONG, or other STRUCTs)
- Create arrays of structure instances
- Access structure members using dot notation
- Use structure pointers for dynamic access
- Pass structures to and return structures from methods

## Defining Structures

### Basic Syntax

Structures are defined in a `CON` block using the `STRUCT` keyword:

```spin2
CON
  STRUCT structName(member1, member2, ...)
```

### Default Member Type

Without an explicit type, members default to `LONG` (4 bytes):

```spin2
CON
  STRUCT point(x, y)           ' x and y are both LONGs (8 bytes total)
```

### Typed Members

Specify member types with `BYTE`, `WORD`, or `LONG`:

```spin2
CON
  STRUCT tinyPoint(BYTE x, BYTE y)           ' 2 bytes total
  STRUCT mediumPoint(WORD x, WORD y)         ' 4 bytes total
  STRUCT fullPoint(LONG x, LONG y)           ' 8 bytes total
```

### Mixed Types

Mix different types in a single structure:

```spin2
CON
  STRUCT colorPoint(WORD x, WORD y, BYTE color)   ' 5 bytes total
  STRUCT sensor(BYTE id, WORD value, LONG timestamp)
```

### Array Members

Members can be arrays:

```spin2
CON
  STRUCT buffer(BYTE data[256])              ' 256 bytes
  STRUCT bigData(values[4])                  ' 4 LONGs = 16 bytes
  STRUCT matrix(WORD row[4], WORD col[4])    ' 16 bytes
```

### Nested Structures

Structures can contain other structures as members:

```spin2
CON
  STRUCT point(x, y)
  STRUCT line(point a, point b)              ' Contains two points (16 bytes)
  STRUCT triangle(point p1, point p2, point p3)
```

### Complex Nested Structures

Combine nested structures with arrays:

```spin2
CON
  STRUCT BIG(n[4])                           ' 128-bit value (4 LONGs)
  STRUCT MotorCmd(cycl, BIG jerk)            ' cycle count + 128-bit jerk
  STRUCT MotorCmds(MotorCmd cmd[8])          ' Array of 8 commands
```

### Structure Assignment (Aliases)

Create an alias for an existing structure:

```spin2
CON
  STRUCT point(x, y)
  STRUCT coordinate = point                   ' Alias for point
```

---

## Declaring Structure Variables

### VAR Block Declarations

Declare structure variables in a `VAR` block:

```spin2
CON
  STRUCT point(x, y)
  STRUCT line(point a, point b)

VAR
  point myPoint                              ' Single point instance
  point points[10]                           ' Array of 10 points
  line myLine                                ' Single line instance
  line lines[5]                              ' Array of 5 lines
```

### Local Variables

Declare structure locals after `|` in methods:

```spin2
PUB Calculate() | point p1, point p2, line segment
  p1.x := 0
  p1.y := 0
  p2.x := 100
  p2.y := 100
  segment.a := p1
  segment.b := p2
```

### Parameters

Structures can be method parameters:

```spin2
PUB DrawLine(line segment)
  ' Draw from segment.a to segment.b
  drawPixel(segment.a.x, segment.a.y)
  drawPixel(segment.b.x, segment.b.y)

PUB ProcessPoints(point pts[10])
  ' Process array of 10 points
```

### Return Values

Methods can return structures:

```spin2
PUB GetOrigin() : point result
  result.x := 0
  result.y := 0

PUB GetEndpoints(line seg) : point start, point finish
  start := seg.a
  finish := seg.b
```

---

## Accessing Structure Members

### Dot Notation

Access members using the `.` operator:

```spin2
VAR
  point p

PUB Example()
  p.x := 100                                 ' Write to member
  p.y := 200
  value := p.x                               ' Read from member
```

### Nested Member Access

Access nested structure members with chained dots:

```spin2
VAR
  line myLine

PUB Example()
  myLine.a.x := 0                            ' Access point a's x
  myLine.a.y := 0                            ' Access point a's y
  myLine.b.x := 100                          ' Access point b's x
  myLine.b.y := 100                          ' Access point b's y
```

### Array Member Access

Access array members with indices:

```spin2
CON
  STRUCT buffer(BYTE data[256])

VAR
  buffer buf

PUB Example()
  buf.data[0] := $FF                         ' First byte
  buf.data[255] := $00                       ' Last byte
```

### Combined Array and Member Access

```spin2
VAR
  point points[10]

PUB Example()
  points[0].x := 100                         ' First point's x
  points[0].y := 200                         ' First point's y
  points[9].x := 0                           ' Last point's x
```

---

## Structure Pointers

### Declaring Pointers

Use `^` prefix to declare structure pointers:

```spin2
CON
  STRUCT point(x, y)

VAR
  ^point pPoint                              ' Pointer to a point
  ^line pLine                                ' Pointer to a line
```

### Pointer Parameters and Returns

```spin2
PUB ProcessPoint(^point p)
  p.x := p.x * 2
  p.y := p.y * 2

PUB GetPointer() : ^point result
  result := @myPoint
```

### Dereferencing Pointers

Access the structure a pointer points to using brackets:

```spin2
VAR
  ^point ptr
  point storage

PUB Example() | value
  ptr := @storage                            ' Point to storage

  ' Access members through pointer
  ptr.x := 100                               ' Write through pointer
  ptr.y := 200
  value := ptr.x                             ' Read through pointer

  ' Dereference entire structure
  value := [ptr]                             ' Get pointed-to structure
  [ptr] := anotherPoint                      ' Assign to pointed-to structure
```

### Pointer Arithmetic

Pointers support increment/decrement to move between array elements:

```spin2
VAR
  point points[10]
  ^point ptr

PUB Example()
  ptr := @points[0]                          ' Point to first element

  ' Post-increment/decrement
  ptr.x := 0                                 ' Access current element
  ptr[++].x := 1                             ' Access current, then advance
  ptr[--].x := 2                             ' Access current, then go back

  ' Pre-increment/decrement
  [++]ptr.x := 3                             ' Advance, then access
  [--]ptr.x := 4                             ' Go back, then access

  ' Reading with post-increment
  value := ptr[++].x                         ' Read x, advance to next
```

### Pointer Increment Size

When incrementing a structure pointer, it advances by the structure's size:

```spin2
CON
  STRUCT point(x, y)                         ' 8 bytes

VAR
  ^point ptr

PUB Example()
  ptr++                                      ' Advances by 8 bytes
  ptr--                                      ' Goes back 8 bytes
```

---

## Structure Operations

### Assignment

Copy one structure to another:

```spin2
VAR
  point p1, p2

PUB Example()
  p1.x := 100
  p1.y := 200
  p2 := p1                                   ' Copy all members
```

For structures larger than 15 LONGs (60 bytes), assignment uses `BYTEMOVE` internally.

### Multi-Value Assignment

Initialize multiple members at once:

```spin2
VAR
  point p
  line seg

PUB Example()
  p := 100, 200                              ' x := 100, y := 200
  seg := 0, 0, 100, 100                      ' a.x, a.y, b.x, b.y
```

### Swap

Swap two structures using `:=:`:

```spin2
VAR
  point p1, p2

PUB Example()
  p1 := 100, 200
  p2 := 300, 400
  p1 :=: p2                                  ' Swap p1 and p2
  ' Now p1 is (300, 400) and p2 is (100, 200)
```

### Clear and Set All

Clear all members to zero or set all bits:

```spin2
VAR
  point p

PUB Example()
  p~                                         ' Clear: all members := 0
  p~~                                        ' Set: all bits := 1
```

### Comparison

Compare structures for equality:

```spin2
VAR
  point p1, p2

PUB Example() | same
  p1 := 100, 200
  p2 := 100, 200

  if p1 == p2                                ' Test equality
    ' Structures are identical

  if p1 <> p2                                ' Test inequality
    ' Structures differ
```

---

## SIZEOF Operator

Get the size of a structure in bytes using `SIZEOF()`:

```spin2
CON
  STRUCT point(x, y)                         ' 8 bytes
  STRUCT bigStruct(data[100])                ' 400 bytes

PUB Example() | size
  size := SIZEOF(point)                      ' Returns 8
  size := SIZEOF(bigStruct)                  ' Returns 400

  ' Can also use with variables
  size := SIZEOF(myPoint)                    ' Returns size of myPoint's type
```

### SIZEOF in PASM2

Use `SIZEOF()` for memory calculations in assembly:

```pasm2
DAT
        ORG

        ' Reserve space for structures
        res     SIZEOF(point) / 4            ' Reserve LONGs for point

        ' Calculate offsets
        add     ptr, #SIZEOF(MotorCmd)       ' Advance by structure size
```

---

## DAT Block Usage

### Structure Declarations in DAT

Declare structure storage in DAT blocks:

```spin2
CON
  STRUCT line(point a, point b)

DAT
  myLine  LINE                               ' Allocate structure space
          LONG    0, 0                       ' Initialize a.x, a.y
          LONG    100, 100                   ' Initialize b.x, b.y
```

### Structure Arrays in DAT

```spin2
DAT
  points  POINT[10]                          ' Array of 10 points (80 bytes)
```

---

## Practical Examples

### 2D Graphics Point/Line

```spin2
CON
  STRUCT point(WORD x, WORD y)
  STRUCT line(point start, point finish)
  STRUCT rect(point topLeft, point bottomRight)

VAR
  rect screenBounds
  line drawLines[100]
  LONG lineCount

PUB Initialize()
  screenBounds.topLeft := 0, 0
  screenBounds.bottomRight := 319, 239
  lineCount := 0

PUB AddLine(WORD x1, WORD y1, WORD x2, WORD y2)
  if lineCount < 100
    drawLines[lineCount].start := x1, y1
    drawLines[lineCount].finish := x2, y2
    lineCount++

PUB DrawAllLines() | i
  repeat i from 0 to lineCount - 1
    DrawLine(drawLines[i])

PRI DrawLine(line seg)
  ' Draw line from seg.start to seg.finish
  ' ... implementation ...
```

### Motor Control with Nested Structures

```spin2
CON
  MotorCount = 4
  CmdQueueSize = 8

  STRUCT BIG(n[4])                           ' 128-bit value
  STRUCT MotorCmd(cycl, BIG jerk)            ' Command: cycles + jerk
  STRUCT MotorCmds(MotorCmd cmd[CmdQueueSize])
  STRUCT MotorStat(tail, cycl, BIG jerk, BIG acel, BIG velo, BIG posi)
  STRUCT MotorSystem(
    head[MotorCount],                        ' Queue heads
    MotorCmds cmds[MotorCount],              ' Command queues
    MotorStat stat[MotorCount]               ' Status for each motor
  )

VAR
  MotorSystem motors

PUB SetCommand(motor, cycles, BIG jerkValue) | head
  head := motors.head[motor]
  motors.cmds[motor].cmd[head].cycl := cycles
  motors.cmds[motor].cmd[head].jerk := jerkValue
  motors.head[motor]++

PUB GetPosition(motor) : BIG position
  position := motors.stat[motor].posi
```

### Sensor Data Collection

```spin2
CON
  MAX_SENSORS = 8

  STRUCT sensor(
    BYTE  id,
    BYTE  type,
    WORD  value,
    LONG  timestamp,
    BYTE  status
  )

  STRUCT sensorArray(
    BYTE count,
    sensor sensors[MAX_SENSORS]
  )

VAR
  sensorArray allSensors

PUB AddSensor(BYTE sensorId, BYTE sensorType) : BYTE index
  if allSensors.count < MAX_SENSORS
    index := allSensors.count
    allSensors.sensors[index].id := sensorId
    allSensors.sensors[index].type := sensorType
    allSensors.sensors[index].status := 0
    allSensors.count++
  else
    index := -1

PUB UpdateSensor(BYTE index, WORD newValue)
  allSensors.sensors[index].value := newValue
  allSensors.sensors[index].timestamp := getct()
  allSensors.sensors[index].status := 1

PUB GetSensorData(BYTE index) : sensor data
  data := allSensors.sensors[index]
```

---

## Structure Size Calculation

Structure sizes are calculated by summing member sizes:

| Member Type | Size |
|-------------|------|
| `BYTE`      | 1 byte |
| `WORD`      | 2 bytes |
| `LONG`      | 4 bytes |
| `BYTE[n]`   | n bytes |
| `WORD[n]`   | n * 2 bytes |
| `LONG[n]`   | n * 4 bytes |
| `structName`| Size of that structure |
| `structName[n]` | n * size of that structure |

### Examples

```spin2
CON
  STRUCT tiny(BYTE a, BYTE b)                ' 2 bytes
  STRUCT small(WORD x, WORD y)               ' 4 bytes
  STRUCT medium(x, y)                        ' 8 bytes (2 LONGs)
  STRUCT big(data[10])                       ' 40 bytes (10 LONGs)
  STRUCT complex(tiny t, small s, medium m)  ' 2 + 4 + 8 = 14 bytes
```

---

## Summary Table

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Define structure | `STRUCT name(members)` | Create new structure type |
| Typed member | `BYTE x` / `WORD x` / `LONG x` | Specify member type |
| Array member | `data[n]` | Array of n elements |
| Nested structure | `otherStruct member` | Include another structure |
| Alias | `STRUCT new = existing` | Create type alias |
| Declare variable | `structName varName` | Instance of structure |
| Declare array | `structName arr[n]` | Array of structures |
| Declare pointer | `^structName ptr` | Pointer to structure |
| Access member | `var.member` | Read/write member |
| Nested access | `var.nested.member` | Access nested member |
| Array element | `arr[i].member` | Access element's member |
| Pointer access | `ptr.member` | Access through pointer |
| Dereference | `[ptr]` | Get/set pointed structure |
| Pointer increment | `ptr[++]` / `[++]ptr` | Pre/post increment |
| Assign | `a := b` | Copy structure |
| Multi-assign | `s := v1, v2, ...` | Assign multiple members |
| Swap | `a :=: b` | Swap two structures |
| Clear | `s~` | Zero all members |
| Set all | `s~~` | Set all bits |
| Compare | `a == b` / `a <> b` | Test equality |
| Size | `SIZEOF(type)` | Get structure size in bytes |

---

## Best Practices

1. **Use appropriate member types**: Choose `BYTE`, `WORD`, or `LONG` based on the data range to conserve memory.

2. **Group related data**: Use structures to keep related variables together for better code organization.

3. **Pass large structures by pointer**: For structures larger than a few LONGs, pass pointers instead of copying.

4. **Use SIZEOF for portable code**: When calculating buffer sizes or offsets, use `SIZEOF()` instead of hardcoding sizes.

5. **Initialize structures**: Always initialize structure members before use; use multi-value assignment for convenience.

6. **Avoid deeply nested structures**: While supported, deeply nested structures can be harder to read and maintain.

7. **Document structure layouts**: For structures used in inter-cog communication or hardware interfaces, document the exact layout.

---

*This document describes STRUCT usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
