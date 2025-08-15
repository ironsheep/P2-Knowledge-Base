# P2 Silicon Documentation v35 - DOCX Extraction

Parallax Propeller 2
Documentation
2021-05-18
v35 (Rev B/C silicon)
## P2X8C4M64PES
LPD1941 (Rev B) or LHU2019 (Rev C)
## PHILIPPINES
(not yet updated: Boot ROM)
### Design Status
Date
Progress
2018_04_25
Verilog design files sent to On Semi for Rev A silicon
(8 cogs, 512KB hub, 64 smart pins)
2018_05_29
Final ROM data sent to On Semi
2018_07_09
Final Sign-off with On Semi, reticles being made
2018_09_11
Wafers done! Only took 9 weeks, instead of 14.
2018_09_27
Received 10 glob-top prototype chips from On Semi.
Chips are functional, but sign-extension problems in Verilog source files caused the following problems:
Cogs' IQ modulators' outputs are nonsensical.
Smart pin measurement modes which are supposed to count by +1/-1 are counting by +1/+3.
ALTx instructions aren't sign-extending S[17:09] before adding into D.
These sign-extension problems have already been fixed in the Verilog source files and tested on the FPGA.
There is also a low-glitch-on-high-to-float problem on some I/O pins due to a race condition between DIR and OUT signals. This will be fixed by timing constraints in the next silicon.
A respin of the silicon is planned after more testing.
2018_11_13
Received 135 Amkor-packaged prototype chips from On Semi. These chips will have better heat dissipation than the glob-top prototypes.
2019_04_11
Rev B respin entered the fab and is due out July 15.
Ten glob-top prototypes should arrive on August 1, with 2,400 production chips to follow in a few weeks.
The following improvements were made to the chip:
All known prior bugs fixed.
Clock-gating implemented, reduces power by ~40%.
PLL filter modified to reduce jitter and improve lock.
System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.
Streamer has many new modes with SINC1/SINC2 ADC conversions for Goertzel mode.
HDMI mode added to streamer with ascending and descending pinouts for easy PCB layout.
SINC2/SINC3 filters added to smart pins for improving ENOB in ADC conversions.
Each cog has four 8-bit sample-per-clock ADC channels that feed from new smart pin 'SCOPE' modes.
BITL/BITH/BITC/BITNC/BITZ/BITNZ/BITRND/BITNOT can now work on a span of bits (+S[9:5] bits). Prior SETQ overrides S[9:5].
DIRx/OUTx/FLTx/DRVx can now work on a span of pins (+D[10:6] pins). Prior SETQ overrides D[10:6].
WRPIN/WXPIN/WYPIN/AKPIN can now work on a span of pins (+S[10:6] pins). Prior SETQ overrides S[10:6].
BIT_DAC output now has two 4-bit settings for low and high states, instead of one 8-bit high-state setting.
RDxxxx/WRxxxx+PTRx expressions now index -16..+16 with updating and -32..+31 without updating.
Sensible PTRx behavior implemented for 'SETQ(2) + RDLONG/WRLONG/WMLONG' operations.
RDLUT/WRLUT can now handle PTRx expressions.
Cog LUT sharing is now glitch-free.
POP now returns Z=1 if result=0, used to return result[30].
XORO32 improved.
Main PRNG upgraded to "Xoroshiro128**".
The core logic increased by a net 15%, even with significant logic reductions resulting from clock-gating. Fortunately, ON Semi was able to make it all fit within the original die area.
2019_07_13
Wafers out of fab. Packaging underway.
2019_08_01
Received 10 glob-top prototype chips from ON Semi.
All bugs from prior silicon are fixed.
All new features work as expected.
PLL jitter is <2ns @100us at all divide/multiply settings.
Power is reduced by ~50%.
The new silicon works much better than expected with the improved PLL filter and new clock gating. At room temperature, the silicon runs at 390MHz and is barely warm to the touch, with the PLL now being the speed limiter, instead of the logic.
2019_08_19
One of the six new wafers exhibits frequent VIO-to-GND shorts in the 5-20 ohm range. ON Semi is looking into the cause.
We know that the design is good, so we are anxious to see ON Semi resume yield testing on the other wafers, in order to get as many Amkor-packaged parts as soon as possible. The new P2 Eval board is ready to be built.
2019_08_29
ON Semi has done failure analysis on the new chips which were exhibiting VIO shorts and it's been determined that there are latch-up problems originating from differently-biased N-wells that lie adjacent to each other. The relatively low resistivity of the new wafers caused this latent design defect to emerge.
We will need to modify the full-custom pad ring to fix these N-well problems. We will soon discuss with ON Semi how many reticles this is going to involve. We will need another fab run, as well, to realize the changes.
2019_09_13
ON Semi recently discovered that a voltage-stress test had been applied to the new silicon which was driving the VDD and VIO pins to +40% nominal voltages. The 4.62V on VIO was triggering the latch-up problem. The first two wafers which had been probed with this new test had developed many bad dies, as a result.
ON Semi probed six remaining virgin wafers without the voltage-stress test and yielded over 1,000 good dies. These have been sent off to Amkor for packaging. From these chips, we will be able to