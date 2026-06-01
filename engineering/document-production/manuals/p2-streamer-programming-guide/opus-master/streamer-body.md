# Part I: Streamer Fundamentals

# Chapter 1: Understanding the Streamer

Before the mode tables and bit fields, it helps to know what the streamer *is*, why the P2 has one, and how to think about it when you sit down to build something. This chapter builds that picture. The rest of the guide is the detailed reference; this chapter is the map.

## 1.1 What the streamer is

Every COG on the P2 has its own **streamer**: a small, tireless engine that moves data between hub memory and the outside world — the pins, the DAC channels, the ADC inputs — entirely on its own, at a rate you choose. Once you start it, it runs without the CPU's help. Your code can compute, make decisions, or sleep while the streamer keeps feeding pixels to a display or pulling samples off a wire.

The detail that makes the streamer special is that it carries **its own clock**. A piece of hardware called the NCO (Numerically-Controlled Oscillator) acts as a metronome: you set the beat, and the streamer moves one piece of data on every beat. That beat can run tens of millions of times per second and — crucially — it is *exact*. This is what lets a single COG produce a clean video picture or a steady audio stream: not raw speed, but precise, unwavering timing that the CPU never has to babysit.

> **If you've used DMA before:** the streamer is a close cousin of a DMA channel, with two important additions. First, it has that built-in metronome, so it does *paced* transfers at an exact sample rate rather than "as fast as the bus allows." Second, it reshapes data as it moves — packing bits, expanding through a palette, converting color formats — instead of copying bytes verbatim. If you have never met DMA, don't worry: everything below stands on its own.

## 1.2 Why the streamer exists

Generating precise, fast, repetitive signals in software is brutally expensive. Imagine driving a video display by hand: your code would have to write a new color to the pins every forty nanoseconds, forever, without ever slipping. A single loop like that would consume an entire COG and still stutter the moment anything interrupted it. The streamer exists so that this relentless, timed, repetitive work happens in hardware, leaving the COG free for the *interesting* part — drawing the next frame, decoding the next packet, running the game.

So why is it so complicated? Because one engine has to serve very different jobs: pushing video to a screen, playing audio through a DAC, capturing pins like a logic analyzer, sampling an analog input like an oscilloscope, generating tones, even detecting a specific frequency in an incoming signal. Rather than give each COG six narrow peripherals, the P2 gives it **one highly configurable engine**. The configurability is the complexity — and it is also the payoff. Learn the handful of knobs once, and the same engine does all of those jobs.

## 1.3 A mental model: a paced, configurable pipe

Picture a pipe running from hub memory to the pins, with an adjustable shaper in the middle and a metronome setting the pace. Every streamer command you issue is just a way of answering four questions about that pipe:

1. **Where does the data come from?** An immediate value you supply, or a stream pulled from hub memory through the FIFO.
2. **Where does it go?** Out to the pins, out to the DAC channels — or, when capturing, back into hub memory.
3. **How is it shaped along the way?** Sliced into 1-, 2-, 4-, 8-, 16-, or 32-bit pieces; expanded through a lookup table (a palette); or converted into a video color format.
4. **How fast?** The NCO's beat.

That is the whole idea. The long list of modes in Part II is nothing more than the *useful combinations* of those four answers. Once you read a mode as "hub data, to the pins, one byte at a time, at the pixel rate," the names stop looking like alphabet soup.

## 1.4 Two directions: output and input

The streamer works in two directions, and they are different enough that it helps to think about them separately.

**Output modes drive the world** — pixels to a screen, samples to a speaker, bits down a serial line. Here the interesting questions are *where the data comes from* (a buffer in memory, or a small repeating table) and *how it is shaped* (raw bytes, palette lookup, RGB color) before it reaches the pins.

**Input modes capture the world** — pin states recorded into memory (a logic analyzer); ADC readings recorded into memory (an oscilloscope). Here the interesting question is *how the captured data is packed* as it is written back to hub.

Knowing which direction you are working in immediately cuts the mode list roughly in half — you only ever care about one side at a time.

## 1.5 Why there are so many modes — and why they differ

It is tempting to see the mode tables as a random pile of similar-looking options. They are not. They vary along just a few axes, and each combination earns its place by doing a *distinct* job. Two quick contrasts make the point:

- **Playing a recording vs. synthesizing a tone.** Both end at the DAC. But playing a recorded sound streams a long buffer out of hub memory, while synthesizing a tone loops a *tiny* table — one cycle of a sine wave — over and over, with the NCO setting the pitch. Same destination, completely different source strategy. That difference is exactly what separates the two modes.
- **One channel vs. multichannel audio.** These are not different engines at all — they are one routing knob (the DAC-routing field) deciding how many of the four DAC channels get fed. "Stereo" is a setting, not a separate mode.

So when two mode names sound alike, the question to ask is: *which of the four pipe-questions do they answer differently?* That is always where the real distinction lives.

## 1.6 The special capabilities, in plain words

A few streamer features have intimidating names. Here is what they actually mean.

**Video (RGB and colorspace conversion).** The streamer can pull pixels from a framebuffer in memory and push them out as an analog VGA signal or a digital HDMI signal, translating color formats as it goes. You provide the picture; the streamer handles the relentless pixel timing. *(Chapters 7 and 15.)*

**DDS — Direct Digital Synthesis.** A grand name for a simple trick: generate a repeating waveform — a sine, a tone, any shape you like — by stepping through a small table at a precise rate. The NCO sets the frequency, so the same table produces any pitch. This is how you build a function generator, an audio tone, or a modulated carrier. *(Chapters 10 and 17.)*

**Goertzel frequency analysis.** This one is never obvious from its name, so plainly: it is a way to ask, in hardware, *"how much of one specific frequency is present in this incoming signal?"* You tell it the frequency you care about, and it reports how strongly that tone is there. The textbook use is decoding telephone touch-tones — the beeps of a phone keypad, known as DTMF — but the same trick detects whistles and alarm tones, measures distance with ultrasound (send a ping, listen for its echo), and builds simple receivers. It is cheap precisely because it checks only the *one* frequency you ask about, instead of computing a whole spectrum. *(Chapters 10 and 17.)*

## 1.7 If you're building...

You usually arrive at the streamer with an application already in mind. Find it below; the chapters on the right are the ones worth reading closely first. The rest of the reference is there for when you need the exact bits.

| If you're thinking about... | The streamer gives you... | Start at |
|------------------------------|----------------------------|----------|
| Video (VGA, HDMI, composite) | color pixels from a framebuffer | Ch. 7, Ch. 15 |
| Audio / sound output | DAC samples from a buffer | Ch. 5–6, Ch. 11 |
| Generating tones or waveforms | DDS from a small table | Ch. 10, Ch. 17 |
| A logic analyzer (capturing pins) | pin states written to memory | Ch. 8 |
| Sampling an analog signal | ADC readings written to memory | Ch. 9 |
| Detecting a specific tone or frequency | Goertzel analysis | Ch. 10, Ch. 17 |
| High-speed serial (fast SPI) | timed bit output, clocked by a smart pin | Ch. 16 |

## 1.8 What each COG actually has

For all that capability, the hardware budget is modest. Each COG contains exactly one streamer, with:

- one 32-bit NCO (the metronome / phase accumulator);
- one command buffer (it holds one queued command, so commands can hand off without a gap);
- four 8-bit DAC channels (X0, X1, X2, X3);
- one Goertzel analyzer;
- access to the COG's LUT RAM (used as a palette or a waveform table).

And it leans on a few neighboring P2 subsystems:

| Subsystem | What it provides |
|-----------|------------------|
| Hub FIFO | the data source / sink, via RDFAST / WRFAST |
| LUT RAM | palette lookups, sine/cosine tables |
| DAC channels | analog output for video and audio |
| Colorspace converter | HDMI encoding and composite video |
| Smart pins | clock generation and timing synchronization |

With that picture in place, Chapter 2 opens up the engine itself — the data paths inside the streamer and how the pieces connect.

# Chapter 2: Architecture

Chapter 1 described the streamer as a paced pipe from memory to the pins. This chapter opens that pipe up — the pieces inside, how data flows through them, and how the NCO drives the whole thing. You do not need this depth to *use* the streamer, but it makes the mode choices in Part II feel inevitable rather than arbitrary.

## 2.1 Block Diagram

```{=latex}
\DiagStreamerArch
```

## 2.2 Data Flow Paths

The streamer supports multiple data flow configurations:

```{=latex}
\DiagDataFlow
```

**Output Paths (Hub → Pins/DACs):**

1. **Immediate → LUT → Pins/DACs**: S operand indexes LUT; LUT data drives output
2. **Immediate → Pins/DACs**: S operand drives output directly
3. **RDFAST → LUT → Pins/DACs**: Hub data indexes LUT; LUT data drives output
4. **RDFAST → Pins/DACs**: Hub data drives output directly
5. **RDFAST → RGB → Pins/DACs**: Hub data passes through colorspace converter

**Input Paths (Pins → Hub):**

1. **Pins → DACs/WRFAST**: Pin states written to Hub
2. **ADC → DACs/WRFAST**: ADC readings written to Hub

**Special Path:**

1. **DDS/Goertzel**: LUT-based synthesis with simultaneous frequency analysis

## 2.3 Component Functions

**NCO (Numerically-Controlled Oscillator):**
Times all streamer operations. On each clock, adds frequency value to phase accumulator. Rollover (MSB set) triggers data advancement.

**Command Buffer:**
Holds one pending command. Enables seamless transitions between streamer operations without gaps.

**Data Shifter:**
Handles data widths from 1-bit to 32-bit. Extracts and formats data according to mode.

**LUT Interface:**
Reads COG LUT RAM for palette expansion or waveform generation. 512 entries × 32 bits.

**DAC Channels:**
Four 8-bit channels (X0-X3) map to pins based on pin number LSBs. Configurable routing allows stereo, differential, or independent operation.

**Goertzel Analyzer:**
Hardware frequency detection using Goertzel algorithm. Accumulates sine and cosine products for magnitude/phase extraction.

# Chapter 3: NCO and Timing

The NCO is the streamer's metronome, and it is the single most important thing to understand about the streamer's timing. Everything the streamer does happens on the NCO's beat, so setting its rate correctly is the difference between a steady picture and a rolling one. This chapter shows how the NCO produces that beat and how to compute the value you need for a given rate.

## 3.1 NCO Operation

The NCO operates on every system clock:

```formula
phase = (phase & $7FFF_FFFF) + frequency
```

1. The MSB is masked (cleared) before addition
2. The frequency value adds to the phase accumulator
3. If the new MSB is set, a "rollover" occurs
4. On rollover, the streamer advances to the next data element

🔧 **Hardware:** The phase accumulator is a 32-bit register. Its most-significant bit is masked off before each addition and used as the rollover flag, so 31 bits accumulate the phase. Frequency resolution is therefore `clock_frequency / 2³¹`.

```{=latex}
\DiagNcoRollover
```

## 3.2 Frequency Calculation

**Formula:**

```formula
frequency = $8000_0000 × (desired_rate / clock_frequency)
```

**Common Values:**

| Rate Ratio | Frequency Value | At 250 MHz | At 300 MHz |
|------------|-----------------|------------|------------|
| 1:1 | `$8000_0000` | 250 MHz | 300 MHz |
| 1:2 | `$4000_0000` | 125 MHz | 150 MHz |
| 1:3 | `$2AAA_AAAB` | 83.3 MHz | 100 MHz |
| 1:4 | `$2000_0000` | 62.5 MHz | 75 MHz |
| 1:5 | `$1999_999A` | 50 MHz | 60 MHz |
| 1:10 | `$0CCC_CCCD` | 25 MHz | 30 MHz |

💡 **Tip:** For fractional ratios (1/3, 1/5, 1/10), add 1 to the calculated value to ensure proper initial rollover timing.

## 3.3 Setting NCO Frequency

**Method 1: SETXFRQ instruction**

```pasm2
        setxfrq ##$0CCC_CCCD        ' 25 MHz at 250 MHz clock
```

**Method 2: SETQ before streamer command**

```pasm2
        setq    ##$0CCC_CCCD        ' Frequency in Q
        xinit   mode, data          ' Uses Q as frequency
```

The **SETQ** method allows changing frequency atomically with a new command.

## 3.4 Pixel Rate Examples

| Application | Pixel Rate | At 250 MHz | At 300 MHz | At 320 MHz |
|-------------|------------|------------|------------|------------|
| VGA 640×480 | 25.175 MHz | `$0CE3_BCD3` | `$0ABD_C805` | `$0A11_EB85` |
| VGA 800×600 | 40 MHz | `$147A_E148` | `$1111_1111` | `$1000_0000` |
| VGA 1024×768 | 65 MHz | `$2147_AE14` | `$1BBB_BBBC` | `$1A00_0000` |

Each value is `round($8000_0000 × pixel_rate / clock_frequency)` — the closest achievable NCO word for that rate at that clock.

⚠️ **Pitfall:** Exact VGA pixel rates rarely divide evenly into P2 clock frequencies. The values above are the nearest achievable rate; monitors tolerate small variations.

# Chapter 4: Command Structure

A streamer command is a single value — the D operand — that packs together every choice from Chapter 1's four questions: what mode, where the data goes, which pins, and how long to run. This chapter lays that packed word out field by field, then introduces the small set of instructions (XINIT, XCONT, XZERO) that start and chain commands.

## 4.1 Command Word Format

The D operand to **XINIT**, **XCONT**, and **XZERO** contains:

```{=latex}
\DiagCommandWord
```

## 4.2 Mode Field D[31:28]

| D[31:28] | Category | Data Source | Data Destination |
|----------|----------|-------------|------------------|
| `%0000`-`%0011` | IMM→LUT | S operand | LUT → Pins/DACs |
| `%0100`-`%0111` | IMM→Direct | S operand | Pins/DACs |
| `%0111` | RF→LUT | RDFAST | LUT → Pins/DACs |
| `%1000`-`%1011` | RF→Direct | RDFAST | Pins/DACs |
| `%1011` | RF→RGB | RDFAST | Colorspace → Pins/DACs |
| `%1100`-`%1111` | Capture | Pins | DACs/WRFAST |
| `%1111` | ADC | ADC | DACs/WRFAST |
| `%1111_x111` | DDS/Goertzel | LUT | DACs + Analysis |

## 4.3 DAC Routing Field D[27:24]

The %dddd field controls DAC channel assignment. See Chapter 11 for the complete routing table.

## 4.4 Enable/Write Field D[23]

| Mode Type | D[23] = 0 | D[23] = 1 |
|-----------|-----------|-----------|
| Output modes | Pins disabled | Pins enabled |
| Input modes | WRFAST disabled | WRFAST enabled |

## 4.5 Pin Group Field D[22:20]

Selects which 32-pin block the streamer addresses:

| %ppp | Pin Range |
|------|-----------|
| `%000` | Pins 31..0 |
| `%001` | Pins 39..8 |
| `%010` | Pins 47..16 |
| `%011` | Pins 55..24 |
| `%100` | Pins 63..32 |
| `%101` | Pins 7..0, 63..40 (wrap) |
| `%110` | Pins 15..0, 63..48 (wrap) |
| `%111` | Pins 23..0, 63..56 (wrap) |

## 4.6 Count Field D[15:0]

Specifies the number of NCO rollovers before the command completes.

- A count of 1 to 65,534 transfers that many data elements, then the command completes
- A count of `$FFFF` (65,535) streams **perpetually** — the command runs until a new command is issued or **XSTOP** stops it
- A count of 0 stops the streamer (this is exactly what **XSTOP** / `XINIT #0,#0` does)

## 4.7 Streamer Instructions

| Instruction | Syntax | Effect |
|-------------|--------|--------|
| **SETXFRQ** | `SETXFRQ {#}D` | Set NCO frequency |
| **XINIT** | `XINIT {#}D,{#}S` | Start immediately, zero phase |
| **XCONT** | `XCONT {#}D,{#}S` | Buffer command, continue phase |
| **XZERO** | `XZERO {#}D,{#}S` | Buffer command, zero phase |
| **XSTOP** | `XSTOP` | Stop immediately (alias: `XINIT #0,#0`) |
| **GETXACC** | `GETXACC D` | Get Goertzel accumulators |

**XINIT** starts the streamer immediately, interrupting any current operation and zeroing the NCO phase.

**XCONT** and **XZERO** buffer a command that executes on the final rollover of the current command. **XCONT** preserves NCO phase; **XZERO** resets it.

💡 **Tip:** Use **XZERO** at video line boundaries to prevent phase drift accumulation across lines.

⚠️ **Pitfall:** Issuing **XCONT** or **XZERO** when no command is active causes unpredictable behavior. Use **XINIT** to start the streamer initially.

# Part II: Mode Reference

The streamer's modes are the heart of this reference. This Part documents each family in turn — immediate, hub-streamed, video, pin-capture, ADC, and the special DDS/Goertzel mode. Each chapter opens with what its modes are *for* before giving the exact encodings.

# Chapter 5: Immediate Modes

Immediate modes are the simplest place to start. Instead of streaming from memory, the data you want to output is a value you hand the streamer directly, in the S operand. Reach for them when you have a small, fixed pattern to emit — a handful of pixels, a test pattern, a short bit sequence — and do not want to set up a hub buffer. The data can go straight to the pins and DACs, or pass through the LUT for palette expansion.

## 5.1 Immediate → LUT → Pins/DACs

The S operand provides index values into the LUT. LUT data drives pins and DACs.

| Mode | Symbol | Elements | Bits/Element |
|------|--------|----------|--------------|
| `%0000` | `X_IMM_32X1_LUT` | 32 | 1 |
| `%0001` | `X_IMM_16X2_LUT` | 16 | 2 |
| `%0010` | `X_IMM_8X4_LUT` | 8 | 4 |
| `%0011` | `X_IMM_4X8_LUT` | 4 | 8 |

**D[19:16] Field:** LUT base address bits [8:5] (`%bbbb` → LUT address `%bbbb_00000`)

**S Operand:** 32-bit immediate data containing packed index values

**Operation:** On each NCO rollover, the next index value selects a LUT entry. The LUT long drives all 32 pins and/or DAC channels.

**Example:**

```pasm2
' Output 32 1-bit pixels using 2-entry palette at LUT $000
        xinit   ##X_IMM_32X1_LUT | X_PINS_ON + 32, ##$AAAA_5555
```

## 5.2 Immediate → Pins/DACs

The S operand drives pins and DACs directly without LUT lookup.

| Mode | Symbol | Pins | DAC Channels |
|------|--------|------|--------------|
| `%0100` | `X_IMM_32X1_1DAC1` | 1 | 1 |
| `%0101` | `X_IMM_16X2_2DAC1` | 2 | 1 |
| `%0101` | `X_IMM_16X2_1DAC2` | 1 | 2 |
| `%0110` | `X_IMM_8X4_4DAC1` | 4 | 1 |
| `%0110` | `X_IMM_8X4_2DAC2` | 2 | 2 |
| `%0110` | `X_IMM_8X4_1DAC4` | 1 | 4 |
| `%0110` | `X_IMM_4X8_4DAC2` | 4 | 2 |
| `%0110` | `X_IMM_4X8_2DAC4` | 2 | 4 |
| `%0110` | `X_IMM_4X8_1DAC8` | 1 | 8 |
| `%0110` | `X_IMM_2X16_4DAC4` | 4 | 4 |
| `%0111` | `X_IMM_2X16_2DAC8` | 2 | 8 |
| `%0111` | `X_IMM_1X32_4DAC8` | 4 | 8 |

**D[19:16] Field:** Mode variant selector

**S Operand:** Packed data values

**Example:**

```pasm2
' Output 8 bytes to 1 pin, 8 bits each (serial)
        xinit   ##X_IMM_4X8_1DAC8 | X_PINS_ON + pin<<17 + 8, ##$12345678
```

# Chapter 6: RDFAST Modes

RDFAST modes are the workhorse of the streamer. Where immediate modes carry a single fixed value, these stream a continuous flow of data out of hub memory — a framebuffer, an audio clip, a bitmap — onto the pins or DACs. This is what you use for anything longer than a few elements. The data arrives through the FIFO, which must be primed with **RDFAST** before the streamer command runs.

⚠️ **Pitfall:** RDFAST modes require FIFO setup before the streamer command. Without **RDFAST** initialization, the FIFO contains undefined data.

## 6.1 RDFAST → LUT → Pins/DACs

Hub data serves as LUT index values.

| Mode | Symbol | Hub Read | Elements | Bits/Element |
|------|--------|----------|----------|--------------|
| `%0111_001a` | `X_RFLONG_32X1_LUT` | RFLONG | 32 | 1 |
| `%0111_010a` | `X_RFLONG_16X2_LUT` | RFLONG | 16 | 2 |
| `%0111_011a` | `X_RFLONG_8X4_LUT` | RFLONG | 8 | 4 |
| `%0111_1000` | `X_RFLONG_4X8_LUT` | RFLONG | 4 | 8 |

**S[3:0]:** LUT base address bits [8:5]

**%a bit:** Alternate bit order (0 = LSB first, 1 = MSB first)

**Example:**

```pasm2
' Setup FIFO
        rdfast  #0, ##bitmap_addr

' Stream 640 pixels through 256-color palette at LUT $000
        xinit   ##X_RFLONG_4X8_LUT | X_PINS_ON + base<<17 + 640, #0
```

## 6.2 RDFAST → Pins/DACs

Hub data drives pins and DACs directly.

| Mode | Symbol | Hub Read | Pins | DAC Bits |
|------|--------|----------|------|----------|
| `%1000` | `X_RFBYTE_1P_1DAC1` | RFBYTE | 1 | 1 |
| `%1001` | `X_RFBYTE_2P_2DAC1` | RFBYTE | 2 | 1 |
| `%1001` | `X_RFBYTE_2P_1DAC2` | RFBYTE | 1 | 2 |
| `%1010` | `X_RFBYTE_4P_4DAC1` | RFBYTE | 4 | 1 |
| `%1010` | `X_RFBYTE_4P_2DAC2` | RFBYTE | 2 | 2 |
| `%1010` | `X_RFBYTE_4P_1DAC4` | RFBYTE | 1 | 4 |
| `%1010` | `X_RFBYTE_8P_4DAC2` | RFBYTE | 4 | 2 |
| `%1010` | `X_RFBYTE_8P_2DAC4` | RFBYTE | 2 | 4 |
| `%1010` | `X_RFBYTE_8P_1DAC8` | RFBYTE | 1 | 8 |
| `%1010` | `X_RFWORD_16P_4DAC4` | RFWORD | 4 | 4 |
| `%1011` | `X_RFWORD_16P_2DAC8` | RFWORD | 2 | 8 |
| `%1011` | `X_RFLONG_32P_4DAC8` | RFLONG | 4 | 8 |

**Example:**

```pasm2
' Stream bytes to 8 pins
        rdfast  #0, ##buffer
        xinit   ##X_RFBYTE_8P_1DAC8 | X_PINS_ON + base<<17 + 256, #0
```

# Chapter 7: RGB Video Modes

Video is the streamer's headline act, and it earns its own family of modes because pixels are not just bytes. A color pixel must be unpacked into red, green, and blue and pushed out in a form a monitor understands. These RGB modes pull pixel data from a framebuffer and run it through the P2's colorspace converter on the way to the pins — so your code stores a picture and the streamer turns it into a signal. The modes differ mainly in how many bits each pixel uses, trading color depth against memory.

## 7.1 RGB Format Modes

| Mode | Symbol | Hub Read | Format | Bits |
|------|--------|----------|--------|------|
| `%1011_0010` | `X_RFBYTE_LUMA8` | RFBYTE | Luminance | 8 |
| `%1011_0011` | `X_RFBYTE_RGBI8` | RFBYTE | RGBI | 2:2:2:2 |
| `%1011_0100` | `X_RFBYTE_RGB8` | RFBYTE | RGB | 3:3:2 |
| `%1011_0101` | `X_RFWORD_RGB16` | RFWORD | RGB | 5:6:5 |
| `%1011_0110` | `X_RFLONG_RGB24` | RFLONG | RGB | 8:8:8 |

## 7.2 Color Format Details

```{=latex}
\DiagRgbFormats
```

**LUMA8:** 8-bit luminance. The `S[2:0]` field selects the output color; the byte sets its intensity.

**RGBI8 (2:2:2:2):** Two bits each for red, green, and blue, plus a 2-bit intensity field.

**RGB8 (3:3:2):** Three bits red, three bits green, two bits blue. Compact format for 256-color graphics.

**RGB16 (5:6:5):** Five bits red, six bits green, five bits blue. Standard 65,536-color format.

**RGB24 (8:8:8):** Eight bits each for R, G, B. True color, one byte wasted per pixel.

## 7.3 RGB Mode Example

```pasm2
' VGA 640×480 RGB16 output
        rdfast  ##640*480*2/64, ##framebuffer
        setxfrq ##$0CCC_CCCD                    ' 25 MHz pixel rate

        xcont   ##X_RFWORD_RGB16 | X_PINS_ON | X_DACS_3_2_1_0 + base<<17 + 640, #0
```

💡 **Tip:** RGB16 (`X_RFWORD_RGB16`) provides the best balance of color depth and memory efficiency for most video applications.

# Chapter 8: WRFAST Input Modes

Here the pipe runs the other way. Instead of driving the pins, these modes *watch* them: on every NCO beat the streamer samples a group of pins and writes the result into hub memory. That turns a COG into a logic analyzer, capturing fast digital activity that software could never sample quickly enough. The captured data flows out through the write FIFO, which — like its read counterpart — must be primed first.

⚠️ **Pitfall:** Initialize the write FIFO with **WRFAST** before issuing capture commands.

## 8.1 Pin Capture Modes

| Mode | Symbol | Pins | DAC Bits | Hub Write |
|------|--------|------|----------|-----------|
| `%1100` | `X_1P_1DAC1_WFBYTE` | 1 | 1 | WFBYTE |
| `%1101` | `X_2P_2DAC1_WFBYTE` | 2 | 1 | WFBYTE |
| `%1101` | `X_2P_1DAC2_WFBYTE` | 1 | 2 | WFBYTE |
| `%1110` | `X_4P_4DAC1_WFBYTE` | 4 | 1 | WFBYTE |
| `%1110` | `X_4P_2DAC2_WFBYTE` | 2 | 2 | WFBYTE |
| `%1110` | `X_4P_1DAC4_WFBYTE` | 1 | 4 | WFBYTE |
| `%1110` | `X_8P_4DAC2_WFBYTE` | 4 | 2 | WFBYTE |
| `%1110` | `X_8P_2DAC4_WFBYTE` | 2 | 4 | WFBYTE |
| `%1110` | `X_8P_1DAC8_WFBYTE` | 1 | 8 | WFBYTE |
| `%1110` | `X_16P_4DAC4_WFWORD` | 4 | 4 | WFWORD |
| `%1111` | `X_16P_2DAC8_WFWORD` | 2 | 8 | WFWORD |
| `%1111` | `X_32P_4DAC8_WFLONG` | 4 | 8 | WFLONG |

**D[23] = %w:** Must be 1 to enable WRFAST writes

**Example:**

```pasm2
' Capture 32 pins to Hub at 10 MHz
        wrfast  #0, ##capture_buffer
        setxfrq ##$0CCC_CCCD

        xinit   ##X_32P_4DAC8_WFLONG | X_WRITE_ON + base<<17 + 1000, #0
        waitxfi
```

# Chapter 9: ADC Sampling Modes

ADC modes are the analog cousin of the pin-capture modes in the previous chapter. Instead of recording whether a pin is high or low, they record *how much* — the digitized voltage on an ADC-capable pin. Streaming those readings into memory at a steady rate turns a COG into an oscilloscope or a data logger. Reach for these when you need to capture a waveform, not just a bit.

## 9.1 ADC Capture Modes

| Mode | Symbol | ADCs | Pins | Hub Write |
|------|--------|------|------|-----------|
| `%1111_0010` | `X_1ADC8_0P_1DAC8_WFBYTE` | 1 | 0 | WFBYTE |
| `%1111_0011` | `X_1ADC8_8P_2DAC8_WFWORD` | 1 | 8 | WFWORD |
| `%1111_0100` | `X_2ADC8_0P_2DAC8_WFWORD` | 2 | 0 | WFWORD |
| `%1111_0101` | `X_2ADC8_16P_4DAC8_WFLONG` | 2 | 16 | WFLONG |
| `%1111_0110` | `X_4ADC8_0P_4DAC8_WFLONG` | 4 | 0 | WFLONG |

**ADC Pin Requirements:** ADC-capable pins must be configured for ADC mode using **WRPIN** before sampling.

## 9.2 ADC Configuration Example

```pasm2
' Configure pin for ADC
        wrpin   ##P_ADC_100X, #adc_pin
        drvl    #adc_pin

' Capture 1024 ADC samples
        wrfast  #0, ##adc_buffer
        xinit   ##X_1ADC8_0P_1DAC8_WFBYTE | X_WRITE_ON + adc_pin<<17 + 1024, #0
        waitxfi
```

🔧 **Hardware:** ADC readings are 8-bit values. For higher resolution, use smart pin ADC modes with post-processing.

# Chapter 10: DDS/Goertzel Mode

This is the streamer's cleverest mode, and it does two things at once (Chapter 1 introduced both in plain terms). **DDS** *generates* a signal — it steps through a waveform table to synthesize a precise tone or arbitrary shape. **Goertzel** *measures* one — it reports how much of a single chosen frequency is present in an incoming signal, the trick behind touch-tone decoding and ultrasonic ranging. Uniquely, this mode advances on **every clock cycle**, not just on NCO rollovers, which is what gives it the resolution to do real signal processing.

## 10.1 Mode Variants

| Mode | Symbol | Filter |
|------|--------|--------|
| `%1111_0ppp_p111` | `X_DDS_GOERTZEL_SINC1` | SINC1 |
| `%1111_1ppp_p111` | `X_DDS_GOERTZEL_SINC2` | SINC2 |

## 10.2 Operation

On each system clock:

1. NCO phase selects LUT entry: `LUT[NCO[30:22]]`
2. NCO phase advances: `NCO += frequency`
3. LUT bytes output to DACs (XOR `$80` for unsigned)
4. ADC input multiplied by sine/cosine from LUT
5. Products accumulated in sine/cosine registers

```formula
DAC3 := LUT.byte[3] ^ $80
DAC2 := LUT.byte[2] ^ $80
DAC1 := LUT.byte[1] ^ $80
DAC0 := LUT.byte[0] ^ $80

sin := LUT.byte[3] (sign-extended)
cos := LUT.byte[2] (sign-extended)
m := ADC_bit ? +1 : -1

sin_acc += sin × m
cos_acc += cos × m
```

```{=latex}
\DiagDdsGoertzel
```

## 10.3 LUT Setup

The LUT must contain 512 entries with signed sine/cosine values:

```spin2
' Build sine/cosine table
repeat i from 0 to 511
  cos, sin := polxy(127, i << 23)
  t.byte[3] := sin          ' Sine for Goertzel
  t.byte[2] := cos          ' Cosine for Goertzel
  t.byte[1] := 0            ' Unused
  t.byte[0] := sin          ' Optional DAC output
  wrlut(t, i)
```

## 10.4 SINC1 vs SINC2

| Characteristic | SINC1 | SINC2 |
|---------------|-------|-------|
| Accumulation | Direct | Double integration |
| Q factor | Lower | Higher |
| Selectivity | Broader | Sharper |
| Max amplitude | ±127 (full signed byte) | Reduced (prevents overflow) |

⚠️ **Pitfall:** SINC2 double-integrates, so its accumulators grow far faster than SINC1's. Scale the LUT waveform amplitude well below the ±127 signed-byte range to prevent accumulator overflow.

## 10.5 Reading Results

```pasm2
        getxacc cos_result          ' Cosine accumulator → D
        mov     sin_result, 0-0     ' Sine accumulator → next S

        qvector cos_result, sin_result
        getqx   magnitude
        getqy   phase
```

## 10.6 Frequency Calculation

To detect frequency F at clock rate CLK:

```formula
frequency = $1_0000_0000 × F / CLK
```

🔧 **Hardware:** The 32-bit frequency word gives sub-Hz resolution at typical system clocks (`clock_frequency / 2³²`, about 0.06 Hz at 250 MHz).

# Part III: Configuration Reference

These chapters cover the choices that apply across modes — where data goes among the DAC channels, which pins are driven, how commands are named, and how your code stays in step with the streamer.

# Chapter 11: DAC Channel Configuration

Many modes send data to the DAC channels, but none of them say *which* channels, or *how*. That is this chapter's job. The %dddd routing field is the knob from Chapter 1's stereo example: it decides how the streamer's data spreads across the four 8-bit DAC channels — one channel, a stereo pair, a differential pair, or all four independently. The same data becomes mono, stereo, or four-channel purely by changing this field.

## 11.1 DAC Routing Table

| %dddd | DAC3 | DAC2 | DAC1 | DAC0 | Symbol |
|-------|------|------|------|------|--------|
| `%0000` | -- | -- | -- | -- | `X_DACS_OFF` |
| `%0001` | X0 | X0 | X0 | X0 | `X_DACS_0_0_0_0` |
| `%0010` | -- | -- | X0 | X0 | `X_DACS_X_X_0_0` |
| `%0011` | X0 | X0 | -- | -- | `X_DACS_0_0_X_X` |
| `%0100` | -- | -- | -- | X0 | `X_DACS_X_X_X_0` |
| `%0101` | -- | -- | X0 | -- | `X_DACS_X_X_0_X` |
| `%0110` | -- | X0 | -- | -- | `X_DACS_X_0_X_X` |
| `%0111` | X0 | -- | -- | -- | `X_DACS_0_X_X_X` |
| `%1000` | !X0 | X0 | !X0 | X0 | `X_DACS_0N0_0N0` |
| `%1001` | -- | -- | !X0 | X0 | `X_DACS_X_X_0N0` |
| `%1010` | !X0 | X0 | -- | -- | `X_DACS_0N0_X_X` |
| `%1011` | X1 | X0 | X1 | X0 | `X_DACS_1_0_1_0` |
| `%1100` | -- | -- | X1 | X0 | `X_DACS_X_X_1_0` |
| `%1101` | X1 | X0 | -- | -- | `X_DACS_1_0_X_X` |
| `%1110` | !X1 | X1 | !X0 | X0 | `X_DACS_1N1_0N0` |
| `%1111` | X3 | X2 | X1 | X0 | `X_DACS_3_2_1_0` |

**Legend:**
- `--` = No override (SETDACS value used)
- `!` = One's complement (inverted)
- `X0`-`X3` = Streamer data channels

## 11.2 DAC Pin Mapping

DAC channels drive pins based on the pin's two LSBs:

| DAC Channel | Pin Pattern | Example Pins |
|-------------|-------------|--------------|
| DAC0 | `%xxxx00` | 0, 4, 8, 12, 16... |
| DAC1 | `%xxxx01` | 1, 5, 9, 13, 17... |
| DAC2 | `%xxxx10` | 2, 6, 10, 14, 18... |
| DAC3 | `%xxxx11` | 3, 7, 11, 15, 19... |

🔧 **Hardware:** Each DAC channel can only drive pins matching its channel number in the two LSBs. This is a silicon constraint, not a configuration option.

## 11.3 Common DAC Configurations

**Mono Audio (single channel):**
```pasm2
mode := X_RFBYTE_1P_1DAC1 | X_DACS_0_0_0_0 | X_PINS_ON + pin<<17 + count
```

**Stereo Audio (two channels):**
```pasm2
mode := X_RFWORD_16P_2DAC8 | X_DACS_X_X_1_0 | X_PINS_ON + pin<<17 + count
```

**Differential Output (noise rejection):**
```pasm2
mode := X_RFBYTE_1P_1DAC1 | X_DACS_X_X_0N0 | X_PINS_ON + pin<<17 + count
```

**Four-Channel Video (RGB + sync):**
```pasm2
mode := X_RFLONG_32P_4DAC8 | X_DACS_3_2_1_0 | X_PINS_ON + pin<<17 + count
```

# Chapter 12: Pin Selection and Control

A streamer command also has to say *which* pins it drives or samples, and that is less obvious than it sounds: the P2 has 64 pins, but a command addresses them 32 at a time, through a window you choose. This chapter covers how to aim the streamer at the right pins, how to enable output, and a few smaller controls such as bit ordering.

## 12.1 Pin Group Selection

The %ppp field in D[22:20] selects the 32-pin block:

| %ppp | Pin Range | Use Case |
|------|-----------|----------|
| `%000` | 31..0 | Lower pins |
| `%001` | 39..8 | Mid-lower pins |
| `%010` | 47..16 | Middle pins |
| `%011` | 55..24 | Mid-upper pins |
| `%100` | 63..32 | Upper pins |
| `%101` | 7..0, 63..40 | Wrap-around |
| `%110` | 15..0, 63..48 | Wrap-around |
| `%111` | 23..0, 63..56 | Wrap-around |

## 12.2 Sub-Pin Selection

For modes using fewer than 8 pins, D[19:17] refines selection within the group:

| D[19:17] | 1-Pin | 2-Pin | 4-Pin |
|----------|-------|-------|-------|
| `%000` | Pin 0 | Pins 1..0 | Pins 3..0 |
| `%001` | Pin 1 | Pins 3..2 | Pins 7..4 |
| `%010` | Pin 2 | Pins 5..4 | Pins 11..8 |
| `%011` | Pin 3 | Pins 7..6 | Pins 15..12 |
| `%100` | Pin 4 | Pins 9..8 | Pins 19..16 |
| `%101` | Pin 5 | Pins 11..10 | Pins 23..20 |
| `%110` | Pin 6 | Pins 13..12 | Pins 27..24 |
| `%111` | Pin 7 | Pins 15..14 | Pins 31..28 |

## 12.3 Enable Control

**Output Modes:** D[23] must be 1 to drive pins

```pasm2
' Pin output enabled
mode := X_RFBYTE_8P_1DAC8 | X_PINS_ON + pin<<17 + count

' Pin output disabled (DACs only)
mode := X_RFBYTE_8P_1DAC8 | X_PINS_OFF + pin<<17 + count
```

**Input Modes:** D[23] must be 1 to write to Hub

```pasm2
' WRFAST enabled
mode := X_32P_4DAC8_WFLONG | X_WRITE_ON + pin<<17 + count

' WRFAST disabled (DACs only)
mode := X_32P_4DAC8_WFLONG | X_WRITE_OFF + pin<<17 + count
```

## 12.4 Alternate Bit Order

The %a bit in D[16] controls bit ordering for 1/2/4-bit modes:

| D[16] | Order | Symbol |
|-------|-------|--------|
| 0 | LSB first (default) | `X_ALT_OFF` |
| 1 | MSB first | `X_ALT_ON` |

💡 **Tip:** Use MSB-first (`X_ALT_ON`) for SPI protocols that transmit MSB first.

# Chapter 13: Programming Constants

You rarely build a command word bit by bit. Instead you OR together named constants — `X_RFWORD_RGB16`, `X_PINS_ON`, `X_DACS_3_2_1_0` — and the compiler assembles the value for you. This chapter is the catalog of those built-in symbols and shows how they compose. Skim it once to learn the naming pattern; after that the names read almost like sentences.

## 13.1 Mode Symbols

**Immediate → LUT → Pins/DACs:**

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_IMM_32X1_LUT` | `%0000 << 28` | 32×1-bit → LUT |
| `X_IMM_16X2_LUT` | `%0001 << 28` | 16×2-bit → LUT |
| `X_IMM_8X4_LUT` | `%0010 << 28` | 8×4-bit → LUT |
| `X_IMM_4X8_LUT` | `%0011 << 28` | 4×8-bit → LUT |

**Immediate → Pins/DACs:**

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_IMM_32X1_1DAC1` | `%0100 << 28` | 32×1-bit direct |
| `X_IMM_16X2_2DAC1` | `%0101 << 28` | 16×2-bit, 2-pin |
| `X_IMM_16X2_1DAC2` | `%0101 << 28 + 2<<16` | 16×2-bit, 1-pin |
| `X_IMM_8X4_4DAC1` | `%0110 << 28` | 8×4-bit, 4-pin |
| `X_IMM_8X4_2DAC2` | `%0110 << 28 + 2<<16` | 8×4-bit, 2-pin |
| `X_IMM_8X4_1DAC4` | `%0110 << 28 + 4<<16` | 8×4-bit, 1-pin |

**RDFAST → Pins/DACs:**

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_RFBYTE_1P_1DAC1` | `%1000 << 28` | RFBYTE, 1-pin |
| `X_RFBYTE_2P_2DAC1` | `%1001 << 28` | RFBYTE, 2-pin |
| `X_RFBYTE_4P_4DAC1` | `%1010 << 28` | RFBYTE, 4-pin |
| `X_RFBYTE_8P_1DAC8` | `%1010 << 28 + $E<<16` | RFBYTE, 8-pin |
| `X_RFWORD_16P_4DAC4` | `%1010 << 28 + $F<<16` | RFWORD, 16-pin |
| `X_RFWORD_16P_2DAC8` | `%1011 << 28` | RFWORD, 16-pin |
| `X_RFLONG_32P_4DAC8` | `%1011 << 28 + 1<<16` | RFLONG, 32-pin |

**RDFAST → RGB:**

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_RFBYTE_LUMA8` | `%1011 << 28 + 2<<16` | 8-bit grayscale |
| `X_RFBYTE_RGBI8` | `%1011 << 28 + 3<<16` | RGBI 2:2:2:2 |
| `X_RFBYTE_RGB8` | `%1011 << 28 + 4<<16` | RGB 3:3:2 |
| `X_RFWORD_RGB16` | `%1011 << 28 + 5<<16` | RGB 5:6:5 |
| `X_RFLONG_RGB24` | `%1011 << 28 + 6<<16` | RGB 8:8:8 |

**DDS/Goertzel:**

| Symbol | Value | Description |
|--------|-------|-------------|
| `X_DDS_GOERTZEL_SINC1` | `%1111 << 28 + 7<<16` | SINC1 filter |
| `X_DDS_GOERTZEL_SINC2` | `%1111 << 28 + $87<<16` | SINC2 filter |

## 13.2 Control Symbols

| Symbol | Value | Effect |
|--------|-------|--------|
| `X_PINS_OFF` | `%0 << 23` | Disable pin output |
| `X_PINS_ON` | `%1 << 23` | Enable pin output |
| `X_WRITE_OFF` | `%0 << 23` | Disable WRFAST |
| `X_WRITE_ON` | `%1 << 23` | Enable WRFAST |
| `X_ALT_OFF` | `%0 << 16` | LSB first |
| `X_ALT_ON` | `%1 << 16` | MSB first |

## 13.3 DAC Symbols

| Symbol | Value | Configuration |
|--------|-------|---------------|
| `X_DACS_OFF` | `%0000 << 24` | No DAC output |
| `X_DACS_0_0_0_0` | `%0001 << 24` | X0 on all channels |
| `X_DACS_X_X_0_0` | `%0010 << 24` | X0 on channels 0,1 |
| `X_DACS_0_0_X_X` | `%0011 << 24` | X0 on channels 2,3 |
| `X_DACS_X_X_X_0` | `%0100 << 24` | X0 on channel 0 |
| `X_DACS_X_X_0_X` | `%0101 << 24` | X0 on channel 1 |
| `X_DACS_X_0_X_X` | `%0110 << 24` | X0 on channel 2 |
| `X_DACS_0_X_X_X` | `%0111 << 24` | X0 on channel 3 |
| `X_DACS_0N0_0N0` | `%1000 << 24` | Differential pairs |
| `X_DACS_X_X_0N0` | `%1001 << 24` | Diff on 0,1 |
| `X_DACS_0N0_X_X` | `%1010 << 24` | Diff on 2,3 |
| `X_DACS_1_0_1_0` | `%1011 << 24` | Stereo pairs |
| `X_DACS_X_X_1_0` | `%1100 << 24` | Stereo on 0,1 |
| `X_DACS_1_0_X_X` | `%1101 << 24` | Stereo on 2,3 |
| `X_DACS_1N1_0N0` | `%1110 << 24` | Differential stereo |
| `X_DACS_3_2_1_0` | `%1111 << 24` | All 4 independent |

## 13.4 Symbol Composition

Build complete commands by combining symbols:

```spin2
' VGA 640-pixel visible line
mode := X_RFWORD_RGB16 | X_PINS_ON | X_DACS_3_2_1_0 + vga_base<<17 + 640

' SPI byte output (MSB first)
mode := X_IMM_8X4_1DAC4 | X_PINS_ON | X_ALT_ON + spi_pin<<17 + 8

' Goertzel analysis (differential DAC)
mode := X_DDS_GOERTZEL_SINC1 | X_DACS_0N0_0N0 + adc_pin<<17 + cycles
```

# Chapter 14: Events and Synchronization

Because the streamer runs on its own, your code needs a way to ask *where it is up to* — is it ready for another command, has it finished, did the NCO just roll over? The streamer raises events for exactly these moments, and this chapter shows how to poll them, wait on them, or branch on them. Getting this right is how you chain commands seamlessly and keep video and audio free of glitches.

## 14.1 Streamer Events

| Event # | Symbol | Trigger Condition |
|---------|--------|-------------------|
| 10 | `EVENT_XMT` | Streamer ready for new command |
| 11 | `EVENT_XFI` | Streamer finished (no pending command) |
| 12 | `EVENT_XRO` | NCO rollover occurred |
| 13 | `EVENT_XRL` | LUT address $1FF read |

## 14.2 Event Instructions

**Polling (non-blocking):**

| Instruction | Effect |
|-------------|--------|
| `POLLXMT WC` | C = 1 if ready for command |
| `POLLXFI WC` | C = 1 if finished |
| `POLLXRO WC` | C = 1 if NCO rolled over |
| `POLLXRL WC` | C = 1 if LUT $1FF read |

**Waiting (blocking):**

| Instruction | Effect |
|-------------|--------|
| `WAITXMT` | Wait until ready for command |
| `WAITXFI` | Wait until finished |
| `WAITXRO` | Wait until NCO rollover |
| `WAITXRL` | Wait until LUT $1FF read |

**Conditional Jumps:**

| Instruction | Condition |
|-------------|-----------|
| `JXMT label` | Jump if ready |
| `JNXMT label` | Jump if not ready |
| `JXFI label` | Jump if finished |
| `JNXFI label` | Jump if not finished |
| `JXRO label` | Jump if rollover |
| `JNXRO label` | Jump if no rollover |
| `JXRL label` | Jump if LUT $1FF |
| `JNXRL label` | Jump if not LUT $1FF |

## 14.3 Event Clearing

Events clear automatically on:
- **XINIT**, **XCONT**, **XZERO** execution
- **POLL**, **WAIT**, or **J** instruction execution for that event

## 14.4 Synchronization Patterns

**Wait for completion:**
```pasm2
        xinit   mode, data
        waitxfi                     ' Block until done
```

**Chain commands without gaps:**
```pasm2
        xinit   mode1, data1        ' Start first command
        xcont   mode2, data2        ' Queue second command
        xcont   mode3, data3        ' Queue third command
        waitxfi                     ' Wait for all to finish
```

**Video line timing:**
```pasm2
line:   xzero   m_sync, sync_data   ' Sync pulse (phase zeroed)
        xcont   m_back, #0          ' Back porch
        xcont   m_visible, #0       ' Visible pixels
        xcont   m_front, #0         ' Front porch
        jmp     #line
```

💡 **Tip:** Use **XZERO** at line start to prevent phase accumulation errors over many lines.

# Part IV: Applications

Here the modes come together into the things people actually build: video, high-speed serial, signal processing, and the patterns that combine them.

# Chapter 15: Video Output

Part IV puts the pieces together into real applications, beginning with the streamer's signature use: video. This chapter walks through generating VGA, HDMI, and composite signals — combining the RGB modes of Chapter 7, the NCO timing of Chapter 3, and the sync discipline that keeps a picture stable. The encoding differs by standard, but the shape is always the same: stream a framebuffer, on the beat, line after line.

## 15.1 VGA Output

VGA uses analog RGB via DAC channels with composite sync.

**Hardware Requirements:**
- Three DAC pins for R, G, B
- One pin for composite sync (active-low)
- Resistor DAC network or direct DAC output

**Timing Structure (640×480 @ 60 Hz):**

| Element | Pixels | Duration @ 25.175 MHz |
|---------|--------|----------------------|
| Visible | 640 | 25.42 µs |
| Front porch | 16 | 0.64 µs |
| Sync pulse | 96 | 3.81 µs |
| Back porch | 48 | 1.91 µs |
| **Total line** | **800** | **31.78 µs** |

```{=latex}
\DiagVgaTiming
```

**Example:**

```pasm2
DAT             org

                ' Setup 250 MHz from 20 MHz crystal
                hubset  ##%1_000001_0000011000_1111_10_00
                waitx   ##20_000_000/200
                hubset  ##%1_000001_0000011000_1111_10_11

                rdfast  ##640*480*2/64, ##framebuffer
                setxfrq ##$0CCC_CCCD            ' 25 MHz pixel rate

field:          mov     line_count, #480

visible_loop:   call    #hsync
                xcont   m_visible, #0           ' 640 RGB16 pixels
                djnz    line_count, #visible_loop

                callpa  #10, #blank_lines       ' Bottom blanking
                call    #vsync
                callpa  #33, #blank_lines       ' Top blanking
                jmp     #field

hsync:          xcont   m_front, sync_off       ' 16 pixels front porch
                xzero   m_sync, sync_on         ' 96 pixels sync
          _ret_ xcont   m_back, sync_off        ' 48 pixels back porch

blank_lines:    call    #hsync
                xcont   m_blank, sync_off
          _ret_ djnz    pa, #blank_lines

vsync:          ' Two lines with vsync active
                xcont   m_front, sync_on
                xzero   m_sync, sync_on
                xcont   m_back, sync_on
                xcont   m_blank, sync_on
                xcont   m_front, sync_on
                xzero   m_sync, sync_on
                xcont   m_back, sync_on
          _ret_ xcont   m_blank, sync_on

' Constants
sync_off        long    %00_01_01_01            ' RGB active, sync off
sync_on         long    %00_01_01_00            ' RGB active, sync on

m_front         long    $F080_0000 + vga_base<<17 + 16
m_sync          long    $F080_0000 + vga_base<<17 + 96
m_back          long    $F080_0000 + vga_base<<17 + 48
m_visible       long    $B085_0000 + vga_base<<17 + 640  ' RGB16
m_blank         long    $F080_0000 + vga_base<<17 + 640

vga_base        long    0                       ' Set to actual pin
line_count      res     1
```

## 15.2 HDMI/DVI Output

HDMI uses TMDS encoding via the colorspace converter. Requires 10× pixel clock.

**Hardware Requirements:**
- Eight pins in sequence for TMDS pairs
- 1 mA pin drive strength
- System clock = 10 × pixel clock

**Configuration:**

```pasm2
                ' Enable DVI forward mode
                setcmod #$100

                ' Configure HDMI pins
                drvl    #7<<6 + hdmi_base
                wrpin   ##%100100_00_00000_0, #7<<6 + hdmi_base

                ' NCO for 1/10 rate (TMDS serialization)
                setxfrq ##$0CCC_CCCD
```

🔧 **Hardware:** HDMI requires the colorspace converter in DVI mode. The converter generates TMDS encoding automatically from RGB data.

## 15.3 Composite Video

Composite video uses the colorspace converter to generate NTSC or PAL signals.

**Configuration:**

```pasm2
                ' Composite mode (NTSC/PAL) — CMOD[6:5] = %11
                setcmod #%11 << 5

                ' NTSC chroma carrier 3.579545 MHz at 250 MHz clock
                ' CFRQ = $1_0000_0000 × carrier / clkfreq
                setcfrq ##$03AA_5B33

                ' Color matrix coefficients
                setcy   ##cy_ntsc
                setci   ##ci_ntsc
                setcq   ##cq_ntsc
```

# Chapter 16: High-Speed Serial (SPI)

Not every streamer job is video or audio. This chapter shows the streamer as a fast, precise bit pump for serial protocols such as SPI — emitting a stream of bits from memory while a smart pin generates the matching clock. The pairing is the point: the streamer handles the data, the smart pin handles the clock, and the two stay locked together for transfers far faster than a software bit-bang.

## 16.1 SPI Output with Streamer

The streamer outputs SPI data while a smart pin generates the clock.

**Configuration:**

```pasm2
                ' Configure clock pin as transition counter
                wrpin   ##P_TRANSITION + P_OE, #spi_clk
                wxpin   ##2, #spi_clk           ' 2 transitions per bit
                drvl    #spi_clk

                ' NCO at half clock rate
                setxfrq ##$4000_0000
```

**Single Byte Transfer:**

```pasm2
spi_byte:       xinit   bmode, pa               ' Output 8 bits
                wypin   #16, #spi_clk           ' 16 clock transitions
          _ret_ waitxfi

bmode           long    X_IMM_8X4_1DAC4 | X_PINS_ON | X_ALT_ON + spi_do<<17 + 8
```

**Bulk Transfer:**

```pasm2
spi_block:      rdfast  #0, ptra                ' Point to data
                xinit   rmode, #0               ' Stream 256 bytes
                wypin   ##256*8*2, #spi_clk     ' Clock transitions
          _ret_ waitxfi

rmode           long    X_RFBYTE_1P_1DAC1 | X_PINS_ON | X_ALT_ON + spi_do<<17 + 256*8
```

## 16.2 Coordinating with WAITXFI

The **WAITXFI** instruction synchronizes streamer completion with clock generation:

```pasm2
                xinit   mode, data
                wypin   transitions, #clk_pin
                waitxfi                         ' Wait for data
                testp   #clk_pin wc             ' Verify clock done
```

⚠️ **Pitfall:** The smart pin clock and streamer operate independently. Verify both complete before starting the next transfer.

# Chapter 17: Signal Processing

This chapter returns to the DDS and Goertzel capabilities of Chapter 10 and puts them to work — generating waveforms with a function generator's precision, and detecting specific frequencies for tone decoding, distance sensing, and measurement. Where Chapter 10 explained the mechanism, this chapter shows the applications.

## 17.1 Goertzel Frequency Detection

Goertzel analysis detects specific frequencies in ADC input.

**Application:** Ultrasonic distance measurement, DTMF decoding, tone detection

**Setup:**

```pasm2
                ' Load sine/cosine table to LUT
                setq2   #$200-1
                rdlong  0, ##sine_table

                ' Configure ADC pin
                wrpin   ##P_ADC_100X, #adc_pin
                drvl    #adc_pin

                ' Configure DAC output (differential)
                wrpin   ##P_DAC_124R_3V + P_CHANNEL, dac_pins
                drvl    dac_pins
```

**Detection Loop:**

```pasm2
detect:         ' Calculate NCO frequency for target
                qfrac   target_freq, clkfreq
                getqx   xfrq

                ' Run Goertzel analysis
                setword dds_cmd, cycles, #0
                setq    xfrq
                xcont   dds_cmd, dds_s

                ' Get result
                getxacc cos_acc
                mov     sin_acc, 0-0

                ' Convert to magnitude
                qvector cos_acc, sin_acc
                getqx   magnitude

                ' Check threshold
                cmp     magnitude, threshold wcz
        if_a    call    #detected

                jmp     #detect

dds_cmd         long    X_DDS_GOERTZEL_SINC1 | X_DACS_0N0_0N0
```

## 17.2 DDS Waveform Generation

DDS synthesizes arbitrary waveforms at precise frequencies.

**Applications:** Function generator, audio synthesis, RF modulation

**Configuration:**

```pasm2
                ' Load waveform to LUT
                setq2   #$200-1
                rdlong  0, ##waveform_table

                ' Set output frequency
                qfrac   output_freq, clkfreq
                getqx   xfrq
                setxfrq xfrq

                ' Continuous output
                xinit   dds_mode, #0
```

💡 **Tip:** The LUT can contain any waveform shape—sine, square, triangle, or arbitrary samples. The NCO steps through the 512 entries at the programmed rate.

# Chapter 18: Integration Patterns

The final chapter collects patterns that cut across everything above: double-buffering so display and rendering never collide, splitting work across multiple COGs, and coordinating the streamer with smart pins. These are the techniques that turn a working streamer demo into a robust system.

## 18.1 Double Buffering

Use two buffers to allow simultaneous rendering and display:

```pasm2
                ' Buffer addresses
                mov     display_buf, ##buffer_a
                mov     render_buf, ##buffer_b

frame_loop:     ' Start displaying current buffer
                rdfast  ##frame_size/64, display_buf

                ' Render to other buffer while displaying
                call    #render_frame

                ' Swap buffers
                mov     temp, display_buf
                mov     display_buf, render_buf
                mov     render_buf, temp

                jmp     #frame_loop
```

## 18.2 Multi-COG Video

Complex video systems span multiple COGs:

| COG | Function |
|-----|----------|
| 0 | Main application |
| 1 | Horizontal timing, pixel streaming |
| 2 | Vertical timing, frame sync |
| 3 | Sprite rendering |

**Synchronization via Hub flags:**

```pasm2
' COG 1: Signal line complete
                wrlong  #1, ##line_done_flag

' COG 2: Wait for line complete
wait_line:      rdlong  temp, ##line_done_flag wz
        if_z    jmp     #wait_line
```

## 18.3 Streamer + Smart Pin Coordination

Many applications combine streamer I/O with smart pin timing:

**Pattern: Streamer data with smart pin clock**

```pasm2
                xinit   data_mode, #0           ' Start data output
                wypin   clocks, #clk_pin        ' Start clock generation
                waitxfi                         ' Wait for data complete
```

**Pattern: Smart pin trigger for streamer**

```pasm2
                akpin   #trigger_pin            ' Acknowledge
wait_trigger:   testp   #trigger_pin wc
        if_nc   jmp     #wait_trigger
                xinit   capture_mode, #0        ' Start capture
```

# Part V: Appendices

# Appendix A: Complete Mode Encoding Table

| D[31:28] | D[19:16] | Mode | Symbol |
|----------|----------|------|--------|
| `%0000` | `%bbbb` | IMM 32×1 → LUT | `X_IMM_32X1_LUT` |
| `%0001` | `%bbbb` | IMM 16×2 → LUT | `X_IMM_16X2_LUT` |
| `%0010` | `%bbbb` | IMM 8×4 → LUT | `X_IMM_8X4_LUT` |
| `%0011` | `%bbbb` | IMM 4×8 → LUT | `X_IMM_4X8_LUT` |
| `%0100` | `%0000` | IMM 32×1 direct | `X_IMM_32X1_1DAC1` |
| `%0101` | `%0000` | IMM 16×2, 2-pin | `X_IMM_16X2_2DAC1` |
| `%0101` | `%0010` | IMM 16×2, 1-pin | `X_IMM_16X2_1DAC2` |
| `%0110` | `%0000` | IMM 8×4, 4-pin | `X_IMM_8X4_4DAC1` |
| `%0110` | `%0010` | IMM 8×4, 2-pin | `X_IMM_8X4_2DAC2` |
| `%0110` | `%0100` | IMM 8×4, 1-pin | `X_IMM_8X4_1DAC4` |
| `%0111` | `%001a` | RFLONG 32×1 → LUT | `X_RFLONG_32X1_LUT` |
| `%0111` | `%010a` | RFLONG 16×2 → LUT | `X_RFLONG_16X2_LUT` |
| `%0111` | `%011a` | RFLONG 8×4 → LUT | `X_RFLONG_8X4_LUT` |
| `%0111` | `%1000` | RFLONG 4×8 → LUT | `X_RFLONG_4X8_LUT` |
| `%1000` | `%pppp` | RFBYTE, 1-pin | `X_RFBYTE_1P_1DAC1` |
| `%1001` | `%ppp0` | RFBYTE, 2-pin | `X_RFBYTE_2P_2DAC1` |
| `%1010` | `%pp00` | RFBYTE, 4-pin | `X_RFBYTE_4P_4DAC1` |
| `%1010` | `%p000` | RFBYTE, 8-pin | `X_RFBYTE_8P_1DAC8` |
| `%1010` | `%1111` | RFWORD, 16-pin | `X_RFWORD_16P_4DAC4` |
| `%1011` | `%0000` | RFWORD, 16-pin | `X_RFWORD_16P_2DAC8` |
| `%1011` | `%0001` | RFLONG, 32-pin | `X_RFLONG_32P_4DAC8` |
| `%1011` | `%0010` | RFBYTE LUMA8 | `X_RFBYTE_LUMA8` |
| `%1011` | `%0011` | RFBYTE RGBI8 | `X_RFBYTE_RGBI8` |
| `%1011` | `%0100` | RFBYTE RGB8 | `X_RFBYTE_RGB8` |
| `%1011` | `%0101` | RFWORD RGB16 | `X_RFWORD_RGB16` |
| `%1011` | `%0110` | RFLONG RGB24 | `X_RFLONG_RGB24` |
| `%1100` | `%pppp` | 1-pin → WFBYTE | `X_1P_1DAC1_WFBYTE` |
| `%1101` | `%ppp0` | 2-pin → WFBYTE | `X_2P_2DAC1_WFBYTE` |
| `%1110` | `%pp00` | 4-pin → WFBYTE | `X_4P_4DAC1_WFBYTE` |
| `%1110` | `%1111` | 16-pin → WFWORD | `X_16P_4DAC4_WFWORD` |
| `%1111` | `%0000` | 16-pin → WFWORD | `X_16P_2DAC8_WFWORD` |
| `%1111` | `%0001` | 32-pin → WFLONG | `X_32P_4DAC8_WFLONG` |
| `%1111` | `%0010` | 1 ADC → WFBYTE | `X_1ADC8_0P_1DAC8_WFBYTE` |
| `%1111` | `%0111` | DDS/Goertzel SINC1 | `X_DDS_GOERTZEL_SINC1` |
| `%1111` | `%0111` (D[23]=1) | DDS/Goertzel SINC2 | `X_DDS_GOERTZEL_SINC2` |

# Appendix B: Symbol Quick Reference

## Mode Symbols

```
X_IMM_32X1_LUT          X_IMM_16X2_LUT          X_IMM_8X4_LUT
X_IMM_4X8_LUT           X_IMM_32X1_1DAC1        X_IMM_16X2_2DAC1
X_IMM_16X2_1DAC2        X_IMM_8X4_4DAC1         X_IMM_8X4_2DAC2
X_IMM_8X4_1DAC4         X_RFLONG_32X1_LUT       X_RFLONG_16X2_LUT
X_RFLONG_8X4_LUT        X_RFLONG_4X8_LUT        X_RFBYTE_1P_1DAC1
X_RFBYTE_2P_2DAC1       X_RFBYTE_4P_4DAC1       X_RFBYTE_8P_1DAC8
X_RFWORD_16P_4DAC4      X_RFWORD_16P_2DAC8      X_RFLONG_32P_4DAC8
X_RFBYTE_LUMA8          X_RFBYTE_RGBI8          X_RFBYTE_RGB8
X_RFWORD_RGB16          X_RFLONG_RGB24          X_1P_1DAC1_WFBYTE
X_2P_2DAC1_WFBYTE       X_4P_4DAC1_WFBYTE       X_32P_4DAC8_WFLONG
X_1ADC8_0P_1DAC8_WFBYTE X_DDS_GOERTZEL_SINC1    X_DDS_GOERTZEL_SINC2
```

## Control Symbols

```
X_PINS_OFF    X_PINS_ON     X_WRITE_OFF   X_WRITE_ON
X_ALT_OFF     X_ALT_ON
```

## DAC Symbols

```
X_DACS_OFF      X_DACS_0_0_0_0    X_DACS_X_X_0_0    X_DACS_0_0_X_X
X_DACS_X_X_X_0  X_DACS_X_X_0_X    X_DACS_X_0_X_X    X_DACS_0_X_X_X
X_DACS_0N0_0N0  X_DACS_X_X_0N0    X_DACS_0N0_X_X    X_DACS_1_0_1_0
X_DACS_X_X_1_0  X_DACS_1_0_X_X    X_DACS_1N1_0N0    X_DACS_3_2_1_0
```

# Appendix C: Frequency Calculation Tables

## NCO Frequency Values

**Formula:** `frequency = $8000_0000 × (rate / clock)`

| Rate Ratio | Value | Notes |
|------------|-------|-------|
| 1:1 | `$8000_0000` | Every clock |
| 1:2 | `$4000_0000` | Half clock |
| 1:3 | `$2AAA_AAAB` | Add 1 for fractional |
| 1:4 | `$2000_0000` | Quarter clock |
| 1:5 | `$1999_999A` | Add 1 |
| 1:8 | `$1000_0000` | Eighth clock |
| 1:10 | `$0CCC_CCCD` | Tenth clock |
| 1:16 | `$0800_0000` | Sixteenth clock |

## Common Video Pixel Rates

| Resolution | Pixel Rate | At 250 MHz | At 300 MHz | At 320 MHz |
|------------|------------|------------|------------|------------|
| 640×480 | 25.175 MHz | `$0CE3_BCD3` | `$0ABD_C805` | `$0A11_EB85` |
| 800×600 | 40.000 MHz | `$147A_E148` | `$1111_1111` | `$1000_0000` |
| 1024×768 | 65.000 MHz | `$2147_AE14` | `$1BBB_BBBC` | `$1A00_0000` |
| 1280×720 | 74.250 MHz | `$2604_1893` | `$1FAE_147B` | `$1DB3_3333` |

Values are `round($8000_0000 × pixel_rate / clock_frequency)`.

# Appendix D: Troubleshooting Guide

## Symptom: No Output on Pins

**Check:**
1. D[23] = 1 (`X_PINS_ON` included in mode)
2. Pin group %ppp selects correct pins
3. Sub-pin selection matches target pins
4. Pins configured as outputs (DRVH/DRVL as needed)

## Symptom: Corrupted Data from RDFAST

**Check:**
1. **RDFAST** executed before streamer command
2. Buffer address aligned to 64-byte boundary for wrap mode
3. Buffer size matches FIFO configuration
4. No other code reading from FIFO simultaneously

## Symptom: Streamer Stops Unexpectedly

**Check:**
1. Count field D[15:0] not zero
2. Command buffer has pending command (**XCONT**/**XZERO** issued)
3. No **XINIT #0,#0** executed

## Symptom: Phase Drift in Video

**Check:**
1. Use **XZERO** at line boundaries
2. NCO frequency matches pixel rate exactly
3. Total pixels per line equals timing specification

## Symptom: DAC Output Incorrect

**Check:**
1. %dddd field selects correct routing
2. DAC channel matches pin LSBs
3. Pin configured for DAC mode

## Symptom: Goertzel Results Invalid

**Check:**
1. LUT contains signed sine/cosine values
2. ADC pin configured for ADC mode
3. Sample count adequate for frequency resolution
4. SINC2 amplitude reduced to prevent overflow

# Index

```{=latex}
\indexletter{A}
```

- ADC sampling modes: Chapter 9
- Alternate bit order: 12.4
- Architecture: Chapter 2

```{=latex}
\indexletter{B}
```

- Block diagram: 2.1

```{=latex}
\indexletter{C}
```

- Colorspace converter: 15.2, 15.3
- Command structure: Chapter 4
- Count field: 4.6

```{=latex}
\indexletter{D}
```

- DAC channels: Chapter 11
- DAC pin mapping: 11.2
- DAC routing table: 11.1
- DAC symbols: 13.3
- DDS mode: Chapter 10
- Double buffering: 18.1

```{=latex}
\indexletter{E}
```

- Enable control: 12.3
- Events: Chapter 14

```{=latex}
\indexletter{F}
```

- Frequency calculation: 3.2, Appendix C

```{=latex}
\indexletter{G}
```

- GETXACC: 4.7, 10.5
- Goertzel mode: Chapter 10

```{=latex}
\indexletter{H}
```

- HDMI output: 15.2
- Hub FIFO: 6.1

```{=latex}
\indexletter{I}
```

- Immediate modes: Chapter 5

```{=latex}
\indexletter{L}
```

- LUT setup: 5.1, 10.3

```{=latex}
\indexletter{M}
```

- Mode encoding table: Appendix A
- Mode field: 4.2
- Mode symbols: 13.1
- Multi-COG: 18.2

```{=latex}
\indexletter{N}
```

- NCO: Chapter 3

```{=latex}
\indexletter{P}
```

- Pin group selection: 12.1
- Pin selection: Chapter 12

```{=latex}
\indexletter{R}
```

- RDFAST modes: Chapter 6
- RGB modes: Chapter 7

```{=latex}
\indexletter{S}
```

- SETXFRQ: 3.3, 4.7
- Signal processing: Chapter 17
- SINC1/SINC2: 10.4
- Smart pin coordination: 18.3
- SPI: Chapter 16
- Sub-pin selection: 12.2
- Symbol composition: 13.4
- Symbols quick reference: Appendix B

```{=latex}
\indexletter{T}
```

- Troubleshooting: Appendix D

```{=latex}
\indexletter{V}
```

- VGA output: 15.1
- Video output: Chapter 15

```{=latex}
\indexletter{W}
```

- WAITXFI: 14.2
- WRFAST modes: Chapter 8

```{=latex}
\indexletter{X}
```

- XCONT: 4.7
- XINIT: 4.7
- XSTOP: 4.7
- XZERO: 4.7
