|    | 0                                     | 1                                                                                   |
|---:|:--------------------------------------|:------------------------------------------------------------------------------------|
|  0 | Table 1-6: CLK Register RESET (Bit 7) |                                                                                     |
|  1 | Bit                                   | Effect                                                                              |
|  2 | 0                                     | Always write ‘0’ here unless you intend to reset the chip.                          |
|  3 | 1                                     | Same as a hardware reset – reboots the chip.  The Spin command REBOOT writes a ‘1’  |
|    |                                       | to the RESET bit.                                                                   |