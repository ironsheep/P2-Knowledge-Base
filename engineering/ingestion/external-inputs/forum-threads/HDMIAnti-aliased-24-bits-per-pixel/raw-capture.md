# Raw Capture — Anti-aliased 24-bits-per-pixel HDMI

Source: https://forums.parallax.com/discussion/175725/anti-aliased-24-bits-per-pixel-hdmi
Thread ID: 175725 · Pages: 3 · Fetched: 2026-07-01

---

## Page 1

### cgracey — 2024-02-14 08:53
I've been working on graphics for the P2, using the P2-EC32MB Edge module.

The PSRAM buffers 960x540 screens at 24bpp for a really nice picture over HDMI. The resolution isn't super high, but it looks surprisingly good with anti-aliasing.

I took the anti-aliased line-draw routine I made for the PC that the DEBUG displays use and got it running on the P2.

To try this code, you'll need a P2-EC32MB module and the DIGITAL VIDEO OUT board which connects 8 pins to an HDMI connector. I will talk about this on the live Propeller Forum tomorrow.

https://drive.google.com/file/d/1UVdZ3K8Q_14O703ysN0Moq1a7pkLBiCz/view?usp=sharing

Next, I want to make a triangle renderer with a Z buffer for 3D graphics.

With the "qHD" mode, or quarter-HD, we'll be able to show really nice anti-aliased fonts and graphics at the same time.

### cgracey — 2024-02-14 09:08
Here are some colored lines. These are 1.5 pixels wide. The anti-aliased line draw has 8 sub-bits for each X, Y, and diameter. So, lines can be placed in X and Y at offsets of 256ths of a pixel. Line diameter is similar, but gets halved to make a radius in 256ths of a pixel. The minimum diameter is $100, or 1 whole pixel.

![](https://forums.parallax.com/uploads/editor/9j/dplcbq2lna0d.jpg)

### rogloh — 2024-02-14 10:41
Is there a simple way to get it to build with flexspin or does it need to be PNut only? I was hoping to run this demo on my Mac however I immediately encountered two problems when I tried to build with flexspin...

1. "repeat x with y" needed patching to the old "repeat y from 0 to x-1" - was simple to fix
2. setregs doesn't appear to be implemented - I'll need to go check the latest version's release docs etc as I'm still on 6.2 beta but it's probably related to management of variables held in COGRAM which I suspect still differs significantly between flexspin and PNut.

Propeller Spin/PASM Compiler 'FlexSpin' (c) 2011-2023 Total Spectrum Software Inc. and contributors
Version 6.2.0-beta-v6.1.7-2-g588815b8 Compiled on: Jun 15 2023
LineDrawAntiAlias.spin2
|-PSRAM_driver.spin2
|-HDMI_960x540_24bpp.spin2
LineDrawAntiAlias.spin2:131: error: syntax error, unexpected '#'
LineDrawAntiAlias.spin2:137: error: syntax error, unexpected '#'

Maybe I'll just have to wait to get some form of Windows running again...I am planning a dual boot MacBook Pro setup in time with a newer larger SSD fitted once I get to opening the thing and installing it.

### evanh — 2024-02-14 11:45
> @rogloh said:
> 2. setregs doesn't appear to be implemented - I'll need to go check the latest version's release docs etc as I'm still on 6.2 beta but it's probably related to management of variables held in COGRAM which I suspect still differs significantly between flexspin and PNut.

Looking at LineDrawAntiAlias.spin2 I see a large DAT section starting with ORG with all RES declares then everything else is ORGH. I'm not sure what Flexspin will make of a DAT section like that but if it compiles that section then it shouldn't be hard to then make a SETREGS like function to match.

> Maybe I'll just have to wait to get some form of Windows running again...I am planning a dual boot MacBook Pro setup in time with a newer larger SSD fitted once I get to opening the thing and installing it.

Pnut, unlike Proptool, runs on Wine fine. It even does the full debug features.

### evanh — 2024-02-14 12:48
Chip,
Your hblanking is way too short! I've found 80 to be about the minimum.

PS: I've got it working via Wine. The no-picture had me scratching my head for a while though. Had to double check each part of of the setup before discovering you had the horizontal blanking at only 16!

### Wuerfel_21 — 2024-02-14 12:59
> @rogloh said:
> 1. "repeat x with y" needed patching to the old "repeat y from 0 to x-1" - was simple to fix

That I'm pretty sure is in there, just the current version.

> @cgracey said:
> To try this code, you'll need a P2-EC32MB module and the DIGITAL VIDEO OUT board which connects 8 pins to an HDMI connector.

Will need to make a VGA patch... Though the monitor I've been using is kinda dying. I got a fancy new capture card that could do HDMI, but ran into some medium driver issues. So bad monitor situation currently.

> @cgracey said:
> Next, I want to make a triangle renderer with a Z buffer for 3D graphics.

My research on the topic has actually led me to believe that doing higher convex N-gons directly can be faster than just triangles. The setup is somewhat more complex, but that gets made up for when you draw a quadliteral in one go (instead of two triangles drawing adjacent spans). That also makes clipping easier - when the tip of a triangle pokes outside the screen, clipping actually turns it into a quadliteral. I think the worst case is a hexagon when all three tips are copped by different clip planes. Of course clipping a quad can turn it into an octagon, but there really isn't a difference between rasterizing quads vs octagons. Just need to iterate through more vertices. Though interpolating values across the face is somewhat more complicated (need to recalculate scale factor per scanline) but would generally be nicer than an affine transform. I think perspective-correct interpolation needs per-scanline work, anyways, so maybe it doesn't matter there. I really haven't fully worked it out, either.

### VonSzarvas — 2024-02-14 16:22
> @cgracey said:
> ![](https://forums.parallax.com/uploads/editor/9j/dplcbq2lna0d.jpg)

Is there a message in there Chip?
Stare long enough, and it seems to suggest... "don't touch the lonely red line" :smiley:

### cgracey — 2024-02-14 19:02
> @evanh said:
> Chip,
> Your hblanking is way too short! I've found 80 to be about the minimum.
>
> PS: I've got it working via Wine. The no-picture had me scratching my head for a while though. Had to double check each part of of the setup before discovering you had the horizontal blanking at only 16!

Yeah, I found that on my TV it could be set minimally, in order to get to 60Hz refresh.

All this timing was carry-in from the analog era. It seems that most of it can be squeezed out in HDMI. Sorry it was too short for your TV. I don't know what the minimum really is. This resolution was standard on many cell phones 12 years ago, but has since been eclipsed by higher resolutions.

### cgracey — 2024-02-14 19:09
> @Wuerfel_21 said:
> [quoting rogloh and cgracey re: repeat, VGA patch, N-gons vs triangles]

Yeah, it seems quadrilaterals would be fine. Even triangles typically get broken into TWO triangles at rendering, so that each begins and ends on a common Y. A section identical to the screen memory can be maintained in the PSRAM to act as a per-pixel Z buffer. Only nearer pixels get written to the screen memory and the corresponding location in the Z buffer is updated with the new distance. By alpha-blending the polygons onto the screen, I think it would look pretty good.

### Rayman — 2024-02-14 19:16
Neat stuff. FTDI's EVE series does subpixel stuff like that. This could be something I'd use with 7" hdmi tfts

3D would be neat for accelerometer and or IMU display…

### Wuerfel_21 — 2024-02-14 20:15
> @cgracey said:
> Yeah, it seems quadrilaterals would be fine. Even triangles typically get broken into TWO triangles at rendering, so that each begins and ends on a common Y.

One can do it like that, but you end up splitting the long edge then. It's better to think of "which side will need a new vertex next" and then grab the next one up/down (depending on wether you're loading a right or a left vertex) and then recalculate that edge only. This all needs a bit of thought since you can go through multiple vertices without crossing an integer scanline boundary where you'd actually get to draw anything.

> A section identical to the screen memory can be maintained in the PSRAM to act as a per-pixel Z buffer. Only nearer pixels get written to the screen memory and the corresponding location in the Z buffer is updated with the new distance. By alpha-blending the polygons onto the screen, I think it would look pretty good.

It's either or. Blending and Z-Buffer don't mix, because you can't meaningfully render behind something that's already been drawn with semi-transparency. [...full discussion of ordering tables, BSP trees, PS1/Saturn ordering table, Quake edge-sorting...] tl;dr; approaches to 3D graphics are infinite in number and infinitely interesting.
![](https://forums.parallax.com/uploads/editor/ii/rlu1ilrhek83.png)

### cgracey — 2024-02-14 20:37
Wuerfel_21, I didn't say what I meant quite right. I know that alpha-blending whole polygons is impossible without Z-ordering per pixel. I meant to say that I would blend the edges, as in anti-alias them. I don't think this would have any detrimental effect. All polygons would be considered opaque, but the edges might as well get blended to reduce jaggies.

### Wuerfel_21 — 2024-02-14 21:09
There's no difference though - the weird effect would be isolated to the edges, but you _always_ get artifacts if you do something that reads the color underneath _at all_.

### evanh — 2024-02-14 21:36
> @cgracey said:
> Yeah, I found that on my TV it could be set minimally, in order to get to 60Hz refresh.
> All this timing was carry-in from the analog era...

Yeah, I don't know what is a safe generalised minimum either.

As for the resolution, in DVI/HDMI there's no restrictions on selection other than multiples of 8 for horizontal and obviously there is a max resolution supported.

You could choose a resolution from the desired dotclock and refresh: Start with 32 MHz and 60 Hz. 32e6 / 60 = 533e3 total dot area, sqrt = 730, x 1.333 = 974 htot, - 80 hblank = 894, round = 896 hres, / 1.78 = 504 vres.

Interestingly, tweaking these, I find my TV is good down to 60 hblanking here. I'm not sure how I figured 80 as the minimum to be honest.

EDIT: So, redoing it at hblank = 60: ... 974 htot, - 60 hblank = 914, round = 912 hres, / 1.78 = 513 vres.

Of course, 960x540 works fine at 56 Hz refresh too.

### evanh — 2024-02-14 22:29
Huh, never expected that. My TV is also fussy about the vertical back porch (top blanking lines). It needs a minimum of 9 lines there. I had been unsure about where to place the vsync, so.it looks like there's more leeway when it's at the beginning of the blanking.

Roger,
Need more allocated bits for this in your timings structure!

### evanh — 2024-02-14 22:58
Here's an example using the tightest DVI/HDMI blanking timings for my TV:

 Sysclock freq = 320 MHz   Dotclock freq = 32.0 MHz
 Hres=1280  hfp=4 hsync=52 hbp=4  Htot=1340   Hfreq = 23881 Hz
 Vres=640  vfp=1 vsync=2 vbp=9  Vtot=652   Vfreq = 36.6 Hz

EDIT: It also seems to be happy to accept up to 75 Hz refresh rate but I know other monitors I have top out at 60 Hz refresh.

 Sysclock freq = 172 MHz   Dotclock freq = 17.2 MHz
 Hres=640  hfp=4 hsync=52 hbp=4  Htot=700   Hfreq = 24571 Hz
 Vres=320  vfp=1 vsync=2 vbp=9  Vtot=332   Vfreq = 74.0 Hz

EDIT2: Uh-oh, so the vblanking has more complexity here. It can go lower when the vres is lower... The 640 vres didn't need any more blanking ... and 640x800 is fine too ... 640x1080 also good. That's the max vertical.

### rogloh — 2024-02-15 00:02
[re repeat/setregs, out of date] ... I just need to call the smoothline function from Spin somehow - or make it inline.

> @evanh said: ... Need more allocated bits for this in your timings structure!

LOL, your favourite bugbear. How many bits do you need for it?

Speaking of timings I temporarily commented out the DAT PASM section in Chip's demo code and hacked in my own smoothline function for flexspin to use without the anti alias stuff and found my resurrected Dell2405FPW did accept the timings. They are tight! 16 pixels of horizontal and 9 lines of vertical blanking with a 960x540 active area at 60Hz. Cool.
![](https://forums.parallax.com/uploads/editor/ei/3t1aly675mwx.png)

Amazing you can get something with this little blanking going. No way it works with VGA at this rate, it needs more blanking for that. My own video driver certainly wouldn't be able to do this little horizontal blanking due to its other housekeeping code required in this interval, like issuing external memory reads and loading in palettes to LUTRAM etc. Also, I found it didn't sync at all on another 17 inch TFT I have though (Samsung B1740). So not all monitors are going to like this signal.

### evanh — 2024-02-15 00:48
> @rogloh said: LOL, your favourite bugbear. How many bits do you need for it?

I'll get back to you on that. I want to allow space for VRR in the vertical allocations.

> ... They are tight! 16 pixels of horizontal and 9 lines of vertical blanking with a 960x540 active area at 60Hz. Cool.

I think Chip might have it at just 8 lines blanking. Isn't the single first line also the sync? ie front porch = 0.

And that 8 works for me. Just had to up the hblanking to 60.

> ... My own video driver certainly wouldn't be able to do this little horizontal blanking...

Oh, I was using your driver in my testing above ... I still need the hblanking of 60 but I can reduce the vblanking further using Chip's driver. So blanking of 60x8, instead of 60x12, works now. Not sure of other resolutions, Chip's program needs 960x540 specifically.

### rogloh — 2024-02-15 02:13
> @evanh said: I think Chip might have it at just 8 lines blanking. Isn't the single first line also the sync? ie front porch = 0.

Just double checked the code, yes you are correct. It's just 8 vblank lines total including the sync.

### cgracey — 2024-02-15 06:06
> @rogloh said:
> Just double checked the code, yes you are correct. It's just 8 vblank lines total including the sync.

Yeah, it's one vsync line and seven blanks. I need to know how tight this can be safely pushed. Ada said today that we need something like 34 total horizontal blank pixel periods to accommodate data packets for sound.

It would be good to know exact numbers.

### evanh — 2024-02-15 10:33
An old Dell U2412M DVI monitor (My first LCD monitor) wants minimum hblank of 68. But it's a lot fussier about resolution options too. More like how VGA inputs work. Ah, uh-oh, the tight timings only seems to work for modes that weren't a VGA type mode. Basically, it's rubbish at adjusting even though it could do so easier than the fixed modes list it has been programmed with.

So it looks like the fully flexible resolution detection is actual a newish (last ten years or so) ability of monitors and TVs.

### evanh — 2024-02-15 10:56
Maybe that came along with firmwares that supported HDMI. Dunno.

### pik33 — 2024-02-15 17:48
Here are my timings for 1024x600@50 Hz:

'                      bf.hs, hs,  bf.vis  visible, up p., vsync, down p.,  cpl, total lines, clock,       hubset                                scanlines  ud bord mode reserved
timings         long   8,     60,  8,       1024,   7,     4,     1,        128, 600,         340500000,   %1_100111__10_1010_1000__1111_1011,   600,        0,     192, 0, 0

76 pixel horizontal, 12 lines vertical.

It worked on what I managed to connect to the P2...

### TonyB_ — 2024-02-15 21:23
How low could sysclk go for 960x540 @ 50Hz? (I don't have the Digital Video Out board.)

### pik33 — 2024-02-15 22:32
> How low could sysclk go for 960x540 @ 50Hz?

If similar to my 1024x600 sync timings are used, something about 290 MHz.

### evanh — 2024-02-16 00:04
Chip's timings: 50 x (540 + 8) x (960 + 16) x 10 = 267.424 MHz
Evan's timings: 50 x (540 + 8) x (960 + 60) x 10 = 279.48 MHz
Pik's timings: 50 x (540 + 12) x (960 + 76) x 10 = 285.936 MHz

PS: Pik's timings will provide the most universal coverage. That'll suit my old Dell because it's not a recognised VGA mode and therefore it'll accept reduced blanking.

### rogloh — 2024-02-16 01:50
I was able to modify Chip's code slightly to run on flexspin to see this demo on my Mac. :smile: It just runs a seperate COG and waits for a command to occur via a cmd mailbox. Quick hack for now. [...attaches LineDrawAntiAlias.spin2, notes uncleared top scan line = COG startup timing; adding 1sec delay fixes it...]
[LineDrawAntiAlias.spin2] 15.3K

### evanh — 2024-02-16 03:08
Replacing the REPEAT with the WAITMS worked for me.

  coginit(NEWCOG, @gfxcog, @cmdbuf)
'  repeat while cmdbuf\[0\]
  waitms(1)

Which suggests the REPEAT isn't working.

### rogloh — 2024-02-16 03:30
I found it happens earlier on and it needs a 1ms wait after the hdmi COG is spawned before the first PSRAM clearing write access can occur. Still not entirely sure why. EDIT: One possible theory is that it could be priority related if the HDMI COG is spawned while a large PSRAM write is underway and the video COG's PSRAM initial reads are delayed and get out of sync with the scan line being rendered. Unlike my driver there is no priority for video COGs and fragmentation for non-realtime COGs in Chip's PSRAM driver, which could cause problems like this.

PUB start()

  psram.start()

  hdmi.start(0, psram.pointer(), 0)
  waitms(1)  '  <<<  adding this fixes graphics issue with first scan line

  psram_ptr := psram.pointer() + cogid() \* 12

  mapbase := 0
  pixeltype := @smooth_pixel1

### pik33 — 2024-02-16 07:24
> Chip's timings: 50 x (540 + 8) x (960 + 16) x 10 = 267.424 MHz

16 horizontal? I had problems even at 60 with several monitors.

### evanh — 2024-02-16 07:37
> @pik33 said: 16 horizontal? I had problems even at 60 with several monitors.

Were those all using DVI/HDMI links?

---

## Page 2

### pik33 — 2024-02-16 08:27
Yes, they were. I tried to get stable 1024x600 . The calculator ( https://tomverbeure.github.io/video_timings_calculator ) for CVT-RBv2 gives 18 lines for vblank and 80 horizontal pixels. This 80 seems to be a standard amount for RBv2. Too many to fit at 336..340 MHz, and then 340 MHz is the upper limit of stable EC32 operation. So I started to experiment with reducing these blanks. There is less problem with vblanks, but when I reduced hblank, the monitor (I think it was Philips 243V) started to lose synchronization. I tried this on several other monitors and left the 76 pixels for hblank, reducing vblank to 12. That is stable on several monitors I tried (several Philips and AOC) . This also works on a Waveshare 1024x600 HDMI touch display - there are the discussion somewhere on USB driver topic as we managed to got the touch data out of it. (and that's why I tried to get this resolution)

### evanh — 2024-02-16 08:34
> @pik33 said: ... This 80 seems to be a standard amount for RBv2.

Ah, maybe that's where I'd got the 80 from earlier.

As for the small vblank value, it worked best for me the way Chip has it with no front porch and only one line for sync.

I'm thinking I need to find docs on how "Variable Refresh Rate" is performed. There's a question mark on how the sync is used. Is sync important at all for VRR signalling or is blanking all that matters? It's possible that the syncs don't even exist in that environment. [...EDIT: FRL / Fixed Rate Link for HDMI 2.1, TMDS for earlier; VRR likely needs FRL; HDMI 2.1 a massive change from 2.0...]

### pik33 — 2024-02-16 08:59
While short vblank works, I didn't want to shorten it too much. The driver is used in the Basic interpreter and the player. Both of these programs use vblank time to do graphics related things. That's why I would prefer to shorten hblank instead of vblank, but my monitors don't like it.

### rogloh — 2024-02-16 09:24
Here's a variant of LineDrawAntiAlias.spin2 that draws/animates some Bezier curve stuff I did a while back using Chip's AA gfx. Uses flexspin, not sure if it works with PNut but it might.
[LineDrawAntiAlias.spin2] 18.9K

### cgracey — 2024-02-16 11:32
> @rogloh said:
> Here's a variant of LineDrawAntiAlias.spin2 that draws/animates some Bezier curve stuff I did a while back using Chip's AA gfx. Uses flexspin, not sure if it works with PNut but it might.

Looks really interesting, but PNut is getting hung up on parameter names conflicting with global names. I will modify it later. Thanks, Roger.

### rogloh — 2024-02-16 12:48
The code I hacked up makes use of this cubic expression (from Wikipedia on Bezier curves) to compute the X,Y co-ordinates from the control points P0,P1,P2,P3 as a function of the parameter t. [...uses integer multiplication with scaling restrictions; CORDIC could be useful...]
![](https://forums.parallax.com/uploads/editor/18/c7ud85c8d2yt.png)

### rogloh — 2024-02-16 13:18
I added some underscores to the conflicting variable names so it might compile now with PNut if I got them all Chip - not sure. Flexspin doesn't care if locals and globals have the same name which is a difference in behaviour with PNut.
[LineDrawAntiAlias.spin2] 19K

### rogloh — 2024-02-16 13:50
Here's another version that uses the CORDIC and is smoother - allowing up to 1024 segments per Bezier curve, and fits better now with your co-ordinate scaling of 8 bits. I think 64 or 128 segments is a nice compromise for this resolution. You could take this PASM and make it into some pixel plotting primitive for Bezier curves.
[LineDrawAntiAlias.spin2] 19K

### cgracey — 2024-02-16 20:45
Very nice!

I made some modifications so it would run under PNut.exe and then made the Bezier lines translucent.
[LineDrawAntiAlias_Bezier.spin2] 19.1K

### rogloh — 2024-02-16 21:14
Cool, this version still works in flexspin now too.

It gives an interesting almost 2D surface effect with the fanned line drawn that you added by moving the x0 and y0 assignments into the inner loop. Also enabling the translucency lets you see the line segments that form the curve where your semicircle ends overlap and are drawn twice. I saw that before also.
You can try reducing the step size in this loop (keep as powers of two) to increase the number of segments drawn.

    repeat t from 0 to 1024 step 8  'step size controls smoothness

With some speeds there's something almost organic watching it move isn't there.

### Wuerfel_21 — 2024-02-17 03:58
Y'all need to post more screenshots, I'm too lazy to dig my edge out :P (or add support for whatever stupid nonsense setup I'm mostly using, which is 96MB EVAL + VGA). [...dumps Processing_PolygonRendering.zip (convex polygon fill w/ perfect fill rule), 3d_render_test_1.zip (all-integer C, PSRAM 320x240 16bpp, vector/matrix math, additive blend), Processing_Minecraft.zip (voxel proof-of-concept)...]
[Processing_PolygonRendering.zip] 1.8K  [3d_render_test_1.zip] 435.4K  [Processing_Minecraft.zip] 73.5K

### rogloh — 2024-02-17 04:25
@Wuerfel_21 Doesn't come across in a static photo so well but... [3 screenshots]

> Uses @rogloh 's memory code, but please fix your video driver. Can't do 320x240 with PSRAM source.

Not sure at which scan rates it applies but my driver may not have time to both pixel double and do external memory accesses as well because the data won't necessarily be returned in time for the doubling operation to happen before this next scan line gets rendered... EDIT: I think line doubling from PSRAM should still work, it's just pixel doubling that gets skipped if external RAM is used.

### cgracey — 2024-02-17 07:26
Thanks for sharing all this stuff, Ada.

And thank you, too, Roger.

### Wuerfel_21 — 2024-02-17 16:29
Looks like a screensaver :+1: Though there's a problem with the end caps being drawn over twice. [...Please don't take what I say too seriously; pixel doubling is tricky; custom driver works out; can even do line quadrupling...]

### cgracey — 2024-02-17 18:33
Here is something needed that is hard to work out:

An efficient anti-aliased curved-line drawer.

### evanh — 2024-02-18 00:09
If you're happy to ignore the older fixed mode monitors and TVs then the newer ones, via their HDMI port, are happy to accept very low res modes. I've tested 640x320 and plenty of other odd-balls. No need to pixel or line double, the monitor/TV has a built-in scan converter for that already. [...tested below 250 MHz min link speed; 4k LG "Out Of Range" above 70 Hz...]

 Sysclock freq = 250 MHz   Dotclock freq = 25.0 MHz
 Hres=640  hfp=53 hsync=64 hbp=53  Htot=810   Hfreq = 30864 Hz
 Vres=320  vfp=59 vsync=2 vbp=60  Vtot=441   Vfreq = 70.0 Hz

### Rayman — 2024-02-18 00:31
> @cgracey said: An efficient anti-aliased curved-line drawer.

It's a good question... Maybe I'd try pretending the bitmap is 16X bigger than it is and instead of setting a pixel to 100% of color value, add 1/16 of the color value to the actual pixel?

### Wuerfel_21 — 2024-02-18 01:18
Interesting. Though that scan converter is often terrible and makes everything super blurry, so doubling in software still wins out in my book. I've figured out how to do it at the same time as encoding audio packets, which already takes up loads of video driver CPU time, so it really isn't so bad.

### evanh — 2024-02-18 02:07
I hate the sharp blocky look in games. And it's not like the blur is degrading text readability either, the pixels are so damn big.

### evanh — 2024-02-18 02:31
The strongest argument is simply that only the commonly used resolutions are recognised by older displays. And only the fixed mode timings are supported by all.

Hell, blanking is everything timing wise in the digital transports. Syncs aren't actually relevant but they're expected anyway and most displays will probably refuse to operate without.

### Wuerfel_21 — 2024-02-18 02:58
Yea, there's a thing such as "too sharp". But doing a 2x integer scale and then going to HD using a smooth scale is an ok middle ground, I feel. For being something that is very cheap to implement, that is. Though some scan converters will make that look awful, too, though.

### rogloh — 2024-02-18 03:19
Here's a snippet of code that makes an animation to show the Bezier curve construction from the four initial control points (two curve endpoints and two points forming their tangents). Add it to Chip's latest code and call it repeatedly to see some random cubic Bezier curves get generated. [...]
![](https://forums.parallax.com/uploads/editor/qu/xc983sm9oxi0.png)

VAR
    LONG xpts[129],ypts[129]
    LONG px0,px1,px2,px3,py0,py1,py2,py3
    LONG mx,my,nx,ny,ox,oy,qx,qy,rx,ry


PRI interp(x1_,y1_,x2_,y2_,t,total) : x_,y_
   x_ := ((total-t) * x1_ + t * x2_)/total
   y_ := ((total-t) * y1_ + t * y2_)/total


PRI show_bezier_curve() | color_,t,i,x_,y_

  single_screen()

  px0 := 480<<8 - (getrnd() +// 100<<8) - 120<<8
  py0 := 370<<8
  px3 := 480<<8 + (getrnd() +// 100<<8) + 120<<8
  py3 := 370<<8
  px1 := px0 - (getrnd() +// 50<<8) - 100<<8
  py1 := py0 - (getrnd() +// 200<<8) - 100<<8
  px2 := px3 + (getrnd() +// 50<<8) - 25<<8
  py2 := py3 - (getrnd() +// 150<<8) + 50<<8
  color_ := getrnd()|$ff ' no transparency

  repeat t from 0 to 128
        flip_screen()
        mx,my := interp(px0,py0,px1,py1,t,128)
        nx,ny := interp(px1,py1,px2,py2,t,128)
        ox,oy := interp(px2,py2,px3,py3,t,128)
        qx,qy := interp(mx,my,nx,ny,t,128)
        rx,ry := interp(nx,ny,ox,oy,t,128)
        x_,y_ := interp(qx,qy,rx,ry,t,128)
        xpts[t]:=x_
        ypts[t]:=y_
        smoothline(px0,py0,px1,py1,$100,$7f7f7fff)
        smoothline(px1,py1,px2,py2,$100,$7f7f7fff)
        smoothline(px2,py2,px3,py3,$100,$7f7f7fff)
        smoothline(mx,my,nx,ny,$100,$407f00ff)
        smoothline(nx,ny,ox,oy,$100,$407f00ff)
        smoothline(nx,ny,ox,oy,$100,$407f00ff)
        smoothline(mx,my,mx,my,$480,$407f00ff)
        smoothline(nx,ny,nx,ny,$480,$407f00ff)
        smoothline(ox,oy,ox,oy,$480,$407f00ff)
        smoothline(qx,qy,rx,ry,$100,$30007fff)
        smoothline(qx,qy,qx,qy,$480,$30007fff)
        smoothline(rx,ry,rx,ry,$480,$30007fff)
        smoothline(x_,y_,x_,y_,$480,color_)
        if t<>0
           repeat i from 0 to t-1
                smoothline(xpts[i],ypts[i],xpts[i+1],ypts[i+1],$280,color_)
      flip_screen()
      waitms(1000)

### evanh — 2024-02-18 04:13
Good read. I've never tried to get to grips with Bezier Curves before.

PS: In the process of trying see how the source code fit the animation I bumped into a typo. You've got a duplicate line draw running twice. I've commented it out.
[annotated smoothline listing with the duplicate green line commented out]

### rogloh — 2024-02-18 04:28
Thanks, must have been a cut-paste error.

Right now I'm looking into some font glyph data which is typically a list of quadratic or cubic Bezier control points for different contours of a character glyph in a font. [...whole font instruction processor, its own language...]

### rogloh — 2024-02-18 13:24
I was able to extract the font data points from a TTF file using SPIN2 as a proof of concept - see attached file for some rudimentary TTF font parsing to extract glyph data. [...relative X,Y deltas per contour, on-curve vs control-point flags, multiple contours per glyph; ComicSans TTF fits in HUB RAM; larger fonts could load into PSRAM...]
[font.spin2] 11.1K

### rogloh — 2024-02-18 13:47
LOL, first attempt at a curve...gotta laugh. [...EDIT: bit better but problem near end of contour transitioning to other contour...]

### cgracey — 2024-02-18 14:47
![](https://forums.parallax.com/uploads/editor/c2/0i7lkhabz3mb.jpg)

That is very interesting, Roger.

I have added text to my anti-alias stuff. In this demo, I started to add your Bezier in, too, but then I realized there were modifications to the line draw and I was too tired to sort it out. So, it's just the text for now.

This font's pitch is 9x16 pixels and it's anti-aliased. It blends onto the background quite nicely. Here is some code with color sweeps.

### rogloh — 2024-02-19 08:48
Got some Parallax TTF font parsing and display working with Chip's AA gfx code. [...scale outlines up/down; kerning not right yet; flood fill between contours best pre-rendered...]
![](https://forums.parallax.com/uploads/editor/09/ujhj4046x7p0.png)

### cgracey — 2024-02-19 15:37
I think the way you could make screen fonts would be to render each character at high resolution in on/off pixels, and then reduce it to dithered pixels by gridding it and counting on/off pixels to get greyscale/blend pixels.

### Wuerfel_21 — 2024-02-19 15:50
That's kinda how (good) terminal programs on PC work. The vector font rendering libraries are butt-slow, but if you cache every character the first time it comes up, you can just draw these pre-rendered tiles very quickly. This idea normally only ends up being used for monospace terminal displays on account of all the advanced stuff that gets bypassed (kerning, ligatures, etc)

---

## Page 3

### SaucySoliton — 2024-02-19 18:05
I was looking into the Parallax bitmap font and made an observation that could reduce the storage requirements of rendered fonts. Background: In order to display a high definition picture through the RF input of a TV, the image will need to be MPEG encoded. [...macroblocks, DCT/quantization/entropy coding once and cache; font is 16x32 = 2 macroblocks; 1bpp source becomes 8bpp when rendered; 8x8 block dedup halves storage...]

Characters  8x8 blocks   Unique  Storage   Font Contents
 32 - 127       768        340      44%    Printable ASCII
 32 - 255      1792        434      24%     + Accents
  0 - 127      1024        464      45%     + Window decorations
  0 - 255      2048        553      27%     All

### evanh — 2024-02-19 22:50
> @cgracey said: This font's pitch is 9x16 pixels and it's anti-aliased...

I just realised that's a 2 MB screen buffer! No wonder it needs the external RAM chips. The antialiasing does look real sweet on the fonts.

### rogloh — 2024-02-19 23:14 (edited 2024-02-20 01:56)
Can the nice background stay put while the text screen scrolls above it? [...bandwidth analysis: (960 * 4 * (548 * 60)) * 3 Bytes/sec = 379MB/s, too much; 30Hz might; EDIT: video driver could render text over PSRAM background on the fly like sprites; ~10 P2 clocks per pixel at 320MHz...]

### evanh — 2024-02-20 06:11
Could probably do it as an overlay of the two buffers merged on the fly. _Only_ needs double bandwidth then.

### rogloh — 2024-02-20 06:19 (edited 2024-02-20 08:40)
Here's the font stuff put into Chip's demo with the quadratic Bezier curves added. I only tested with flexspin but hopefully it might still run with PNut the way I coded it. TBD. Also, it might be slower to process the data in PNut vs flexspin as much of the work is coded in SPIN2.
![](https://forums.parallax.com/uploads/editor/jr/74haj60e220w.png)
[fonttest.zip] 38.6K

### cgracey — 2024-02-20 15:14 (edited 2024-02-20 15:16)
> @rogloh said:
> Here's the font stuff put into Chip's demo with the quadratic Bezier curves added...

So, what you are showing is that TTF's are points with Bezier curves, mainly. Is that right? I remember they allow some kerning rules and fixed typefaces for lower-res fonts, as well.

In your estimation, does the TTF format look pretty efficient or is it kind of bloated? It's really tempting to use TTF's if they can be small enough.

I will try to run your code soon to see what it does.

### Wuerfel_21 — 2024-02-20 16:23 (edited 2024-02-20 16:23)
If it's too bloated, one could just convert it to a custom format. Some preprocessing is neccessary, anyways, if you want to use just any font, since many halfway competent fonts will have tens of MBs of various unicode characters (mostly CJK).

### rogloh — 2024-02-20 21:13 (edited 2024-02-20 23:52)
Yeah quadratic Bezier curves. Some other font formats may use the cubic ones. [...TTF raw contour data is efficient (compression + deltas); one flag byte per X,Y delta with on-curve/control-point bit, repeat flag, 8-bit deltas with sign bits (or optional signed 16-bit), zero deltas not stored, intermediate on-curve points omitted; pre-process to save re-parsing; flood-fill rasterization needs per-scanline sorting/interpolation and lots of temp storage...]
![](https://forums.parallax.com/uploads/editor/s8/bd0h0it6gjwe.png)

### Tubular — 2024-02-20 21:16
Amazing to see TTF fonts rendered by the P2

I've been meaning to hook a P2 up to the big laser and do something real/live with gcode generation. A 'laser typewriter' could be a good starting point

### rogloh — 2024-02-20 22:54
Yeah Tubular I was thinking about your laser and gcode. Or maybe even your robot arm. Add a paintbrush to the end of it and make a real "Paint" program. :wink:

### rogloh — 2024-02-23 04:00 (edited 2024-02-23 04:24)
Worked on a flood fill operation for TT outline fonts using a coordinate sorting method today. [...not 100% correct for some curves; slow at bigger sizes; up to 10 longs per scanline (540) ~21kB; ideas: draw outline into PSRAM then readback to HUB; use spare bits above 24bpp to mark span start/stop...]
![](https://forums.parallax.com/uploads/editor/83/m71yz9wkh7a8.png)

### Rayman — 2024-10-14 21:54
@cgracey Is this code posted here? I can't seem to find it. Or, is the font rendering just a call to SmoothPixel() for every pixel in the font?

### Rayman — 2024-10-14 23:40
Looks like this is the part need to get a handle on:

                setpiv  plot_color              'blend background pixel with new pixel
                blnpix  pa,plot_color

Appears that plot_color must be encoded as RGBA as setpiv just uses the lower 8 bits. So, setpiv is setting the alpha factor to be used. Then, blnpix uses that alpha and the two colors in pa and plot_color to create a new color in pa. Guessing this ignores the alpha in pa...

### rogloh — 2024-10-14 23:56
Yeah it doesn't use those lower 8 bits directly for transparency. They are used in the prior instruction. The pixel effects are cool but only really usable in 32bpp mode or LUMA modes or if you convert back and forth using RGBSQZ/RGBEXP from 16 bit mode which adds overhead. Maybe you could use them with LUT 256 if you have a gradient in LUT for example. I think these pixel instructions would have benefitted from different M values per byte (possibly via a prior SETQ). Then you could have used them for transparency with 8 bit modes on a per pixel basis or to accelerate 8 bit sprite stuff, but MUXQ can still be used for that.

### Rayman — 2024-11-04 22:35
I'm thinking this is very useful for drawing some GUI elements, like dials and clocks. Will probably target PSRAM buffer eventually, but might look to see if can hijack this for 256-color VGA mode where 16 palette colors represent 4-bit alpha transition between two colors. Also, this HDMI mode is interesting, have to see how well it works on my monitors...

### Rayman — 2024-11-05 14:58
@rogloh Guess I could use code that draws circular arcs with antialiasing. Guess your code here can do that?

### rogloh — 2024-11-05 19:30
Yes that code I posted a while back can compute/draw arcs with Bezier curves and cubic or quadratic interpolation but I didn't do the anti-aliasing part. That is all Chip's stuff.

### Rayman — 2024-11-05 22:37
My test TV won't take the signal... But, this was with Prop Tool, maybe I need PNUT? Guess I'll try that. Chip's spiral code works, so know setup is OK. Dug out a 32MB PSRAM Edge module for this. At first, module wouldn't work at all. But then, saw need to flip some tiny switches to make it work :(

### Rayman — 2024-11-05 22:42
Ok, PNUT doesn't make it work either... Think I'll change the code to 640x480 and see if that works...

### Rayman — 2024-11-05 22:49
Ok, just changed the resolution constants to 640x480 and it works.
[LineDrawAntiAlias - Archive ...zip] 12.2K  [VGA_Res_Anti.png] 240K

### Rayman — 2024-11-16 21:45
Moved the graphics routines into a separate cog. Hopefully, can be beginning of an anti-aliased GUI. Also, hope to be able to use with FlexProp this way... Rigged PSRAM driver for Platform board, but it's easy to switch back to Edge 32 MB in OBJ section...
[LineDrawAntiAlias_RJA_Platform_2a ...zip] 13.2K

### Rayman — 2024-11-16 23:19
Was hoping a very short line would make a circle, but no such luck

### Rayman — 2024-11-18 21:36
Now adapted for VGA. Can use either Edge 32MB module or Platform/SimpleP2 boards with PSRAM. This is with graphics moved to it's own cog. [...double buffering in PSRAM; refresh 5-10 fps; good enough for GUI, maybe 320x240 gaming...]
[LineDrawAntiAlias_Cogged_2a ...zip] 18.6K

### Rayman — 2024-11-25 22:33
Looking into changing it from 24-bit to 16-bit. 24-bit looks more efficient because it's the natural quanta of the PSRAM. 16-bit mode pixel operations mean figuring out which word to use, using RGBEXP and then using RGBSQZ, then setting the right word with the result. So, going to add 8 or so instructions to the setpixel call. The advantage is that doing simple buffer copy operations can be twice as fast... So, video can be 3X faster...

### evanh — 2024-11-26 05:45 (edited 2024-11-26 05:47)
If the display buffer is always 32-bit aligned then even horizontal pixel positions are also the even sub-addressing.

### Rayman — 2024-11-29 17:37 (edited 2024-11-29 17:54)
Finally got 16bpp version of this working. Took forever to figure out that can't set Z or C flags. Added this to the end and all good now:
`modcz _clr,_clr wcz 'Need to clear CZ!!!`
This is VGA and should work on Edge 32MB with a change in the OBJ section. Maybe should get the HDMI version working in 16bpp one day...
[LineDrawAntiAlias_Cogged_2a_16bpp ...zip] 156.5K

### Rayman — 2024-11-30 19:04
Added anti-aliased circles to the mix, based on code from here, converted to assembly:
https://github.com/Versa-Design/Antialiased_Circle
Still need to work on 16-bit HDMI...
[IMG_3829.jpg] 198.9K  [LineDrawAntiAlias_Cogged_2b_16bpp ...zip] 160.1K

### refaQtor — 2024-12-27 08:16
I like what you've got going on here. I only had HDMI AddOn boards on my bench. I just ordered a couple VGA AddOn boards so I can get this (your) code going on my bench. I will certainly get to using them in any case.
