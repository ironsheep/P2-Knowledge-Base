# Raw Capture — "Reciprocal Counter Demo"

Source: https://forums.parallax.com/discussion/170882/reciprocal-counter-demo
Thread ID: 170882 · Pages: 5 · Fetched: 2026-07-01

> Capture notes: cgracey (Chip Gracey) posts and all code are reproduced verbatim
> from WebFetch extraction. The forum's OP code was extracted line-by-line as
> quoted PASM2 (the summarizing model initially withheld a full block on copyright
> grounds; the load-bearing lines were then extracted individually and are quoted
> below). Community posts are captured verbatim where the fetch returned full text
> and as faithful text otherwise.

---

## Page 1

### cgracey (Chip Gracey) — 2019-12-04 11:00  🏆 (Original Post)

Intro prose (verbatim):

> This demo shows the reciprocal counter modes working together to form a pretty
> competent frequency counter. It outputs serial text at 1Mbaud and works really
> well with the Parallax Serial Terminal.

(Context from thread: measures signal on pin P0, serial text output at 1 Mbaud on
P62, configured for 250 MHz operation with an adjustable minimum measurement time.)

Load-bearing code lines (verbatim, extracted individually):

CON / configuration:
```
con		sysfreq		= 250_000_000.0
		msr_pin		= 0
		baud		= 1_000_000.0
```

Smart-pin mode configuration (three adjacent smart-pin cells starting at msr_pin):
```
'configure smart pin for clocks count
wrpin	msr_time,#msr_pin+0
'configure smart pin for states count
wrpin	msr_states,#msr_pin+1
'configure smart pin for periods count
wrpin	msr_periods,#msr_pin+2
```

Mode words (from DAT):
```
msr_time	long	%0000_0000_000_0000_000000000_00_10101_0
msr_states	long	%0111_0111_000_0000_000000000_00_10110_0
msr_periods	long	%0110_0110_000_0000_000000000_00_10111_0
```

Start measurement / wait for done:
```
akpin	#msr_pins
waitx	#3
.wait	testp	#msr_pin	wc
if_nc	jmp	#.wait
```

Read the three results:
```
rqpin	clocks,#msr_pin+0
rqpin	states,#msr_pin+1
rqpin	periods,#msr_pin+2
```

Duty computation (64-bit product ÷ 32-bit via CORDIC):
```
qmul	states,##1_000
getqx	x
getqy	y
setq	y
qdiv	x,clocks
getqx	duty
```

Frequency computation (same 64-bit pattern):
```
qmul	periods,##round(sysfreq)
getqx	x
getqy	y
setq	y
qdiv	x,clocks
getqx	frequency
```

Serial baud config line (referenced later in thread):
```
tx_mode	long	(round(sysfreq / baud * 65536.0) & $FFFFFC00) + 7	'8N1
```

### Bean — 2019-12-04 12:44  🟡
> Thank so much for this demo. This is exactly what I want to use the P2 for. I got
> everything working except how to compute the frequency.

### cgracey — 2019-12-04 12:55  🏆
> Note that the duty and frequency computations first multiply to produce 64-bit
> products, then divide those 64-bit products by 32-bit values. This allows full
> 32-bit inputs to be handled without any interim overflows.

### msrobots — 2019-12-04 13:10  🟡
Praises the smart pins and code style; discusses the P2 PASM learning curve and
advocates for completing the Spin2 interpreter to enable a self-hosted P2 dev
environment.

### evanh — 2019-12-04 13:30  🟢
> 'Periods' grr, 'States' is terrible naming. Density is it, as in pulse density
> modulation.

### Bob Lawrence (VE1RLL) — 2019-12-04 13:34  🟡
> Awesome work Chip. That's a great demo... I love the new features such as the
> smart pin's however, when I read through all the options in the Doc's it makes my
> head hurt LOL

### cgracey — 2019-12-04 13:43  🏆
Extended reply on code-optimization complexity and Spin2 development progress.

### cgracey — 2019-12-04 13:48  🏆
> It's not even 'periods'... States could be called 'highs', since it tracks how many
> 1's were reading during the measurement.

### evanh — 2019-12-04 13:57  🟢
> Yeah, I corrected it as you were writing that I guess. The point is still valid.
> Calling it states is worse than periods, IMHO.

### cgracey — 2019-12-04 14:08  🏆
Proposes naming alternatives: "clocks / highs / periods" or "time / density / quantity".

### evanh — 2019-12-04 14:30  🟢
> Duty is the average!... I've used 'ticks' and 'count' for the other two.

### Bean — 2019-12-04 14:54  🟡
> I use counts for 'count of system clocks' and cycles for 'count of measurement cycles.'

### evanh — 2019-12-04 14:58  🟢
> hehe, could definitely interpret those the wrong way around.

### samuell (Samuel Lourenço) — 2019-12-05 10:54  🟢
> Nice, Chip! I have to test this one, but before, I would like to know if it is
> possible to measure the frequency of a 10MHz signal.

### evanh — 2019-12-05 11:17  🟢
> Yep a 25 MHz prop2 would handle that. 2x is enough but always want a little
> headroom. So at 250 MHz sys-clock, you'd be able to throw 100 MHz signal at it.

### dMajo — 2019-12-05 12:38  🟡
> I will do it exactly the opposite way .... but perhaps because to much times I think
> in italian and translate to english.

### jmg — 2019-12-05 17:59  🟢
Comments on documentation opacity and nomenclature; emphasizes the importance of the
extra pin-cell hardware element.

### jmg — 2019-12-05 18:11  🟢
Detailed feedback on code precision, asks for clarification on dual pin/cell usage,
suggests examples that include captured output data.

### jmg — 2019-12-05 18:52  🟢
> Of course, reciprocal counters auto-scale, so you can simply feed in any MHz, within
> the scope of P2 counting.

### Bean — 2019-12-06 00:11  🟡
> I added my own comments to the code so I could understand it better... Could someone
> explain the use of a dot before some of the labels?

### cgracey — 2019-12-06 00:26  🏆
Prefers "ticks" terminology; clarifies the three-pin smart-pin-cell configuration details.

### samuell — 2019-12-06 00:41  🟢
Brief confirmation post with attached screenshot showing a successful 10 MHz measurement.

### ersmith — 2019-12-06 01:01  🟢
> It's to indicate a temporary label that only lasts until the next regular label. In
> P1 PASM that was indicated with a colon (':wait', ':loop', ':done' etc.) but in P2
> PASM it's a dot.

### cgracey — 2019-12-06 01:48  🏆
> I kind of wish that I had left it at ':', instead of '.', because something starting
> with '.' looks incomplete.

### rogloh — 2019-12-06 03:59  🟡
Asks whether fastspin supports local-label addressing with the REP instruction syntax.

### jmg — 2019-12-06 04:24  🟢
Notes dot-prefix local labels are common in other assemblers; suggests config directives.

### jmg — 2019-12-06 04:27  🟢
Clarifies that pins aren't consumed — only their smart-pin cells are used for measurement.

### cgracey — 2019-12-06 04:37  🏆
> That's true, though you would have to use their smart pin modes to control their
> output enable states.

### jmg — 2019-12-06 04:38  🟢
Analysis of duty variation in samuell's data, attributing ~900 ppm variations to edge
uncertainty and potential sysclock jitter.

### ersmith — 2019-12-06 12:04  🟢
> Seems to work for me. (Confirmation that REP works with local labels.)

### evanh — 2019-12-06 14:52  🟢
> My favourite feature in this counter demo is the demonstration of using a 64-bit
> intermediate in the calculations.

---

## Page 2

### samuell — 2019-12-06 18:11  🟢
> It is this one: http://www.bloguetronica.com/2016/05/gerador-de-relogio-gr10m-s.html.
> I would say so. The 10MHz reference clock generator shows 461fs(rms) of phase jitter
> (12-5000KHz) on the output I was using. See the "datashort" to see more details and
> some scope data. Kind regards, Samuel Lourenço  [Attachment: Especificações.pdf]

### jmg — 2019-12-06 19:24  🟢
> That's quite a decent source, but thinking on this some more, I'd expect that large
> number of samples (100,002) to average down the jitter ? It may be that ~90ps is
> already averaged down ? Picking one variance, 1254196-1253059 = 1137 counts
> difference in 10ms, over 100002 gate pulses.

### cgracey — 2019-12-06 19:32 (edited 19:33)  🏆
> There could be a low beat frequency between the 250 MHz sample rate and the input
> frequency that contributes to a varying duty cycle via gradual aperture shift.

### samuell — 2019-12-06 19:59 (edited 20:01)  🟢
> I forgot to mention that I had to do some unorthodox things in order to get those
> measurements. For one, I didn't used any terminating resistor. Also, I hadn't used a
> ground return connecting the GR10M-S and the P2 Eval grounds, as that seemingly aided
> noise and introduced a very noticeable and very variable skew in the frequency and
> duty cycle readings. That makes me wonder. I would place my bet on the fact that any
> deviation is mostly on the P2 Eval XO. However, expect some deviation on the GR10M-S
> side. Mind that the ±25ppb of stability does not translate to accuracy, as you may
> know. The free run accuracy of the OCXO used in the GR10M-S reference clock allows for
> a ±4.6ppm deviation, in the worst case scenario. As for jitter, i seriously doubt that
> the P2 Eval would be able to capture any. Even the possibility that it can capture
> wander is very dubious. Kind regards, Samuel Lourenço

### jmg — 2019-12-06 20:01  🟢
> Yes, plotting the %H variances may give a clue. Samuell's numbers suggest a ~16ppm
> offset, of P2 to his reference clock. Maybe a better P2 clock source, or a trim-cap,
> can lower than ppm to reduce the beat frequency ?

### cgracey — 2019-12-06 20:06  🏆
> I was using crystal mode %10 (7.5pF). He could try %11 (15pF), or even %01 (no caps).

### jmg — 2019-12-06 20:14  🟢
> These are my recorded Trim values, it looks like P2 is already 'too low' at the 'best'
> %10 and %01 does oscillate, but quite a long way off( +125~144ppm). Notice the simple
> warming of the Xtal gives another variance, from the Xtal tempco.
> ```
> %CC     XI/XO caps     Cooler, No PLL       180MHz/warming  (Eval-A numbers)
> %01     OFF            +144   ppm            +125.68 ppm
> %10     15pF per pin   -6.700 ppm            -24.356 ppm
> %11     30pF per pin   -53    ppm            -68.188 ppm
> ```
> (Note: jmg's cap values per pin differ from Chip's — Chip: %10=7.5pF, %11=15pF; jmg
> labels %10=15pF, %11=30pF. Discrepancy flagged for verification.)

### jmg — 2019-12-06 20:23 (edited 20:25)  🟢
> Yes, any ppm is certainly mostly the Xtal, and that will also vary as the Xtal warms.
> As an example, a NTC-included Xtal spec I have here, gives First-order curve fitting
> coefficient -0.35 ~ -0.18 ppm/'C ie roughly -3ppm every 11 degrees warming. It is
> certainly showing some variances ! My numbers above show the wander in the Xtal, so P2
> can easily capture that. Derive of jitter is not as easy, as you cannot directly
> measure 90ps, but you can see the effects of apertures, and work back from there. I'd
> expect most of the jitter to be in the PLL VCO side of P2, rather than the Xtal
> oscillator.

### samuell — 2019-12-06 20:44 (edited 21:38)  🟢
> I will have to measure other 10MHz clock sources as well, and then compare results.

### jmg — 2019-12-08 19:06  🟢
> Do you have any faster, low jitter clock sources ? You could clock P2 from one of those,
> via the XI pin. Then an A-B comparison with same-MHz done via PLL should be possible,

### samuell — 2019-12-09 20:59  🟢
> I have a faster, yet ultra jittery, clock source. The source you saw me using is the
> best I have. However, I see the need of using an ultra-low jitter clock generator.

### samuell — 2019-12-09 21:18  🟢
Describes using an AD9834 DDS function generator (GF2) to produce a jittery 10 MHz CMOS
3.3V clock through a 7th-order near-Chebyshev filter and fast comparator; results attached
(much worse than the GR10M-S reference; duty tends toward 50% as frequency decreases).
[Attachments: freqgen.png, setup.jpg, schematic.pdf]

### jmg — 2019-12-09 22:40  🟢
> That seems to actually be better (less variance in Duty numbers)... This test:
> 1-1299192/1299454 = ~202ppm ; Previous test 1-1254643/1252723 = ~1532ppm
> ( I think you still use the PLL inside P2 here, as no connections go to XI ? )

### samuell — 2019-12-10 01:07 (edited 01:11)  🟢
> The variance of the duty cycle values may be due to some granularity from the P2 itself.
> ... Chip's program uses the crystal and PLL, and so I'm using those too. No external
> clock is being fed to the P2. No modifications were made to the code.

### evanh — 2019-12-10 01:35  🟢
> Jitter is high frequency, and erratic, it won't register in any significance with this
> method of measuring. The final sampling is what, one per second. And that goes for the
> duty too. It's one humongous average.

### jmg — 2019-12-10 02:29  🟢
> Curious. Are they both CMOS signals, with equally fast-rise drives into P2 ? The
> frequency is very stable in both, because it is averaged over 10ms. The gated-hi counts
> vary by more, because that is a tougher test, where P2 is gating an average of 12.99428
> or 12.541709 SysCLK counts per gate... If you have multi-stable 10.000MHz sources...
> feed one 10MHz ref into XI, (change code to /1 x25, to keep 250Mhz SysCLK) and the other
> into test pin.

### samuell — 2019-12-10 11:42  🟢
Posts oscilloscope shots comparing the GR10M-S (red) and GF2 (yellow) traces; yellow shows
substantially more (~200 ps) cycle-to-cycle jitter. [Attachments: 10MHzWaveforms.png,
10MHzC2CJitter.png]

### evanh — 2019-12-10 12:06 (edited 12:38)  🟢
> Hmm, that's not showing jitter either - because you're locked to a single edge (the one
> on screen) for each pass. You need to include more edges per pass to show any momentary
> stretching of the clock. (with links to prior forum jitter-measurement examples)

### samuell — 2019-12-10 12:35 (edited 12:38)  🟢
> Notice that I'm focused on the next ascending edge from where the trigger is. The trigger
> is actually set with a 100ns deviation... [Attachment: 10MHzC2CJitterRemarks.png]

### evanh — 2019-12-10 12:44  🟢
> They rises are all centre aligned, there's nothing to see.

### samuell — 2019-12-10 13:08 (edited 13:15)  🟢
Explains that at 2 ns/div the yellow trace is visibly thicker at the trigger crossing =
cycle-to-cycle jitter, not scope artifact.

### evanh — 2019-12-10 13:32  🟢
> Then you need to increase the delay a lot more... Looking now at Chip's example, it looks
> like that's exactly how he did it - The time at the top says 100 us, while the time scale
> is 50 ns/div. [Attachment: P2_v1_jitter.jpg]

### samuell — 2019-12-10 13:57 (edited 13:59)  🟢
Agrees the discussion is off-topic; reiterates that Chip's program doesn't measure jitter
in any form; the scope shots only proved GF2 is more jittery than the GR10M-S reference.

### evanh — 2019-12-10 14:09 (edited 14:12)  🟢
> To be honest, I'm not 100% certain of my assertion any longer. I realise now that JMG was
> referencing multiple samples just by looking at the history in the screen shots... It's
> dawning on me that that might be a valid indicator after all. Albeit very low sample count.

### samuell — 2019-12-10 14:34 (edited 14:35)  🟢
Asks how the density variance translates to jitter; asks whether a 10 MHz PLL-derived clock
can be extracted from the P2 under the same conditions as Chip's program.

### evanh — 2019-12-10 14:40 (edited 16:07)  🟢
Sets up an A-B test using a revB globtop Eval board as generator vs a revB-finished Eval
board + scope; corrects board naming in an edit.

### evanh — 2019-12-10 16:01 (edited 16:30)  🟢
> Okay, nope, not even close. Attached is a bunch of consecutive densities (states) as
> reported by Chip's frequency counter program. Doing what JMG did gives about 180 ppm. And
> I think I know why... the crystal oscillator is stable but the PLL instability is causing
> very short oscillations back and forth across the ideal. The absolute jitter of about 110
> ns then fades wrt the long average (10 ms) of the frequency counter... 110ns / 10ms only
> equals 11 ppm so the counter is picking up something more.
> [Attachments: densities.txt, revB_20M5HZ.PNG]

### evanh — 2019-12-10 16:22  🟢
> OH ... the parts-per-million method is rubbish! It completely depends on the measurement
> interval. If the interval is halved then the effect is doubled.

### samuell — 2019-12-10 16:22 (edited 16:25)  🟢
> And I though that GF2 was jittery. Now, that is jitter! The PLL seems to be re-syncing
> every four clocks of the output signal. This seems to be the consequence of coarse
> adjustments, leading to oscillations in phase. I'm not surprised if that causes problems
> related with HDMI...

### evanh — 2019-12-10 16:37 (edited 16:49)  🟢
> I named that wrongly, it is the revB. The revA looks a lot better in that config... Don't
> worry, I am abusing the PLL to get that result, pushing it outside its spec and found a
> particularly bad spot. PS: The setting is 20.5 MHz sys-clock with XDIVP = 1. Normally,
> XDIVP should be something like 4 when this low. This way the VCO in the PLL will be
> operating 4x faster. Note the 20 GS/s at the top...

---

## Page 3

### samuell — 2019-12-10 16:48  🟢
> Sorry, Evan. My mistake. Kind regards, Samuel Lourenço

### evanh — 2019-12-10 17:22  🟢
On his Yokogawa DL-1640 scope purchase history (off-topic).

### jmg — 2019-12-10 18:49  🟢
Long technical post on jitter types, gated-counter variance, duty-cycle effects, and
suggestions for testing with flip-flops and VCTCXOs to normalize duty cycles.

### jmg — 2019-12-10 19:04  🟢
Asks about the test setup and PLL settings.

### evanh — 2019-12-10 19:36 (edited)  🟢
> It's same software and same settings from last time you commented in the other topic. The
> software tries to produce a 1 MHz square wave using smartpin mode NCO_FREQUENCY with
> Y=$8000_0000 and X with closest match rounded down. The 'modulation' looks to be 4.0 μs
> period (250 kHz), or 1/80 of crystal. EDIT: And this could be the half wave I guess.

### jmg — 2019-12-10 19:46  🟢
> ...producing 10MHz and 50% is not going to be easy with 250MHz sysclk.

### jmg — 2019-12-10 19:56  🟢
> Ah, thanks, I skipped over the time base, and thought that was still 10MHz. Asking for
> 1MHz from 20.5MHz is not going to give a great test case, as it needs to /20/21/20/21
> alternating which is 48.78ns of edge wobble just in the NCO effect.

### evanh — 2019-12-10 19:59 (edited)  🟢
> Y=$8000_0000 The square wave is constant regular. It's just a little faster than 1 MHz
> is all.

### evanh — 2019-12-10 20:12  🟢
Posts FFT analysis screenshots comparing clean 80 MHz and dirty 20.5 MHz sysclock references.

### jmg — 2019-12-10 22:27 (edited)  🟢
> Ah yes, the NCO distracted me. Configured that way, you have SysCLK/2/N, and N=10 gives a
> predicted time of 3.90243us for 4 cycles, which is what your scope shows as the mean, now I
> look closely at the scales.

### pilot0315 (Martin) — 2020-02-08 20:19  🟡
Tried the code, found no scope output or PST display; asks if something was missed.

### pilot0315 — 2020-02-08 20:21  🟡
> @ersmith Howdy, can you tell me why Chip's code did not work as is? Thanks

### pilot0315 — 2020-02-09 01:08  🟡
> @cgracey Got nothing with this baud rate, tried others, no joy...

### cgracey — 2020-02-09 02:39  🏆
> Are you using PNut or FlexGUI? It was written under PNut. There could be some difference
> between tools.

### evanh — 2020-02-09 10:19  🟢
> loadp2 defaults to 115200 baud. I think FlexGUI uses -b230400 parameter to loadp2. If you
> want to use faster then -b1000000 will match Chip's baud setting. Pin P2 is the measuring
> input. There is no generated signal so touching the first accessory header with your finger
> will be enough to get numbers sent to the comport.

### pilot0315 — 2020-02-10 23:55  🟡
> @evanh got it thanks

### pilot0315 — 2020-02-11 08:54  🟡
> @cgracey Pnut. @evanh told me about touching the header. Gonna try it.

### pilot0315 — 2020-02-11 09:07 (edited)  🟡
Asks clarifying questions about terminology ("time density and quantity"); thanks others.

### evanh — 2020-02-11 11:23 (edited)  🟢
> Err, sorry, the input pin is P0 rather than P2. The frequency is of the electrical
> discharge... If you have a typical oscilloscope then it'll have a 1 kHz 1 Volt square wave
> output as a calibration test point. You can hook this up and measure it with the prop2. Two
> wires: One for GND, the other is the 1 kHz to P0. However, for the prop2 to see the 1 Volt
> it needs a small tweak to the program. Update this one line:
> ```
> msr_time	long	%0000_0000_000_1100_000100000_00_10101_0	'msr_pin+0 config
> ```

### pilot0315 — 2020-02-11 23:59  🟡
> @evanh I will do that thanks

### pilot0315 — 2020-03-01 00:25  🟡
Asks for a plain-English explanation of:
> tx_mode long (round(sysfreq / baud * 65536.0) & $FFFFFC00) + 7 '8N1
and how the mask is applied.

### jmg — 2020-03-01 00:52  🟢
> I think the intention is to not lose precision, so items are kept as floats, as long as
> possible. The 65536.0 is 2^16 in floating point, and is equivalent to shift left 16. The
> anded mask, then keeps the wanted shifted bits, and removes the unwanted ones. IIRC Chip
> as some fractional baud support in P2, so the mask is keeping some bits that would be to
> the right of the decimal point.

### evanh — 2020-03-01 01:03 (edited)  🟢
Detailed five-point explanation of the serial-config equation: round(), floating-point
scaling, 16.16 fixed-point format, masking (& $FFFFFC00), and word-length bits.

### evanh — 2020-03-01 01:17 (edited)  🟢
> Here's an alternative that produces the same outcome
> ```
> tx_mode    long (round(sysfreq / baud * 64.0) << 10) | 7
> ```

### pilot0315 — 2020-03-01 01:19  🟡
> Thanks @evanh and @jmg . I will study this.

### evanh — 2020-03-01 01:28  🟢
> Yes, it retains some fractional precision that can be directly used by the smartpin serial
> hardware.

### pilot0315 — 2020-03-01 23:50  🟡
Reports no square wave appearing after modification while using the scope calibration output.

### pilot0315 — 2020-03-15 22:10  🟡
> Attached the Propscope to P0 It appears to ground out P0. Remove scope ground from the
> ground pin and the program works. With or without scope grounded to the board, nothing
> shows on the screen.

### evanh — 2020-03-16 03:44  🟢
> Does PropScope have a square wave output? Most likely, without a ground reference, your
> probe will be acting as an antenna and wiggling pin0 input on the prop2.

### Rayman — 2020-03-17 01:24  🟡
> I had no idea what 'reciprocal counter' meant, but I got curious just now and googled this
> up (link to a Keysight article explaining frequency-counter operation).

---

## Page 4

### jmg — 2020-03-17 02:36  🟢
> Yes the block diagram and maths are simple. Chip added support in the smart pins to make
> the hardware details simple too.. (it can get tricky to ensure the two captures of time and
> cycles are made on the same edge, and ideally, you want lossless/gapless capture too, so 10
> or 100 captures of time and cycles can be summed to give higher precisions )

### Rayman — 2020-03-18 13:28  🟡
> I think it should actually be called 'period counter'. I guess they mean 'reciprocal of
> frequency' counter. But 'reciprocal of frequency' == period. I think that would make usage
> more clear. But, when you google 'period counter' you get other stuff, which is maybe why
> the chose this name...

### pilot0315 — 2020-03-18 17:04  🟡
> @evanh I used it to do the other waves that you helped me with in the past.

### jmg — 2020-03-18 19:12  🟢
Long post on naming: suggests "reciprocal frequency counter" or "whole periods timer",
emphasizing that the final units are Hz and "frequency" should be in the name.

### pilot0315 — 2020-06-23 01:01  🟡
Thanks cgracey and evanh for help with the reciprocal counter demo; asks assembly-code
questions with an attached file.

### Ramon — 2021-04-05 03:13  🟡
Reports success on FlexProp and PNUT; notes modifications (line feed for FlexProp, clock
frequency for PNUT); shares measured results from a 50 MHz oscillator.

### evanh — 2021-04-05 06:16  🟢
Answers pilot0315's assembly questions about the `pop` instruction and return addresses in
stack operations.

### evanh — 2021-04-05 06:54  🟢
Explains `shl`, `altgb`, and `getbyte` regarding bit shifting and indirect addressing.

### Ramon — 2021-04-05 12:59  🟡
Asks how to convert the PASM code to Spin2 with minimal lines; includes an attempted conversion.

### Francis Bauer — 2021-04-06 04:23  🟢
Recommends reviewing the TSL235R Quick Byte documentation, with two inline-PASM2 driver
routines for frequency measurement using 2–3 smart pins.

### evanh — 2021-04-06 06:43  🟢
> Ramon, You won't be able to JMP between assembly blocks like that. Each Pasm block is
> handled one at a time with just what is defined for it, not unlike Spin methods. Any
> branching will have to be within a block.

### Ramon — 2021-04-06 14:49  🟡
Thanks Francis and evanh; asks about using single smart pins.

### Ariba (Andy) — 2021-04-06 23:42  🟢
Complete Spin2 example for simple frequency measurement using P40 input and P39 test output
(the canonical dual-smartpin Spin2 version widely reused later in the thread).

### Ramon — 2021-04-07 14:50  🟡
Notes typos in Ariba's code (lines 4 and 7); provides a FlexProp-compatible version.

### Ariba — 2021-04-07 23:11  🟢
> (Explains) the first pinstart generates the test frequency; the dual smartpins measure
> complete periods within a time window; explains the ticks and periods terminology.

### ersmith — 2021-04-08 01:15  🟢
> I think you need to update your flexprop. addpins, frac, and debug have been supported for
> some time now.

### evanh — 2021-04-08 01:23  🟢
Asks about the debug-support mechanism in flexspin/loadp2.

### ersmith — 2021-04-08 01:26  🟢
> It is exactly via loadp2 -t :) debug statements just get translated into the equivalent of
> BASIC 'print' statements.

### evanh — 2021-04-08 01:45  🟢
Reports the simple debug demo doesn't produce output with flexspin 5.3.3-beta.

### ersmith — 2021-04-08 12:16  🟢
> DEBUG() statements are optional... In order to enable debug() flexspin needs the -g flag on
> the command line.

### evanh — 2021-04-08 13:12  🟢
> Thanks, that got it. The needed .c sources was a surprise.

### Ramon — 2021-04-08 13:51  🟡
Reports syntax errors with frac, addpins, debug, and udec in FlexProp 5.3.2.

### Ramon — 2021-04-08 14:04  🟡
Thanks Ariba; enthusiastic about smartpin capabilities; proposes a test-program concept.

### ersmith — 2021-04-08 15:35  🟢
> Ah, I see the problem, your file is named .spin (for Spin 1) instead of .spin2 (for Spin 2).
> The two languages are slightly different, unfortunately.

### Ramon — 2021-04-08 16:17  🟡
Humorous acknowledgment of the file-extension mistake.

### evanh — 2021-04-08 23:35  🟢
Clarifies that each pin has one smartpin; describes input-rerouting capabilities without wires.

### evanh — 2021-04-08 23:53  🟢
Code example showing smartpin setup without wires using P_MINUS routing modes.

### Ramon — 2021-04-09 00:55  🟡
Asks about generating and measuring a test frequency with just two pins.

### evanh — 2021-04-09 01:07  🟢
Explains that one active pin suffices due to configurable input rerouting (test without a
loopback wire).

### evanh — 2021-04-09 01:10  🟢
References the smartpin block diagram; explains logic-input selection and routing from nearby pins.

---

## Page 5

### jmg — 2021-04-09 01:25  🟢
> Yes, a wire is useful for complete connection testing, but you can also use internal
> loopback... The code above gives a Reciprocal Frequency Counter, so it captures both Whole
> window Periods and time for those periods. It uses 2 smart pin cells, but does not fully
> consume the second pin, it can still be used for general SW IO tasks. Then Cycles/Time gives
> frequency, and has a very wide dynamic range. eg The numbers you gave in #97, show a LSB of
> 0.4ppm. If you can accept lower dynamic range... you could configure for a simpler,
> non reciprocal fixed time gate, and count cycles on a single pin cell. eg a 100ms time gate,
> with 1KHz in, counts 99 or 100 or 101, so only has 1% precision, but at 5MHz it is 2ppm.

### evanh — 2021-04-09 01:29  🟢
> I don't think the external wire has any use.

### jmg — 2021-04-09 01:39  🟢
> It does if someone wants to check 100% the PCB wiring and pin soldering, which is why I
> suspect it is stated as being 'a requirement'. Self-test internal loopback is ok, but it
> only reaches so far.

### evanh — 2021-04-09 01:51  🟢
> That's not testing the chip any longer is it. You'd also want to load up the pins for solder
> testing. Make sure there's no parasitics making the test pass when it should fail. And then
> put the whole board in a test jig as well.

### evanh — 2021-04-09 02:04  🟢
> Frequency response of the different drive strengths could be used for board level pass/fail,
> still without any external loop-backs. An advantage available due to every I/O pin capable of
> simultaneous output and input, including threshold setting and DAC/ADC options.

### Ramon — 2021-04-09 04:55  🟡
> Exactly what jmg said. The wire is the load. Otherwise you are just testing until the I/O die
> pad, right? Variable frequency output/input response plot. Better than just pass/fail test
> (like a Shmoo plot, maybe?)

### Ariba — 2021-04-09 11:33  🟢
> @evanh said: I don't think the external wire has any use.
> You can use the same wire to measure the frequency of the the source with unknown frequency,
> for which you have made this whole frequncy counter ;-) There is a world outside the P2 in
> that you can do practical things...  Andy

### evanh — 2021-04-09 13:18  🟢
> Lol, now you've completely change the subject. The "wire" was only a link between two pins
> that Ramon wanted for checking I/O function. Now it's a dangly antennae with a kitchen
> attached. :)

### evanh — 2021-04-09 13:19  🟢
> In terms of board testing, that can be done without any external loopback.

### Ramon — 2021-04-09 15:23  🟡
> I don't think so. Based on my limited but previous experience doing exactly that kind of
> testing for telco equipment. The main question is: where is your loopback? My guess is that
> you are just testing the I/O pad...

### evanh — 2021-04-09 23:37  🟢
> When it comes to frequency response, there is an expected ideal for a given layout. Each I/O
> pin can be mapped with a unique signature from a selection of drive strengths... With the
> Prop2, the input of each pin can monitor that response while the output is driving it with
> varying strengths. It's a huge advantage that every pin has the full set of I/O resources to
> select from. You couldn't do this with just any chip.

### evanh — 2021-04-10 01:37  🟢
> On the very left of that block diagram earlier you can see how there is four blocks all
> connected to the physical pin... It is simplified but still accurately depicting the way each
> I/O pin is wired internally. The input circuits are always active irrespective of if an output
> circuit is driving the pin. DAC outputs are settable to strengths of 75 ohms to 990 ohms,
> while logic outputs are settable to strengths of 20 ohms to 150 kohms. Inputs can be simple
> 50% threshold logic, or 1 volt hysteresis Schmitt Trigger, or comparator threshold, or even
> using the ADC. Performance of the output is affected by what's connected externally and how
> hard it's being driven. The input circuits can monitor that performance. And can do it in
> multiple ways in parallel thanks to the %AAAA and %BBBB input selectors.

### evanh — 2021-04-10 01:48  🟢
> I've noticed there is a 600 ohm resistor in the schematics that could be added to the block
> diagram. It's inline from the physical pin to the logic/compare/schmitt input circuits. But
> not for the ADC interestingly. EDIT: Ah, that's because the ADC has it's own input resistors.

### pilot0315 (Martin) — 2022-09-02 13:39  🟡
> @cgracey Howdy, I tried the rcd when you first posted it. I have been out of the loop for
> almost two years. Tried it again in Pnut and Prop tool. Getting nothing at the
> baud = 1_000_000.0 'serial baud rate on P62 (float). Is there something I am missing? Thanks
> in advance. Martin

### evanh — 2022-09-02 14:47  🟢
> It doesn't print anything until the measurement pin is toggling. Wipe pin P0 with your finger.

### pilot0315 — 2022-09-06 12:16  🟡
> @evanh Thanks. Got it working, forgot about the finger triggering the code.

### Rayman — 2024-12-20 21:46  🟡
> Wanted to measure the VSync rate for a TFT LCD project... Adapted @Ariba code like this and
> seems to work:
> ```spin2
> OBJ
>     ser    : "SimplestSerial"
>
> PUB TxVsyncFreq() |mintime,ticks,periods,freq
>
>   'SclPin = basepin+15
>   'SdaPin = basepin+14
>   'VSyncPin = basepin+12
>
>   ser.start(230_400) 'start serial
>
>   mintime := clkfreq / 1_000             '1ms min measure time
>   pinstart(VSyncPin+2, P_MINUS2_A + P_MINUS2_B + P_COUNTER_TICKS, mintime, %00)
>   pinstart(VSyncPin+3, P_MINUS3_A + P_MINUS3_B + P_COUNTER_PERIODS, mintime, %00)
>
>   repeat
>     akpin(VSyncPin+2 addpins 1)              'start next measurement
>     repeat until pinr(VSyncPin+2)            'wait until done
>     ticks   := rqpin(VSyncPin+2)           'read measured values
>     periods := rqpin(VSyncPin+3)
>     freq := muldiv64(clkfreq, periods, ticks-1)     'calc frequency
>
>     ser.str(@"VSync Freq = ")
>     ser.dec(freq)
>     ser.tx(13)
>
>     waitms(300)
> ```
> [SimplestSerial.spin2 attached, 4.7K]

### Rayman — 2024-12-20 21:48  🟡
> Kind of wish snippets like this were collected somewhere... @JonnyMac Made a lot of things
> like this for the PropTool library, but this one isn't there (?)
