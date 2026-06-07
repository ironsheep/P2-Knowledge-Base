```{=latex}
% Banner image at top (full width) with drop shadow for visual balance
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
\vspace{0.6cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Single-Step Debugger Manual\par}
\vspace{0.3cm}
{\Large\itshape Observe and Control Your Running P2 Code\par}
\vspace{0.6cm}
{\large May 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Manual Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{A teaching guide to the P2 single-step debugger}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Getting Started}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item What Single-Step Debugging Is
\item Turning On Debugging
\item The Debugger Window
\item Your First Session
\item Commands and Controls
\end{itemize}
\end{minipage}%
\begin{minipage}[t]{0.45\textwidth}
\textbf{Working With the Debugger}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Breakpoints
\item Observing State
\item Working Sessions
\item DEBUG Display Windows
\item Tips and Troubleshooting
\item Appendix: Feature by Version
\end{itemize}
\end{minipage}

\end{tcolorbox}
\vspace{0.5cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
\listoffigures
\clearpage
```

# Copyright and License

Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made (for example, formatting or excerpting).
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, translate, or build upon the material, you may not distribute the modified material.

**Commercial use:** For uses that may be commercial (including paid courses, kits, or redistribution with products), please contact Iron Sheep Productions, LLC and Parallax Inc. (info@ironsheep.biz) for separate permission.

To view the full license, visit: https://creativecommons.org/licenses/by-nc-nd/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

```{=latex}
\clearpage
```
