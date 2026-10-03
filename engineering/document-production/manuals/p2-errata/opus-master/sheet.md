```{=latex}
\pagestyle{empty}
\begin{center}
{\fontsize{26}{30}\selectfont\bfseries \DocTitle\par}
\vspace{0.15cm}
{\large\itshape \DocSubtitle\par}
\vspace{0.15cm}
{\normalsize \DocDate\ \textperiodcentered\ {\color{blue}Version \DocVersion}\par}
\vspace{0.1cm}
{\normalsize\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-10-03\par}
\vspace{0.1cm}
{\scriptsize Copyright \textcopyright\ 2026 Iron Sheep Productions, LLC and Parallax Inc. Licensed under CC BY-SA 4.0 (\url{https://creativecommons.org/licenses/by-sa/4.0/}). Parallax, Propeller, Spin and the Parallax logo are trademarks of Parallax Inc.\par}
\end{center}
\vspace{0.2cm}
```

This sheet lists the silicon errata of the Propeller 2 found so far, and for each one, who meets it, what it looks like and what to do. Each erratum has the same number and the same summary in the guide *P2 Errata*, which explains it, prints a workaround proven on P2 hardware, and says how it was confirmed. Every erratum here was confirmed on Rev C silicon. Erratum numbers are permanent.

# Which errata can affect your program {#sh-which}

<!-- include: shared-triage.md -->

# Find an erratum by symptom {#sh-symptoms}

<!-- include: shared-symptoms.md -->

# The errata {#sh-errata}

## Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#sh-e1}

<!-- include: shared-e1.md -->

## Erratum E2: An Immediate ALTx Takes a Pending AUGS {#sh-e2}

<!-- include: shared-e2.md -->

## Erratum E3: GETCT Returns a Stale Upper Long {#sh-e3}

<!-- include: shared-e3.md -->

## Erratum E4: GETXACC Clears Only During a Goertzel Burst {#sh-e4}

<!-- include: shared-e4.md -->

## Erratum E5: The Goertzel Accumulators Trail by One Clock {#sh-e5}

<!-- include: shared-e5.md -->

## Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#sh-e6}

<!-- include: shared-e6.md -->

## Erratum E7: After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early {#sh-e7}

<!-- include: shared-e7.md -->
