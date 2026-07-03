# Chapter 1: Direct I/O — The Foundation {#ch1}

Direct I/O is the fundamental layer of P2 pin control. Every pin operation—from simple LED blinking to complex smart pin configurations—ultimately depends on three core concepts: **direction**, **output state**, and **input sensing**. This chapter documents the hardware model and all Direct I/O instructions.


## 1.1 The Hardware Model

### Pin Control Registers

Each cog maintains its own set of pin control registers:

| Register | Cog Address | Function |
|----------|-------------|----------|
| DIRA | $1FA | Output enable bits for P0..P31 (active high) |
| DIRB | $1FB | Output enable bits for P32..P63 (active high) |
| OUTA | $1FC | Output state bits for P0..P31 |
| OUTB | $1FD | Output state bits for P32..P63 |
| INA | $1FE | Input state bits for P0..P31 |
| INB | $1FF | Input state bits for P32..P63 |

### The Three-State Model

Every pin operates according to three independent states:

1. **Direction (DIR)**: Controls whether the pin is an output (DIR=1) or input/floating (DIR=0)
2. **Output State (OUT)**: The logic level driven when the pin is an output
3. **Input State (IN)**: The current logic level present on the pin

**Critical relationship:** The OUT register value only affects the physical pin when DIR=1. When DIR=0, the pin floats (high impedance) and the OUT register has no effect on the pin, though the OUT value is preserved for when the pin later becomes an output.

### Multiple Cog Arbitration

Multiple cogs can control the same pin. The P2 uses OR logic to combine control signals:

- **DIR**: If any cog sets DIR=1 for a pin, the pin becomes an output
- **OUT**: The output state is the OR of all cogs' OUT bits

This means:

- Any cog can "claim" a pin by setting its DIR bit
- When multiple cogs drive the same pin, the output is high if any cog drives high

### Pin Output Driver

When DIR=1, the pin's output driver connects to the pad. The driver strength is configurable via WRPIN (see Chapter 2). The default is "fast" drive providing approximately 30mA source/sink capability.


## 1.2 Timing

### Output Timing: 3-Clock Delay

When a DIR or OUT bit is changed by any instruction, **three additional clock cycles pass** after the instruction completes before the pin begins transitioning to the new state.

```{=latex}
\DiagOutputTiming
```

**Total latency from instruction start to pin transition:** 5 clock cycles (2 for instruction execution + 3 pipeline delay).

### Input Timing via INx Registers: 3 Clocks Old

When an INx register is read by an instruction, it reflects the state of the pins registered **three clocks before** the start of the instruction.

```{=latex}
\DiagInputTimingINA
```

### Input Timing via TESTP/TESTPN: 2 Clocks Old

The TESTP and TESTPN instructions provide "fresher" input data—the value read reflects the state of the pin registered **two clocks before** the start of the instruction.

```{=latex}
\DiagInputTimingTESTP
```

**Recommendation:** Use TESTP/TESTPN for time-critical input sensing. The one-clock fresher data can matter in tight timing loops.

### Timing Summary

| Operation | Latency | Notes |
|-----------|---------|-------|
| Output change (any DRV/OUT/DIR instruction) | 3 clocks after instruction | Before pin transitions |
| Input via INx register (MOV, TESTB, etc.) | 3 clocks before instruction | Older data |
| Input via TESTP/TESTPN | 2 clocks before instruction | Fresher data |


## 1.3 Drive Instructions (DRVx)

Drive instructions set both the DIR bit (set to 1) and the OUT bit in a single atomic operation. These are the most common pin control instructions.

### Common Properties

- **Execution time:** 2 clock cycles
- **Output latency:** 3 additional clock cycles after instruction
- **Flags:** With the optional WCZ effect, C and Z are **both** set to the pin's prior OUT-bit state (its output level before the instruction executes); without WCZ, neither flag changes
- **Pin range:** D[5:0] specifies base pin (0-63); D[10:6] specifies span (0-31 additional pins)


### DRVH - Drive High

Drives pin high by setting DIR=1 and OUT=1.

```pasm-syntax
        DRVH    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to 1 (high state)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles; pin begins driving 3 clocks after instruction completes

**Spin2 Equivalent:** `PINHIGH(pin)`

**Example - Spin2:**
```spin2
CON
  LED_PIN = 56                    ' Onboard LED on P2 Eval board

PUB main()
  PINHIGH(LED_PIN)                ' Drive LED pin high (LED on)
```

**Example - PASM2:**
```pasm2
              drvh      #56       ' Drive pin 56 high
```

**Related:** DRVL, DRVNOT, OUTH, DIRH


### DRVL - Drive Low

Drives pin low by setting DIR=1 and OUT=0.

```pasm-syntax
        DRVL    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to 0 (low state)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles; pin begins driving 3 clocks after instruction completes

**Spin2 Equivalent:** `PINLOW(pin)`

**Example - Spin2:**
```spin2
CON
  LED_PIN = 56

PUB main()
  PINLOW(LED_PIN)                 ' Drive LED pin low (LED off)
```

**Example - PASM2:**
```pasm2
              drvl      #56       ' Drive pin 56 low
```

**Related:** DRVH, DRVNOT, OUTL, DIRL


### DRVNOT - Drive Toggle

Toggles the output state while keeping the pin as an output.

```pasm-syntax
        DRVNOT  {#}Dest        {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Toggle OUT bit for pin D (0→1 or 1→0)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Spin2 Equivalent:** `PINTOGGLE(pin)`

**Example - Spin2:**
```spin2
CON
  LED_PIN = 56

PUB main()
  PINHIGH(LED_PIN)                ' Start with LED on
  repeat
    WAITMS(500)                   ' Wait 500ms
    PINTOGGLE(LED_PIN)            ' Toggle LED state
```

**Example - PASM2:**
```pasm2
              drvh      #56       ' Start high
.loop
              waitx     delay     ' Wait
              drvnot    #56       ' Toggle pin 56
              jmp       #.loop
delay         long      100_000_000  ' 0.5 sec at 200 MHz
```

**Related:** DRVH, DRVL, OUTNOT


### DRVC - Drive to C

Drives pin to the current state of the C flag.

```pasm-syntax
        DRVC    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to C flag value
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (use conditional logic with PINHIGH/PINLOW)

**Example - PASM2:**
```pasm2
              testp     #10 wc    ' Read pin 10 into C
              drvc      #11       ' Drive pin 11 to same state as pin 10
```

**Related:** DRVNC, OUTC


### DRVNC - Drive to Not C

Drives pin to the inverse of the C flag.

```pasm-syntax
        DRVNC   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to !C (inverted C flag)
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (use conditional logic)

**Example - PASM2:**
```pasm2
              testp     #10 wc    ' Read pin 10 into C
              drvnc     #11       ' Drive pin 11 to opposite state
```

**Related:** DRVC, OUTNC


### DRVZ - Drive to Z

Drives pin to the current state of the Z flag.

```pasm-syntax
        DRVZ    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to Z flag value
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (use conditional logic)

**Example - PASM2:**
```pasm2
              cmp       value, #0 wz    ' Z=1 if value is zero
              drvz      #led            ' Drive LED based on Z
```

**Related:** DRVNZ, OUTZ


### DRVNZ - Drive to Not Z

Drives pin to the inverse of the Z flag.

```pasm-syntax
        DRVNZ   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to !Z (inverted Z flag)
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (use conditional logic)

**Example - PASM2:**
```pasm2
              cmp       value, #0 wz    ' Z=1 if value is zero
              drvnz     #led            ' Drive high if value != 0
```

**Related:** DRVZ, OUTNZ


### DRVRND - Drive Random

Drives pin to a random state.

```pasm-syntax
        DRVRND  {#}Dest        {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. Set OUT bit for pin D to a random value (0 or 1)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (use GETRND() with conditional logic)

**Example - PASM2:**
```pasm2
              drvrnd    #led      ' Drive LED to random state
```

**Related:** OUTRND, DIRRND


## 1.4 Output Instructions (OUTx)

Output instructions modify only the output state register bit. The direction register is unchanged. The output state only affects the physical pin when DIR=1.

### Common Properties

- **Execution time:** 2 clock cycles
- **Flags:** With the optional WCZ effect, C and Z are **both** set to the pin's prior OUT-bit state (its output level before the instruction executes); without WCZ, neither flag changes
- **Note:** If DIR=0, the instruction changes the OUT register but has no immediate effect on the pin


### OUTH - Output High

Sets the output state to high without changing direction.

```pasm-syntax
        OUTH    {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to 1
2. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)
3. DIR is unchanged

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (PINHIGH also sets direction; for OUT-only, use register access)

**Example - PASM2:**
```pasm2
              dirh      #led      ' Make pin output (once)
              ' ...later...
              outh      #led      ' Set high without touching DIR
              outl      #led      ' Set low without touching DIR
```

**Related:** OUTL, OUTNOT, DRVH


### OUTL - Output Low

Sets the output state to low without changing direction.

```pasm-syntax
        OUTL    {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to 0
2. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)
3. DIR is unchanged

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (PINLOW also sets direction)

**Example - PASM2:**
```pasm2
              outl      #led      ' Set output register low
```

**Related:** OUTH, OUTNOT, DRVL


### OUTNOT - Output Toggle

Toggles the output state without changing direction.

```pasm-syntax
        OUTNOT  {#}Dest        {WCZ}
```

**Operation:**

1. Toggle OUT bit for pin D
2. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)
3. DIR is unchanged

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None (PINTOGGLE also sets direction)

**Example - PASM2:**
```pasm2
              outnot    #led      ' Toggle output state only
```

**Related:** OUTH, OUTL, DRVNOT


### OUTC - Output to C

Sets output state to the C flag value without changing direction.

```pasm-syntax
        OUTC    {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to C flag value
2. With WCZ, set C and Z flags to the prior OUT bit state
3. DIR is unchanged

**Timing:** 2 clock cycles

**Related:** OUTNC, DRVC


### OUTNC - Output to Not C

Sets output state to the inverse of C flag without changing direction.

```pasm-syntax
        OUTNC   {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to !C
2. With WCZ, set C and Z flags to the prior OUT bit state
3. DIR is unchanged

**Timing:** 2 clock cycles

**Related:** OUTC, DRVNC


### OUTZ - Output to Z

Sets output state to the Z flag value without changing direction.

```pasm-syntax
        OUTZ    {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to Z flag value
2. With WCZ, set C and Z flags to the prior OUT bit state
3. DIR is unchanged

**Timing:** 2 clock cycles

**Related:** OUTNZ, DRVZ


### OUTNZ - Output to Not Z

Sets output state to the inverse of Z flag without changing direction.

```pasm-syntax
        OUTNZ   {#}D           {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to !Z
2. With WCZ, set C and Z flags to the prior OUT bit state
3. DIR is unchanged

**Timing:** 2 clock cycles

**Related:** OUTZ, DRVNZ


### OUTRND - Output Random

Sets output state to a random value without changing direction.

```pasm-syntax
        OUTRND  {#}Dest        {WCZ}
```

**Operation:**

1. Set OUT bit for pin D to a random value
2. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)
3. DIR is unchanged

**Timing:** 2 clock cycles

**Related:** DRVRND


## 1.5 Direction Instructions (DIRx)

Direction instructions modify only the direction register bit. The output state register is unchanged.

### Common Properties

- **Execution time:** 2 clock cycles
- **Flags:** With the optional WCZ effect, C and Z are **both** set to the pin's prior DIR-bit state (its direction before the instruction executes); without WCZ, neither flag changes


### DIRH - Direction High (Output)

Sets the pin to output mode.

```pasm-syntax
        DIRH    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 1 (output mode)
2. If WC/WZ is specified, set C and Z to the pin's prior DIR bit (otherwise leave flags unchanged)
3. OUT is unchanged; pin drives current OUT value

**Timing:** 2 clock cycles

**Spin2 Equivalent:** None directly. PINHIGH / PINLOW set DIR=1 and OUT in a single call (direction control is part of the operation, not a side effect).

**Example - PASM2:**
```pasm2
              outh      #led      ' Pre-set output high
              dirh      #led      ' Now enable output (no glitch)
```

**Related:** DIRL, DIRNOT, DRVH


### DIRL - Direction Low (Input/Float)

Sets the pin to input mode (floating).

```pasm-syntax
        DIRL    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (input mode, pin floats)
2. If WC/WZ is specified, set C and Z to the pin's prior DIR bit (otherwise leave flags unchanged)
3. OUT is unchanged

**Timing:** 2 clock cycles

**Spin2 Equivalent:** `PINFLOAT(pin)`

**Example - Spin2:**
```spin2
PUB main()
  PINFLOAT(10)                    ' Float pin 10 (high impedance)
```

**Example - PASM2:**
```pasm2
              dirl      #10       ' Float pin 10
```

**Related:** DIRH, DIRNOT, FLTL


### DIRNOT - Direction Toggle

Toggles the direction between input and output.

```pasm-syntax
        DIRNOT  {#}Dest        {WCZ}
```

**Operation:**

1. Toggle DIR bit for pin D
2. If WC/WZ is specified, set C and Z to the pin's prior DIR bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Example - PASM2:**
```pasm2
              dirnot    #10       ' Toggle pin 10 direction
```

**Related:** DIRH, DIRL


### DIRC - Direction to C

Sets direction based on C flag.

```pasm-syntax
        DIRC    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to C flag value
2. With WCZ, set C and Z flags to the prior DIR bit state

**Timing:** 2 clock cycles

**Related:** DIRNC, DRVC


### DIRNC - Direction to Not C

Sets direction based on inverse of C flag.

```pasm-syntax
        DIRNC   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to !C
2. With WCZ, set C and Z flags to the prior DIR bit state

**Timing:** 2 clock cycles

**Related:** DIRC, DRVNC


### DIRZ - Direction to Z

Sets direction based on Z flag.

```pasm-syntax
        DIRZ    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to Z flag value
2. With WCZ, set C and Z flags to the prior DIR bit state

**Timing:** 2 clock cycles

**Related:** DIRNZ, DRVZ


### DIRNZ - Direction to Not Z

Sets direction based on inverse of Z flag.

```pasm-syntax
        DIRNZ   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to !Z
2. With WCZ, set C and Z flags to the prior DIR bit state

**Timing:** 2 clock cycles

**Related:** DIRZ, DRVNZ


### DIRRND - Direction Random

Sets direction to a random value.

```pasm-syntax
        DIRRND  {#}Dest        {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to a random value
2. If WC/WZ is specified, set C and Z to the pin's prior DIR bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Related:** DRVRND, OUTRND


## 1.6 Float Instructions (FLTx)

Float instructions set the pin to input mode (DIR=0) AND pre-set the output state. This is useful for preparing the output level before switching to output mode, avoiding glitches.

### Common Properties

- **Execution time:** 2 clock cycles
- **Flags:** With the optional WCZ effect, C and Z are **both** set to the pin's prior OUT-bit state (its output level before the instruction executes); without WCZ, neither flag changes
- **Effect:** DIR=0 (floating) AND OUT=specified value


### FLTH - Float with Output High

Floats pin and pre-sets output register high.

```pasm-syntax
        FLTH    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to 1 (high)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Use Case:** Pre-set output high so that when DIRH is later executed, the pin immediately drives high without a glitch.

**Example - PASM2:**
```pasm2
              flth      #led      ' Float pin, prepare to drive high
              ' ...later...
              dirh      #led      ' Enable output - immediately high
```

**Related:** FLTL, DRVH


### FLTL - Float with Output Low

Floats pin and pre-sets output register low.

```pasm-syntax
        FLTL    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to 0 (low)
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Spin2 Equivalent:** `PINFLOAT(pin)` is approximately equivalent (floats pin)

**Example - PASM2:**
```pasm2
              fltl      #led      ' Float pin, prepare to drive low
```

**Related:** FLTH, DRVL, DIRL


### FLTNOT - Float with Output Toggle

Floats pin and toggles the output register.

```pasm-syntax
        FLTNOT  {#}Dest        {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Toggle OUT bit for pin D
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Related:** FLTH, FLTL


### FLTC - Float with Output to C

Floats pin and sets output register to C flag.

```pasm-syntax
        FLTC    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to C flag value
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Related:** FLTNC


### FLTNC - Float with Output to Not C

Floats pin and sets output register to inverse of C flag.

```pasm-syntax
        FLTNC   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to !C
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Related:** FLTC


### FLTZ - Float with Output to Z

Floats pin and sets output register to Z flag.

```pasm-syntax
        FLTZ    {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to Z flag value
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Related:** FLTNZ


### FLTNZ - Float with Output to Not Z

Floats pin and sets output register to inverse of Z flag.

```pasm-syntax
        FLTNZ   {#}D           {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to !Z
3. With WCZ, set C and Z flags to the prior OUT bit state

**Timing:** 2 clock cycles

**Related:** FLTZ


### FLTRND - Float with Output Random

Floats pin and sets output register to random value.

```pasm-syntax
        FLTRND  {#}Dest        {WCZ}
```

**Operation:**

1. Set DIR bit for pin D to 0 (float)
2. Set OUT bit for pin D to random value
3. If WC/WZ is specified, set C and Z to the pin's prior OUT bit (otherwise leave flags unchanged)

**Timing:** 2 clock cycles

**Related:** DRVRND, OUTRND


## 1.7 Test Pin Instructions

Test instructions read the physical pin state and affect the C and/or Z flags. These instructions do NOT change pin direction or output state.


### TESTP - Test Pin

Reads the physical pin state and affects C or Z flags.

```pasm-syntax
        TESTP   {#}D           WC/WZ
```

**Operation:**

1. Read the physical state of pin D
2. Apply the specified operation to C or Z flag

**Flag Operations:**

| Modifier | Effect |
|----------|--------|
| WC | C = pin state |
| WZ | Z = pin state |
| ANDC | C = C AND pin state |
| ANDZ | Z = Z AND pin state |
| ORC | C = C OR pin state |
| ORZ | Z = Z OR pin state |
| XORC | C = C XOR pin state |
| XORZ | Z = Z XOR pin state |

**Timing:** 2 clock cycles

**Input Latency:** Reads pin state from 2 clock cycles before instruction start (fresher than INx registers)

**Spin2 Equivalent:** `PINREAD(pin)`

**Example - Spin2:**
```spin2
CON
  BUTTON_PIN = 10

PUB main() | state
  repeat
    state := PINREAD(BUTTON_PIN)  ' Read button state
    if state == 0                 ' Button pressed (active low)
      PINHIGH(56)                 ' Turn on LED
    else
      PINLOW(56)                  ' Turn off LED
```

**Example - PASM2:**
```pasm2
              testp     #10 wc    ' Read pin 10 into C flag
        if_c  drvh      #56       ' If pin high, drive LED high
        if_nc drvl      #56       ' If pin low, drive LED low
```

**Related:** TESTPN


### TESTPN - Test Pin Negated

Reads the physical pin state inverted and affects C or Z flags.

```pasm-syntax
        TESTPN  {#}D           WC/WZ
```

**Operation:**

1. Read the physical state of pin D
2. Invert the value
3. Apply the specified operation to C or Z flag

**Timing:** 2 clock cycles

**Use Case:** Useful for active-low inputs (buttons, sensors) where high means "not pressed" and low means "pressed".

**Example - PASM2:**
```pasm2
              testpn    #button wc  ' C=1 if button pressed (active-low)
        if_c  call      #handle_button
```

**Related:** TESTP


## 1.8 Spin2 Pin Methods

Spin2 provides high-level methods for common pin operations. These methods execute from hub RAM and have additional overhead compared to inline PASM2.

Spin2 also accepts short-form aliases for the three most common of these: `PINH` for `PINHIGH`, `PINL` for `PINLOW`, and `PINF` for `PINFLOAT`. The two forms are interchangeable; this guide uses both.


### PINHIGH(PinField)

Drives pin(s) high.

**Function:** Sets DIR=1 and OUT=1 for specified pins

**Equivalent PASM2:** DRVH instruction

**Parameter:** PinField - Single pin number (0-63), range (Bottom..Top), or ADDPINS expression

**Example:**
```spin2
PINHIGH(56)                       ' Drive pin 56 high
PINHIGH(0..7)                     ' Drive pins 0-7 all high
PINHIGH(16 ADDPINS 3)           ' Drive pins 16-19 high
```


### PINLOW(PinField)

Drives pin(s) low.

**Function:** Sets DIR=1 and OUT=0 for specified pins

**Equivalent PASM2:** DRVL instruction

**Example:**
```spin2
PINLOW(56)                        ' Drive pin 56 low
```


### PINTOGGLE(PinField)

Toggles pin output state.

**Function:** Toggles OUT bit and sets DIR=1

**Equivalent PASM2:** DRVNOT instruction

**Example:**
```spin2
PINTOGGLE(56)                     ' Toggle pin 56
```


### PINFLOAT(PinField)

Floats pin(s) (sets to input mode).

**Function:** Sets DIR=0 for specified pins

**Equivalent PASM2:** DIRL instruction

**Example:**
```spin2
PINFLOAT(10)                      ' Float pin 10 (high impedance)
```


### PINWRITE(PinField, Value)

Writes value to pin(s).

**Function:** Sets OUT to Value and DIR=1

**Parameters:**

- PinField: Pin specification
- Value: 0 or 1 (or multi-bit value for pin ranges)

**Equivalent PASM2:** DRVL (value=0) or DRVH (value=1)

**Example:**
```spin2
PINWRITE(56, 1)                   ' Same as PINHIGH(56)
PINWRITE(56, 0)                   ' Same as PINLOW(56)
PINWRITE(0..7, %10101010)         ' Write pattern to pins 0-7
```


### PINREAD(PinField)

Reads pin input state.

**Function:** Returns current state of pin(s)

**Returns:** 0 or 1 for single pin; multi-bit value for pin ranges

**Equivalent PASM2:** TESTP (approximately)

**Example:**
```spin2
VAR
  long button_state

PUB main()
  button_state := PINREAD(10)     ' Read single pin
  
  ' For pin range, returns value with LSB = lowest pin
  byte_val := PINREAD(0..7)       ' Read 8 pins as byte
```


### PINCLEAR(PinField)

Clears smart pin configuration.

**Function:** Resets pin to normal mode (P_NORMAL)

**Equivalent PASM2:** `WRPIN #0, pin`

**Example:**
```spin2
PINCLEAR(10)                      ' Reset pin 10 to normal mode
```

**Note:** Use this to disable smart pin modes and return to basic Direct I/O.


## 1.9 Pin Span Operations

All DRV/OUT/DIR/FLT instructions support operating on multiple pins simultaneously using the span encoding in the D operand or via SETQ.

### Span Encoding

- D[5:0]: Base pin number (0-63)
- D[10:6]: Number of additional pins (0-31)

Bit 5 of the base-pin field is what selects the target port: a base pin in 0–31 lands the operation on Port A (the DIRA/OUTA registers), and 32–63 lands it on Port B (DIRB/OUTB). That is also why a span never crosses the 32-pin boundary — see *Wrap Behavior* below.

### Using SETQ for Span

```pasm2
              setq      #7        ' Set span to 8 pins (0 + 7 additional)
              drvh      #0        ' Drive pins 0-7 high
```

### Using ADDPINS for Span

`ADDPINS` sets the additional-pins field (D[10:6]) inline, without a preceding SETQ — convenient when the span is known at assembly time:

```pasm2
              drvh      #10 ADDPINS 7   ' P10..P17 high (base 10 + 7)
```

As with every span operation, an `ADDPINS` range cannot cross a 32-pin port boundary.

### Wrap Behavior

Span operations wrap within the same 32-pin port. Pins 0-31 (Port A) and 32-63 (Port B) are independent. A span starting at pin 28 with span 7 affects pins 28-31, then wraps to 0-3.


## 1.10 Instruction Quick Reference

| Instruction | Effect | DIR | OUT | Flags |
|-------------|--------|-----|-----|-------|
| **DRVH** | Drive high | 1 | 1 | C/Z=OUT |
| **DRVL** | Drive low | 1 | 0 | C/Z=OUT |
| **DRVNOT** | Drive toggle | 1 | toggle | C/Z=OUT |
| **DRVC** | Drive to C | 1 | C | C/Z=OUT |
| **DRVNC** | Drive to !C | 1 | !C | C/Z=OUT |
| **DRVZ** | Drive to Z | 1 | Z | C/Z=OUT |
| **DRVNZ** | Drive to !Z | 1 | !Z | C/Z=OUT |
| **DRVRND** | Drive random | 1 | rnd | C/Z=OUT |
| **OUTH** | Output high | - | 1 | C/Z=OUT |
| **OUTL** | Output low | - | 0 | C/Z=OUT |
| **OUTNOT** | Output toggle | - | toggle | C/Z=OUT |
| **OUTC** | Output to C | - | C | C/Z=OUT |
| **OUTNC** | Output to !C | - | !C | C/Z=OUT |
| **OUTZ** | Output to Z | - | Z | C/Z=OUT |
| **OUTNZ** | Output to !Z | - | !Z | C/Z=OUT |
| **OUTRND** | Output random | - | rnd | C/Z=OUT |
| **DIRH** | Direction output | 1 | - | C/Z=DIR |
| **DIRL** | Direction input | 0 | - | C/Z=DIR |
| **DIRNOT** | Direction toggle | toggle | - | C/Z=DIR |
| **DIRC** | Direction to C | C | - | C/Z=DIR |
| **DIRNC** | Direction to !C | !C | - | C/Z=DIR |
| **DIRZ** | Direction to Z | Z | - | C/Z=DIR |
| **DIRNZ** | Direction to !Z | !Z | - | C/Z=DIR |
| **DIRRND** | Direction random | rnd | - | C/Z=DIR |
| **FLTH** | Float, out high | 0 | 1 | C/Z=OUT |
| **FLTL** | Float, out low | 0 | 0 | C/Z=OUT |
| **FLTNOT** | Float, toggle out | 0 | toggle | C/Z=OUT |
| **FLTC** | Float, out to C | 0 | C | C/Z=OUT |
| **FLTNC** | Float, out to !C | 0 | !C | C/Z=OUT |
| **FLTZ** | Float, out to Z | 0 | Z | C/Z=OUT |
| **FLTNZ** | Float, out to !Z | 0 | !Z | C/Z=OUT |
| **FLTRND** | Float, out random | 0 | rnd | C/Z=OUT |
| **TESTP** | Test pin | - | - | C/Z=pin |
| **TESTPN** | Test pin negated | - | - | C/Z=!pin |

**Legend:** "-" = unchanged, "toggle" = inverts current value, "rnd" = random. **Flag effects (with the optional WCZ effect):** DRV/OUT/FLT set **both C and Z** to the pin's prior OUT-bit state, and DIR sets **both C and Z** to the pin's prior DIR-bit state — i.e. the output/direction level *before* the instruction executes. TESTP/TESTPN set both C and Z to the pin's input state. Without WC/WZ, no flag is written. The single value shown in the Flags column above is the value delivered to both flags. (Source: *P2 Assembly Language Reference*.)


## 1.11 Common Patterns

### LED Blink (Spin2)

```spin2
CON
  _clkfreq = 200_000_000
  LED_PIN = 56

PUB main()
  repeat
    PINTOGGLE(LED_PIN)
    WAITMS(500)
```

### LED Blink (PASM2)

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

              drvh      #56             ' Start with LED on

.loop         waitx     delay           ' Wait
              drvnot    #56             ' Toggle LED
              jmp       #.loop          ' Repeat

delay         long      100_000_000     ' 0.5 seconds at 200 MHz
```

### Button-Controlled LED (Spin2)

```{.spin2 caption="ch01-button-led.spin2"}
CON
  _clkfreq = 200_000_000
  BUTTON_PIN = 10
  LED_PIN = 56

PUB main()
  repeat
    if PINREAD(BUTTON_PIN) == 0       ' Active-low button
      PINHIGH(LED_PIN)
    else
      PINLOW(LED_PIN)
```

### Button-Controlled LED (PASM2)

```pasm2
CON
  _clkfreq = 200_000_000

DAT           org

.loop         testp     #10 wc          ' Read button into C
        if_nc drvh      #56             ' Button pressed: LED on
        if_c  drvl      #56             ' Button released: LED off
              jmp       #.loop
```

### Glitch-Free Output Start

```pasm2
              flth      #motor          ' Prepare output high, but float
              ' ... other setup ...
              dirh      #motor         ' Enable output - immediately high
```


*This chapter establishes the foundational concepts of P2 pin control. All smart pin modes (Chapters 6-19) build upon these Direct I/O principles. See Chapter 2 for enhanced pin configuration via P_ constants.*
