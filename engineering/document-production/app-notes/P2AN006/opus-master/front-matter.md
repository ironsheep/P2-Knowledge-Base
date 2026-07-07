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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN006\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Sizing Cog \& Task Stacks\par}
\vspace{0.25cm}
{\Large\itshape Give every cog and task exactly the stack it needs — and catch an overflow before it corrupts memory\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 1.0.0\par}

\vspace{0.25cm}
% App-note cover box: repurposes the manuals' bottom-of-cover content table.
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
\textbf{A repeatable way to size the stack buffer every cog and task needs — and a drop-in utility that turns a silent stack overflow into a clear, halted error message.}

\vspace{0.10cm}
{\footnotesize
One shared idea — fill a stack with a known pattern and watch a sentinel just
past its end — then a small catalog of recipes you choose among by need:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{R1 — instrument a new-cog stack} — guard a \texttt{cogspin} worker against overflow
\item \textbf{R2 — find the high-water mark} — measure real usage, then right-size
\item \textbf{R3 — pinpoint the culprit} — localize which routine overran the stack
\item \textbf{R4 — size a task stack} — the same technique on an intra-cog \texttt{taskspin} task
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut (v47+ for the task recipe)
\textbullet{} P2 Edge or P2 Eval board; every recipe reports over DEBUG.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
