# Appendix B: Packed Data Format Reference

*Complete specifications for all packed data formats, compression ratios, performance characteristics, and selection guidelines.*

## Format Specifications

### PACK1 - Binary Format
- **Bits per sample**: 1
- **Range**: 0-1 
- **Compression ratio**: 32:1
- **Samples per long**: 32
- **Best for**: Digital signals, GPIO states, binary sensors
- **Bandwidth at 1MHz**: 31.25 KB/s

### PACK2 - 2-Bit Format  
- **Bits per sample**: 2
- **Range**: 0-3
- **Compression ratio**: 16:1
- **Samples per long**: 16
- **Best for**: Quaternary states, I2C (SDA/SCL), quadrature
- **Bandwidth at 1MHz**: 62.5 KB/s

### PACK4 - Nibble Format
- **Bits per sample**: 4
- **Range**: 0-15
- **Compression ratio**: 8:1
- **Samples per long**: 8
- **Best for**: Hex digits, BCD, 16-level ADC
- **Bandwidth at 1MHz**: 125 KB/s

### PACK8 - Byte Format
- **Bits per sample**: 8
- **Range**: 0-255 (unsigned) or -128 to 127 (signed)
- **Compression ratio**: 4:1
- **Samples per long**: 4
- **Best for**: 8-bit ADC, audio samples, serial data
- **Bandwidth at 1MHz**: 250 KB/s

### PACK16 - Word Format
- **Bits per sample**: 16
- **Range**: 0-65535 (unsigned) or -32768 to 32767 (signed)
- **Compression ratio**: 2:1
- **Samples per long**: 2
- **Best for**: 16-bit ADC, precision measurements, audio
- **Bandwidth at 1MHz**: 500 KB/s

### PACK32 - Long Format
- **Bits per sample**: 32
- **Range**: Full 32-bit
- **Compression ratio**: 1:1 (no compression)
- **Samples per long**: 1
- **Best for**: Full precision, floating point, timestamps
- **Bandwidth at 1MHz**: 1 MB/s

## Packing Algorithms

### Bit Packing (PACK1)
```spin2
' Pack 32 bits into one long
packed := 0
repeat bit from 0 to 31
  if samples[bit]
    packed |= (1 << bit)
```

### Multi-bit Packing
```spin2
' PACK4 example - 8 nibbles per long
packed := 0
repeat nibble from 0 to 7
  packed |= (samples[nibble] & $F) << (nibble * 4)
```

## Performance Comparison Table

| Format | Compression | Max Sample Rate @ 2Mbaud | Latency | CPU Usage |
|--------|------------|---------------------------|---------|-----------|
| Text   | 0.14×      | 4 kHz                    | High    | Very High |
| PACK1  | 32×        | 2 MHz                    | Low     | Low       |
| PACK2  | 16×        | 1 MHz                    | Low     | Low       |
| PACK4  | 8×         | 500 kHz                  | Low     | Low       |
| PACK8  | 4×         | 250 kHz                  | Low     | Medium    |
| PACK16 | 2×         | 125 kHz                  | Low     | Medium    |
| PACK32 | 1×         | 62.5 kHz                 | Low     | High      |

## Selection Guidelines

### Decision Tree
1. **Is data binary?** → Use PACK1
2. **Is data ≤ 4 states?** → Use PACK2
3. **Is data ≤ 16 levels?** → Use PACK4
4. **Is data ≤ 256 levels?** → Use PACK8
5. **Need full precision?** → Use PACK16 or PACK32
6. **Bandwidth critical?** → Use smallest format that fits

## Advanced Compression

### Delta Encoding
```spin2
' Send differences instead of absolute values
delta[0] := samples[0]  ' First sample absolute
repeat i from 1 to count-1
  delta[i] := samples[i] - samples[i-1]
' Most deltas fit in PACK8 even if samples are PACK16
```

### Run-Length Encoding
```spin2
' Compress repeated values
value := samples[0]
count := 1
repeat i from 1 to n-1
  if samples[i] == value
    count++
  else
    ' Send count and value
    send_rle(count, value)
    value := samples[i]
    count := 1
```

## Format Conversion

### Unpacking Data
```spin2
' Unpack PACK4 data
repeat nibble from 0 to 7
  samples[nibble] := (packed >> (nibble * 4)) & $F
```

### Format Upgrading
```spin2
' Convert PACK8 to PACK16 with sign extension
word_value := byte_value
if word_value & $80  ' Negative?
  word_value |= $FF00  ' Sign extend
```

## Bandwidth Calculations

### Formula
```
Bandwidth (bytes/sec) = Sample_Rate × Bits_Per_Sample / 8
```

### Examples
- 1MHz sampling, PACK1: 1,000,000 × 1 / 8 = 125 KB/s
- 100kHz sampling, PACK16: 100,000 × 16 / 8 = 200 KB/s
- 44.1kHz audio, PACK16: 44,100 × 16 / 8 = 88.2 KB/s

## Memory Requirements

### Buffer Sizing
```spin2
' Calculate buffer size needed
samples_needed := sample_rate * capture_time
longs_needed := (samples_needed * bits_per_sample + 31) / 32
bytes_needed := longs_needed * 4
```

## Common Use Cases

### Digital Logic Analysis
- **Format**: PACK1 or PACK2
- **Typical rate**: 1-10 MHz
- **Buffer**: 1-16 KB

### Analog Waveforms
- **Format**: PACK16
- **Typical rate**: 10-100 kHz
- **Buffer**: 4-32 KB

### Audio Processing
- **Format**: PACK16
- **Typical rate**: 44.1 kHz
- **Buffer**: 8-64 KB

### Sensor Data
- **Format**: PACK8 or PACK16
- **Typical rate**: 100 Hz - 10 kHz
- **Buffer**: 1-8 KB

## Error Handling

### Buffer Overflow Prevention
```spin2
if (write_ptr + samples) > buffer_size
  ' Handle overflow
  samples_to_write := buffer_size - write_ptr
  overflow_samples := samples - samples_to_write
```

### Data Validation
```spin2
' Check packed data integrity
checksum := 0
repeat i from 0 to packed_longs-1
  checksum ^= packed_data[i]
```

This reference provides complete specifications for optimizing data transmission through packed formats.