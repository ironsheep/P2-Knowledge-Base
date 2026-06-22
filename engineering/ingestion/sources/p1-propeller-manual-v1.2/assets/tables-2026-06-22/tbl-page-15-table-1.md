|    | 0                           | 1         | 2                                                                             |
|---:|:----------------------------|:----------|:------------------------------------------------------------------------------|
|  0 | Table 1-1: Pin Descriptions |           |                                                                               |
|  1 | Pin Name                    | Direction | Description                                                                   |
|  2 | P0 – P31                    | I/O       | General purpose I/O Port A.  Can source/sink 40 mA each at 3.3 VDC.           |
|    |                             |           | Logic threshold is ≈ ½ VDD; 1.65 VDC @ 3.3 VDC.                               |
|    |                             |           |   T                                                                           |
|    |                             |           | he pins shown below have a special purpose upon power-up/reset but are        |
|    |                             |           | general purpose I/O afterwards.                                               |
|    |                             |           | P28  - I2C SCL connection to optional, external EEPROM.                       |
|    |                             |           | P29  - I2C SDA connection to optional, external EEPROM.                       |
|    |                             |           | P30  - Serial Tx to host.                                                     |
|    |                             |           | P31  - Serial Rx from host.                                                   |
|  3 | VDD                         | ---       | 3.3 volt power (2.7 – 3.3 VDC).                                               |
|  4 | VSS                         | ---       | Ground.                                                                       |
|  5 | BOEn                        | I         | Brown Out Enable (active low).  Must be connected to either VDD or VSS.       |
|    |                             |           | If low, RESn becomes a weak output (delivering VDD through 5 KΩ) for          |
|    |                             |           | monitoring purposes but can still be driven low to cause reset.  If high,     |
|    |                             |           | RESn is CMOS input with Schmitt Trigger.                                      |
|  6 | RESn                        | I/O       | Reset (active low).  When low, resets the Propeller chip: all cogs disabled   |
|    |                             |           | and I/O pins floating.  Propeller restarts 50 ms after RESn transitions from  |
|    |                             |           | low to high.                                                                  |
|  7 | XI                          | I         | Crystal Input.  Can be connected to output of crystal/oscillator pack (with   |
|    |                             |           | XO left disconnected), or to one leg of crystal (with XO connected to other   |
|    |                             |           | leg of crystal or resonator) depending on CLK Register settings.  No          |
|    |                             |           | external resistors or capacitors are required.                                |
|  8 | XO                          | O         | Crystal Output.  Provides feedback for an external crystal, or may be left    |
|    |                             |           | disconnected depending on CLK Register settings.  No external resistors       |
|    |                             |           | or capacitors are required.                                                   |