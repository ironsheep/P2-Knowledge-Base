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