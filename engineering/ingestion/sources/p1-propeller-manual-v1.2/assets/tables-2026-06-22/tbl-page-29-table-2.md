|    | 0                                      | 1                                                                                          |
|---:|:---------------------------------------|:-------------------------------------------------------------------------------------------|
|  0 | Table 1-8: CLK Register OSCENA (Bit 5) |                                                                                            |
|  1 | Bit                                    | Effect                                                                                     |
|  2 | 0                                      | Disables the Crystal Oscillator circuit.  The RCFAST and RCSLOW settings of the            |
|    |                                        | _CLKMODE declaration configure OSCENA this way.                                            |
|  3 | 1                                      | Enables the Crystal Oscillator circuit so that a clock signal can be input to XIN, or so   |
|    |                                        | that XIN and XOUT can function together as a feedback oscillator. The XINPUT and           |
|    |                                        | XTALx settings of the _CLKMODE declaration configure OSCENA this way. The OSCMx            |
|    |                                        | bits select the operating mode of the Crystal Oscillator circuit. Note that no external    |
|    |                                        | resistors or capacitors are required for crystals and resonators. Allow a crystal or       |
|    |                                        | resonator 10 ms to stabilize before switching to a Crystal Oscillator or Clock PLL output  |
|    |                                        | via the CLKSELx bits. When enabling the Crystal Oscillator circuit, the Clock PLL may      |
|    |                                        | be enabled at the same time so that they can share the stabilization period.               |