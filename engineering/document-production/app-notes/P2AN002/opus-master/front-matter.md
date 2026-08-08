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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN002\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries CORDIC for Real Work\par}
\vspace{0.25cm}
{\Large\itshape Rotations, distances, headings, and transcendentals from the P2's hardware math solver\par}
\vspace{0.35cm}
{\large August 2026\par}
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
\textbf{Compute rotations, distances, headings, and trig on the P2 — in a few cycles, with no math library.}

\vspace{0.10cm}
{\footnotesize
A shared foundation — queue an operation, do other work, retrieve the result — then a
small catalog of recipes you choose among by what your project needs:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{Distance \& heading} — cartesian-to-polar in one operation (the navigation primitive)
\item \textbf{Rotate a point} — coordinate rotation about the origin
\item \textbf{Draw a circle} — polar-to-cartesian, plotted live in a DEBUG window
\item \textbf{Sine \& cosine} — waveform synthesis straight from the angle
\item \textbf{Fixed-point scale \& magnitude} — 64-bit-safe multiply/divide, log and exp
\item \textbf{Pipeline for throughput} — overlap operations for one result every eight clocks
\item \textbf{The ceiling} — three-phase motor control as coordinate rotations (reference)
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut, current release
\textbullet{} any P2 board, with a DEBUG window and no extra hardware.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
