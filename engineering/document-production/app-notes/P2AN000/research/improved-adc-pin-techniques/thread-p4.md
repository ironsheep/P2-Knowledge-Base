# Improved ADC Pin Techniques — Parallax Forum Thread (Page 4 of 4)

**Source:** https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques/p4
**Captured:** 2026-06-27 via WebFetch.
**Note:** Page 4 is entirely BLDC/PMSM motor-commutation theory — a tangent that grew out of
SaucySoliton's motor-driver use case (p3 Post 21+). No new P2 ADC technique or code here.
Captured for completeness; **not** core to the ADC app note.

---

## Post 1 — tritonium — 2024-04-07 09:53
Hi. This is a good explanation — if you can get your head around it... https://www.ti.com/lit/ml/slyp711/slyp711.pdf  — dave

## Post 2 — evanh — 2024-04-07 11:54 (edited 11:56)
Erna, thank you very much. The following really helped me grok it better: "So the motor is designed to keep the torque constant over 60°. DC has no phase angle. There is just one closed loop running one current. If you switch the loop from phase to phase, that doesn't make DC an AC."

That implies there was a concerted effort to design the structural layout of the windings and magnets, to keep it steady through that 60° segment, for the purpose of making the motor phase management electronically as simple as possible.

I presume the trapezoidal labelling just comes from the current waveform to energise and de-energise the windings of each segment. ie: The voltage switchover can be a sharp box shape.

## Post 3 — ErNa — 2024-04-07 12:28 (edited 12:45)
> @tritonium said: [TI PDF link]

Let me say it this way: It is the state of the art. And if we remember: Chip made the Propeller different, as the state of the art is just old wine in new bottles. If anybody is interested in finding the rotor position at standstill he may digest the attached document ;-)
**Attachment:** US2011050209A1-1.pdf (779.8K) — patent on standstill rotor-position detection. URL: https://forums.parallax.com/uploads/editor/4l/0nfe9qk0x7pv.pdf (patent doc; not downloaded — off-topic for ADC)

## Post 4 — ErNa — 2024-04-07 12:40 (edited 12:52)
[detailed BLDC commutation theory: current is constant and commuted phase-to-phase; "trapezoidal" refers to the phase voltage profile (positive 120° / open 60° / negative 120°); the floating pin is a sensor output, not a voltage; motor constant links BEMF/rotation and torque/amp.]
[Image: current waveform diagram]

## Post 5 — evanh — 2024-04-07 13:50 (edited 13:59)
[agrees, references the TI PDF; notes industrial servo motors went AC (PMSM + resolver feedback) decades ago.]

---

*End of Page 4 capture — thread ends here. Last post 2024-04-07.*
