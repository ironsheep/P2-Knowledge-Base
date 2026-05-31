# Appendix B: Packed-Data Format Reference

Packed-data modes let one `DEBUG` call carry many small samples, multiplying the
throughput of the debug link. You name a packing mode in a window's feed, then send
packed longs/words/bytes; the window unpacks them. See Chapter 13 for usage.

## The twelve formats

| Keyword | Container | Values per container | Compression |
|---------|-----------|----------------------|-------------|
| `LONGS_1BIT` | long | 32 | 32× |
| `LONGS_2BIT` | long | 16 | 16× |
| `LONGS_4BIT` | long | 8 | 8× |
| `LONGS_8BIT` | long | 4 | 4× |
| `LONGS_16BIT` | long | 2 | 2× |
| `WORDS_1BIT` | word | 16 | 16× |
| `WORDS_2BIT` | word | 8 | 8× |
| `WORDS_4BIT` | word | 4 | 4× |
| `WORDS_8BIT` | word | 2 | 2× |
| `BYTES_1BIT` | byte | 8 | 8× |
| `BYTES_2BIT` | byte | 4 | 4× |
| `BYTES_4BIT` | byte | 2 | 2× |

Maximum compression is **32×** (`LONGS_1BIT`). Fields are extracted LSB-first.

## Modifiers

- `SIGNED` — sign-extend each field instead of treating it as unsigned. Signed
  ranges: 1-bit −1…0, 2-bit −2…1, 4-bit −8…7, 8-bit −128…127, 16-bit −32768…32767.
- `ALT` — reverse the sub-field order within each container.

Syntax: `<packing-mode> {ALT} {SIGNED}`.

## Choosing a format

Match the field width to your data's range: a single digital line packs at
`LONGS_1BIT` (32×); an 8-bit sample at `LONGS_8BIT` (4×) or `BYTES_*`. Windows that
accept packed data include BITMAP, LOGIC, SCOPE, SCOPE_XY, FFT, and SPECTRO.
