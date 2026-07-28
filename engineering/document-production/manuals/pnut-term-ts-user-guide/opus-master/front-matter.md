```{=latex}
% ISP cover standard (p2kb-platform-isp-cover): maroon 5:1 band inset to the
% text block, trace field at the right, Iron Sheep mark alone bottom-right.
% This is an Iron Sheep Productions-only document — NO P2 Knowledge Base
% banner, no Parallax mark, no affiliation line.
\ispcoverband{PNut-Term-TS}{Downloader · Terminal · Debug Display}

\begin{center}
\vspace{1.4cm}
{\fontsize{34}{40}\selectfont\bfseries PNut-Term-TS User Guide\par}
\vspace{0.35cm}
{\Large\itshape The Cross-Platform Downloader, Terminal,\\ and Debug Display for the Propeller 2\par}
\vspace{0.9cm}
{\large July 2026\par}
\vspace{0.15cm}
{\large\color{blue}Version 0.1.0 (draft)\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Guide Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{A practical guide to operating PNut-Term-TS}

\vspace{0.3cm}
\begin{minipage}[t]{0.46\linewidth}
\textbf{Getting Oriented \& Using the GUI}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Where It Fits, and the Fork
\item The Main Window
\item Downloading \& Running
\item The Serial Terminal
\item Debug Windows \& Placement
\item The Single-Step Debugger
\item Menus, Settings, Devices
\item Further Features
\end{itemize}
\end{minipage}\hfill
\begin{minipage}[t]{0.46\linewidth}
\textbf{Headless \& Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Running Headless
\item Ending a Run Cleanly
\item The Log as Feedback Loop
\item A Complete Automated Run
\item Command-Line Reference
\item Keyboard Shortcuts
\item Troubleshooting
\item Support \& Resources
\end{itemize}
\end{minipage}

\end{tcolorbox}
\end{center}

% The Iron Sheep mark stands alone bottom-right — it replaces the old
% publisher/affiliation text lines (ISP-only document, no KB affiliation).
\vfill
\ispcovermark

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
\listoffigures
\clearpage
```

```{=latex}
% ISP copyright page — the mark carries the page that makes the ownership claim.
% Deliberately NOT a \chapter: \chapter forces a page break, which would strand
% the mark alone on the preceding page. The TOC entry is added by hand so the
% page still lists as "Copyright and License".
\ispcopyrightmark
\addcontentsline{toc}{chapter}{Copyright and License}
\markboth{Copyright and License}{}
\vspace{0.5cm}
{\Large\bfseries Copyright and License\par}
\vspace{0.4cm}
```

Copyright © 2026 Iron Sheep Productions, LLC.

PNut-Term-TS is © 2024–2026 Iron Sheep Productions, LLC and is licensed under the MIT License.

This user guide is licensed under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made (for example, formatting or excerpting).
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, translate, or build upon the material, you may not distribute the modified material.

**Commercial use:** For uses that may be commercial (including paid courses, kits, or redistribution with products), please contact Iron Sheep Productions, LLC (info@ironsheep.biz) for separate permission.

To view the full license, visit: https://creativecommons.org/licenses/by-nc-nd/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

```{=latex}
\clearpage
```
