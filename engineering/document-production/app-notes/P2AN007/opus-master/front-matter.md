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
{\large\scshape Propeller 2 \textbullet{} Application Note P2AN007\par}
\vspace{0.30cm}
{\fontsize{30}{36}\selectfont\bfseries Data Structures with the New Language Facilities\par}
\vspace{0.25cm}
{\Large\itshape Spin2 STRUCT for in-cog records — and the worked code for sharing them safely across cogs\par}
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
\textbf{Real data structures on the P2 — a typed record with the Spin2 STRUCT facility, and three worked ways to move those records safely between cogs.}

\vspace{0.10cm}
{\footnotesize
One shared idea — a STRUCT is a packed, named record; sharing it across cogs
is about publishing it atomically — then a catalog of recipes you choose among
by how the data flows:

\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=3pt]
\item \textbf{R1 — in-cog record + array} — declare, fill, copy, and size a STRUCT
\item \textbf{R2 — lock-free ring buffer} — one producer, one consumer, no lock
\item \textbf{R3 — latest-wins mailbox} — a command block published with a sequence counter
\item \textbf{R4 — locked multi-writer queue} — many writers, one hardware lock
\item \textbf{R5 — a whole record in one long} — member bitfields; the publish IS the payload
\item \textbf{R6 — raw addressing with OFFSETOF} — computed offsets, never hand-counted
\end{itemize}

\vspace{0.05cm}
\textbf{Applies to:} P2 (Propeller 2) silicon \textbullet{} Spin2 / PNut v45 or later (STRUCT;
R6 needs v53, R5 needs v54) \textbullet{} P2 Edge or P2 Eval board; every recipe reports over DEBUG.
}
\end{tcolorbox}
\vspace{0.10cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}
```
