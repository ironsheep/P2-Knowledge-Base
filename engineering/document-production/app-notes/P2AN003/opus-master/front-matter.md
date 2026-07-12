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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN003\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Generate Analog Waveforms and Audio on a P2 Pin\par}
\vspace{0.25cm}
{\Large\itshape No external DAC — sample playback, synthesis, dithering, and mixing, straight from the smart pin\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 1.0.1\par}

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
\textbf{Turn a single P2 pin into a 16-bit audio DAC — playing samples, synthesizing waveforms, and mixing channels, with no converter chip.}

\vspace{0.10cm}
{\footnotesize
A shared output stage — configure the dithered DAC, pace it from the smart pin's
own sample clock — then a small catalog of recipes you choose among by what your
project needs:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{Sample playback (DDS)} — resample a stored buffer to any pitch
\item \textbf{Waveform synthesis} — sine, sawtooth, and triangle from the phase
\item \textbf{Dithering} — trade the 8-bit DAC up to clean 16-bit resolution
\item \textbf{ADC \textrightarrow{} DAC passthrough} — a live analog wire through the chip
\item \textbf{Mixing \& panning} — sum many voices to a stereo pair of pins
\item \textbf{The ceiling} — a 32-stream software mixer (reference)
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut, current release
\textbullet{} any P2 board, plus an RC filter or a headphone jack to hear the output.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
