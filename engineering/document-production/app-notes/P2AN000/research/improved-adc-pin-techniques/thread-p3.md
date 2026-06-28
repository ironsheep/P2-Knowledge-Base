# Improved ADC Pin Techniques — Parallax Forum Thread (Page 3 of 4)

**Source:** https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques/p3
**Captured:** 2026-06-27 via WebFetch (verbatim post-by-post). Requote chains compressed.
**Attachments saved locally** under `code/`:
- `P2_ADC_Schematic.pdf` (88.5K, evanh, Post 1) — the actual P2 ADC front-end schematic
- `ThreePinADC_SampleFiltering-4.9K.spin2` (Post 4) — N-stage time-halving filter
- `ThreePinADC_SampleFiltering-8K.spin2` (Post 15, requires PNut_v43) — Chip's working file w/ idea comments
- `EightPinADC.spin2` (10.2K, Post 17) — **8 ADC pins via PASM2 bytecode interpreter**
- `trapezoid-adc/` (Post 21, SaucySoliton) — trapezoid-window SINC3 double-integration approach

---

## Post 1 — evanh — 2023-12-04 16:38 (edited 16:50)
> @"Christof Eb." said: What is the size of these capacitors "C"? ... together with R=450k gives ... how long you have to wait after switching the input?

Full circuit is attached, but not that simple sorry. Far above my skill level, real ADC hardware uses a current balancing circuit in between the front end resistors and the modulated capacitor. Here's the capacitor pair. I can make out 10 x 10 = 100 um gate area on each. 3.3 Volt transistor means a thicker dielectric I guess. No idea what Wtot means.

[Image of capacitor pair schematic]
**Attachment:** P2_ADC_Schematic.pdf (88.5K) → `code/P2_ADC_Schematic.pdf`

## Post 2 — Christof Eb. — 2023-12-05 10:55
Thank you, evanh!

@cgracey what absolute value in mV do you get, when you connect a pin directly to GND with you new method? I did some measurements and had the impression, that not noise but the absolute error is the bigger problem?

## Post 3 — cgracey — 2023-12-05 11:16 (edited 11:38)
Yes, the absolute errors at GND and VIO are the biggest problems. I should have designed the ADC differently, so that the same high-z resistor was used for GIO, VIO, and pin measurement. Instead, I have three separate matched resistors that differ more than I thought they would. So, I've seen pins that are as much as 15mV off. The only way to overcome that error is if you are able to drive the pin low (which can be done when using the ADC) and overcome the analog input signal, forcing the pin very close to GND and then measuring it. Same could be done for VIO by driving it high.

To answer the cap question, the 3p3v gate capacitors have a capacitance of 4.4 fF / um2. So, for eight (m=8) 10um x 10um gate caps, that's 3520 fF (4.4 fF * 8 * 10 * 10). Because we have both PMOS and NMOS cap sets for power supply noise rejection, double that to get 7040 fF or about 7 pF. That's not much, but consider that the circuit was designed to run at 200 MHz.

## Post 4 — cgracey — 2023-12-05 12:33 (edited 13:05)
I found a way to make a time-halving, resolution-doubling N-stage filter that takes almost no memory and a constant amount of time to operate. It outputs 17 stages of samples, from the raw base sample to the average of 64K samples.

Here are WHEN the stages are computed for up to stage 7, but the stages could be infinitely higher:

```
00000000000000000000000000000000000000000000000000000000000000000
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
  2   2   2   2   2   2   2   2   2   2   2   2   2   2   2   2  
    3       3       3       3       3       3       3       3    
        4               4               4               4        
                5                               5                
                                6                                
                                                                7
```

Stage 0 is the ADC sample that is generated each period.
Stage 1 is the sum of two Stage 0 samples. It is generated every second period.
Stage 2 is the sum of two Stage 1 samples. It is generated every fourth period.
Stage 3 is the sum of two Stage 2 samples. It is generated every eighth period.
etc.

I found a way to pick which stage needs to be computed each period by reversing the bits in an incrementing counter, taking the magnitude via ENCOD, then subtracting it from 32.

Each time a stage executes, it outputs a sample by right-shifting its stored value by its stage number.

The idea is that you don't need to specify a sample rate and quality. You just pick the sample stream that gives the best tradeoff between rate and resolution. The ADC is running full speed all the time, generating fast low-res samples.

Here is the code for it, along with the ADC and DAC generator for testing.
**Attachment:** ThreePinADC_SampleFiltering.spin2 (4.9K) → `code/ThreePinADC_SampleFiltering-4.9K.spin2`

## Post 5 — Rayman — 2023-12-05 16:34
[re Christof's circuit diagram]

This drawing is helpful to understand how it works...

I see it as a current measuring circuit... There is a current coming into to ADC from the voltage applied to the pin, through one of for resistors. Then, there is current coming from the digital circuit through the 300 kOhm resistor. The digital circuit works to cancel out the input current with it's output current to maintain VIO/2 voltage where they meet.

I think the first of those four buffers in series is more like a voltage comparator than a buffer. Giving 0 if above VIO/2 and 1 if below VIO/2...

So, if one wanted to measure a much higher voltage, could just add an extra series resistor between voltage to be measured and pin. As long as that resistance was bigger than say, 10k, the protection diodes should keep chip save when ADC is off... But, probably need to look into spec for how much current protection diodes can take to be sure it's OK...

## Post 6 — evanh — 2023-12-06 00:26 (edited 00:28)
> @Rayman said: ... add an extra series resistor between voltage to be measured and pin.

Totally, it's a good solution. Maybe throw in a high frequency capacitor from the pin to GIO to absorb spikes.

The ADC electrically centres on VIO/2 so you have to accept that there is an offset. But it's a fixed value voltage and at large voltage ranges the lopsided current becomes insignificant.

## Post 7 — jmg — 2023-12-06 20:48
> @Rayman said: ... add an extra series resistor between voltage to be measured and pin.

On paper, yes. In practice the on chip resistors have a tempco that should be matched by that external R.

## Post 8 — evanh — 2023-12-06 23:08 (edited 23:17)
Could use the x100 setting for a smaller internal resistor so that the external resistor completely dominates. With internal 5 kOhm, a 50 MOhm to handle up to 500 Volts peak would make any small difference in the coefficients well below noise floor.

PS: That functional drawing was made years before Chip released the full schematic. The 4k5R to 450kR was a pure guess on my part originally. The real x1 resistors are over 500 kOhms.

## Post 9 — cgracey — 2023-12-06 23:22
The pin will bias itself somewhere around VIO/2, but not exactly at VIO/2. So, the amplified modes (ie 100x) need to be allowed to go to their center voltage, because the full range may be as little as 50mV peak-peak around that center voltage. You would want a huge series resistor (megohms) in that case. For AC signals, just a series capacitor is sufficient, since it will allow the DC to settle where it wants, but will convey voltage changes.

## Post 10 — evanh — 2023-12-06 23:40
Oops, you reminded me, 50 MOhm makes 500 V peak-peak, so only 250 V peak.

## Post 11 — evanh — 2023-12-06 23:59 (edited 00:01)
[anecdote about cleaning a high-voltage vacuum valve in a plastic-welding machine — off-topic]

## Post 12 — rogloh — 2023-12-11 01:49
> @cgracey said: [N-stage time-halving filter]

If you can dedicate a COG this seems a rather useful way to generate clean/filtered analog results at whatever sample rate you need. I've not messed about with ADCs and DACs on the P2 as yet so having something like this is pretty handy.

With 6 IO pins needed it might be good to build a 2 channel ADC P2 breakout board that leverages this concept. You could put a voltage reference on it for calibration, and you might be able to use the two spare pins in an 8 bit group with an i2c expander to control an analog input mux or FETs to switch in series resistors and capacitors for voltage range extending or AC coupling or to select the voltage reference. Or to keep it simpler, maybe these 2 spare IO pins could just be 2 DAC channel outputs. This could then become a simple 2 channel analog IO P2 breakout with a nominal 0-3.3V voltage range that also has the extra headroom to detect under/over voltage conditions. Might be good to add some bulkier input protection in that case to help protect P2 inputs.

## Post 13 — cgracey — 2023-12-11 17:38
> @rogloh said: [dedicate a COG / breakout board]

A board like that would be nice.

I started breaking apart the sections of code needed to perform each step of the ADC conversion, in order to make a configurable system that could handle any number of ADCs. When I started putting the state code around it, it got really ugly. Then I had a realization that there was a better way to do it. I could make a bytecode interpreter that could contain all the needed code, kind of like the Spin2 interpreter. Then, rather than put all this stateful code around the core ADC code sections, I could just call them out via bytecodes with very little memory and execution overhead. Plus, configuration becomes super flexible this way.

## Post 14 — Christof Eb. — 2023-12-12 12:19
> @cgracey said: [bytecode interpreter idea]
Sounds like doing it with Forth....

## Post 15 — cgracey — 2023-12-14 00:54 (edited 00:55)
Here is my current working file on ADC stuff with a bunch of ideas in comments. Martin Montague on the Propeller Live Forum today wanted me to post this. It requires PNut_v43 to run.
**Attachment:** ThreePinADC_SampleFiltering.spin2 (8K) → `code/ThreePinADC_SampleFiltering-8K.spin2`

## Post 16 — RS_Jim — 2023-12-28 00:23 (edited 11:41)
@cgracey chip, Can the single Pin version be modified to run two adc channels at the same time or should it be run in two cogs? Jim

## Post 17 — cgracey — 2024-01-17 20:59
Eight ADC pins at once with bytecode interpreter.
**Attachment:** EightPinADC.spin2 (10.2K) → `code/EightPinADC.spin2`

## Post 18 — Rayman — 2024-01-18 16:41
@cgracey Is there supposed to be a plot in the scope window? Mine is blank. Just see what looks like text values for the ADCs in the regular debug window....

## Post 19 — cgracey — 2024-01-20 05:14
Ah, I think it's because you'll need the latest version of PNut and I'm not sure if it's in PropellerTool, yet. I added an auto-scale function to the SCOPE mode that will confuse older versions of DEBUG.

## Post 20 — SaucySoliton — 2024-03-23 06:20
I've been looking into this code to try to read a current shunt. It looks like with <100uVpp noise that would be 2mA on a 0.05 Ohm shunt. That would be excellent. What is not so good is the 2000-5000 uV offset.

So, I've added an external multiplexer. (Single Pole Double Throw. Maybe SN74LVC1G3157 or equivelent.) The plan was to connect the analog input to 1 of 2 analog pins. Instead of using the ADC Gio/Vio mode, I measure the pin all the time and drive the pin to Gio/Vio by making it an output. I'm only using the readings from 1 pin right now and had about -1000uV of offset.

I measured about 300uV between a ground hole on the Edge module and a ground hole on the breadboard. The current draw was ~80mA. So a resistance of 4 miliOhms could cause that voltage drop. Not that bad. I suppose the bond wires could have a 600uV drop.

We might be able to solve some issues with differential measurement. I've done that to measure +-400V on both P1 and P2 with good accuracy. A 4:1 multiplexer would allow selection of positive and negative references and positive and negative signal values. It would be nice to not need external parts, but multiplexers are usually pretty cheap when compared to high performance ADCs.

## Post 21 — SaucySoliton — 2024-04-04 21:20
ADC development has gone full circle. Here is the superthread where Chip discovered that tapering the edges of the ADC sampling window significantly improved the quality. https://forums.parallax.com/discussion/169298/adc-sampling-breakthrough/p1 Later, we discovered that a triangular window aka SINC2 would perform even better.

Recently I have been working on a sensorless BLDC motor driver. There is a project showing how to build one of those using Arduino. It uses 3 resistors to simulate a motor ground connection. This voltage is compared to one of the phases to determine commutation. I would rather not need to add the virtual ground resistors to the P2 Universal Motor Driver board. I could use the ADCs to measure the voltages on each pin. The slight problem is the PWM on the motor power. I haven't tested the triangular SINC2 window on a PWM signal yet. But I don't think it would work well. I would expect significant variation depending on the alignment between the PWM signal and the sampling window. I could use P_COUNT_HIGHS to measure the ADC. That should average out the PWM very well if the sample window matches the PWM interval. However, as discovered years ago, sample windows with smooth edges work better.

So I would expect a trapezoid window function to work better than rectangular while also filtering the PWM away. How to generate such a thing efficiently? Summing together overlapping SINC2 samples would work. (This is what I think Chip's code in this thread does.) That creates a trade-off. I want a relatively short ramp up and down on the sides so I can measure the average voltage of a PWM signal. But that would require a higher sampling rate and a lot of clock cycles to add all those samples together at the top of the trapezoid. Not ideal. Based on my simulations and intuition, I think that the samples in the middle of the trapezoid cancel each other out of the calculations. So it is only necessary to acquire 2 samples at the beginning and 2 at the end.

One last hurdle. The P2 smart pin does one of the differentiations in hardware. Normally that is great because it saves 2 instructions and some memory. To make the trapezoidal sampling work, I needed a continuous double integration of the ADC bitstream. I set it to a 1 clock sampling interval to get the pin to update every clock. Then the pin must be set to SINC3 mode. The first integrator is continually reset, so the data is double integrated.

[Image showing waveform diagram]

There are a few neat things that can be done with this new technique.
1. Multiple cogs can read the same ADC, even at different sample rates and without any concern about sample overlap.
2. The sampling window can start and stop at any time. The multiplexer settling time, window ramp up, and window top are all independent now.
3. By taking many more samples during the ramp up and ramp down phases we can create a big Tukey window.

The proof of concept code attached seems to perform similarly to Chip's code when using 1 pin. The only metric I looked at as peak to peak noise.
**Attachment:** trapezoid-adc.zip (21.9K) → `code/trapezoid-adc/` (extracted: trapadc3.spin2, multiratesinc2b.m, sinc2trapezoid.png, jm_fullduplexserial.spin2, jm_nstr.spin2)

## Post 22 — ManAtWork — 2024-04-05 07:30
[BLDC motor discussion — star-point voltage can be calculated from PWM duty cycles; floating phase used for rotor position]

## Post 23 — SaucySoliton — 2024-04-05 19:04
[confirms floating-leg detection; following simple-circuit.com Arduino sensorless ESC design]

## Posts 24–30 — ErNa / evanh / SaucySoliton / Electrodude — 2024-04-05..07
[BLDC vs PMSM motor theory discussion; QROTATE tricks for 3-phase generation; trapezoidal vs sinusoidal commutation. Tangential to ADC — motor-control domain. SaucySoliton: generate 3-phase with only 2 QROTATEs by exploiting sine symmetry; the non-min/non-max phase left floating for back-EMF sensing.]

---

*End of Page 3 capture. (Pages 3–4 drift into BLDC motor-control theory, off the ADC core.)*
