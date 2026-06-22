|    | 0                                        |   1 | 2          | 3          | 4               | 5                              |
|---:|:-----------------------------------------|----:|:-----------|:-----------|:----------------|:-------------------------------|
|  0 | Table 1-9: CLK Register OSCMx (Bits 4:3) |     |            |            |                 |                                |
|  1 | OSCMx                                    |     | _CLKMODE   | XOUT       | XIN/XOUT        | Frequency Range                |
|    |                                          |     | Setting    | Resistance | Capacitance     |                                |
|  2 | 1                                        |   0 |            |            |                 |                                |
|  3 | 0                                        |   0 | XINPUT     | Infinite   | 6 pF (pad only) | DC to 80 MHz Input             |
|  4 | 0                                        |   1 | XTAL1      | 2000 Ω     | 36 pF           | 4 to 16 MHz Crystal/Resonator  |
|  5 | 1                                        |   0 | XTAL2      | 1000 Ω     | 26 pF           | 8 to 32 MHz Crystal/Resonator  |
|  6 | 1                                        |   1 | XTAL3      | 500 Ω      | 16 pF           | 20 to 60 MHz Crystal/Resonator |