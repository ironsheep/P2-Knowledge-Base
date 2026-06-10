# Special Registers

The P2 provides a set of special-purpose registers that enable critical system functions including Hub RAM access, I/O control, interrupt handling, and timing operations. These registers fall into three categories: dual-purpose registers that can also serve as general RAM, fixed special registers with dedicated hardware functions, and non-memory-mapped registers accessed through specific instructions.

## Register Architecture

The P2's special register architecture provides a balance between functionality and flexibility. Each cog has its own independent copy of all special registers, allowing parallel operation without interference. Changes to these registers take effect immediately, enabling precise control over timing-critical operations.

### Memory Map ($1F0-$1FF) {#special-registers-map}

The top 16 locations of cog RAM are reserved for special registers:

```{=latex}
\SpecialRegistersMapDiagram
```

::: {.figurecaption #fig:special-registers-map-part2}
Figure R.1: Special Registers Memory Map ($1F0–$1FF)
:::

### Dual-Purpose vs. Fixed Registers

**Dual-purpose registers** ($1F0-$1F7) can be used as general-purpose cog RAM when their special functions are not enabled. This provides eight additional general-purpose registers for programs that do not use interrupts or the PA/PB facilities.

**Fixed special registers** ($1F8-$1FF) always provide their special functions when accessed. These registers implement hardware behaviors that activate whenever the register is read or written.

## Dual-Purpose Registers

### IJMP3 {#ijmp3}

Address $1F0. Interrupt 3 call address. Stores the address where execution jumps when interrupt 3 is triggered.

**Access**: Read/Write

**Usage**: When the INT3 event is triggered, the cog saves the current PC in IRET3 and jumps to the address stored in IJMP3. This register can be used as general RAM when interrupt 3 is not enabled.

**Example**:
```pasm2
        mov     IJMP3, ##int3_handler   ' Set INT3 handler address
        setint3 #event_ct1              ' Enable INT3 for CT1 event
```

**Related**: [IRET3](#iret3), SETINT3, RETI3



### IRET3 {#iret3}

Address $1F1. Interrupt 3 return address. Stores the return address when interrupt 3 is triggered.

**Access**: Read/Write

**Usage**: When INT3 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI3 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 3 is not enabled.

**Example**:
```pasm2
int3_handler
        ' Handle interrupt...
        reti3                           ' Return to saved address in IRET3
```

**Related**: [IJMP3](#ijmp3), SETINT3, RETI3



### IJMP2 {#ijmp2}

Address $1F2. Interrupt 2 call address. Stores the address where execution jumps when interrupt 2 is triggered.

**Access**: Read/Write

**Usage**: When the INT2 event is triggered, the cog saves the current PC in IRET2 and jumps to the address stored in IJMP2. This register can be used as general RAM when interrupt 2 is not enabled.

**Example**:
```pasm2
        mov     IJMP2, ##int2_handler   ' Set INT2 handler address
        setint2 #event_ct2              ' Enable INT2 for CT2 event
```

**Related**: [IRET2](#iret2), SETINT2, RETI2



### IRET2 {#iret2}

Address $1F3. Interrupt 2 return address. Stores the return address when interrupt 2 is triggered.

**Access**: Read/Write

**Usage**: When INT2 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI2 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 2 is not enabled.

**Example**:
```pasm2
int2_handler
        ' Handle interrupt...
        reti2                           ' Return to saved address in IRET2
```

**Related**: [IJMP2](#ijmp2), SETINT2, RETI2



### IJMP1 {#ijmp1}

Address $1F4. Interrupt 1 call address. Stores the address where execution jumps when interrupt 1 is triggered.

**Access**: Read/Write

**Usage**: When the INT1 event is triggered, the cog saves the current PC in IRET1 and jumps to the address stored in IJMP1. This register can be used as general RAM when interrupt 1 is not enabled.

**Example**:
```pasm2
        mov     IJMP1, ##int1_handler   ' Set INT1 handler address
        setint1 #event_ct3              ' Enable INT1 for CT3 event
```

**Related**: [IRET1](#iret1), SETINT1, RETI1



### IRET1 {#iret1}

Address $1F5. Interrupt 1 return address. Stores the return address when interrupt 1 is triggered.

**Access**: Read/Write

**Usage**: When INT1 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI1 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 1 is not enabled.

**Example**:
```pasm2
int1_handler
        ' Handle interrupt...
        reti1                           ' Return to saved address in IRET1
```

**Related**: [IJMP1](#ijmp1), SETINT1, RETI1



### PA {#pa}

Address $1F6. Multi-purpose register A. Serves multiple special functions or can be used as general RAM.

**Access**: Read/Write

**Usage**: PA serves three primary special functions:

1. **CALLD immediate return address storage**: When using CALLD with PA as the destination, return information is stored here.
2. **CALLPA parameter passing**: The CALLPA instruction copies a value to PA before calling a routine.
3. **LOC address storage**: The LOC instruction can store an address in PA.

When these functions are not needed, PA can be used as general-purpose cog RAM.

**Example**:
```pasm2
        calld   PA, #subroutine         ' Return info in PA, call
        callpa  param, #handler         ' Copy param to PA, call
        loc     PA, #label              ' Store label address in PA

        ' Using PA as general RAM
        mov     PA, #42                 ' Regular register usage
```

**Related**: [PB](#pb), CALLD, CALLPA, LOC



### PB {#pb}

Address $1F7. Multi-purpose register B. Serves multiple special functions or can be used as general RAM.

**Access**: Read/Write

**Usage**: PB serves three primary special functions:

1. **CALLD immediate return address storage**: When using CALLD with PB as the destination, return information is stored here.
2. **CALLPB parameter passing**: The CALLPB instruction copies a value to PB before calling a routine.
3. **LOC address storage**: The LOC instruction can store an address in PB.

When these functions are not needed, PB can be used as general-purpose cog RAM.

**Example**:
```pasm2
        calld   PB, #subroutine         ' Return info in PB, call
        callpb  param, #handler         ' Copy param to PB, call
        loc     PB, #label              ' Store label address in PB

        ' Using PB as general RAM
        mov     PB, ##hub_addr          ' Regular register usage
```

**Related**: [PA](#pa), CALLD, CALLPB, LOC



## Communication Registers (PR0-PR7) {#pr0-pr7}

Addresses $1D8-$1DF. Eight general-purpose registers with predefined symbols.

**Access**: Read/Write

**Memory Map**:

| Address | Register |
|---------|----------|
| $1D8 | PR0 |
| $1D9 | PR1 |
| $1DA | PR2 |
| $1DB | PR3 |
| $1DC | PR4 |
| $1DD | PR5 |
| $1DE | PR6 |
| $1DF | PR7 |

**Usage**: For standalone PASM2 programs, these are ordinary general-purpose registers available for any purpose. The compiler reserves the symbols PR0-PR7 as aliases for these addresses.

**Note**: The PR0-PR7 symbols exist primarily for Spin2 inline assembly interoperability. See the Spin2 Language Manual for Spin2/PASM2 communication patterns.



## Fixed Special Registers

### PTRA {#ptra}

Address $1F8. Pointer A to Hub RAM. Primary pointer register for Hub RAM access with automatic increment/decrement support.

**Access**: Read/Write

**Usage**: PTRA is the primary pointer for Hub RAM operations. It supports indexed addressing modes with automatic pre- and post-increment/decrement, making it ideal for sequential memory access patterns. PTRA is a 32-bit register; its low 20 bits address the full 1 MB Hub RAM space. On COGINIT, the target cog's PTRA receives the SETQ value (typically a parameter-block hub address) if a SETQ was executed immediately before the COGINIT; otherwise PTRA is cleared to 0. This is the standard P2 mechanism for passing a 32-bit parameter or data-structure pointer to a launched cog.

**Addressing Modes**:

The increment/decrement amount (SCALE) depends on the instruction:

| Instruction | SCALE | Increment/Decrement |
|-------------|-------|---------------------|
| RDBYTE, WRBYTE | 1 | 1 byte |
| RDWORD, WRWORD | 2 | 2 bytes |
| RDLONG, WRLONG, WMLONG | 4 | 4 bytes |

- `PTRA++` — Post-increment by SCALE bytes
- `PTRA--` — Post-decrement by SCALE bytes
- `++PTRA` — Pre-increment by SCALE bytes
- `--PTRA` — Pre-decrement by SCALE bytes
- `PTRA[index]` — Indexed access: address = PTRA + (index × SCALE)
- `PTRA++[index]` — Post-update indexed: use PTRA, then PTRA += index × SCALE
- `++PTRA[index]` — Pre-update indexed: PTRA += index × SCALE, then use PTRA

Index ranges: -32 to +31 for non-updating indexed; 1 to 16 for updating forms.

**Example**:
```pasm2
        mov     ptra, ##hub_buffer      ' Set PTRA to Hub address
        rdlong  data, ptra++            ' Read long, PTRA += 4 (SCALE=4 for RDLONG)
        rdbyte  char, ptra++            ' Read byte, PTRA += 1 (SCALE=1 for RDBYTE)
        wrlong  data, ptra[4]           ' Address: PTRA + (4 × 4) = PTRA+16

        ' Block transfer using SETQ
        setq    #15                     ' Transfer 16 longs
        rdlong  cog_buffer, ptra++      ' Read 16 longs, auto-inc
```

**Related**: [PTRB](#ptrb), RDLONG, WRLONG, RDBYTE, RDWORD, SETQ



### PTRB {#ptrb}

Address $1F9. Pointer B to Hub RAM. Secondary pointer register for Hub RAM access with automatic increment/decrement support.

**Access**: Read/Write

**Usage**: PTRB is the secondary pointer for Hub RAM operations, providing the same capabilities as PTRA. Having two independent pointers enables efficient dual-buffer operations and complex memory access patterns. COGINIT writes the code start address to the target cog's PTRB, enabling position-independent code.

**Addressing Modes**:

PTRB supports the same addressing modes as PTRA, with SCALE determined by instruction type (see PTRA for details):

- `PTRB++` — Post-increment by SCALE bytes
- `PTRB--` — Post-decrement by SCALE bytes
- `++PTRB` — Pre-increment by SCALE bytes
- `--PTRB` — Pre-decrement by SCALE bytes
- `PTRB[index]` — Indexed access: address = PTRB + (index × SCALE)
- `PTRB++[index]` — Post-update indexed: use PTRB, then PTRB += index × SCALE
- `++PTRB[index]` — Pre-update indexed: PTRB += index × SCALE, then use PTRB

**Example**:
```pasm2
        mov     ptrb, ##hub_source      ' Set PTRB to source address
        rdlong  data, ptrb++            ' Read long, PTRB += 4 (SCALE=4)
        rdword  wval, ptrb++            ' Read word, PTRB += 2 (SCALE=2)
        wrlong  data, ptrb[8]           ' Address: PTRB + (8 × 4) = PTRB+32

        ' COGINIT sets PTRB in launched cog
        coginit cognumber, ##code_addr  ' PTRB in target cog gets code_addr
```

**Related**: [PTRA](#ptra), RDLONG, WRLONG, COGINIT



### DIRA {#dira}

Address $1FA. Direction register A for pins 0-31. Controls whether each pin is an input or output.

**Access**: Read/Write

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | DIR | Direction for each pin: 1 = output, 0 = input |

**Usage**: DIRA controls the direction of pins 0-31. Setting a bit to 1 configures the corresponding pin as an output, while 0 configures it as an input. Changes take effect immediately. When a pin is configured as an output, the value in the corresponding OUTA bit is driven onto the pin. When configured as an input, the pin state can be read from INA.

**Example**:
```pasm2
        mov     DIRA, ##$00FF_0000      ' Set pins 16-23 as outputs
        or      DIRA, #1                ' Set pin 0 as output
        andn    DIRA, ##$0000_00FF      ' Set pins 0-7 as inputs

        ' Atomic direction change
        mov     DIRA, new_directions    ' Change all 32 directions
```

**Related**: [DIRB](#dirb), [OUTA](#outa), [INA](#ina), DIRC, DIRH, DIRL



### DIRB {#dirb}

Address $1FB. Direction register B for pins 32-63. Controls whether each pin is an input or output.

**Access**: Read/Write

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | DIR | Direction for each pin: 1 = output, 0 = input |

**Usage**: DIRB controls the direction of pins 32-63. Setting a bit to 1 configures the corresponding pin as an output, while 0 configures it as an input. The bit positions map to pins 32-63, where bit 0 controls pin 32 and bit 31 controls pin 63.

**Example**:
```pasm2
        mov     DIRB, #0                ' Set all pins 32-63 as inputs
        or      DIRB, ##$8000_0000      ' Set pin 63 as output
        andn    DIRB, ##$0000_FFFF      ' Set pins 32-47 as inputs
```

**Related**: [DIRA](#dira), [OUTB](#outb), [INB](#inb)



### OUTA {#outa}

Address $1FC. Output register A for pins 0-31. Sets the output state for pins configured as outputs.

**Access**: Read/Write

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | OUT | Output state for each pin: 1 = high, 0 = low |

**Usage**: OUTA sets the output state for pins 0-31. Only affects pins configured as outputs via DIRA. Reading OUTA returns the current output register state, not the actual pin states (use INA to read pin states). When multiple cogs drive the same pin, the outputs are OR'd together—if any cog outputs high, the pin goes high.

**Example**:
```pasm2
        mov     OUTA, #0                ' Clear all outputs 0-31
        or      OUTA, #1                ' Set pin 0 high
        xor     OUTA, ##$0000_00FF      ' Toggle pins 0-7
        andn    OUTA, pin_mask          ' Clear specific outputs

        ' Atomic pattern change
        mov     OUTA, new_pattern       ' Change all 32 outputs atomically
```

**Related**: [OUTB](#outb), [DIRA](#dira), [INA](#ina), OUTC, OUTH, OUTL



### OUTB {#outb}

Address $1FD. Output register B for pins 32-63. Sets the output state for pins configured as outputs.

**Access**: Read/Write

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | OUT | Output state for each pin: 1 = high, 0 = low |

**Usage**: OUTB sets the output state for pins 32-63. Only affects pins configured as outputs via DIRB. The bit positions map to pins 32-63, where bit 0 controls pin 32 and bit 31 controls pin 63. When multiple cogs drive the same pin, the outputs are OR'd together.

**Example**:
```pasm2
        mov     OUTB, pattern           ' Set output pattern for pins 32-63
        andn    OUTB, mask              ' Clear specific outputs
        or      OUTB, ##$8000_0000      ' Set pin 63 high
        xor     OUTB, toggle_mask       ' Toggle specific pins
```

**Related**: [OUTA](#outa), [DIRB](#dirb), [INB](#inb)



### INA {#ina}

Address $1FE. Input register A for pins 0-31. Reads the current state of pins regardless of direction setting.

**Access**: Read-only for pin states (overlaid as IJMP0, R/W, during a debug ISR)

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | IN | Current state of each pin: 1 = high, 0 = low |

**Usage**: INA returns the actual electrical state of pins 0-31, regardless of whether they are configured as inputs or outputs. This allows output pins to be read back to verify their state. Reading INA captures the pin states at the moment the instruction executes, providing a consistent snapshot of all 32 pins. During a debug ISR, $1FE is overlaid as IJMP0 — the debug-interrupt jump address — and becomes read/write (it is initialized to $1F8, the debug-ISR-entry routine, on COGINIT).

**Example**:
```pasm2
                mov     state, INA              ' Read all pins 0-31
                test    INA, #1             wz  ' Test if pin 0 is high
        if_nz   jmp     #pin_high

                and     inputs, INA             ' Mask input pins

                ' Wait for pin high
.wait           test    INA, pin_mask       wz
        if_z    jmp     #.wait
```

**Related**: [INB](#inb), [DIRA](#dira), [OUTA](#outa)



### INB {#inb}

Address $1FF. Input register B for pins 32-63. Reads the current state of pins regardless of direction setting.

**Access**: Read-only for pin states (overlaid as IRET0, R/W, during a debug ISR)

**Bit Field**:

| Bits | Name | Description |
|------|------|-------------|
| 31:0 | IN | Current state of each pin: 1 = high, 0 = low |

**Usage**: INB returns the actual electrical state of pins 32-63, regardless of whether they are configured as inputs or outputs. The bit positions map to pins 32-63, where bit 0 represents pin 32 and bit 31 represents pin 63. During a debug ISR, $1FF is overlaid as IRET0 (the debug-interrupt return address) and becomes read/write.

**Example**:
```pasm2
                mov     state, INB              ' Read all pins 32-63
                test    INB, ##$8000_0000   wz  ' Test if pin 63 is high
        if_z    jmp     #pin_low

                ' Copy input pattern to output
                mov     OUTB, INB
```

**Related**: [INA](#ina), [DIRB](#dirb), [OUTB](#outb)



## Non-Memory-Mapped Registers

Several critical registers exist outside the cog RAM address space and are accessed only through specific instructions.

### Program Counter (PC)

The program counter is a 20-bit register that holds the Hub RAM address of the currently executing instruction.

**Access**: Read via GETPC, modified implicitly by jumps and calls

**Range**: $00000-$FFFFF (full Hub address space)

**Usage**: The PC automatically increments by 4 after each instruction execution, pointing to the next long-aligned instruction in Hub RAM. Jump and call instructions modify the PC to change program flow. The PC wraps at the 20-bit boundary when incremented beyond $FFFFF.

**Example**:
```pasm2
        getpc   current_addr            ' Read current PC value

        ' PC modified by control flow
        jmp     #target                 ' Sets PC to target address
        call    #subroutine             ' Saves PC+4, jumps to subroutine
```

**Related**: GETPC, JMP, CALL, CALLD



### Q Register

The Q register is a 32-bit auxiliary register used for CORDIC operations, division results, and block transfer setup.

**Access**: Read via GETQX/GETQY, write via SETQ/SETQ2

**Usage**: The Q register serves multiple purposes:

1. **CORDIC results**: After CORDIC operations (QROTATE, QVECTOR, etc.), results are read from Q using GETQX and GETQY.
2. **Division quotient**: Division instructions place the quotient in Q.
3. **Block operations**: SETQ and SETQ2 configure the Q register to enable multi-long transfers with RDxxxx/WRxxxx instructions.

The Q register contents are volatile—CORDIC and division operations overwrite previous values. Read results immediately after the operation completes.

**Example**:
```pasm2
        setq    y                       ' Y coordinate via Q
        qrotate x, angle                ' Rotate (X, Y) by angle
        getqx   result_x                ' Get X result from Q
        getqy   result_y                ' Get Y result from Q

        ' Block transfer setup
        setq    #15                     ' Setup for 16-long transfer
        rdlong  buffer, ptra++          ' Read 16 longs using Q count

        ' Division
        qdiv    dividend, divisor       ' Quotient goes to Q
        getqx   quotient                ' Read quotient from Q
        getqy   remainder               ' Read remainder from Q
```

**Related**: GETQX, GETQY, SETQ, SETQ2, QROTATE, QVECTOR, QDIV



### System Counter (CT)

The system counter is a free-running 64-bit counter (Rev B/C silicon) that increments on every system clock cycle. It is global across all cogs—all cogs reading CT simultaneously receive the same value. GETCT returns the lower 32 bits by default, or the upper 32 bits with WC.

**Access**: Read via GETCT, used by ADDCT1/ADDCT2/ADDCT3 and WAITCT1/WAITCT2/WAITCT3

**Resolution**: System clock cycles (typically 200 MHz = 5ns resolution)

**Usage**: CT provides precise timing for delays, timeouts, and event synchronization. The lower 32 bits wrap approximately every 21.5 seconds at 200 MHz. For precise waits, read the current CT value, add the desired delay to compute a target time, and wait for CT to reach that target. This approach compensates for instruction execution time between reading CT and initiating the wait.

**Example**:
```pasm2
                getct   target                  ' Get current time
                addct1  target, ##delay_cycles  ' target = now + delay
                waitct1                         ' Wait for CT to reach it

                ' Timeout pattern
                getct   timeout
                add     timeout, ##max_cycles
.loop           ' ... do work ...
                getct   now
                cmp     now, timeout        wc  ' Check if timeout exceeded
        if_nc   jmp     #timed_out
                jmp     #.loop
```

**Related**: GETCT, ADDCT1, ADDCT2, ADDCT3, WAITCT1, WAITCT2, WAITCT3



### Hardware Random Number Generator (RANDOM)

The hardware random number generator produces true random numbers based on thermal noise, providing a new random value on each read.

**Access**: Read via GETRND

**Features**: True random number generation (not pseudo-random), continuously generates new values

**Usage**: Each execution of GETRND returns a new 32-bit random value. The generator runs continuously in hardware, so consecutive reads produce different values. The randomness quality is suitable for cryptographic applications.

**Example**:
```pasm2
        getrnd  random_value            ' Get 32-bit random number

        ' Generate random in range 0-99
        getrnd  temp
        qmul    temp, #100              ' Multiply by 100
        getqy   random_0_99             ' High 32 bits = value*100/2^32

        ' Random bit
        getrnd  temp
        shr     temp, #31               ' Get bit 31 (random 0 or 1)
```

**Related**: GETRND, QMUL (for scaling random values)



### C and Z Flags

The carry (C) and zero (Z) flags are 1-bit condition flags that store the results of tests and arithmetic operations.

**Access**: Set by instructions with WC, WZ, or WCZ effects; tested by conditional instruction execution

**Persistence**: Flags maintain their values until explicitly modified by another instruction with WC/WZ/WCZ

**Usage**: The C and Z flags enable conditional execution and branching. Most ALU instructions can update these flags based on their results. Conditional prefixes (IF_Z, IF_NZ, IF_C, IF_NC, etc.) determine whether an instruction executes based on flag states.

**Flag Setting**:

- **WZ**: Sets Z flag based on result (Z=1 if result is zero)
- **WC**: Sets C flag based on operation (carry out, bit shifted out, etc.)
- **WCZ**: Sets both flags

**Example**:
```pasm2
                cmp     value, #100         wz  ' Compare, set Z if equal
        if_z    jmp     #equal

                test    flags, ##$8000_0000 wc  ' Test bit 31, put in C
        if_c    jmp     #bit_set

                add     sum, addend         wc  ' Add, set C if overflow
        if_c    jmp     #overflow

                shr     data, #1            wc  ' Shift right, C = bit out
```

**Related**: All conditional execution (IF_xx), CMP, TEST, and ALU instructions with WC/WZ/WCZ



## Common Usage Patterns

### Pin Control

Toggle a pin:
```pasm2
        xor     OUTA, pin_mask          ' Toggle pin atomically
```

Wait for pin high:
```pasm2
.wait           test    INA, pin_mask       wz
        if_z    jmp     #.wait
```

Copy inputs to outputs:
```pasm2
        mov     OUTA, INA               ' Mirror inputs to outputs
```

Set multiple pins atomically:
```pasm2
        mov     OUTA, new_pattern       ' All 32 pins change simultaneously
```



### Hub RAM Access

Block read with pointer:
```pasm2
        mov     ptra, ##hub_buffer
        setq    #count-1                ' Transfer 'count' longs
        rdlong  cog_buffer, ptra++      ' Read block, auto-increment PTRA
```

Dual buffer operation:
```pasm2
        mov     ptra, ##source_buffer
        mov     ptrb, ##dest_buffer
        setq    #15                     ' Transfer 16 longs
        rdlong  temp, ptra++            ' Read from PTRA
        setq    #15
        wrlong  temp, ptrb++            ' Write to PTRB
```



### Interrupt Setup

Configure interrupt handler:
```pasm2
        mov     IJMP1, ##handler_addr   ' Set handler address
        setint1 #event_ct1              ' Enable INT1 for CT1 event

handler_addr
        ' ... handle interrupt ...
        reti1                           ' Return to interrupted code
```



### Timing Operations

Precise delay:
```pasm2
        getct   target                  ' Get current time
        addct1  target, ##delay_cycles  ' Add delay
        waitct1                         ' Wait until target time
```

Timeout detection:
```pasm2
                getct   deadline
                add     deadline, ##max_time
.loop           ' ... do work ...
                getct   now
                cmp     now, deadline       wc
        if_nc   jmp     #timeout
                ' ... continue if not timed out ...
                jmp     #.loop
```



## Important Behaviors

**Multi-Cog Pin Control**: When multiple cogs drive the same pin as an output, the pin outputs are OR'd together. If any cog outputs high, the pin goes high. This enables cooperative control but requires coordination to avoid conflicts.

**Smart Pin Override**: When a pin is configured for smart pin operation, the smart pin mode overrides the basic DIRA/OUTA/INA functions for that pin. The pin is controlled through smart pin registers and commands rather than the basic I/O registers.

**Immediate Effect**: Changes to DIR and OUT registers take effect immediately—the hardware updates pin states on the same clock cycle as the register write.

**Input Reading**: INA and INB always return actual pin states, regardless of direction settings. This allows outputs to be read back for verification.

**Pointer Auto-Modification**: When using PTRA++ or PTRB++ addressing modes, the pointer update occurs after the memory access completes. The modification affects subsequent operations using that pointer.

**PC Wrap Behavior**: The program counter wraps at the 20-bit boundary ($FFFFF → $00000). Code executing near the top of Hub RAM must account for this wrap behavior.

**Per-Cog Independence**: Each cog has its own independent copy of all special registers. Changes in one cog do not affect other cogs' registers, enabling parallel independent operation.
