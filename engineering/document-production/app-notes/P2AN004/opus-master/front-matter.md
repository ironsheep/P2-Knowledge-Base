```{=latex}
% Banner image at top (full width) with drop shadow — same cover artwork as the
% manual family, for visual consistency across the P2 document set.
\begin{tcolorbox}[
  enhanced,
  boxrule=1.5pt,
  colframe=gray!60,
  colback=white,
  drop shadow southeast,
  shadow={3pt}{-3pt}{1mm}{black!15},
  left=0pt, right=0pt, top=0pt, bottom=0pt,
  width=\textwidth,
  arc=0pt,
  outer arc=0pt
]
\includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
\end{tcolorbox}

\begin{center}
\vspace{0.35cm}
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN004\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Read Real-World Sensors by Frequency, Period, and RC Timing on a P2 Pin\par}
\vspace{0.25cm}
{\Large\itshape Three smart-pin instruments that turn a transducer into a number — no external counter or ADC\par}
\vspace{0.35cm}
{\large June 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 0.1.0 (draft)\par}

\vspace{0.25cm}
% App-note cover box: repurposes the manuals' bottom-of-cover content table.
% A manual lists Parts/Chapters here; an app note has neither, so this box
% carries the app-note's actual job instead — the outcome + the techniques.
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} What You'll Build},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Read a resistive, capacitive, light, or rotary sensor directly on a P2 pin — the smart pin does the measuring, the cog just reads the answer.}

\vspace{0.10cm}
{\footnotesize
One shared idea — let a smart pin time or count the signal so the cog never has
to — then a small catalog of sensor recipes you choose among by what you are
reading:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{R1 — RC-decay reader} — read a photocell, thermistor, or pot by timing a capacitor's discharge
\item \textbf{R2 — light-to-frequency reader} — turn a TSL235R's frequency into an irradiance value
\item \textbf{R3 — quadrature-knob instrument} — a drop-in encoder knob with range clamp, preset, and a debounced button
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut, current release
\textbullet{} P2 Edge or P2 Eval board; R3 self-tests with two jumper wires.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
