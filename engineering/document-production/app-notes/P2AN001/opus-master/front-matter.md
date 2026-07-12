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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN001\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Measure an Absolute Voltage in Microvolts on a P2 Pin\par}
\vspace{0.25cm}
{\Large\itshape No external ADC — a single-pin instrumentation ADC and a catalog of techniques\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 1.0.2\par}

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
\textbf{Read an absolute voltage, in microvolts, on a single P2 pin — with no external converter.}

\vspace{0.10cm}
{\footnotesize
A single-pin instrumentation ADC that streams a live microvolt reading to a DEBUG
scope window, verified on the bench with one jumper wire — then a small catalog of
techniques you choose among by what your project needs:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{Base build} — single-pin absolute microvolts (the foundation)
\item \textbf{Three pins} — constant impedance for lower noise in the same time
\item \textbf{Filter cascade} — every rate-vs-resolution trade available at once
\item \textbf{Range extension} — read voltages above 3.3\,V with one resistor
\item \textbf{Mains averaging} — null 50/60\,Hz pickup for free
\item \textbf{The ceiling} — eight channels via a bytecode interpreter (reference)
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut, current release
\textbullet{} P2 Edge or P2 Eval board, plus one jumper wire.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
