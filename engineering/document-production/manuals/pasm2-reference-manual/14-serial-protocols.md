# Chapter 14: Serial Protocols

*Talking to the world*

## The Hook: Hardware UART, SPI, and I2C

```pasm2
' UART in hardware
        wrpin   ##P_ASYNC_TX, #TX_PIN
        wxpin   ##BAUD_115200, #TX_PIN
        dirh    #TX_PIN
        wypin   char, #TX_PIN    ' Send character!
```

## UART Implementation

Smart Pins handle the bit timing, you handle the bytes.

## SPI Master and Slave

```pasm2
' SPI using Smart Pins
        wrpin   ##P_SYNC_TX, #MOSI_PIN
        wrpin   ##P_SYNC_RX, #MISO_PIN
        ' Clock and data handled in hardware!
```

## I2C Communication

Bit-banged or Smart Pin assisted - your choice!

---

*Continue to [Chapter 15: Signal Processing](15-signal-processing.md) →*