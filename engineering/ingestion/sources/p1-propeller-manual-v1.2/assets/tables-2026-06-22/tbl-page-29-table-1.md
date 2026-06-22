|    | 0                                      | 1                                                                                       |
|---:|:---------------------------------------|:----------------------------------------------------------------------------------------|
|  0 | Table 1-7: CLK Register PLLENA (Bit 6) |                                                                                         |
|  1 | Bit                                    | Effect                                                                                  |
|  2 | 0                                      | Disables the PLL circuit.  The RCFAST and RCSLOW settings of the _CLKMODE declaration   |
|    |                                        | configure PLLENA this way.                                                              |
|  3 | 1                                      | Enables the PLL circuit. Each of the PLLxx settings of the _CLKMODE declaration         |
|    |                                        | configures PLLENA this way at compile time. The Clock PLL internally multiplies the     |
|    |                                        | XIN pin frequency by 16. OSCENA must also be ‘1’ to propagate the XIN signal to the     |
|    |                                        | Clock PLL. The Clock PLL's internal frequency must be kept within 64 MHz to 128 MHz     |
|    |                                        | – this translates to an XIN frequency range of 4 MHz to 8 MHz. Allow 100 µs for the     |
|    |                                        | Clock PLL to stabilize before switching to one of its outputs via the CLKSELx bits.     |
|    |                                        | Once the Crystal Oscillator and Clock PLL circuits are enabled and stabilized, you can  |
|    |                                        | switch freely among all clock sources by changing the CLKSELx bits.                     |