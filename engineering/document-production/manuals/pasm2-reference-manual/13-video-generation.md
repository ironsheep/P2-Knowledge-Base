# Chapter 13: Video Generation

*From pixels to pictures*

## The Hook: VGA in 10 Instructions

```pasm2
        setcmod #$100           ' Set colorspace
        setcy   ##640*480      ' Set resolution
        setci   ##HSYNC_TIMING ' Set timing
        setcq   ##VSYNC_TIMING
        setcfrq ##PIX_FREQ     ' Set pixel frequency
        setcy   ##LINE_BUFFER  ' Set buffer address
        xinit   ##STREAMER_CMD, #0  ' Start video!
```

## Video Fundamentals

P2 generates video through:
- The streamer (DMA engine)
- Smart pins (sync signals)
- COG timing (line control)

## VGA Generation

Complete VGA driver example with proper timing and double buffering.

## HDMI Basics

P2 can generate HDMI signals using Smart Pins in special modes.

---

*Continue to [Chapter 14: Serial Protocols](14-serial-protocols.md) →*