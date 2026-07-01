# Raw Capture — "Problem discovered in the streamer's Goertzel SINC2 mode!!"

Source: https://forums.parallax.com/discussion/176065/problem-discovered-in-the-streamers-goertzel-sinc2-mode
Thread ID: 176065
Fetched: 2026-07-01
Pages: 1 (page /p2 returns HTTP 404 — single-page thread)

---

## Page 1

### cgracey — 2024-12-16 10:48 (edited 2024-12-16 10:50)

I have been experimenting with software-defined-radio ideas and I just found a problem with the streamer's Goertzel SINC2 mode.

When the number of clocks varies from the norm to complete a full NCO cycle, the X and Y values coming from GETXACC will be off by one double integration and it will corrupt the computed sample, along with the next one, before correcting.

The fix is to only use Goertzel SINC2 mode with a power-of-two iteration count. For example, if you run at 256 MHz and are measuring for 1 MHz, that will always take 256 clocks per Goertzel cycle, so you have consistency in the SINC2 double-integration process.

I made this note in the silicon doc:

NOTE ABOUT GOERTZEL SINC2 MODE (2024.12.16)
It has just been discovered that the SINC2 mode generates periodic problematic GETXACC readings when the number of iterations in a Goertzel cycle varies, due to SETXFREQ's D being a non-power-of-two value. The above example code was modified so that the clock frequency is now 256 MHz, instead of 250 MHz, so that the 1MHz being listened to will always take 256 clocks per Goertzel cycle. This causes the double-integrating accumulators in SINC2 mode to always have the same number of iterations before a GETXACC instruction executes and captures the double accumulations. Being off by a single clock cycle will corrupt the current and next samples.

---

### cgracey — 2024-12-16 10:54 (edited 2024-12-16 10:59)

@SaucySoliton, you were probably experiencing this problem and maybe didn't realize what was going on. This could have been causing periodic noise in your analog video measurements. It happens on the order of 30-60ms per error.

The fix would be to run at some power-of-two frequency above the frequency you are analyzing, or just stick with SINC1 mode.

If you want to simulate 1 clock of jitter before doing a GETXACC, just do a 'WAITX #1 WC' beforehand and you will get huge noise in your readings.

If you always start with XZERO, instead of XCONT, and your measurement period is under 20ms, you may be fine using SINC2 in the Goertzel.

---

### ozpropdev — 2024-12-17 05:54

Good to know Chip. Thanks for the head's up.
