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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN005\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Cooperative Multitasking with Spin2 TASK Methods\par}
\vspace{0.25cm}
{\Large\itshape Run several jobs in one cog — the TASK methods that retire the hand-coded coroutine\par}
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
\textbf{Several cooperative jobs sharing one cog — launched, yielded, halted, resumed, and shut down cleanly, all through Spin2's TASK methods instead of a hand-written PASM coroutine.}

\vspace{0.10cm}
{\footnotesize
One shared idea — a task runs until it voluntarily yields, so several jobs
take turns inside a single cog — then a small catalog of recipes you choose
among by what you need:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{R1 — two-task round-robin} — two independent blinkers from one cog
\item \textbf{R2 — cooperative yield} — a long computation that keeps a second job responsive
\item \textbf{R3 — halt / resume flow control} — a consumer that pauses and wakes its producer
\item \textbf{R4 — task dashboard} — a live census of every slot, and a clean shutdown
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut v47 or later
\textbullet{} P2 Edge or P2 Eval board; every recipe runs and reports over DEBUG.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
