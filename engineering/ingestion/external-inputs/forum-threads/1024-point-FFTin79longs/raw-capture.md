# Raw Capture — "1024-point FFT in 79 longs"

Source: https://forums.parallax.com/discussion/170948/1024-point-fft-in-79-longs
Thread ID: 170948 · Pages: 4 · Fetched: 2026-07-01

> NOTE: Some very large attachment-style code listings (full HDMI+mic+spectrograph
> programs, ~500–600 lines) were posted as forum code blocks / file attachments and
> were elided by the fetcher as "[Complete … code provided]". These are marked inline
> below. All cgracey inner-loop / butterfly code and all short code fragments are verbatim.

---

## Page 1

### cgracey — 2019-12-17 15:27
"I just made this and it works fine. It takes a hair over 3ms at 250MHz. It converts 1024 signed word samples to 512 frequency powers."

[FFT code block with assembly implementation — full listing posted as forum code block; elided by fetcher]

"Maybe someone can figure out how to make it faster. I used all the tricks I could think of, but I'm sure more is possible."

### Reinhard — 2019-12-17 17:11
"WOW!!! With this demo, the P2 is in the league of digital signal processors. I suspected it, but so far I still lack the experience in p2asm. I will also need a demo board soon. Testing with the simulator is very tedious. Thanks for sharing this example. Reinhard

edit:
Cheers to the rev command.
I wanted to assemble that next, but there is ;-)"

### cgracey — 2019-12-17 17:41
"I wonder how fast mdern DSP's can do a 1024-point FFT. It might be a few microseconds.

I think the simplest way to speed up this program would be to take bigger bites in the inner loop, so that we load/store more A's and B's and pipeline more CORDIC operations. Right now it's taking ~750,000 clocks to do 10,000 operations. That's 75 clocks per. We could probably get it down to 30 clocks. Then, boost the clock a little more and we'll be under 1ms."

### Publison — 2019-12-17 17:56
"We need to get a board to you ASAP. I can send you my board right now. I can wait for the new run in the next 2-3 weeks. PM me if you are interested."

### Reinhard — 2019-12-17 18:02
"In this context, I have another question. How fast is the internal ADC and what bit width does it have. An external ADC with 16 bit would not be a drama either."

### Reinhard — 2019-12-17 18:05
"Thank you, I live in Germany and I don't know how complicated it is to send."

### jmg — 2019-12-17 18:27
"The internal ADC are modest, ok for a MCU. Tests on the ES1 silicon, had 10~12bit ADC, which varied with supply and pin and MHz. An external ADC will be needed to highest performance. P2 can support the external isolated ADCs, which give 78kHz BW and 12~14b useful from a 16b result."

### Reinhard — 2019-12-17 18:36
"Thank you. I mean the P2 has enough pins if a very high-performance application is needed. a flash ADC can also be connected, which loads the data in parallel."

### Rayman — 2019-12-17 18:54
"I wonder how much using two cogs with shared LUT would speed things up..."

### Reinhard — 2019-12-17 19:03
"Yes, I've already thought of that. I just have no concrete idea at the moment how it can be synchronized. A parallel processing, that would be a huge thing. I think it is possible."

### Publison — 2019-12-17 19:11
"On the road now. PM in about an hour."

### TonyB_ — 2019-12-17 20:22
"I haven't looked at pipelined CORDIC yet. Is it possible to issue a new command every 8 cycles, with three 2-cycle instructions in between? Eight A's and B's in the inner loop look to be optimal, at first glance. More accurately, anything less looks to be sub-optimal.

Pity there's no SUB2 (D = D - 2*S), nor for other applications an atomic SHR & ZEROX, the latter operation using the spare S bits, similar to BITx."

### evanh — 2019-12-17 22:47
"Correct for an 8-cog prop2. For a 16-cog prop2 the tightest is every 16 clocks, with up to seven 2-cycle instructions between."

### cgracey — 2019-12-19 19:16
"I just had a huge realization!

The core of the inner loop of the FFT has this:

```
		qrotate	b1,angle

		qrotate	b2,angle

		getqx	b1
		getqy	b2

		getqx	n
		add	b2,n
		getqy	n
		sub	b1,n
```

I started staring at that sequence, thinking there must be some simple objective to what it does. I had transcribed this code from some 80386 assembly code I had written 16 years ago, so I was just trying to do it faithfully, without really understanding WHAT it was doing. Actually, I never before REALIZED what it was doing.

Looking at that sequence, my brain started to remember the (X,Y) rotation equations:

x′=xcosθ−ysinθ
y′=ycosθ+xsinθ

That seemed to be maybe what it was doing.

So, I substituted a single CORDIC operation for that whole sequence:

```
		setq	b2		'rotate (b1,b2) by angle
		qrotate	b1,angle
		getqx	b1
		getqy	b2
```

AND IT WORKED!!!!!

So, the CORDIC can really whip the core of the FFT problem. This just leaves some adds and subtracts in the inner loop. Cool!!!!! This can be sped up WAY more than I originally thought."

### cgracey — 2019-12-19 19:33
"The inner loop of the FFT now looks like this. Very straightforward:

```
.loop3		setq	#2-1		'read (a1,a2)
		rdlong	a1,ptra

		setq	#2-1		'read (b1,b2)
		rdlong	b1,ptrb

		setq	b2		'rotate (b1,b2) by angle
		qrotate	b1,angle
		getqx	b1
		getqy	b2

		add	a1,b1		'write (a1+b1,a2+b2) to (a1,a2)
		add	a2,b2
		setq	#2-1
		wrlong	a1,ptra++

		sub	a1,b1		'write (a1-b1,a2-b2) to (b1,b2)
		sub	a1,b1
		sub	a2,b2
		sub	a2,b2
		setq	#2-1
		wrlong	a1,ptrb++

		djnz	c2,#.loop3
```
"

### Rayman — 2019-12-19 19:35
"wonder if you could rdlong ptra[1], rdlong ptrb[1] to get the next values in between qrotate and getqx…"

### cgracey — 2019-12-19 19:58
"We could read 16 pairs at a time and then stuff the CORDIC pipeline.

This FFT does the following-sized runs of rotations and adds/subs on contiguously-placed coordinate pairs:

512
256
128
64
32
16
8
4
2
1

So, if we hard-coded 16 rotations+adds/subs, the extra operations just wouldn't be saved in the last four runs of 8, 4, 2, and 1. That would speed things way up and not waste much time."

### Rayman — 2019-12-19 20:31
"Not sure if this is the right place, but I had a question about your FFT demo on the Chat yesterday...

Looks like you are coupling the microphone input just through a cap to a prop2 pin, as you said.

But, don't you need to bias the pin at Vdd/2 for that to work right?
Seems to me the bias level would float around, potentially causing the peaks or valleys to get clipped..."

### cgracey — 2019-12-19 20:35
"The ADC pulls it to its own center, which is the threshold of a particular inverter, and close to VIO/2."

### Rayman — 2019-12-19 20:45
"Ok, interesting. That's a nice feature.

One other thing...
I think in real life, you'd want to apply a windowing function to avoid distortions due to the first point not being close to the last point in the set... looks like Hamming window might be popular from this:

https://www.edn.com/windowing-functions-improve-fft-results-part-i/"

### Cluso99 — 2019-12-19 20:47
"```
		sub	a1,b1		'write (a1-b1,a2-b2) to (b1,b2)
		sub	a1,b1
		sub	a2,b2
		sub	a2,b2
		setq	#2-1
		wrlong	a1,ptrb++
```

This seems to be doing
(a1-2*b1, a2-2*b2)
???"

### cgracey — 2019-12-19 20:50
"A1 and A2 previously had B1 and B2 added to them. So we need to subtract twice now."

### cgracey — 2019-12-19 20:52
"Ah, yes, it never occurred to me, but we need to do that. I'll integrate it into the FFT input gathering. Thanks."

### cgracey — 2019-12-19 21:22
"Upon closer examination, the FFT does the following-sized runs of rotations and adds/subs on contiguously-placed coordinate pairs:

512 x 1 time
256 x 2 times
128 x 4
64 x 8
32 x 16
16 x 32
8 x 64
4 x 128
2 x 256
1 x 512

I've got a 16-pair CORDIC stuffer coded up, but I noticed it was slowing down when it got to the 8x64 operation.

All operation sets of size 16x32 and up are each taking only ~68us! So, it's getting 60% of the job done in only 420us. I need to code special cases for the last four operation sets to get the overall time minimized."

### TonyB_ — 2019-12-20 00:50
"The 'Hanning' window is another name for Hann that we use in scope mode."

### Rayman — 2019-12-20 01:24
"Seems we could use this for voice recognition...
There are some free datasets available these days:
https://www.cmswire.com/digital-asset-management/9-voice-datasets-you-should-know-about/"

### TonyB_ — 2019-12-20 01:34
"I think most of us would find the 16-pair pipelined CORDIC code interesting, even if not complete. The egg-beater comes in to play here, too. Is there any fixed phase relationship between ptra & ptrb in the inner loop, for 16 x 32 in particular? Or do the bit reversals make the address differences pretty random?

There are five instructions between wrlong a1,ptra++ and wrlong a1,ptrba++ which could be reduced to three with a few more instructions earlier."

### cgracey — 2019-12-20 02:39
"Thanks, Rayman. I didn't know such things existed. I wonder how usable it is by us.

By the way, I did what you said and placed one of the SETQ+RDLONG sequences between the QROTATE and GETQX and it certainly sped things up. I will use that for a simple implementation that is compact.

I've been playing around with optimizing the FFT today and have made a lot of progress, but when I get to the last iteration set of 1x512, the angle must be recalculated for every sample and I can't fit it into two instruction, as I'd like, in order to get it to flow with the CORDIC. There is a REV needed and two instructions before that. That last iteration set is a special case in a few different ways, when trying to optimize it. It's slowing the whole FFT down."

### cgracey — 2019-12-20 02:40
"Tony, how would you reorder that?

I have it like this now, for readability:

```
.loop3		setq	#2-1		'read (bx,by)
		rdlong	bx,ptrb

		setq	by		'rotate (bx,by) by angle
		qrotate	bx,angle

		setq	#2-1		'read (ax,ay)
		rdlong	ax,ptra

		getqx	bx		'get rotated (bx,by)
		getqy	by

		add	ax,bx		'(ax,ay) = (ax+bx,ay+by)
		add	ay,by

		shl	bx,#1		'(bx,by) = (ax-bx,ay-by)
		subr	bx,ax
		shl	by,#1
		subr	by,ay

		setq	#2-1		'write (ax,ay)
		wrlong	ax,ptra++

		setq	#2-1		'write (bx,by)
		wrlong	bx,ptrb++

		djnz	c2,#.loop3
```
"

### TonyB_ — 2019-12-20 03:22
"Chip, what you have now is excellent, with the absolute minimum between the WRLONGs. SUBR is such as great instruction, yet so easily overlooked. I was re-ordering the SUBs and it's not worth showing now.

Could we use REP in the inner loop?"

### cgracey — 2019-12-20 03:32
"We could use REP, but it wouldn't save much time. Also, it would block interrupts."

---

## Page 2

### Cluso99 — 2019-12-20 06:46
"Aha. Makes sense now :)"

### cgracey — 2019-12-20 11:29
"I cleaned up the spectrograph program and the FFT inside. If you want to run it on your P2 Eval board, connect the HDMI board to P[55:48] and hook a microphone into the A/V board on P[7:0]. Or, just connect a microphone via a .1uF capacitor to P[5].

I made some enhancements that Rayman suggested, like adding a window function for the FFT input sample set. I made a nice cosine-shaped window filter which actually cleaned up the output quite a bit.

Here is the code, followed by a partial screen shot of me talking into it:"

[Complete PASM2 code provided — ~500 lines of assembly including HDMI driver, microphone handler, and spectrograph processor with FFT implementation; posted as forum code block, elided by fetcher]

"Here is a file containing the code and the updated PNut.exe you will need to compile it with:

https://drive.google.com/file/d/1vWiyXDIwwLDsx0Fsyc7Mdqqu4jC87jdc/view?usp=sharing"

### cgracey — 2019-12-20 11:38
"I've been messing around with FFT stuff all day and I realized that when you are dealing with small contiguous operations, they all lie next to each other in memory, making it easy to load and save contiguous stretches of hub RAM, while performing the smaller math on the entire loaded memory section. I'm going to work on this a little more tomorrow and be done with it for a while. Currently, this code takes 3ms to do the entire FFT procedure. Tomorrow, I should be able to get it working in under 1ms."

### Rayman — 2019-12-20 11:47
"Looking at mp3 again... noticed that they take samples from past frame and next frame into ends of current frame.

I think that makes sure you don't miss anything when the window is applied...

For this, I wouldn't do it.
But for voice recognition, might want to."

### evanh — 2019-12-20 12:09
"I don't think I've ever seen a spectrum analyser image looking that detailed before. The flashy MP3 ones always appeared useless so it hasn't much interested me."

### lonesock — 2019-12-20 18:21
"My FFT skillz are rusty, but isn't the smallest loop (1x512) only doing rotations by 90-degrees (or was it 180?). If that's the case it should be easy to special case that pass. If I am way off, then sorry for the distraction!

Jonathan"

### Rayman — 2019-12-20 19:03
"I think it'd also be nice to just show x-y plot of magnitude vs. frequency..."

### cgracey — 2019-12-20 20:10
"> Rayman wrote: I think it'd also be nice to just show x-y plot of magnitude vs. frequency...

You probably already realize this, but that spectrograph program shows frequency (0Hz..15KHz) on the vertical, time rolling left on the horizontal (60 pixel columns per second), and magnitude as pixel intensity. Seeing the FFT output change over time gives a whole extra dimension to what FFT's are usually used for."

### cgracey — 2019-12-20 20:13
"> evanh wrote: I don't think I've ever seen a spectrum analyser image looking that detailed before. The flashy MP3 ones always appeared useless so it hasn't much interested me.

It's going to be really interesting when we can modify DDS signals within feedback loops and watch them like this. It'll be a whole new frontier of possibilities."

### cgracey — 2019-12-20 20:58
"> lonesock wrote: My FFT skillz are rusty, but isn't the smallest loop (1x512) only doing rotations by 90-degrees (or was it 180?). If that's the case it should be easy to special case that pass. If I am way off, then sorry for the distraction! Jonathan

I just looked at the angles and I'm surprised to see that they only range from 0 to just under 180 degrees. Makes sense, though, as the compounding of rotations can create many effective angles greater than 180 degrees.

Here is what I'm seeing:

```
span	iter's	angles (MSBS, 000/400/200 = 0/90/45 deg)
--------------------------------------------------------
512	1 	000
256	2	000 400
128	4	000 400 200 600
64	8	000 400 200 600 100 500 300 700
32	16	000 400 200 600 ... 180 580 380 780
16	32	000 400 200 600 ... 1C0 5C0 3C0 7C0
8	64	000 400 200 600 ... 1E0 5E0 3E0 7E0
4	128	000 400 200 600 ... 1F0 5F0 3F0 7F0
2	256	000 400 200 600 ... 1F8 5F8 3F8 7F8
1	512	000 400 200 600 ... 1FC 5FC 3FC 7FC
```

So, the first 512-span iteration doesn't even rotate anything, and just does the adds/subs. The next 256-span iteration only rotates by 90 degrees in its last half. In every inner loop, the rotation can be skipped when the angle is zero."

### cgracey — 2019-12-20 22:10
"I think I'm going to go back to work on Spin2 now and not worry about optimizing this FFT. That can be done at a later time. What we have is very simple and understandable and not too slow. I think only a 3x speed-up is possible. If 10x was possible, I'd keep working on it, but for now, we've got something pretty good and very compact.

I was really pleased to realize that SETQ+QROTATE takes care of all the hard math in the FFT. The rest is just adds and subtracts. I keep wondering, though, if there's another level of optimization possible, aside from stuffing the CORDIC and unrolling the inner loop, somewhat."

### msrobots — 2019-12-20 22:15
"You need to write a spin version and compare the results, so back to Spin...

Mike"

### Publison — 2019-12-26 20:32
"The unrelated responses were moved to a new thread:
http://forums.parallax.com/discussion/170982/heater-has-6-3-vac#latest"

### SaucySoliton — 2020-05-07 04:48
"Finally tried this out. Very cool! Here is a version that uses scope mode and therefore can support data rates in the megasamples. It's set at 3.676MSPS right now as that is what is needed to show the entire AM radio band on the screen. It really looks like we could receive AM radio by just connecting a wire to a P2 pin.

I added some syncronization between the acquire and processing. The streamer would otherwise write so fast that samples would change before the an entire 1024 samples is read by the window filter code. It's my first time using cogatn. It was easy. The code also has changes to compile with fastspin."

[Complete scope-mode spectrograph code provided — ~600 lines; posted as forum code block, elided by fetcher]

### Rayman — 2023-10-13 23:07
"I'm wondering if this could be used for wake word voice recognition or maybe a few simple commands...

Looks to be pre-Spin2 though, might take some work to get it going in Spin2...

Also not sure why Chip had the ADC at 100X for a real mic. Pretty sure my SparkFun one only needs about 10X or so... Need that for sure for unamplified mic for sure..."

### Rayman — 2023-10-14 14:41
"Just tested this out with SparkFun amplified mic: https://www.sparkfun.com/products/12758

100X gain on ADC is definitely way too much. Dialed that down to 1X (or maybe 10X with LDO board) like this:

```
pgm_mic         'wrpin   ##%100111_0000000_00_11000_0,#mic_pin   'set mic for 100x-mag and 14-bit SINC2 sampling
                wrpin   ##P_LOCAL_A|P_ADC_1X|P_ADC ,#mic_pin
```

I'm thinking there is definitely possibility of using this for voice recognition...

Took some pics, first with a board without LDOs. I think you can see the power supply ripple showing up as horizontal lines with this board...
IMG_1918: Saying "Yes" then "No" repeat. 1X gain. "Yes" is the skinny, tall one and "No" is short and wide.
IMG_1919: Wistling three notes repeatedly. 1X gain. This would be another way to interact, probably easier...

Next, switch to a board with LDOs on the mic pins.
IMG_1920: "Yes" and "No" with 10X gain
IMG_1921: "Yes" and No" with 1X gain

[Attachments: IMG_1918.jpg, IMG_1919.jpg, IMG_1920.jpg, IMG_1921.jpg, Chip_FFT_mod2.spin2]"

### Rayman — 2023-10-14 15:16
"Here's a slightly modernized version of the code. It doesn't start with an erased screen like the original though...
Next step is to un-hardcode the buffer addresses...

[Attachment: Mic_FFT_HDMI_1b.spin2]"

### avsa242 — 2023-10-14 15:27
"Very cool...I don't know how I ever missed this thread. I ported Heater's P1 spin-based FFT to the P2 several months back to try out things like audio and hopefully eventually RF - looks like @SaucySoliton had a similar idea with this code here. This is great though...so compact. One thing I couldn't figure out with Heater's code was how to change the sampling bandwidth (so for ex., to focus on smaller swath of spectrum) - I think I was only able to accomplish something like it by setting the number of points to something smaller. Not having looked at this in depth yet, is it reasonably easy to change parameters like that?
Good luck with the voice recognition btw, that'd be a great addition."

### Christof Eb. — 2023-10-15 11:50
"For voice recognition after you have decided, which few frequencies are relevant, it will be probably more efficient to use the Goertzel algorithm instead of fft. Wasn't there a thread about it somewhere?"

### Ariba — 2023-10-15 22:27
"https://forums.parallax.com/discussion/115725/goertzel-based-speech-recognizer-now-with-source-code/p1"

### Rayman — 2023-10-19 13:23
"Starting to get a handle on this code...
Here's a version with VGA instead of HDMI

There's one thing that Chip added to the HDMI driver that I needed to copy into the VGA driver:
`wrbyte #1,#0 'signal ideal time to update bitmap`

Seems like would be better to use cogatn instead, but I guess this works.

[Attachment: Mic_FFT_VGA_1b - Archive.zip]"

### Rayman — 2023-10-19 13:40
"Right now, the buffers start at $1000, which kind of clobbers the spin2 interpreter. Kind of surprising it still works.
But, it's mostly all assembly, Spin2 just needs to start up to cogs...
Original was all assembly and so didn't have spin2 interpeter..."

### Rayman — 2023-10-19 17:16
"Got the buffers change from being constants to addresses of variable arrays.
Should be able to make this into a subobject now.
Mic ADC gain is set to 100x for unamplified electret mic.

One thing I haven't figured out is why I can't insert instructions at the start of the Spectrograph Driver.
Adding even a nop there breaks it...

```
DAT  'Spectrograph Driver
'******************
'*  Spectrograph  *
'******************
org
                   'nop  'RJA: Can't have anything here!  Why not?

pgm_spectro     call    #fft                    'do fft on current samples
```

[Attachment: Mic_FFT_VGA_1c - Archive.zip]"

### evanh — 2023-10-19 21:33
"Someone a while back did a test of the ADC performance and found that the noise floor of x100 gain is ten times noisier than the x10 gain. That said, I have no idea how scientific the testing actually was."

### evanh — 2023-10-19 21:45
"> Rayman said: One thing I haven't figured out is why I can't insert instructions at the start of the Spectrograph Driver. Adding even a nop there breaks it...

The COGINIT requires `pgm_spectro` to be at ORG 0."

### Rayman — 2023-10-19 22:14
"Right. Thanks @evanh
Obvious now…"

### Rayman — 2023-10-20 16:18
"I've added this brief analysis of the situation to the top of the code here.
Only the lower half of the screen is going to be useful for voice recognition.
So, using the upper half of screen to plot the results of the last FFT operation.
Also, doing a very crude amplification of higher frequencies.

```
CON ''Notes:
        ''Mic Sample rate is dependent on P2 clock frequency
        ''Code is set for SINC2 sampling at 14 bits, 8192 clocks per sample. --> Sample frequency =  250_000_000/8192 =  30517.58 Hz
        ''FFT on 1024 samples -->  Max. update rate on all fresh samples =     30517.58/1024 =  29.8 Hz
        ''Video driver signals Spectroscope driver to refresh screen during vertical blanking (and then do another FFT and wait), so 60 Hz
        ''   --> Each FFT is on about half old, half new samples

        ''Frequency resolution (steps in frequency between FFT result) =  30517.58/1024 = 29.80 Hz
        ''FFT result is 512 real and 512 imaginary steps, so range is from 0 Hz to 29.80*511=   15228.99 Hz
        ''Wikipedia says telephony uses range from 300 to 3400 Hz.  0..4000 Hz would be lower 134 pixels in this display (about lower 1/4 of display)
```

[Attachment: Mic_FFT_VGA_1f - Archive.zip]"

### SaucySoliton — 2024-01-14 20:39
"Here's a first try at an optimized FFT library based on Chip's code. Usable in flexprop. I haven't tested propeller tool. QROTATE is huge boost for FFT. It does sin(), cos(), 4 multiplies and 2 adds in as little as 8 clocks, provided the pipeline can be kept full.

New optimizations:
1. FIFO can read some of the data in the background.
2. Some instructions placed in wait interval between hub writes.
3. SKIPF bypasses cordic instructions when angle is zero.
4. Unrolled loop packs the cordic pipeline with 4 points at a time.
5. Bitreverse reads in order with FIFO and writes out of order.

I've tried not to grow the length of code too much. The unrolled loop processes 4 samples at a time. I have not done any tests to determine if that is the optimal number. The inline ASM version does not use the unrolled loop. From Chip's work it sounds like 16 points would be good.

```
fft_bench v1.2.1 for PROPELLER
OpenMP not available on this system
Freq.    Magnitude
           0      200
          c0      1ff
         140      1ff
         200      200
1024 point bit-reversal and butterfly run time = 2059 us  PASM
clock frequency = 160000000

1024 point butterfly run time = 1901 us PASM, with out of order outputs

1024 point butterfly run time = 3638 us inline ASM, with out of order outputs

Freq.    Magnitude
           0      1fe
          c0      1ff
         140      1ff
         200      1ff
1024 point bit-reversal and butterfly run time = 13625 us  flexc
clock frequency = 160000000
```

The C code in fftbench has real and imaginary data stored in separate arrays. I don't know if any of the compilers could improve performance if they were packed together. It's not quite apples to apples; the PASM bit reverser is an out-of-place algorithm (more memory required). The C bit reverser is in-place. The benchmarks exclude the QVECTOR on the final output.

I started working with inline assembler. There were a lot of limitations there like can't use ptra, can't use fifo, skipf can't jump over instructions if in hubexec, that I moved my development to a dedicated cog for now.

[Attachment: fftbench_asm01.zip]"

### evanh — 2024-01-14 21:42
"It suits to make it like a coprocessor anyway. It's a compute intensive process that is fine implemented as a concurrent task. Now we just need 16 cores for multiple FFT channels. :)"

### avsa242 — 2024-01-14 21:43
"This already seemed impressive at first, then I realized Chip was running his code at 250MHz and you're only running the above at 160. I tried it at 250 (default settings; didn't try any of the different variants) and got 1317usec. Nice :)

Cheers"

---

## Page 3

### Rayman — 2024-01-14 23:22
"@SaucySoliton did you find a way to make the 1024 point fft faster than what chip posted?
Sorry if I'm being slow…"

### evanh — 2024-01-15 00:08
"More than twice as fast, so far. Mainly from using the FIFO for data fetches and unrolling the inner loop to utilise the Cordic pipeline."

### SaucySoliton — 2024-01-15 01:54
"> Rayman said: @SaucySoliton did you find a way to make the 1024 point fft faster than what chip posted? Sorry if I'm being slow…

I posted a list of optimizations. I could have forgotten some.

For the same clock frequency, Chip's posted code was 3400-3600 uS. (It's not that variable, I just don't remember precisely and can't test it right now. It would be a bit faster than the inline version.) My FFT alone was 1900 uS. Then I added in bit reversal for comparison to fftbench. The alignment does affect performance by a few percent. Not quite double the speed."

### SaucySoliton — 2024-01-15 21:24
"Another performance boost has been unlocked! In many common use cases, the input to the FFT is entirely real data. So half of the input values are zeros. That's the imaginary part of the complex number input. Then we throw away half the output. No more! It is possible to pack all of the real number values in and process them as a complex FFT of half the size. Since the complexity of an FFT is N log(N), by halving N we more than double the speed. But there is some post-processing required which is comparable to another level of butterflies. So the log(N) term is unchanged while the N term is halved. So the time to process the FFT can be halved. That is reflected in the formula here: https://www.fftw.org/speed/

The post-processing does result in the output values being doubled compared to the usual.

```
fft_bench v1.2.1 for PROPELLER
OpenMP not available on this system
Freq.    Magnitude         I         Q
       0,     1024,     1024,        0
     192,     1023,     1023,        0
     256,     1024,     1024,        0
     512,     1024,    -1024,        0
1024 point bit-reversal and butterfly run time = 1188 us
clock frequency = 160000000
```

Based on this test the P2 scored 21.5 MOPS for the real FFT and 24.8 MOPS for the complex FFT.

[Attachment: fftbench_real01.zip]"

### evanh — 2024-01-15 21:41
"You just said real goes twice as fast. How come 21.5 vs 24.8 MOPS?"

### SaucySoliton — 2024-01-15 22:37
"The real FFT theoretically halves the operations and should theoretically run twice as fast. In practice, it's a really nice speed boost, but not quite double. The MOPS was calculated from the formula on the FFTW page. https://www.fftw.org/speed/ Most systems experience a reduction in MFLOPS when processing real data. It doesn't matter, we just want our desired transform to finish as quickly as possible.

2059 uS complex 1024 point with bitreverse

1188 uS real 1024 point with bitreverse and postprocessing

1022 uS for a 512 point complex fft and non-optimized bitreverse

978 uS for a 512 point complex fft and optimized bitreverse

899 uS for a 512 point complex fft no bitreverse

MOPS went down for the real version because of the extra post-processing. The post-processing for the real FFT version hasn't been optimized too much. Those cordic operations take a while."

### evanh — 2024-01-15 22:48
"Oh, so the 21.5 is actually 43 MOPS. Why are they halving it?"

### SaucySoliton — 2024-01-17 23:59
"> cgracey said: [quotes the 2019-12-20 02:39 post about the 1x512 last iteration set]

Found a solution for a bit reversed counter: Just manually change the bits with an XOR.

```
        setq    ay2             'rotate (bx,by) by angle
        qrotate ax2,angle       ' %000x...

        xor angle,##$4000_0000  ' %010x...
        add i3,#8               ' 2*fftsize*4
        setq    ay4             'rotate (bx,by) by angle
        qrotate ax4,angle

        xor angle,##$6000_0000  ' %001x...
        mov ax2,ax1
        setq    by2             'rotate (bx,by) by angle
        qrotate bx2,angle

        mov ay2,ay1
        xor angle,##$4000_0000  ' %011x...
        setq    by4             'rotate (bx,by) by angle
        qrotate bx4,angle

        mov angle,i3
        rev angle
```

The full counter and bit reverse runs once per loop. The XORs fit into the 4 butterfly unrolled loop perfectly. Of course, in practice you would store those constants in a long to avoid the AUGS penalty.

Posting here to back up my work. o:) Now a 1024 point real data FFT runs in 982uS ! At 160MHz

[Attachment: fftbench_real02.zip]"

### cgracey — 2024-01-18 05:35
"I had worked on a fast 1024-point FFT a few years ago and got it down to 700us at 250MHz. I hard-coded different parts of the butterfly to speed it up. I attached it here. It's part of a program which does microphone ADC, HDMI display, and FFT.

[Attachment: HDMI_Spectrum_Demo_Fast_FFT.spin2]"

### SaucySoliton — 2024-01-18 05:52
"> evanh said: Oh, so the 21.5 is actually 43 MOPS. Why are they halving it?

It's not doing 43 MOPS. From the formula on the FFTW page:

1024 point complex data requires 51,200 useful operations. (100%)

512 point complex data requires 23,040 useful operations. (45%)

1024 point real data requires 25,600 useful operations. (50%)

The useful operations counts the mathematical operations in the data path like multiplies and adds. It does not include stuff like loop counters, memory reads, and so on.

Now if you have 1024 points of real number data you certainly can use a 1024 point complex fft to process it. But the CPU will end up doing twice as many operations as compared to an optimal algorithm. The 1024 point real fft is based on the 512 point real fft. Then another level of processing is required. I've made massive gains by optimizing the assembly code. It was also very much worthwhile to use an optimal algorithm that eliminates 50% of the operations required."

### evanh — 2024-01-18 11:03
"Oh!!! I had that inverted. Here I was thinking MOPS was a speed measure (Mega Operations Per Second) when it's really a demand measure (Mega OPerationS)."

### SaucySoliton — 2024-01-19 06:23
"> cgracey said: I had worked on a fast 1024-point FFT a few years ago and got it down to 700us at 250MHz. I hard-coded different parts of the butterfly to speed it up. I attached it here. It's part of a program which does microphone ADC, HDMI display, and FFT.

Thanks, Chip!

Also, the simple version you posted years earlier was one of the things that helped me understand how an fft works. The cordic operations add just the right amount of abstraction. In most code you see a complex multiply as individual multiplies. Using some algorithm to do a complex rotate with 3 multiplies. It's easy to get lost there. I plan to include the simple version in the library for those who want to try to understand it.

It occurred to me tonight that the loops running bfly4, bfly2, and bfly1 are operating on the same data. So it works to call them all in the same loop. No need to write the data to hub ram in between. Sadly, that only saved 50uS. 1024 point real fft with ordered iq output takes 760uS at 160MHz. So 486uS at 250MHz. The bit reversal step is really starting to slow things down.

I don't really even need to keep optimizing the FFT but the ideas to speed things up keep coming. It's too much fun! I have an idea about how to split the work between multiple cogs. But first I want to squeeze as much performance out of one cog.

[Attachment: fftbench_real03.zip]"

### cgracey — 2024-01-19 19:57
"> SaucySoliton said: [quotes above]

Yeah, optimizations can go on and on. I was talking with Shannon Mackey the other day and I was telling him that because hardware optimizations exist in the P2 that enable software optimizations, you wind up playing chess instead of checkers, which can be taxing. If we had just simple instructions like AND, OR, ADD, SUB, SHR, SHL, and no CORDIC, it would be more straightforward to write code, but everything would be slow. He pointed out that if the hardware was simple, everyone's software efforts would result in the same solutions. So, it's not simple, but there's potential for lots of optimization. Enough to wear your brain out."

### Rayman — 2024-01-19 22:58
"Wonder if the shared LUT would help when using 2 cogs..."

### cgracey — 2024-01-20 04:48
"> Rayman said: Wonder if the shared LUT would help when using 2 cogs...

Maybe it could."

### bob_g4bby — 2026-01-08 21:33
"@SaucySoliton , how is your FFT code these days - have you made any more speed improvements? Did you try using more than one cog? I could do with a 1024 complex to complex FFT and inverse FFT for my dsp library.
Cheers, Bob"

### SaucySoliton — 2026-01-08 22:40
"IFFT isn't much different that FFT, but I just never got around to it. If this is something you would like I have some free time right now to work on it. I really need to clean it up and post to obex anyway.

The ironic thing is after doing all this work I found another FFT library https://forums.parallax.com/discussion/comment/1466754/#Comment_1466754 There is a fundamental difference. This library does the bit reversal first. (Decimation In Time)

The code in this thread does bit reversal last. (Decimation In Frequency) Usually the type of algorithm doesn't matter. If you are doing FFT filtering, the bit reversal step can be omitted.

How much speed do you need? The 1024 complex FFT is 1015uS at 160MHz without bit reversal. With bit reversal is 1220uS."

### bob_g4bby — 2026-01-09 06:28
"Thank you very much for offering to tidy up and obex the code. That would be great. Speed - I hope to run a software defined radio at 48 ksamples/s. With 1024 iq samples per buffer, that sets the main loop at 21.33 ms, or 42.66ms, or 63.99ms - at the expense of more buffers. So the fft times you mention would be acceptable. I aim to use as many cogs as I can to speed things up. I'm writing an inline assembly library - sine generator, modulator and mixer so far. Working on iq to polar and polar to iq at the moment. If I use two cogs with shared lut, should run at 14 cycles per iq sample.

Could the bit reversal step in the fft be run optionally to suit the application? Likewise windowing?

Best regards, Bob"

### bob_g4bby — 2026-01-09 06:50
"I'm copying the design of a software radio that first appeared a decade ago. The receiver main filter is calculated in the frequency domain as an fft fast convolution filter:-
1. Convert from time domain to frequency domain with fft
2. Frequency translate from an offset of 12khz to baseband IF of 0 Hz
3. Sideband selection
4. Generate the required bandpass filter coefficients, when user changes bandwidth. Apply Blackman-Harris windowing to this once, rather than the signal path all the time
5. Fft fast convolution filtering
6. Conversion back to time domain with ifft

I made a successful receiver in the language LabView, so reasonably confident about doing it on the P2, providing I reuse buffers as much as possible.

I forget whether reordering was used or not, hence my question about keeping it as a discrete method. I'll look that up in the code. I think it probably was. See article https://www.arrl.org/files/file/Technology/tis/info/pdf/021112qex027.pdf

The code I've written so far is demoed near the bottom of https://forums.parallax.com/discussion/176026/efficiently-processing-continuous-signals#latest I've standardised on buffers that store samples as two longs like real1, imag1, real2, imag2 - real1024, imag1024. It's best run in Spin Tools, where the Debug Scope windows are fast enough to keep up. Pnut doesn't keep up.

Cheers, Bob"

### Christof Eb. — 2026-01-10 08:39
"[quotes bob's 06:50 post]

Hi Bob
If you do FFT, then set most of the results to zero and then do IFFT, isn't this rather inefficient in comparison to directly using a filter, that does only calculate the desired result(s) like Goertzel algorithm? You could vary bandwidth modifying block length, as you could use any block length. I wonder, what inverse Goertzel would be, just generate sin and cos?
And second question: Why do you need to do IFFT at all? Is this not amplitude modulated signal anyways?
I understand that a complete FFT is interesting for a graphical display, but probably that does not need a high update rate?
Cheers Christof"

### bob_g4bby — 2026-01-10 11:18
"Hi @"Christof Eb." , good to hear from you - Happy New Year!

Good questions! I am no mathematician, but turn instead to a four part article written by Gerald Youngblood, the CEO of FlexRadio Systems. He claims that using an FFT Fast Convolution Filter gives a far superior filter performance to any FIR filter calculated in the time domain. The desirable filter features are flat top and almost vertical deep filter sides. The fast convolution filter done in the frequency domain is the equivalent of a many, many staged FIR filter in the time domain, taking far less time to compute and with much better filter shape. This is covered in some detail in part 3 of 'sdr for the masses' under 'Fast Convolution Filter Magic'. You can see the 'brick wall' shape of the filter that results. I've been using PC based radios based on this architecture for many years and can vouch for how pleasant they are to use - good quality audio, very good adjacent signal rejection, good signal to noise, absence of ringing even at 100Hz filter width for morse code and so on. I recommend reading the whole series (attached), he's very good at explaining the various design decisions.

Ham radio operators use morse code, lower single sideband, upper single sideband, AM (rarely), FM, and many digital modes. Single sideband is efficient for long distance weak signal performance, since one sideband and the carrier is not transmitted. So sideband selection is trivial to do in the frequency domain.

You're right, the graphical display doesn't need to be updated more than (say) 10-15 times per second for a smooth appearance.

At the moment, I have no clear idea how much of this design can be squeezed into 500 kbytes, but I'm willing to have a go. The development of an array based dsp library is probably of general interest to any audio programmer or signal analyst, so it's worth doing anyway. The hi-speed techniques used, e.g. dual cog with shared LUT, can be used in other applications. Also, so far, I'm surprised how small the dsp functions are when written in assembly language, which is encouraging.

Cheers, Bob

[Attachments: sdr for the masses part 1-4.pdf]"

### bob_g4bby — 2026-01-10 11:32
"Oh - and why not develop in Taqoz? I started out with Taqoz, but found having to transfer arrays to and from LabView on the PC a bit tiresome. So I turned to SPIN/PASM.
1. The debug scope windows are so easy to use and essential for debugging the dsp methods
2. The SPIN interpreter has a tiny footprint compared to the Taqoz system. Spin byte code is tiny / there is the option in Flexprop ide to turn it into machine code.
3. The PNUT or Spin Tools ide offer single shot through assembly code - very handy, no need to guess what's wrong
4. The assemblers flag many more errors than the Taqoz assembler
5. It was high time I learnt how to code in SPIN/PASM, to take advantage of the Obex and the friendly help avaiable.
I prefer and enjoy using Taqoz for some jobs, but not this one.
Cheers, Bob"

### Christof Eb. — 2026-01-10 14:41
"Thanks @bob_g4bby for the pdfs!
I am always learning in this forum.... So in this type of receiver a big number of bins is used and also a frequency shift.
When full speed is needed a compiler or assembler is better than Forth, ideally with good debugging possibilities.
Cheers Christof"

### SaucySoliton — 2026-01-15 05:44
"[quotes bob's questions]

The code could still use some cleanup. I just threw together a spin2 test program to see if the library compiled with something other than flexspin. Surprise! it didn't. The fft_ifft_cog.spin2 is a hastily patched version to get it working in Propeller Tool.

I didn't add an option to turn off bit reversal. I couldn't get the IFFT output to look anything like the FFT input without bit reversal. Each FFT or IFFT takes about 200,000 clock cycles. And that's with the silliness of restarting the cog every time. The frequency shift from 12khz to 0 would be complicated by trying to work on bit reversed data. So let's just leave bit reversal on for now. It should be possible to FFT, copy the desired bands, zero the undesired bands, and IFFT in 3 mS.

My library is "Bring Your Own Window."

```
    //           size + config , input arry, output arry    input array is modified!
    fft.cog_fft( FFT_SIZE      ,     bxy   ,     rxy ); // time domain -> frequency domain

    // frequency domain filter and value scaling
    for(i=0;i<FFT_SIZE*2;i++)  rxy[i]=i < 800 ? rxy[i]/FFT_SIZE : 0 ;

    fft.cog_fft( FFT_SIZE | fft.IFFT , rxy , bxy ); // frequency domain -> time domain

    fft.cog_fft( FFT_SIZE , bxy , rxy ); // FFT for spectrum analysis
```

Some of the runtimes in comparefftbench are inflated because the FFT is running 3 times. The 2 additional transforms don't seem to affect the results unexpectedly and spectrum mask seems to filter out unwanted frequencies.

[Attachment: ifftbench_beta1.zip]"

### bob_g4bby — 2026-01-15 08:21
"Thank you very much @SaucySoliton , "could still use some cleanup" is fine. Starting with code that works is the essential issue. Yes, I agree, the 12kHz shift wants frequency ordered results, so bit reversal on is essential for that step.

I have cartesian to polar and polar to cartesian working mice and fast. I'm working on a gain control method right now. Since qmul and qdiv don't handle signed words, I'll do the math in polar coords (since the magnitude of a signal is always positive - at least I hope so!)

Windowing - Gerald Youngblood took a novel turn on this. Instead of putting the windowing in the signal path, where it would have to be combined every buffer, he placed the windowing in the passband filter definition, where it only needs running once, when the user changes filter width.

I'll be trying your code out tonight - thanks again, Bob"

### bob_g4bby — 2026-01-16 03:57
"This demo of IFFT / FFT will run correctly under PNUT v52, and Spin Tools version 0.52.1. Start with ctrl-F10. The three scope windows displayed are:-
1. scope1 spectrum with two signals, two different frequencies
2. scope2 the inverse FFT is taken to show the signal waveform
3. scope3 the FFT is taken of the waveform to see if the same spectrum results
The scope3 spectrum is much bigger amplitude, which could be corrected by scaling if so desired.

[Attachment: fft_filter_demo with scope windows.zip]"

### Christof Eb. — 2026-01-20 16:32
"Hi,
stumbled over this interesting site: https://101-things.readthedocs.io/en/latest/breadboard_radio_part3.html
They use FFT filter too, but to prevent overflow do some scaling during FFT:
" During the forward FFT, a growth of 256 can occur. With no scaling at all, a sin wave with an amplitude of 16 in the time domain would result in a peak with a magnitude of 4096 in the frequency domain. Various scaling strategies can be employed in an FFT to allow for this growth.

Scaling by a factor of 2 after each stage is safe and prevents any possibility of overflow. The downside of this approach is that we truncate the lowest 8 bits of the output data, 4 of these bits contain useful data and 4 contain noise.

To preserve as many useful bits as possible, a smaller scaling factor is used in this design. Scaling by a factor of 2 after every second stage means that we truncate by 4 bits overall, losing only the bits that contain noise. This means that there is a possibility of overflow under worst-case conditions if the input data exceeds 12 bits."
Cheers Christof"

### bob_g4bby — 2026-01-20 17:36
"What an interesting project, @"Christof Eb." ! The animated graphs make a lot of the techniques so clear. Plenty of integer dsp ideas there, showing it should be possible on a P2 as well. I'm enjoying getting each dsp method running, the debug Scope windows confirming whether I've got it right, or there's still a bug to fix. The Scope and other windows must be unique to Propeller, I think. They save having to write so much tedious test harness.

Overflow is an issue with integer dsp, so I've written an "atten" method which divides the signal amplitude by an integer. Useful as a volume control too. I might change that to an integer / 10 if necessary, for finer control. None of my methods have overflow detection built in, but it would be easy to fit."

### SaucySoliton — 2026-01-31 23:34
"I think I have the cleanup done. Also:

*   Faster bit-reversal, about 4% faster FFT and IFFT.
*   Selectable in-place mode, saves memory at the cost of some speed.
*   Inline PASM2 version split off into separate file. Was necessary to compile with PNut. Or I could have changed variable names, but I didn't see a reason to put both the dedicated cog and inline version in one file.
*   Functions are renamed. Sorry.
*   NEW! Non-blocking API so the main spin2/C cog can do other work while waiting for the FFT.

This will go into the obex once my account is approved.

```
1024 point butterfly run time = 1018 us FFT ONLY, no bit reversal
1024 point bit-reversal and butterfly run time = 1328 us IFFT In-Place Algorithm
1024 point bit-reversal and butterfly run time = 1297 us In-Place Algorithm
1024 point bit-reversal and butterfly run time = 1204 us IFFT was 1275uS
1024 point bit-reversal and butterfly run time = 1174 us Out-of-Place Algorithm, was 1220uS
1024 point bit-reversal and butterfly run time = 664 us Real Input
1024 point bit-reversal and butterfly run time = 3764 us Inline
1024 point bit-reversal and butterfly run time = 12991 us flexcc -2 comparefftbench.c -O3
```

IFFT is a bit slower than FFT by 2.5%. The IFFT is implemented as an FFT with the inputs and outputs conjugated. I felt this was an acceptable trade-off between speed, library size, and development effort.

[Attachment: libfft-p2-rc1.zip]"

### bob_g4bby — 2026-02-02 09:17
"An excellent piece of work James, should do much to encourage folks to dsp with P2. Impressed you managed to squeeze a little more speed out of it. Thank you very much, Bob
--- I'm now reading up on windowing (Blackman-Harris is popular for software defined radios) and bandpass filter coefficient generation with a view to writing the receiver filter."

---

## Page 4

### bob_g4bby — 2026-02-03 09:44
"Here's the Blackman-Harris window produced in a spreadsheet - what's the best way of applying it to a signal in the 32 bit integer environment of the P2?

[Image of window function]

A question of scaling the function up? Large enough to retain as much precision as possible, consistent with avoiding overflow when multiplying the signal, sample by sample.

The scaled window is a constant, so it's a DATA block to be loaded into a buffer on start up, I guess.

[Attachment: blackman harris window.xls]"

### TonyB_ — 2026-02-03 12:22
"> @bob_g4bby said: Here's the Blackman-Harris window produced in a spreadsheet - what's the best way of applying it to a signal in the 32 bit integer environment of the P2?

The best you could do with the CORDIC QMUL is one sample every 16 cycles. Your Blackman-Harris window length is 1024 samples with 512 different values so the obvious place to store them is LUT RAM. Will successive windows overlap by 512 samples?

Data could be read from hub RAM using RFLONG with 256 results, say, stored temporarily in reg RAM then written back later using fast block write. Alternatively, do fast block read to pre-load 256 samples in reg RAM and write results directly to hub RAM using WFLONG. Or use RFLONG and WRLONG (but the former might stall the later) with no intermediate storage in reg RAM if timing allows for that."

### bob_g4bby — 2026-02-03 14:12
"Good idea, LUT ram is the best place and like you say, the window is symmetric, so storing half of it is enough.
Yes, the FFT fast convolution filtering that comprises the software defined radio main filter does include an overlap-add feature - see attached pdf

I've got the dsp functions going quite fast as follows:-
1. Move 16 iq pairs from the input buffer in hub ram into a small register array using SETQ #31, RDLONG regarray, ptra++. This takes 1 cycle per long.
2. Preload the cordic engine with 8 inputs from the register array.
3. Read result back from cordic into register array and load the cordic engine with another input - do this 8 times
4. Read the last 8 results from the cordic engine back into register array. For many dsp functions (2) to (4) results in around 9 cycles per cordic result
5. Move 16 iq pairs from register array back to the output buffer in hub ram. This again takes 1 cycle per long.
6. Repeat (1) to (5) 64 times for the whole buffer

Here's an example, with timing based on Chip's example (Overlapping CORDIC commands to maximize throughput):-

```
' convert x,y (cartesian) samples in buffin to magnitude, angle (polar) samples in buffout - optionally, buffout can be the same as buffin
' at 320MHz clock, runs about 56.1uS
' result stored as mag1, real1, mag2, real2 etc.
pub xytopol(buffin, buffout) | counter

    org
        push ptra
        mov ptra, buffin
        mov ptrb, buffout
        mov counter, #(sigbuffsize/16)
xypol1
            setq #31
            rdlong array, ptra++
            qvector array, array+1
            nop
            qvector array+2, array+3
            nop
            qvector array+4, array+5
            nop
            qvector array+6, array+7
            nop
            qvector array+8, array+9
            nop
            qvector array+10, array+11
            nop
            qvector array+12, array+13
            nop
            qvector array+14, array+15
            getqx   array
            getqy   array+1
            nop
            qvector array+16, array+17
            getqx   array+2
            getqy   array+3
            nop
            qvector array+18, array+19
            getqx   array+4
            getqy   array+5
            nop
            qvector array+20, array+21
            getqx   array+6
            getqy   array+7
            nop
            qvector array+22, array+23
            getqx   array+8
            getqy   array+9
            nop
            qvector array+24, array+25
            getqx   array+10
            getqy   array+11
            nop
            qvector array+26, array+27
            getqx   array+12
            getqy   array+13
            nop
            qvector array+28, array+29
            getqx   array+14
            getqy   array+15
            nop
            qvector array+30, array+31
            getqx   array+16
            getqy   array+17
            getqx   array+18
            getqy   array+19
            getqx   array+20
            getqy   array+21
            getqx   array+22
            getqy   array+23
            getqx   array+24
            getqy   array+25
            getqx   array+26
            getqy   array+27
            getqx   array+28
            getqy   array+29
            getqx   array+30
            getqy   array+31
            setq #31
            wrlong array, ptrb++
            djnz counter, #xypol1
        pop ptra
        ret

array res    32

    end
```
"

### TonyB_ — 2026-02-03 16:02
"[quotes bob's xytopol code]

The `NOP`'s between the `QVECTOR`'s are not necessary, I think. Re window coefficients in LUT RAM, the 3 cycle `RDLUT` could be an issue for CORDIC pipelining and it might be quicker to keep some of them in reg RAM and swap them in and out as required."

### Wuerfel_21 — 2026-02-03 16:27
"> @TonyB_ said: The `NOP`'s between the `QVECTOR`'s are not necessary, I think.

Not needed. CORDIC ops automatically insert waitstates so they're spaced a multiple of 8 cycles apart"

### bob_g4bby — 2026-02-03 18:35
"That's very interesting, I'll take the nops out, thanks both! RDLUT issue noted too."

### TonyB_ — 2026-02-03 19:27
"> @bob_g4bby said: That's very interesting, I'll take the nops out, thanks both! RDLUT issue noted too.

You could put up to 3*7=21 normally two-cycle but effectively zero-cycle instructions between 1st and 8th `QVECTOR`. I'll be interested to see your windowing code, whenever that may be."

### SaucySoliton — 2026-02-27 07:54
"I made a huge breakthrough on the bit-reversal that is a usual part of doing an FFT. The bit-reversal code in the last update took 160uS. This new code does digit-reversal in 50uS, when combined with other parts of the FFT.

Radix-4 FFT need digit reversal instead of bit reversal. For radix-4, digits are 2 bits. Thankfully with the P2's bit shuffling instructions it's only 3 extra instructions. This is still a lot of instructions for reading a single sample.

```
        rdfast  c_8000,ptrr
        add     i1,#1
        mov     next_ptrr,i1
        splitw  next_ptrr  *
        rev     next_ptrr
        rol next_ptrr,shift  *
        mergew  next_ptrr  *
        shl      next_ptrr,#3
        add     next_ptrr,real_imag_ptr
        rflong  ax+A
        rflong  ay+A
```

Let's look at what the digit reversal does.
[Image]

The XOR trick I used previously won't work for addressing data because we can't assume that the arrays are aligned to their size. The carries would happen at different times depending on the array starting address. If we look at the differences between addresses we see that it follows a regular pattern. The current address can be adjusted to the next address with only a single ADD. After 16 samples there are additional bits rolling over. It's not a big deal. We just need to run the full digit reversal calculation to deal with this. The same method could be applied to bit-reversal as well, but will require more unique step sizes.

Of course the FIFO takes time to read from the hub. This wait time can be filled with the next address calculation or butterfly operations.

Combined with the greater computational efficiency of the radix-4 FFT, a complete 1024 point transform happens in 870uS. That is an unbelievable 25% reduction from the previous 1175uS. All times at 160MHz.

Sorry, flexspin only right now.

[Attachment: cog_fft_radix4.spin2]"

### TonyB_ — 2026-02-27 14:00
"> @SaucySoliton said: [quotes breakthrough post]

Good work!

Re your code:

```
                setnib  .dit4ret,#%0000,#7    ' set condition to _ret_
'...
                setnib  .dit4ret,#%1111,#7    ' set condition to always
```

changing the instruction prefix from `always` to `_ret_` is an interesting way of converting plain code into a subroutine. The drawback is that another instruction is needed to reverse the change. Quite often in skip sequences I create a routine by duplicating an instruction but with a `_ret_` prefix and which is always skipped. This adds only one long although it does require skipping to be active."

### SaucySoliton — 2026-02-27 18:41
"> @TonyB_ said: Good work! [...]

Thanks!

The call/return happens 64 times. It runs inline 64*3 = 192 times. The called section is 154 instructions so it would be nice to not duplicate that.

```
if_c   ret       '  would be 2 cycles if not returning,   4 cycles if returning
 _ret_  sub  ay,cy    ' 0 cycles if not returning,   2 cycles if returning
```

Due to hub and cordic alignment saving 2 cycles might cut 8 cycles off the loop.

I came up with another way of trying not to branch within the loop. The return address for djnz can be patched return to different locations.

```
            testb   p_fft_flags,#NOBR_BIT wc
        ' patch the loop return location to reduce time penalty for
        ' selecting which read method to use.
        ' only 3uS difference.
    if_c    sets    .first_loop_end,#(.seqread_dit - .first_loop_end -1 )&$1ff
    if_nc   sets    .first_loop_end,#(.randread_reorder - .first_loop_end -1)&$1ff
.first_loop
    if_nc   jmp #.randread_reorder


.seqread_dit    setq    #32-1
                rdlong  ax,ptra++
                jmp #.bfly1

.randread_reorder
...  ' this code mutually exclusive with .seqread
.bfly1
...  ' this code always runs
.first_loop_end djnz    flight_count,#.first_loop
```

This isn't in the uploaded code. After unrolling the randread function, most of bfly1 became dispersed between fifo reads. It was simpler just to go to 2 separate loops."

### bob_g4bby — 2026-02-27 19:01
"That's a very worthwhile gain in performance - can't wait to adopt your code. I've been reviewing fft fast convolution filtering and I've made spin code that creates the required bandpass filter impulse response. A small windows based software radio has been modified to supply an analogue iq signal which is converted to 48ks/s signal buffers in the P2 via an HDaudio kit. Spin Tools writes a single debug scope window fast enough to keep up with the signal, which is really useful. I've just written an 8x knobs driver to control signal settings later on.
Much appreciated, bob"

### SaucySoliton — 2026-03-01 06:49
"https://obex.parallax.com/obex/fft-ifft/

Fair warning, the new library might invert your spectrum. I think the issue can be corrected by inverting the IFFT flag from how it used to be.

The new library does not modify the input data array. That might save some time. It think it's possible to modify the input section to read directly from a circular buffer.

For FFT filtering, I still think it is possible to filter without doing any bit reversals. It would go like this:

time data -> DIF FFT -> digit reversed frequency data -> DIT IFFT -> time data

The transformed data would not even need to be written to hub ram. The filter coefficients could be digit reversed once after they are generated. However, given the massive improvements to the bit reversal section I'm not sure it's worth trying to do that.

I found a page that suggested the Inverse FFT could be computed by reversing most of the input array. The new input section could accommodate that at minimal cost. It didn't work quite right. It looked like a bad window function that allowed energy from the peaks to spread across the spectrum. This doesn't show what I saw but it's a good explanation. https://www.katjaas.nl/inverseFFT/inverseFFT.html The ARRL handbook did not mention the reversal method, maybe they know. So, back to conjugating the input and output data."

### Rayman — 2026-03-09 23:02
"Thinking about 2D fft on fft vs time for wake word identification …. This should help.."

### Rayman — 2026-03-09 23:08
"Think need to do on PC first to optimize .

Guess need to figure out how to do this kind of fixed point in C++"

### bob_g4bby — 2026-03-16 10:08
"@SaucySoliton , Here are two fft tests. 'fft test 1.spin2' uses the inline fft, 'fft test 2.spin2' uses the radix 4 fft. Test 1 shows a swept sinewave and the resulting spectrum - looks normal. Test 2, the spectrum bobs up and down in an unexpected way. Have I misused the radix 4 method, or is there a bug? I notice the spectrum inversion - I've adjusted the debug PLOT so both spectrums appear normal - 0Hz on the left. Please run both tests under Spin Tools with debug enabled.
Cheers, Bob

[Attachment: fft tests.zip]"

### SaucySoliton — 2026-03-17 04:53
"I've not been able to get spin tools to work. I did build the tests with pnut-ts and run them in pnut-term-ts. I did see the amplitude change. The reason for that may be that the scope is showing the input to xytopol instead of the output.

I've quietly uploaded a mixed-radix fft to the obex. The mixed-radix version adds a radix-2 stage onto the radix-4 fft in the case the size is not a power of 4. If you are using a 1024 there no reason to change.

Also I wrote a new fft accuracy tester in spin2. It's in the obex. The fft libraries are tested against a discrete Fourier transform which still uses the cordic. The DFT is simple enough that it's unlikely I made a mistake with it, plus the results match the other FFT functions. With the exception of the phase rotation direction issue. If you are concerned with only the magnitudes of a real-input signal, as was the original use of Chip's code posted here, there is no difference. My newer libraries are designed to use either direction rotation as that is the fastest way to compute IFFT."

### bob_g4bby — 2026-03-17 09:32
""the scope is showing the input to xytopol instead of the output" - phew! sorry for ringing a false alarm bell - having fixed my bug, it's identical to the radix 2 again. Your test against DFT reminds me that some of the railway signalling kit I EMC tested had two identical microprocessors in them which had to cooperate to control the railway. The two channels had to employ two different versions of firmware using only certain instructions in each, so that there was little chance of a common mode bug getting through. If they ever disagreed, they would blow an internal fuse!

I've started timing the dsp code sections and all looks well - 48ksample/s dsp based on in-line pasm methods is a viable technique and I'll use the radix-4 fft from now on. Spin2 byte interpreter speed has been a pleasant surprise - I imagined it to be far slower than Taqoz forth, but it isn't and occupies far less space.

Cheers, bob"

### SaucySoliton — 2026-05-26 06:03
"I thought maybe I could put my LameStation to work for a spectrum analysis project. Would just need an FFT for P1.

PASM2 isn't that different from PASM, we just need to replace the CORDIC. How about with a software CORDIC? After 31 cordic stages the shifted terms will round to zero, as well as the angle.
[Images]

I think it can be done in 7 instructions per stage if unrolled. The P1 will take about 210 instructions or 840 clocks to replicate QROTATE without any scaling. I figured I could just use unscaled cordic operations and scale it all at the end.

A QROTATE needs 8 clock cycles on the P2, if there is enough other work to fill the latency. P2's higher clock rate it's 200-400x faster. So depending on the instruction mix the P1 FFT would be somewhere between 4 and 200 times slower. Thus a 1024 FFT could take as long as 176mS.

Heater's FFT takes 25mS. https://forums.parallax.com/discussion/128292/heaters-fast-fourier-transform I'm glad I searched before writing any code."

### Christof Eb. — 2026-05-26 18:38
"In Chips speech synthesis for P1 he used a software cordic with very carefully chosen number of bits resolution."
