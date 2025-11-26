# Chapter 9: Streaming Data

*Moving data at maximum velocity*

## The Hook: DMA-Like Streaming

```pasm2
        setq    ##1000-1         ' Transfer 1000 longs
        rdlong  buffer, source   ' Happens at maximum speed!
        ' 4KB moved in microseconds!
```

## The Streamer Concept

The streamer is P2's DMA engine:
- Moves data between hub and pins
- Generates video
- Captures high-speed data
- All without CPU intervention

## FIFO Operations

```pasm2
        rdfast  #0, hubaddr     ' Start FIFO read
loop    rflong  data           ' Read from FIFO (no waiting!)
        ' Process data
        djnz    count, #loop
```

---

*Continue to [Chapter 10: Hub Execution](10-hub-execution.md) →*