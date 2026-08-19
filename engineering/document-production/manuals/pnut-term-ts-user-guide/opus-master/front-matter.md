```{=latex}
% ISP cover standard (p2kb-platform-isp-cover): maroon 5:1 band inset to the
% text block, trace field at the right, Iron Sheep mark alone bottom-right.
% This is an Iron Sheep Productions-only document — NO P2 Knowledge Base
% banner, no Parallax mark, no affiliation line.
\ispcoverband{PNut-Term-TS}{Downloader · Terminal · Debug Display}

\begin{center}
\vspace{1.4cm}
{\fontsize{34}{40}\selectfont\bfseries \DocTitle\par}
% 0.69cm not 0.35cm: the minipage below sets its own first baseline, which
% consumed 9.5pt of this gap (measured v1 vs v2 on the daemon, 20.8pt -> 11.3pt).
\vspace{0.69cm}
% Subtitle measure is PRESENTATION and stays here; the TEXT is single-sourced
% (\DocSubtitle from request.json). Narrowing the measure balances the two-line
% break — at full width it breaks after "for the" and orphans "Propeller 2".
{\Large\itshape\begin{minipage}{0.66\linewidth}\centering \DocSubtitle\end{minipage}\par}
\vspace{0.9cm}
{\large \DocDate\par}
\vspace{0.15cm}
{\large\color{blue}Version \DocVersion\par}

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

\clearpage

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
% \phantomsection is REQUIRED before a hand-added TOC line: without an anchor of
% its own, hyperref points the entry at the last anchor it saw -- the document
% start -- so the bookmark and the TOC link both jumped to the cover instead of
% this page. (Verified in the 2026-08-08 pre-release check: entry targeted p1,
% section lives on p5.)
\phantomsection
\addcontentsline{toc}{chapter}{Copyright and License}
\markboth{Copyright and License}{}
\vspace{0.5cm}
{\Large\bfseries Copyright and License\par}
\vspace{0.4cm}
```

Copyright © 2026 Iron Sheep Productions, LLC.

PNut-Term-TS is © 2024–2026 Iron Sheep Productions, LLC and is licensed under the MIT License.

This user guide is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC.

```{=latex}
\clearpage
```
