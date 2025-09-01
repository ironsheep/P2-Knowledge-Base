
*Learning the native tongue*

## The Hook: One Instruction, Many Powers

Look at this single PASM2 instruction:

```pasm2
        add     value, #1 wc
```

This one line:
- Adds 1 to 'value'
- Optionally sets the carry flag
- Executes in exactly 2 clock cycles
- Can be conditional
- Can even modify itself!

In most processors, that would take multiple instructions. In PASM2, it's just one. Let's learn to speak this powerful language.

## Instruction Anatomy 101

Every PASM2 instruction follows the same basic pattern:

```
[condition] instruction dest, [#]source [flags]
     ↑           ↑        ↑       ↑        ↑
 optional    what to do  target  data   optional
```

Let's dissect a real instruction:

```pasm2
if_z    add     total, #10 wc
 ↑       ↑        ↑     ↑   ↑
only if  add    to this immediate set carry
Z flag           value   value    flag
is set
```

## The Basic Vocabulary

### Moving Data Around

The MOV family - your bread and butter:

```pasm2
' Basic move
        mov     dest, source    ' dest = source
        mov     x, #42         ' x = 42 (immediate)
        mov     x, ##70000     ' x = 70000 (32-bit immediate)

' But wait, there's more!
        mvn     dest, source    ' dest = NOT source (inverted)
        abs     dest, source    ' dest = |source|
        neg     dest, source    ' dest = -source

' And the mind-blowing ones
        altd    dest, source    ' Modify NEXT instruction's dest field!
        alts    dest, source    ' Modify NEXT instruction's source field!
```

Well, that escalated quickly! Don't worry about ALTD/ALTS yet - just know they exist and they're amazing.

### Math Without Tears

P2 has hardware multiply and divide. Let that sink in. Hardware. Multiply. And. Divide.

```pasm2
' Addition and subtraction
        add     x, y           ' x = x + y
        sub     x, y           ' x = x - y
        adds    x, y           ' Signed add
        subs    x, y           ' Signed subtract

' The revolution: hardware multiply!
        mul     x, y           ' x = x * y (low 32 bits)
        muls    x, y           ' Signed multiply
        
' And hardware divide!
        qdiv    x, y           ' Start division x/y
        getqx   result         ' Get quotient
        getqy   remainder      ' Get remainder
```

Here's a complete multiply example:

```pasm2
' Multiply two numbers and get 64-bit result
        mov     x, #123
        mov     y, #456
        mul     x, y           ' Low 32 bits in x
        getmulh high           ' High 32 bits in high
        ' Result: 123 * 456 = 56088
        ' (all in 2 clock cycles!)
```

Uff! In the old days, we'd write loops for this. Now it's instant.

### Logic Operations

Your Boolean friends:

```pasm2
        and     x, mask        ' x = x AND mask
        or      x, bits        ' x = x OR bits  
        xor     x, toggle      ' x = x XOR toggle
        not     x              ' x = NOT x (same as XOR with $FFFFFFFF)
        
' Bit manipulation
        bitl    x, #5          ' Clear bit 5 of x
        bith    x, #5          ' Set bit 5 of x
        bitnot  x, #5          ' Toggle bit 5 of x
        testb   x, #5 wc       ' Test bit 5, result in C flag
```

### Shifting and Rotating

Moving bits around:

```pasm2
        shl     x, #3          ' Shift left 3 bits
        shr     x, #3          ' Shift right 3 bits
        sar     x, #3          ' Arithmetic shift right (sign-extend)
        rol     x, #3          ' Rotate left 3 bits
        ror     x, #3          ' Rotate right 3 bits
        
' Variable shifts (amount in register)
        shl     x, y           ' Shift x left by y bits
        
' Fancy ones
        rev     x              ' Reverse bit order (!!)
        mergeb  x              ' Merge bytes (AABBCCDD -> ABCDABCD)
```

## Flow Control: Jump!

### Unconditional Jumps

```pasm2
        jmp     #target        ' Jump to target
        jmp     target         ' Jump to address in target register
        
' Relative jumps
        jmp     #$-4          ' Jump back 4 instructions
        jmp     #$+8          ' Jump forward 8 instructions
```

### Conditional Execution (The Magic)

Here's where PASM2 gets beautiful. ANY instruction can be conditional:

```pasm2
if_z    add     x, #1          ' Only add if Z flag set
if_nz   add     x, #1          ' Only add if Z flag clear
if_c    add     x, #1          ' Only add if C flag set
if_nc   add     x, #1          ' Only add if C flag clear
```

The conditions:

```
if_z     - If Z flag set (result was zero)
if_nz    - If Z flag clear (result not zero)
if_c     - If C flag set (carry/borrow occurred)
if_nc    - If C flag clear
if_c_and_z   - If both C and Z set
if_c_or_z    - If either C or Z set
if_c_eq_z    - If C equals Z
if_c_ne_z    - If C not equal to Z
```

And the advanced ones:

```
if_a     - If above (unsigned greater)
if_b     - If below (unsigned less)
if_ae    - If above or equal
if_be    - If below or equal
```

### The Call/Return Dance

```pasm2
        call    #subroutine    ' Call subroutine
        ret                    ' Return from subroutine
        
' But here's the P2 twist - CALL uses internal stack
subroutine
        ' Do something useful
        ret                    ' Returns to instruction after CALL
        
' You get 8 levels of hardware stack!
```

## The Flags: C and Z (and Q!)

Flags are your friends. They remember things:

```pasm2
' Z flag - was the result zero?
        sub     x, y wz        ' Set Z if x-y equals zero
if_z    jmp     #equal         ' Jump if they were equal

' C flag - did we carry/borrow?
        add     x, y wc        ' Set C if addition overflowed
if_c    jmp     #overflow      ' Handle overflow

' Both at once!
        cmp     x, y wcz       ' Compare and set both flags
if_a    jmp     #x_greater     ' Jump if x > y (unsigned)
```

The Q flag is special - it's used by CORDIC operations (Chapter 7).

## Special Instructions That Will Blow Your Mind

### SKIP - The Instruction Skipper

```pasm2
        skip    ##%11010000    ' Skip pattern (1=skip, 0=execute)
        add     x, #1         ' Skipped!
        add     y, #1         ' Skipped!  
        add     z, #1         ' Executed
        sub     a, #1         ' Skipped!
        sub     b, #1         ' Executed
        ' ... pattern continues
```

This is like having conditional execution on steroids!

### REP - Hardware Loops

```pasm2
        rep     #4, #5         ' Repeat next 4 instructions 5 times
        add     x, #1
        sub     y, #1
        rol     z, #1
        ror     w, #1
        ' These 4 instructions execute 5 times total
        ' No loop overhead!
```

### ALTD/ALTS - Instruction Modification

```pasm2
' Modify the next instruction's destination
        mov     index, #10
        altd    index, #array  ' Next instruction's dest = array+10
        mov     0-0, value     ' Actually moves to array[10]!
```

This replaces self-modifying code from P1. Much cleaner!

## Real-World Example: Fast Memory Copy

Let's combine what we've learned:

```pasm2
' Fast block copy using REP
fast_copy
        mov     ptra, ##source_addr    ' Source pointer
        mov     ptrb, ##dest_addr      ' Destination pointer
        
        rep     #2, ##256              ' Repeat 256 times
        rdlong  temp, ptra++           ' Read and increment
        wrlong  temp, ptrb++           ' Write and increment
        ' 512 bytes copied with no loop overhead!
        
temp    long    0
```

## The Medicine Cabinet

Feeling overwhelmed? Here's your simplified prescription:

### Minimum Instructions to Know

```pasm2
' Moving data
mov     dest, source   ' Copy data

' Math
add     dest, source   ' Addition
sub     dest, source   ' Subtraction

' Logic
and     dest, source   ' AND operation
or      dest, source   ' OR operation

' Flow
jmp     #label        ' Jump
call    #label        ' Call subroutine
ret                   ' Return

' Flags
cmp     x, y wcz      ' Compare and set flags
if_z    jmp #label    ' Conditional jump
```

Master these 10 instructions and you can write real programs!

## Common Gotchas

1. **Immediate values**: 
   - `#value` for 9-bit immediates (0-511)
   - `##value` for 32-bit immediates
   - Forgetting # uses the register at that address!

2. **Flag confusion**:
   - `wz` sets Z flag, `wc` sets C flag, `wcz` sets both
   - No flag update means flags unchanged

3. **PTRA/PTRB are special**:
   ```pasm2
   rdlong  x, ptra++      ' Read and auto-increment
   rdlong  x, ++ptra      ' Pre-increment then read
   rdlong  x, ptra--      ' Read and auto-decrement
   rdlong  x, ptra[5]     ' Read from ptra + 5*4
   ```

4. **Address confusion**:
   - COG addresses are in longs (0-511)
   - Hub addresses are in bytes (0-524287)

## Your Turn: Experiments

### Experiment 1: Conditional Counter
Count up if button pressed, down if not:

```pasm2
        org     0
        
loop    testp   #BUTTON_PIN wc ' Test button
if_c    add     counter, #1    ' Increment if pressed
if_nc   sub     counter, #1    ' Decrement if not
        
        wrlong  counter, ##HUB_ADDR ' Display count
        waitx   ##1_000_000
        jmp     #loop
        
counter long    0
```

### Experiment 2: Pattern Matcher
Find a pattern in data:

```pasm2
        org     0
        
        mov     pattern, ##$DEADBEEF
        mov     ptra, ##data_start
        
search  rdlong  value, ptra++
        cmp     value, pattern wz
if_z    jmp     #found
        cmp     ptra, ##data_end wcz
if_b    jmp     #search
        jmp     #not_found
        
found   ' Pattern found!
        drvh    #SUCCESS_LED
        jmp     #$
        
not_found
        drvh    #FAIL_LED
        jmp     #$
```

### Experiment 3: Speed Test
Compare multiply methods:

```pasm2
' Method 1: Hardware multiply
        getct   start_time
        mul     x, y
        getct   end_time
        sub     end_time, start_time
        ' Result: 2 clocks!
        
' Method 2: Shift and add (old school)
        getct   start_time
        ' ... shift/add loop here
        getct   end_time
        ' Result: Many more clocks!
```

## Sidetrack: Why PASM2 Is Different

Most assembly languages are thin wrappers over hardware. PASM2 is different - it's designed for humans:

1. **Symmetry**: Every instruction can use every addressing mode
2. **Orthogonality**: Features combine predictably
3. **Conditional everything**: Not just jumps, ANY instruction
4. **No special cases**: General-purpose registers, no accumulator

This isn't accident - it's philosophy. The P2 was designed to make assembly programming pleasant.

## What We've Learned

- ✅ Instruction anatomy and structure
- ✅ Basic data movement and math
- ✅ Hardware multiply and divide (!)
- ✅ Conditional execution on any instruction
- ✅ Special instructions (SKIP, REP, ALT*)
- ✅ Flag operations and testing
- ✅ Why PASM2 is human-friendly

## Coming Up Next

Chapter 4, "The Hub Connection", explores:
- Reading and writing hub memory
- The FIFO and fast block transfers
- Hub execution mode
- Sharing data between COGs

You now speak basic PASM2. Time to learn how COGs communicate!

---

**Have Fun!** Remember, PASM2 isn't like other assembly languages - it's actually enjoyable!

---

*Continue to [Chapter 4: The Hub Connection](04-hub-connection.md) →*

---

# Chapter 4: The Hub Connection

*How COGs share and care*

## The Hook: Instant Communication

```pasm2
' COG 1: Leave a message
        wrlong  ##$DEADBEEF, ##$1000
        
' COG 2: Get the message
        rdlong  message, ##$1000
        ' message now contains $DEADBEEF!
```

That's it - COGs talking through hub memory. But there's so much more...

## Reading from Hub

The basics are simple:

```pasm2
        rdbyte  value, hubaddr    ' Read 1 byte
        rdword  value, hubaddr    ' Read 2 bytes (word)
        rdlong  value, hubaddr    ' Read 4 bytes (long)
        
' With PTRA/PTRB magic
        rdlong  value, ptra++     ' Read and increment pointer
        rdlong  value, ++ptra     ' Increment then read
        rdlong  value, ptra[5]    ' Read from ptra + 5*4
```

## Writing to Hub

Just as easy:

```pasm2
        wrbyte  value, hubaddr    ' Write 1 byte
        wrword  value, hubaddr    ' Write 2 bytes
        wrlong  value, hubaddr    ' Write 4 bytes
        
' The mighty block transfer
        setq    #16-1             ' Transfer 16 longs
        rdlong  buffer, hubaddr   ' Reads 16 longs in one go!
```

## The FIFO Pipeline

Here's where P2 gets serious about speed:

```pasm2
' Start the FIFO
        rdfast  #0, ##data_start  ' Start fast read
        
' Now read at maximum speed
loop    rflong  value            ' Read from FIFO
        ' Process value
        djnz    count, #loop     ' Decrement and jump if not zero
        
' No hub timing worries - FIFO handles it all!
```

## Real-World Example: Video Buffer

```pasm2
' Fast screen clear using block transfer
clear_screen
        mov     color, ##$00_00_00_00  ' Black
        setq2   ##640*480-1             ' Number of longs
        wrlong  color, ##screen_buffer  ' Fills entire screen!
        ' 1.2MB cleared in microseconds!
```

## The Medicine Cabinet

**Simple hub access pattern**:
```pasm2
' Just use PTRA for everything
        mov     ptra, ##hub_address
        rdlong  value, ptra++
        ' That's all you really need!
```

---

*Continue to [Chapter 5: Mathematics Unleashed](05-mathematics-unleashed.md) →*

---

